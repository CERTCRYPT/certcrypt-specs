# holder-keyset.merkle-sha3-256/1 · CERTCRYPT Holder Operation-Key Set Commitment Scheme

**Identifier:** `holder-keyset.merkle-sha3-256/1`

**Label:** CERTCRYPT Holder Operation-Key Set Commitment Scheme v1

**Page:** Informative version index

**Specification type:** Protocol

**Layer:** Layer 1 — Protocols

**Status:** Frozen

**Depends on:**
- [system-domain/1](../../../../foundation/system-domain/1/index.md)
- [rules-domain/1](../../../../foundation/rules-domain/1/index.md)
- [security-model/1](../../../../foundation/security-model/1/index.md)
- [CCCP/1](../../../CCCP/1/index.md)

> This document is **informative**.
> The normative requirements for `holder-keyset.merkle-sha3-256/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `holder-keyset.merkle-sha3-256/1`?

`holder-keyset.merkle-sha3-256/1` defines one exact interoperable commitment scheme over a holder's set of per-operation signing keys.

It defines:

- exact leaf-hash input semantics (one operation public key per leaf)
- exact internal-node hash semantics
- exact tree-shape and ordering rules
- the exact disclosure object model and membership-verification boundary
- exact failure conditions for unsupported or ambiguous disclosure material

It does **not** define:

- holder authorization (a Level-1 system-domain signature over the root)
- signature verification of any commitment
- pseudonym derivation (CCCP/1 §7.4)
- capacity consumption
- `Issued` or `Independent`

---

## Architectural role

`holder-keyset.merkle-sha3-256/1` is the key-material primitive of the zero-data capacity profile.

Within the current architecture:

- [capacity.holder-authorization/1](../../../../ecosystem/settlement/capacity.holder-authorization/1/index.md) commits to a `holder_key_set_root` instead of a stable holder public key
- `holder-keyset.merkle-sha3-256/1` defines how that root is computed and how one disclosed operation key proves membership
- [capacity.commitment/1](../../../../ecosystem/settlement/capacity.commitment/1/index.md) (projected form) is signed by one operation leaf key and carries the disclosure
- higher-layer authorization, signature, and pseudonym semantics remain defined elsewhere

It uses the same tree shape (ordering, odd-node promotion, proof walk) as [collection.merkle-sha3-256/1](../../collection.merkle-sha3-256/1/index.md), with the single-byte leaf and node prefixes of the aggregated settlement Merkle tree (`settlement.binding/1` §6); its roots are kept apart from settlement roots by context and leaf input, not by those prefixes.

---

## Normative documents

The normative component of `holder-keyset.merkle-sha3-256/1` is:

- [Specification](./specification.md)

---

## Related documents

- [Overview](./overview.md)
- [CCCP/1](../../../CCCP/1/index.md)
- [collection.merkle-sha3-256/1](../../collection.merkle-sha3-256/1/index.md)
- [capacity.holder-authorization/1](../../../../ecosystem/settlement/capacity.holder-authorization/1/index.md)
- [capacity.commitment/1](../../../../ecosystem/settlement/capacity.commitment/1/index.md)

---

## Versioning

- **Protocol family identifier:** `holder-keyset.merkle-sha3-256`
- **Scheme version:** `/1`

Any change that alters leaf-hash input, node-hash input, tree shape, disclosure interpretation, or failure conditions requires a new major version. Already valid roots or disclosures under `/1` are not retroactively reinterpreted by later versions.

---

## One-line summary

**`holder-keyset.merkle-sha3-256/1` defines the exact Merkle-SHA3-256 root and membership-proof semantics over a holder's per-operation signing keys, so a Level-2 authorization can commit to a `holder_key_set_root` without exposing a stable holder key.**
