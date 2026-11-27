# CERTCRYPT Verification Package Specification (verification-package/1)

**Identifier:** `verification-package/1`  

**Label:** CERTCRYPT Verification Package Specification (verification-package/1)  

**Type:** Ecosystem Specification

**Status:** Frozen

**Layer:** Layer 3 — Ecosystem

**Depends on:** See References *(active normative dependencies are listed below)*  

**Naming convention:**  
`verification-package/1` is the formal identifier.  
CERTCRYPT Verification Package Specification (verification-package/1) is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.  

**Audience:** Implementers, verifiers, ecosystem integrators, auditors  

**Purpose:** Define the normative semantics, constraints, and interpretation boundary of verification-package/1 within the active CERTCRYPT public architecture.  

**Intended use:** verification-package/1 is intended to be the authoritative public specification used by conforming implementers, verifiers, auditors, and ecosystem tooling when handling this artifact or behavior.  

**Scope:** Defines the active normative behavior of verification-package/1; adjacent protocols, profiles, operational tooling, and product behavior remain out of scope except where explicitly referenced.  

**Non-goals:** verification-package/1 does not prove truth, semantic validity, legal validity, or live service authority by itself, and MUST NOT be interpreted as a substitute for cryptographic authenticity, Proof of Independence, or managed-service behavior outside its own normative scope.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale
This specification defines the structure, semantics, and validation requirements of the `verification_package` within CERTCRYPT.

A `verification_package` is a standardized optional offline verification package by which a verifier can evaluate a certificate in either `Issued` or `Independent` state without requiring CERTCRYPT, the issuer, or any other live authority.

This specification operates within the CERTCRYPT model of Proof of Independence.

The `verification_package` exists to reduce operational complexity in real-world verification scenarios by minimizing the need for artifact discovery, reconstruction, or external dependency resolution.

This document defines:

- what a `verification_package` is
- what it MUST contain for `Issued` and `Independent` verification
- how offline verification sufficiency MUST be interpreted
- how package integrity and anti-splicing semantics MUST be enforced
- what complete verification against original material requires

This document does **not** define:

- certificate issuance semantics
- `submission-set`
- settlement execution
- capacity issuance or lock workflows
- the canonical semantics of `independence_proof`

Those concerns belong to separate specifications.

---

## 2. Scope

This specification applies to all systems, implementations, SDKs, verifiers, managed delivery layers, issuer-side packaging flows, and archival or export mechanisms that:

- construct
- serialize
- transmit
- validate
- store
- inspect

a `verification_package` claiming conformity with CERTCRYPT.

Any implementation that uses `verification_package` as the offline verification container for CERTCRYPT certificates MUST conform to this specification.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

---

## 4. Design principles

`verification-package/1` is designed around the following principles:

- **Proof without data custody:** A verification package assembles the artifacts needed for offline verification without requiring platform-held documents, identities, or internal systems.
- **Deterministic verification inputs:** The package MUST carry one exact artifact set whose integrity and coherence can be checked mechanically under public rules.
- **Institutional independence:** Verification MAY be performed from the package or from independently obtained artifacts, but in either case it MUST NOT depend on a live CERTCRYPT service.
- **Infrastructure neutrality:** The package is a transport and assembly convenience, not a competing semantic model or managed-service dependency.
- **Interpretation boundaries:** A `verification_package` does not produce Proof of Independence, does not create truth, and does not replace original material where original-material verification is required.

---

## 5. Architectural role

Within the current CERTCRYPT architecture:

- issuers emit base certificates
- CERTCRYPT does not emit certificates
- `independence_proof` remains the canonical independence artifact
- `verification_package` is a standardized offline verification package, not the ontological source of independence
- verification remains offline and MUST NOT depend on CERTCRYPT as a live authority
- original material MAY still be required for complete verification, but MUST be provided independently of CERTCRYPT

`verification-package/1` defines the package semantics required to verify, not the semantics of issuance, settlement, or independence production.

It MUST NOT redefine `independence_proof`.

---

## 6. Definitions

For the purposes of this specification:

- **verification package** means the self-contained artifact set required to perform offline verification under the applicable verification target
- **base certificate** means the issuer-emitted certificate being verified
- **independence proof** means the canonical artifact proving that a leaf reached `Independent` under public rules
- **supporting proof material** means any additional material required by the applicable proof model or rule set to validate `independence_proof` offline
- **original material** means the subject material independently supplied by the verifier when required for complete verification
- **issued verification** means verification of the issuer-emitted certificate without evaluating `Independent`
- **independent verification** means verification that a certificate validly reached `Independent`
- **complete verification** means verification against original material, package artifacts, and public rules where the applicable rule set requires original-material comparison

