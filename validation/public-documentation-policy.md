# Public documentation checks

`product-status.json` is canonical; `docs/product-status.json` must be identical. Schema 1.1 distinguishes endpoint reachability from verified paid availability: `payment.enabled: null` means unknown, not disabled. A historical challenge price is not a current offer.

An active `limited-beta` record requires callable endpoint, explicitly enabled payment, current terms, a future terms expiry, and verification no older than seven days (UTC). Future-dated verification is rejected. Paused, expired and unverified records are valid but must not advertise enabled payment. An honest unavailable state passes structural checks and prints an availability warning, separate from analyzer correctness.

A daily scheduled workflow detects stale active claims without a push. It neither probes the paid route nor renews terms. Scheduling requires this workflow to be on the default branch; a PR-only workflow is not an active freshness monitor.

The renderer generates ordinary HTML, canonical URLs, sitemap and status banners from Markdown and canonical JSON. Run `python scripts/render_docs.py` after editing their sources; `--check` rejects stale generated pages. Markdown remains available for agents.

Report checks validate every published example against the public schema, then check finding/indicator evidence, unique finding/contribution references, score arithmetic and duplicate copies. Tests deliberately corrupt reports and exercise truncation flags. These checks do not run the private analyzer or establish operational containment.

The exported report schema was inspected against local source on September 24, 2026. No private analyzer implementation or private data is included. Active deployment/build reconciliation and complete paid-response schemas remain separate work.
