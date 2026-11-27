# security-model/1 · CERTCRYPT Security Model

**Identifier:** `security-model/1`

**Label:** Security Model v1

**Page:** Informative version index

**Specification type:** Foundation Specification

**Layer:** Layer 0 — Foundation

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `security-model/1` are defined by the normative components linked below.
> In case of discrepancy, the normative component documents prevail.

---

## What is `security-model/1`?

`security-model/1` defines the foundational security boundary of the current CERTCRYPT architecture.

It does **not** define:

- protocol message formats
- canonicalization algorithms
- submission-set transport
- settlement adapter mechanics
- capacity issuance workflows
- managed-service operating policies

It defines:

- the immutable security meaning boundary of `Issued`
- the additional structural boundary of `Independent`
- the trans-layer limits on what CERTCRYPT can and cannot prove
- the non-authority constraints of CERTCRYPT
- the fail-closed semantics required of conforming verification
- the conditions under which later versions must be introduced

`security-model/1` is the foundational meaning boundary of the architecture.

It is not a protocol, not a dashboard truth source, and not a live CERTCRYPT authority.

---

## Role within CERTCRYPT

`security-model/1` is the foundational normative authority of the CERTCRYPT specification suite.

Within the architecture:

- issuers emit base certificates
- public states are constrained to `Issued` and `Independent`
- leaf-first structural integrity must be preserved
- valid capacity and valid settlement constrain `Independent`
- offline-verifiable proof must remain possible
- resolvers and managed services remain optional and non-authoritative

`security-model/1` does not execute any of those paths.

It defines the meaning limits and invariants that every lower-layer specification must preserve while implementing them.

---

## Normative documents

The normative components of `security-model/1` are:

- [Specification](./specification.md)
- [Security invariants](./security-invariants.md)
- [Threat model](./threat-model.md)
- [Invariant-Threat Mapping](./invariant-threat-mapping.md)
- [Security guarantees and non-claims](./security-guarantees-and-non-claims.md)
- [Failure modes and safe failure](./failure-modes-and-safe-failure.md)
- [Evolution and freeze policy](./evolution-and-freeze-policy.md)

Together, these documents define:

- the foundational security boundary
- the invariant set
- the threat boundary
- the permitted guarantee surface
- the safe-failure rules
- the version-freeze rules

---

## See also

- [Overview](./overview.md)

Related lower-layer documents include:

- normative protocol specifications
- normative profile specifications
- normative model specifications such as `independence.proof`
- specifications such as `submission-set/1`, `capacity.commitment/1`, and `verification-package/1`

---

## Versioning

- **Model identifier:** `security-model`
- **Model version:** `/1`

Version `/1` defines the first foundation package aligned with the leaf-based `Issued` / `Independent` architecture.

Any change that alters:

- the meaning boundary of `Issued` or `Independent`
- foundational invariants
- threat boundaries
- non-claims or guarantee surface
- fail-closed semantics
- freeze and non-retroactivity rules

requires a new major version.

Already governed certificates under `/1` are not retroactively reinterpreted by later model versions.

---

## One-line summary

`security-model/1` defines the foundational security limits that determine what CERTCRYPT can and cannot mean for both `Issued` and `Independent`.
