# CERTCRYPT Binary Subject Canonicalization Profile (`subject.binary/1`) — overview

**Identifier:** `subject.binary/1`

**Label:** CERTCRYPT Binary Subject Canonicalization Profile v1

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
> The normative requirements for `subject.binary/1` are defined exclusively in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `subject.binary/1`?

`subject.binary/1` defines how opaque binary subjects are reduced to deterministic canonical bytes under CERTCRYPT public rules.

It treats the subject conservatively as bytes.

It does not parse the subject, infer meaning from it, or normalize it into a semantically equivalent form.

The profile exists for cases where byte-level fidelity matters more than any convenience transformation.

---

## Why this specification exists

Many real-world binary artifacts contain internal structure that makes semantic normalization unsafe or unverifiable across toolchains, including:

- container formats
- compressed formats
- offset-based formats
- media formats
- office or publishing formats
- archives and executable payloads

Attempting to normalize such artifacts can silently change the byte sequence while preserving apparent meaning.

That is acceptable for editing workflows, but not for CERTCRYPT canonicalization.

`subject.binary/1` therefore fixes the safest boundary:

- the subject is the exact input byte sequence
- the canonical bytes are exactly those bytes
- anything that would reinterpret or transform them is outside the profile

---

## Scope boundaries

`subject.binary/1` defines:

- the exact binary input boundary
- how `canonical_bytes(subject)` are produced
- which transformations are forbidden
- how profile-level verification remains subordinate to the broader CERTCRYPT architecture

It does not define:

- issuance
- independence
- consistency semantics
- semantic truth of the binary artifact
- legal meaning
- institutional approval
- trust or authority

---

## Core guarantees

Under `/1`, the profile preserves:

- byte-level fidelity of the subject input
- deterministic canonicalization that produces identical `canonical_bytes(subject)` for identical inputs
- absence of semantic inference, parsing, or transformation
- compatibility with hidden-content verification paths
- interpretation boundaries between byte-level identity and any higher-layer semantic, legal, or institutional outcome

---

## Relationship to other CERTCRYPT specifications

`subject.binary/1` is not a standalone verification system.

It sits below higher-layer artifact evaluation:

- [system-domain/1](../../../foundation/system-domain/1/index.md) decides which system is being evaluated
- [rules-domain/1](../../../foundation/rules-domain/1/index.md) decides which exact public rules apply
- [security-model/1](../../../foundation/security-model/1/index.md) decides which interpretation and fail-closed boundaries must hold
- [CCCP/1](../../../protocols/CCCP/1/index.md) supplies the canonicalization and commitment semantics
- [CCSP/1](../../../protocols/CCSP/1/index.md) supplies certificate envelope structure
- [verification-package/1](../../../ecosystem/verification/verification-package/1/index.md) and [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md) may later use the resulting subject material during offline verification

This profile contributes only one thing:

`canonical_bytes(subject)`

It does not by itself produce `Issued`, `Independent`, or any verifier authority outcome.

### Relationship to verification

CERTCRYPT certificates do not embed original binary subject material.

Verification against a binary subject therefore requires the verifier to possess the original bytes, or an exact byte-identical copy, whenever the applicable verification path requires subject recomputation.

That requirement remains fully offline-capable.

It does not justify:

- hosted truth services
- resolver authority
- managed interpretation shortcuts
- semantic upgrades from packaging convenience

### Anti-notarization boundary

`subject.binary/1` must not be read as a notarization profile.

It defines byte-preserving subject canonicalization only.

It does not define:

- timestamping semantics
- anchoring semantics
- proof-of-existence semantics
- proof-of-independence semantics

If a binary artifact is later used inside a CERTCRYPT `Independent` path, that meaning comes from the higher-layer issuance, leaf, settlement, proof, and verifier semantics, not from this profile alone.

---

## Reading guide

Recommended reading order for implementers and auditors:

1. [Specification](./specification.md)
2. [CCCP/1](../../../protocols/CCCP/1/specification.md)
3. [CCSP/1](../../../protocols/CCSP/1/specification.md)
4. [security-model/1](../../../foundation/security-model/1/specification.md)
5. [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/specification.md)

---

## Versioning

- **Specification identifier:** `subject.binary`
- **Specification version:** `/1`

Version `/1` defines the first canonical byte-preserving subject canonicalization profile under the active corpus.

Changes that alter the binary input boundary, the canonicalization rule, the forbidden-transformation list, or the boundary between byte-level identity and higher-layer semantics require a new major version.

Later versions do not retroactively reinterpret already valid subject canonicalizations governed by `/1`.

---

## One-line summary

**`subject.binary/1` defines the canonical byte-preserving canonicalization profile that produces deterministic `canonical_bytes(subject)` for opaque binary inputs, without parsing, inferring, or transforming them, and without itself producing `Issued`, `Independent`, or any institutional outcome.**

---

## Normative reference

This overview is informational only.

All definitive rules and constraints are defined in:

- [subject.binary/1/specification](./specification.md)

In case of discrepancy, the specification prevails.
