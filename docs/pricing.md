# APK Sentinel availability and pricing

**Analysis pipeline restored; paid intake explicitly paused.**

The [canonical status record](product-status.json) is the maintained availability record. The pipeline verification date does not renew payment terms or imply a paid-service test.

## Verified November 11, 2026

Synthetic APK jobs completed through the production analysis pipeline, including after service restart, with matching artifact identity and successful cleanup. These were internal unpaid operational canaries, not customer uploads or settlement tests.

An empty unpaid `POST https://api.willowbirdie.com/v1/apk/triage` returns **HTTP 503 without a payment challenge**. Admission is blocked by the server. No payment was submitted or settled.

## Historical challenge, not an offer

The previous HTTP 402 observation remains historical evidence. It advertised x402 v2 exact on Base mainnet and `0.01 USDC`; it is neither the current endpoint response nor renewed pricing. The published window ended September 5 UTC.

## Before submitting anything

Do not send payment or private APKs until the operator publishes current terms and verifies the paid workflow. General customer intake, browser uploads, and customer support remain disabled. No new price, deadline, retention guarantee or support SLA is introduced here.

For integrations or pilot discussions, contact [admin@willowbirdie.com](mailto:admin@willowbirdie.com). Do not email APKs or secrets.
