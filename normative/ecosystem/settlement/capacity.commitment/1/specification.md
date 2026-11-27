# CERTCRYPT Capacity Commitment Specification (capacity.commitment/1)

**Identifier:** `capacity.commitment/1`  

**Label:** CERTCRYPT Capacity Commitment Specification (capacity.commitment/1)  

**Type:** Ecosystem Specification

**Status:** Frozen

**Layer:** Layer 3 — Ecosystem

**Depends on:** See References *(active normative dependencies are listed below)*  

**Naming convention:**  
`capacity.commitment/1` is the formal identifier.  
CERTCRYPT Capacity Commitment Specification (capacity.commitment/1) is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.  

**Audience:** Implementers, verifiers, ecosystem integrators, auditors  

**Purpose:** Define the normative semantics, constraints, and interpretation boundary of capacity.commitment/1 within the active CERTCRYPT public architecture.  

**Intended use:** capacity.commitment/1 is intended to be the authoritative public specification used by conforming implementers, verifiers, auditors, and ecosystem tooling when handling this artifact or behavior.  

**Scope:** Defines the active normative behavior of capacity.commitment/1; adjacent protocols, profiles, operational tooling, and product behavior remain out of scope except where explicitly referenced.  

**Non-goals:** capacity.commitment/1 does not prove truth, semantic validity, legal validity, or live service authority by itself, and MUST NOT be interpreted as a substitute for cryptographic authenticity, Proof of Independence, or managed-service behavior outside its own normative scope.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale
This specification defines the canonical authorization model for `capacity_commitment` within CERTCRYPT.

A `capacity_commitment` is the artifact by which CERTCRYPT capacity becomes applicable to fixation under public rules.

This document defines:

- what a `capacity_commitment` is
- what it MUST bind to
- what it authorizes
- what it MUST NOT be interpreted as proving
- how conforming implementations validate applicability, sufficiency, and scope
- how authorization remains distinct from actual consumption

This document does **not** define:

- certificate issuance semantics
- submission-set transport
- settlement execution choreography
- the canonical semantics of `independence_proof`
- complete verification against original material

Those concerns belong to separate specifications.

---

## 2. Scope

This specification applies to all systems, implementations, SDKs, issuer-side nodes, settlement adapters, operational layers, and verifiers that:

- generate
- serialize
- transmit
- validate
- inspect
- apply

`capacity_commitment` material claiming conformity with CERTCRYPT.

Any implementation that uses `capacity_commitment` as authorization material for CERTCRYPT fixation MUST conform to this specification.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

---

## 4. Design principles

`capacity.commitment/1` is designed around the following principles:

- **Authorization, not consumption:** A `capacity_commitment` authorizes applicability under public rules. It does not prove settlement, consumption, or `Independent`.
- **Deterministic applicability:** Validity, scope, and authorization lineage MUST be mechanically checkable under one exact rules domain and system domain.
- **Attributed lineage:** Commitment meaning depends on auditable lineage and exact attribution, not on generic balance visibility, wallet state, or service-credit metaphors.
- **Institutional independence:** Authorization validity MUST remain verifiable from public artifacts and rules without requiring live CERTCRYPT infrastructure.
- **Interpretation boundaries:** A `capacity_commitment` MUST NOT be presented as semantic endorsement, proof of truth, or a substitute for settlement and Proof of Independence.

---

## 5. Normative role

For any valid positive independence result, capacity consumption MUST be attributable to valid CERTCRYPT capacity under the applicable public rules.

`capacity_commitment` defines the pre-settlement authorization material that can make such consumption validly possible.

It does not by itself establish that the authorized capacity was consumed.

No local state, API response, dashboard, or operational convenience layer SHALL be treated as a substitute for the commitment semantics defined here.

Managed capacity views MAY expose operational status, but they MUST NOT collapse domain attribution, authorization lineage, or later settlement consumption into a generic “balance available” semantics.

Implementations MUST NOT treat node-local caches, retry-state accounting, optimistic reservation views, or equivalent operational estimates as “nearly valid” authorization merely because they usually converge to the referenced authorization lineage.

---

## 6. Definitions

For the purposes of this specification:

- **capacity commitment** means the canonical authorization artifact by which capacity becomes applicable under public rules
- **authorized capacity** means the quantity or bounded allowance made available by that commitment
- **capacity scope** means the issuer, system, rules, operational, and any additional public-rule constraints under which the authorization may be used
- **capacity applicability** means that a valid commitment can lawfully authorize the submitted fixation request under the applicable public rules
- **capacity sufficiency** means that the authorized capacity is enough for the requested fixation under the applicable public rules
- **capacity consumption** means the capacity amount actually fixed as consumed through valid settlement