---

## 7. Verification package semantics

A `verification_package` MUST be interpreted as a verification container only.

A `verification_package` MUST NOT be treated as an authority.

It is only a transport container for independently verifiable artifacts.

No package, widget, verification view, managed delivery layer, or branded presentation derived from a `verification_package` MAY be presented as a trust seal, institutional endorsement, or semantic upgrade of the underlying proof result.

It MUST NOT be interpreted as:

- semantic truth of issuer assertions
- semantic validation by CERTCRYPT
- an authority independent of the artifacts it carries
- a replacement for complete verification against original material

The meaning of the package is wholly derived from:

- the base certificate
- the contained independence artifacts when present
- supporting proof material when required
- the applicable public rules
- original material when the selected verification path requires it

Any artifact in the package whose meaning depends on a rules domain MUST correspond to the same exact rules domain required by the contained `independence_proof` or by the claimed verification target under the applicable public rules.

Trustlessness in CERTCRYPT does not mean the package proves all issuer assertions true.

It means the verifier can evaluate or refute the relevant claims under public rules without relying on the issuer or on CERTCRYPT as a live authority.

The package standardizes delivery convenience.

It does not standardize truth, and it does not monopolize verification.

A `verification_package` MUST NOT be required by any conforming verifier as the only valid input for verification.

A conforming verifier MUST NOT reject verification solely because a `verification_package` was not provided, if equivalent required artifacts are otherwise available under the same public rules.

A `verification_package` MUST NOT introduce any additional verification semantics beyond those defined by the contained artifacts and applicable public rules.

A `verification_package` MUST NOT elevate, strengthen, or reinterpret the semantic meaning of any contained artifact beyond what is defined by that artifact and the applicable public rules.

A valid `verification_package` MUST NOT be interpreted as stronger evidence than the underlying artifacts when those artifacts are evaluated independently under the same public rules.

No conforming verifier MAY treat package readability, package opening success, artifact presence, or superficial structural plausibility as sufficient for `Independent`.

No conforming verifier MAY return or present `Independent` merely because:

- the package opens successfully
- an object labeled as `independence_proof` is present
- a certificate signature validates
- a `system_id` string looks CERTCRYPT-like
- a `settlement_ref`, transaction reference, receipt, or root-like value appears syntactically plausible
- the artifact set looks visually or structurally similar to a conforming CERTCRYPT package

Those conditions MAY be diagnostically useful, but they are never a substitute for exact proof-context validation under the applicable public rules.

Partial, best-effort, fallback, compatibility-mode, or heuristically downgraded verification MUST NOT be represented as successful `Independent` verification.

---

## 8. Verification targets

### 8.1 `Issued`

A `verification_package` MAY be used to verify a certificate in `Issued` state only.

In that case, the package MUST be sufficient to:

- validate the base certificate structure and integrity
- validate the base certificate signature or equivalent issuance authenticity mechanism
- perform any required original-material comparison under the applicable issuance rules

### 8.2 `Independent`

A `verification_package` MAY be used to verify a certificate in `Independent` state.

In that case, the package MUST be sufficient to:

- verify the base certificate as `Issued`
- verify the contained `independence_proof` according to its normative semantics
- provide all additional material required to validate that proof offline under the applicable public rules

The verification target is the individual base certificate carried in the package, not the leaf as an aggregate. Although the contained `independence_proof` establishes `Independent` at the leaf level, the package MUST be sufficient to project that result onto the exact base certificate it carries, by binding that certificate to one accepted commitment whose `commitment_id` includes into the proof's `subtree_root` through the inclusion material the proof requires. This is the per-certificate projection defined in [independence.proof/1 §7.10](../../../../models/independence.proof/1/specification.md). The package MUST NOT present a leaf as itself `Independent` as an aggregate, nor expose any other base certificate carried in the same leaf.

Submission receipts, API responses, dashboards, managed copies, or transport-level acknowledgments MUST NOT be treated as substitutes for an `Independent`-sufficient `verification_package`.

---

## 9. Required composition

### 9.1 Common required members

Every conforming `verification_package` MUST include:

- `base_certificate`
- `verification_context`

