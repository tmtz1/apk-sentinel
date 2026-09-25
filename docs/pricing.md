# APK Sentinel availability and pricing

**Published beta terms expired; current paid-service availability is unverified.**

The [canonical status record](product-status.json) is the only maintained availability record. Its original September 3 verification date has not been advanced to imply a new paid-service test.

## What was actually checked

An empty, unpaid `POST https://api.willowbirdie.com/v1/apk/triage` returned HTTP 402 on September 24, 2026 (America/Chicago; September 25 UTC). The challenge advertised x402 v2 exact, Base mainnet (`eip155:8453`), and `10000` atomic USDC units (`0.01 USDC`). These are **observed challenge values, not renewed pricing terms**. The previously published window ended September 5 UTC.

No APK was uploaded, no payment was authorized, and no paid analysis, worker readiness, settlement, retention or cleanup was tested in this check. An endpoint answering is not evidence that the complete service works.

## Before submitting anything

Do not send payment or private APKs until the operator publishes current terms and verifies the paid workflow. General customer intake, browser uploads, and customer support are not enabled. No new price, deadline, retention guarantee or support SLA is being introduced by this documentation correction.

For integrations or pilot discussions, contact [admin@willowbirdie.com](mailto:admin@willowbirdie.com). Do not email APKs or secrets.
