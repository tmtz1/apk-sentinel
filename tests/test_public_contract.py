import copy
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PublicContract(unittest.TestCase):
    def validator(self):
        path = ROOT / 'scripts/validate_public.py'
        self.assertTrue(path.exists(), 'Public consistency validator missing')
        spec = importlib.util.spec_from_file_location('validate_public', path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_human_pages_are_html_not_markdown_redirects(self):
        for name in ['about', 'pricing', 'contact', 'security', 'agent-product', 'agent-api-contract']:
            path = ROOT / 'docs' / name / 'index.html'
            self.assertTrue(path.exists(), name)
            text = path.read_text()
            self.assertNotIn('http-equiv="refresh"', text.lower())
            self.assertIn('<nav', text)
            self.assertIn('rel="canonical"', text)
            self.assertIn('<h1>', text)

    def test_reports_reject_bad_schema_arithmetic_and_evidence(self):
        v = self.validator()
        self.assertTrue(hasattr(v, 'validate_report'), 'Semantic report validation missing')
        report = json.loads((ROOT / 'examples/apk-sentinel-sanitized-report.json').read_text())
        v.validate_report(report)
        for mutate in [
            lambda r: r['risk_score'].update(total=69),
            lambda r: r['findings']['findings'][0].update(evidence=['invented']),
            lambda r: r['findings']['findings'][0].update(severity='critical'),
            lambda r: r.update(schema_version='unsupported'),
            lambda r: r['risk_score'].update(total=True),
        ]:
            bad = copy.deepcopy(report)
            mutate(bad)
            with self.assertRaises((ValueError, v.ValidationError)):
                v.validate_report(bad)
        report['url_evidence']['scan_truncated'] = True
        report['indicators']['scan_truncated'] = True
        v.validate_report(report)

    def test_active_claim_expires_and_has_bounded_freshness(self):
        v = self.validator()
        status = json.loads((ROOT / 'product-status.json').read_text())
        status.update(status='limited-beta', endpoint_publicly_callable=True)
        status['payment'].update(enabled=True, terms_status='current')
        now = datetime(2026, 9, 25, tzinfo=timezone.utc)
        with self.assertRaises(ValueError):
            v.validate_status(status, copy.deepcopy(status), now)
        status['payment']['test_ends'] = '2026-10-01T00:00:00Z'
        with self.assertRaises(ValueError):
            v.validate_status(status, copy.deepcopy(status), now)
        status['last_verified'] = '2026-09-25'
        v.validate_status(status, copy.deepcopy(status), now)
        status['last_verified'] = '2026-09-26'
        with self.assertRaises(ValueError):
            v.validate_status(status, copy.deepcopy(status), now)

    def test_paused_valid_but_conflicting_copies_rejected(self):
        v = self.validator()
        status = json.loads((ROOT / 'product-status.json').read_text())
        status.update(status='paused', endpoint_publicly_callable=False)
        status['payment']['enabled'] = False
        now = datetime(2026, 9, 25, tzinfo=timezone.utc)
        v.validate_status(status, copy.deepcopy(status), now)
        different = copy.deepcopy(status)
        different['status'] = 'unverified'
        with self.assertRaises(ValueError):
            v.validate_status(status, different, now)
