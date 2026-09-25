#!/usr/bin/env python3
"""Public evidence checks; does not assert live analyzer availability."""
from datetime import datetime, timezone
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[1]


def validate_status(status, published, now):
    if status != published:
        raise ValueError('Root and published status copies disagree')
    schema = json.loads((ROOT / 'docs/schemas/product-status.schema.json').read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(status)
    if status['status'] == 'limited-beta':
        payment = status['payment']
        if not status['endpoint_publicly_callable'] or payment['enabled'] is not True or payment['terms_status'] != 'current':
            raise ValueError('Active paid beta requires explicit current terms and availability')
        expiry = datetime.fromisoformat(payment['test_ends'].replace('Z', '+00:00'))
        verified = datetime.fromisoformat(status['last_verified']).replace(tzinfo=timezone.utc)
        if now >= expiry:
            raise ValueError('Active availability terms have expired')
        age = (now - verified).total_seconds()
        if not 0 <= age <= 7 * 86400:
            raise ValueError('Active availability verification must be within seven days, not future-dated')
    elif status['payment']['enabled'] is True:
        raise ValueError('Non-active availability must not advertise enabled payment')


def validate_report(report):
    schema = json.loads((ROOT / 'docs/schemas/analysis-report.schema.json').read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(report)
    findings = report['findings']['findings']
    contributions = report['risk_score']['contributions']
    ids = [f['rule_id'] for f in findings]
    contribution_ids = [c['rule_id'] for c in contributions]
    if len(set(ids)) != len(ids) or len(set(contribution_ids)) != len(contribution_ids) or set(ids) != set(contribution_ids):
        raise ValueError('Finding and contribution rule references disagree')
    if report['risk_score']['total'] != min(100, sum(c['points'] for c in contributions)):
        raise ValueError('Score contribution arithmetic disagrees')
    evidence = {i['category']: set(i['evidence']) for i in report['indicators']['indicators']}
    for finding in findings:
        category = finding['rule_id'].removeprefix('suspicious.')
        if not set(finding['evidence']) <= evidence.get(category, set()):
            raise ValueError('Finding evidence is absent from its indicator category')


def main():
    status = json.loads((ROOT / 'product-status.json').read_text())
    published = json.loads((ROOT / 'docs/product-status.json').read_text())
    validate_status(status, published, datetime.now(timezone.utc))
    paths = sorted((ROOT / 'examples').rglob('*.json')) + sorted((ROOT / 'docs/examples').rglob('*.json'))
    if not paths:
        raise ValueError('No published reports discovered')
    for path in paths:
        validate_report(json.loads(path.read_text()))
    if (ROOT / 'examples/apk-sentinel-sanitized-report.json').read_bytes() != (ROOT / 'docs/examples/apk-sentinel-sanitized-report.json').read_bytes():
        raise ValueError('Synthetic report copies disagree')
    print(f'Public schema, status copies and {len(paths)} report artifacts: PASS')
    if status['status'] != 'limited-beta':
        print('AVAILABILITY WARNING: paid service is not currently verified; analyzer correctness was not tested')


if __name__ == '__main__':
    main()