### 9.2 Additional requirements for `Independent`

For `Independent` verification, a conforming `verification_package` MUST include:

- `independence_proof`
- the supporting proof material required by the applicable `independence_proof` model and public rules: under the active architecture for `/1`, `capacity_evidence`, `commitment_inclusion_proof` and `settlement_material` (§9.4)

Under the active architecture for `/1`, that supporting proof material MUST be limited to the exact minimal set required to validate the contained `independence_proof` offline under public rules: the capacity evidence of the certificate's commitment (zero-data path), the per-commitment inclusion path of that commitment into the proof's `subtree_root`, and the settlement material of the leaf.

That minimal set MUST include or deterministically imply, validated in causal order — authorized-and-consumed capacity first, then the settlement that anchors that consumption:

- on the zero-data path, the exact capacity evidence required to recompute the verified certificate's `commitment_id` and to validate capacity authorization and the holder signature offline, without exposing stable identifiers (see `independence.proof/1 §9` input 7 and §10.4.2)
- the exact verification context required to validate system-domain and rules-domain coherence (`verification_context`)
- the per-commitment inclusion path binding that commitment into the proof's `subtree_root` (`commitment_inclusion_proof`, [settlement.binding/1](../../../settlement/settlement.binding/1/specification.md) §7)
- the exact supporting material required to resolve and validate the aggregated settlement binding already claimed by the contained `independence_proof` (`settlement_material`, [settlement-material/1](../../../settlement/settlement-material/1/specification.md) under the settlement profile the rules select); the settlement reference itself is the proof's `settlement_ref`

The capacity evidence is the offline-transportable projection of the capacity artifacts (`capacity.commitment/1` and `capacity.holder-authorization/1`); its canonical form is fixed by the applicable public rules for the zero-data capacity profile. It MUST preserve the system's zero-data and cross-certificate unlinkability properties: it MUST NOT carry original material, and it MUST NOT carry stable identifiers in clear (see §18).

The package MUST NOT include:

- a replica of the whole batch (the leaves of the container and their material); the settlement material's own `batch_manifest` (`settlement-material/1` §8.8) is not such a replica
- other leaves from the same settlement container
- unrelated settlement artifacts
- redundant copies of the same logical binding under different names or formats

### 9.2.1 Minimal Independent verification set

For `Independent`, a conforming `verification_package` MUST contain the minimal artifact set required to complete standard offline verification of the claimed independence result under the applicable public rules.

That minimal set defines the mandatory baseline for any verifier claiming support for `Independent` verification under this specification.

No implementation MAY claim conforming `Independent` verification support while omitting, downgrading, heuristically substituting, or operationally bypassing any element of that minimal set.

That minimal set MUST be sufficient to validate, without live authority access:

- exact system-domain attribution
- exact rules-domain selection
- exact leaf binding
- exact settlement-context binding
- capacity-consumption binding as required by the contained proof model
- sufficient settlement finality as defined by the applicable rules domain
- inclusion binding when aggregated settlement semantics apply

No receipt, settlement-root value, container identifier, transport acknowledgment, or superficially similar settlement evidence MAY substitute for that baseline if exact CERTCRYPT domain attribution and exact proof-context binding have not been validated.

No verifier implementation MAY treat the mere coexistence of `base_certificate`, `independence_proof`, and a plausible settlement or receipt artifact as sufficient package coherence.

The verifier MUST validate that those artifacts refer to one exact certificate context, one exact leaf context, one exact rules domain, one exact system domain, and one exact settlement context under public rules.

If the package requires the verifier to reconstruct any of the above through discretionary discovery, live chain exploration, managed-service interpretation, or heuristic artifact selection, the package MUST be treated as insufficient for `Independent`.

The package MUST also be treated as insufficient if the contained settlement-derived proof material does not expose the exact finality profile, leaf-assignment interpretation, capacity-consumption interpretation, and authorization-to-consumption bridge required by the aggregated settlement profile the applicable public rules select for the declared `rules_version`.

### 9.3 Optional material

The only optional member a `verification_package` defines is `settlement_reference` (§9.4), a convenience copy of the proof's `settlement_ref`. Packaging, transport or archival metadata is not carried inside the package object: a member outside §9.4 makes the package non-conformant. Metadata a delivery needs travels beside the package, in the transport, and never changes how the package is read.

Optional material MUST NOT:

