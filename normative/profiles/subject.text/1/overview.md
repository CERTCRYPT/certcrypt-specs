# CERTCRYPT Plain Text Subject Canonicalization Profile (`subject.text/1`) — overview

**Identifier:** `subject.text/1`

**Label:** CERTCRYPT Plain Text Subject Canonicalization Profile v1

**Page:** Informative overview

**Specification type:** Profile Specification

**Layer:** Layer 2 — Profiles

**Status:** Frozen

**Depends on:**
- [system-domain/1](../../../foundation/system-domain/1/index.md)
- [rules-domain/1](../../../foundation/rules-domain/1/index.md)
- [security-model/1](../../../foundation/security-model/1/index.md)
- [CCCP/1](../../../protocols/CCCP/1/index.md)
- [CCSP/1](../../../protocols/CCSP/1/index.md)

> This document is **informative**.
> The normative requirements for `subject.text/1` are defined exclusively in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `subject.text/1`?

`subject.text/1` defines how plain text subjects are reduced to deterministic canonical bytes under CERTCRYPT public rules.

It exists for cases where the subject is legitimately plain text and where minimal explicit normalization is needed to preserve reproducibility across environments.

The profile does not interpret text semantically.

It only defines the bounded transformations required to make textual byte representation stable enough for CERTCRYPT canonicalization.

---

## Why this specification exists

Plain text often suffers from benign representation drift across systems, especially around:

- line endings
- trailing newline presence
- platform export behavior

If such content were always treated as opaque binary, equivalent text could produce unnecessarily different canonical bytes across environments.

`subject.text/1` therefore defines a deliberately narrow textual normalization boundary:

- line endings are normalized deterministically
- exactly one final CRLF is enforced
- all other bytes remain preserved

Anything beyond that is outside the profile.

---

## Scope boundaries

`subject.text/1` defines:

- what counts as acceptable plain text input for the profile
- the exact line-ending normalization model
- final newline behavior
- the byte-preservation boundary
- when an implementation must stop and use another profile instead

It deliberately does not define:

- issuance
- independence
- consistency semantics
- markup interpretation
- authorship
- truth
- legal meaning
- trust or institutional endorsement

---

## Core guarantees

Under `/1`, the profile preserves:

- bounded textual canonicalization with deterministic line-ending normalization and final-CRLF behavior
- byte preservation outside the explicitly defined transformations
- compatibility with hidden-content verification paths
- subordination to higher-layer artifact evaluation
- interpretation boundaries between text canonicalization and any authorship, semantic, legal, or institutional outcome

---

## Relationship to other CERTCRYPT specifications

`subject.text/1` is not a standalone verification system.

It sits below higher-layer artifact evaluation:

- `system-domain/1` decides which system is being evaluated
- `rules-domain/1` decides which exact public rules apply
- `security-model/1` decides which interpretation and fail-closed boundaries must hold
- `CCCP/1` supplies the canonicalization and commitment semantics
- `CCSP/1` supplies certificate envelope structure
- `verification-package/1` and `verifier-toolkit/1` may later use the resulting subject material during offline verification

This profile contributes only:

`canonical_bytes(subject)`

It does not by itself produce `Issued`, `Independent`, or any verifier authority outcome.

---

### Relationship to `subject.binary/1`

`subject.text/1` is narrower than [subject.binary/1](../../subject.binary/1/index.md).

Use `subject.text/1` only when the subject can safely and deterministically be treated as plain text under the rules defined by this profile.

If that cannot be established without ambiguity, parser discretion, or higher-level semantic interpretation, the safer profile is [subject.binary/1](../../subject.binary/1/index.md).

---

### Relationship to verification

CERTCRYPT certificates do not embed original text subject material.

Verification against a text subject therefore requires the verifier to possess the original text bytes, or an exact byte-identical copy, whenever the applicable verification path requires subject recomputation.

That remains fully offline-capable.

It does not justify:

- hosted truth services
- resolver authority
- managed interpretation shortcuts
- semantic upgrades from packaging convenience

---

### Anti-notarization boundary

`subject.text/1` must not be read as a notarization profile.

It defines text canonicalization only.

It does not define:

- timestamping semantics
- anchoring semantics
- proof-of-existence semantics
- proof-of-independence semantics

If a text artifact is later used inside a CERTCRYPT `Independent` path, that meaning comes from the higher-layer issuance, leaf, settlement, proof, and verifier semantics, not from this profile alone.

---

## Reading guide

Recommended order for implementers and auditors:

1. [foundation](../../../foundation/index.md)
2. [CCCP/1](../../../protocols/CCCP/1/index.md)
3. [CCSP/1](../../../protocols/CCSP/1/index.md)
4. [subject.binary/1](../../subject.binary/1/index.md)
5. [subject.text/1/specification](./specification.md)
6. [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md)

---

## Versioning

- **Specification identifier:** `subject.text`
- **Specification version:** `/1`

Version `/1` defines the first canonical plain-text canonicalization profile under the active corpus.

Changes that alter the input boundary, the line-ending normalization rule, the final-CRLF rule, the byte-preservation rule, or the boundary between canonicalization and higher-layer semantics require a new major version.

Later versions do not retroactively reinterpret already valid text canonicalizations governed by `/1`.

---

## One-line summary

**`subject.text/1` defines the canonical bounded canonicalization profile for plain-text input, applying only deterministic line-ending normalization and final-CRLF enforcement, and producing deterministic `canonical_bytes(subject)` without itself producing authorship, semantic interpretation, or `Independent`.**

---

## Normative reference

This overview is informational only.

All definitive rules and constraints are defined in:

- [subject.text/1/specification](./specification.md)

In case of discrepancy, the specification prevails.
