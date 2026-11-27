# Overview · capacity.holder-authorization/1

**Identifier:** `capacity.holder-authorization/1`

**Label:** CERTCRYPT Capacity Holder Authorization Specification (capacity.holder-authorization/1)

**Page:** Informative overview

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

> This document is **informative**.
> The normative requirements live in [specification.md](./specification.md).
> Examples are illustrative, not normative.

---

## Purpose

`capacity.holder-authorization/1` answers one question, offline:

> "Was this `capacity.commitment/1` signed by a key actually authorized to sign it, under the active CERTCRYPT System Domain?"

A verifier with access to `system-manifest/1` can answer that question without contacting CERTCRYPT, without consulting any live registry, and without relying on branding or local allowlists.

---

## Position in the signature chain

```
Level 0:  system-manifest/1                     (root attribution material)
Level 1:   └─ system-domain signing key         (delegated by the manifest)
              kid: authorization_issuer_kid
              └─ signs ↓
Level 2:        └─ level1_binding (capacity.holder-authorization/1)
                    declares holder_key_set_root (no stable holder key)
                    └─ authorizes ↓
Level 3:            └─ capacity.commitment/1
                        signed by a non-reused operation leaf key,
                        disclosed with a membership proof to the root
                        └─ consumed in settlement, included in independence.proof/1
```

The authorization declares a `holder_key_set_root` — a Merkle commitment to a set of per-operation keys ([holder-keyset.merkle-sha3-256/1](../../../../protocols/commitment/holder-keyset.merkle-sha3-256/1/index.md)) — instead of a stable key. A stable holder key would be a cross-certificate correlator, so there is none. Each commitment is signed by a distinct, non-reused leaf key proven to belong to the authorized root.

`authorization_issuer_kid` (Level 1) identifies the system-domain key that signs the authorization, and MUST NOT be confused with any holder-level key.

---

## What the signed binding carries

- Anchoring fields (`system_id`, `rules_version`, `system_root_fingerprint`).
- Authorized role (`capacity_commitment_holder`).
- The Level-1 key id (`authorization_issuer_kid`).
- Validity window (`valid_from`, `valid_until`).
- The authorized key set (`holder_key_set_root`).

It carries no holder, contract, pool or issuer identifier. The fixation service keeps which holder and contract it issued the authorization for, and checks that scope when capacity is consumed; that record is not signed and does not travel. Nothing here resembles holder-internal accounting, balances, payment metadata, or a wallet.

---

## What this artifact does not do

- It does not prove `Independent`. That requires the entire chain plus settlement.
- It does not consume capacity. Consumption is bound to the `submission-set/1` submission and settlement.
- It does not prove holder solvency or live operational state.
- It does not introduce a live revocation mechanism. Validity is bounded by `valid_from`/`valid_until` and the system domain's Level-1 key.
- It is not a timestamp authority. Times in this artifact bound delegation validity, not real-world events.

---

## Distinct timescales

`valid_until` of the authorization MAY align with long contractual windows. The TTL applied to individual `capacity.commitment/1` artifacts is shorter and governed by `rules-domain/1`. The two MUST NOT be collapsed: an active authorization does not extend the lifetime of an individual commitment beyond its own `expires_at`.

---

## Signing roles

CERTCRYPT signs `capacity.holder-authorization/1`; the holder signs `capacity.commitment/1`.
