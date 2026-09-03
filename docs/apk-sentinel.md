# APK Sentinel project description

## Deterministic Android APK triage

APK Sentinel is a limited-beta Willow & Birdie service for evidence-backed static analysis of Android application packages.

The bounded service route accepts one APK through x402 v2 exact payment on Base mainnet and produces a bounded, versioned JSON triage report. The canonical report core is repeatable for the same APK, analyzer version, and rules version. General human/private customer intake remains closed.

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
