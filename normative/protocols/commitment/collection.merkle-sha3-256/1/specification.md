# CERTCRYPT Merkle Collection Commitment Scheme (`collection.merkle-sha3-256/1`)

**Identifier:** `collection.merkle-sha3-256/1`

**Label:** CERTCRYPT Merkle Collection Commitment Scheme v1

**Type:** Protocol

**Status:** Frozen

**Layer:** Layer 1 — Protocols

**Depends on:**
- [system-domain/1](../../../../foundation/system-domain/1/index.md)
- [rules-domain/1](../../../../foundation/rules-domain/1/index.md)
- [security-model/1](../../../../foundation/security-model/1/index.md)
- [CCCP/1](../../../CCCP/1/index.md)
- [subject.collection/1](../../../../profiles/subject.collection/1/index.md)

**Naming convention:**  
`collection.merkle-sha3-256/1` is the formal identifier.  
CERTCRYPT Merkle Collection Commitment Scheme v1 is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.

**Audience:** Protocol implementers, verifiers, auditors

**Purpose:** Define the normative interoperable root-construction and inclusion-proof semantics for collection subjects that declare `commitment_scheme = "collection.merkle-sha3-256/1"` within the active CERTCRYPT public architecture.

**Intended use:** `collection.merkle-sha3-256/1` is intended to be the authoritative public specification for deriving and verifying collection roots and element inclusion proofs under the declared `collection.merkle-sha3-256/1` scheme.

**Scope:** Defines exact leaf-hash input, internal-node hash input, tree shape, ordering, duplicate handling, odd-width handling, proof serialization model, and verification procedure for the declared `collection.merkle-sha3-256/1` collection commitment scheme; higher-layer proof acceptance, pricing, policy, and semantic truth remain out of scope except where explicitly referenced.

**Non-goals:** `collection.merkle-sha3-256/1` does not prove truth, completeness, distinctness, legal validity, or authority of hidden leaves by itself, and MUST NOT be interpreted as a trust mark, notarization mechanism, or live service authority.

> This document is **normative**.
> All requirements expressed using MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in RFC 8174.

---

## 1. Background & rationale

`subject.collection/1` allows an issuer to bind one exact `commitment_scheme`, one exact `root`, one exact `declared_cardinality`, and one declared profile per leaf without disclosing hidden leaf values to CERTCRYPT.

That profile deliberately does not define every possible collection commitment scheme.

`collection.merkle-sha3-256/1` closes that remaining interoperability gap for one exact scheme identifier:

```text
collection.merkle-sha3-256/1
```

This specification exists so that conforming implementations can:

- compute the same root from the same ordered leaf set
- interpret the same proof object the same way
- reject malformed or ambiguous proof material deterministically

It defines exact cryptographic commitment semantics only.

It does not redefine `subject.collection/1`, quantity semantics, verifier policy, or semantic truth.

---

## 2. Scope

`collection.merkle-sha3-256/1` defines:

- the exact scheme identifier governed by this specification
- the leaf input model
- the exact Merkle leaf-hash construction
- the exact internal-node hash construction
- the exact ordering and duplicate-handling rules
- the exact odd-width tree rule
- the exact prohibition of empty trees
- the exact logical proof object model
- the exact verification procedure
- failure conditions

`collection.merkle-sha3-256/1` does not define:

- the collection subject object itself
- every possible leaf profile
- every possible verifier policy for external workflows
- semantic acceptance of higher-order leaf compositions
- pricing

Those concerns remain defined elsewhere in the architecture.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

Additional terms:

- **Collection subject:** The exact `subject.collection/1` JSON object that declares `commitment_scheme = "collection.merkle-sha3-256/1"`.
- **Leaf subject value:** The exact original leaf value intended to be processed under the profile declared for it.
- **Leaf canonical bytes:** The exact `canonical_bytes(subject)` output produced by that leaf's declared profile when applied to one leaf subject value.
- **Leaf hash:** The SHA3-256 digest derived from one leaf canonicalization result under this scheme.
- **Internal node hash:** The SHA3-256 digest derived from two child hashes under this scheme.
- **Declared cardinality:** The exact positive integer value declared in the collection subject.
- **Leaf index:** The zero-based position of one leaf within the ordered hidden leaf sequence.
- **Sibling hash list:** The ordered list of sibling hashes carried by an inclusion proof, from the leaf level upward.

