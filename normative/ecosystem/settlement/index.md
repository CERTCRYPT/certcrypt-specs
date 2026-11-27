# settlement · CERTCRYPT ecosystem · settlement category

**Identifier:** `ecosystem/settlement`

**Type:** Ecosystem Category Index

**Layer:** Ecosystem

> This document is **informative**.
> Normative rules are defined only by the versioned documents listed below.

---

## Purpose

This page indexes the active settlement-layer artifacts and contracts of the CERTCRYPT ecosystem.

Settlement specifications govern capacity authorization, the offline settlement-material contract, and concrete settlement profiles under the active public corpus.

## Active families

- [capacity.holder-authorization](./capacity.holder-authorization/index.md)
- [capacity.commitment](./capacity.commitment/index.md)
- [capacity.evidence](./capacity.evidence/index.md)
- [settlement-material](./settlement-material/index.md)
- [settlement.binding](./settlement.binding/index.md)
- [settlement.aggregated.xrpl](./settlement.aggregated.xrpl/index.md)

## Recommended reading order

1. [capacity.holder-authorization](./capacity.holder-authorization/index.md) — offline delegation from system-domain to a commitment-holder key
2. [capacity.commitment](./capacity.commitment/index.md) — pre-settlement authorization signed by the holder under a valid `capacity.holder-authorization/1`
3. [capacity.evidence](./capacity.evidence/index.md) — zero-data, unlinkable projection of the authorized commitment for offline verification
4. [settlement-material](./settlement-material/index.md) — generic offline settlement-material contract
5. [settlement.binding](./settlement.binding/index.md) — the cryptographic binding every aggregated profile selects: anchor, Merkle derivations, leaf assignment, temporal property, defined once and substrate-independently
6. [settlement.aggregated.xrpl](./settlement.aggregated.xrpl/index.md) — concrete profile that instantiates the contract on the XRP Ledger

## Boundary

Settlement specifications define authorization and consumption artifacts; they do not by themselves prove truth, replace cryptographic authenticity, or produce `Independent` outside the proof model.

## One-line summary

The settlement category defines the active artifacts and contracts that govern CERTCRYPT capacity issuance, authorization, and settlement-backed consumption under the active public corpus.