- alter package semantics
- redefine `independence_proof`
- create a new public certificate state
- become required for verification if it is not normatively required by the applicable public rules

### 9.4 Member set

A `verification_package` is one JSON object whose members are exactly these, each at most once:

| Member | JSON type | Present | Content |
|---|---|---|---|
| `base_certificate` | object | always | The issuer-emitted certificate ([CCSP/1](../../../../protocols/CCSP/1/specification.md)) |
| `verification_context` | object | always | Exactly `{rules_version, system_id}`, two non-empty strings: the rules version and system domain the certificate's signed payload names, and the proof's when present |
| `independence_proof` | object | for `Independent` | The proof ([independence.proof/1](../../../../models/independence.proof/1/specification.md)) |
| `capacity_evidence` | object | for `Independent`, zero-data path | The evidence of the certificate's commitment ([capacity.evidence/1](../../../settlement/capacity.evidence/1/specification.md)) |
| `commitment_inclusion_proof` | object | for `Independent` | The per-commitment inclusion path (§9.4.1) |
| `settlement_material` | object | for `Independent` | The leaf's settlement material ([settlement-material/1](../../../settlement/settlement-material/1/specification.md)) |
| `settlement_reference` | string | optional | Equal to the proof's `settlement_ref`; it carries no meaning of its own and MUST NOT appear without an `independence_proof` |

No other member is permitted. In particular a package carries no original material (§10), no `system_foundation` (§9.5), no other leaf, and no member naming a version, a target or a nested container of supporting material. A verifier that meets any other member MUST reject the package rather than read around it.

### 9.4.1 `commitment_inclusion_proof`

The per-commitment inclusion path of [settlement.binding/1](../../../settlement/settlement.binding/1/specification.md) §7 is a closed object of five members:

- `commitment_id` — 64 lowercase hexadecimal characters; on the zero-data path, the digest of the commitment's capacity evidence ([capacity.evidence/1](../../../settlement/capacity.evidence/1/specification.md) §7.1);
- `commitment_leaf_hash` — 64 lowercase hexadecimal characters, which the verifier recomputes from `commitment_id` (settlement.binding/1 §7) and requires equal;
- `commitment_index` — the commitment's position in the leaf's sub-tree, a canonical unsigned integer string;
- `commitment_siblings` — the sibling hashes, bottom-up, each 64 lowercase hexadecimal characters;
- `subtree_size` — the number of commitments in the sub-tree, a canonical positive integer string greater than `commitment_index`.

A path with any other member, or a member of another form, is malformed and the package is rejected.

### 9.5 The system foundation is not a member

The `system-foundation/1` statement through which a verifier attributes the proof to its system domain is applicable public rules material, not package content. The verifier obtains it on its own and accepts it only when its `foundation_statement_id` and recomputed root fingerprint are the ones the registry entry of the system domain declares (`verifier-toolkit/1` §8.2). A package that carried it would add a second source for material the verifier must pin independently; the member set of §9.4 therefore excludes it.

---

## 10. Original material and complete verification

Verification against original material remains a separate verification plane from package integrity.

The `verification_package` MUST NOT include original material by default.

The verifier MUST provide original material independently whenever the applicable verification path requires:

- validation of subject binding
- validation of issuer-declared properties against original material
- complete verification under public rules

For `Independent`, a valid package MAY establish that the certificate reached `Independent` under public rules while original-material-dependent checks remain a separate verifier responsibility.

Therefore:

- package sufficiency for `Independent` MUST NOT be interpreted as proof that issuer assertions are true
- package sufficiency for `Independent` MUST NOT be interpreted as proof that declared properties reflect actual material properties
- complete verification MAY still fail against original material even when the package is structurally valid and the independence result is valid
- no package-based `Independent` result MAY be presented as if it also established institutional trust, governance endorsement, or validation against original material when that deeper verification plane was not performed

---

## 11. Collection subjects carry their own leaves

A `subject.collection/1` subject declares its leaves INSIDE the certificate subject
that commits to it (`subject.collection/1` §7.4): each leaf's profile and commitment
travel in the signed `collection.leaves` array.

A `verification_package` therefore carries NOTHING extra for collection subjects. The
signed certificate is already sufficient for element-level inclusion
(`verifier-toolkit/1` §8.4.2), and a package MUST NOT introduce a parallel copy of
that data — two sources for one fact is a divergence waiting to happen.

Leaf VALUES remain original material and MUST NOT be included by default (§10, §18).
Only their commitments travel, and they travel signed.

