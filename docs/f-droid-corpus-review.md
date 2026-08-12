# F-Droid corpus review

## Why this review exists

The most useful part of testing APK Sentinel was not the number of green checks. It was finding where the analyzer met the real world and got too strict for its own good.

This review brings together the public example already in this repository and two rounds of F-Droid testing. It focuses on what was learned, what changed, and what is worth showing publicly without turning private test material into a scrapbook.

## The 20-sample view

The comparison set contains 20 real-world samples:

- 9 samples from the earlier edge-case round
- 10 samples from the later, broader corpus round
- 1 separately documented F-Droid example already published here

All testing was static analysis. The applications were not installed or run.

### Earlier edge-case round

The first nine-sample round deliberately leaned toward larger packages and applications likely to exercise URL, DEX, permission, and metadata handling:

- VLC
- Termux
- Termux:API
- CanIWebView
- androidcrypt
- PGPony
- Just Video Player
- CryptoSafe
- Simple Text Crypt

The first pass exposed two important boundary problems. One sample exceeded the input-size ceiling, and several others reached bounded evidence-scan limits. Those were not mysterious application failures; they were analyzer policy failures. The analyzer was protecting its resource budget, then treating the budget boundary as a reason to reject the whole sample.

The fix was deliberately small: raise the input ceiling within the existing spool boundary, preserve evidence found before a scan cutoff, and mark the result as truncated instead of pretending the scan was complete. Regression tests were added before the implementation. The five affected samples were then rerun twice against the final analyzer build.

Result after hardening: 9/9 samples produced reports, with deterministic repeat runs and cleanup checks passing.

### Later corpus round

The later ten-sample round was designed to provide a different kind of pressure: a wider mix of ordinary, feature-rich, and relatively large F-Droid applications, plus a test-only simultaneous-job pass.

| Sample | Sequential dual-run outcome |
|---|---|
| Conversations | Report produced; schema-valid and byte-identical on repeat |
| AntennaPod | Report produced; schema-valid and byte-identical on repeat |
| KDE Connect | Report produced; schema-valid and byte-identical on repeat |
| Aegis Authenticator | Report produced; schema-valid and byte-identical on repeat |
| AnkiDroid | Bounded fail-closed result; repeat behavior matched |
| Syncthing-Fork | Bounded fail-closed result; repeat behavior matched |
| FairEmail | Bounded fail-closed result; repeat behavior matched |
| Etar | Bounded fail-closed result; repeat behavior matched |
| NewPipe | Bounded fail-closed result; repeat behavior matched |
| F-Droid | Bounded fail-closed result; repeat behavior matched |

Result: 4 report-producing samples and 6 deterministic bounded failures. These were expected limit outcomes, not silent crashes or inconsistent results. The test-only simultaneous pairs also kept their outputs separated and left no workspaces or analyzer jobs behind.

## What stayed the same

Across both rounds, the useful safety properties held:

- analysis remained static-only;
- reports were checked for repeatability;
- resource limits stayed explicit;
- evidence extraction was bounded rather than unbounded;
- cleanup was treated as part of the result, not an afterthought;
- successful reports were validated against the report schema;
- the risk score remained a rule-based triage aid, not a verdict;
- unusual permissions, components, reflection, or URLs were treated as clues for review, not proof of malicious intent.

That consistency matters more than a flattering pass percentage. A detector that changes its mind between two identical inputs has bigger problems than one that says “I cannot process this within the current budget.”

## What changed

The later corpus round differed in three useful ways.

First, it included six samples that stopped at existing APK or DEX bounds. That showed the analyzer could fail closed and repeat the same decision, but it also made the remaining coverage gap visible: the corpus still contains workloads that need either a future bounded-analysis policy or a clearly documented unsupported disposition.

Second, the earlier round led to a policy improvement. A scan cutoff is now represented as partial evidence instead of automatically poisoning the entire report. That is a better distinction between “the analyzer reached a safe limit” and “the APK is invalid.”

Third, the later round included a separate simultaneous-job check without changing the normal production concurrency setting. Outputs remained attributed to the correct inputs, and cleanup held under the extra pressure.

## The separately published real-world example

The existing Oxproxion example remains the best individual showcase in this repository. It is small enough to read, comes from an official F-Droid release, and demonstrates the difference between evidence and interpretation:

- permissions and exported components can be summarized in context;
- reflection can be flagged without calling it malicious;
- a low static score is not a safety certificate;
- provenance and verification limits should be recorded plainly;
- the APK itself does not need to be published to make the analysis useful.

That example shows the report format. The two corpus rounds show how the analyzer behaves when real packages push against its boundaries. They serve different purposes and should stay separate.

## What is worth showcasing

The strongest public story is not “20 APKs passed.” That would be tidy, and wrong in the interesting way.

A better showcase is:

1. the synthetic report for the machine-readable contract;
2. the Oxproxion report for a readable, provenance-backed real-world example;
3. the earlier nine-sample round for demonstrating that a boundary bug was found, fixed with tests, and rerun deterministically;
4. the later ten-sample round for showing honest fail-closed behavior, repeatability, cleanup, and job isolation;
5. the lessons below, because the failures are where the engineering work earned its keep.

## Lessons learned

1. Limits need a failure policy. A safe bound is useful; rejecting every sample that reaches it is often too coarse.
2. Partial evidence needs a visible marker. Otherwise a short report can look complete when it is not.
3. Reproducibility includes the analyzer build. Results from different builds should not be mixed casually.
4. A bounded failure can be a successful safety outcome. Empty output, sanitized errors, repeatable behavior, and cleanup are meaningful evidence.
5. Concurrency deserves its own lane. Test simultaneous jobs separately while keeping the normal production setting conservative.
6. Corpus testing should chase assumptions, not just popular applications. The awkward samples teach more.
7. Static analysis is triage, not a courtroom verdict. Context beats theatrics.

## Current boundary

APK Sentinel remains an in-development, static-only analyzer. It does not install applications, execute them, contact extracted URLs, or claim to prove that an application is safe or malicious. The public material is intentionally limited to aggregate results, selected reports, and reproducible lessons rather than raw samples or operational artifacts.

That is the useful version of the story: enough detail to show the work, not enough loose material to create a new problem.
