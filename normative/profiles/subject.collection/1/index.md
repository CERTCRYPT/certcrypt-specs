# subject.collection/1 · CERTCRYPT Collection Subject Canonicalization Profile

**Identifier:** `subject.collection/1`

**Label:** CERTCRYPT Collection Subject Canonicalization Profile v1

**Page:** Informative version index

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
> The normative requirements for `subject.collection/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `subject.collection/1`?

`subject.collection/1` defines the canonicalization boundary for issuer-declared collection subjects under CERTCRYPT public rules.

It defines:

- what counts as the exact collection subject input boundary
- which structural fields are normatively meaningful
- how `canonical_bytes(subject)` are produced deterministically
- which interpretation and verification claims remain outside the profile

It does **not** define:

- issuance semantics
- quantity or pricing rules
- independence semantics
- inclusion-proof semantics
- truth, legality, or institutional endorsement

---

## Architectural role

`subject.collection/1` is a subject canonicalization profile only.

Within the current architecture:

- `system-domain/1` determines which system is being evaluated
- `rules-domain/1` determines which exact public rules apply
- `security-model/1` defines the interpretation and failure boundary
- `CCCP/1` defines canonicalization, hashing, and commitment semantics
- `CCSP/1` defines certificate envelope structure
- `subject.collection/1` defines how an issuer-declared collection subject becomes `canonical_bytes(subject)`

Under `/1`, the profile never upgrades a subject into `Issued` or `Independent`.

It contributes only the subject-side canonical bytes required by higher layers.

---

## Normative documents

The normative component of `subject.collection/1` is:

- [Specification](./specification.md)

The specification defines:

- collection subject input boundary
- deterministic canonicalization rules
- required structural fields
- forbidden transformations
- profile-verification boundary
- interpretation and misuse boundaries

---

## Related documents

- [Overview](./overview.md)
- [collection.merkle-sha3-256/1](../../../protocols/commitment/collection.merkle-sha3-256/1/index.md)
- [subject.binary/1](../../subject.binary/1/index.md)
- [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md)
- [submission-set/1](../../../protocols/settlement/submission-set/1/index.md)
- [capacity.commitment/1](../../../ecosystem/settlement/capacity.commitment/1/index.md)

---

## Versioning

- **Profile identifier:** `subject.collection`
- **Profile version:** `/1`

Version `/1` defines the first collection-subject profile for the current CERTCRYPT architecture.

Any change that alters:

- the collection subject input boundary
- canonical byte output
- required structural fields
- profile-verification meaning

requires a new major version.

Already valid results under `/1` are not retroactively reinterpreted by later versions.

---

## One-line summary

**`subject.collection/1` defines how issuer-declared collection subjects are reduced to deterministic canonical bytes without redefining system, proof, settlement, quantity, or authority semantics.**
