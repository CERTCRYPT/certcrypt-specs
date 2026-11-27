# capacity.evidence/1 · CERTCRYPT Capacity Evidence

**Identifier:** `capacity.evidence/1`

**Label:** CERTCRYPT Capacity Evidence Specification (capacity.evidence/1)

**Page:** Informative version index

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

**Depends on:** `system-manifest/1`, `system-domain/1`, `rules-domain/1`, `CCCP/1`, `holder-keyset.merkle-sha3-256/1`, `capacity.commitment/1`, `capacity.holder-authorization/1`

> This document is **informative**.
> The normative requirements for `capacity.evidence/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `capacity.evidence/1`?

`capacity.evidence/1` is the offline-transportable, zero-data projection of a holder's authorized-and-signed `capacity.commitment/1`. It lets an offline verifier re-run the capacity authorization proof for one certificate's commitment — verifying the system-domain authorization and the holder signature for real — without receiving personal data or stable business identifiers in clear. Its unlinkability guarantee applies to the protocol surface; evidence objects carrying the same stable `holder_key_set_root` remain correlatable to an observer who holds them (§9).

It defines:

- the object layout (projected authorization, projected commitment, operation-key disclosure, signature)
- the two canonicalizations (insertion-order signing bytes; JCS evidence digest)
- the offline verification procedure (§8, steps 1–7)
- fail-closed conditions

It does **not** define:

- consumption (settlement-bound, `capacity.commitment/1 §9`)
- the Merkle key-set primitive (`holder-keyset.merkle-sha3-256/1`) or pseudonym derivation (CCCP/1 §7.4) — referenced, not redefined
- `Issued` or `Independent`

---

## Architectural role

`capacity.evidence/1` is the offline counterpart of the online capacity chain.

- `capacity.holder-authorization/1` commits to a `holder_key_set_root`; `capacity.commitment/1` is the commitment model whose only wire form is this artifact's `projected_commitment`.
- `capacity.evidence/1` is the **derived** projection of both, carrying only what the offline capacity proof needs, with stable business identifiers replaced by pseudonyms and the stable holder key replaced by a non-reused operation leaf key. The authorized key-set root remains stable and visible by design, so artifact-side correlation by root remains possible (§9).
- it travels under `supporting_material.capacity_evidence` of a [verification-package/1](../../../verification/verification-package/1/index.md), is bound to the commitment it backs because its digest IS that commitment's `commitment_id` (§7.1) listed in [independence.proof/1](../../../../models/independence.proof/1/index.md), and is consumed by [verifier-toolkit/1](../../../verification/verifier-toolkit/1/index.md).

It establishes that consumption was **authorized**; it does not establish consumption, which is settlement-bound.

---

## Normative documents

- [Specification](./specification.md)

---

## Related documents

- [Overview](./overview.md)
- [CCCP/1](../../../../protocols/CCCP/1/index.md)
- [holder-keyset.merkle-sha3-256/1](../../../../protocols/commitment/holder-keyset.merkle-sha3-256/1/index.md)
- [capacity.commitment/1](../../capacity.commitment/1/index.md)
- [capacity.holder-authorization/1](../../capacity.holder-authorization/1/index.md)
- [independence.proof/1](../../../../models/independence.proof/1/index.md)

---

## Versioning

- **Specification identifier:** `capacity.evidence`
- **Specification version:** `/1`

Any change to the object layout, signing-bytes order, canonicalization rules, signature targets, or verification procedure requires a new major version.

---

## One-line summary

**`capacity.evidence/1` is the zero-data projection of an authorized capacity commitment that an offline verifier re-verifies in place of the online capacity chain, with protocol-surface unlinkability and the explicit artifact-side correlation boundary of §9.**
