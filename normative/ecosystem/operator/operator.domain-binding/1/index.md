# operator.domain-binding/1 · CERTCRYPT Operator Domain Binding Specification

**Identifier:** `operator.domain-binding/1`

**Label:** CERTCRYPT Operator Domain Binding Specification (operator.domain-binding/1)

**Page:** Informative version index

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `operator.domain-binding/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `operator.domain-binding/1`?

`operator.domain-binding/1` defines an optional, mutual declaration between a node's operator key and an HTTPS origin: the key signs a statement naming the host name, and the origin publishes it under `/.well-known/certcrypt-node.json`. Anyone holding the operator identifier can check that both declare each other.

It does **not** define:

- identity proofing, endorsement or certification of operators
- any input to the verification of an independence proof
- a registry of operators or host names
- any visual distinction between operators

---

## Documents

- [Overview](./overview.md)
- [Specification](./specification.md)

---

## One-line summary

`operator.domain-binding/1` lets a node operator be associated with an HTTPS origin through a statement its key signs and the origin publishes, outside independence proofs and without any endorsement.
