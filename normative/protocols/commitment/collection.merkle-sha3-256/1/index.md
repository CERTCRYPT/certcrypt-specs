# collection.merkle-sha3-256/1 · CERTCRYPT Merkle Collection Commitment Scheme

**Identifier:** `collection.merkle-sha3-256/1`

**Label:** CERTCRYPT Merkle Collection Commitment Scheme v1

**Page:** Informative version index

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
> The normative requirements for `collection.merkle-sha3-256/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `collection.merkle-sha3-256/1`?

`collection.merkle-sha3-256/1` defines one exact interoperable collection-commitment scheme for `subject.collection/1` when the declared `commitment_scheme` is `collection.merkle-sha3-256/1`.

It defines:

- exact leaf-hash input semantics
- exact internal-node hash semantics
- exact tree-shape and ordering rules
- exact inclusion-proof model and verification boundary
- exact failure conditions for unsupported or ambiguous proof material

It does **not** define:

- subject canonicalization outside the declared collection scheme
- certificate issuance
- pricing
- truth, completeness, or distinctness of hidden leaves
- `Issued` or `Independent`

---

## Architectural role

`collection.merkle-sha3-256/1` is not a standalone subject profile.

Within the current architecture:

- [subject.collection/1](../../../../profiles/subject.collection/1/index.md) binds `commitment_scheme`, `root`, `declared_cardinality`, and per-leaf declared profiles (`leaves[]`)
- `collection.merkle-sha3-256/1` defines how that exact declared scheme computes the root and verifies per-leaf inclusion proof material
- higher-layer quantity, verifier, and independence semantics remain defined elsewhere

The scheme closes interoperability for the declared root.

It does not upgrade the collection subject into semantic truth or authority.

---

## Normative documents

The normative component of `collection.merkle-sha3-256/1` is:

- [Specification](./specification.md)

The specification defines:

- hashing domains
- leaf canonicalization inputs
- internal node construction
- ordering and duplicate handling
- odd-node handling
- proof object model
- verification procedure
- failure modes

---

## Related documents

- [Overview](./overview.md)
- [subject.collection/1](../../../../profiles/subject.collection/1/index.md)
- [capacity.commitment/1](../../../../ecosystem/settlement/capacity.commitment/1/index.md)
- [verifier-toolkit/1](../../../../ecosystem/verification/verifier-toolkit/1/index.md)

---

## Versioning

- **Protocol family identifier:** `collection.merkle-sha3-256`
- **Scheme version:** `/1`

Version `/1` defines the first interoperable Merkle-SHA3-256 collection-commitment scheme for the current CERTCRYPT architecture.

Any change that alters:

- leaf-hash input
- node-hash input
- tree shape
- proof interpretation
- failure conditions

requires a new major version.

Already valid roots or proofs under `/1` are not retroactively reinterpreted by later versions.

---

## One-line summary

**`collection.merkle-sha3-256/1` defines the exact Merkle-SHA3-256 root and inclusion-proof semantics used when a `subject.collection/1` subject declares `commitment_scheme = "collection.merkle-sha3-256/1"`.**
