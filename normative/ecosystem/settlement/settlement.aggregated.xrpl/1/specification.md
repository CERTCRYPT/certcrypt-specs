# CERTCRYPT XRPL Aggregated Settlement Profile (settlement.aggregated.xrpl/1)

**Identifier:** `settlement.aggregated.xrpl/1`  

**Label:** CERTCRYPT XRPL Aggregated Settlement Profile (settlement.aggregated.xrpl/1)  

**Type:** Ecosystem Specification

**Status:** Frozen

**Layer:** Layer 3 — Ecosystem

**Depends on:** See References *(active normative dependencies are listed below)*  

**Naming convention:**  
`settlement.aggregated.xrpl/1` is the formal identifier.  
CERTCRYPT XRPL Aggregated Settlement Profile (settlement.aggregated.xrpl/1) is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.  

**Audience:** Implementers, verifiers, ecosystem integrators, auditors  

**Purpose:** Define the normative semantics, constraints, and interpretation boundary of settlement.aggregated.xrpl/1 within the active CERTCRYPT public architecture.  

**Intended use:** settlement.aggregated.xrpl/1 is intended to be the authoritative public specification used by conforming implementers, verifiers, auditors, and ecosystem tooling when handling this artifact or behavior.  

**Scope:** Defines the active normative behavior of settlement.aggregated.xrpl/1; adjacent protocols, profiles, operational tooling, and product behavior remain out of scope except where explicitly referenced.  

**Non-goals:** settlement.aggregated.xrpl/1 does not prove truth, semantic validity, legal validity, or live service authority by itself, and MUST NOT be interpreted as a substitute for cryptographic authenticity, Proof of Independence, or managed-service behavior outside its own normative scope.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale

CERTCRYPT settles consumed capacity by destroying supply on a public, permissionless ledger. The settlement record is the evidence a verifier evaluates offline; the issuing system is never the authority for it.

This profile defines that settlement on the **XRP Ledger (XRPL)**.

It is one of potentially several settlement profiles, each describing the same aggregated settlement model on a different substrate. All of them select the same binding (§1.1) and differ only where the substrates genuinely differ.

### 1.1 This profile selects `settlement.binding/1`

The cryptographic binding is **not defined here**. This profile selects
[`settlement.binding/1`](../../settlement.binding/1/specification.md), which defines — substrate-independently, once, for every aggregated settlement profile:

| Component | Defined in |
|---|---|
| Batch binding anchor (`ccab1:` + digest) | `settlement.binding/1` §5 |
| `settlement_root` derivation | `settlement.binding/1` §6 |
| `subtree_root` derivation | `settlement.binding/1` §7 |
| Leaf assignment interpretation | `settlement.binding/1` §8 |
| Temporal property | `settlement.binding/1` §9 |

Those sections apply to this profile unchanged. This document deliberately does NOT restate them: a restatement is a second source of truth, and a divergence between the two would not surface as a specification conflict — it would surface as a digest that does not match, on a certificate that should have validated. Per `settlement.binding/1` §1.1, a profile that restates a derivation rather than referencing it is non-conforming.

What this document defines is the other half: how the settlement is **carried**, **referenced**, and **proven final** on the XRP Ledger.

### 1.2 Why a substrate needs its own profile

A profile identifier binds a verifier to a set of substrate-specific assertions, and those assertions must be ones the substrate can actually satisfy.

XRPL has no smart contracts, no named actions, no sub-position within a transaction, and no irreversibility depth. A profile written for a substrate that has all four would ask a verifier to check things that do not exist here, so the assertions — not the binding — are what makes a profile substrate-specific.

Per `settlement.binding/1` §5.1, the profile identifier is inside the anchor preimage. An anchor produced under this profile therefore can never be replayed as evidence under another, and vice versa.

---

## 2. Scope

This profile defines:

- the qualifying settlement event on XRPL
- the settlement reference that resolves it uniquely
- the proof material contract
- the finality profile
- the validation procedure a conforming verifier MUST perform

This profile does NOT define: key custody, issuance governance, pricing, or any managed-service behavior.

---

## 3. Terminology

Terms not defined here carry the meaning assigned in `settlement-material/1` and `independence.proof/1`.

