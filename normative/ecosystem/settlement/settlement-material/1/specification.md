# CERTCRYPT Settlement Material Specification (settlement-material/1)

**Identifier:** `settlement-material/1`  

**Label:** CERTCRYPT Settlement Material Specification (settlement-material/1)  

**Type:** Ecosystem Specification

**Status:** Frozen

**Layer:** Layer 3 — Ecosystem

**Depends on:** See References *(active normative dependencies are listed below)*  

**Naming convention:**  
`settlement-material/1` is the formal identifier.  
CERTCRYPT Settlement Material Specification (settlement-material/1) is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.  

**Audience:** Implementers, verifiers, ecosystem integrators, auditors  

**Purpose:** Define the normative semantics, constraints, and interpretation boundary of settlement-material/1 within the active CERTCRYPT public architecture.  

**Intended use:** settlement-material/1 is intended to be the authoritative public specification used by conforming implementers, verifiers, auditors, and ecosystem tooling when handling this artifact or behavior.  

**Scope:** Defines the active normative behavior of settlement-material/1; adjacent protocols, profiles, operational tooling, and product behavior remain out of scope except where explicitly referenced.  

**Non-goals:** settlement-material/1 does not prove truth, semantic validity, legal validity, or live service authority by itself, and MUST NOT be interpreted as a substitute for cryptographic authenticity, Proof of Independence, or managed-service behavior outside its own normative scope.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale
This specification defines the public offline settlement-material contract for settlement-backed CERTCRYPT independence paths.

It defines:

- what settlement material is
- what one exact `settlement_profile_id` MUST determine
- how settlement binding, finality, leaf assignment, and settlement-bound capacity consumption are represented for offline verification
- how the bridge between pre-settlement authorization and settlement-fixed consumption MUST be exposed under public rules
- what fail-closed conditions apply when any required settlement component is missing or ambiguous

This specification does **not** define:

- certificate issuance semantics
- submission-set transport
- backend-specific settlement execution choreography
- wallet or ledger UX
- complete verification against original material

Those concerns belong to separate specifications.

---

## 2. Scope

This specification applies to all systems, implementations, SDKs, settlement adapters, proof builders, verifiers, packaging layers, and managed delivery layers that:

- construct
- serialize
- transmit
- validate
- store
- inspect

settlement material claiming conformity with CERTCRYPT.

Any implementation that relies on settlement-derived material for standard offline `Independent` verification MUST conform to this specification.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

---

## 4. Design principles

`settlement-material/1` is designed around the following principles:

- **Proof without data custody:** Settlement-path verification MUST rely on the carried artifact set and public rules, not on live chain queries or internal CERTCRYPT data.
- **Deterministic verification:** The same settlement material under the same settlement profile and rules domain MUST produce the same verifier outcome.
- **Exact profile binding:** Sufficient finality, capacity consumption, and leaf assignment MUST be interpreted only under one exact settlement profile and one exact rules domain.
- **Institutional independence:** Settlement-path verification MUST remain possible without continued operator custody or hosted CERTCRYPT infrastructure.
- **Interpretation boundaries:** Settlement material enables independent evaluation of the settlement path under public rules. It does not create independence by itself and is not a semantic truth claim.

---

## 5. Definitions

For the purposes of this specification:

- **settlement profile** means the exact public-rule-defined contract selected by one `settlement_profile_id`
- **settlement material** means the exact offline artifact set required by that settlement profile
- **settlement finality proof** means the exact material by which sufficient finality is evaluated for that profile
- **capacity consumption proof** means the exact settlement-bound material by which valid CERTCRYPT capacity consumption is established
- **leaf assignment proof** means the exact material by which one claimed `subtree_root` is assigned to one settlement context
- **authorization-to-consumption bridge** means the exact public-rule-defined relationship by which pre-settlement authorization becomes settlement-fixed consumption for the claimed independence path

---

## 6. Settlement profile completeness

Every public rules domain that permits settlement-backed `Independent` MUST define one or more exact `settlement_profile_id` values.

For each permitted `settlement_profile_id`, the applicable public rules MUST define all of the following:

1. one exact settlement mode
2. one exact method for resolving `settlement_ref`
3. one exact finality profile sufficient for canonical acceptance
4. one exact settlement-material contract
5. one exact capacity-consumption interpretation
6. one exact authorization-to-consumption bridge
7. one exact leaf-assignment interpretation

If any of those elements is omitted, only partially specified, discretionary, or left to implementation-local policy, that `settlement_profile_id` MUST be treated as non-conformant and MUST fail closed.

