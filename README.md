# APK Sentinel — Public Technical Showcase

**Willow & Birdie Innovations · Tmtz**

APK Sentinel is a private, in-development project for evidence-backed static analysis of Android APKs.

The intended workflow is bounded and deterministic: validate one APK, analyze it statically inside a restricted job boundary, return a versioned JSON report, and clean up temporary artifacts.

## What it is designed to show

- APK identity and package metadata
- Permissions and dangerous permission combinations
- Exported Android components
- Signing certificate metadata
- Bounded URL, domain, and IP extraction
- Suspicious static API indicators with evidence references
- Structured findings and a deterministic rule-based risk score

## Safety boundary

- APKs are not installed, executed, or side-loaded
- The analyzer is designed for a networkless job boundary
- Uploaded samples and derived artifacts are intended to be ephemeral
- Input size, extraction, output, and wall-time limits are explicit
- Extracted URLs are inert report data and are not fetched
- The risk score is rule-based, not LLM-generated

## Evidence package

- [APK Sentinel architecture](assets/apk-sentinel-architecture.svg)
- [Sanitized synthetic report](examples/apk-sentinel-sanitized-report.json)
- [Validation notes](validation/apk-sentinel-validation.md)
- [Real-world oxproxion 2.1.104 example](examples/real-world/oxproxion-2.1.104/)
- [Real-world hard cases and fixes](docs/real-world-hard-cases.md)
- [Project description](docs/apk-sentinel.md)

## Status and limits

The app-only static-analysis lane has completed its current internal acceptance review. A nine-sample F-Droid edge-case corpus was exercised in isolated, static-only runs; the initially rejected large/complex samples were rerun after bounded-input and partial-evidence handling were improved. Successful reports were checked for repeatability and cleanup.

The analyzer now uses a 125 MiB input ceiling and reports when bounded URL or indicator scans are truncated rather than silently presenting incomplete evidence. These limits are safety bounds, not a promise of complete APK coverage.

This is not a public paid endpoint and does not claim that static analysis can prove an APK safe or malicious. Payment integration, public deployment, private fixtures, customer data, and dynamic analysis remain deferred or restricted.

The public report uses a synthetic test APK. No customer samples, private APKs, credentials, or proprietary detection logic are included.

## Links

- [Willow & Birdie Innovations](https://willowbirdie.com)
- [Project profile](https://github.com/tmtz1)
- [Contact](mailto:admin@willowbirdie.com)
