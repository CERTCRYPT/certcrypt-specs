# settlement.aggregated.xrpl/1 · CERTCRYPT XRPL Aggregated Settlement Profile

**Identifier:** `settlement.aggregated.xrpl/1`

**Label:** CERTCRYPT XRPL Aggregated Settlement Profile (settlement.aggregated.xrpl/1)

**Page:** Informative version index

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `settlement.aggregated.xrpl/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `settlement.aggregated.xrpl/1`?

`settlement.aggregated.xrpl/1` defines one concrete settlement profile of reference for aggregated settlement on the XRP Ledger.

It defines:

- one exact `settlement_profile_id`
- one exact settlement mode (`aggregated`)
- the qualifying settlement event on XRPL
- the settlement reference that resolves it uniquely
- the finality profile a verifier evaluates
- the validation procedure a conforming verifier performs

---

## Relationship to `settlement.binding/1`

This profile is one half of a pair, and it is the substrate half.

[`settlement.binding/1`](../../settlement.binding/1/specification.md) defines the cryptographic binding — the anchor, the Merkle derivations, the leaf assignment, the temporal property — substrate-independently, once, for every aggregated settlement profile. This profile **selects** it and does not restate it.

What this profile adds is everything the ledger determines:

| Defined by `settlement.binding/1` | Defined here |
|---|---|
| How a batch is hashed and anchored | What a settlement transaction looks like |
| `settlement_root` / `subtree_root` | How to resolve it uniquely |
| Leaf assignment | What makes it final |
| The temporal rule | How absence is proven |

An implementation supporting more than one profile MUST compute the same `settlement_root` for the same batch under every one. It MUST NOT produce the same anchor: the profile identifier is inside the anchor preimage, so an anchor is bound to the rules that produced it.

---

## Why a substrate needs its own profile

A profile identifier binds a verifier to substrate-specific assertions, and those must be assertions the substrate can actually satisfy.

XRPL has no smart contracts, no named actions, no sub-position inside a transaction, and no irreversibility depth. A profile written for a substrate that has those would ask a verifier to check things that do not exist here.

The binding is shared; the assertions are not. That is the line the identifier draws.

---

## Profile selection

`settlement.aggregated.xrpl/1` is the aggregated settlement profile selected by the active public rules. References to depth-based substrates explain why finality here is binary; they do not describe an alternative profile.

---

## Related documents

- [specification.md](./specification.md) — the normative requirements
- [overview.md](./overview.md) — an informative walkthrough
- [`settlement.binding/1`](../../settlement.binding/1/specification.md) — the substrate-independent binding this profile selects
- `settlement-material/1` — the material contract every settlement profile satisfies
