# CERTCRYPT Settlement Material Specification (`settlement-material/1`) — overview

**Identifier:** `settlement-material/1`

**Label:** CERTCRYPT Settlement Material Specification (settlement-material/1)

**Page:** Informative overview

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

> This document is **informative**.
> All normative rules are defined exclusively in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `settlement-material/1`?

`settlement-material/1` defines the public offline settlement-material contract required to validate a settlement-backed CERTCRYPT independence path.

It defines:

- what settlement proof material is
- what one exact `settlement_profile_id` must determine
- how settlement finality, capacity consumption, and leaf assignment are exposed offline
- how authorization remains distinct from settlement-fixed consumption

It does not define certificate issuance or backend-specific settlement choreography.

---

## Why this specification exists

CERTCRYPT needs a public offline contract that bridges:

- settlement execution
- proof construction
- verifier-side independent evaluation

Without that contract, implementations would drift toward:

- live chain queries
- managed-service memory
- incomplete or heuristic settlement interpretation

`settlement-material/1` exists to prevent that drift and keep settlement-backed proof paths reproducible offline.

---

## Scope boundaries

`settlement-material/1` applies only to the settlement-path artifact set required for settlement-backed `Independent` verification.

It does:

- define the required logical components of settlement-path material
- require exact profile binding
- require deterministic authorization-to-consumption bridging

It does not:

- replace the selected settlement profile
- redefine certificate issuance
- turn settlement execution into proof by itself
- collapse execution into semantic truth

---

## Core guarantees

Under `/1`, the settlement-material contract preserves:

- proof without data custody
- deterministic verification
- exact profile binding
- institutional independence from live infrastructure
- interpretation boundaries between settlement evidence and proof meaning

---

## Relationship to other CERTCRYPT specifications

Within the current architecture:

- `submission-set/1` selects one exact settlement profile
- `capacity.commitment/1` authorizes applicability before settlement
- one concrete settlement profile such as `settlement.aggregated.xrpl/1` instantiates the contract
- `independence.proof/1` remains the canonical proof-path model
- `verification-package/1` and `verifier-toolkit/1` carry and validate the offline artifact set

`settlement-material/1` therefore defines the public contract between settlement execution and offline proof verification.

---

## Reading guide

Recommended reading order for implementers and auditors:

1. [Specification](./specification.md)
2. [submission-set/1](../../../../protocols/settlement/submission-set/1/specification.md)
3. [settlement.aggregated.xrpl/1](../../settlement.aggregated.xrpl/1/specification.md) as the active settlement profile that instantiates this contract
4. [capacity.commitment/1](../../capacity.commitment/1/specification.md)
5. [independence.proof/1](../../../../models/independence.proof/1/specification.md)
6. [verification-package/1](../../../verification/verification-package/1/specification.md)

---

## Versioning

- **Specification identifier:** `settlement-material`
- **Specification version:** `/1`

Version `/1` defines the first canonical settlement-material contract for settlement-backed `Independent` verification under the active corpus.

Changes that alter the required logical components, the exact profile binding, the authorization-to-consumption bridge, or the boundary between settlement execution and proof meaning require a new major version.

Later versions do not retroactively reinterpret already valid settlement material governed by `/1`.

---

## One-line summary

**`settlement-material/1` defines the public offline settlement-material contract that bridges settlement execution, proof construction, and verifier-side independent evaluation, without itself replacing the selected settlement profile or producing `Independent`.**

---

## Normative reference

This overview is informational in nature.

All definitive rules and constraints are defined in:

- [settlement-material/1/specification](./specification.md)

In case of discrepancy, the specification prevails.