---

## 4. Design principles

`collection.merkle-sha3-256/1` is designed around the following principles:

- **Exact interoperability:** The same ordered leaf set MUST always produce the same root under the same per-leaf declared profiles.
- **Profile-bound leaf semantics:** Leaf hashing MUST bind each leaf's declared profile so that incompatible leaf interpretations cannot be substituted silently.
- **Position sensitivity:** Identical leaf values at different positions remain distinct by index and tree placement, not by semantic uniqueness claims.
- **Zero-data compatibility:** Root construction and proof verification MUST remain compatible with hidden leaves and independent evaluation.
- **Interpretation boundaries:** This scheme defines commitment and proof mechanics only. It does not determine truth, completeness, atomicity, or authority.

---

## 5. Scheme identifier

The exact collection commitment scheme identifier governed by this specification is:

```text
collection.merkle-sha3-256/1
```

Any workflow that declares another identifier is outside this specification.

---

## 6. Collection preconditions

For this scheme to apply, the collection subject MUST satisfy all of the following:

- it MUST conform to [subject.collection/1](../../../../profiles/subject.collection/1/index.md)
- its declared `commitment_scheme` MUST be exactly `collection.merkle-sha3-256/1`
- its declared `root` MUST be a 64-character lowercase hexadecimal string
- its declared `declared_cardinality` MUST be a positive canonical unsigned decimal string
- every entry of its declared `leaves` MUST identify one exact subject profile

The hidden leaf sequence governed by this scheme MUST:

- contain exactly `declared_cardinality` leaves
- preserve one exact zero-based order from index `0` through index `declared_cardinality - 1`
- be non-empty

An empty tree is forbidden under `/1`.

The exact leaf count is therefore bound at workflow level by the collection subject declaration together with this scheme's conformance rules.

Under `/1`, `declared_cardinality` is not separately re-encoded inside each leaf hash or internal node hash.

No implementation MAY treat the Merkle root alone as a substitute for the collection subject's declared `declared_cardinality` boundary.

---

## 7. Binary encoding conventions

This specification uses the following exact binary encoding helpers:

- `utf8(s)` means the UTF-8 bytes of string `s`
- `u64be(n)` means the unsigned 64-bit big-endian encoding of non-negative integer `n`

All hash digests under this specification are 32-byte SHA3-256 outputs.

All externally serialized digest strings under this specification MUST use 64-character lowercase hexadecimal encoding.

---

## 8. Domain tags

The following exact UTF-8 domain tags are fixed by `/1`:

- `CERTCRYPT:collection.merkle-sha3-256/1:leaf`
- `CERTCRYPT:collection.merkle-sha3-256/1:node`

These tags MUST be used exactly as written.

Implementations MUST NOT rewrite, normalize, shorten, localize, or version-strip them.

---

## 9. Leaf input model

Each leaf is defined by:

- the **collection salt** supplied by the calling profile
- the leaf's OWN declared profile, supplied per leaf by the calling profile
- one exact leaf subject value at one exact zero-based leaf index

The salt is an opaque byte string supplied per collection commitment. This scheme
fixes only that it is bound into every leaf preimage; it does NOT define where the
salt comes from, and MUST NOT assume any structure or meaning for it. The calling
subject profile is the sole authority on the salt's origin (see
`subject.collection/1`).

A salt MUST be supplied. An empty salt is not permitted under `/1`.

Because the salt is bound into every leaf, the same ordered list of leaf values
under the same per-leaf profiles produces a DIFFERENT `root` under a different salt.
That is the intended behavior: it prevents `leaf_hash` values from becoming stable
global identifiers of content across commitments.