---

## 12. Offline sufficiency requirement

A conforming `verification_package` MUST be sufficient to perform its claimed verification target offline.

Offline sufficiency means the verifier MUST NOT require:

- a live CERTCRYPT API
- a CERTCRYPT-managed resolver
- issuer-controlled live infrastructure
- a managed storage dependency
- discretionary assistance from any authority

Offline sufficiency for `Independent` does **not** mean the verifier never needs original material for deeper or complete verification.

It means the verification artifacts required to establish `Issued` or `Independent` under the system's own semantics MUST already be present in the package, without requiring live authority access.

For `Independent`, offline sufficiency MUST include the minimal independent verification set required by Section 9.2.1.

Offline sufficiency is relative to the applicable public rules, which the verifier holds independently of any package: the rules text, and the `system-foundation/1` statement of the system domain with the identifier and root fingerprint its registry entry declares (§9.5). A package never needs to carry them, and never does.

If a verifier ecosystem, delivery model, or operational profile regularly drives verifiers to depend on managed retrieval, managed interpretation, resolver mediation, or hosted package opening merely because the offline path is too operationally burdensome, that condition SHOULD be treated as architectural degradation of the verification model rather than as neutral convenience.

The existence of this sufficiency rule MUST NOT be interpreted as requiring package-based verification in all cases.

Verification MAY still be performed from independently obtained artifacts, provided the same public rules and semantic requirements are satisfied.

---

## 13. Package integrity and coherence

All artifacts included in a `verification_package` MUST be mutually coherent.

In particular, where applicable:

- the `base_certificate` MUST correspond to the certificate being verified
- the `independence_proof` MUST correspond to the same certificate or leaf context
- any rules-domain-dependent material MUST correspond to the same exact rules domain required by the contained `independence_proof`
- any `subtree_root`-relevant material MUST correspond to the same exact leaf claimed by the proof
- any settlement-derived material MUST correspond to the same independence result
- any `inclusion_proof` MUST correspond to the same settlement context and leaf commitment
- any aggregated-settlement bookkeeping material MUST correspond to the same exact settlement container, membership interpretation, ordering semantics, and positional semantics required by the proof

If any rules-domain-dependent materials correspond to different, only heuristically compatible, successor, fallback, or parser-selected rule domains, verification MUST fail.

If the package contains artifacts that can be interpreted as belonging to different leaves, different independence results, different settlement contexts, or different system domains, verification MUST fail.

The package's own declarations are bound to its artifacts. `verification_context.system_id` and `verification_context.rules_version` MUST equal the `system_id` and `rules_version` of the certificate's signed payload and, when an `independence_proof` is present, those of the proof; `settlement_reference`, when present, MUST equal the proof's `settlement_ref`. A package whose declaration contradicts an artifact it carries admits two readings and is rejected as ambiguous (§22.5): a conforming verifier returns `REJECTED` (`verifier-toolkit/1` §9.7, `PACKAGE_CONTEXT_COHERENT`).

This includes, without limitation, any package in which:

- the `base_certificate` is valid on its own
- the contained `independence_proof` is valid on its own
- supporting proof material is valid on its own

but those artifacts do not resolve to the same exact canonical `leaf / rules / system / settlement` context required for one exact independence result.

If the package contains artifacts that are individually valid but jointly permit more than one plausible aggregated-settlement interpretation, verification MUST fail.

This anti-splicing rule is mandatory.

---

## 14. Canonical semantics of `independence_proof`

For `Independent`, the package MUST treat `independence_proof` as the canonical independence artifact.

The package MUST NOT:

- redefine the semantics of `independence_proof`
- weaken its validation requirements
- replace it with a transport receipt or package-level status marker
- rescue an invalid proof by packaging convenience

If any conflict exists between package-level convenience and `independence_proof` semantics, the semantics of `independence_proof` SHALL prevail.

---

## 15. Verification procedure

### 15.1 `Issued`

For `Issued` verification, a conforming verifier MUST:

1. validate package structure
2. validate `base_certificate` integrity and authenticity
3. perform any required original-material comparison under the applicable rules

### 15.2 `Independent`

For `Independent` verification, a conforming verifier MUST:

1. validate package structure
2. validate package coherence and anti-splicing conditions
3. validate `Issued` verification of the `base_certificate`
4. validate `independence_proof` according to its normative semantics
5. validate any additional supporting proof material required by that proof and the applicable public rules

