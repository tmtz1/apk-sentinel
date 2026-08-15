# APK Sentinel — Agent Product Brief

## One-line description

Submit one Android APK and receive a deterministic, evidence-backed static triage report.

## Why an agent would call it

An agent handling a mobile package, app-review queue, fraud case, or security workflow needs a compact answer before deciding whether to escalate the sample to a human analyst or deeper tooling. APK Sentinel returns structured evidence rather than an unbounded narrative.

## Core result

The report contains package identity, SDK metadata, permissions, exported components, signing metadata, bounded URL/domain evidence, suspicious static indicators, findings with evidence references, and a rule-based risk score.

## Agent-facing properties

- JSON-first output.
- Stable schema versioning.
- Deterministic rule-based scoring.
- Explicit limits and error states.
- No caller-supplied analyzer flags.
- No dynamic execution.
- No implicit URL fetching.
- Temporary artifact lifecycle with cleanup verification.

## Intended buyers and callers

- Mobile security and malware-triage systems.
- App stores and distribution platforms.
- Fraud and trust-and-safety pipelines.
- Mobile device-management and endpoint-security tools.
- App-testing and compliance workflows.
- Other agent services that need package evidence as an intermediate result.

## Boundaries

APK Sentinel is triage, not proof of benignness or maliciousness. It does not replace reverse engineering, threat intelligence, dynamic analysis, or incident response. Deployment availability, payment activation, pricing, retention, and customer intake are separate operational gates.

## Public evidence

The repository contains synthetic and sanitized examples only. It does not contain customer APKs, credentials, private keys, queue state, or production configuration.
