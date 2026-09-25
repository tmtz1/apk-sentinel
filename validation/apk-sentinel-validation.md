# APK Sentinel validation notes

> Historical evidence, contextualized September 24, 2026. The test count below belongs to this earlier observation, not the current deployed build or a fresh test run. Its exact run date, analyzer commit and rules identifier are not recorded in this public packet; they remain unknown. The 395-test Oxproxion record and 426-test general record must not be combined into one suite result.


## What was exercised

The private APK Sentinel implementation was tested with its local test suite:

```text
./.venv/bin/pytest -q
```

Observed result:

```text
426 passed
```

The app-only acceptance lane has since been exercised against a nine-sample F-Droid edge-case corpus in isolated static-only runs. Large-input and bounded-scan handling were revised, then the previously rejected cases were rerun with deterministic report and cleanup checks.

A signed synthetic APK fixture was built locally from committed test source. It was analyzed statically and serialized using the canonical report serializer. The published example was then parsed back through the `AnalysisReport` schema before writing.

The fixture is intentionally synthetic:

- Package: `com.example.apksentinelfixture`
- Version: `1.2.3` / code `123`
- Target SDK: 34
- Test-only signing certificate
- Inert references used to exercise static indicators
- Never installed, executed, or side-loaded

## Published example

[`examples/apk-sentinel-sanitized-report.json`](../examples/apk-sentinel-sanitized-report.json)

Observed report properties:

- Schema version: `1.0`
- Four static indicators
- Four evidence-backed findings
- Deterministic rule-based risk score: `70`
- Historical recorded canonical size: 2,850 bytes. Current checked-in file: 4,128 bytes; compact sorted UTF-8 serialization (no newline): 2,850 bytes, measured September 24, 2026. The old size is not evidence of the current file size.

## What this demonstrates

- APK metadata can be extracted into a strict report model.
- Findings carry evidence references.
- The canonical report is versioned and machine-readable.
- The same fixture is suitable for repeatability tests.
- Static analysis does not require execution or network access.

## Deliberate limits

This example is not a malware verdict and does not prove that static analysis can establish whether an APK is safe or malicious. It is a safe fixture demonstrating report structure and validation behavior. Production implementation, private fixtures, deployment evidence, and payment integration remain restricted.