---

## 7. Rules domain

For the purposes of this specification, the **rules domain** means the exact versioned public ruleset governing:

- authorization semantics
- quantity semantics
- scope constraints
- applicability checks
- sufficiency checks
- the relationship between authorization and settlement consumption

The applicable rules domain MUST be explicitly present in the commitment or deterministically derivable from commitment material under public rules.

It MUST NOT be inferred heuristically from implementation defaults, transport context, local configuration, or fallback parser behavior.

---

## 8. Capacity commitment semantics

A valid `capacity_commitment` MUST authorize all of the following, as applicable under the relevant public rules:

- one exact CERTCRYPT System Domain
- one exact rules domain
- one issuer scope or equivalent authorization scope
- one bounded capacity allowance or bounded capacity applicability set
- one valid authorization window or equivalent validity condition set

A `capacity_commitment` MUST NOT authorize use outside those constraints.

It MUST NOT be interpreted as transferable or reusable beyond the exact scope defined under public rules.

The commitment semantics MUST make clear whether the authorized capacity represents:

- fungible quantity
- scope-bound allowance
- reservation-like applicability
- lock-equivalent applicability
- or another explicitly defined bounded authorization mode

Implementations MUST NOT treat these authorization meanings as interchangeable unless equivalence is explicitly defined by the applicable public rules.

### 8.1 Authorization lineage

A valid `capacity_commitment` MUST belong to an auditable capacity lineage under public rules.

That lineage MUST be:

- directly derived from auditable capacity issuance or top-up material
- or cryptographically linked to such material through a deterministic authorization chain

Under the active architecture, the sources of auditable issuance lineage are those defined by the applicable public rules.

No implementation MAY infer valid lineage merely from hosted balances, dashboard views, or operational estimates that are not attributable under public rules.

The lineage MUST remain attributable to:

- one exact CERTCRYPT System Domain
- one exact rules domain
- the relevant authorization scope
- the applicable issuance or top-up policy context where required by public rules

A `capacity_commitment` MUST NOT be treated as a floating authorization artifact disconnected from auditable issuance or top-up lineage.

That auditable lineage is part of what distinguishes CERTCRYPT capacity from a generic prepaid service model: validity depends on attributable authorization lineage under the CERTCRYPT System Domain, not merely on the operational existence of spendable units.

### 8.2 The signed commitment: the zero-data projection

This specification defines the commitment **model**: what a commitment authorizes and how it is validated. Its wire form is the `projected_commitment` of [capacity.evidence/1](../../capacity.evidence/1/specification.md) §6, and no other form is signed or transmitted. The holder signs exactly that object, with a non-reused per-operation leaf key, and nothing else.

The projection is designed to be unlinkable:

- the holder, pool and authorization are named only by **operation-scoped pseudonyms** ([CCCP/1 §7.4](../../../../protocols/CCCP/1/index.md); domain tags `holder`, `pool`, `authorization`), never by stable identifiers;
- the signing key is a **per-operation leaf key**, disclosed with a membership proof to the authorized `holder_key_set_root` ([holder-keyset.merkle-sha3-256/1](../../../../protocols/commitment/holder-keyset.merkle-sha3-256/1/index.md)), never a stable holder key;
- it carries no original material and no stable identifier in clear.

The cryptographic checks are not weakened: the same exact `(system_id, rules_version, system_root_fingerprint)` coherence holds, and the holder signature is re-verified for real against the disclosed leaf key. It establishes authorization to consume, not consumption (§9). §15 maps each logical field of §14 to where the projection carries it.

---

## 9. Separation between authorization and consumption

The architectural boundary in `/1` is strict:

- `capacity_commitment` authorizes possible use
- `submission-set` validates applicability and sufficiency
- settlement fixes actual consumption
- `independence_proof` proves that valid consumption occurred in the path to `Independent`

No implementation MAY treat a valid `capacity_commitment`, or a reference to it, as sufficient evidence that capacity was consumed.

No implementation MAY treat `capacity_authorization_ref` as equivalent to settlement-bound consumption evidence in `independence_proof`.

`capacity_authorization_ref` concerns authorization for execution.

Settlement-bound consumption evidence in `independence_proof` concerns proof-path evidence that valid CERTCRYPT capacity was consumed through settlement.

---

## 10. Required bindings

