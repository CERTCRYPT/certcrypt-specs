# Normative

This is the normative corpus: the specifications that state the public rules a verifier applies. A document is part of it once it is published here, and nothing outside it carries normative weight, however closely it describes the same model.

The corpus is organized by plane and versioned per family. Every artifact carries the `rules_version` in force when it was issued, and a verifier resolves that exact version from here — later versions do not re-evaluate an older artifact, do not supersede it, and cannot break it. That is what makes the corpus additive: publishing a new version extends what is readable without moving the rules any existing artifact is already bound to.

These documents are published in English only. A verifier resolves one text from an artifact's `rules_version`, and the corpus proof commits to the bytes of that text, so there is exactly one version of each and no rendering of it.

## Inside this section

The corpus has five planes. Each family within a plane is versioned
independently, and a version states its own status: freezing is a formal step
with stated conditions, not something publication confers.

- [Foundation](./foundation/index.md) — the plane the rest builds on: the system
  manifest and foundation statements, the system and rules domains, the composite
  signature profile, and the security model.
- [Protocols](./protocols/index.md) — canonicalization and commitment, envelope
  serialization, consistency verification, the collection and holder-key-set
  commitment schemes, and the submission-set protocol on the settlement side.
- [Profiles](./profiles/index.md) — how each kind of subject is reduced to
  deterministic canonical bytes before anything commits to it.
- [Models](./models/index.md) — how independence is derived from a fixed leaf and
  settled capacity.
- [Ecosystem](./ecosystem/index.md) — the artifacts and contracts that bind
  authorization, settlement and verification, and the operator specifications.

## Recommended reading order

1. [Foundation](./foundation/index.md) — nothing else is interpretable without
   the system domain, the rules domain and the security model
2. [Protocols](./protocols/index.md) — the canonicalizations and envelopes every
   later artifact consumes
3. [Profiles](./profiles/index.md) — the subject canonicalizations those
   protocols commit to
4. [Models](./models/index.md) — what a proof of independence asserts, given the
   above
5. [Ecosystem](./ecosystem/index.md) — the settlement, capacity and verification
   artifacts that carry it, and the operator specifications beside them

## The limits of this corpus

It defines interpretation and verification boundaries, and nothing beyond them. It does not prove that a claim is true, does not replace cryptographic authenticity, and does not by itself produce `Independent` — that is a verdict a verifier reaches by applying these rules, not a status this corpus confers.

Read together, these specifications are what makes a verdict reproducible by someone who has neither the issuer's systems nor CERTCRYPT's: the rules are public, resolvable by version, and named by every artifact that is bound to them.
