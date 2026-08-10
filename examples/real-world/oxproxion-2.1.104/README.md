# oxproxion 2.1.104 — real-world static-analysis example

## Provenance

- Official listing: https://f-droid.org/en/packages/io.github.stardomains3.oxproxion/
- Source: https://github.com/stardomains3/oxproxion
- License: Apache-2.0
- Version: `2.1.104`
- Version code: `214`
- F-Droid source commit: `fb7ab9907c04b2593b7443ea898a0dfa6b0f2d5e`
- APK SHA-256: `699cf26b831f6c903e0bc860fc4bb408548c37be927e65615ff7407b4cd45f47`
- F-Droid APK: `https://f-droid.org/repo/io.github.stardomains3.oxproxion_214.apk`
- F-Droid PGP signature: `https://f-droid.org/repo/io.github.stardomains3.oxproxion_214.apk.asc`
- F-Droid build log: `https://f-droid.org/repo/io.github.stardomains3.oxproxion_214.log.gz`

The APK was obtained from F-Droid and analyzed locally. The APK is not included in this repository.

## Analysis result

APK Sentinel produced schema version `1.0` with a deterministic rule-based score of `10`.

The report identified:

- Dangerous permissions consistent with the app's advertised camera, microphone, location, notification, and local-network features
- Explicitly exported activities and other Android components
- V2 APK signing
- A reflection API indicator: `java.lang.Class.forName`
- A medium-severity static finding: `suspicious.reflection`

## Interpretation

This is **not a malware verdict**. The permissions and components require review, but they are not by themselves evidence of malicious behavior. Reflection is common in legitimate Android applications and can produce false positives.

The URL evidence was sanitized before publication because the current extractor also surfaces URL-like strings from embedded documentation, HTML, and library resources. The published report retains only a bounded set of recognizable application-related domains.

## Safety statement

The APK was analyzed statically. It was not installed, executed, side-loaded, connected to a device, or uploaded to an external malware-analysis service. This report demonstrates triage evidence and deterministic reporting; it does not certify the APK as safe or malicious.
