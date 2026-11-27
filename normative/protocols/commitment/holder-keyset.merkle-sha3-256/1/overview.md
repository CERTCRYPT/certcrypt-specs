# Overview · holder-keyset.merkle-sha3-256/1

**Identifier:** `holder-keyset.merkle-sha3-256/1`

**Label:** CERTCRYPT Holder Operation-Key Set Commitment Scheme v1

**Page:** Informative overview

**Specification type:** Protocol

**Layer:** Layer 1 — Protocols

**Status:** Frozen

This page explains what the scheme is for and why it exists. The normative rules live in the [specification](./specification.md); where the two differ, the specification prevails.

---

## The problem it solves

To verify a holder's signature offline, a verifier needs the holder's public key. But a *stable* holder public key, reused across every commitment that holder signs, links all of those certificates together — it is a cross-certificate correlator. Shipping it would break the zero-data unlinkability the protocol promises.

`holder-keyset.merkle-sha3-256/1` removes the stable key. The holder generates a **set** of per-operation keys and commits to them with a single Merkle root, the `holder_key_set_root`. The authorization is issued once, offline, over that root. Each commitment is then signed by a **different, non-reused leaf key**, and the evidence discloses only that one leaf plus a short proof that it belongs to the authorized root.

Two commitments from the same holder share only the root. The root travels in clear in the capacity evidence, so a recipient holding two evidence objects can recognize them as issued under the same authorized key set; it is never anchored on the protocol surface ([capacity.evidence/1](../../../../ecosystem/settlement/capacity.evidence/1/index.md) §9). The leaf keys differ and are never reused, so the two commitments are not linkable by key.

---

## What it is, mechanically

The same tree shape (ordering, odd-node promotion, proof walk) as [collection.merkle-sha3-256/1](../../collection.merkle-sha3-256/1/index.md), with the leaf prefix `0x00` and node prefix `0x01` of the aggregated settlement Merkle tree (`settlement.binding/1` §6), applied to operation public keys instead of collection subjects:

- **leaf:** `SHA3-256(0x00 || operation_public_key_bytes)`
- **node:** `SHA3-256(0x01 || left || right)`
- **root:** folded left-to-right over the ordered key set
- **disclosure:** one leaf key, its index, the tree size, and its bottom-up sibling hashes

A verifier recomputes the leaf hash from the disclosed key, walks the siblings up, and accepts only if the result equals the authorized root.

No new cryptography: it is SHA3-256 over a fixed tree, with the same tree shape as [collection.merkle-sha3-256/1](../../collection.merkle-sha3-256/1/index.md) and the leaf and node prefixes of the settlement tree; what keeps its roots apart from settlement roots is their context and leaf input. A disclosure proves membership, never identity: its `tree_size` is not committed to by the root.

---

## What it does NOT do

Membership in the root proves only that a disclosed key belongs to a committed set. It is necessary but not sufficient. The consuming specification still has to:

- prove the root itself was **authorized** — a system-domain (Level-1) signature over the root, so a holder cannot fabricate their own root and pass membership against it;
- **verify the signature** of the commitment against the disclosed leaf key;
- enforce, as a holder emission invariant, that **no leaf is reused** across commitments — the verifier holds no global state and cannot detect reuse offline.

This scheme is one link in that chain, not the whole chain.

---

## Tree size and re-issuance

The tree size bounds how many unlinkable operations one authorization covers before it must be re-issued (offline, within the validity window). It is a sizing parameter, not a redesign: dimension it to the operations expected in the authorization window with margin. Revealing `(tree_size, leaf_index)` is acceptable by design — position carries no identity, only order, and the holder may assign leaves from a sparse set in any order.

---

## Related

- [Specification](./specification.md)
- [CCCP/1](../../../CCCP/1/index.md) — hashing (§7.1) and operation-scoped pseudonym derivation (§7.4)
- [collection.merkle-sha3-256/1](../../collection.merkle-sha3-256/1/index.md) — the sibling scheme
- [capacity.holder-authorization/1](../../../../ecosystem/settlement/capacity.holder-authorization/1/index.md) — commits to the root
- [capacity.commitment/1](../../../../ecosystem/settlement/capacity.commitment/1/index.md) — signed by one operation leaf, carries the disclosure
