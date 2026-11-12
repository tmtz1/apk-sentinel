# APK Sentinel availability and pricing

**Limited paid API beta: 0.02 USDC per APK on Base mainnet.**

- Price: **0.02 USDC (20000 atomic units)** per APK, using x402 v2 exact and canonical Base USDC.
- Beta starts: **2026-11-12T01:00:38Z**.
- Beta ends: **2026-12-12T01:00:38Z**. New paid admission automatically closes at expiry. Renewal requires a new operator decision; this is not a subscription or automatic renewal.
- Endpoint: `POST https://api.willowbirdie.com/v1/apk/triage`.

Read the [canonical status](product-status.json) and the live unsigned payment challenge before signing. The server can pause new admission if the analysis pipeline is unavailable. HTTP402 requests payment; HTTP202 means admission, not successful analysis. Never pay by an unsolicited direct transfer.

## Scope and verification

This is a limited agent/API beta for APKs you are authorized to analyze. Browser uploads, confidential/private-data intake and unrestricted general-customer intake are not enabled. APKs are analyzed statically, not installed or executed. A risk score is not a guarantee that an APK is safe or malicious.

The corrected API and queue are deployed. The synthetic production pipeline, cleanup and paused rollback were verified. At activation, public readiness and the unsigned challenge were checked for the advertised network and amount. No new paid transaction was submitted as part of this activation; these checks do not claim a new mainnet settlement test. Earlier isolated payment tests are historical evidence, not a promise of uptime or successful analysis.

## Failed or uncertain analysis

For payment or analysis problems, contact [admin@willowbirdie.com](mailto:admin@willowbirdie.com). This address is monitored for the beta; no response-time SLA is promised. Provide the job ID and public transaction hash, if available. Do not send APKs, signed payment headers, result tokens, credentials or private keys.

Do not pay again or create a second authorization after a timeout or ambiguous failure. Poll an existing result when possible, then ask support to reconcile it. An abandoned job is a terminal failure, not a successful report. Refunds and no-charge retries are not automatic; verified cases require operator review and an explicitly approved remedy. This beta does not establish a guaranteed retention period or data-residency SLA; see [security and data handling](security.md).

## Historical terms

The earlier 0.01-USDC offer and September5 expiry are historical and superseded by the current beta above. The previous commercial pause did not consume any of this beta's 30-day window.
