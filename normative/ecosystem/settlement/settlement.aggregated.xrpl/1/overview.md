# CERTCRYPT XRPL Aggregated Settlement Profile (`settlement.aggregated.xrpl/1`) — overview

**Identifier:** `settlement.aggregated.xrpl/1`

**Label:** CERTCRYPT XRPL Aggregated Settlement Profile (settlement.aggregated.xrpl/1)

**Page:** Informative overview

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

> This document is **informative**.
> All normative rules are defined exclusively in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `settlement.aggregated.xrpl/1`?

`settlement.aggregated.xrpl/1` defines one concrete settlement profile of reference for aggregated settlement on the XRP Ledger.

CERTCRYPT settles consumed capacity by destroying supply on a public, permissionless ledger. This profile says exactly what that means on XRPL, and exactly what a verifier must check to accept it — offline, from public data, without trusting the issuing system.

---

## How settlement works here

One settlement is one XRPL `Payment`:

1. A batch of consumed capacity is aggregated into a settlement container.
2. Its binding digest is computed locally — before any transaction exists — and becomes the anchor `ccab1:<digest>`.
3. The settlement account (`xrpl_settlement_account`) pays the settled amount of the CERT MPT **back to the issuer**, carrying that anchor in the transaction memo.
4. The payment lands in a ledger, and consensus validates it.

Step 3 is what destroys supply. XRPL has no separate burn operation for Multi-Purpose Tokens: paying an MPT to its own issuer reduces the issuance's outstanding amount by exactly that quantity. Moving it to an unspendable address would not do this — the supply would still exist, merely immobile — so the specification requires the issuer as destination.

---

## Three things a depth-based substrate would do differently

### Finality is binary

On a substrate where a block becomes irreversible as later blocks accumulate, a verifier checks a depth. XRPL has no such gradient: a ledger is validated or it is not, and a validated ledger cannot be reorganized.

The proof material still carries irreversibility fields — the shape is shared across profiles — but under this profile they name a validated ledger at or after the inclusion ledger, and `last_irreversible_block_num >= block_num` is the whole finality check. A verifier must not expect a gap.

### There is no sub-position

Some substrates address an action within a block by ordinal. On XRPL the transaction is the atomic unit, and nothing addresses a position inside it. The field stays for shape compatibility and is always `0`.

This matters more than it looks: a value that varied between reads would be indistinguishable from a re-inclusion that never happened, so the specification requires a stable zero rather than any synthesized index.

### Absence is proven by expiry, not by searching

The hardest question in reconciliation is not "did the settlement land?" but "can I prove it never will?".

On some substrates it is answered by sweeping the account's history and showing the sweep was complete. On XRPL, history enumeration cannot be shown to be complete, so its emptiness is not evidence.

Instead the profile uses the transaction's own inclusion bound. A transaction carrying a `LastLedgerSequence` becomes permanently un-includable once a ledger beyond it has been validated. Once that point has passed and the transaction still does not resolve, it never will — a stronger guarantee than a complete search, because it depends on no index at all.

---

## What stays identical

Everything cryptographic. The anchor format, the Merkle derivations, the leaf preimages, the temporal rule — all defined once in [`settlement.binding/1`](../../settlement.binding/1/specification.md), which this profile selects rather than restates.

This is deliberate and testable: an implementation supporting more than one settlement profile must produce the same `settlement_root` for the same batch under every one. The substrate changes how a settlement is carried and proven; it does not change what is being bound.

One nuance worth stating, because it looks like an inconsistency and is not: the **anchors** do differ between profiles. The profile identifier sits inside the anchor preimage, so an anchor is evidence of settlement under exact rules — and the rules are part of what is committed to. An anchor from one profile can never be replayed as evidence under another.

---

## What this profile does not do

- It does not prove a document existed at a time. It binds aggregated consumption, never per-certificate content.
- It does not make the issuing system an authority for time or finality — both come from the ledger.
- It does not grant service authority. A valid settlement says capacity was consumed, nothing more.
