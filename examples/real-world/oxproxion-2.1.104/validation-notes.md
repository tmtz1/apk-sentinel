# oxproxion validation notes

## Commands and evidence

Source artifact:

```text
F-Droid version 2.1.104 / version code 214
SHA-256: 699cf26b831f6c903e0bc860fc4bb408548c37be927e65615ff7407b4cd45f47
```

Static analysis was run twice with the same analyzer and APK bytes. The canonical report hashes were identical:

```text
374f2643e1a83ac9a65f62cb492cc91c055d17b99908fbe64696cf527348635f
374f2643e1a83ac9a65f62cb492cc91c055d17b99908fbe64696cf527348635f
```

The APK Sentinel test suite also passed:

```text
393 passed in 4.87s
```

## Provenance verification

- The APK is an Android package and was downloaded from the official F-Droid repository URL.
- The embedded signing certificate fingerprint matched the signing key recorded in the F-Droid metadata:
  `3f3af0c2b724c4918458c223508a61178e27d192caf942aa2d5825301bb1078e`.
- The detached F-Droid PGP signature was downloaded, but local GnuPG could not complete cryptographic verification because the corresponding F-Droid public key was not present in the local keyring. This is recorded rather than overstated.
- F-Droid's reproducibility page currently displays successful verification through version `2.1.97`; verification for `2.1.104` was not displayed at the time of review.

## Known limitation

The current URL extractor is intentionally bounded but noisy for applications containing HTML, documentation, and library resources. The raw local report contained malformed URL-like strings. Those were retained privately for engineering follow-up and excluded from the public report; no analyzer code was changed for this showcase.