The calling profile declares a profile PER LEAF (`subject.collection/1` §7.4.1), not
one profile for the whole collection.

A collection MAY therefore be heterogeneous: different leaves MAY be hashed under
different profiles within the same root. This scheme takes each leaf's profile as
supplied and MUST NOT assume that all leaves share one.

Leaf hashing MUST bind:

- the exact supplied collection salt
- the exact profile declared for THAT leaf
- the exact `canonical_bytes(subject)` output of the leaf subject value under that profile

This scheme does not require leaves to be semantically atomic.

If a leaf value is itself a higher-order composition, that remains outside what this scheme can inspect or validate.

---

## 10. Leaf hash construction

For one leaf subject value:

1. The implementation MUST obtain `collection_salt_bytes`, the exact salt supplied by the calling profile (§9). If no salt is supplied, or the supplied salt is empty, the implementation MUST fail closed.
2. The implementation MUST compute `leaf_profile_bytes = utf8(leaf_profile)`, where `leaf_profile` is the profile declared for THIS leaf.
3. The implementation MUST compute `leaf_canonical_bytes` by applying that exact declared profile to the exact leaf subject value.
4. The implementation MUST construct `leaf_preimage` as:

```text
utf8("CERTCRYPT:collection.merkle-sha3-256/1:leaf")
|| u64be(len(collection_salt_bytes))
|| collection_salt_bytes
|| u64be(len(leaf_profile_bytes))
|| leaf_profile_bytes
|| u64be(len(leaf_canonical_bytes))
|| leaf_canonical_bytes
```

The salt is length-prefixed and precedes the profile, so no salt/profile pair can be
reinterpreted as a different pair with the same concatenation.

5. The implementation MUST compute:

```text
leaf_hash = SHA3-256(leaf_preimage)
```

No other leaf-hash construction is valid under `/1`.

The leaf index does not appear directly inside the leaf preimage.

Position sensitivity comes from ordered tree placement, not from modifying leaf-hash input by index.

---

## 11. Internal node construction

For two child hashes `left_hash` and `right_hash`, each exactly 32 bytes:

1. The implementation MUST construct `node_preimage` as:

```text
utf8("CERTCRYPT:collection.merkle-sha3-256/1:node")
|| left_hash
|| right_hash
```

2. The implementation MUST compute:

```text
node_hash = SHA3-256(node_preimage)
```

No other internal-node construction is valid under `/1`.

---

## 12. Ordering, duplicates, and tree shape

### 12.1 Ordering

Leaves MUST be interpreted in one exact zero-based order.

The root is computed from that order exactly as declared by the issuer's hidden leaf sequence.

Implementations MUST NOT:

- sort leaves by value
- sort leaves by hash
- deduplicate leaves
- reorder leaves by external metadata

### 12.2 Duplicates

Duplicate leaf values are permitted.

If two leaves produce the same `leaf_hash`, they still remain distinct positions if they occupy different indices in the ordered leaf sequence.

This scheme does not interpret duplicate leaves semantically.

It only preserves ordered membership positions.

### 12.3 Odd-width levels

If a tree level contains an odd number of hashes, the last hash at that level MUST be promoted unchanged to the next level.

It MUST NOT be duplicated, rehashed alone, or paired with itself.

### 12.4 Empty tree prohibition

The tree MUST contain at least one leaf.

An empty tree is invalid under `/1`.

---

## 13. Root computation procedure

Given the ordered leaf sequence:

1. Compute one `leaf_hash` per leaf in order.
2. If there is exactly one leaf, the root is that `leaf_hash`.
3. Otherwise, repeatedly derive the next level from left to right:
   - pair adjacent hashes
   - compute one internal node per adjacent pair using Section 11
   - if one unpaired hash remains at the right edge, promote it unchanged
4. Continue until exactly one hash remains.
5. Encode that final 32-byte hash as a 64-character lowercase hexadecimal string.

That final string is the collection `root` under `collection.merkle-sha3-256/1`.

---

## 14. Inclusion proof model

This specification defines one exact logical inclusion-proof object model.

