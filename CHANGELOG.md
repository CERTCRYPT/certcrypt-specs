# CHANGELOG

This repository follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
The repository version in [`VERSION`](VERSION) identifies a published snapshot of
the corpus as a whole; it is not the version of any specification. Each
specification carries its own version and status, and a frozen version never
changes (see [Versioning](README.md#versioning)).

Entries are one line per change: `type:scope: what changed`, where `type` is
`feature`, `bugfix`, `breaking`, `deprecation`, `security` or `docs`.

## 1.0.0

* feature:Corpus: the normative specifications under `normative/`, with the frozen versions and the digest of each frozen set in `frozen-versions.json`
* feature:Verification: the corpus proof of the `rules/2026-01` rules domain under `verification/rules/`, and the certification of the published files under `verification/`
