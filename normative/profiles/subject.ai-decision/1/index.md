# subject.ai-decision/1 · CERTCRYPT AI-Decision Subject Canonicalization Profile

**Identifier:** `subject.ai-decision/1`

**Label:** CERTCRYPT AI-Decision Subject Canonicalization Profile v1

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
> The normative requirements for `subject.ai-decision/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `subject.ai-decision/1`?

`subject.ai-decision/1` defines the canonicalization boundary for a record of one AI decision under CERTCRYPT public rules.

It defines:

- what counts as the exact decision-record input boundary
- the required and optional fields of a decision record
- how `canonical_bytes(subject)` are produced deterministically (RFC 8785 JCS, with arrays only for ordered input and output descriptors)
- which transformations are forbidden
- which interpretation and verification claims remain outside the profile

It does **not** define:

- whether the decision is correct, fair, lawful, or unbiased
- model quality, accuracy, safety, or reproducibility
- the semantics of the decision input or output (carried only as salted commitments)
- truth, legality, or institutional endorsement

---

## Architectural role

`subject.ai-decision/1` is a subject canonicalization profile only.

Within the current architecture:

- `system-domain/1` determines which system is being evaluated
- `rules-domain/1` determines which exact public rules apply
- `security-model/1` defines the interpretation and failure boundary
- `CCCP/1` defines canonicalization contexts, hashing, and commitment semantics
- `CCSP/1` defines certificate envelope structure
- `subject.ai-decision/1` defines how a decision record becomes `canonical_bytes(subject)`

Under `/1`, the profile never upgrades a subject into `Issued` or `Independent`, and never asserts anything about the merit of the decision.

It contributes only the subject-side canonical bytes required by higher layers.

---

## Zero-data posture

The decision's actual inputs and outputs are NEVER embedded in the record. Each side is a non-empty ordered array of closed material descriptors containing an opaque part identifier, role, media type, subject profile, independently generated material nonce, and CCCP/1 commitment. The materials themselves are verifier-held original material under verifier-toolkit/1 §8.5. CERTCRYPT retains nothing about the decision's content.

Although the record binds the order and cardinality of multiple parts, it is one non-collection subject for one observable invocation and decision: it defines no Merkle root or element-inclusion proof and contributes one economic unit under rules that count a non-collection subject as one.

---

## Verifying the input and output

A verifier that also holds any declared input or output part can deliver it with the record, keyed by the part's globally unique `id`: the toolkit canonicalizes it under the named profile, derives the commitment with the descriptor's `material_nonce_hex`, and compares it with `commitment_digest_hex` (verifier-toolkit/1 §8.5.6). The profiles a descriptor may declare are `subject.text/1`, `subject.binary/1`, `subject.email/1` and `subject.ai-decision/1`.

---

## Normative documents

The normative component of `subject.ai-decision/1` is:

- [Specification](./specification.md)

---

## Related documents

- [Overview](./overview.md)
- [CCCP/1](../../../protocols/CCCP/1/index.md)
- [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md)

---

## Versioning

- **Profile identifier:** `subject.ai-decision`
- **Profile version:** `/1`

Version `/1` defines the first AI-decision subject profile for the current CERTCRYPT architecture. Any change that alters the input boundary, canonical byte output, the member set, or forbidden transformations requires a new major version. Already valid results under `/1` are not retroactively reinterpreted by later versions.

---

## One-line summary

**`subject.ai-decision/1` defines how one observable model invocation and decision record is reduced to deterministic canonical bytes — committing its declared circumstances and ordered material descriptors, never its correctness.**