When a proof is serialized as JSON under `/1`, it MUST be a JSON object containing exactly:

- `proof_version`
- `leaf_index`
- `sibling_hashes`

### 14.1 `proof_version`

`proof_version` MUST be present.

It MUST be the exact string:

```text
collection.merkle-sha3-256/1
```

### 14.2 `leaf_index`

`leaf_index` MUST be present.

It MUST be a canonical unsigned base-10 integer string.

It MUST identify the zero-based leaf position being proven.

### 14.3 `sibling_hashes`

`sibling_hashes` MUST be present.

It MUST be a JSON array.

Each entry MUST be a 64-character lowercase hexadecimal string.

Entries MUST appear in bottom-up order.

The array MUST contain exactly one sibling hash for each tree level at which the current node has a sibling.

Levels at which the current node is promoted unchanged because it is the odd rightmost node MUST contribute no sibling-hash entry.

### 14.4 No additional proof fields

When a proof is serialized as JSON under `/1`, it MUST NOT contain additional members.

Implementations MUST reject additional members rather than ignoring them.

Future versions MAY define extended proof-object models, but `/1` does not permit optional or forward-compatible proof members.

---

## 15. Inclusion proof verification procedure

To verify one leaf against one collection subject under `/1`, the implementation MUST have:

- the exact collection subject conforming to `subject.collection/1`
- support for every declared leaf profile
- the exact leaf subject value to be checked
- one proof object conforming to Section 14

The implementation MUST then perform the following procedure:

1. Validate that the collection subject declares `commitment_scheme = "collection.merkle-sha3-256/1"`.
2. Parse `declared_cardinality` as a positive integer `N`.
3. Parse `leaf_index` as a non-negative integer `i`.
4. Reject if `i >= N`.
5. Compute the exact `leaf_hash` using Section 10.
6. Initialize:
   - `current_hash = leaf_hash`
   - `current_index = i`
   - `current_width = N`
   - `proof_cursor = 0`
7. While `current_width > 1`, evaluate the current level:
   - if `current_index` is the last index of an odd-width level, and therefore has no sibling:
     - promote `current_hash` unchanged
   - otherwise:
     - consume exactly one entry from `sibling_hashes` at `proof_cursor`
     - if `current_index` is even, compute `current_hash = node_hash(current_hash, sibling_hash)`
     - if `current_index` is odd, compute `current_hash = node_hash(sibling_hash, current_hash)`
8. After each level:
   - set `current_index = floor(current_index / 2)`
   - set `current_width = ceil(current_width / 2)`
9. Reject if `proof_cursor` does not exactly equal the number of entries in `sibling_hashes` when the loop ends.
10. Encode the final `current_hash` as lowercase hexadecimal.
11. Accept only if the resulting string exactly equals the collection subject's declared `root`.

No conforming verifier MAY:

- reorder sibling hashes
- infer missing siblings heuristically
- accept additional sibling hashes
- ignore `declared_cardinality` bounds
- verify under another odd-width rule

---

## 16. Failure conditions

Verification MUST fail if any of the following applies:

- the collection subject does not conform to `subject.collection/1`
- `commitment_scheme` is not exactly `collection.merkle-sha3-256/1`
- `root` is not a 64-character lowercase hexadecimal string
- `declared_cardinality` cannot be parsed as a positive integer
- a declared leaf profile is unsupported for the requested workflow
- a leaf subject value cannot be canonicalized under its declared profile
- `proof_version` differs
- `leaf_index` is missing, non-canonical, or out of bounds
- `sibling_hashes` contains malformed entries
- the proof contains additional members
- the proof contains too few or too many sibling hashes
- the recomputed root differs from the declared `root`

This scheme also MUST fail closed for any higher-layer workflow that requires semantic acceptance of leaves but lacks the applicable public rules for that semantic workflow.

A verification MUST also fail closed when:

- no collection salt is supplied, or the supplied salt is empty (§9, §10)
- the salt used for verification differs from the salt the commitment was built with —
  the recomputed root will differ, and the implementation MUST report the root mismatch
  rather than searching for a salt that fits