- **Issuance** — an XRPL Multi-Purpose Token (MPT) issuance, identified by its `MPTokenIssuanceID`.
- **Validated ledger** — a ledger version that XRPL consensus has declared validated. On XRPL this state is final; there is no deeper confirmation.
- **Inclusion bound** — the `LastLedgerSequence` of a transaction: the last ledger in which it can ever be included.
- **Inclusion ledger** — the validated ledger that contains the settlement transaction.
- **Issuance issuer** — the account that created the issuance. An `MPTokenIssuanceID` is the 32-bit sequence of the creating transaction followed by the 160-bit `AccountID` of that account, so the issuer is determined by the issuance identifier and is not a separate value.

---

## 4. Design principles

- The settlement record MUST be independently resolvable from public data alone.
- The issuing system MUST NOT be a source of time, finality, or authority.
- Every substrate-specific assertion MUST be one the substrate can actually satisfy, so a verifier never has to approximate.
- Failure MUST be closed: an unresolvable or ambiguous settlement MUST fail validation rather than be accepted provisionally.

---

## 5. Profile identifier and mode

The exact `settlement_profile_id` of this profile is:

```text
settlement.aggregated.xrpl/1
```

The exact `settlement_mode` of this profile is:

```text
aggregated
```

One valid settlement transaction under this profile MUST correspond to one and only one aggregated settlement container.

That container MAY include multiple leaves and multiple issuers.

Each valid proof path under this profile MUST still resolve to one and only one claimed `subtree_root`.

---

## 6. Profile parameters

The applicable rules domain selecting this profile MUST define the following exact parameters:

- `xrpl_chain_id`
- `xrpl_mpt_issuance_id`
- `xrpl_settlement_account`
- `xrpl_action_name`
- `xrpl_token_symbol`
- `xrpl_asset_scale`
- `xrpl_memo_prefix`
- `root_hash_alg`
- `leaf_hash_alg`

For `/1`:

- `xrpl_action_name` MUST be `payment`
- `xrpl_token_symbol` MUST be `CERT`
- `xrpl_asset_scale` MUST be `2`, and MUST equal the `AssetScale` of the issuance named by `xrpl_mpt_issuance_id`
- `xrpl_memo_prefix` MUST be `ccab1:`
- `root_hash_alg` MUST be `sha3-256-merkle-v1`
- `leaf_hash_alg` MUST be `sha3-256-json-v1`

`xrpl_memo_prefix`, `root_hash_alg` and `leaf_hash_alg` are fixed by `settlement.binding/1`, not chosen by this profile: the binding is substrate-independent, so a rules domain MUST NOT redefine them. They appear in this list only because a rules domain must declare the full parameter set it selects; the authority for their values is the binding.

`xrpl_action_name`, `xrpl_token_symbol` and `xrpl_asset_scale` are this profile's own: they describe the transaction and the asset settled on this substrate. `xrpl_chain_id`, `xrpl_mpt_issuance_id` and `xrpl_settlement_account` identify the network, the issuance and the aggregate settlement account of one deployment, and are values of the rules domain.

### 6.1 Network identity

XRPL defines no chain identifier: a ledger reports a `network_id` (`0` for Mainnet, `1` for Testnet). `xrpl_chain_id` is a namespaced identity string derived from it:

```text
xrpl-network-<network_id>
```

It is an **identity string**. A verifier MUST compare it for equality and MUST NOT parse, decompose, or interpret it. Its only normative requirement is that it differ between networks, so material settled on Testnet can never be accepted as Mainnet. It is the `chain_id` of the settlement material and the first segment of `settlement_ref`.

### 6.2 No contract, issuer, or destination parameter

XRPL has no smart contracts and no named actions; the settlement is a native payment. `xrpl_action_name` names the XRPL **transaction type**, and `payment` is the only value `/1` admits.

This profile defines no contract, issuer, sink or destination parameter. The issuance occupies the place a token contract would, and the destination of the settlement is the issuance issuer (§3), which the issuance identifier determines. A rules domain selecting `/1` MUST NOT define `xrpl_token_contract`, `xrpl_issuer_account`, `xrpl_sink_account`, or any destination parameter.

If any required parameter is absent, ambiguous, or inconsistent across related artifacts, the profile MUST fail closed.

---

## 7. Settlement container model

The qualifying settlement event under this profile is one exact XRPL `Payment` transaction that:

- transfers an amount of the MPT identified by `xrpl_mpt_issuance_id`
- has `Account` = `xrpl_settlement_account`
- has `Destination` = the issuance issuer (§3)
- carries exactly one memo whose data is the batch binding anchor (`settlement.binding/1` §5)
- is included in a validated ledger

