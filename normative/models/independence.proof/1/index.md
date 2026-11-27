# independence.proof/1 · CERTCRYPT Independence Proof Model

**Identifier:** `independence.proof/1`

**Label:** CERTCRYPT Independence Proof Model (independence.proof/1)

**Page:** Informative version index

**Specification type:** Model Specification

**Layer:** Layer 2 — Models

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `independence.proof/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `independence.proof/1`?

`independence.proof/1` defines the canonical artifact model by which a verifier can establish that a specific leaf reached `Independent` under CERTCRYPT public rules.

It does **not** define:

- submission-set transport
- capacity issuance workflows
- settlement execution choreography
- optional managed retrieval interfaces
- leaf construction procedures

It defines:

- what an `independence_proof` is
- the mandatory bindings of a valid proof
- the logical fields a proof must contain or imply
- the validation sequence a conforming verifier must follow
- the security properties that every conforming implementation must preserve

Under `/1`, `independence_proof` is the canonical independence artifact.

Proof of Independence is the structural result under public rules.

`independence_proof` is the artifact that represents that result.

It is not a dashboard result, not an API truth source, and not a semantic endorsement by CERTCRYPT.

---

## Role within CERTCRYPT

`independence.proof/1` is the artifact model for the accepted independence result.

Within the architecture:

- issuance remains issuer-local
- leaf participation is fixed from issuance
- leaf validity and submission are governed separately
- capacity validity and settlement are governed separately
- `independence_proof` expresses the canonical result once a leaf validly reaches `Independent`

`independence.proof/1` does not execute that path.

It defines the artifact that proves the path completed successfully under public rules.

---

## Normative documents

The normative component of `independence.proof/1` is:

- [Specification](./specification.md)

The specification defines:

- independence conditions
- required bindings
- logical proof fields
- validation procedure
- aggregated settlement semantics
- security properties
- conformance boundaries

---

## Related documents

- [Overview](./overview.md)
- [submission-set/1](../../../protocols/settlement/submission-set/1/index.md)
- [capacity.commitment/1](../../../ecosystem/settlement/capacity.commitment/1/index.md)
- [settlement-material/1](../../../ecosystem/settlement/settlement-material/1/index.md)
- [verification-package/1](../../../ecosystem/verification/verification-package/1/index.md)

---

## Versioning

- **Model identifier:** `independence.proof`
- **Model version:** `/1`

Version `/1` defines the first canonical `independence.proof` model for the leaf-based `Independent` architecture.

Any change that alters:

- canonical proof semantics
- mandatory proof bindings
- proof validation order
- system attribution rules
- finality requirements
- parser strictness or semantic coherence across serializations

requires a new major version.

Already valid proofs under `/1` are not retroactively reinterpreted by later model versions.

---

## One-line summary

`independence.proof/1` defines the canonical offline-verifiable artifact that represents that a specific leaf reached `Independent` under CERTCRYPT public rules.