---

## 17. Relationship to `subject.collection/1`

`subject.collection/1` binds:

- `commitment_scheme`
- `root`
- `declared_cardinality`
- `leaves` (each entry declaring its own profile and commitment)

This scheme defines how to interpret those exact values when `commitment_scheme = "collection.merkle-sha3-256/1"`.

In particular:

- `declared_cardinality` determines the tree width and leaf-index bounds
- each leaf's declared profile participates directly in that leaf's hashing
- `root` is the exact lowercase hexadecimal encoding of the final Merkle root

This scheme does not reinterpret collection cardinality transitively or recursively.

It verifies one exact collection level only.

---

## 18. Relationship to quantity and verification rules

This scheme does not define pricing or fairness by itself.

However, it supports higher-layer workflows that:

- treat `declared_cardinality` as economically relevant declared quantity under public rules
- require element-level inclusion proof material for some verifier path
- fail closed when unsupported leaf profiles or unsupported collection schemes are encountered

Acceptance of a valid proof under this scheme does not prove that the full hidden collection is complete, truthful, or semantically acceptable for every external workflow.

---

### 18.1 Non-equivalence with settlement merkle constructions

This scheme defines subject-level collection commitment semantics only.

It MUST NOT be assumed to apply automatically to leaf-level, batch-level, or settlement-level Merkle constructions unless another specification explicitly says so.

Other CERTCRYPT Merkle constructions MAY use:

- different leaf-preimage models
- different binding fields
- different domain-separation conventions
- different proof-context semantics

For example, aggregated settlement profiles may commit batch-assignment leaves that bind settlement-specific fields such as batch identity, leaf commitment, authorization reference, and consumed quantity.

Such constructions are not interchangeable with `collection.merkle-sha3-256/1` merely because both use Merkle trees.

---

## 19. Security and interpretation boundaries

`collection.merkle-sha3-256/1`:

- does not prove authorship
- does not prove truth
- does not prove collection completeness
- does not prove leaf distinctness
- does not prove that hidden leaves are atomic
- does not prove `Independent`

It closes commitment and proof interoperability only.

Any interpretation beyond that remains governed by other applicable public rules.

---

## 20. Reference vectors

Golden vectors for this scheme are published in the CERTCRYPT Conformance Suite,
together with the generator that derives them from this specification and a
negative-inclusion case.

They live there and not here on purpose. A conformance vector is only worth
something if it is executed: the conformance suite recomputes every one of them
from the public rules on each run, so a vector that stopped matching this
specification would fail loudly instead of sitting in a directory being wrong.

A conforming implementation reproduces, for each declared leaf set, exactly the
`root` and exactly the `inclusion_proofs` those vectors carry. Two
implementations that disagree on any vector cannot both be conformant.

---

## 21. Versioning & extensibility

- **Protocol family identifier:** `collection.merkle-sha3-256`
- **Scheme version:** `/1`

Any change that alters leaf hashing, internal-node hashing, tree-shape rules, proof-object interpretation, or failure conditions MUST require a new major version.

No optional hashing or proof-verification behavior is permitted under `/1`.

---

## 22. References

- CERTCRYPT Specifications
    - [security-model/1 — CERTCRYPT Security Model](../../../../foundation/security-model/1/index.md)
    - [system-domain/1 — CERTCRYPT System Domain](../../../../foundation/system-domain/1/index.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../../../foundation/rules-domain/1/index.md)
    - [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../../CCCP/1/index.md)
    - [subject.collection/1 — CERTCRYPT Collection Subject Canonicalization Profile](../../../../profiles/subject.collection/1/index.md)
    - [verification/verifier-toolkit/1 — verifier-toolkit/1 · CERTCRYPT Verifier Toolkit Specification](../../../../ecosystem/verification/verifier-toolkit/1/index.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
    - [FIPS 202 — SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions](https://csrc.nist.gov/pubs/fips/202/final)

---

**End of collection.merkle-sha3-256/1**
