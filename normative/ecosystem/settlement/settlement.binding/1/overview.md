# CERTCRYPT Aggregated Settlement Binding · Overview

**Identifier:** `settlement.binding/1`

**Label:** CERTCRYPT Aggregated Settlement Binding (settlement.binding/1)

**Page:** Informative overview

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `settlement.binding/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## Purpose

`settlement.binding/1` defines the substrate-independent cryptographic binding shared by CERTCRYPT aggregated settlement profiles. It specifies how a closed batch is represented by an anchor, a settlement root, issuer-level subtree roots, and exact inclusion paths.

The binding can be recomputed without access to a dashboard, node-local state, or a particular ledger implementation. The settlement profile remains responsible for carrying the anchor on its substrate and defining the event, reference, finality, and authorization-to-consumption rules.

## What the binding commits to

The binding defines:

- the `ccab1:<digest>` batch binding anchor and its canonical preimage
- the ordered `settlement_root` derivation
- the per-leaf `subtree_root` derivation
- the interpretation of leaf and commitment inclusion paths
- the temporal requirement that accepted commitments predate settlement

The selected `settlement_profile_id` is included in the batch anchor. The same batch settled under different profiles therefore has the same settlement root but different anchors.

## Verification flow

A verifier applying this specification:

1. validates the selected settlement profile and its finality rules;
2. recomputes the batch anchor from the canonical binding preimage;
3. recomputes the assigned leaf and its path to `settlement_root`;
4. recomputes the commitment path to the assigned `subtree_root`;
5. checks the exact equality constraints among the proof, binding preimage, and settlement material; and
6. checks the temporal property required by the binding.

Any mismatch fails closed. A managed copy, API response, receipt, resolver result, or dashboard view is not a substitute for the canonical proof material.

## Boundary

This specification does not define:

- the qualifying settlement event on a substrate
- how `settlement_ref` is resolved
- the finality profile
- key custody or managed-service behavior
- the truth, semantic validity, or legal validity of the certified subject

It enables independent evaluation of the cryptographic and protocol conditions it defines. It does not make a semantic judgment about the underlying subject.

## Relationship to other specifications

- [specification.md](./specification.md) contains the normative requirements.
- `settlement-material/1` defines the material contract in which the binding is carried.
- `submission-set/1` defines the `cost_commitment` used by each settlement leaf.
- A settlement profile, such as `settlement.aggregated.xrpl/1`, selects this binding and defines substrate-specific carrying and finality.
