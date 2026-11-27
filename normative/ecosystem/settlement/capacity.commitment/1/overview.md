# CERTCRYPT Capacity Commitment Specification (capacity.commitment/1) — overview

**Identifier:** `capacity.commitment/1`

**Label:** CERTCRYPT Capacity Commitment Specification (capacity.commitment/1)

**Page:** Informative overview

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

**Depends on:**

- public rules capable of defining authorization scope and capacity semantics
- CERTCRYPT system-domain verification material sufficient to validate attribution
- submission-set rules capable of determining applicability and sufficiency
- settlement rules capable of determining actual consumption

> This document is **informative**.
> All normative rules are defined exclusively in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `capacity.commitment/1`?

`capacity.commitment/1` defines the canonical model for the artifact by which CERTCRYPT capacity is authorized for later fixation use.

It is a specification of authorization semantics, not a balance API, not a settlement receipt, and not a proof of independence.

It does not make a leaf `Independent`.

Instead, it defines the artifact by which a conforming implementation can establish that:

- capacity was validly authorized under the relevant system and rules domain
- that authorization belonged to the correct issuer or operational scope
- the authorization was applicable to the submitted leaf
- the authorization could be used only within the scope and constraints defined by public rules

---

## Why this specification exists

CERTCRYPT separates:

- issuer-local issuance
- leaf construction and closure
- economic authorization
- fixation execution
- settlement
- proof of independence

`capacity.commitment/1` exists to keep one boundary extremely clear:

- authorization is not consumption
- pre-authorization is not independence
- local availability is not final settlement

Without that boundary, an implementation could incorrectly treat:

- local capacity state
- a pre-authorized commitment
- or a reusable authorization reference

as if they were already proof that valid CERTCRYPT capacity had been consumed.

The specification prevents that collapse.

---

## Scope boundaries

Within the current architecture, `capacity.commitment/1` sits before positive independence completion.

Its role is to define:

- how capacity becomes applicable
- how that applicability is bound to system, rules, issuer, and scope
- how `submission-set` checks applicability and sufficiency
- why only settlement can fix actual consumption

Under `/1`, the commitment authorizes the path.

It does not complete the path.

Actual consumption must later be evidenced through settlement and reflected in `independence_proof`.

---

## Core guarantees

`capacity.commitment/1` governs:

- the meaning of `capacity_commitment`
- authorization scope and non-transferability
- quantity and applicability semantics
- rules-domain and system-domain binding
- validation requirements for commitments
- the separation between authorization material and consumption evidence
- failure semantics and conformance

It does **not** govern:

- certificate issuance
- submission-set transport
- settlement orchestration details
- the canonical semantics of `independence_proof`
- complete verification against original material

---

## Relationship to other CERTCRYPT specifications

`capacity.commitment/1` depends conceptually on:

- submission-set rules for checking whether a commitment is applicable and sufficient
- settlement rules for determining whether authorized capacity was actually consumed
- `independence.proof/1` rules for proving that such consumption occurred in the path that led to `Independent`

It remains authoritative for the authorization artifact itself.

If any later workflow, SDK, or convenience layer treats pre-authorization as if it were already evidence of consumption, that later layer is in conflict with [specification.md](./specification.md).

---

## Reading guide

Recommended reading order for implementers and auditors:

1. [Specification](./specification.md)
2. [submission-set/1](../../../../protocols/settlement/submission-set/1/specification.md)
3. [independence.proof/1](../../../../models/independence.proof/1/specification.md)
4. the settlement profile used by the deployment

---

## Versioning

- **Specification identifier:** `capacity.commitment`
- **Specification version:** `/1`

Version `/1` is defined for the current CERTCRYPT leaf-based independence architecture.

Changes that alter authorization semantics, scope binding, applicability rules, replay boundaries, or the separation between authorization and consumption require a new major version.

Later versions do not retroactively reinterpret already valid commitments governed by `/1`.

---

## One-line summary

`capacity.commitment/1` defines the canonical authorization artifact that makes CERTCRYPT capacity applicable to fixation without itself proving that capacity was consumed or that a leaf reached `Independent`.

---

## Normative reference

This overview is informational in nature.

All definitive rules and constraints are defined in:

- [capacity.commitment/1/specification](./specification.md)

In case of discrepancy, the specification prevails.