A valid `capacity_commitment` MUST be bound to at least:

- `commitment_version`
- `system_id`
- `rules_version`
- `issuer_scope` or equivalent authorization scope identifier
- the authorized capacity quantity or equivalent bounded authorization semantics
- validity conditions or equivalent authorization constraints

If any required binding is missing, ambiguous, or parser-dependent, the commitment MUST be rejected.

The commitment MUST NOT permit valid interpretation outside its exact system and rules domain.

---

## 11. Scope and non-transferability

A valid `capacity_commitment` MUST define the scope within which it may be used.

That scope MAY include, as required by the applicable public rules:

- issuer scope
- operational scope
- node scope
- temporal validity window
- quantity bounds
- settlement profile compatibility

Capacity authorized for one scope MUST NOT be accepted as valid for another unrelated scope.

Any attempt to reuse, transplant, or reinterpret a commitment across unrelated scopes MUST be rejected.

Any delegated operational scope, node scope, or equivalent actor-specific applicability permitted by public rules MUST be explicit and MUST NOT broaden the `issuer_scope`, system domain, or rules domain bound into the commitment.

The commitment MUST resolve to exactly one valid authorization interpretation for one exact issuer namespace within one exact CERTCRYPT System Domain.

### 11.1 Expiry, release, and stranded commitments

Under `/1`, a valid `capacity_commitment` MAY:

- expire without any consumption having occurred
- become partially or wholly unusable because its validity conditions are no longer satisfied
- require release, regularization, or equivalent public-rule handling before the underlying authorized capacity becomes reusable

Such outcomes MUST NOT be interpreted as:

- settlement
- consumption
- proof that a leaf reached `Independent`
- a permanent right immune to later public-rule constraints

If the applicable public rules define release, expiry, replenishment, or stranded-commitment handling, those rules MUST be deterministic and publicly evaluable.

Implementations MUST NOT silently convert expired, stranded, or released authorization state into evidence of consumption.

### 11.2 Temporal conditions

A commitment carries `issued_at` and `expires_at`, RFC 3339 UTC with whole seconds. Under the zero-data profile:

- `issued_at` MUST fall within the authorization's window, `valid_from <= issued_at <= valid_until`, inclusive at both ends ([capacity.evidence/1](../../capacity.evidence/1/specification.md) §8, offline);
- `expires_at` MUST equal `issued_at` plus the capacity-commitment TTL the rules domain declares; it is not required to fall inside the authorization's window ([capacity.holder-authorization/1](../../capacity.holder-authorization/1/specification.md) §5.3);
- when a submission set consumes the commitment, the fixation service MUST refuse it unless `closure_time <= expires_at` ([submission-set/1](../../../../protocols/settlement/submission-set/1/specification.md)) and its own receipt of the submission is not after `expires_at`. These are admission checks of the fixation service; the receipt time is operational state and is not part of any proof;
- offline, the settlement MUST satisfy `block_timestamp <= expires_at` ([settlement.binding/1](../../settlement.binding/1/specification.md) §9). That is the only temporal condition an offline verifier evaluates against `expires_at`, and its time comes from the substrate, never from the issuing system.

---

## 12. Applicability and sufficiency

To be validly used in a fixation path, a `capacity_commitment` MUST be:

- valid under the applicable rules domain
- attributable to the correct system domain
- applicable to the submitted canonical leaf identity
- sufficient for the required capacity under the same public rules

Applicability and sufficiency MUST be determined mechanically.

No hidden, discretionary, or proprietary logic MAY be required.

---

## 13. Deterministic quantity semantics

The public rules governing capacity quantity MUST be deterministic.

Given the same canonical leaf identity, the same exact rules domain, and the same declared economically relevant assertion set, conforming implementations MUST derive the same capacity requirement.

That leaf-level determinism MUST remain orthogonal to subject-level declaration models.

In particular:

- leaf aggregation MUST NOT, by itself, imply subject-level cardinality
- one leaf MUST NOT be treated as equivalent to one collection subject merely because it aggregates multiple certified subjects
- subject-level structures such as `subject.collection/1` MUST remain governed by their own declared and committed fields
- where quantity rules rely on subject-level structure, they MUST do so through declared economically relevant assertions bound under the applicable subject and leaf rules, not through ad hoc inference from leaf packaging alone

### 13.1 Effective declared units

Where the applicable public rules derive capacity quantity from subject-level declared units, those rules MUST define one exact deterministic subject-to-unit mapping.

Under the current `/1` quantity model:

