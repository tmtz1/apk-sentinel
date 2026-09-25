# Reading an APK Sentinel report

The [synthetic example](examples/apk-sentinel-sanitized-report.json) and [public JSON Schema](schemas/analysis-report.schema.json) are the starting points. This schema was exported from inspected model definitions on September 24, 2026; it describes report artifacts, not proof of the deployed analyzer version.

## Evidence and scoring

`findings.findings` contains a rule ID, severity (`low`, `medium`, `high`), title and nonempty evidence strings. Those strings refer to signatures in the matching `indicators.indicators` category; they are not URLs to fetch. Scoring contributions reference the same finding rule IDs. The public validator checks those references, unique rules and `total = min(100, sum(contribution points))`.

The score is a bounded rule-based triage priority, not a probability, a detection-accuracy measure or a benign/malicious verdict. Reflection, permissions and embedded URLs often have legitimate explanations. Review individual evidence and provenance before escalation. A zero score is not a safety certificate.

## Partial results

`url_evidence.scan_truncated` and `indicators.scan_truncated` identify bounded scans. `true` means missing evidence cannot be interpreted as absence. Older published schema-1.0 examples omit these fields; the schema supplies a compatibility default of false, but omission in a historical artifact is **not independent proof** that no scan limit occurred. Failure to produce a report must remain a failure/unsupported outcome, not an empty successful report.

## Determinism and versioning

The inspected canonical serializer sorts JSON keys, uses compact separators, preserves Unicode, and emits UTF-8 without an added newline. Pretty-printed public files have different byte hashes and sizes. Certificate validity dates are input-derived metadata, not run timestamps. Request IDs, queue/lease state and payment receipts are outside the report core; do not compare transport envelopes as canonical reports.

Compare reports only for the same APK bytes, analyzer build, rules identity and schema. `schema_version: 1.0` alone does not identify a build or rules revision. These published report artifacts lack an embedded rules-version field, so carry build/rules provenance separately when available and label unknown provenance honestly. Future rule changes should carry a changed rules identifier; enforcement and migration need implementation verification before they become guarantees.

## Local checks

From the repository root:

```sh
python3.12 -m venv .venv
.venv/bin/pip install -r requirements-docs.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/validate_public.py
.venv/bin/python scripts/render_docs.py --check
```

The validator checks published examples, schema and selected semantics. It does not run APK analysis, test containment, or contact a paid endpoint.
