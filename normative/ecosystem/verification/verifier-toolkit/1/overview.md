# CERTCRYPT Verifier Toolkit Specification (verifier-toolkit/1) — overview

**Identifier:** `verifier-toolkit/1`

**Label:** CERTCRYPT Verifier Toolkit Specification (verifier-toolkit/1)

**Page:** Informative overview

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

**Depends on:**

- [security-model/1 — CERTCRYPT Security Model Specification](../../../../foundation/security-model/1/index.md)
- [system-domain/1 — CERTCRYPT System Domain Specification](../../../../foundation/system-domain/1/index.md)
- [rules-domain/1 — CERTCRYPT Rules Domain Specification](../../../../foundation/rules-domain/1/index.md)
- [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../../../protocols/CCSP/1/index.md)
- [independence.proof/1 — CERTCRYPT Independence Proof Model](../../../../models/independence.proof/1/index.md)
- [verification-package/1 — CERTCRYPT Verification Package Specification](../../verification-package/1/index.md)

> This document is **informative**.
> All normative rules are defined exclusively in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `verifier-toolkit/1`?

`verifier-toolkit/1` defines the minimum conformance boundary for the reference verifier toolkit for CERTCRYPT.

It exists to make correct offline verification easier than degraded verification.

Under the active `/1` architecture, correct `Independent` verification means deterministic verification against aggregated settlement only.

It does not create new certificate states, new proof semantics, or new authority surfaces.

Instead, it defines the minimum toolkit behavior required to:

- verify `Issued`
- verify `Independent`
- fail closed when required checks cannot be completed
- distinguish standard offline verification from deeper or complete verification against original material

---

## Why this specification exists

CERTCRYPT already defines:

- foundational security invariants
- system and rules attribution
- certificate envelope rules
- canonical `independence_proof` semantics
- optional `verification_package` transport semantics

`verifier-toolkit/1` adds the verifier-toolkit boundary that prevents the ecosystem from degrading into:

- partial verifiers
- plausible-looking package readers
- “compatible enough” widgets
- hosted flows that silently replace the offline baseline

`verifier-toolkit/1` exists to define that minimum behavior without inventing any new ontology.

---

## Scope boundaries

Within the current architecture:

- the issuer emits the base certificate
- CERTCRYPT does not become a live verification authority
- `verification_package` remains optional
- `independence_proof` remains canonical for `Independent`
- the verifier toolkit is the minimum fail-closed implementation boundary for verifier behavior
- no alternative settlement profile may be treated as a compatible `Independent` path under `/1`

The toolkit is therefore not a product badge or trust anchor.

It is the minimum implementation contract required to keep `Independent` from degrading into a soft category.

---

## Core guarantees

`verifier-toolkit/1` governs:

- minimum supported inputs
- minimum supported verification targets
- mandatory verifier principles
- output taxonomy
- required baseline verification checks
- minimum proof-handling behavior
- anti-splicing and anti-downgrade requirements
- deterministic aggregated-settlement verification behavior
- conformance-suite and “done” criteria

It does **not** govern:

- issuance
- fixation
- settlement execution
- governance semantics
- semantic truth of issuer declarations
- live token supply state or online burn inspection for the standard path

---

## Relationship to other CERTCRYPT specifications

`verifier-toolkit/1` is subordinate to:

- [security-model/1](../../../../foundation/security-model/1/index.md)
- [system-domain/1](../../../../foundation/system-domain/1/index.md)
- [rules-domain/1](../../../../foundation/rules-domain/1/index.md)
- [independence.proof/1](../../../../models/independence.proof/1/index.md)
- [verification-package/1](../../verification-package/1/index.md)

If any toolkit convenience conflicts with those public specifications, those public specifications prevail.

---

## Reading guide

Recommended reading order for implementers:

1. [Specification](./specification.md)
2. [security-model/1](../../../../foundation/security-model/1/index.md)
3. [system-domain/1](../../../../foundation/system-domain/1/index.md)
4. [rules-domain/1](../../../../foundation/rules-domain/1/index.md)
5. [independence.proof/1](../../../../models/independence.proof/1/index.md)
6. [verification-package/1](../../verification-package/1/index.md)

---

## Versioning

- **Specification identifier:** `verifier-toolkit`
- **Specification version:** `/1`

Version `/1` defines the first canonical minimum verifier-toolkit profile for the active CERTCRYPT corpus.

Changes that alter minimum supported targets, supported inputs, fail-closed behavior, or the offline-first guarantee require a new major version.

Later versions do not retroactively reinterpret already valid verifier outputs governed by `/1`.

---

## One-line summary

`verifier-toolkit/1` defines the minimum fail-closed, offline-first verifier behavior required to evaluate `Issued` and aggregated-settlement `Independent` under CERTCRYPT public rules.

---

## Normative reference

This overview is informational in nature.

All definitive rules and constraints are defined in:

- [verifier-toolkit/1/specification](./specification.md)

In case of discrepancy, the specification prevails.