- a subject governed by `subject.collection/1` MUST contribute exactly its declared `declared_cardinality` as effective declared units
- any other subject MUST contribute exactly `1` effective declared unit unless another applicable public specification explicitly defines a different recognized subject-level unit model

Where such declared units are used for capacity, pricing, admissibility, or other deterministic economic consequences under the applicable public rules, that use MUST be interpreted as rule application to a bound issuer declaration, not as semantic validation of the underlying original material by CERTCRYPT.

That default contribution of `1` effective declared unit for non-collection subjects applies even where the subject itself does not carry an explicit `declared_cardinality` field.

Conforming implementations MUST derive that default subject-level quantity from the applicable public rules, not by requiring a redundant cardinality field in non-collection subject profiles.

The effective declared units of a leaf MUST equal the sum of the effective declared units of all certified subjects bound into that exact closed leaf under the applicable public rules.

Accordingly, mechanically packaging multiple hidden items inside one opaque non-collection subject MUST NOT, by itself, increase effective declared units.

Where complete verification later shows that an issuer-declared economically relevant quantity was materially unsustainable under the applicable public rules and original material, that later outcome MUST be interpreted as failure of the issuer declaration under those rules, not as evidence that CERTCRYPT had previously validated its truth.

Such later outcomes MUST NOT retroactively alter the deterministic capacity application that occurred under the committed economically relevant declaration set and the exact public rules applied at that time.

#### 13.1.1 Verifier enforcement of the effective-declared-units equality

The equality in §13.1 — that the effective declared units of a leaf MUST equal the sum of the effective declared units of all certified subjects bound into that leaf — is a normative binding, not merely a construction rule for the issuer.

A conforming Independent-path verifier MUST enforce it. Concretely, the verifier MUST recompute the sum of per-subject effective declared units over the certified subjects of the base certificate under verification — a `subject.collection/1` subject contributing exactly its `declared_cardinality`, any other subject contributing exactly `1` (§13.1) — and MUST require that sum to equal the issuer-declared `declared_effective_units` carried in the bound capacity evidence (`capacity.evidence/1`, `submission-set/1 §13.2`).

This enforcement is the sole point in the system that holds both operands: under the zero-data profile the settlement plane carries evidence digests, not the base certificate or its subjects (`submission-set/1 §8.1`), so no issuing-time or settlement-time actor can recount the certified subjects. The offline verifier — which holds both the base certificate anchor and the capacity evidence — is therefore the normative enforcement point.

If the recomputed sum does not equal `declared_effective_units`, the verifier MUST fail closed with a negative Independent outcome (`INDEPENDENT_INVALID`) under the check identity `EFFECTIVE_UNITS_BINDING_VALID`. A cryptographically well-formed certificate whose declared units understate the certified subjects (for example, `N` certified subjects declared as `1` to be priced as one) MUST NOT verify.

Where a `subject.collection/1` subject is present but its `declared_cardinality` is not resolvable to the verifier offline (the certificate subject carries no signed collection descriptor, `subject.collection/1` §7, and no original material supplies one, §8.5 of `verifier-toolkit/1`), the verifier cannot recompute the exact sum. In that case it MUST still enforce the lower bound implied by the certified-subject count (each subject contributes at least `1`) and fail closed under `EFFECTIVE_UNITS_BINDING_VALID` if `declared_effective_units` is below that lower bound; exact-equality enforcement over collection cardinality is then deferred to the run in which original material is supplied. The all-non-collection case is always exactly computable and MUST always be enforced as strict equality.

### 13.2 Secondary canonical-byte guardrails

The applicable public rules MAY additionally define deterministic byte-based quantity guardrails, thresholds, or surcharges derived from canonical subject size.

Where such guardrails exist:

- they MUST be derived from `canonical_bytes(subject)` or from deterministic sums thereof under the applicable public rules
- they MUST remain secondary to the primary effective-declared-unit model where that model is in force
- they MUST NOT permit leaf packaging alone to substitute for subject-level declared units
- they MUST NOT be described or implemented as semantic inspection of hidden content

Terms such as `payload size` or `document size` MUST NOT be used as substitutes for canonical-byte measurement where the applicable rules require canonical-byte measurement.

### 13.3 Deterministic admissibility limits

The applicable public rules MAY define deterministic admissibility limits, including:

- maximum effective declared units per leaf
- maximum `declared_cardinality` for one `subject.collection/1` subject
- maximum canonical byte size for one subject
- maximum total canonical byte size for one leaf

