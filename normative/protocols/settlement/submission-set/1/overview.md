# CERTCRYPT Submission Set Protocol (`submission-set/1`) — overview

**Identifier:** `submission-set/1`

**Label:** CERTCRYPT Submission Set Specification (submission-set/1)

**Page:** Informative overview

**Specification type:** Protocol

**Layer:** Layer 1 — Protocols

**Status:** Frozen

> This document is **informative**.
> All normative rules are defined exclusively in [specification.md](./specification.md).
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

It does not by itself make a commitment `Independent`.

---

## A set, not a bundle

A submission set is a transport container of autonomous commitments:

- what concerns the set as a whole is decided once, from a closed list: its envelope and identity, its rules domain, the operator carrying it, the single issuer it belongs to, and whether that issuer's capacity covers it
- past those, members are validated independently, and a failing member does not tumble the valid ones
- the accepted subset forms the settlement leaf
- the response carries either one set-level verdict or a per-member outcome — which commitments were accepted, and why the others were not

The set's identity (`submission_set_id`) is the idempotency anchor and the value the transporting operator's possession proof binds; it is never what an `independence_proof` or settlement anchors. Those anchor each leaf's `subtree_root` over the accepted members. A commitment's own identity, for replay, is what its holder signed.

---

## Role within CERTCRYPT

Within the architecture:

- the issuer emits the base certificate
- commitments are transported together; the set is not atomic and requires no coherence between its members
- CERTCRYPT fixes the accepted subset
- only valid settlement plus sufficient finality may produce `Independent`, per accepted member
- `independence_proof` remains the canonical artifact of the positive result, produced per accepted member
- verification remains possible offline and does not require CERTCRYPT as a live authority

---

## One-line summary

**`submission-set/1` defines the request boundary for fixing a set of autonomous commitments, accepted or rejected per member.**
