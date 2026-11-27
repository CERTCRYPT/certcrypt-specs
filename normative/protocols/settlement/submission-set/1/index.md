# submission-set/1 · CERTCRYPT Submission Set Protocol

**Identifier:** `submission-set/1`

**Label:** CERTCRYPT Submission Set Specification (submission-set/1)

**Page:** Informative version index

**Specification type:** Protocol

**Layer:** Layer 1 — Protocols

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `submission-set/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `submission-set/1`?

`submission-set/1` defines the canonical execution-request boundary by which one or more autonomous commitments enter fixation under public rules, transported together as one set.

It governs:

- the set envelope and the derivation of its identity
- the closed list of set-level preconditions
- per-member replay boundaries, keyed on what the holder signed
- per-member validation
- the accepted subset and the leaf it forms
- per-member outcomes and the set-level verdicts, including `insufficient_capacity`
- fail-closed conditions

It does **not** by itself make a commitment `Independent`.

---

## Role within CERTCRYPT

Within the architecture:

- the issuer emits the base certificate
- commitments are transported together in a submission set
- the set is NOT atomic: past a closed list of set-level preconditions and the capacity verdict, members are accepted or rejected independently
- only valid settlement plus sufficient finality may produce `Independent`, per accepted member
- `independence_proof` remains the canonical artifact of the positive result, produced per accepted member

When implementations expose request-response APIs, the public contract centers on `submit` as a synchronous-first operation whose internal batching, settlement, retries, and publication concerns remain internal, and whose response carries a per-member outcome or one set-level verdict. The specification fixes guarantees, not HTTP routes; an issuer-side node's interface description is referenced informatively from the specification.

---

## Normative documents

The normative component of `submission-set/1` is:

- [Specification](./specification.md)

---

## Related documents

- [independence.proof/1](../../../../models/independence.proof/1/index.md)
- [settlement-material/1](../../../../ecosystem/settlement/settlement-material/1/index.md)
- [settlement.aggregated.xrpl/1](../../../../ecosystem/settlement/settlement.aggregated.xrpl/1/index.md)
- [capacity.commitment/1](../../../../ecosystem/settlement/capacity.commitment/1/index.md)

---

## Versioning

- **Identifier:** `submission-set/1`

Version `submission-set/1` defines the active public contract for this document. Any further non-backward-compatible semantic or structural change requires a new major version.

## One-line summary

**`submission-set/1` defines the exact request boundary for fixing a set of autonomous commitments, accepted or rejected per member, without itself proving settlement, capacity consumption, or independence.**