Such limits MAY vary by authorization scope, operation tier, or other exact public-rule applicability boundary.

If any such limit is exceeded, the applicable workflow MUST fail closed with an explicit non-positive outcome.

These limits are admissibility constraints and economic guardrails.

They MUST NOT be implemented as silent reinterpretation of declared quantity semantics.

This determinism applies to the committed economically relevant declaration set, not to an independently audited measurement of the original material.

Accordingly, deterministic quantity derivation MUST NOT be interpreted as proof that the issuer-declared economically relevant properties are materially true.

Compatible, equivalent, or successor rules MUST NOT be used as substitutes unless equivalence is explicitly defined under the applicable public rules.

The consumption semantics of a `capacity_commitment` (for example partial, atomic, bounded-use, or another explicitly defined model) MUST be defined by the applicable `authorization_mode` and rules domain.

Implementations MUST NOT assume partial consumption, reusable consumption, or balance-like behavior unless those semantics are explicitly allowed by the applicable public rules.

Where public rules define later economic reconciliation, regularization, or equivalent fairness controls for materially unsustainable declared values discovered during complete verification, those controls MUST remain distinct from the authorization semantics defined here.

Where the applicable rules domain relies on issuer-declared economically relevant properties for quantity derivation, those public rules SHOULD also define explicit later fairness consequences for materially unsustainable declarations, such as reconciliation, regularization, surcharge, debit, temporary restriction, or future authorization-eligibility adjustment.

Where the applicable rules domain is exposed to strategic issuer behavior, those public rules SHOULD also define explicit economic responses to systematic leaf fragmentation, opportunistic aggregation, or other mechanically valid but economically distortive packaging strategies that would otherwise arbitrage the intended pricing or fairness model.

Such responses MUST remain public-rule economic consequences and MUST NOT be implemented as hidden semantic reinterpretation of authorization or as ad hoc case-by-case discretion.

### 13.4 Minimum closure for public quantity and fairness rules

If an applicable public rules domain uses issuer-declared economically relevant properties to derive capacity quantity, pricing, admissibility, or later fairness consequences, that rules domain MUST define at least:

- one exact deterministic subject-to-unit mapping
- one exact rule for the default contribution of recognized non-collection subjects
- one exact rule for `subject.collection/1` quantity contribution
- one exact set of deterministic admissibility limits applicable to that rules domain, whether global or tier-scoped
- one exact declaration-binding model for any economically relevant assertion set required by `submission-set/1`
- one exact consequence model for materially unsustainable issuer declarations when later complete verification under public rules can expose them

If the applicable public rules domain uses leaf-level overhead, thresholds, step functions, or tier transitions that could make fragmentation or opportunistic aggregation economically distortive, that rules domain MUST also define explicit deterministic responses to those strategies.

Those responses MAY include:

- surcharge
- reconciliation
- debit
- temporary restriction
- future authorization-eligibility adjustment
- explicit admissibility rejection above defined thresholds

No conforming implementation MAY replace those public-rule consequences with hidden discretionary interpretation of submitted content.

---

## 14. Canonical logical fields

Every valid `capacity_commitment` MUST contain or deterministically imply the following logical fields. They describe the model; §15 fixes how the only wire form (§8.2) carries each of them.

### 14.1 `commitment_version`

Identifies the capacity-commitment model version.

### 14.2 `system_id`

Identifies the CERTCRYPT System Domain.

This field MUST resolve, directly or through public rules, to verifiable system-domain root material.

That attribution path MUST expose, directly or deterministically, one exact system-domain root identifier sufficient to distinguish the CERTCRYPT domain from cloned, forked, or merely similar systems.

#### 14.2.1 `system_root_fingerprint`

Identifies the exact system-domain root identifier used for attribution.

This field MUST be present.

It MUST match the exact system-domain root identifier required by the applicable public rules.

### 14.3 `rules_version`

Identifies the exact versioned public ruleset governing the commitment semantics.

This field MUST be present or deterministically derivable.

### 14.4 `commitment_id`

Identifies the exact commitment instance.

This field MUST be unique within the applicable system and rules domain as required by public rules.

### 14.5 `issuer_scope`

Identifies the issuer scope or equivalent authorization scope to which the commitment applies.

This field MUST resolve to one exact issuer namespace or equivalent authorization namespace under the applicable public rules.

### 14.6 `authorized_capacity`

Represents the quantity or bounded allowance authorized by the commitment.

The exact semantic kind of `authorized_capacity` MUST be defined by the applicable rules domain and `authorization_mode`.

