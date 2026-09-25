#!/usr/bin/env python3
"""Public evidence checks; does not assert live analyzer availability."""
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[1]
REDACTED = 'REDACTED_PUBLIC_RECIPIENT'
# Claims that only belong in current-offer copy; pricing.md history is deliberately not scanned.
ACTIVE_ONLY_CLAIMS = [r'limited[- ]beta', r'\d+(?:\.\d+)?\s*USDC', r'atomic units', r'\bprice\s*:', r'through \d{4}-\d{2}-\d{2}']


def parse_time(value):
    Draft202012Validator({'type': 'string', 'format': 'date-time'}, format_checker=FormatChecker()).validate(value)
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def validate_status_bytes(root_raw, published_raw):
    if root_raw != published_raw:
        raise ValueError('Root and published status copies differ byte-for-byte')


def validate_status(status, published, now):
    if status != published:
        raise ValueError('Root and published status copies disagree')
    schema = json.loads((ROOT / 'docs/schemas/product-status.schema.json').read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(status)
    for observed in [status['reviewed_at'], status['observed_unpaid_challenge']['checked_at']]:
        if parse_time(observed) > now:
            raise ValueError('Status observations must not be future-dated')
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
    elif status['payment']['enabled'] is True or status['payment']['terms_status'] == 'current':
        raise ValueError('Non-active availability must not advertise enabled payment or current terms')


def validate_availability_text(text, status, name):
    for required in ['product-status.json', status['endpoint']]:
        if required not in text:
            raise ValueError(name + ' must cite ' + required)
    if status['status'] == 'limited-beta':
        for required in [status['payment']['price_usdc'], status['payment']['test_ends']]:
            if required not in text:
                raise ValueError(name + ' omits current terms ' + required)
    else:
        for claim in ACTIVE_ONLY_CLAIMS:
            if re.search(claim, text, flags=re.I):
                raise ValueError(name + ' makes a current-offer claim while status is ' + status['status'])


def validate_observation(fixture, now):
    """Check a captured unpaid 402 as a past observation; not a paid-client contract."""
    if fixture['http_status'] != 402 or fixture['method'] != 'POST':
        raise ValueError('Observation is not an unpaid POST challenge')
    if parse_time(fixture['observed_at']) > now:
        raise ValueError('Observation must not be future-dated')
    openapi = json.loads((ROOT / 'docs/openapi.json').read_text())
    Draft202012Validator(openapi['components']['schemas']['PaymentRequired'], format_checker=FormatChecker()).validate(fixture['body'])
    body = fixture['body']['paymentRequired']
    header = fixture['decoded_payment_required']
    if header.get('x402Version') != 2 or not header.get('accepts'):
        raise ValueError('Decoded header is not an x402 v2 challenge')
    if not any(all(a.get(k) == body[k] for k in ['scheme', 'network', 'asset']) and a.get('amount') == body['maxAmountRequired'] for a in header['accepts']):
        raise ValueError('Body and decoded header challenge terms disagree')
    if body['payTo'] != REDACTED or any(a.get('payTo') != REDACTED for a in header['accepts']):
        raise ValueError('Recipient must carry the explicit redaction marker')
    if not {'body.paymentRequired.payTo', 'decoded_payment_required.accepts[*].payTo'} <= set(fixture['redactions']):
        raise ValueError('Recipient redactions are not listed')


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
    now = datetime.now(timezone.utc)
    validate_status_bytes((ROOT / 'product-status.json').read_bytes(), (ROOT / 'docs/product-status.json').read_bytes())
    status = json.loads((ROOT / 'product-status.json').read_text())
    published = json.loads((ROOT / 'docs/product-status.json').read_text())
    validate_status(status, published, now)
    for name in ['README.md', 'llms.txt', 'docs/llms.txt']:
        validate_availability_text((ROOT / name).read_text(), status, name)
    validate_observation(json.loads((ROOT / 'tests/fixtures/unpaid-402-observation.json').read_text()), now)
    paths = sorted((ROOT / 'examples').rglob('*.json')) + sorted((ROOT / 'docs/examples').rglob('*.json'))
    if not paths:
        raise ValueError('No published reports discovered')
    for path in paths:
        validate_report(json.loads(path.read_text()))
    if (ROOT / 'examples/apk-sentinel-sanitized-report.json').read_bytes() != (ROOT / 'docs/examples/apk-sentinel-sanitized-report.json').read_bytes():
        raise ValueError('Synthetic report copies disagree')
    print(f'Public schema, status copies, availability summaries, unpaid 402 observation and {len(paths)} report artifacts: PASS')
    if status['status'] != 'limited-beta':
        print('AVAILABILITY WARNING: paid service is not currently verified; analyzer correctness was not tested')


if __name__ == '__main__':
    main()
