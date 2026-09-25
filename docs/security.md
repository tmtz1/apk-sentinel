# APK Sentinel security

## Scope

APK Sentinel is designed as bounded static APK triage. The documented product boundary is:

- APK files are treated as untrusted input.
- The analyzer does not install or execute APKs.
- Extracted URLs and domains are evidence only; the static analyzer does not fetch them as part of this showcase.
- Results are structured, schema-versioned JSON with evidence and explicit limitations.
- The public documentation site accepts no APK uploads and exposes no customer intake endpoint.

## Authorized use

Only submit APKs that you are authorized to analyze. Do not send credentials, private keys, tokens, personal data, or customer artifacts through the public documentation site or the contact mailbox.

## Reporting a security issue

Send a concise report to [admin@willowbirdie.com](mailto:admin@willowbirdie.com?subject=APK%20Sentinel%20security%20report). Do not include secrets or live customer samples. Describe the affected public URL, impact, reproduction steps, and a safe test fixture where possible.

This page is a product security boundary, not a guarantee that every deployment has identical controls. Deployment-specific isolation, retention, payment, availability, and incident-response terms must be confirmed for the deployment being used.

## Named endpoint: unresolved operational guarantees

For `api.willowbirdie.com`, deletion deadlines, failure-retention windows, sample-metadata logging, data residency, and support response times have **not been reverified for current public use**. Ephemeral processing is a design intent, not a time-bound deletion guarantee. The current [availability record](product-status.json) therefore does not authorize private intake.

Allowed evaluation material is limited to authorized synthetic/public fixtures after availability and terms are confirmed. Do not submit customer or confidential samples. Reopening requires a dated operator-backed retention/logging statement and verified success/failure cleanup; documentation changes do not satisfy that gate.

## Evidence

- [Agent-facing API contract](agent-api-contract.md)
- [OpenAPI description](openapi.json)
- [Synthetic report](examples/apk-sentinel-sanitized-report.json)
- [Public source repository](https://github.com/tmtz1/apk-sentinel)
