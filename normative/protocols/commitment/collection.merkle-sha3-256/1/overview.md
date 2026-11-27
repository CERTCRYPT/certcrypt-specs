# CERTCRYPT Merkle Collection Commitment Scheme (`collection.merkle-sha3-256/1`) — overview

**Identifier:** `collection.merkle-sha3-256/1`

**Label:** CERTCRYPT Merkle Collection Commitment Scheme v1

**Page:** Informative overview

**Specification type:** Protocol

**Layer:** Layer 1 — Protocols

**Status:** Frozen

**Depends on:**

- [system-domain/1](../../../../foundation/system-domain/1/index.md)
- [rules-domain/1](../../../../foundation/rules-domain/1/index.md)
- [security-model/1](../../../../foundation/security-model/1/index.md)
- [CCCP/1](../../../CCCP/1/index.md)
- [subject.collection/1](../../../../profiles/subject.collection/1/index.md)

> This document is **informative**.
> The normative requirements for `collection.merkle-sha3-256/1` are defined exclusively in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `collection.merkle-sha3-256/1`?

`collection.merkle-sha3-256/1` defines one exact way to compute and verify a declared collection root using Merkle-SHA3-256.

It exists so that a `subject.collection/1` subject with:

```json
{
  "profile": "subject.collection/1",
  "commitment_scheme": "collection.merkle-sha3-256/1",
  "root": "<64-char lowercase hex>",
  "declared_cardinality": "<decimal string>",
  "leaves": [
    { "profile": "<subject profile>", "commitment_digest_hex": "<64-char lowercase hex>" }
  ]
}
```

can be interpreted interoperably across conforming implementations.

The scheme defines:

- how each leaf is canonicalized and hashed
- how internal nodes are hashed
- how duplicates are treated
- how odd-width levels are handled
- how a proof for one leaf is serialized and verified

---

## Why this specification exists

Without a scheme specification, different implementations could disagree about:

- what exactly gets hashed for a leaf
- whether each per-leaf declared profile (`leaves[].profile`) participates in leaf hashing
- how internal nodes are constructed
- what happens with duplicates
- what happens on odd-width tree levels
- how inclusion proof material is interpreted

That ambiguity would make the declared root non-interoperable.

`collection.merkle-sha3-256/1` exists to close that ambiguity for `collection.merkle-sha3-256/1` while preserving zero-data compatibility with hidden leaves.

---

## Scope boundaries

`collection.merkle-sha3-256/1` applies only to the declared commitment level of a `subject.collection/1` subject under the active rules.

It does:

- define exact leaf-hash and internal-node hash construction
- define exact ordering, duplicate handling, and odd-width promotion
- define exact inclusion-proof object semantics

It does not:

- define the collection subject object itself
- prove that hidden leaves are truthful, complete, or distinct
- force leaves to be atomic rather than higher-order compositions
- define pricing or quantity policy by itself
- define `Issued` or `Independent`

If a hidden leaf is itself a higher-order composition, that remains outside what this scheme can inspect or validate.

---

## Core guarantees

Under `/1`, the scheme preserves:

- exact interoperability of declared roots across implementations
- profile-bound leaf semantics
- position sensitivity through tree placement
- zero-data compatibility with hidden leaves
- deterministic verification under one fixed odd-width rule
- interpretation boundaries between commitment mechanics and external semantic acceptance

The scheme verifies only:

- that a supplied leaf subject value, processed under its per-leaf declared profile (`leaves[].profile`), hashes into one exact position in one exact Merkle tree
- that the resulting root matches the `root` bound by the collection subject

It does not verify:

- whether the leaf should be semantically accepted by a particular external workflow
- whether the full hidden set is complete
- whether `declared_cardinality` is materially truthful
- whether a downstream verifier should accept collection-level or element-level evidence for some external policy purpose

---

## Relationship to other CERTCRYPT specifications

Within the active corpus:

- [subject.collection/1](../../../../profiles/subject.collection/1/index.md) defines the subject object whose `commitment_scheme` may select this scheme
- [CCCP/1](../../../CCCP/1/index.md) defines canonicalization rules consumed by leaf hashing
- [capacity.commitment/1](../../../../ecosystem/settlement/capacity.commitment/1/index.md) and the active settlement profile rely on subject-level commitment semantics defined here when `subject.collection/1` subjects appear in a leaf
- [verifier-toolkit/1](../../../../ecosystem/verification/verifier-toolkit/1/index.md) implements the verification procedure defined here

This scheme does not redefine any of those specifications.

---

## Reading guide

Recommended reading order for implementers and auditors:

1. [Specification](./specification.md)
2. [subject.collection/1](../../../../profiles/subject.collection/1/specification.md)
3. [CCCP/1](../../../CCCP/1/specification.md)
4. [capacity.commitment/1](../../../../ecosystem/settlement/capacity.commitment/1/specification.md)
5. [verifier-toolkit/1](../../../../ecosystem/verification/verifier-toolkit/1/specification.md)

---

## Versioning

- **Specification identifier:** `collection.merkle-sha3-256`
- **Specification version:** `/1`

Version `/1` defines the first canonical Merkle commitment scheme for `subject.collection/1` subjects under the active corpus.

Changes that alter leaf hashing, internal-node hashing, tree-shape rules, the inclusion-proof object, or the verification procedure require a new major version.

Later versions do not retroactively reinterpret already valid commitments governed by `/1`.

---

## One-line summary

**`collection.merkle-sha3-256/1` defines the canonical Merkle-SHA3-256 commitment scheme used by `subject.collection/1` subjects, fixing leaf hashing, internal-node hashing, odd-width handling, and inclusion-proof semantics for byte-for-byte interoperable roots.**

---

## Normative reference

This overview is informational only.

All definitive rules and constraints are defined in:

- [collection.merkle-sha3-256/1/specification](./specification.md)

In case of discrepancy, the specification prevails.