---

## 7. Mandatory semantics

A conforming settlement-material contract MUST be sufficient to validate, offline and under one exact rules domain:

- one exact settlement context
- sufficient settlement finality
- settlement-bound CERTCRYPT capacity consumption
- one exact leaf assignment
- one exact authorization-to-consumption bridge
- cross-artifact coherence with the claimed CERTCRYPT System Domain and rules domain

No conforming profile MAY rely on a verifier privately inventing missing bookkeeping, missing finality logic, missing capacity-consumption semantics, or missing authorization-bridge logic.

---

## 8. Required logical components

A conforming settlement-material set MUST contain or deterministically imply at least the following logical components. Their serialization is not left to implementations: the selected settlement profile fixes one exact wire form (§9.5 of `settlement.aggregated.xrpl/1`), and a producer and a verifier under that profile use it.

### 8.1 `settlement_profile_id`

Identifies the exact settlement profile governing interpretation of the proof material.

This field MUST be present or deterministically derivable.

### 8.2 `settlement_ref`

Resolves to one and only one settlement event or one and only one aggregated settlement container under the applicable public rules.

### 8.3 `finality_proof`

Contains the exact material required to evaluate the finality profile for the selected `settlement_profile_id`.

It MUST be sufficient to validate the exact deterministic finality parameters required by the applicable public rules.

### 8.4 `capacity_consumption_proof`

Contains the exact material required to establish that valid CERTCRYPT capacity was consumed within the referenced settlement context.

It MUST be inseparably tied to that settlement context.

It MUST NOT remain reusable across different settlement contexts.

### 8.5 `submission_assignment_proof`

