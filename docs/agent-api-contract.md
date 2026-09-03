# APK Sentinel — Agent-Facing Contract

This is the public product contract for the current bounded AI-agent/service-buyer beta.

- Base URL: `https://api.willowbirdie.com`
- Payment: x402 v2 exact on Base mainnet (`eip155:8453`)
- Current price: `0.01 USDC` (`10,000` atomic units) through 2026-09-05 UTC
- General human/private customer intake is not enabled.
- Canonical machine-readable status: [product-status.json](product-status.json).

## Primary operation

```http
POST /v1/apk/triage
Content-Type: multipart/form-data
```

Input:

- One APK binary in the `file` field.
- One APK per request.
- Maximum upload: 125 MiB.

Success:

- HTTP `200`.
- Versioned JSON analysis report.
- Report includes package metadata, permissions, components, signing metadata, bounded URL/domain evidence, suspicious indicators, findings, and risk score.

## Optional preflight

```http
POST /v1/apk/preflight
Content-Type: multipart/form-data
```

Preflight validates the upload boundary and returns a deployment-specific quote or validation result. It is not a malware verdict and does not by itself settle payment.

## Health and readiness

```http
GET /healthz
GET /readyz
```

`/healthz` reports process health. `/readyz` reports dependency and workspace readiness. A service may return `503` when it is not ready.

## Error shape

```json
{
  "error": {
    "code": "invalid_apk",
    "message": "uploaded file is not a valid APK",
    "request_id": "request-specific-uuid"
  }
}
```

Expected classes include malformed upload, oversized upload, invalid APK, analysis failure, and temporary service unavailability. Messages are sanitized and do not expose paths, credentials, or stack traces.

## Processing boundary

- Static analysis only.
- No APK installation, execution, or side-loading.
- Extracted URLs are inert evidence and are not fetched.
- Automatic retries are not assumed by this contract.
- Current bounded payment and availability are documented above. Retention, support, and data residency remain deployment-specific.