The verifier MUST reject the package if any required validation step is unknown, unsupported, omitted, or only partially completed.

The verifier MUST NOT substitute:

- package readability for proof validity
- signature presence for semantic completeness
- transport success for independence verification
- parser fallback for exact version support
- heuristic compatibility for exact rules-domain evaluation

The verifier MUST reject the package if supporting proof material depends on a different rules domain than the one fixed by the contained `independence_proof`.

The verifier MUST also reject the package if a valid `base_certificate` is paired with an `independence_proof`, settlement-derived material, inclusion material, or other supporting proof material that would be valid only for a different leaf, a different independence result, a different settlement context, or a different exact CERTCRYPT system/rules context.

When aggregated settlement semantics apply, the verifier MUST also reject the package if the included receipt material, inclusion material, root material, ordering material, or positional material is insufficient to establish one exact leaf-assignment interpretation for the claimed independence result.

The verifier MUST also reject the package if any aggregated receipt, inclusion path, root value, positional claim, or bookkeeping artifact could be validly re-used across another plausible settlement container or another plausible leaf target under the applicable public rules.

For the standard offline verification path, the package MUST contain canonical material sufficient to validate:

- settlement-context binding
- sufficient finality under the applicable rules domain
- settlement-bound capacity consumption
- aggregated inclusion and bookkeeping semantics when applicable

That sufficiency MUST hold without requiring direct live validation of raw burn events, live balances, token supply state, or equivalent external economic state.

If the verifier also selects a deeper or complete verification path, the verifier MAY additionally perform verification against original material under the applicable public rules.

Such deeper verification MAY include direct inspection of settlement substrate, burn lineage, balances, or equivalent economic context, but that is a separate audit plane and MUST NOT be treated as a prerequisite for conforming standard `Independent` verification.

Returning a successful `Independent` result from package verification MUST NOT be interpreted as semantic endorsement by CERTCRYPT.

It means only that the verifier was able to validate the relevant independence artifacts offline under public rules.

If the verifier cannot complete that exact validation path, it MUST return a non-success result explicitly indicating incompleteness, incompatibility, or rejection.

Implementations MAY expose diagnostic, preview, demo, exploratory, or partial verification modes for operational purposes, but those modes MUST NOT be presented as conforming `Independent` verification results.

### 15.2.1 Minimal package for `Independent`

Under the active aggregated settlement architecture, the minimal package for `Independent` verification on the zero-data path is the object below. Each member is required (§9.4) except `settlement_reference`, which is shown because producers commonly include it; the order shown is the causal order of validation — authorized-and-consumed capacity first, then the settlement that anchors it — and carries no meaning, since member order in a JSON object is not significant.

```json
{
  "base_certificate": { "...": "the CCSP/1 certificate" },
  "independence_proof": { "...": "independence.proof/1" },
  "verification_context": {
    "rules_version": "<rules_version>",
    "system_id": "<system_id>"
  },
  "capacity_evidence": { "...": "capacity.evidence/1 of the certificate's commitment" },
  "commitment_inclusion_proof": {
    "commitment_id": "<64 hex>",
    "commitment_leaf_hash": "<64 hex>",
    "commitment_index": "0",
    "commitment_siblings": ["<64 hex>"],
    "subtree_size": "2"
  },
  "settlement_material": { "...": "settlement-material/1 under the selected profile" },
  "settlement_reference": "<the proof's settlement_ref>"
}
```

Together with the applicable public rules (§12), this is sufficient for a conforming verifier to reach `INDEPENDENT_VALID`: the capacity evidence recomputes to the `commitment_id` and binds the certificate (`SHA3-256(JCS(base_certificate))` equals its `certificate_commitment_digest`), the inclusion path binds that commitment into the proof's `subtree_root`, and the settlement material resolves the proof's `settlement_ref` to the settlement root, its finality and the consumed capacity. A package missing any of the required members cannot reach `INDEPENDENT_VALID`; a conforming verifier returns `INCOMPLETE`.

## 16. Non-authority clause

A `verification_package` MUST NOT be interpreted as proving:

- factual truth of the certified event
- semantic truth of issuer assertions
- legal validity by itself
- institutional endorsement by CERTCRYPT

The package enables reproducible verification under public rules.

It does not transform issuer declarations into facts.

---

## 17. Failure conditions

Verification MUST fail if any required condition fails, including at least:

