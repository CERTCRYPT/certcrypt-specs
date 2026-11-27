# settlement-material/1 · CERTCRYPT Settlement Material Specification

**Identifier:** `settlement-material/1`

**Label:** CERTCRYPT Settlement Material Specification (settlement-material/1)

**Page:** Informative version index

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `settlement-material/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `settlement-material/1`?

`settlement-material/1` defines the public offline settlement-material contract required to validate a settlement-backed CERTCRYPT independence path.

It does **not** define:

- certificate issuance semantics
- submission-set transport
- backend-specific settlement execution choreography
- hosted retrieval behavior
- truth, legitimacy, or semantic correctness of issuer claims

It defines:

- what settlement proof material is
- what one exact `settlement_profile_id` MUST determine
- how authorization, settlement consumption, and proof remain distinct
- what finality, capacity-consumption, and leaf-assignment evidence the offline verifier MUST receive
- what fail-closed conditions apply when that evidence is incomplete

---

## Role within CERTCRYPT

Within the current CERTCRYPT architecture:

- `capacity_commitment` authorizes possible use
- `submission-set` selects one exact settlement profile
- settlement fixes actual consumption
- `settlement-material/1` defines the settlement-material contract for that settlement profile
- `independence_proof` binds the canonical independence result to that settlement context
- `verification_package` and `verifier-toolkit` carry and validate the resulting offline artifact set

`settlement-material/1` therefore closes the public contract between settlement execution and offline verification.

---

## Normative documents

The normative component of `settlement-material/1` is:

- [Specification](./specification.md)

---

## Related documents

- [capacity.commitment/1](../../capacity.commitment/1/index.md)
- [submission-set/1](../../../../protocols/settlement/submission-set/1/index.md)
- [independence.proof/1](../../../../models/independence.proof/1/index.md)
- [verification-package/1](../../../verification/verification-package/1/index.md)
- [verifier-toolkit/1](../../../verification/verifier-toolkit/1/index.md)
- [rules-domain/1](../../../../foundation/rules-domain/1/index.md)

---

## Versioning

- **Identifier:** `settlement-material/1`

Version `settlement-material/1` defines the active public contract for this document. Any non-backward-compatible semantic or structural change requires a new major version.

## One-line summary

**`settlement-material/1` defines the exact offline settlement-material contract required to validate settlement, finality, leaf assignment, and settlement-bound capacity consumption under one exact settlement profile.**