### 7.1 Destruction of supply

A payment of an MPT **to its own issuer** destroys the amount paid: the issuance's `OutstandingAmount` decreases by exactly that amount. XRPL provides no separate burn operation for MPTs, and this is the normative mechanism by which consumed capacity ceases to exist.

A transfer to any other account — including an unspendable "black hole" account — MUST NOT be accepted as settlement under this profile. Such a transfer leaves `OutstandingAmount` unchanged: the supply still exists and is merely immobile, which is not destruction.

### 7.2 Unlinkability

The settlement's source MUST always be `xrpl_settlement_account`, never an issuer's own account. The aggregated container is what reaches the ledger, so the public record never reveals which issuer certified what.

### 7.3 Signing

The transaction MAY be signed by the account's own keys or by a delegate the account has authorized on the ledger to send payments on its behalf. Whoever signs, `Account` MUST be `xrpl_settlement_account`: the settlement debits that account, and the signer's identity is not part of the settlement.

### 7.4 Issuance properties

The issuance named by `xrpl_mpt_issuance_id` MUST have `lsfMPTRequireAuth` set: only an account that the issuance issuer (§3) has authorized can hold the token.

The issuance MUST NOT have `lsfMPTCanClawback` or `lsfMPTCanLock` set: the issuance issuer can neither take back a holder's balance nor lock it.

The issuance MAY have `lsfMPTCanTransfer` set, which lets accounts the issuance issuer has authorized transfer the token between them. Such a transfer is not a settlement: it settles no submission set, consumes no capacity, and is outside this profile's verifier result.

With authorization required and neither clawback nor lock available, consumption in a settlement (§7.1) is the only movement of the token this protocol recognizes. The token is a counter of use, not a position that anyone holds.

Anyone can check these properties by reading the `Flags` field of the `MPTokenIssuance` ledger object for `xrpl_mpt_issuance_id` (`lsfMPTCanLock` = `0x02`, `lsfMPTRequireAuth` = `0x04`, `lsfMPTCanTransfer` = `0x20`, `lsfMPTCanClawback` = `0x40`). Like the optional ledger confirmation of §11.3, that reading is outside this profile's verifier result: it MUST NOT be a precondition of `FINALITY_SUFFICIENT` or of `Independent`, and the offline verdict does not depend on it.

---

## 8. Settlement reference

The `settlement_ref` under this profile MUST contain semantic equivalents of at least:

- `chain_id` (as defined in §6.1)
- `trx_id`
- `action_ordinal`
- `batch_id`
- `window_id`

The tuple:

```text
(chain_id, trx_id, batch_id)
```

MUST resolve to one and only one qualifying settlement transaction and one and only one claimed settlement container on the declared XRPL network.

### 8.1 `action_ordinal` under this profile

XRPL has no concept of an action ordinal: a transaction is the atomic unit, and there is no addressable sub-position within it. The field is retained for cross-profile shape compatibility with `settlement-material/1` and MUST be `0`.

A verifier MUST accept `0` and MUST reject any other value. An implementation MUST NOT synthesize an index, a transaction position within the ledger, or any other varying value: a value that changes between reads is indistinguishable from a re-inclusion that did not occur.

### 8.2 Resolved transaction requirements

The transaction a `settlement_ref` names MUST be a `Payment` with `Account` = `xrpl_settlement_account`, `Destination` = the issuance issuer, and a delivered amount whose `mpt_issuance_id` = `xrpl_mpt_issuance_id`. These are obligations of the producer (§11.4): the settlement material declares the transaction and does not carry it, so they are facts an offline verifier cannot read. What the verifier checks offline is the declaration (§13).

### 8.3 Field names on this substrate (informative)

The field names `trx_id`, `action_ordinal`, `block_num`, `block_id`, `last_irreversible_block_num` and `last_irreversible_block_id` are wire names shared by every settlement profile under `settlement-material/1` and `rules/2026-01`; they are retained unchanged. Under this profile they carry the following XRPL values:

| Wire field | XRPL value |
|---|---|
| `trx_id` | the transaction hash of the settlement `Payment` |
| `action_ordinal` | always `0` (§8.1) |
| `block_num` | the `ledger_index` of the validated ledger that includes the transaction |
| `block_id` | the `ledger_hash` of that ledger |
| `last_irreversible_block_num` | the `ledger_index` of a validated ledger observed at or after inclusion |
| `last_irreversible_block_id` | the `ledger_hash` of that observed validated ledger |

