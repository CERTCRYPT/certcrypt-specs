# CERTCRYPT Email Subject Canonicalization Profile (`subject.email/1`) — overview

**Identifier:** `subject.email/1`

**Label:** CERTCRYPT Email Subject Canonicalization Profile v1

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
> The normative requirements for `subject.email/1` are defined exclusively in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `subject.email/1`?

`subject.email/1` defines how complete email messages are reduced to deterministic canonical bytes under CERTCRYPT public rules.

It exists for cases where the subject is a complete message and where minimal, explicitly bounded canonicalization is needed to preserve reproducibility across different capture and export environments.

The profile does not interpret email semantically.

It defines only the bounded transformations required to make a message representation stable enough for CERTCRYPT canonicalization.

---

## Why this specification exists

The same emitted message may appear in different byte forms when it is exported and re-opened by different local tooling, because of:

- line-ending differences across exports
- RFC 5322 header folding applied at different points by different export libraries
- an added, removed, or repeated final line terminator on save

The profile reconciles exactly those differences and no others. Transit mutation (relay-added headers, re-encoding between hops) and message regeneration by a store that does not retain the message as bytes are deliberately out of scope; the normative specification states this boundary precisely.

If email were treated either as opaque binary in all cases or as a semantically parsed object, implementations would either lose interoperability or introduce parser-dependent ambiguity.

`subject.email/1` therefore defines a narrow canonicalization boundary:

- complete-message input is required
- header treatment is explicit and deterministic
- body treatment is explicit and bounded
- MIME is not semantically reserialized

Anything beyond that is outside the profile.

---

## Scope boundaries

`subject.email/1` defines:

- what counts as acceptable complete-message input
- how line endings are normalized
- how headers are split from the body and unfolded, with header field order, names, and values otherwise preserved as bytes
- how the body is preserved byte-for-byte after line-ending normalization and trailing-terminator normalization, without semantic MIME reinterpretation
- when an implementation must stop and use another profile instead

It deliberately does not define:

- issuance
- independence
- consistency semantics
- sender authenticity
- delivery or receipt evidence
- truth
- legal meaning
- trust or institutional endorsement

---

## Core guarantees

Under `/1`, the profile preserves:

- bounded canonicalization of complete-message email input
- deterministic line-ending, header, and body treatment without semantic MIME reinterpretation
- usability as a leaf profile whose canonical bytes feed CCCP-governed commitment construction
- subordination to higher-layer artifact evaluation
- interpretation boundaries between byte-level canonicalization and any sender, delivery, legal, or institutional outcome

---

## Relationship to other CERTCRYPT specifications

`subject.email/1` is not a standalone verification system.

It sits below higher-layer artifact evaluation:

- `system-domain/1` decides which system is being evaluated
- `rules-domain/1` decides which exact public rules apply
- `security-model/1` decides which interpretation and fail-closed boundaries must hold
- `CCCP/1` supplies the canonicalization and commitment semantics
- `CCSP/1` supplies certificate envelope structure
- `verifier-toolkit/1` may later use the verifier-held subject material during offline verification; `verification-package/1` never carries the material itself

This profile contributes only:

`canonical_bytes(subject)`

It does not by itself produce `Issued`, `Independent`, or any verifier authority outcome.

---

### Relationship to `subject.binary/1`

`subject.email/1` is narrower than [subject.binary/1](../../subject.binary/1/index.md).

Use `subject.email/1` only when the subject can safely and deterministically be treated as one complete message under the rules defined by this profile.

If that cannot be established without ambiguity, parser discretion, or reconstructed mailbox semantics, implementations are required by the specification (§10) to use [subject.binary/1](../../subject.binary/1/index.md) instead.

---

### Relationship to verification

CERTCRYPT certificates do not embed original email subject material.

Verification against an email subject therefore requires the verifier to possess the original message bytes, or an export that canonicalizes to the same `canonical_bytes(subject)`, whenever the applicable verification path requires subject recomputation.

A conforming verifier toolkit supports original-material comparison for this profile. The comparison is against the exact emitted message supplied to the profile, subject only to the deterministic transformations defined by the normative algorithm. It does not infer that a mailbox export, a received copy, or regenerated MIME is the same emitted message.

That remains fully offline-capable.

It does not justify:

- hosted truth services
- resolver authority
- managed interpretation shortcuts
- semantic upgrades from packaging convenience

---

### Anti-notarization boundary

`subject.email/1` must not be read as a notarization profile.

It defines email-message canonicalization only.

It does not define:

- timestamping semantics
- anchoring semantics
- proof-of-existence semantics
- proof-of-independence semantics

If an email artifact is later used inside a CERTCRYPT `Independent` path, that meaning comes from the higher-layer issuance, leaf, settlement, proof, and verifier semantics, not from this profile alone.

---

## Reading guide

Recommended order for implementers and auditors:

1. [foundation](../../../foundation/index.md)
2. [CCCP/1](../../../protocols/CCCP/1/index.md)
3. [CCSP/1](../../../protocols/CCSP/1/index.md)
4. [subject.binary/1](../../subject.binary/1/index.md)
5. [subject.email/1/specification](./specification.md)
6. [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md)

---

## Versioning

- **Specification identifier:** `subject.email`
- **Specification version:** `/1`

Version `/1` defines the first canonical email-message canonicalization profile under the active corpus.

Changes that alter the input boundary, the canonicalization rule (line-ending normalization, header/body split, header unfolding, body trailing-terminator normalization, final assembly), the forbidden-transformation list, or the boundary between canonicalization and higher-layer semantics require a new major version.

Later versions do not retroactively reinterpret already valid email canonicalizations governed by `/1`.

---

## One-line summary

**`subject.email/1` defines the canonical bounded canonicalization profile for complete-message email input, producing deterministic `canonical_bytes(subject)` without semantic MIME reinterpretation, and without itself producing sender authenticity, delivery evidence, or `Independent`.**

---

## Normative reference

This overview is informational only.

All definitive rules and constraints are defined in:

- [subject.email/1/specification](./specification.md)

In case of discrepancy, the specification prevails.
