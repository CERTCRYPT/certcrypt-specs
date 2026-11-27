# Overview · capacity.evidence/1

**Identifier:** `capacity.evidence/1`

**Label:** CERTCRYPT Capacity Evidence Specification (capacity.evidence/1)

**Page:** Informative overview

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

> This document is **informative**.
> The normative requirements live in [specification.md](./specification.md).
> Where the two differ, the specification prevails.

---

## The problem it solves

CERTCRYPT's anti-notarization property — that `Independent` reflects authorized, consumed, scarce capacity, not a free hash — is enforced when a commitment is submitted, online. But the public promise is about **offline** verification: a verifier holding the artifacts should be able to check it without calling CERTCRYPT.

To re-verify the holder's signature offline, a verifier needs the holder's key. A stable holder key would correlate every certificate that holder signs. `capacity.evidence/1` is how the verifier gets to re-verify the chain **for real** while keeping the protocol surface structurally unlinkable. Evidence objects carrying the same stable `holder_key_set_root` remain correlatable on the artifact surface (§9).

---

## What it is

A derived, minimal projection of one `capacity.commitment/1` and the `capacity.holder-authorization/1` that authorizes it:

- **projected authorization** — carries the `holder_key_set_root` and the system-domain Level-1 signature over it (the trust anchor: it proves the root was authorized, not fabricated)
- **projected commitment** — the commitment's fields with stable identifiers replaced by operation-scoped pseudonyms, signed by a per-operation leaf key
- **operation-key disclosure** — that one leaf key plus its membership proof to the root
- **commitment signature** — the holder's real ML-DSA-65 signature over the projected commitment

Its signed commitment is the only wire form of a capacity commitment: it carries only what the offline proof needs and exposes no stable personal or business identifier. The stable `holder_key_set_root` is the deliberate exception: an observer holding multiple evidence objects with the same root can correlate them as belonging to the same authorized key-set (§9).

---

## The four-step trust, offline

A verifier with only the evidence, the system-domain public key, and public rules:

1. verifies the **Level-1 signature** over the `holder_key_set_root` → the root is system-domain-authorized
2. verifies the disclosed leaf is a **member** of that root
3. verifies the **commitment signature** against that leaf → a real holder signature, not an opaque commitment
4. checks the **pseudonym bindings** tie commitment and authorization together, and the **evidence digest** matches what `independence.proof/1` bound

That establishes authorized capacity. Consumption is a separate, settlement-bound step (`capacity.commitment/1 §9`); authorization is its precondition (`independence.proof/1 §12.5`).

---

## Two canonicalizations (the easy thing to get wrong)

- **signing bytes** (what a signature covers — the projected commitment, the Level-1 binding): insertion order, NOT JCS. Field order is the contract.
- **evidence digest** (what binds to the proof): RFC 8785 JCS, sorted keys.

Applying JCS to the signing bytes, or insertion order to the digest, breaks verification silently. This is covered by the conformance suite.

---

## What it does NOT do

- It does not prove consumption — that is settlement-bound.
- It does not prove `Independent` — that is the whole proof plus settlement.
- It does not redefine the Merkle primitive (`holder-keyset.merkle-sha3-256/1`) or pseudonym derivation (CCCP/1 §7.4); it composes them.
- It does not promise observer-side inobservability of a received artifact — only protocol-surface unlinkability (specification.md §9).

---

## Related

- [Specification](./specification.md)
- [CCCP/1 §7.4](../../../../protocols/CCCP/1/index.md) — pseudonym derivation
- [holder-keyset.merkle-sha3-256/1](../../../../protocols/commitment/holder-keyset.merkle-sha3-256/1/index.md) — key-set root + membership
- [capacity.commitment/1](../../capacity.commitment/1/index.md) · [capacity.holder-authorization/1](../../capacity.holder-authorization/1/index.md)
- [independence.proof/1](../../../../models/independence.proof/1/index.md) · [verification-package/1](../../../verification/verification-package/1/index.md)