This mapping does not alter any requirement of this profile; it only names the substrate values the shared fields hold.

---

## 9. Settlement-proof-material contract

For this profile, settlement material MUST satisfy `settlement-material/1` and MUST contain or deterministically imply at least the following logical components.

### 9.1 `settlement_profile_id`

This field MUST equal:

```text
settlement.aggregated.xrpl/1
```

### 9.2 Settlement action shape

The `settlement_action` MUST declare:

- `from` = `xrpl_settlement_account`
- `quantity` — the settled amount (§9.3)
- `memo` — the batch binding memo
- `name` = `xrpl_action_name`
- `contract` — the MPT issuance identifier (`xrpl_mpt_issuance_id`)

The `contract` field is retained from `settlement-material/1` for cross-profile shape compatibility. Under this profile it names the **issuance**, which is the closest equivalent XRPL has to a token contract: it is the object whose supply the settlement destroys.

### 9.3 Quantity representation

The `quantity` MUST be expressed in the same canonical decimal form used across CERTCRYPT settlement material:

```text
<integer>.<exactly 2 fractional digits> CERT
```

XRPL carries MPT amounts as **integers in the issuance's own scale**; the ledger stores no decimal point. A conforming implementation MUST convert between the two without rounding:

- to settle: the decimal quantity, multiplied by `10^xrpl_asset_scale`, MUST be an exact integer, and that integer is the amount the producer pays. A quantity with more fractional digits than the scale MUST fail closed rather than be rounded.
- to verify offline: the declared quantity MUST have exactly `xrpl_asset_scale` fractional digits, which makes its conversion exact by construction. The on-ledger integer is not in the material; that it equals the declared quantity at the scale is an obligation of the producer (§11.4).

The quantity MUST be strictly positive, and MUST NOT carry a sign, an exponent, or leading zeros in its integer part.

### 9.4 Anchor placement

The batch binding memo MUST be carried in the transaction's `Memos` field, and MUST NOT be carried in the MPT issuance metadata.

This placement is normative because it is what makes the anchor immutable: altering a memo changes the transaction's hash, and no XRPL transaction type can modify the memos of an already-validated transaction. Issuance metadata, by contrast, is mutable by the issuer under the `DynamicMPT` amendment, and an anchor placed there would not be evidence.

### 9.5 Wire form

Under this profile, the settlement material of one leaf is one JSON object with exactly the members below. Every scalar is a JSON string; a producer MUST NOT emit other members, and a verifier MUST NOT derive meaning from any other member. Decimal integers are canonical (no sign, no leading zero except `0`); quantities are canonical decimals with exactly two fractional digits; digests are 64 lowercase hexadecimal characters.

| Member | Content |
|---|---|
| `settlement_profile_id` | `settlement.aggregated.xrpl/1` |
| `settlement_action` | `from`, `quantity` (`<decimal> CERT`), `memo` (`ccab1:` + digest), `contract`, `name`, `chain_id`, `trx_id`, `action_ordinal` (§9.2, §8) |
| `finality_proof` | `block_num`, `block_id`, `last_irreversible_block_num`, `last_irreversible_block_id`, `block_timestamp` (§8.3, §11, §12) |
| `batch_manifest` | `batch_id`, `window_id`, `leaf_count`, `total_quantity`, `settlement_root`, `system_id`, `rules_version`, `settlement_profile_id` |
| `capacity_consumption_proof` | `total_quantity`, `leaf_quantity`, `token_symbol`, `token_contract` (§10.1) |
| `submission_assignment_proof` | `subtree_root`, `leaf_index`, `leaf_preimage` (`settlement.binding/1` §6), `leaf_hash`, `sibling_hashes` (array of digests) |
| `authorization_bridge_proofs` | non-empty array; each element: `resolved_authorization_digest`, `cost_commitment`, `consumed_quantity`, `batch_binding_preimage` (`settlement.binding/1` §5) |
| `coherence_material` | optional: `system_id`, `rules_version`, `settlement_profile_id` |