- package structure is malformed
- required artifacts are missing
- artifact bindings are inconsistent
- artifacts are ambiguously serialized
- `base_certificate` validation fails
- `independence_proof` validation fails
- required supporting proof material is missing or invalid
- anti-splicing checks fail
- the claimed verification target cannot be established deterministically
- a required model version is unsupported
- a fallback or compatibility interpretation would be required to continue
- any required check is skipped, downgraded, or left inconclusive while still attempting to return success

No partial success state MAY be substituted for a failed required condition.

---

## 18. Privacy and data minimization

A `verification_package` SHOULD minimize disclosure beyond what is strictly required for verification.

It MUST NOT include:

- original material by default
- unnecessary sensitive data
- unrelated leaf data
- unrelated settlement data

The package MAY be publicly distributable only to the extent permitted by the included artifacts and the verifier's operational context.

Zero-data system design MUST be preserved at the CERTCRYPT layer even when verifiers later compare against independently supplied original material.

---

## 19. Managed delivery and storage

Managed delivery, caching, or retrieval interfaces MAY expose `verification_package` copies.

Such interfaces:

- MUST be optional
- MUST be non-authoritative
- MUST NOT be required for package existence
- MUST NOT be required for verification
- MUST NOT change the verification result by serving inconsistent copies

Any managed copy MUST remain subordinate to the package semantics defined by this specification and to the semantics of the artifacts it contains.

---

## 20. Interoperability

Any conforming implementation MUST be able to verify a package using only:

- the package contents
- original material when the selected verification path requires it
- the applicable public rules

No proprietary logic, private API dependency, or CERTCRYPT-exclusive live service MAY be required.

Different serializations MAY exist, but they MUST preserve equivalent package semantics and MUST NOT introduce parser-dependent validation results.

---

## 21. Summary

The `verification_package` is a standardized offline verification package for CERTCRYPT certificate evaluation.

It supports `Issued` and `Independent` verification without requiring CERTCRYPT or issuer availability as live authorities.

For `Independent`, it packages `independence_proof` and any required supporting proof material so a verifier can evaluate Proof of Independence under public rules.

It does not prove truth.

It enables independent evaluation under public rules.

---

## 22. Serialization formats

Serialization is a portable representation of the `verification_package`.

It MUST NOT redefine package semantics.

It MUST NOT be required for verification if the relevant artifacts are already independently available under the same public rules.

It exists only for transport, storage, and interoperability.

A serialized `verification_package` MUST NOT be interpreted as producing, finalizing, or declaring independence.

Independence is defined exclusively by the underlying `independence_proof` and the applicable public rules.

### 22.1 JSON format

A `verification_package` is serialized as one JSON object: the member set of §9.4, each member holding the artifact in its own JSON form. That object is the package; there is no envelope around it.

The object carries no member naming its version or a verification target. The member set is closed, so a package of any later version, which MUST add a top-level `version` member, is rejected by a `/1` verifier rather than misread. The verification target is chosen by the verifier, not declared by the package: a package that carries an `independence_proof` and its supporting material can be verified as `Issued` or as `Independent`; a package without them can be verified only as `Issued`.

The JSON format is a transport representation only. It MUST NOT alter package meaning, proof meaning, or verification outcome.

### 22.2 Archive format

A `verification_package` MAY be transported as a ZIP archive that holds it member by member. The archive holds, at its root, one file per present member, named after the member: `base_certificate.json`, `verification_context.json`, `independence_proof.json`, `capacity_evidence.json`, `commitment_inclusion_proof.json`, `settlement_material.json`, and `settlement_reference.json` (a JSON string). Each file holds that member's JSON value, UTF-8 encoded.

A member is identified by its file name and by nothing else: a reader MUST NOT classify a file by inspecting its content. The archive MUST NOT contain a directory, a file with any other name, two entries with the same name, or a file that is not strict JSON; a reader that meets any of these rejects the archive. The package read from an archive is the JSON object of §22.1 whose members are the files' values, and it is verified as such.

A transport that delivers, beside a package archive, files that are not package members — for example the verifier's own original material — is not a package (§10). A reader of such a transport MUST still identify every entry by its exact path and never by its content.

### 22.3 Deterministic serialization rules

For any supported serialization format:

- the same logical package input MUST produce the same structural representation under the same serialization profile
- member ordering MUST be stable
- parsing MUST be deterministic
- duplicate keys in JSON objects MUST be rejected
- ambiguous field interpretation MUST be rejected
- multiple structurally valid but semantically conflicting interpretations of the same serialized package MUST be rejected