It MUST NOT be treated as an untyped fungible quantity if the applicable rules distinguish among quantity, allowance, reservation, lock-equivalent authorization, or other bounded applicability models.

### 14.7 `validity_conditions`

Represents the validity window, constraints, or equivalent conditions under which the commitment remains applicable.

`validity_conditions` MUST be schema-governed under the applicable public rules.

It MUST NOT function as an open-ended catch-all field whose semantics depend on private implementation logic.

Two conforming implementations interpreting the same `validity_conditions` under the same rules domain MUST reach the same applicability result.

### 14.8 `authorization_mode`

Indicates the authorization mode if the applicable rules distinguish among commitment forms such as allocation, reservation, or lock-equivalent authorization.

### 14.9 `proof_material`

Represents the signature, proof, or equivalent verification material required to validate the commitment under public rules.

### 14.10 Canonical coherence requirement

All logical fields of a valid `capacity_commitment` MUST be mutually coherent.

In particular:

- `system_id`
- `rules_version`
- `commitment_id`
- `issuer_scope`
- `authorized_capacity`
- `validity_conditions`

MUST resolve to one and only one valid authorization interpretation for one exact system and one exact rules domain.

---

## 15. Wire mapping

Under the zero-data profile the logical fields of §14 are carried as follows. Nothing else is signed, and nothing in this table travels in clear unless the table says so.

| Logical field | Carried as |
|---|---|
| `commitment_version` | `projected_commitment.commitment_version` |
| `system_id`, `system_root_fingerprint`, `rules_version` | the same members of `projected_commitment`, equal to those of `projected_authorization` |
| `commitment_id` | the evidence digest of the `capacity.evidence/1` that carries the commitment (capacity.evidence/1 §7.1); the commitment has no other public identifier |
| `issuer_scope` | not carried: the holder, pool and authorization travel only as operation-scoped pseudonyms, and the scope is checked by the fixation service at submission (capacity.holder-authorization/1 §6) |
| `authorized_capacity` | `consumed_quantity` (the capacity the commitment consumes) and `declared_effective_units` (§13.1) |
| `validity_conditions` | `issued_at` and `expires_at` (§11.2) |
| `authorization_mode` | not carried: the zero-data profile defines one mode, a per-operation allocation consumed whole |
| `proof_material` | `commitment_signature_b64` (ML-DSA-65, by the leaf key) with `operation_key` and its membership proof |

---

## 16. Validation procedure

A conforming implementation validating a `capacity_commitment` MUST follow the following logical sequence. Under the zero-data profile the steps are split by who can perform them: §16.1–§16.4 and the authorization window of §16.5 are the offline steps of [capacity.evidence/1](../../capacity.evidence/1/specification.md) §8, performed by every verifier; scope (§16.5), sufficiency (§16.6) and lineage (§16.8) rest on records that do not travel and are evaluated by the fixation service when a submission set consumes the commitment ([submission-set/1](../../../../protocols/settlement/submission-set/1/specification.md)). An offline verifier MUST NOT report the latter as checked.

### 16.1 Validate commitment model version

The implementation MUST confirm that the commitment version is supported.

If unsupported, validation MUST fail deterministically.

The implementation MUST reject any attempt to interpret the commitment under a less strict, earlier, heuristically selected, or implementation-default model version.

### 16.2 Validate rules domain

The implementation MUST validate the commitment under the exact `rules_version` declared in, or deterministically bound into, the commitment.

If the applicable rules domain cannot be identified uniquely and deterministically, validation MUST fail.

### 16.3 Validate system attribution

The implementation MUST confirm that the commitment belongs to the CERTCRYPT domain using the configured system root or equivalent public verification material.

If attribution cannot be validated, the commitment MUST be rejected.

The implementation MUST validate that the attributed commitment resolves to one exact system-domain root identifier under the applicable public rules.

If the root identifier is ambiguous, missing when required, or inconsistent with the commitment context, validation MUST fail.

### 16.4 Validate commitment integrity

The implementation MUST validate that:

- all mandatory logical fields are present or deterministically derivable
- the proof material is structurally valid under the applicable rules
- the commitment has not been altered or ambiguously serialized

If integrity cannot be established, validation MUST fail.

### 16.5 Validate scope and validity conditions

The implementation MUST validate that:

- the issuer or authorization scope is the correct one for the attempted use
- the validity conditions are satisfied
- no scope escape or cross-domain reinterpretation is occurring
- no delegated or operational scope expansion is occurring beyond what is explicitly bound into the commitment
- the `validity_conditions` are interpretable under an exact public schema for the applicable rules domain