Contains the exact material required to assign one claimed `subtree_root` (the Merkle root over a leaf's accepted commitments) to the referenced settlement context.

When settlement is aggregated, this component MUST include the exact inclusion and bookkeeping semantics required to determine one and only one valid assignment. The per-commitment inclusion path (`commitment_id` into `subtree_root`) is carried per certificate alongside the base certificate, not in this component.

### 8.6 `authorization_bridge_proof`

Contains the exact material required to show how the pre-settlement authorization path admitted the settlement-fixed consumption claimed by the proof.

This component MUST make the relationship between authorization and consumption mechanically evaluable under public rules.

It MUST NOT collapse authorization into consumption.

It MUST instead prove, under the selected profile, how one exact authorized path became one exact consumed path in settlement.

### 8.7 `coherence_material`

Contains any exact profile-required context needed to ensure that the settlement context, finality proof, capacity-consumption proof, leaf assignment proof, and authorization bridge all refer to the same exact CERTCRYPT System Domain, rules domain, and independence result. Where the other components already bind that context, the profile MAY make this component optional; when present, it MUST name the same system domain, rules domain and settlement profile as the proof.

### 8.8 `batch_manifest`

An unsigned restatement of the batch the settlement container carries: its identifiers, width, total and root. It is required where the profile's binding requires it ([`settlement.binding/1`](../../settlement.binding/1/specification.md) §6), and each of its members is accepted only when it repeats the anchored value. It is a member of the settlement material, not a separate artifact, and it carries no signature and no history of batches.

---

## 9. Authorization-to-consumption bridge

The bridge from pre-settlement authorization to settlement-fixed consumption is mandatory.

For every permitted `settlement_profile_id`, the applicable public rules MUST define one exact authorization-to-consumption bridge.

That bridge MAY be expressed through:

- settlement-carried authorization lineage
- deterministic settlement-side derivation from the referenced authorization material
- exact consumed-slot or consumed-lock semantics
- another explicitly defined public-rule mechanism

It MUST NOT be expressed through:

- node-local memory
- retry logs
- operational caches
- managed-service assertions
- heuristic reconstruction after the fact

If the verifier cannot validate the bridge deterministically from the settlement-material contract and the other required public artifacts, the claimed independence result MUST be rejected.

---

## 10. Finality semantics

For every permitted `settlement_profile_id`, the applicable public rules MUST define one exact finality profile.

That profile MUST specify the exact deterministic parameters required for canonical acceptance, including any applicable:

- confirmation depth
- epoch boundary
- challenge window
- attestation threshold
- timeout
- equivalent deterministic finality criterion

If the finality profile for the selected `settlement_profile_id` is absent, incomplete, or not evaluable from the required proof material, verification MUST fail.

---

## 11. Direct and aggregated assignment

If the selected settlement profile is direct, the `submission_assignment_proof` MUST still be sufficient to show that the referenced settlement context is the unique carrier of the claimed leaf's capacity consumption.

If the selected settlement profile is aggregated, the `submission_assignment_proof` MUST additionally fix:

- one exact container
- one exact membership interpretation
- one exact bookkeeping interpretation
- one exact claimed leaf assignment

No reusable root, receipt, index, path, or bookkeeping hint MAY be treated as sufficient if it permits more than one plausible assignment.

---

## 12. Validation procedure

A conforming verifier validating settlement material MUST perform the following logical sequence.

### 12.1 Validate rules domain and settlement profile

The verifier MUST identify one exact `rules_version` and one exact `settlement_profile_id`.

If exact selection fails, validation MUST fail.

### 12.2 Validate settlement resolution

The verifier MUST validate that `settlement_ref` resolves uniquely under the selected settlement profile.

### 12.3 Validate finality

The verifier MUST validate `finality_proof` against the exact finality profile required by the selected settlement profile.

If sufficient finality cannot be established, validation MUST fail.

### 12.4 Validate capacity consumption

The verifier MUST validate `capacity_consumption_proof` under the selected settlement profile.

If the claimed capacity consumption could be reused, rebound, or interpreted outside the referenced settlement context, validation MUST fail.

### 12.5 Validate leaf assignment

The verifier MUST validate `submission_assignment_proof` and reject any context that permits more than one plausible leaf assignment.

### 12.6 Validate authorization bridge

The verifier MUST validate `authorization_bridge_proof` and reject any context in which authorization is merely presumed, cached, or retrospectively inferred rather than mechanically connected to the claimed settlement-fixed consumption under public rules.

### 12.7 Validate cross-artifact coherence

The verifier MUST validate that all settlement-proof components resolve to one exact CERTCRYPT System Domain, one exact rules domain, one exact settlement context, and one exact claimed independence path.

---

## 13. Failure semantics

Validation MUST fail if any required condition fails, including at least:

- unsupported or ambiguous `settlement_profile_id`
- missing or ambiguous finality profile
- missing or ambiguous authorization-to-consumption bridge
- missing or ambiguous leaf assignment
- capacity-consumption proof that is not settlement-bound
- proof material requiring live discretionary interpretation for the standard offline path
- cross-artifact mismatch between settlement-proof components and the claimed CERTCRYPT context

No partial success state MAY substitute for a failed required condition.

---

## 14. Managed interfaces

Managed delivery, indexing, or retrieval layers MAY expose settlement proof material.

Such layers:

- MUST be optional
- MUST be non-authoritative
- MUST NOT redefine the selected settlement profile
- MUST NOT supply missing finality or authorization-bridge semantics by private policy

---

## 15. Conformance

An implementation conforms to `settlement-material/1` if and only if:

- it preserves the mandatory semantics defined in this document
- it defines one exact offline proof-material contract per permitted `settlement_profile_id`
- it keeps authorization distinct from consumption while making their bridge mechanically evaluable
- it rejects incomplete, ambiguous, heuristic, or live-authority-dependent standard verification paths

Partial implementations MUST NOT claim full conformance.

---

## 16. Final normative statement

`settlement-material/1` defines the exact public offline settlement-material contract by which one selected settlement profile exposes settlement resolution, sufficient finality, leaf assignment, settlement-bound CERTCRYPT capacity consumption, and the authorization-to-consumption bridge required for deterministic independent evaluation under public rules.

---

## 17. Versioning & extensibility

This `/1` specification defines the current active public contract for `settlement-material/1`.

Once frozen, this version MUST NOT be modified in place in any way, including editorial, typographic or clarifying changes that would leave its normative meaning unchanged. Any change MUST be published under a new version identifier.

---

## 18. References

- CERTCRYPT Specifications
    - [security-model/1 — CERTCRYPT Security Model](../../../../foundation/security-model/1/index.md)
    - [system-domain/1 — CERTCRYPT System Domain](../../../../foundation/system-domain/1/index.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../../../foundation/rules-domain/1/index.md)
    - [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../../../protocols/CCCP/1/index.md)
    - [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../../../protocols/CCSP/1/index.md)
    - [CCVP/1 — CERTCRYPT Consistency Verification Protocol](../../../../protocols/CCVP/1/index.md)
    - [settlement.aggregated.xrpl/1 — CERTCRYPT XRPL Aggregated Settlement Profile](../../settlement.aggregated.xrpl/1/index.md)
    - [settlement.binding/1 — CERTCRYPT Aggregated Settlement Binding](../../settlement.binding/1/index.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)

---

**End of settlement-material/1**
