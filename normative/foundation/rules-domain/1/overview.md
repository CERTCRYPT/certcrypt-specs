# CERTCRYPT Rules Domain (`rules-domain/1`) — overview

**Identifier:** `rules-domain/1`

**Label:** CERTCRYPT Rules Domain Specification (rules-domain/1)

**Page:** Informative overview

**Specification type:** Foundation Specification

**Layer:** Layer 0 — Foundation

**Status:** Frozen

> This document is **informative**.
> All normative rules are defined exclusively in [specification.md](./specification.md).

---

## What is `rules-domain/1`?

`rules-domain/1` defines how one exact public rules domain is identified and selected for CERTCRYPT evaluation.

It makes rules-domain exactness a foundation concern rather than an implementation convenience.

Within the active architecture, it fixes:

- how the applicable `rules_version` is identified
- when selection is exact enough to proceed
- when ambiguity or fallback must fail closed
- how related artifacts remain rule-consistent during one evaluation

---

## Why this specification exists

Many CERTCRYPT artifacts depend explicitly on:

- one exact `rules_version`
- one exact settlement profile
- one exact finality profile
- one exact proof and verifier interpretation boundary

Without a dedicated foundation document, those requirements become easier to implement inconsistently across the stack.

`rules-domain/1` exists to prevent that drift.

---

## Scope boundaries

`rules-domain/1` applies only to exact public-rule selection and cross-artifact rule consistency.

It does:

- define how one exact rules domain is selected
- bind evaluations to one exact public-rule context
- require fail-closed behavior when selection is ambiguous

It does not:

- replace `system-domain/1`
- replace `security-model/1`
- prove truth
- produce `Independent`

---

## Core guarantees

Under `/1`, the rules-domain foundation preserves:

- deterministic rule selection
- no heuristic fallback or successor guessing
- cross-artifact rule coherence
- institutional independence from live CERTCRYPT services
- interpretation boundaries between rule selection and proof meaning

---

## Relationship to other CERTCRYPT specifications

`rules-domain/1` does not replace:

- `system-domain/1`, which answers which exact system is being evaluated
- `system-foundation/1`, which fixes the bootstrap artifact carrying the root material
- `security-model/1`, which defines the foundational guarantees and fail-closed boundaries

Instead:

- `system-domain/1` answers: "Which exact system is this?"
- `rules-domain/1` answers: "Under which exact public rules must this be evaluated?"
- `security-model/1` answers: "What must remain true and what must fail closed under those rules?"

---

## Reading guide

Recommended reading order for implementers and auditors:

1. [Specification](./specification.md)
2. [system-domain/1](../../system-domain/1/specification.md)
3. [system-foundation/1](../../system-foundation/1/specification.md)
4. [security-model/1](../../security-model/1/specification.md)
5. the active registry entry under [system-domain/1/registry/certcrypt/rules/](../../system-domain/1/registry/certcrypt/rules/index.md)

---

## Versioning

- **Specification identifier:** `rules-domain`
- **Specification version:** `/1`

Version `/1` is defined for the current CERTCRYPT leaf-based independence architecture.

Changes that alter rules-domain identification, selection requirements, equivalence rules, cross-artifact coherence, or fail-closed boundaries require a new major version.

Later versions do not retroactively reinterpret already valid evaluations governed by `/1`.

---

## One-line summary

`rules-domain/1` defines how one exact public rules domain is identified, selected, and bound across artifacts so that any CERTCRYPT evaluation proceeds under one and only one applicable ruleset.

---

## Normative reference

This overview is informational in nature.

All definitive rules and constraints are defined in:

- [rules-domain/1/specification](./specification.md)

In case of discrepancy, the specification prevails.
