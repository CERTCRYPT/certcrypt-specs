# CERTCRYPT Independence Proof Model (independence.proof/1) — overview

**Identifier:** `independence.proof/1`

**Label:** CERTCRYPT Independence Proof Model (independence.proof/1)

**Page:** Informative overview

**Specification type:** Model Specification

**Layer:** Layer 2 — Models

**Status:** Frozen

**Depends on:**

- public rules capable of defining leaf validity and independence conditions
- deterministic leaf commitment derivation
- settlement reference material sufficient to validate the claimed settlement
- CERTCRYPT system-domain verification material sufficient to validate attribution

> This document is **informative**.
> All normative rules are defined exclusively in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `independence.proof/1`?

`independence.proof/1` defines the canonical model for the artifact that expresses that a leaf reached `Independent` under CERTCRYPT public rules.

Within that architecture, Proof of Independence is the structural result under public rules, while `independence_proof` is the canonical artifact representing that result.

It is a model specification, not a transport protocol and not a submission workflow.

Under `/1`, the only valid settlement interpretation for that artifact is aggregated settlement.

It does not make a certificate true, lawful, or institutionally endorsed.

Instead, it defines the artifact by which a verifier can establish that:

- the exact leaf being evaluated is the one claimed by the proof
- the proof belongs to the CERTCRYPT System Domain
- valid aggregated settlement occurred
- valid CERTCRYPT capacity was consumed
- the independence result is deterministic and non-replayed

---

## Why this specification exists

CERTCRYPT separates:

- issuer-local certificate issuance
- leaf construction and closure
- capacity commitment
- settlement execution
- proof of independence
- optional managed retrieval or delivery layers

`independence.proof/1` exists to ensure that the independence result is represented by a canonical offline-verifiable artifact rather than by:

- a live API response
- a dashboard status
- a resolver lookup
- a CERTCRYPT signature treated as authority

The model preserves the architectural thesis that CERTCRYPT may participate in producing `Independent`, but must not become a required live authority for verifying it.

---

## Scope boundaries

Within the leaf-based architecture, `independence.proof/1` sits after successful structural and economic completion of the path that leads to `Independent`.

Its role is to bind together:

- the exact leaf commitment
- the relevant aggregated settlement reference
- the relevant inclusion proof
- the relevant batch binding
- the CERTCRYPT system-domain attribution

Under `/1`, the `independence_proof` is the canonical independence artifact inside the broader verification context.

It does not replace the need for a complete verification package in practice, but it defines the core artifact whose semantics must prevail if any packaging convenience conflicts with the proof meaning.

---

## Core guarantees

`independence.proof/1` governs:

- the logical meaning of an `independence_proof`
- the required conditions for a leaf to be considered `Independent`
- the logical fields that a valid proof must contain or imply, including the mandatory system-domain signature over its signed view and the optional, signed attestation of the recognized node the submission entered through
- the validation sequence for conforming verifiers
- the aggregated settlement semantics required by the active architecture
- proof failure semantics
- security properties and conformance boundaries

It does **not** govern:

- submission-set transport
- capacity issuance lifecycle
- settlement orchestration details
- optional managed retrieval interfaces
- leaf construction procedures
- legal validity, factual truth, or institutional endorsement

---

## Relationship to other CERTCRYPT specifications

`independence.proof/1` depends conceptually on:

- deterministic leaf commitment rules defined elsewhere
- settlement rules capable of validating the referenced settlement and its finality
- capacity rules capable of validating consumed CERTCRYPT capacity
- verification-package rules for practical transport of the complete verifier-facing material

It remains authoritative for the semantics of the proof artifact itself.

If any later packaging, delivery, or convenience layer conflicts with this model, the semantics defined in [specification.md](./specification.md) prevail.

---

## Reading guide

Recommended reading order for implementers and auditors:

1. [Specification](./specification.md)
2. the leaf commitment and canonicalization rules used by the relevant leaf model
3. the settlement and capacity specifications used by the deployment
4. the verification-package specification used to transport the proof in practice

---

## Versioning

- **Model identifier:** `independence.proof`
- **Model version:** `/1`

Version `/1` is defined for the current leaf-based `Independent` architecture.

Changes that alter proof semantics, mandatory bindings, validation order, system attribution rules, parser strictness, or finality requirements require a new major version.

Later versions do not retroactively reinterpret already valid proofs issued under `/1`.

---

## One-line summary

`independence.proof/1` is the canonical offline-verifiable artifact model that represents that a specific leaf reached `Independent` through valid aggregated CERTCRYPT settlement and valid CERTCRYPT capacity.

---

## Normative reference

This overview is informational in nature.

All definitive rules and constraints are defined in:

- [independence.proof/1/specification](./specification.md)

In case of discrepancy, the specification prevails.
