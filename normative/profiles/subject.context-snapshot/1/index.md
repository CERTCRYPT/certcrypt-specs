# subject.context-snapshot/1 · CERTCRYPT Context Snapshot Subject Canonicalization Profile

**Identifier:** `subject.context-snapshot/1`

**Label:** CERTCRYPT Context Snapshot Subject Canonicalization Profile v1

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
- [CCVP/1](../../../protocols/CCVP/1/index.md)

> This document is **informative**.
> The normative requirements for `subject.context-snapshot/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `subject.context-snapshot/1`?

`subject.context-snapshot/1` defines the canonicalization boundary for context snapshot subjects under CERTCRYPT public rules.

It defines:

- what counts as the exact context-snapshot input boundary
- how `canonical_bytes(subject)` are produced deterministically
- which transformations are forbidden
- which interpretation and verification claims remain outside the profile

It does **not** define:

- issuance semantics
- independence semantics
- settlement semantics
- truth, legality, or institutional endorsement

---

## Architectural role

`subject.context-snapshot/1` is a subject canonicalization profile only.

Within the architecture:

- `system-domain/1` determines which system is being evaluated
- `rules-domain/1` determines which exact public rules apply
- `security-model/1` defines the interpretation and failure boundary
- `CCCP/1` defines canonicalization contexts, hashing, and commitment semantics
- `CCSP/1` defines certificate envelope structure
- `CCVP/1` defines context snapshot meaning and verifier-side consistency behavior
- `subject.context-snapshot/1` defines how a context snapshot subject becomes `canonical_bytes(subject)`

Under `/1`, the profile never upgrades a subject into `Issued` or `Independent`.

It contributes only the subject-side canonical bytes required by higher layers.

---

## Normative documents

The normative component of `subject.context-snapshot/1` is:

- [Specification](./specification.md)

The specification defines:

- context-snapshot input boundary
- deterministic canonicalization rules
- forbidden transformations
- profile-verification boundary
- interpretation and misuse boundaries

---

## Related documents

- [Overview](./overview.md)
- [CCVP/1](../../../protocols/CCVP/1/index.md)
- [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md)

---

## Versioning

- **Profile identifier:** `subject.context-snapshot`
- **Profile version:** `/1`

Version `/1` defines the first context-snapshot subject profile.

Any change that alters:

- the context-snapshot input boundary
- canonical byte output
- forbidden transformations
- profile-verification meaning

requires a new major version.

Already valid results under `/1` are not retroactively reinterpreted by later versions.

---

## One-line summary

**`subject.context-snapshot/1` defines how context snapshot subjects are reduced to deterministic canonical bytes without redefining system, proof, settlement, or authority semantics.**
