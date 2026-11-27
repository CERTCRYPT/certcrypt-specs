# CERTCRYPT Holder Operation-Key Set Commitment Scheme (`holder-keyset.merkle-sha3-256/1`)

**Identifier:** `holder-keyset.merkle-sha3-256/1`

**Label:** CERTCRYPT Holder Operation-Key Set Commitment Scheme v1

**Type:** Protocol

**Status:** Frozen

**Layer:** Layer 1 — Protocols

**Depends on:**
- [system-domain/1](../../../../foundation/system-domain/1/index.md)
- [rules-domain/1](../../../../foundation/rules-domain/1/index.md)
- [security-model/1](../../../../foundation/security-model/1/index.md)
- [CCCP/1](../../../CCCP/1/index.md)

**Naming convention:**
`holder-keyset.merkle-sha3-256/1` is the formal identifier.
CERTCRYPT Holder Operation-Key Set Commitment Scheme v1 is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.

**Audience:** Protocol implementers, verifiers, auditors

**Purpose:** Define the normative interoperable root-construction and inclusion-proof semantics for a holder's set of per-operation signing keys, so that a Level-2 authorization can commit to a `holder_key_set_root` and each `capacity.commitment/1` can disclose one operation-key leaf with a membership proof — without exposing a stable holder verification key.

**Intended use:** `holder-keyset.merkle-sha3-256/1` is the authoritative public specification for computing a `holder_key_set_root` over a set of operation public keys and for verifying that one disclosed operation public key is a member of that root. It is the key-material primitive of the zero-data capacity profile: it lets an offline verifier re-verify a holder signature against a per-operation leaf key while binding that leaf to a system-domain-authorized root.

**Scope:** Defines exact leaf-hash input, internal-node hash input, tree shape, ordering, duplicate handling, odd-width handling, the disclosure object model, and the membership-verification procedure. Higher-layer signature semantics, authorization anchoring, pseudonym derivation, capacity consumption, and proof acceptance remain out of scope except where explicitly referenced.

