# settlement.binding/1 · CERTCRYPT Aggregated Settlement Binding

**Identifier:** `settlement.binding/1`

**Label:** CERTCRYPT Aggregated Settlement Binding (settlement.binding/1)

**Page:** Informative version index

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `settlement.binding/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `settlement.binding/1`?

`settlement.binding/1` defines the **substrate-independent** half of CERTCRYPT aggregated settlement: how a batch of consumed capacity is aggregated, hashed, and committed to an anchor.

It defines:

- the batch binding anchor (`ccab1:<digest>`) and its canonical preimage
- the `settlement_root` derivation
- the `subtree_root` derivation
- the leaf-assignment interpretation
- the temporal property

None of these involve a ledger. Every digest is computed from the batch's own data, before any transaction exists.

---

## What it does not define

The settlement event, the settlement reference, and the finality profile — all of which are properties of the ledger that carries the settlement. Those belong to a **settlement profile**, which selects this binding by reference.

| | Defined by |
|---|---|
| How a batch is hashed and anchored | `settlement.binding/1` |
| How the anchor reaches a ledger | the settlement profile |
| What makes it final | the settlement profile |
| What a settlement looks like on-chain | the settlement profile |

---

## Why it exists separately

The binding is what a verifier recomputes offline. If two profiles stated it separately, a divergence would not surface as a specification conflict — it would surface as a digest that does not match, on a certificate that should have validated, possibly years later.

Stating it once removes that failure mode by construction. A profile that restates a derivation rather than referencing it is non-conforming, even if the restatement is currently identical.

---

## Selecting profiles

- `settlement.aggregated.xrpl/1` — settlement on the XRP Ledger

Every profile produces the **same `settlement_root`** for the same batch. Profiles produce **different anchors**, because the profile identifier is inside the anchor preimage (§5.1) — an anchor is evidence of settlement under exact rules, and the rules are part of what is committed to.

---

## Related documents

- [specification.md](./specification.md) — the normative requirements
- `settlement-material/1` — the material contract this binding is carried in
- `submission-set/1` — the derivation of `cost_commitment`
