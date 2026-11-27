# verifier-toolkit/1 · CERTCRYPT Verifier Toolkit Specification

**Identifier:** `verifier-toolkit/1`

**Label:** CERTCRYPT Verifier Toolkit Specification (verifier-toolkit/1)

**Page:** Informative version index

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `verifier-toolkit/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `verifier-toolkit/1`?

`verifier-toolkit/1` defines the minimum conformance boundary for the reference offline verifier toolkit for CERTCRYPT artifacts.

Under `/1`, the toolkit treats aggregated settlement as the only valid `Independent` path.

It does **not** define:

- certificate issuance
- fixation
- settlement execution
- live resolver semantics
- truth validation of issuer assertions

It defines:

- minimum supported verification targets
- mandatory verifier principles and fail-closed behavior
- required inputs and output taxonomy
- mandatory `Independent` verification baseline
- anti-splicing, anti-downgrade, and anti-heuristic behavior
- minimum conformance-suite requirements

Under `/1`, the toolkit is a verifier only.

It is not a semantic authority and it is not a substitute for the public rules and canonical artifacts it evaluates.

---

## Role within CERTCRYPT

`verifier-toolkit/1` sits at the verifier-facing edge of the architecture.

Within the current system:

- issuers emit base certificates
- CERTCRYPT may participate in fixation
- `independence_proof` remains the canonical independence artifact
- `verification_package` remains an optional convenience container
- the verifier toolkit defines the minimum behavior required to evaluate `Issued` and `Independent` offline under public rules
- for `Independent`, no fallback to direct or alternative settlement profiles is permitted under `/1`

For `Independent`, `/1` does not redefine proof semantics.

It defines the minimum verifier behavior required to evaluate those semantics correctly and fail closed when they cannot be completed.

---

## Normative documents

The normative component of `verifier-toolkit/1` is:

- [Specification](./specification.md)

The specification defines:

- purpose and scope
- supported verification routes
- normative toolkit principles
- minimum input sets
- output taxonomy
- mandatory verification baseline
- required handling of `independence_proof`
- anti-splicing, aggregated-settlement, and original-material boundaries
- conformance-suite requirements

---

## Related documents

- [Overview](./overview.md)
- [verification-package/1](../../verification-package/1/index.md)
- [independence.proof/1](../../../../models/independence.proof/1/index.md)
- [security-model/1](../../../../foundation/security-model/1/index.md)
- negative test vectors are part of the public conformance suite (§17)

---

## Versioning

- **Specification identifier:** `verifier-toolkit`
- **Specification version:** `/1`

Version `/1` defines the first canonical minimum verifier-toolkit model for the current CERTCRYPT architecture.

Any change that alters:

- supported verification targets
- mandatory verification checks
- fail-closed requirements
- output taxonomy
- conformance-suite meaning

requires a new major version.

Already valid verifier results under `/1` are not retroactively reinterpreted by later versions.

---

## One-line summary

`verifier-toolkit/1` defines the minimum fail-closed offline verifier behavior required to evaluate `Issued` and aggregated-settlement `Independent` under CERTCRYPT public rules.
