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

## Evidence

- [Agent-facing API contract](agent-api-contract.md)
- [OpenAPI description](openapi.json)
- [Synthetic report](examples/apk-sentinel-sanitized-report.json)
- [Public source repository](https://github.com/tmtz1/apk-sentinel-public-showcase)
