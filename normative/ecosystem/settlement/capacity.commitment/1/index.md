# capacity.commitment/1 · CERTCRYPT Capacity Commitment Specification

**Identifier:** `capacity.commitment/1`

**Label:** CERTCRYPT Capacity Commitment Specification (capacity.commitment/1)

**Page:** Informative version index

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `capacity.commitment/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `capacity.commitment/1`?

`capacity.commitment/1` defines the canonical authorization model by which CERTCRYPT capacity becomes applicable to fixation under public rules.

It does **not** define:

- certificate issuance semantics
- submission-set transport
- settlement execution choreography
- the canonical semantics of `independence_proof`
- complete verification against original material

It defines:

- what a `capacity_commitment` is
- what a valid commitment authorizes
- what bindings and scopes a commitment must preserve
- how conforming implementations validate applicability and sufficiency
- what the commitment does **not** prove

Under `/1`, `capacity_commitment` is an authorization artifact.

It is not proof of `Independent`, not proof of consumption, and not a substitute for settlement.

---

## Role within CERTCRYPT

`capacity.commitment/1` sits between economic authorization and fixation execution.

Within the current architecture:

- issuers emit base certificates
- `submission-set` validates whether capacity is applicable to the requested fixation
- settlement fixes whether valid CERTCRYPT capacity was actually consumed
- `independence_proof` proves the resulting independence state

`capacity.commitment/1` does not consume capacity by itself.

It defines the artifact and semantics by which capacity may become validly applicable before fixation completes.

---

## Normative documents

The normative component of `capacity.commitment/1` is:

- [Specification](./specification.md)

The specification defines:

- authorization semantics
- scope and non-transferability rules
- applicability and sufficiency checks
- rules-domain and system-domain binding
- separation between authorization and consumption
- security and conformance properties

---

## Related documents

- [Overview](./overview.md)
- [submission-set/1](../../../../protocols/settlement/submission-set/1/index.md)
- [independence.proof/1](../../../../models/independence.proof/1/index.md)

---

## Versioning

- **Specification identifier:** `capacity.commitment`
- **Specification version:** `/1`

Version `/1` defines the first canonical capacity-authorization model for the current CERTCRYPT architecture.

Any change that alters:

- authorization meaning
- scope binding
- applicability semantics
- non-transferability
- the boundary between authorization and consumption
- rules-domain binding

requires a new major version.

Already valid commitments under `/1` are not retroactively reinterpreted by later versions.

---

## One-line summary

`capacity.commitment/1` defines the canonical authorization artifact by which CERTCRYPT capacity becomes applicable to fixation without itself proving that capacity was consumed.