`batch_manifest` is the unsigned restatement of the batch description that `settlement.binding/1` §6 names: each member repeats a member of the anchored `batch_binding_preimage`, and it carries no signature and no history. `token_contract` names the issuance (`xrpl_mpt_issuance_id`), as `settlement_action.contract` does. Every element of `authorization_bridge_proofs` carries the same `batch_binding_preimage`; there is one element per distinct Level-1 authorization among the leaf's commitments (`settlement-material/1` §9). `coherence_material`, when present, MUST name the proof's `system_id`, `rules_version` and settlement profile.

This form is published as a JSON Schema with the conformance suite (`certcrypt-conformance`, `schemas/input/settlement-material.schema.json`). The schema is necessary, not sufficient: the value rules of this profile and of `settlement.binding/1` remain the verifier's.

---

## 10. Binding and derivations

The batch binding anchor, the `settlement_root` and `subtree_root` derivations, the leaf assignment interpretation and the temporal property are defined in [`settlement.binding/1`](../../settlement.binding/1/specification.md) §5 through §9 and apply to this profile **unchanged**.

A conforming implementation MUST compute them exactly as specified there. This document adds no derivation of its own and modifies none.

### 10.1 Capacity-consumption interpretation

`settlement.binding/1` defines the binding; the mapping onto this substrate's action shape is profile-specific and is defined here.

Under this profile, the capacity-consumption event is the qualifying `Payment` of §7 together with the exact claimed leaf inside the referenced container.

The verifier MUST validate that:

- `settlement_action.from` = `xrpl_settlement_account`
- `settlement_action.contract` = `capacity_consumption_proof.token_contract` = `xrpl_mpt_issuance_id`
- `capacity_consumption_proof.token_symbol` = `xrpl_token_symbol`
- `capacity_consumption_proof.total_quantity` equals the payment quantity exactly
- `capacity_consumption_proof.total_quantity` equals `batch_binding_preimage.total_quantity` exactly
- `batch_manifest.total_quantity` equals `batch_binding_preimage.total_quantity` exactly; `batch_manifest` is required settlement material ([`settlement.binding/1`](../../settlement.binding/1/specification.md) §6), and material without it is `INCOMPLETE`
- every other member that `batch_manifest` shares with `batch_binding_preimage` equals the `batch_binding_preimage` value exactly
- `capacity_consumption_proof.leaf_quantity` equals `leaf_preimage.consumed_quantity` exactly

The reference total is `batch_binding_preimage.total_quantity`, evaluated only after the batch binding anchor has been recomputed from that preimage and matched against the transaction memo ([`settlement.binding/1`](../../settlement.binding/1/specification.md) §5). It is the only copy of the batch total that the anchor binds. `batch_manifest` is not covered by the anchor: its `total_quantity` is accepted only when it repeats the anchored value, and a verifier MUST NOT use it as the reference for the burned quantity. Otherwise material could anchor one total, burn a smaller quantity, and restate the manifest to match the burn.

The same rule applies to every member the manifest restates from the preimage. The anchor binds the batch's description only through `batch_binding_preimage`; each copy in `batch_manifest` is accepted only when it repeats the anchored value, and a verifier MUST NOT use any of them as the reference. Otherwise material could keep the anchor, the leaf and the inclusion path intact while the manifest describes a different batch.

That the payment's destination is the issuance issuer (§7.1) is an obligation of the producer (§11.4), not an offline check: the material declares the debited account and the issuance, and the destination follows from the issuance.

The quantity semantics used to decide whether that leaf quantity is sufficient for the claimed leaf remain governed by the exact applicable rules domain. This profile defines only the mechanical settlement-side interpretation of aggregated consumption.

---

## 11. Finality profile

The finality profile for `/1` describes what the settlement material asserts:

- the resolved transaction is included in the ledger identified by `block_num`
- `block_id` is the `ledger_hash` of that exact ledger
- that ledger is **validated**
- `last_irreversible_block_num` names a validated ledger with `last_irreversible_block_num >= block_num`
- `last_irreversible_block_id` is the `ledger_hash` of the validated ledger at `last_irreversible_block_num`

A producer MUST NOT emit settlement material whose finality proof does not satisfy every item above (§11.4). A verifier evaluates them as §11.3 states.

### 11.1 Finality is binary on this substrate

XRPL finality is not a depth: a ledger is either validated or it is not, and a validated ledger cannot be reorganized. There is no last-irreversible-block boundary trailing behind the head, and no number of subsequent ledgers makes a validated ledger "more final".

