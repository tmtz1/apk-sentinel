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
        now = datetime(2026, 9, 25, 12, tzinfo=timezone.utc)
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
        now = datetime(2026, 9, 25, 12, tzinfo=timezone.utc)
        v.validate_status(status, copy.deepcopy(status), now)
        different = copy.deepcopy(status)
        different['status'] = 'unverified'
        with self.assertRaises(ValueError):
            v.validate_status(status, different, now)


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def state(name):
    status = json.loads((ROOT / 'product-status.json').read_text())
    status['status'] = name
    if name == 'limited-beta':
        status['endpoint_publicly_callable'] = True
        status['payment'].update(enabled=True, terms_status='current', test_ends='2026-10-01T00:00:00Z')
        status['availability_note'] = 'Bounded agent testing only.'
    else:
        status['payment'].update(enabled=False if name == 'paused' else None, terms_status='expired' if name == 'expired' else 'unverified')
        status['availability_note'] = 'Availability is ' + name + '. Do not submit payment.'
    return status


STALE_CLAIMS = [
    'Limited beta for AI agents and service buyers.',
    'Current bounded availability: accepts one APK per request at `0.01 USDC` (`10,000` atomic units) through 2026-09-05 UTC.',
    'Price: 0.01 USDC per request.',
]


class AvailabilitySummaries(unittest.TestCase):
    FILES = ['README.md', 'llms.txt', 'docs/llms.txt']

    def test_published_summaries_are_current_rendered_and_valid(self):
        v, r = load_script('validate_public'), load_script('render_docs')
        status = json.loads((ROOT / 'product-status.json').read_text())
        for name in self.FILES:
            text = (ROOT / name).read_text()
            self.assertEqual(r.render_availability(text, status, name), text, name)
            v.validate_availability_text(text, status, name)

    def test_every_state_renders_usable_summary(self):
        v, r = load_script('validate_public'), load_script('render_docs')
        for name in self.FILES:
            text = (ROOT / name).read_text()
            for current in ['limited-beta', 'paused', 'expired', 'unverified']:
                status = state(current)
                rendered = r.render_availability(text, status, name)
                v.validate_availability_text(rendered, status, name)
                self.assertIn(status['availability_note'], rendered)
                self.assertEqual(status['payment']['price_usdc'] in rendered, current == 'limited-beta', (name, current))

    def test_state_change_without_regeneration_is_drift(self):
        r = load_script('render_docs')
        status = state('paused')
        for name in self.FILES:
            text = (ROOT / name).read_text()
            self.assertNotEqual(r.render_availability(text, status, name), text, name)
        with self.assertRaises(ValueError):
            r.render_availability('no markers here', status, 'llms.txt')

    def test_stale_or_missing_claims_rejected_when_inactive(self):
        v = load_script('validate_public')
        for current in ['paused', 'expired', 'unverified']:
            status = state(current)
            for name in self.FILES:
                text = load_script('render_docs').render_availability((ROOT / name).read_text(), status, name)
                for claim in STALE_CLAIMS:
                    with self.assertRaises(ValueError, msg=(name, claim)):
                        v.validate_availability_text(text + '\n' + claim + '\n', status, name)
                for required in ['product-status.json', status['endpoint']]:
                    with self.assertRaises(ValueError, msg=(name, required)):
                        v.validate_availability_text(text.replace(required, 'removed'), status, name)

    def test_pricing_history_is_not_a_summary_target(self):
        r = load_script('render_docs')
        self.assertNotIn(ROOT / 'docs/pricing.md', r.artifacts())


class UnpaidObservation(unittest.TestCase):
    def fixture(self):
        return json.loads((ROOT / 'tests/fixtures/unpaid-402-observation.json').read_text())

    def test_fixture_body_matches_openapi_and_header(self):
        v = load_script('validate_public')
        v.validate_observation(self.fixture(), datetime(2026, 9, 26, tzinfo=timezone.utc))

    def test_fixture_mutations_rejected(self):
        v = load_script('validate_public')
        now = datetime(2026, 9, 26, tzinfo=timezone.utc)
        for mutate in [
            lambda f: f['body'].update(error={'code': 'payment_required'}),
            lambda f: f['body']['paymentRequired'].pop('maxAmountRequired'),
            lambda f: f['body']['paymentRequired'].update(maxAmountRequired='20000'),
            lambda f: f['body']['paymentRequired'].update(network='eip155:1'),
            lambda f: f['body']['paymentRequired'].update(scheme='upto'),
            lambda f: f['body']['paymentRequired'].update(asset='0x0'),
            lambda f: f['decoded_payment_required'].update(x402Version=1),
            lambda f: f['decoded_payment_required']['accepts'][0].update(amount='1'),
            lambda f: f['decoded_payment_required']['accepts'][0].update(payTo='0xabc'),
            lambda f: f['body']['paymentRequired'].update(payTo='0xabc'),
            lambda f: f['redactions'].clear(),
            lambda f: f.update(http_status=200),
            lambda f: f.update(observed_at='2026-09-27T00:00:00Z'),
            lambda f: f.update(observed_at='yesterday'),
        ]:
            bad = self.fixture()
            mutate(bad)
            with self.assertRaises((ValueError, v.ValidationError)):
                v.validate_observation(bad, now)


class StatusHardening(unittest.TestCase):
    def test_current_record_and_format_enforcement(self):
        v = load_script('validate_public')
        status = json.loads((ROOT / 'product-status.json').read_text())
        now = datetime(2026, 9, 26, tzinfo=timezone.utc)
        v.validate_status(status, copy.deepcopy(status), now)
        for field, value in [('reviewed_at', 'not-a-time'), ('last_verified', '2026-13-01')]:
            bad = copy.deepcopy(status)
            bad[field] = value
            with self.assertRaises(v.ValidationError):
                v.validate_status(bad, copy.deepcopy(bad), now)
        bad = copy.deepcopy(status)
        bad['observed_unpaid_challenge']['checked_at'] = 'soon'
        with self.assertRaises(v.ValidationError):
            v.validate_status(bad, copy.deepcopy(bad), now)

    def test_future_observations_and_inactive_contradictions_rejected(self):
        v = load_script('validate_public')
        now = datetime(2026, 9, 26, tzinfo=timezone.utc)
        for mutate in [
            lambda s: s.update(reviewed_at='2026-09-27T00:00:00Z'),
            lambda s: s['observed_unpaid_challenge'].update(checked_at='2026-09-27T00:00:00Z'),
            lambda s: s['payment'].update(terms_status='current'),
        ]:
            bad = json.loads((ROOT / 'product-status.json').read_text())
            mutate(bad)
            with self.assertRaises(ValueError):
                v.validate_status(bad, copy.deepcopy(bad), now)

    def test_status_copies_compared_as_raw_bytes(self):
        v = load_script('validate_public')
        raw = (ROOT / 'product-status.json').read_bytes()
        v.validate_status_bytes(raw, raw)
        with self.assertRaises(ValueError):
            v.validate_status_bytes(raw, raw.replace(b'\n', b'\r\n'))

    def test_requirements_enable_format_checks(self):
        self.assertIn('jsonschema[format]==4.26.0', (ROOT / 'requirements-docs.txt').read_text().split())
