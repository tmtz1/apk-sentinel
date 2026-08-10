# oxproxion validation notes

## Commands and evidence

Source artifact:

```text
F-Droid version 2.1.104 / version code 214
SHA-256: 699cf26b831f6c903e0bc860fc4bb408548c37be927e65615ff7407b4cd45f47
```

The analyzer was run twice against the same APK bytes before the URL extractor fix; the canonical report was deterministic. After the fix, the regenerated canonical analyzer report was:

```text
Raw analyzer report SHA-256: ae50651216b6e5072292d12395a669973f67e6a5c5dfb78e8ed299fcdbf526c8
```

The focused URL regression tests and the full APK Sentinel suite passed:

```text
2 focused regression tests passed
395 passed in 4.88s
```

## Fix covered by this example

The extractor now rejects malformed HTTP(S) candidates with invalid hosts or ports and rejects unmistakable Markdown link concatenations such as:

```text
https://example/releases](https://example/releases
```

It continues to retain syntactically valid namespace URLs as static evidence rather than guessing that unusual means malicious. The public report applies a separate bounded publication filter to omit library/documentation namespaces.

## Provenance verification

- The APK is an Android package and was downloaded from the official F-Droid repository URL.
- The embedded signing certificate fingerprint matched the signing key recorded in the F-Droid metadata:
  `3f3af0c2b724c4918458c223508a61178e27d192caf942aa2d5825301bb1078e`.
- The detached F-Droid PGP signature was downloaded, but local GnuPG could not complete cryptographic verification because the corresponding F-Droid public key was not present in the local keyring. This is recorded rather than overstated.
- F-Droid's reproducibility page currently displays successful verification through version `2.1.97`; verification for `2.1.104` was not displayed at the time of review.

## Safety statement

The APK was analyzed statically. It was not installed, executed, side-loaded, connected to a device, or uploaded to an external malware-analysis service.
