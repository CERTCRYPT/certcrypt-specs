# CERTCRYPT Security Model (security-model/1) — overview

**Identifier:** `security-model/1`

**Label:** Security Model v1

**Page:** Informative overview

**Specification type:** Foundation Specification

**Layer:** Layer 0 — Foundation

**Status:** Frozen

**Depends on:** None _(foundational security framework)_

> This document is **informative**.
> All normative rules are defined by the normative components of `security-model/1`.
> In case of discrepancy, the normative component documents prevail.

---

## What is `security-model/1`?

`security-model/1` defines the foundational security boundary of the current CERTCRYPT architecture.

It is the layer that fixes the meaning limits for:

- issuer-local issuance
- cryptographic `Issued` verification
- structural `Independent` verification
- leaf-first security semantics
- zero-data and stateless core properties
- non-authoritative managed and resolver layers

It is a foundation package, not a protocol or a workflow specification.

It does not define transport, canonicalization algorithms, submission-set choreography, or settlement execution details.

---

## Why this specification exists

CERTCRYPT distinguishes two public security-relevant states:

- `Issued`
- `Independent`

That distinction makes the security boundary stricter, not looser.

`Issued` remains a cryptographic result of issuer-local issuance.

`Independent` adds structural conditions that depend on:

- issuance-time participation in the independence flow
- valid leaf inclusion
- valid CERTCRYPT capacity
- valid settlement with sufficient finality under public rules
- offline-verifiable proof material

`security-model/1` exists to ensure that none of those conditions can later be reinterpreted as:

- truth
- institutional endorsement
- legal validity
- payment-based authority
- trust in live CERTCRYPT services

---

## Scope boundaries

Within the leaf-based architecture, `security-model/1` sits above protocols, profiles, models, ecosystem texts, and governance texts.

Its role is to bind together:

- the meaning boundary of `Issued`
- the meaning boundary of `Independent`
- the invariant set that lower layers must preserve
- the threat boundary the architecture claims to mitigate
- the safe-failure rules that prevent degraded verification
- the non-retroactivity and freeze rules for future evolution

It does not replace lower-layer specifications.

It defines the semantics that must prevail if any lower-layer convenience, packaging, delivery, or service document conflicts with the foundation meaning boundary.

---

## Core guarantees

`security-model/1` governs:

- foundational invariants
- threat boundaries
- guarantees and explicit non-claims
- safe-failure semantics
- evolution and freeze rules

It does **not** govern:

- protocol message formats
- canonicalization algorithms
- proof field layouts
- settlement adapter mechanics
- capacity issuance lifecycle
- governance procedures
- implementation deployment details

Those concerns belong to lower layers, but they remain constrained by this foundation model.

---

## Relationship to other CERTCRYPT specifications

`security-model/1` constrains:

- protocol specifications
- profile specifications
- model specifications
- ecosystem documents
- governance documents

It depends conceptually on no lower-layer document, but later documents must remain compatible with it.

If any lower-layer packaging, delivery, service, or policy text conflicts with the meaning fixed here, the normative components of `security-model/1` prevail.

---

## Reading guide

Recommended reading order for reviewers and auditors:

1. [Specification](./specification.md)
2. [Security invariants](./security-invariants.md)
3. [Threat model](./threat-model.md)
4. [Invariant-Threat Mapping](./invariant-threat-mapping.md)
5. [Security guarantees and non-claims](./security-guarantees-and-non-claims.md)
6. [Failure modes and safe failure](./failure-modes-and-safe-failure.md)
7. [Evolution and freeze policy](./evolution-and-freeze-policy.md)

---

## Versioning

- **Model identifier:** `security-model`
- **Model version:** `/1`

Version `/1` is defined for the current leaf-based `Issued` / `Independent` architecture.

Changes that alter foundational invariants, threat boundaries, the meaning of `Issued` or `Independent`, fail-closed behavior, or freeze semantics require a new major version.

Later versions do not retroactively reinterpret already governed certificates under `/1`.

---

## One-line summary

`security-model/1` is the foundational security model that fixes what CERTCRYPT can and cannot mean for both `Issued` and `Independent`.

---

## Normative reference

This overview is informational in nature.

All definitive rules and constraints are defined in:

- [security-model/1/specification](./specification.md)

In case of discrepancy, the specification prevails.
