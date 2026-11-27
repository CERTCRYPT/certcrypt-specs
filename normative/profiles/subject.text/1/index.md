# subject.text/1 · CERTCRYPT Plain Text Subject Canonicalization Profile

**Identifier:** `subject.text/1`

**Label:** CERTCRYPT Plain Text Subject Canonicalization Profile v1

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
> The normative requirements for `subject.text/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `subject.text/1`?

`subject.text/1` defines the canonicalization boundary for plain text subjects under CERTCRYPT public rules.

It defines:

- what counts as text input for this profile
- which minimal transformations are permitted
- how `canonical_bytes(subject)` are produced deterministically
- which interpretation and verification claims remain outside the profile

It does **not** define:

- issuance semantics
- independence semantics
- consistency meaning
- package semantics
- truth, legality, or institutional endorsement

---

## Architectural role

`subject.text/1` is a subject canonicalization profile only.

Within the current architecture:

- `system-domain/1` determines which system is being evaluated
- `rules-domain/1` determines which exact public rules apply
- `security-model/1` defines the interpretation and failure boundary
- `CCCP/1` defines canonicalization, hashing, and commitment semantics
- `CCSP/1` defines certificate envelope structure
- `subject.text/1` defines how a plain text subject becomes `canonical_bytes(subject)`

Under `/1`, the profile never upgrades a subject into `Issued` or `Independent`.

It contributes only the subject-side canonical bytes required by higher layers.

---

## Normative documents

The normative component of `subject.text/1` is:

- [Specification](./specification.md)

The specification defines:

- plain-text input boundary
- deterministic line-ending normalization
- byte-preservation boundary
- forbidden transformations
- profile-verification boundary
- interpretation and misuse boundaries

---

## Related documents

- [Overview](./overview.md)
- [subject.binary/1](../../subject.binary/1/index.md)
- [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md)
- [verification-package/1](../../../ecosystem/verification/verification-package/1/index.md)

---

## Versioning

- **Profile identifier:** `subject.text`
- **Profile version:** `/1`

Version `/1` defines the first canonical plain-text profile for the current CERTCRYPT architecture.

Any change that alters:

- the text input boundary
- canonical byte output
- permitted normalization
- forbidden transformations

requires a new major version.

Already valid results under `/1` are not retroactively reinterpreted by later versions.

---

## One-line summary

**`subject.text/1` defines how plain text subjects are reduced to deterministic canonical bytes using only minimal explicit normalization and without redefining system, proof, settlement, or authority semantics.**
