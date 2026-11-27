# subject.email/1 · CERTCRYPT Email Subject Canonicalization Profile

**Identifier:** `subject.email/1`

**Label:** CERTCRYPT Email Subject Canonicalization Profile v1

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
> The normative requirements for `subject.email/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `subject.email/1`?

`subject.email/1` defines the canonicalization boundary for complete email-message subjects under CERTCRYPT public rules.

It defines:

- what counts as acceptable message input
- how the header and body sections are split and deterministically canonicalized
- which minimal transformations are permitted
- which interpretation and verification claims remain outside the profile

It does **not** define:

- issuance semantics
- independence semantics
- consistency meaning
- package semantics
- truth, legality, or institutional endorsement

---

## Architectural role

`subject.email/1` is a subject canonicalization profile only.

Within the current architecture:

- `system-domain/1` determines which system is being evaluated
- `rules-domain/1` determines which exact public rules apply
- `security-model/1` defines the interpretation and failure boundary
- `CCCP/1` defines canonicalization, hashing, and commitment semantics
- `CCSP/1` defines certificate envelope structure
- `subject.email/1` defines how a complete email message becomes `canonical_bytes(subject)`

Under `/1`, the profile never upgrades a subject into `Issued` or `Independent`.

It contributes only the subject-side canonical bytes required by higher layers.

---

## Normative documents

The normative component of `subject.email/1` is:

- [Specification](./specification.md)

The specification defines:

- message-input boundary
- deterministic email canonicalization rules
- header/body processing boundary
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

- **Profile identifier:** `subject.email`
- **Profile version:** `/1`

Version `/1` defines the first canonical email-message profile for the current CERTCRYPT architecture.

Any change that alters:

- the message input boundary
- canonical byte output
- header or body normalization behavior
- forbidden transformations

requires a new major version.

Already valid results under `/1` are not retroactively reinterpreted by later versions.

---

## One-line summary

**`subject.email/1` defines how complete email-message subjects are reduced to deterministic canonical bytes without redefining system, proof, settlement, or authority semantics.**