**Non-goals:** `holder-keyset.merkle-sha3-256/1` does not by itself authorize a holder, verify any signature, prove capacity consumption, or establish `Independent`. Membership in a root proves only that a disclosed key belongs to a committed set; it does not prove that the set was authorized (that is the consuming specification's Level-1 anchoring obligation) and it does not prove that the key signed anything (that is a separate signature check). It MUST NOT be interpreted as a trust mark, notarization mechanism, or live service authority.

> This document is **normative**.
> All requirements expressed using MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in RFC 8174.

---

## 1. Background & rationale

The zero-data capacity profile re-verifies a holder's Level-3 signature offline without shipping a stable holder verification key, because a stable key is a cross-certificate correlator: re-checking a signature requires the public key, and the same public key across many commitments links them all.

`holder-keyset.merkle-sha3-256/1` closes that gap. Instead of authorizing one stable holder public key, a Level-2 authorization commits to a **Merkle root over a set of per-operation holder keys** (`holder_key_set_root`). Each `capacity.commitment/1` is signed by a **distinct, non-reused leaf key**, and the evidence discloses that one leaf key plus a Merkle inclusion proof binding it to the authorized root.

Two commitments from the same holder then share only the root. The root travels in clear in the capacity evidence and is never anchored on the protocol surface, so a recipient holding two evidence objects can recognize them as issued under the same authorized key set (`capacity.evidence/1` §9). They expose different, non-reused leaf keys, so they are not linkable by key.

This scheme introduces no new cryptography: it is SHA3-256 (CCCP/1 §7.1) over a fixed Merkle construction. It uses the same tree shape (ordering, odd-node promotion, proof walk) as [collection.merkle-sha3-256/1](../../collection.merkle-sha3-256/1/index.md), but not its domain tags: its leaf and node hashes use the single-byte prefixes of the aggregated settlement Merkle tree (`settlement.binding/1` §6), and its leaf input is an operation public key rather than a collection-subject canonicalization (§6).

---

## 2. Conformance

A conforming implementation MUST implement every MUST in this document.
A conforming verifier MUST fail closed when any MUST is unsatisfied.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 (BCP 14).

Additional terms:

- **Operation key:** one signing keypair used by the holder to sign at most one `capacity.commitment/1`.
- **Operation public key:** the public half of an operation key, as carried in a disclosure.
- **Holder key set:** the ordered set of operation keys a single Level-2 authorization commits to.
- **`holder_key_set_root`:** the Merkle root over the holder key set, in 64-character lowercase hexadecimal.
- **Disclosure:** the per-commitment object revealing one operation public key, its zero-based index, the tree size, and its inclusion proof.

---

## 4. Design principles

- **Determinism:** the same ordered operation public keys MUST produce the same `holder_key_set_root` everywhere.
- **Zero-data:** the scheme carries only operation public keys, positions, and hashes; no stable holder identifier and no secret key material appear in any disclosed object.
- **Non-reuse is an emission invariant:** unlinkability across commitments depends on each leaf signing at most one commitment. The offline verifier cannot detect reuse (it holds no global state); the holder is responsible for never assigning the same leaf to two commitments. See §12.1.
- **Membership is not authorization:** binding a leaf to a root proves set membership only. Authorization of the root itself is the consuming specification's obligation (a Level-1 system-domain signature over the root).

---

## 5. Binary encoding conventions

- `u64be(n)` means the unsigned 64-bit big-endian encoding of non-negative integer `n`.
- All hash digests under this specification are 32-byte SHA3-256 outputs (CCCP/1 §7.1).
- All externally serialized digest strings MUST use 64-character lowercase hexadecimal encoding.
- An operation public key is carried in a disclosure as canonical base64: RFC 4648 standard alphabet, with padding, and with the unused low bits of the last character before the padding set to zero (RFC 4648 §3.5), so one key has exactly one accepted spelling. Its raw decoded bytes are what enter the leaf hash.
- Integers in a disclosure are JSON integers: JSON numbers with no fractional part and no exponent, within `0 … 2^53 − 1` so that every JSON implementation represents them exactly. A string, a fraction, a negative value or a boolean is not an integer.

---

## 6. Domain prefixes

Leaf and internal-node preimages are separated from each other by a single leading byte:

- leaf prefix: `0x00`
- internal-node prefix: `0x01`

These prefix bytes MUST be used exactly. Implementations MUST NOT substitute string domain tags or any other framing.

The two prefixes separate a leaf from an internal node within one tree; they are not specific to this scheme. They are the same bytes the aggregated settlement Merkle tree uses (`settlement.binding/1` §6), and [collection.merkle-sha3-256/1](../../collection.merkle-sha3-256/1/index.md), which uses string domain tags instead, shares only the tree shape. What keeps a holder key set root apart from a settlement root is its context and its leaf input: a holder key set root is only ever checked against the `holder_key_set_root` a Level-1 signature authorized, with leaves that are raw operation public keys, while a settlement leaf hashes a canonical leaf preimage and is checked against a settlement root. A value is never accepted as one kind of root because it verifies as the other.

---

## 7. Leaf hash construction

Each leaf is one operation public key. For one operation public key with raw decoded bytes `pubkey_bytes`:

```text
leaf_preimage = 0x00 || pubkey_bytes
leaf_hash     = SHA3-256(leaf_preimage)
```

No other leaf-hash construction is valid under `/1`.

The leaf index does not appear inside the leaf preimage. Position sensitivity comes from ordered tree placement, not from modifying leaf-hash input by index.

---

## 8. Internal node construction

For two child hashes `left_hash` and `right_hash`, each exactly 32 bytes (the raw decoded bytes of their hexadecimal encodings):

```text
node_preimage = 0x01 || left_hash || right_hash
node_hash     = SHA3-256(node_preimage)
```

No other internal-node construction is valid under `/1`.

---

## 9. Ordering, duplicates, and tree shape

### 9.1 Ordering

Operation keys MUST be interpreted in one exact zero-based order — the order the holder fixed when the authorization committed to the root. Implementations MUST NOT sort keys by value or by hash, deduplicate them, or reorder them by external metadata.

### 9.2 Duplicates

Distinct operation keys are expected. If two leaves were to produce the same `leaf_hash`, they still occupy distinct positions if they hold different indices. The scheme preserves ordered membership positions only; it does not interpret duplicates semantically. A holder SHOULD NOT generate duplicate operation keys.

### 9.3 Odd-width levels

If a tree level contains an odd number of hashes, the last hash at that level MUST be promoted unchanged to the next level. It MUST NOT be duplicated, rehashed alone, or paired with itself.

### 9.4 Empty set prohibition

The holder key set MUST contain at least one operation key. An empty set is invalid under `/1`.

---

## 10. Root computation procedure

Given the ordered operation public keys:

1. Compute one `leaf_hash` per operation public key in order (§7).
2. If there is exactly one leaf, the root is that `leaf_hash`.
3. Otherwise, repeatedly derive the next level left to right:
   - pair adjacent hashes
   - compute one internal node per adjacent pair (§8)
   - if one unpaired hash remains at the right edge, promote it unchanged (§9.3)
4. Continue until exactly one hash remains.
5. Encode that final 32-byte hash as a 64-character lowercase hexadecimal string.

That final string is the `holder_key_set_root`.

---

## 11. Disclosure object model

A disclosure reveals one operation key's membership for one commitment. When serialized as JSON under `/1`, it MUST be a JSON object containing exactly:

- `leaf_index`
- `public_key_b64`
- `inclusion_proof`
- `tree_size`

### 11.1 `leaf_index`

MUST be present. The zero-based position of the disclosed operation key in the ordered set: a JSON integer (§5) with `0 <= leaf_index < tree_size`.

### 11.2 `public_key_b64`

MUST be present. The operation public key, canonical base64 (§5). Its raw decoded bytes are the leaf input (§7).

### 11.3 `inclusion_proof`

MUST be present. A JSON array; each entry a 64-character lowercase hexadecimal string (`0-9`, `a-f`). An uppercase or otherwise non-canonical entry is not another spelling of the same proof: it fails (§13). Entries appear in bottom-up order, exactly one sibling hash per tree level at which the current node has a sibling. Levels at which the current node is promoted unchanged as the odd rightmost node contribute no entry.

### 11.4 `tree_size`

MUST be present. The total number of leaves in the holder key set: a JSON integer (§5), at least 1. It bounds `leaf_index` and fixes the odd-width interpretation at each level. A producer MUST disclose the actual number of leaves the root was computed over.

The root does not commit to `tree_size`. A verifier therefore cannot tell the actual size from another value that walks the same path: leaf 0 of a four-leaf tree, for one, consumes the same two siblings with the same orientation whether `tree_size` is 3 or 4, and both verify. Such a value proves the same membership with different disclosure bytes. That is acceptable for membership, which is all this scheme proves, and it is why a disclosure is never an identity (§12.2).

### 11.5 Position metadata is acceptable; identity is not

`(tree_size, leaf_index)` is public metadata acceptable by design: leaf indices need not follow an observable temporal order (the holder MAY assign leaves in any order from a sparse set), so position carries no timing or sequence signal an observer could use to link operations. A stable key, the holder identifier and the authorization identifier never appear: the leaf key is per-operation, and the identifiers are projected to operation-scoped pseudonyms by the consuming specification. The root itself travels in clear, which lets a holder of two evidence objects recognize the same authorized key set; that boundary is defined by `capacity.evidence/1` §9.

### 11.6 No additional disclosure fields

When serialized as JSON under `/1`, a disclosure MUST NOT contain additional members. Implementations MUST reject additional members rather than ignoring them.

---

## 12. Membership verification procedure

To verify that one disclosed operation public key is a member of an authorized `holder_key_set_root`, the implementation MUST have the disclosure (§11) and the `holder_key_set_root`.

1. Decode `public_key_b64` to raw bytes; reject if undecodable.
2. Compute `leaf_hash` from those bytes (§7).
3. Parse `tree_size` as a positive integer `N` and `leaf_index` as a non-negative integer `i`; reject if `i >= N`.
4. Initialize `current_hash = leaf_hash`, `current_index = i`, `current_width = N`, `proof_cursor = 0`.
5. While `current_width > 1`:
   - if `current_index` is the last index of an odd-width level and therefore has no sibling, promote `current_hash` unchanged;
   - otherwise consume exactly one entry from `inclusion_proof` at `proof_cursor`: if `current_index` is even, `current_hash = node_hash(current_hash, sibling)`; if odd, `current_hash = node_hash(sibling, current_hash)`.
   - then set `current_index = floor(current_index / 2)` and `current_width = ceil(current_width / 2)`.
6. Reject if `proof_cursor` does not exactly equal the number of entries in `inclusion_proof` when the loop ends.
7. Encode the final `current_hash` as lowercase hexadecimal.
8. Accept only if the result exactly equals the authorized `holder_key_set_root`.

No conforming verifier MAY reorder sibling hashes, infer missing siblings, accept extra sibling hashes, ignore `tree_size` bounds, or apply another odd-width rule.

### 12.1 Membership is necessary, not sufficient

A successful membership check proves only that the disclosed key belongs to the committed set. The consuming specification MUST additionally:

- verify that the `holder_key_set_root` is authorized by a system-domain (Level-1) signature, so the root is not one the holder fabricated;
- verify the holder's signature over the commitment against the disclosed leaf key;
- enforce, as a holder emission invariant, that no leaf is reused across commitments (§4).

This scheme provides the membership step only.

### 12.2 Membership is not identity

A disclosure is not covered by any signature, and its `tree_size` is not committed to by the root (§11.4). Two disclosures with different bytes can therefore prove the same membership of the same key. A consuming specification MUST NOT use the disclosure's bytes, or any digest that covers them, as the identity of what the disclosed key signed. Where it needs such an identity — replay and exclusivity of a commitment, for one — it MUST derive it from the signed material alone (`capacity.evidence/1` §7.2, `submission-set/1` §9.1).

---

## 13. Failure conditions

Verification MUST fail if any of the following applies:

- `public_key_b64` is not canonical base64 (§5)
- the disclosure carries additional members beyond §11, or lacks one of them
- `tree_size` is not a JSON integer of at least 1, `leaf_index` is not a non-negative JSON integer, or `leaf_index >= tree_size`
- any `inclusion_proof` entry is not a 64-character lowercase hexadecimal string
- `proof_cursor` does not exactly consume `inclusion_proof`
- the recomputed root does not exactly equal the authorized `holder_key_set_root`

No partial or best-effort acceptance is permitted. A failure is a negative verdict, never an error of the implementation: a malformed entry MUST NOT be decoded leniently (a non-hex character read as zero, an uppercase digit accepted) and MUST NOT abort the surrounding evaluation.

The conformance suite pins these conditions: `fixtures/primitives/holder-keyset/` carries trees of 1, 2, 3, 4 and 5 keys, and full disclosures checked against a root, with the verdict each must yield.

---

## 14. Relationship to the zero-data capacity profile

This scheme provides the key-material commitment that the zero-data capacity profile builds on:

- `capacity.holder-authorization/1` commits to a `holder_key_set_root` instead of a stable holder public key, and a system-domain Level-1 signature anchors that root.
- `capacity.commitment/1` (projected form) is signed by one operation leaf key and carries the disclosure defined here.
- the offline verifier checks membership (this scheme), then the Level-1 anchoring of the root, then the commitment signature against the disclosed leaf, then the operation-scoped pseudonym bindings (CCCP/1 §7.4).

It defines the membership mechanics only; the authorization, signature, and pseudonym steps are defined by those specifications.

---

## 15. Versioning & extensibility

- **Protocol family identifier:** `holder-keyset.merkle-sha3-256`
- **Scheme version:** `/1`

Any change that alters leaf-hash input, node-hash input, tree shape, disclosure interpretation, or failure conditions requires a new major version. Already valid roots or disclosures under `/1` are not retroactively reinterpreted by later versions.

---

## 16. References

- [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../../CCCP/1/index.md) (§7.1 hashing, §7.4 pseudonym derivation)
- [collection.merkle-sha3-256/1](../../collection.merkle-sha3-256/1/index.md) (the sibling Merkle scheme; same tree shape, its own domain tags and leaf input)
- [settlement.binding/1](../../../../ecosystem/settlement/settlement.binding/1/index.md) (§6, the aggregated settlement Merkle tree whose leaf and node prefixes this scheme shares)
- [capacity.evidence/1](../../../../ecosystem/settlement/capacity.evidence/1/index.md) (§7.2, the replay identity derived from signed material)
- [submission-set/1](../../../settlement/submission-set/1/index.md) (§9.1, replay keyed on what the holder signed)
- [capacity.holder-authorization/1](../../../../ecosystem/settlement/capacity.holder-authorization/1/index.md)
- [capacity.commitment/1](../../../../ecosystem/settlement/capacity.commitment/1/index.md)
- [security-model/1](../../../../foundation/security-model/1/index.md)
- [rules-domain/1 — CERTCRYPT Rules Domain](../../../../foundation/rules-domain/1/index.md)
- [system-domain/1 — CERTCRYPT System Domain](../../../../foundation/system-domain/1/index.md)
