# CERTCRYPT Verification Package Specification (verification-package/1) — overview

**Identifier:** `verification-package/1`

**Label:** CERTCRYPT Verification Package Specification (verification-package/1)

**Page:** Informative overview

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

**Depends on:**

- [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../../../protocols/CCSP/1/index.md)
- [independence.proof/1 — CERTCRYPT Independence Proof Model](../../../../models/independence.proof/1/index.md)
- the per-commitment inclusion material and zero-data capacity evidence sufficient to validate the claimed `subtree_root` through the hybrid emission binding
- public rules capable of defining `Issued`, `Independent`, and complete verification semantics

> This document is **informative**.
> All normative rules are defined exclusively in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `verification-package/1`?

`verification-package/1` defines the verifier-facing package by which CERTCRYPT certificates are evaluated offline.

It is a package specification, not an issuance model, not a submission protocol, and not a settlement workflow.

Under the active `/1` architecture, `Independent` is evaluated against aggregated settlement only.

It does not make a certificate true, lawful, or institutionally endorsed.

Instead, it defines the package structure by which a verifier can:

- validate an `Issued` certificate offline
- validate an `Independent` result offline
- perform deeper verification against original material when the selected verification path requires it

It also exists to reduce operational complexity in real-world verification scenarios by minimizing artifact discovery, reconstruction, and external dependency resolution.

---

## Why this specification exists

CERTCRYPT separates:

- issuer-local certificate issuance
- submission-set and fixation
- independence proof semantics
- verifier-side package transport
- complete verification against original material

`verification-package/1` exists so that practical verifier workflows do not collapse into:

- live CERTCRYPT API dependency
- managed resolver dependency
- issuer-controlled online dependency
- package-level semantic authority

The package preserves the architectural thesis that verification remains offline, reproducible, and non-authoritative.

---

## Scope boundaries

Within the current architecture:

- `base_certificate` remains the issuer artifact for `Issued`
- `independence_proof` remains the canonical artifact for `Independent`
- the `verification_package` assembles those artifacts, plus any required supporting proof material, for offline verification
- when `Independent` is claimed, the package supports the aggregated-settlement path defined by the aggregated settlement profile the applicable public rules select for the declared `rules_version`

For `Independent`, the package does not redefine Proof of Independence.

It carries the artifacts by which Proof of Independence can be evaluated by a verifier without live infrastructure.

It does not carry a full batch replica, alternative settlement-profile branches, or unrelated leaf material.

Original material may still be required for deeper or complete verification, but that remains a separate verification plane from the package's own structural sufficiency.

The package is therefore a standardized convenience mechanism, not a required gateway for verification.

---

## Core guarantees

`verification-package/1` governs:

- package semantics
- package composition
- `Issued` and `Independent` verification targets
- offline sufficiency requirements
- anti-splicing and coherence requirements
- failure conditions
- managed-copy and interoperability boundaries

It does **not** govern:

- certificate issuance semantics
- submission-set or fixation execution
- settlement orchestration
- capacity issuance lifecycle
- the semantic model of `independence_proof`
- semantic truth of issuer assertions

---

## Relationship to other CERTCRYPT specifications

`verification-package/1` depends conceptually on:

- [CCSP/1](../../../../protocols/CCSP/1/index.md) for certificate serialization
- [independence.proof/1](../../../../models/independence.proof/1/index.md) for the canonical independence artifact and its semantics
- [verifier-toolkit/1](../../verifier-toolkit/1/index.md) for minimum fail-closed verifier behavior
- public rules that define the applicable verification targets

It remains subordinate to the semantics of the artifacts it carries.

If any package convenience conflicts with `independence_proof`, the semantics of `independence.proof/1` prevail.

---

## Reading guide

Recommended reading order for implementers and auditors:

1. [Specification](./specification.md)
2. [independence.proof/1](../../../../models/independence.proof/1/index.md)
3. the leaf and canonicalization rules used by the deployment
4. any applicable settlement or ecosystem verification specifications

For the active architecture, readers should treat aggregated settlement as the only valid `Independent` path under `/1`.

---

## Versioning

- **Specification identifier:** `verification-package`
- **Specification version:** `/1`

Version `/1` is defined for the current CERTCRYPT leaf-based architecture.

Changes that alter package meaning, required artifact composition, offline sufficiency, anti-splicing semantics, or the relationship to `independence_proof` require a new major version.

Later versions do not retroactively reinterpret already valid packages governed by `/1`.

---

## One-line summary

`verification-package/1` is a standardized offline verification package that transports the minimal artifacts needed to evaluate `Issued` or aggregated-settlement `Independent` under CERTCRYPT public rules.

---

## Normative reference

This overview is informational in nature.

All definitive rules and constraints are defined in:

- [verification-package/1/specification](./specification.md)

In case of discrepancy, the specification prevails.