If scope validity cannot be established, the commitment MUST be rejected.

### 16.6 Validate applicability and sufficiency

When a commitment is used in a fixation path, the implementation MUST validate that:

- the commitment is applicable to the canonical leaf identity under the same rules domain
- the authorized capacity is sufficient under the public quantity rules
- the commitment does not need heuristic reinterpretation to appear sufficient
- the semantic kind of `authorized_capacity` is interpreted exactly as required by the applicable rules domain and `authorization_mode`
- no partial, reusable, balance-like, or equivalent consumption behavior is assumed unless explicitly allowed by the applicable public rules
- no manipulated local state, private accounting cache, wallet-like display, node-local synthetic balance, or equivalent operational surrogate is being treated as if it were normative authorization material
- no optimistic local estimate of apparent availability is being treated as sufficient authorization where the referenced authorization lineage would not itself support that interpretation under public rules

If applicability or sufficiency cannot be established, the commitment MUST be rejected for that use.

### 16.7 Reject consumption confusion

The implementation MUST reject any attempt to treat a commitment, or a reference to it, as proof that capacity was already consumed.

Consumption MUST be proven only through the relevant settlement path and the proof model that depends on that settlement.

### 16.8 Validate authorization lineage

The implementation MUST validate that the commitment belongs to an auditable issuance or top-up lineage under the applicable public rules.

If lineage to valid issuance or top-up material cannot be established deterministically, the commitment MUST be rejected.

Local operational availability state MAY assist scheduling or UX, but it MUST NOT be treated as a substitute for auditable authorization lineage or as an independent source of capacity truth.

---

## 17. Interaction with `submission-set`

`submission-set/1` validates whether a capacity commitment is applicable and sufficient for the requested fixation under the declared rules domain.

For that interaction:

- `capacity_authorization_ref` MUST refer to valid authorization material governed by this specification or an equivalent one under public rules
- the `rules_version` used to interpret the commitment MUST match the exact rules domain applied during fixation
- submission validation MUST fail if authorization material is valid only under a different rules domain, system domain, or issuer scope
- submission validation MUST fail if apparent authorization depends on local-only state that is not reproducible from the referenced authorization lineage under public rules

The submission layer MUST NOT treat commitment existence as proof that valid CERTCRYPT capacity was consumed.

---

## 18. Interaction with `independence_proof`

Under `independence.proof/1`, a verifier evaluates whether the presented artifacts establish that valid CERTCRYPT capacity was consumed through settlement in the path that led to `Independent`.

For that interaction:

- `capacity_commitment` MAY be part of the authorization lineage that made such consumption possible
- `capacity_commitment` MUST NOT be treated as the proof of consumption itself
- settlement-bound consumption evidence in `independence_proof` MUST remain distinct from pre-settlement authorization references unless public rules define a deterministic and inseparable bridge through settlement
- any such bridge MUST be fully defined by the selected `settlement_profile_id` and its settlement-material contract under public rules
- no implementation MAY rely on node-local reservation history, retry memory, managed accounting views, or other operational state as a substitute for that bridge

Any implementation that collapses authorization and consumption into one undifferentiated artifact is non-conformant.

---

## 19. Non-goals

A `capacity_commitment` MUST NOT be interpreted as proving any of the following:

- that a leaf already reached `Independent`
- that capacity was already consumed
- that settlement already occurred
- that the issuer's declarations are true
- that CERTCRYPT endorsed the content or semantics of the leaf

Implementations, user interfaces, and documentation MUST NOT describe `capacity_commitment` as if it proved any of the above.

---

## 20. Managed interfaces

CERTCRYPT MAY expose convenience interfaces for:

- issuing or retrieving authorization material
- operational inspection
- packaging or formatting

Such interfaces:

- MUST be non-authoritative with respect to consumption proof
- MUST be optional
- MUST NOT redefine commitment semantics
- MUST NOT replace settlement as the source of truth for actual consumption

Any managed copy of a `capacity_commitment` MUST be treated as an operational convenience layer only.

Managed availability, top-up status, or accounting views MUST NOT be treated as a substitute for the auditable authorization lineage required by this specification.

---

## 21. Failure semantics

Validation MUST fail if any required condition fails, including at least:

- unsupported commitment version
- ambiguous or parser-dependent serialization
- unattributable system domain
- unidentified or heuristic rules domain
- invalid proof material
- invalid scope or validity conditions
- insufficient or non-applicable authorized capacity
- untyped or ambiguously typed `authorized_capacity` semantics
- `validity_conditions` that are not schema-interpretable under the applicable public rules
- missing or invalid authorization lineage to auditable issuance or top-up material
- any attempt to reinterpret authorization as consumption proof

No partial success state MAY be substituted for a failed required condition.

---

## 22. Security properties

A conforming `capacity_commitment` model MUST preserve the following properties:

1. system-domain attribution
2. rules-domain attribution
3. scope integrity
4. quantity determinism
5. applicability determinism
6. non-transferability across unrelated scopes
7. auditable authorization lineage
8. deterministic expiry / release / stranded-state interpretation under public rules
9. rejection of authorization-as-consumption confusion
10. deterministic validation without heuristic rule selection
11. compatibility with offline verification of commitment validity under public rules

Any implementation that weakens any of these properties MUST be considered non-conformant.

---

## 23. Privacy and data-minimization

A `capacity_commitment` SHOULD minimize disclosure beyond what is strictly necessary for authorization validation.

It MUST NOT require inclusion of:

- original certified payload material
- semantic content of the certified subject
- internal CERTCRYPT operational databases as a source of truth

The model MUST remain compatible with the CERTCRYPT zero-data architecture.

---

## 24. Conformance

An implementation conforms to `capacity.commitment/1` if and only if:

- it preserves all mandatory semantics defined in this document
- it validates all required bindings deterministically
- it rejects invalid or ambiguous commitments deterministically
- it does not collapse authorization into settlement consumption
- it does not reinterpret operational convenience as ontological proof of use

Partial implementations MUST NOT claim full conformance.

---

## 25. Future evolution

Future versions of this model MAY:

- add new authorization materializations
- add new quantity schemas
- add new scope profiles
- refine the interface between authorization and settlement adapters

Future versions MUST NOT:

- collapse authorization into proof of consumption
- remove system-domain attribution
- remove rules-domain attribution
- permit heuristic selection of the governing rules domain
- permit ambiguous scope transfer across unrelated actors or domains

Any such change would require a non-compatible new model version.

---

## 26. Final normative statement

A valid `capacity_commitment` is the canonical authorization artifact by which CERTCRYPT capacity becomes applicable to fixation under one exact system domain, one exact rules domain, and one exact authorization scope, without itself proving that such capacity was consumed or that a leaf reached `Independent`.

---

## 27. Versioning & extensibility

This `/1` specification defines the current active public contract for `capacity.commitment/1`.

Once frozen, this version MUST NOT be modified in place in any way, including editorial, typographic or clarifying changes that would leave its normative meaning unchanged. Any change MUST be published under a new version identifier.

---

## 28. References

- CERTCRYPT Specifications
    - [security-model/1 — CERTCRYPT Security Model](../../../../foundation/security-model/1/index.md)
    - [system-domain/1 — CERTCRYPT System Domain](../../../../foundation/system-domain/1/index.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../../../foundation/rules-domain/1/index.md)
    - [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../../../protocols/CCCP/1/index.md)
    - [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../../../protocols/CCSP/1/index.md)
    - [CCVP/1 — CERTCRYPT Consistency Verification Protocol](../../../../protocols/CCVP/1/index.md)
    - [capacity.evidence/1 — CERTCRYPT Capacity Evidence](../../capacity.evidence/1/index.md)
    - [capacity.holder-authorization/1 — CERTCRYPT Capacity Holder Authorization Specification](../../capacity.holder-authorization/1/index.md)
    - [holder-keyset.merkle-sha3-256/1 — CERTCRYPT Holder Operation-Key Set Commitment Scheme](../../../../protocols/commitment/holder-keyset.merkle-sha3-256/1/index.md)
    - [independence.proof/1 — CERTCRYPT Independence Proof Model](../../../../models/independence.proof/1/index.md)
    - [settlement.binding/1 — CERTCRYPT Aggregated Settlement Binding](../../settlement.binding/1/index.md)
    - [subject.collection/1 — CERTCRYPT Collection Subject Canonicalization Profile](../../../../profiles/subject.collection/1/index.md)
    - [submission-set/1 — CERTCRYPT Submission Set Protocol](../../../../protocols/settlement/submission-set/1/index.md)
    - [verifier-toolkit/1 — CERTCRYPT Verifier Toolkit Specification](../../../verification/verifier-toolkit/1/index.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)

---

**End of capacity.commitment/1**