The `last_irreversible_block_*` fields therefore name a validated ledger observed at or after the inclusion ledger: either the inclusion ledger itself or any later validated ledger. Because a validated ledger is final, `last_irreversible_block_num >= block_num` establishes finality; a verifier MUST NOT require a gap, and MUST NOT accept material in which `last_irreversible_block_num` is lower than `block_num`.

No provisional, proposed, current-ledger, or submitted-but-unvalidated transaction MAY satisfy this profile. In particular, a transaction reported by the substrate as present but not validated MUST NOT be accepted: submission is not inclusion.

### 11.2 Absence

A transaction that has not been included is not thereby absent. Under this profile, absence is established by **expiry**, not by enumeration of history:

- a transaction carrying a `LastLedgerSequence` becomes permanently un-includable once a ledger beyond it has been validated
- absence MAY be concluded only when the validated ledger has passed that bound **and** the transaction still does not resolve

Neither condition alone is sufficient. A verifier MUST NOT conclude absence from a "not found" response alone, and MUST NOT conclude absence by enumerating an account's transaction history: such enumeration cannot be shown to be complete on this substrate, so its emptiness is not evidence.

### 11.3 Offline evaluation

Finality under this profile is evaluated **offline, exclusively from the artifacts presented**: the `finality_proof` of the settlement material and the finality witnesses (`finality_proofs`) of `independence_proof`. A verifier MUST NOT query the substrate, a node, or any live service to decide `FINALITY_SUFFICIENT`, and an `Independent` result MUST be reachable without network access.

Offline, a verifier MUST check, and MUST fail closed when any check does not hold:

- `finality_proof` is present
- `block_num` and `last_irreversible_block_num` are canonical non-negative decimal integers
- `last_irreversible_block_num >= block_num`
- `block_id` and `last_irreversible_block_id` are present and non-empty
- `independence_proof` carries at least one finality witness, and every witness declares `confirmation_level` = `irreversible`
- every witness declares `substrate` = `xrpl`, and its `block_height` and `timestamp` equal, string for string, `block_num` and `block_timestamp` of the `finality_proof` (`independence.proof/1` §10.6): the settlement material is authoritative, and a witness that disagrees with it is an incoherent proof

`block_id` and `last_irreversible_block_id` are checked for **presence only**. Offline, a verifier cannot establish that a hash names a real validated ledger, and MUST NOT treat that as missing evidence: the offline result attests that the presented material is complete, internally consistent and bound to the public rules, not that the substrate was consulted.

**Optional ledger confirmation.** A party with access to the substrate MAY additionally confirm the producer obligations of §11.4: that `block_id` is the `ledger_hash` of a validated ledger at `block_num`, that the transaction resolves in it, and that it is a `Payment` from `xrpl_settlement_account` to the issuance issuer, of the declared quantity at `xrpl_asset_scale`, with exactly one memo. That confirmation is outside this profile's verifier result: it MUST NOT be a precondition of `FINALITY_SUFFICIENT` or of `Independent`, and its outcome MUST NOT be reported as part of the offline verdict.

### 11.4 Producer obligations

The settlement material declares a transaction it does not carry. A producer MUST NOT emit settlement material unless all of the following hold for the transaction `settlement_action.trx_id` names, read from the substrate:

- it is a `Payment` with `Account` = `xrpl_settlement_account` and `Destination` = the issuance issuer
- its delivered amount is the MPT `xrpl_mpt_issuance_id`, and its integer value divided by `10^xrpl_asset_scale` equals the declared quantity exactly
- it carries exactly one memo, and that memo's data is `settlement_action.memo`
- it is included in a validated ledger, and `block_num`, `block_id` and `block_timestamp` are that inclusion ledger's `ledger_index`, `ledger_hash` and close time (§12), read from that ledger — never from the ledger that was validated when the transaction was submitted, and never from the producer's clock
- `last_irreversible_block_*` name a validated ledger at or after the inclusion ledger
- the issuance named by `xrpl_mpt_issuance_id` has `lsfMPTRequireAuth` set and neither `lsfMPTCanClawback` nor `lsfMPTCanLock` (§7.4)

A producer that cannot read any of these facts — for example after a restart, from a transaction it submitted earlier — MUST read them from the substrate before emitting, and MUST NOT emit material with an empty or guessed value. Material whose recorded inclusion ledger differs from the ledger in which the transaction resolves MUST NOT be emitted.

---

## 12. Temporal property

The temporal property is defined in [`settlement.binding/1`](../../settlement.binding/1/specification.md) §9 and applies unchanged.

