# APK Sentinel availability and pricing

APK Sentinel is a deterministic, automation-friendly static APK triage API in a limited beta. The current bounded service route uses x402 v2 exact payment on Base mainnet at 0.01 USDC per accepted APK through 2026-09-05 UTC. General human/private customer intake is closed; retention and support terms remain deployment-specific.

The current bounded service route is `POST https://api.willowbirdie.com/v1/apk/triage`, protected by x402 v2 exact payment on Base mainnet (`eip155:8453`) at `0.01 USDC` per accepted APK (`10,000` atomic units) through 2026-09-05 UTC. One APK is accepted per request; concurrency remains `1` and automatic retries are disabled.

This is an agent/service-buyer test, not unrestricted human or private APK intake. Static analysis only: APKs are not installed or executed. For a pilot or integration discussion, contact [admin@willowbirdie.com](mailto:admin@willowbirdie.com?subject=APK%20Sentinel%20pricing).

The public showcase contains synthetic and sanitized evidence only. No customer intake is enabled through this documentation site.
