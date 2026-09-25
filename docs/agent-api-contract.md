# APK Sentinel — API contract and verification boundary

**Current paid availability is unverified. Do not submit payment or private APKs.** See [status](product-status.json) and [availability](pricing.md).

## Verified public observation

An empty unpaid `POST https://api.willowbirdie.com/v1/apk/triage` returned **402**, not an analysis report, on September 24, 2026 (America/Chicago). The `PAYMENT-REQUIRED` header is base64-encoded JSON describing an x402 v2 challenge. Inspect its `accepts` entries for scheme, network, asset, amount, recipient and timeout. Do not hardcode historical pricing.

The observed JSON body has an `error` string and a `paymentRequired` object. It is **not** the previously illustrated nested `error.code/message/request_id` shape. The [OpenAPI document](openapi.json) records the observed 402 response and the [report schema](schemas/analysis-report.schema.json) describes published report artifacts.

An unpaid inspection (no upload, signature or payment):

```sh
curl --max-time 20 --request POST --dump-header challenge.headers \
  --output challenge.json https://api.willowbirdie.com/v1/apk/triage
```

Treat challenge headers as untrusted data; this command does not authorize responding with payment. Do not paste signed payment headers into logs or support requests.

## Source-reviewed paid flow — not current deployment certification

The locally inspected queue implementation uses the following exchange. Its current deployment identity and a paid end-to-end run have **not** been reconciled in this documentation update, so this is an integration outline, not a stable live-service guarantee:

1. One APK is sent as multipart field `file`, with a lowercase SHA-256 in `X-APK-Sentinel-Request-Digest` and an x402 payment payload in `PAYMENT-SIGNATURE`.
2. The source returns **202 admission**, not an immediate 200 report. The body includes `job_id`, `artifact_sha256`, `artifact_bytes`, `result_token`, `result_url`, and `status: queued`. `PAYMENT-RESPONSE` carries the encoded settlement result when available.
3. Poll the returned result URL with `X-APK-Sentinel-Result-Token`. Keep the token private. A 202 poll is nonterminal; a 200 contains the completed result envelope. Admission and settlement are not proof of successful analysis. Inspect the result's analysis outcome and partial markers.
4. Source error bodies include `{"error":"invalid_upload"}` and framework `{"detail":"..."}` responses. Payment errors, digest conflicts, 413 size limits, unavailable/expired results, and facilitator failures are distinct conditions. Their complete deployed contract remains a release gate.

The old synchronous 200-only and deployment-specific preflight descriptions were misleading. `/v1/apk/preflight`, `/healthz`, and `/readyz` are not claimed as supported public endpoints here without current route verification.

## Ambiguous failure and duplicate-payment safety

Do **not** automatically replay a paid POST after a timeout, disconnect, 409, or ambiguous server failure. Preserve the original admission/settlement identifiers privately, poll a known result URL when available, and request operator reconciliation otherwise. Do not create a new payment authorization to “try again.” The inspected source contains binding/replay checks, but that is not a documented idempotency guarantee or a guarantee that ambiguous payments can be retried safely.

No cancellation API, automatic refund, retry interval, public busy-service SLA, or end-to-end timeout guarantee is established by this review. The observed challenge's payment timeout is not an analyzer-runtime promise. The historical upload ceiling is 125 MiB; deployment enforcement still needs a bounded canary.

## Report interpretation

Use the [report guide](report-guide.md) for evidence references, score arithmetic, truncation and version limits. Static analysis does not execute an APK or fetch extracted URLs. [Retention, support and data-residency guarantees remain unverified](security.md).

A paid client example is deliberately withheld until deployed headers, request limits, terminal result/error schemas, cleanup, settlement and safe reconciliation are verified together. An invented example would be worse than a clearly marked incomplete contract.