That section requires the profile to define what the "final inclusion unit" is on its substrate and how its consensus time is obtained. Under this profile:

- the final inclusion unit is the **validated ledger** containing the settlement transaction (§11)
- its consensus time is that ledger's own close time

XRPL expresses ledger close times as seconds since its own epoch, beginning `2000-01-01T00:00:00Z` (Unix time `946684800`). A producer MUST convert the inclusion ledger's `close_time` to UTC and populate `finality_proof.block_timestamp` with it as RFC 3339. The temporal authority remains the ledger's own consensus close time; the issuing system's clock MUST NOT be used.

---

## 13. Validation procedure

A conforming verifier validating settlement under this profile MUST perform the following logical sequence.

### 13.1 Validate profile selection

The verifier MUST confirm that:

- the exact `settlement_profile_id` is `settlement.aggregated.xrpl/1`
- the exact `settlement_mode` is `aggregated`
- the exact profile parameters defined by the rules domain are available

### 13.2 Validate settlement reference

The verifier MUST confirm that `settlement_ref` has exactly five segments and that each equals the corresponding settlement-material field (`rules/2026-01` §9), and that `settlement_action.chain_id` = `xrpl_chain_id`.

The facts of the resolved transaction itself — its type, `Account`, `Destination`, delivered issuance and memo count — are producer obligations (§11.4). An offline verifier does not read them, and MUST NOT report them as checked.

### 13.3 Validate settlement action shape

The verifier MUST validate:

- `from` = `xrpl_settlement_account`
- `name` = `xrpl_action_name`
- `contract` = `xrpl_mpt_issuance_id`
- `action_ordinal` = `0`
- the quantity is present, has exactly `xrpl_asset_scale` fractional digits, carries the symbol `xrpl_token_symbol`, and is strictly positive
- the memo equals the batch binding memo (§13.4)

### 13.4 Validate binding

The verifier MUST recompute the batch binding digest from the declared preimage and MUST confirm that the memo equals `xrpl_memo_prefix` concatenated with that digest, using the derivation of [`settlement.binding/1`](../../settlement.binding/1/specification.md) §5.

### 13.5 Validate merkle path

The verifier MUST recompute `subtree_root` and `settlement_root` using the derivations of [`settlement.binding/1`](../../settlement.binding/1/specification.md) §6 and §7, and MUST confirm the claimed path resolves.

### 13.6 Validate finality

The verifier MUST perform the offline checks of §11.3, including `last_irreversible_block_num >= block_num`.

### 13.7 Validate temporal property

The verifier MUST evaluate the temporal property of §12 from `finality_proof.block_timestamp` alone.

---

## 14. Failure semantics

Any of the following MUST cause validation to fail:

- profile identifier or mode mismatch
- missing, ambiguous, or inconsistent profile parameters
- a `settlement_ref` whose segments do not equal the material's fields
- a settlement action whose `from`, `name`, `contract` or `chain_id` differs from the rules domain's value
- `action_ordinal` other than `0`
- a quantity that is not strictly positive or does not have exactly `xrpl_asset_scale` fractional digits
- a memo that does not equal the recomputed binding
- a Merkle path that does not resolve, or a tree width other than the anchored `leaf_count`
- a finality proof that fails any offline check of §11.3, including `last_irreversible_block_num` lower than `block_num` and empty ledger hashes
- a `block_timestamp` after the commitment's `expires_at`

A verifier MUST NOT downgrade any of these to a warning, and MUST NOT accept settlement provisionally pending later confirmation.

---

## 15. Managed interfaces

Operational tooling, key custody, issuance governance, and refill policy are outside this profile. Nothing in this document grants authority to any operator, and a verifier MUST NOT infer service authority from a valid settlement.

---

## 16. Conformance

An implementation conforms to `settlement.aggregated.xrpl/1` if and only if it:

- produces or validates settlement material satisfying §9
- performs the validation procedure of §13 in full
- fails closed on every condition of §14
- conforms to [`settlement.binding/1`](../../settlement.binding/1/specification.md) in full

The last requirement is testable and MUST be tested: an implementation supporting more than one settlement profile MUST produce the same `settlement_root` for the same batch under every profile.

It MUST NOT be expected to produce the same **anchor**: per `settlement.binding/1` §5.1 the profile identifier is inside the anchor preimage, so the anchors differ by construction. An implementation that produced identical anchors under two profiles would be non-conforming.
