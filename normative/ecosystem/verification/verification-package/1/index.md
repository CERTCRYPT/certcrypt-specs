# verification-package/1 · CERTCRYPT Verification Package Specification

**Identifier:** `verification-package/1`

**Label:** CERTCRYPT Verification Package Specification (verification-package/1)

**Page:** Informative version index

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `verification-package/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `verification-package/1`?

`verification-package/1` defines a standardized offline verification package for CERTCRYPT certificate evaluation.

Under `/1`, any `Independent` path carried by the package is aggregated-settlement only.

It does **not** define:

- certificate issuance semantics
- submission-set transport
- settlement execution
- capacity issuance workflows
- the semantic model of `independence_proof`

It defines:

- what a `verification_package` is
- what artifacts it must contain for `Issued` and `Independent`
- how offline sufficiency is interpreted
- how anti-splicing and package coherence must be enforced
- how package verification relates to complete verification against original material

Under `/1`, the `verification_package` is a verification package only.

It is not the ontological source of independence and it is not a semantic authority.

---

## Role within CERTCRYPT

`verification-package/1` sits at the verifier-facing edge of the architecture.

Within the current system:

- issuers emit base certificates
- CERTCRYPT may participate in fixation
- `independence_proof` remains the canonical independence artifact
- `verification_package` carries the artifacts needed for practical offline verification
- for `Independent`, those artifacts are aligned to the aggregated settlement profile the applicable public rules select for the declared `rules_version`

For `Independent`, `/1` packages an `independence_proof` and its required supporting material in verifier-usable form.

It does not create that proof.

It transports the artifacts by which that proof can be evaluated under public rules.

---

## Normative documents

The normative component of `verification-package/1` is:

- [Specification](./specification.md)

The specification defines:

- package semantics
- verification targets
- required composition
- original-material and complete-verification boundaries
- offline sufficiency
- package integrity and anti-splicing rules
- failure semantics and interoperability boundaries

---

## Related documents

- [Overview](./overview.md)
- [independence.proof/1](../../../../models/independence.proof/1/index.md)
- [settlement-material/1](../../../settlement/settlement-material/1/index.md)
- [verifier-toolkit/1](../../verifier-toolkit/1/index.md)

---

## Versioning

- **Specification identifier:** `verification-package`
- **Specification version:** `/1`

Version `/1` defines the first canonical verification-package model for the current CERTCRYPT architecture.

Any change that alters:

- package meaning
- package sufficiency for offline verification
- required artifact composition
- anti-splicing semantics
- relationship to `independence_proof`

requires a new major version.

Already valid packages under `/1` are not retroactively reinterpreted by later versions.

---

## One-line summary

`verification-package/1` defines a standardized offline package by which a verifier can evaluate `Issued` or aggregated-settlement `Independent` under CERTCRYPT public rules.
