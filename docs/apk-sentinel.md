# APK Sentinel project description

## Deterministic Android APK triage

APK Sentinel is a private, in-development Willow & Birdie project for evidence-backed static analysis of Android application packages.

The planned product accepts one APK and produces a bounded, versioned JSON triage report. The canonical report core is intended to be repeatable for the same APK, analyzer version, and rules version.

## Planned report areas

- Package metadata and APK identity
- Requested permissions and dangerous combinations
- Exported Android components
- Signing certificate metadata and fingerprints
- Bounded URL, domain, and IP evidence
- Suspicious API indicators with source references
- Structured findings with severity and category
- A deterministic rule-based risk score

## Explicit non-goals

- No APK installation or execution
- No dynamic analysis in the current MVP
- No URL-based APK ingestion
- No sample retention as a product feature
- No VirusTotal dependency or sample resale
- No LLM-generated core scoring

The project is not a guarantee that an APK is safe or malicious. Static analysis can miss encrypted, downloaded, environment-triggered, or runtime-only behavior.