Serialization profiles MAY differ across implementations only if they preserve equivalent package semantics and identical verification outcomes.

### 22.4 Optional integrity material

A serialization MAY include:

- `package_digest`
- `signature`

When present, `package_digest` MUST be interpreted as an integrity feature over the package, and MUST be `SHA3-256(JCS(package))`, as 64 lowercase hexadecimal characters: SHA3-256 over the RFC 8785 canonical form of the JSON object of §22.1 — for an archive, of the object read from it. Neither digest nor signature is a member of the package object; they travel beside it.

When present, `signature` MUST be interpreted as an optional authenticity or delivery-integrity feature over the serialized representation.

Neither `package_digest` nor `signature`:

- defines independence
- defines truth
- rescues an invalid `independence_proof`
- rescues an invalid package

### 22.5 Anti-splicing requirements for serialization parsers

A conforming parser MUST reject serialized packages that can be interpreted as:

- mixing artifacts from different leaves
- mixing artifacts from different settlement contexts
- mixing artifacts from different system domains
- yielding multiple plausible package interpretations under the same declared format
- yielding multiple plausible aggregated-settlement bookkeeping interpretations for the same declared proof target

If a serialized package permits more than one plausible artifact mapping, more than one plausible verification target, or more than one plausible leaf/proof context, parsing MUST fail.

Serialized packages containing receipt material, settlement-root material, or inclusion material that is valid in isolation but ambiguous in joint aggregated interpretation MUST also be rejected.

A parser MUST treat any ambiguity as a validation failure, not as a recoverable condition.

### 22.6 Offline sufficiency of serialized packages

When a serialized package claims a verification target, it MUST contain all package artifacts required for that target under this specification.

The serialized package MUST NOT depend on:

- live APIs
- managed resolvers
- transport callbacks
- remote artifact discovery as a required verification step

Serialization remains OPTIONAL.

Verification MAY still be performed from independently obtained artifacts under the same public rules and semantic requirements.

### 22.7 Interoperability across formats

JSON Inline Format and Archive Format MUST yield the same verification result when they represent the same logical package.

No conforming implementation MAY introduce:

- parser-dependent verification results
- format-dependent package semantics
- semantics that exist only in JSON and not in ZIP
- semantics that exist only in ZIP and not in JSON

Format choice affects portability only.

It MUST NOT affect package meaning or verification outcome.

---

## 23. Versioning & extensibility

This `/1` specification defines the current active public contract for `verification-package/1`.

Once frozen, this version MUST NOT be modified in place in any way, including editorial, typographic or clarifying changes that would leave its normative meaning unchanged. Any change MUST be published under a new version identifier.

---

## 24. References

- CERTCRYPT Specifications
    - [security-model/1 — CERTCRYPT Security Model](../../../../foundation/security-model/1/index.md)
    - [system-domain/1 — CERTCRYPT System Domain](../../../../foundation/system-domain/1/index.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../../../foundation/rules-domain/1/index.md)
    - [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../../../protocols/CCCP/1/index.md)
    - [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../../../protocols/CCSP/1/index.md)
        - [independence.proof/1 — CERTCRYPT Independence Proof](../../../../models/independence.proof/1/index.md)
    - [capacity.evidence/1 — CERTCRYPT Capacity Evidence](../../../settlement/capacity.evidence/1/index.md)
    - [capacity.holder-authorization/1 — CERTCRYPT Capacity Holder Authorization](../../../settlement/capacity.holder-authorization/1/index.md)
    - [settlement.binding/1 — CERTCRYPT Aggregated Settlement Binding](../../../settlement/settlement.binding/1/index.md)
    - [settlement-material/1 — CERTCRYPT Settlement Material](../../../settlement/settlement-material/1/index.md)
    - [subject.collection/1 — CERTCRYPT Collection Subject Canonicalization Profile](../../../../profiles/subject.collection/1/index.md)
    - [system-foundation/1 — CERTCRYPT System Foundation](../../../../foundation/system-foundation/1/index.md)
    - [verifier-toolkit/1 — CERTCRYPT Verifier Toolkit](../../verifier-toolkit/1/index.md)
    - [capacity.commitment/1 — CERTCRYPT Capacity Commitment Specification](../../../settlement/capacity.commitment/1/index.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)

---

**End of verification-package/1**
