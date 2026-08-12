# Real-world hard cases: where APK Sentinel had to grow up

The Oxproxion example shows what a finished report looks like. This page shows the less glamorous part: what happened when real Android packages pushed the analyzer into corners its first design had not handled gracefully.

The examples below are intentionally anonymized. They describe the engineering problem and the fix, not the private artifact trail.

## Case 1 — The package that was safe to reject, but not safe to misunderstand

### What happened

A legitimate F-Droid package arrived just above the original input ceiling. The analyzer rejected it before the static analysis phase began.

That first behavior was technically bounded, but the result was too easy to misread. It did not mean the application was suspicious. It meant the workload was outside the analyzer's current admission policy.

### What we changed

We raised the input ceiling only within the existing temporary-storage boundary. The analyzer still refuses oversized inputs rather than allowing an unbounded upload to dictate resource use.

We added boundary tests for:

- just-below-limit input;
- exactly-at-limit input;
- just-over-limit input;
- cleanup after each decision.

### What we learned

Admission policy and security verdict are different things. A package can be a perfectly ordinary application and still be unsupported by a particular analysis budget.

The public-facing lesson is simple: “unsupported at this limit” is a workload result, not a malware label.

## Case 2 — The scan that hit its fence and took the whole report down with it

### What happened

Several larger packages contained enough DEX content and URL-like material to reach the analyzer's bounded evidence-scan budget. The analyzer stopped protecting the scan budget by rejecting the entire package.

That was the wrong level of failure. The limit was doing its job. The reporting policy was not.

### What we changed

The scanner now:

- stops at the configured budget;
- keeps the evidence found before the cutoff;
- marks the affected section as truncated;
- preserves a sanitized, structured result;
- avoids pretending that the scan was complete.

The same policy was applied to the related static-indicator scan after testing exposed that it had the older, harsher behavior.

### What we learned

A bounded partial result is more honest and more useful than an all-or-nothing failure, provided the report makes the boundary visible. “Some evidence, scan stopped” is a real state. It deserves a real field in the schema.

We added regression tests before changing the implementation. The tests cover both the cutoff itself and preservation of evidence collected before the cutoff.

## Case 3 — The packages that exposed image-provenance drift

### What happened

The first rerun fixed the observed analyzer behavior, but not every affected sample had yet been rerun against the final rebuilt analyzer image. The results looked good, but mixing results from successive builds would have made the evidence weaker than it appeared.

### What we changed

The affected samples were rerun as a single evidence lane against the final analyzer build. Successful reports had to pass schema validation and produce byte-identical results on the repeated run.

The project record now treats the analyzer build as part of the evidence identity. A result without a clear build boundary is not discarded, but it is not quietly presented as if all samples used the same implementation.

### What we learned

Reproducibility is not just “run it twice.” It is “run the same input twice under the same relevant implementation and rules.” Paperwork is less exciting than code, but it catches expensive misunderstandings.

## Case 4 — The clean failure that proved containment was working

### What happened

A later ten-sample corpus included packages that reached existing APK or DEX limits. Six ended in the bounded failure path rather than producing reports.

That is not the headline anyone puts on a sales slide. It is still useful evidence.

Each affected sample showed the same essential behavior on repeat:

- bounded non-success outcome;
- no report pretending to be complete;
- sanitized error handling;
- no unexplained output;
- cleanup completed;
- no leftover analyzer job or workspace.

### What we learned

Fail-closed behavior is only valuable when it is deterministic and clean. A service that refuses a workload consistently, leaves no residue, and tells the caller enough to understand the disposition is behaving much better than one that guesses.

The remaining work is also clear: add more malformed, corrupted, boundary-sized, and archive-abuse fixtures so the real-world corpus is not carrying the entire burden of parser coverage.

## Case 5 — The concurrency test that stayed out of production settings

### What happened

The normal analyzer lane is intentionally conservative. We wanted to test simultaneous jobs without quietly changing the production concurrency setting and creating a new failure mode.

### What we changed

A separate test-only lane ran simultaneous pairs with independent workspaces and output attribution. The normal one-job setting was left alone.

The check looked for:

- cross-job output mix-ups;
- stale workspace reuse;
- surviving analyzer jobs;
- leftover temporary data;
- incorrect cleanup attribution.

No cross-job attribution problem was observed in that pass.

### What we learned

Concurrency testing should be isolated from production policy. Otherwise the test becomes the change, and nobody notices until the first real customer arrives with a second request.

## What these cases add to the showcase

The Oxproxion report demonstrates a readable real-world result. These cases demonstrate the engineering discipline behind the result:

- limits are explicit;
- unsupported workloads are not mislabeled as malicious;
- partial evidence is declared rather than hidden;
- build provenance is respected;
- failures are deterministic;
- cleanup is part of correctness;
- concurrency is tested without casually widening the production blast radius.

That is the part worth showing. Not because the analyzer never had a bad day, but because the bad days left a paper trail and became tests instead of folklore.

## Current boundary

APK Sentinel remains static-only. It does not install or execute applications, fetch extracted URLs, or claim to prove that an application is safe or malicious. This page contains engineering summaries only; it does not publish APK files, raw reports, private manifests, internal paths, infrastructure identifiers, or operational credentials.
