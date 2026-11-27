# CERTCRYPT Independence Proof Model (independence.proof/1)

**Identifier:** `independence.proof/1`  

**Label:** CERTCRYPT Independence Proof Model (independence.proof/1)  

**Type:** Model Specification

**Status:** Frozen

**Layer:** Layer 2 — Models

**Depends on:** See References *(active normative dependencies are listed below)*  

**Naming convention:**  
`independence.proof/1` is the formal identifier.  
CERTCRYPT Independence Proof Model (independence.proof/1) is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.  

**Audience:** Implementers, verifiers, auditors  

**Purpose:** Define the normative semantics, constraints, and interpretation boundary of independence.proof/1 within the active CERTCRYPT public architecture.  

**Intended use:** independence.proof/1 is intended to be the authoritative public specification used by conforming implementers, verifiers, auditors, and ecosystem tooling when handling this artifact or behavior.  

**Scope:** Defines the active normative behavior of independence.proof/1; adjacent protocols, profiles, operational tooling, and product behavior remain out of scope except where explicitly referenced.  

**Non-goals:** independence.proof/1 does not prove truth, semantic validity, legal validity, or live service authority by itself, and MUST NOT be interpreted as a substitute for cryptographic authenticity, Proof of Independence, or managed-service behavior outside its own normative scope.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale
This specification defines the canonical model for `independence_proof` within CERTCRYPT.

Within CERTCRYPT, **Proof of Independence** is the structural property or result that holds when a leaf reaches `Independent` under the applicable public rules.

An `independence_proof` is the canonical verifiable artifact that represents that result.

This specification operates within the CERTCRYPT model of Proof of Independence.

This document defines:

- what an `independence_proof` is
- what it MUST bind to
- what it MUST prove
- what inputs are required for its validation
- what properties implementations MUST preserve

This document does **not** define:

- submission-set transport
- capacity issuance workflows
- settlement execution workflows
- the backend-specific shape of settlement proof material beyond the public contract fixed by the selected settlement profile
- optional managed retrieval interfaces

Those concerns belong to separate specifications.

---

## 2. Scope

This specification applies to all systems, implementations, SDKs, verifiers, services, and managed layers that:

- generate
- serialize
- transmit
- validate
- store
- inspect

an `independence_proof` claiming conformity with CERTCRYPT.

Any implementation that uses the term `independence_proof` in a CERTCRYPT context MUST conform to this specification.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

---

## 4. Design principles

`independence.proof/1` is designed around the following principles:

- **Structural proof, not truth:** An `independence_proof` carries the artifacts a verifier evaluates to establish Proof of Independence under public rules. It does not prove semantic truth, legal validity, or institutional endorsement.
- **Deterministic verification:** Given the same proof material, `subtree_root`, settlement context, and rules domain, conforming verifiers MUST converge on the same `Independent` result.
- **Proof without data custody:** Verification MUST rely on the proof artifact, applicable public rules, and verifier-available original material where required, not on retained platform data or internal CERTCRYPT systems.
- **Institutional independence:** A valid `independence_proof` MUST remain verifiable without dependence on continued issuer existence or live CERTCRYPT infrastructure.
- **Infrastructure neutrality:** The proof model MUST remain valid across publication layers, hosts, providers, and operational environments.
- **Interpretation boundaries:** An `independence_proof` proves that a closed leaf reached an independently verifiable structural state under public rules. It MUST NOT be interpreted as proof that the certified content is true.

---

## 5. Normative role

For any leaf that validly reaches state `Independent`, there MUST exist exactly one canonical independence result.

That canonical result MAY have multiple equivalent materializations or serializations, but those materializations MUST represent the same underlying result.

The `independence_proof` is the canonical artifact representing that result.

Proof of Independence is therefore the property or result under public rules.

`independence_proof` is the artifact by which that result is carried, transported, inspected, or verified.

No dashboard, API response, resolver output, or managed interface SHALL be treated as a substitute for `independence_proof`.

---

### 5.1 Rules domain

For the purposes of this specification, the **rules domain** means the exact versioned public ruleset governing:

- leaf validation
- issuance-time participation semantics
- settlement interpretation
- capacity semantics
- independence derivation

The applicable rules domain MUST be explicitly present in the proof or deterministically derivable from proof material under public rules.

It MUST NOT be inferred heuristically from implementation defaults, parser behavior, transport context, or deployment-specific assumptions.

Where the selected rules domain permits settlement-backed `Independent`, it MUST also determine one exact `settlement_profile_id` and one exact settlement-material contract for the claimed proof context.

---

## 6. Independence conditions

A leaf — the Merkle sub-tree of accepted commitments whose `subtree_root` is anchored and signed by the proof — SHALL be considered `Independent` if and only if all of the following conditions are satisfied:

1. the leaf is structurally valid under public rules
2. the leaf is closed and immutable for the purpose of independence evaluation
3. the leaf is bound to the relevant issuance-time commitments
4. a valid settlement event with sufficient finality exists
5. that same settlement event consumes valid CERTCRYPT capacity attributable to the relevant CERTCRYPT System Domain under the applicable public rules
6. the settlement event is non-replayed and uniquely attributable
7. the resulting independence state is derivable deterministically from public rules and required proofs

The leaf — not the `submission-set` — is the unit that is fixed. The `submission-set` is the transport container the node submits; it may contain commitments that are later rejected and it is never fixed as such. The leaf is the sub-tree of the accepted commitments, and its `subtree_root` is what settlement anchors and the proof signs. The verdict is then evaluated per individual base certificate carried in the leaf (§7.10).

An `independence_proof` MUST bind to all conditions necessary to validate those properties.

No independence state MAY be considered valid if it was not derived from a valid settlement event consuming valid CERTCRYPT capacity under the applicable public rules.

Capacity consumption is a required condition under the applicable public rules, not an independent source of independence semantics.

Under the CERTCRYPT economic model, satisfaction of that condition implies that `Independent` is not merely validated against capacity, but reached through non-reversible capacity consumption fixed by valid settlement under public rules.

---

## 7. Independence proof semantics

An `independence_proof` MUST prove all of the following:

### 7.1 Leaf identity

It MUST identify the exact leaf — by its `subtree_root` — for which independence is claimed.

### 7.2 Leaf binding

It MUST cryptographically bind the independence result to the exact `subtree_root` and not merely to a leaf label or local identifier.

It MUST thereby bind the result to the issuer-declared properties included in that exact closed leaf under the applicable public rules, without converting those declarations into semantically validated facts.

### 7.3 Settlement binding

It MUST bind the claimed independence result to a valid settlement event or settlement reference.

The referenced settlement event MUST be the unique carrier of the capacity consumption on which the claimed independence result depends.

The proof MUST NOT permit independence to be established by combining settlement evidence from one context with capacity evidence from another.

When settlement is aggregated, the proof semantics MUST also fix one exact aggregated settlement container and one exact membership interpretation for the claimed `subtree_root` under the applicable public rules.

The proof semantics MUST also ensure that the aggregated container, inclusion material, and bookkeeping interpretation are not reusable across multiple plausible leaf assignments for the claimed independence result.

The applicable rules domain MUST define, for each settlement mode it permits, one exact finality profile sufficient for canonical independence derivation.

No valid independence result MAY be derived from a settlement mode whose finality profile is omitted, discretionary, only heuristically selected, or left to implementation-local judgment.

### 7.4 Capacity validity

It MUST allow validation that the settlement consumed valid CERTCRYPT capacity under the system domain.

Capacity validity MUST be established from the referenced settlement event itself or from material cryptographically bound to that settlement event.

Capacity MUST be proven as consumed within the referenced settlement event, not merely as available or pre-authorized.

Capacity MUST NOT be accepted on the basis of a standalone, reusable, or ambiguously scoped reference that is not inseparably tied to the referenced settlement.

Any interpretation of capacity evidence that permits reuse across settlement contexts MUST be rejected.

Any interpretation that would allow locally invented, operationally cached, or node-synthesized capacity state to stand in for settlement-bound capacity consumption MUST be rejected.

### 7.5 Uniqueness / non-replay

It MUST allow validation that the same `subtree_root` was not validly consumed more than once for independence.

This uniqueness requirement MUST be enforced for the same `system_id`, the same applicable public-rules domain, and the same `subtree_root`.

The proof semantics MUST NOT permit the same `subtree_root` to yield more than one valid independence result within the same CERTCRYPT System Domain and rules domain by replaying or recontextualizing settlement.

A `subtree_root` MUST NOT yield more than one valid independence result across compatible, equivalent, or successor rule domains within the same CERTCRYPT System Domain.

### 7.6 System attribution

It MUST allow validation that the independence result belongs to the CERTCRYPT System Domain and not merely to a compatible or similar external system.

System attribution MUST be anchored to verifiable system-domain root material and MUST NOT rely on `system_id` as a bare semantic string.

### 7.7 Deterministic verifiability

It MUST be verifiable deterministically under public rules without requiring live access to CERTCRYPT.

The exact rules domain used for validation MUST be fixed by the proof and MUST NOT be selected heuristically by the verifier.

### 7.8 Valid Independence path

It MUST prove that the claimed leaf underwent a valid independence path under the applicable public rules.

The path is the whole of it, end to end: leaf fixation is one stage and settlement is another, and this section requires every stage (see `submission-set/1` Section 6).

This means the proof semantics MUST permit validation that the claimed independence result derives from:

- one exact closed leaf (its `subtree_root`)
- valid leaf binding under the applicable rules
- valid settlement with sufficient finality
- valid CERTCRYPT capacity consumption
- non-replayed and uniquely attributable result semantics

### 7.9 Non-reversible Independent state

It MUST prove that the claimed result is fixed into an independently verifiable state that no longer depends on the issuer as a live verification dependency.

This property concerns structural independence and offline verifiability only.

It MUST NOT be interpreted as upgrading issuer assertions into truth.

This property establishes independence from the issuer as a verification dependency, not merely immutability of the underlying data.

The independence state MUST be non-reversible under the applicable public rules once validly established.

Non-reversibility MUST be enforced by the underlying public rules and MUST NOT depend on any actor's discretion.

### 7.10 Per-certificate projection of the leaf result

`Independent` is established at the leaf level under §6: the canonical independence result, the capacity consumption, the settlement binding, and the anti-replay semantics are all properties of one exact closed leaf (its `subtree_root`), not of any individual certificate carried inside it.

The verdict a verifier reaches, however, MUST be evaluable per individual base certificate carried in that leaf, not only for the leaf as an aggregate.

For each base certificate carried in the claimed leaf:

- the base certificate MUST bind to exactly one accepted commitment through a hybrid emission binding: the digest of the canonical base certificate MUST equal the `certificate_commitment_digest` carried by that commitment, and that commitment's `commitment_id` MUST include into the leaf's `subtree_root` through a per-commitment inclusion path
- that leaf's `subtree_root` MUST in turn bind to the claimed container through the `inclusion_proof` (§10.8) under the applicable public rules
- a verifier evaluating that base certificate MUST be able to reach its verdict from that certificate, its per-commitment inclusion path, the `inclusion_proof`, the `independence_proof`, the applicable public rules, and the verifier-available original material, without requiring the full leaf contents and without requiring any other base certificate or any other commitment carried in the same leaf
- the per-certificate verdict MUST derive deterministically from the same canonical leaf-level independence result and MUST NOT introduce a separate or weaker independence semantics at the certificate level

A leaf MUST NOT be exposed to a verifier as a unit that is itself `Independent` or not-`Independent` as an aggregate. The leaf is the operational and cryptographic unit through which independence is established; the verdict surface is the individual base certificate anchored into that leaf.

This projection MUST NOT weaken any leaf-level binding defined in §6 or §7, and MUST NOT permit a base certificate to reach `Independent` unless the leaf that carries it validly reached `Independent` under public rules.

This requirement preserves the zero-data system design under multi-tenant operation: a verifier evaluating one base certificate MUST NOT gain visibility into any other base certificate carried in the same leaf, nor into the full leaf membership beyond the inclusion material strictly required to bind the claimed certificate.

A leaf carries the accepted commitments of exactly one submission set, and a fixation service MUST NOT fix a submission set whose members belong to more than one issuer: a leaf never mixes issuers. The membership the proof itself discloses is therefore bounded to that one issuer's set, and it is limited to opaque identifiers: `consumed_commitment_ids` (§10.4.1) lists the `commitment_id` values of the leaf, each a digest that reveals neither the commitment's content nor any other certificate, and nothing else about the other members travels with the proof. That list, its order and its cardinality are the leaf membership this specification accepts as disclosed; any further disclosure is prohibited by the paragraph above.

---

## 8. Non-goals

An `independence_proof` MUST NOT be interpreted as proving any of the following:

- that the issuer is legitimate
- that the issuer acted lawfully
- that the certified content is true
- that issuer assertions are true
- that declared properties reflect the actual properties of the original material
- that CERTCRYPT validated the original material
- that the leaf would pass complete verification against original material
- that a third party must accept the certificate
- that legal effect automatically exists
- that the certified event occurred exactly as described in a non-cryptographic sense

Implementations, user interfaces, and documentation MUST NOT describe `independence_proof` as if it proved any of the above.

`independence_proof` proves that a valid independence process occurred under public rules.

It does not prove that the issuer's declarations are true.

---

## 9. Required inputs for validation

To validate an `independence_proof`, a verifier MUST have access to:

1. the `independence_proof`
2. the exact leaf or a leaf-equivalent canonical representation sufficient to recompute its `subtree_root`
3. the relevant settlement reference or settlement-derived proof material
4. the inclusion proof when settlement is aggregated
5. the exact applicable public rules required to validate the proof
6. the CERTCRYPT system-domain verification material required to validate attribution
7. on the zero-data path, the capacity evidence for the verified certificate's commitment, sufficient to recompute that commitment's `commitment_id` (§10.4.2) and to validate capacity authorization and the holder signature offline without receiving stable identifiers

These inputs define the standard offline verification plane for `Independent`.

The enumeration above lists the inputs a verifier must possess; it does not fix the order in which they are validated (that order is defined in §12). On the zero-data path, the verifier MUST establish authorized-and-consumed capacity (input 7) before, and as a precondition of, validating the settlement that anchors that consumption (inputs 3 and 4): the settlement attests to a capacity consumption that must first be shown legitimate. A package whose settlement validates but whose capacity evidence does not MUST be rejected, never accepted on settlement alone.

Input 7 is the offline-transportable counterpart of the online capacity chain. On the zero-data path, a verifier that lacks this input cannot complete capacity-consumption validation offline and MUST treat the proof as insufficient for `Independent` rather than returning a downgraded result. The canonical form of this capacity evidence, and the artifacts it projects, are defined by the applicable public rules for the zero-data capacity profile.

An implementation MUST NOT present a zero-data `Independent` result as offline-complete unless the zero-data capacity path (input 7) and the external anchoring of time and consumption are both operative under the applicable public rules; a verifier that cannot complete the input-7 validation MUST return a non-success result indicating incompleteness, never a downgraded success (§16).

Under `/1`, a standard verifier validates `Independent` at the proof level from the canonical offline artifact set defined here and by the applicable public rules.

An advanced auditor MAY additionally inspect or reconstruct deeper settlement-layer material, raw economic substrate, or publication-layer context.

Such deeper inspection MAY reinforce auditability, but it MUST NOT be treated as a prerequisite for the standard offline verification plane defined by this specification.

That plane MUST be sufficient to validate settlement binding, settlement finality, capacity-consumption binding, and aggregated inclusion semantics when applicable, without requiring direct live validation of raw burn events, live balances, token-supply state, or equivalent economic substrate outside the canonical proof material required by the applicable public rules.

The canonical representation used to recompute the `subtree_root` MUST be deterministic and unambiguous under the applicable public rules.

A verifier MUST NOT require:

- a live CERTCRYPT API
- a managed storage service
- a resolver controlled by CERTCRYPT
- internal issuer systems
- historical CERTCRYPT databases
- direct online access to raw burn ledgers, live balances, or token-supply state when canonical settlement-derived proof material already suffices under public rules

Complete verification against original material is a separate verification plane.

Validation of `independence_proof` establishes whether the leaf validly reached `Independent` under public rules.

It does not establish whether issuer-declared properties would survive complete verification against original material.

---

## 10. Canonical logical fields

An implementation MAY choose its own serialization format, but every valid `independence_proof` MUST contain or deterministically imply the following logical fields.

Different serializations MAY exist, but they MUST remain semantically equivalent and MUST NOT permit parser-dependent changes to proof meaning.

### 10.1 `proof_version`

Identifies the proof model version.

This field MUST identify the version of the `independence_proof` model used to interpret the artifact.

### 10.2 `system_id`

Identifies the CERTCRYPT System Domain.

This field MUST bind the proof to the unique CERTCRYPT system identity.

It MUST resolve, directly or through public rules, to verifiable system-domain root material sufficient to reject proofs originating from a merely compatible or cloned external system.

That attribution path MUST expose, directly or deterministically, one exact system-domain root identifier sufficient to distinguish the CERTCRYPT domain from cloned, forked, or merely similar systems.

#### 10.2.1 `system_root_fingerprint`

Identifies the exact system-domain root identifier used for attribution.

This field MUST be present.

It MUST match the exact system-domain root identifier required by the applicable public rules.

### 10.3 `rules_version`

Identifies the exact versioned public ruleset under which the independence result is derived.

This field MUST be present or deterministically derivable.

It MUST identify the exact rules domain governing leaf validation, settlement interpretation, capacity semantics, and independence derivation.

The `rules_version` MUST match the exact rules domain under which the leaf was fixed.

#### 10.3.1 `proof_id`

The deterministic identifier of the proof.

This field MUST be present. It MUST be a 64-character lowercase hex value equal to:

```text
proof_id = SHA3-256( UTF-8( JCS( identity view ) ) )
```

where the identity view is the JSON object with exactly the members `proof_version`, `system_id`, `rules_version`, `system_root_fingerprint`, `subtree_root`, `closure_time`, `consumed_commitment_ids` and `settlement_ref`, carrying the proof's own values, canonicalized under RFC 8785 JCS. It excludes `proof_id` itself, `anti_replay`, `node_attestation`, `signature`, `proof_digest`, and every structural field outside the signed view (§10.13.1).

`proof_id` identifies a proof materialization. It is part of the signed view and carries no meaning of its own beyond the fields it digests.

### 10.4 `subtree_root`

The canonical Merkle root over the commitments accepted into the leaf for which independence is claimed. It is the leaf's bound value: a leaf commits to a sub-tree of one or more accepted commitments, and `subtree_root` is the root of that sub-tree.

This field MUST be mandatory.

The proof anchors `subtree_root`, not any single opaque commitment. Each accepted commitment binds into this root through its own inclusion path (`settlement.binding/1` §7); each base certificate binds to one such commitment through the hybrid emission binding (§7.10).

#### 10.4.1 `consumed_commitment_ids`

The ordered list of `commitment_id` values accepted into the leaf and consumed by this independence result. The `commitment_id` to which a verified base certificate binds (§7.10) MUST be a member of this list.

This field MUST be mandatory. It MUST be a non-empty array of 64-character lowercase hex values, in the canonical order of the submission set, with no value repeated. All of them belong to the single issuer whose submission set the leaf carries (§7.10).

#### 10.4.2 Capacity-evidence binding (zero-data profile)

On the zero-data path the proof does not carry a separate capacity-evidence digest. A commitment's identifier IS the canonical digest of its capacity evidence (`capacity.evidence/1 §7.1`): the proof lists the consumed commitments by those identifiers in `consumed_commitment_ids` (§10.4.1), and the verified certificate binds to exactly one of them through its per-commitment inclusion path (§7.10).

For the certificate it evaluates, a verifier MUST require the supplied capacity evidence to recompute to the `commitment_id` carried in that certificate's inclusion path, and MUST verify that evidence offline (capacity authorization and holder signature) without receiving stable identifiers. This is a per-commitment binding: a leaf of N commitments carries N independent evidences, each identified by its own `commitment_id`, with no single proof-level digest that could bind only one of them.

#### 10.4.3 `closure_time`

The canonical close timestamp of the submission set whose accepted commitments the leaf carries, as declared on the issuer side when the set was closed.

This field MUST be present, as an RFC 3339 timestamp in UTC with whole seconds, in the exact form `YYYY-MM-DDTHH:MM:SSZ`. It is part of the signed view (§10.13.1) and of the identity view of `proof_id` (§10.3.1).

`closure_time` is the issuer side's own declaration of when its submission set closed. It MUST NOT be treated as a CERTCRYPT time seal, as evidence that any subject existed at that time, or as the time authority of the independence result: the temporal property of the result derives from the settlement's irreversible block time (§10.6), not from this field.

### 10.5 `settlement_ref`

A canonical reference to the settlement event or settlement container from which independence is derived.

This field MUST be mandatory.

The `settlement_ref` MUST resolve deterministically to one and only one settlement event or settlement container under the applicable public rules.

The exact interpretation of that reference MUST be governed by the settlement-material contract of the selected `settlement_profile_id`.

It MUST NOT permit multiple valid interpretations.

For `/1`, `settlement_ref` MUST identify the exact aggregated settlement container, not merely a reusable external receipt label, transport identifier, or root-like value that could remain valid across multiple plausible bookkeeping contexts.

### 10.6 `settlement`

A mandatory settlement object describing the exact aggregated settlement context.

This field MUST be present.

It MUST contain or deterministically imply at least:

- `profile_id`
- `ref`
- `finality_proofs`

For `/1`:

- `profile_id` MUST equal the exact aggregated settlement profile the applicable public rules select for the declared `rules_version`
- `ref` MUST resolve to the same exact settlement container as `settlement_ref`
- `finality_proofs` MUST be a non-empty list of finality witnesses, each exposing the exact deterministic finality context required by the selected profile and applicable public rules. Each witness MUST name the public, permissionless substrate that witnesses it. A profile is satisfied when every present witness establishes sufficient irreversible finality. The list shape admits a future second public-substrate witness additively, without a new proof version; a qualified-authority or accredited time-attestation service MUST NOT be admitted as a witness.

Each finality witness carries `substrate`, `block_height`, `timestamp` and `confirmation_level`. Under `/1` a witness is a projection of the settlement-derived proof material, not an independent source:

- `substrate` MUST be the substrate of the selected settlement profile (for `settlement.aggregated.xrpl/1`, the exact string `xrpl`)
- `block_height` MUST equal the settlement material's `finality_proof.block_num`, and `timestamp` MUST equal its `finality_proof.block_timestamp`, string for string
- `confirmation_level` MUST be `irreversible`

The authoritative values are those of the settlement material, which the settlement anchor binds; the witness members are outside the signed view (§10.13.1). A verifier MUST require the equalities above and MUST reject a proof whose witness disagrees with the settlement material. A consumer that needs the block time of the result reads it from the settlement material, or from a witness only after that equality has been verified.

No valid proof MAY omit the aggregated settlement profile identifier.

No alternative settlement profile MAY be treated as compatible with `/1`.

### 10.7 `batch`

A mandatory batch object describing the exact aggregated settlement container claimed by the proof.

This field MUST be present.

It MUST contain or deterministically imply at least:

- `root`
- `index`
- `size`

Where:

- `root` identifies the exact `settlement_root`
- `index` identifies the exact deterministic position of the claimed leaf's `subtree_root` inside the settlement container
- `size` identifies the exact cardinality of the claimed settlement container; it MUST equal the anchored `batch_binding_preimage.leaf_count`, which is the width the inclusion path is evaluated against ([settlement.binding/1](../../../ecosystem/settlement/settlement.binding/1/specification.md) §6)

The `batch` object MUST be sufficient, together with `inclusion_proof` and the selected settlement profile, to determine one exact membership interpretation and one exact container-binding outcome for the claimed `subtree_root`.

### 10.8 `inclusion_proof`

This field MUST be present.

The `inclusion_proof` MUST be sufficient to determine one exact membership path, one exact leaf interpretation, and one exact container-binding outcome for the claimed `subtree_root` under the applicable public rules.

The `inclusion_proof`, together with each commitment's per-commitment inclusion path into `subtree_root`, MUST be sufficient to bind each individual base certificate carried in the claimed leaf to that `subtree_root`, as required by the per-certificate projection in §7.10.

For `/1`, the `inclusion_proof` terminal binding MUST match `batch.root` deterministically.

The `inclusion_proof` MUST NOT be valid if:

- it could also support a different plausible container interpretation
- it could also support a different leaf assignment
- it omits exact positional or bookkeeping semantics required by the selected settlement profile

### 10.9 `anti_replay`

A mandatory anti-replay object sufficient to validate uniqueness constraints for the claimed independence result.

This field MUST be present.

It MUST contain or deterministically imply at least:

- `nonce`
- `derivation`

The `anti_replay` object MUST be inseparably bound to the referenced settlement context and claimed leaf context.

It MUST NOT permit valid interpretation if the uniqueness evidence could be re-bound across different settlement containers, different leaf targets, or different CERTCRYPT rule contexts.

Under `/1` both members are derived, and nothing else is admissible:

```text
nonce      = hex( SHA3-256( UTF-8( "certcrypt/anti-replay/1/nonce:"      || settlement_ref || ":" || subtree_root ) ) )
derivation = hex( SHA3-256( UTF-8( "certcrypt/anti-replay/1/derivation:" || settlement_ref || ":" || subtree_root ) ) )
```

where `||` is concatenation, `settlement_ref` (§10.5) and `subtree_root` (§10.4) are the proof's own values, and `hex` is lowercase hexadecimal (64 characters). `anti_replay` is part of the signed view (§10.13.1). A verifier MUST recompute both members and MUST reject a proof in which either differs, even when it is well formed and signed: a value derived from another settlement container or another leaf is replay material. The non-replay property itself rests on the settlement binding and the inclusion proof (§12.6–§12.9); `anti_replay` makes the claimed context explicit in the signed proof and lets a verifier detect re-binding without any external record.

### 10.10 `independence_result`

A canonical result marker indicating that the leaf satisfied `Independent`.

This field MUST be semantically fixed to the independence result and MUST NOT be overloaded with institutional or semantic trust claims.

This field MUST NOT introduce alternative result states within the same proof model version. Under `/1` its value is exactly the string `independent`.

### 10.11 `proof_digest`

The canonical digest of the proof materialization.

This field MUST be present. Under `/1` a proof is always transported and archived as a standalone serialized artifact, and its digest is exactly:

```text
proof_digest = hex( SHA3-256( UTF-8( JCS( proof with proof_digest set to "" ) ) ) )
```

where `proof` is the complete artifact, `signature` and `node_attestation` included, and the member `proof_digest` is present with the empty string as its value (not removed). A verifier MUST recompute it and MUST reject a proof whose `proof_digest` differs. `proof_digest` is the artifact's integrity digest; it is outside the signed view and adds no authenticity of its own.

### 10.12 `created_at`

Timestamp of proof materialization.

This field MAY be present, but it MUST NOT be treated as the source of truth for the independence event itself.

### 10.13 `signature`

The system domain's signature over the signed view of the proof (§10.13.1).

This field MUST be present. Its value is a composite signature object under [`composite-signature/1`](../../../foundation/composite-signature/1/index.md): `alg` (the profile identifier), `mode` (`AND`), the ordered component `signatures`, and `signing_kid`, a non-empty string naming the signing key, and no other member. Under each rules domain:

- the profile is the one the applicable public rules select for the independence proof signature (for `rules/2026-01`, `certcrypt-composite-p256-mldsa65-v1`, ECDSA P-256 and ML-DSA-65); a verifier MUST take the expected profile from the rules, never from the artifact
- the signing key is the system-domain Level-1 capacity key published in the bootstrap statement ([`system-foundation/1`](../../../foundation/system-foundation/1/index.md) Section 6), whose component public keys a verifier resolves offline from that statement
- the signed message is `SHA3-256( UTF-8( JCS( signed view ) ) )`, framed as `composite-signature/1` defines, and both components MUST verify

A proof without a signature, with a signature under another profile, or whose signature does not verify against that key MUST NOT reach `Independent`. A verifier that cannot resolve the key or cannot run a component MUST return a non-success result (incomplete or unsupported), never treat the signature as optional.

The signature authenticates the members of the signed view; it MUST NOT be treated as the ontological source of independence (§14).

#### 10.13.1 Signed-view boundary

The signature covers the signed view: the JSON object with exactly the members `proof_version`, `system_id`, `system_root_fingerprint`, `rules_version`, `proof_id` (§10.3.1), `subtree_root`, `closure_time` (§10.4.3), `consumed_commitment_ids`, `settlement_ref`, `anti_replay` (§10.9) and, only when the proof carries it, `node_attestation` (§10.15), with the proof's own values, canonicalized under RFC 8785 JCS. An absent `node_attestation` is omitted from the view, never represented as `null`.

It does NOT cover `settlement`, `batch`, `inclusion_proof`, `independence_result`, `proof_digest`, `created_at`, or `signature`. This is deliberate, not a gap:

- The leaf-bound value the signature commits to is `subtree_root`. Each verified certificate binds to that `subtree_root` through its own per-commitment inclusion path (§7.10), so a forged or substituted leaf cannot be paired with a signed `subtree_root` it does not belong to.
- `batch`, `inclusion_proof` and the finality witnesses of `settlement` are membership and anchoring material whose authority derives from the settlement anchor, NOT from the proof signature: the `batch.root`/`settlement_root` is bound to the on-chain settlement memo through the batch-binding preimage, a verifier MUST require the settlement-side coherence (`batch_manifest.settlement_root` == batch-binding `settlement_root` == `batch.root`), the irreversible anchoring (§12.6), and the equality of each finality witness with the settlement material (§10.6). Mutating any of them without a correspondingly anchored settlement does not yield a valid verdict.
- `independence_result` is fixed (§10.10) and `proof_digest` is recomputed (§10.11).
- Therefore the integrity of the verdict rides the signed view plus the anchored settlement, not a signature over every transported member. A profile MUST NOT rely on the proof signature alone to authenticate `batch`, `inclusion_proof` or the finality witnesses.

### 10.14 Canonical coherence requirement

All logical fields of a valid `independence_proof` MUST be mutually coherent.

In particular:

- `rules_version`
- `subtree_root`
- `consumed_commitment_ids`
- `settlement_ref`
- `settlement`
- `batch`
- `inclusion_proof`
- `anti_replay`
- `system_id`
- `system_root_fingerprint`
- `independence_result`
- `node_attestation`, when present

MUST resolve to one and only one canonical independence result for one exact leaf under one exact CERTCRYPT System Domain and one exact rules domain.

No valid interpretation MAY be obtained by pairing a syntactically valid `independence_proof` with a different valid base certificate, different supporting proof material, or a different settlement context if those elements do not resolve to that same exact canonical result.

### 10.15 `node_attestation`

An optional attestation, by the system domain, that the submission set whose commitments the leaf carries entered fixation through a node the system domain recognized, and when that recognition was checked.

This field MAY be present. When present, it MUST be an object with exactly two members:

- `node_id` — the stable identifier of the recognized node: the string `op:` followed by exactly 22 characters of the standard base64 alphabet (`A`–`Z`, `a`–`z`, `0`–`9`, `+`, `/`). It is stable for as long as the node keeps the same recognized identity, so a node that wants to be recognizable (for example a sector node) can publish it and a verifier can recognize it. It is an opaque identifier: it names a transport, not the issuer of the certificates, and its derivation is not needed to verify it.
- `recognized_at` — the instant at which the fixation service checked that node's recognition when it received the submission, as an RFC 3339 timestamp in UTC with whole seconds (`YYYY-MM-DDTHH:MM:SSZ`). It MUST NOT be earlier than `closure_time`.

Nothing else MAY appear in the attestation. In particular it MUST NOT carry, reference or summarize any register of nodes, the recognition history of this or any other node, or any other operator's identity: a verifier learns which node carried this leaf and nothing about the others.

`node_attestation` is part of the signed view (§10.13.1). Its authenticity is the authenticity of the proof signature: a verifier MUST NOT consult any register, list or service to validate it, and once the proof signature verifies, the attestation is authentic as stated. A verifier MUST reject a proof whose `node_attestation` is malformed, and a conforming verifier SHOULD expose the attested `node_id` and `recognized_at` in its result when, and only when, the proof reaches `Independent`.

A proof without `node_attestation` is complete and MAY reach `Independent`: the attestation is evidence about the transport, not a condition of independence. A producer emits it whenever the submission was carried by a recognized node.

`node_attestation` MUST NOT be read as:

- evidence that the issuer is legitimate, or that the node vouched for the certified content
- a time seal: `recognized_at` states when recognition was checked, not when any subject existed, and the temporal property of the result remains the settlement's irreversible block time (§10.6)
- an endorsement, rating or certification of the node

---

## 11. Canonical minimal structure

The following JSON object illustrates a minimal logical structure.

```json
{
  "proof_version": "independence.proof/1",
  "system_id": "<system_id>",
  "system_root_fingerprint": "<system_root_fingerprint>",
  "rules_version": "<rules_version>",
  "proof_id": "<proof_id>",
  "subtree_root": "<subtree_root>",
  "closure_time": "<closure_time>",
  "consumed_commitment_ids": ["<commitment_id_1>", "<commitment_id_2>"],
  "settlement_ref": "<settlement_reference>",
  "settlement": {
    "profile_id": "<settlement_profile_id>",
    "ref": "<settlement_reference>",
    "finality_proofs": [
      {
        "substrate": "<public_substrate_id>",
        "block_height": "<block_height>",
        "timestamp": "<irreversible_block_time>",
        "confirmation_level": "<confirmation_level>"
      }
    ]
  },
  "batch": {
    "root": "<settlement_root>",
    "index": "<leaf_index>",
    "size": "<leaf_count>"
  },
  "inclusion_proof": ["<hash1>", "<hash2>", "<hash3>"],
  "anti_replay": {
    "nonce": "<uniqueness_nonce>",
    "derivation": "<uniqueness_derivation>"
  },
  "node_attestation": {
    "node_id": "<node_id>",
    "recognized_at": "<recognition_check_time>"
  },
  "independence_result": "independent",
  "proof_digest": "<proof_digest>",
  "signature": {
    "signing_kid": "<system_domain_level1_kid>",
    "alg": "<signature_profile_id>",
    "mode": "AND",
    "signatures": ["<classical_component>", "<pq_component>"]
  }
}
```

`node_attestation` is optional (§10.15); every other member shown is mandatory.

These examples are illustrative only.  
The exact serialization MAY vary, but the semantics MUST remain equivalent.

---

## 12. Validation procedure

A conforming verifier MUST validate an `independence_proof` using the following logical sequence.

Every step is mandatory. The sequence is logical: a verifier MAY evaluate the steps in another order provided it evaluates all of them and reaches the same verdict, with one fixed constraint — on the zero-data path, §12.5 is evaluated before §12.6 and §12.7, and a failure in §12.5 is reported as that failure, not as a settlement failure (§9).

### 12.1 Validate proof model version

The verifier MUST confirm that the proof version is supported.

If unsupported, validation MUST fail deterministically.

The verifier MUST NOT silently downgrade interpretation to an older or looser proof model.

The verifier MUST reject any attempt to interpret the proof under a less strict, earlier, heuristically selected, or implementation-default model version.

The verifier MUST reject serializations that are structurally ambiguous, including duplicate conflicting fields, missing mandatory logical fields, or unsupported semantic values in critical proof members.

In particular the verifier MUST reject a proof in which:

- `proof_id` is not the digest of the identity view (§10.3.1)
- `proof_digest` is not the digest of §10.11
- `closure_time`, or `node_attestation.recognized_at` when present, is not RFC 3339 UTC with whole seconds
- `consumed_commitment_ids` is empty, repeats a value, or carries a value that is not 64 lowercase hex characters
- `node_attestation`, when present, does not have exactly the shape of §10.15, or its `recognized_at` precedes `closure_time`
- `independence_result` is not exactly the string `independent` (§10.10)

### 12.2 Validate rules domain

The verifier MUST validate the proof under the exact `rules_version` declared in, or deterministically bound into, the proof.

If the applicable rules domain cannot be identified uniquely and deterministically, validation MUST fail.

The verifier MUST NOT infer the rules domain heuristically from transport context, adapter defaults, local configuration shortcuts, or compatible fallback behavior.

Compatible, equivalent, or successor rules MUST NOT be used as substitutes unless explicitly defined as equivalent under the applicable public rules.

### 12.3 Validate system attribution

The verifier MUST confirm that the proof belongs to the CERTCRYPT domain using the configured system root or equivalent public verification material.

If attribution cannot be validated, the proof MUST be rejected.

The verifier MUST NOT treat `system_id` alone as sufficient attribution evidence.

The verifier MUST validate that the attributed proof resolves to one exact system-domain root identifier under the applicable public rules.

The verifier MUST reject any proof that is only syntactically compatible with CERTCRYPT but whose attributed settlement or surrounding evidence could also belong to a merely similar, cloned, or external system domain.

If the root identifier is ambiguous, missing when required, or inconsistent with the proof context, the proof MUST be rejected.

The verifier MUST verify the proof signature (§10.13) over the signed view (§10.13.1) against the system-domain Level-1 capacity key of the bootstrap statement, under the profile the rules select. A proof whose signature is absent, declares another profile, or does not verify MUST NOT reach `Independent`. When the signature verifies, the members of the signed view, `node_attestation` included, are authentic.

### 12.4 Validate commitment binding and sub-tree inclusion

The verifier MUST validate that the supplied base certificate corresponds exactly to one accepted commitment whose `commitment_id` includes into the `subtree_root` referenced in the proof, through the hybrid emission binding of §7.10.

If the certificate-to-commitment binding or the commitment-to-`subtree_root` inclusion does not match, the proof MUST be rejected.

### 12.5 Validate capacity authorization (zero-data path)

This step applies on the zero-data path (§10.4.2). It validates the authorization to consume capacity, which is logically prior to, and independent of, the settlement that later fixes the consumption (`capacity.commitment/1 §9`: authorization authorizes possible use; settlement fixes actual consumption). The verifier performs it before settlement validation (§12.6–§12.7): the settlement attests to a consumption whose authorization must first be shown legitimate.

Using only the capacity evidence supplied as input 7 (§9) and public verification material, the verifier MUST validate, without contacting CERTCRYPT and without receiving stable identifiers:

- that the supplied capacity evidence recomputes to exactly the `commitment_id` carried in the verified certificate's per-commitment inclusion path (§10.4.2, `capacity.evidence/1 §7.1`)
- that the system-domain (Level 1) signature over the holder authorization binds the authorized holder key set under the same exact system domain and rules domain claimed by the proof
- that the holder's signature over the commitment is valid against a key whose membership in the authorized holder key set is proven, under the applicable public rules for the zero-data capacity profile

If any of these cannot be established, the proof MUST be treated as insufficient for `Independent`. The verifier MUST NOT substitute settlement validation for this step, and MUST NOT infer authorized capacity from the existence of a settlement reference alone.

This step establishes that consumption was authorized; §12.7 establishes that the authorized consumption was fixed through settlement. Neither is sufficient without the other, and the canonical form of the capacity evidence is fixed by the applicable public rules for the zero-data capacity profile, not by this section.

### 12.6 Validate settlement reference

The verifier MUST validate that the referenced settlement event:

- exists
- resolves uniquely under the applicable rules domain
- is structurally valid for the settlement model in use

For the standard offline verification plane, that validation MUST be satisfiable from the required proof inputs and any exact settlement-derived proof material mandated by the applicable public rules.

That settlement-derived proof material MUST satisfy the settlement-material contract defined for the selected `settlement_profile_id`.

If the settlement cannot be validated, the proof MUST be rejected.

The verifier MUST also validate that the referenced settlement has sufficient finality under the applicable public rules before accepting the proof as canonically valid.

If sufficient finality cannot be established, the proof MUST be rejected even if the settlement reference is otherwise structurally valid.

Sufficient finality MUST be defined by the applicable rules domain and MUST be deterministically evaluable.

The applicable rules domain MUST define sufficient finality per permitted settlement mode, including any exact depth, threshold, epoch-boundary, challenge-window, attestation threshold, timeout, or equivalent deterministic parameters required for canonical acceptance.

If the applicable rules domain does not fully define the finality profile for the referenced settlement mode, the proof MUST be rejected.

Where the applicable public rules express finality through exact parameters such as confirmation depth, threshold, epoch boundary, challenge window, or equivalent deterministic criteria, those parameters MUST be validated explicitly.

Reorganization risk, rollback risk, orphaning risk, probabilistic acceptance, or equivalent reversible-settlement conditions MUST be treated as failure to establish canonical finality unless the referenced settlement has already satisfied the exact deterministic finality profile required by the applicable rules domain.

Implementations MUST NOT return `Independent` on the basis of a provisional, optimistic, pending, soft-confirmed, or otherwise not-yet-final settlement interpretation.

### 12.7 Validate settlement-bound capacity consumption

The verifier MUST validate that the referenced aggregated settlement container consumed valid CERTCRYPT capacity attributable to the system domain.

For the standard offline verification plane, this validation MUST be satisfiable from settlement-bound canonical proof material and MUST NOT require direct inspection of live balances, token ledgers, or equivalent raw economic state unless the verifier has explicitly entered a deeper audit path outside standard `Independent` verification.

If valid settlement-bound capacity cannot be established, the proof MUST be rejected.

The verifier MUST NOT infer capacity validity from detached, reusable, or standalone economic references.

The verifier MUST reject any interpretation of settlement-bound capacity evidence that allows reuse, ambiguity, or re-binding across settlement contexts.

### 12.8 Validate inclusion proof

The verifier MUST validate the inclusion proof binding the `subtree_root` to the aggregated settlement container.

If inclusion cannot be validated, the proof MUST be rejected.

The verifier MUST also validate that the terminal inclusion root or equivalent inclusion binding matches `batch.root` and the referenced settlement context deterministically.

The verifier MUST validate the exact inclusion position given by `batch.index`.

The verifier MUST also validate any exact aggregated bookkeeping parameters required by the applicable public rules, including ordering, cardinality, path interpretation, leaf interpretation, and deterministic membership semantics.

The verifier MUST reject any proof context in which the same referenced settlement container, root, receipt material, or inclusion material could yield more than one plausible leaf-assignment interpretation.

The verifier MUST also reject any proof context in which aggregated receipt material or membership material is reusable across multiple containers, multiple bookkeeping interpretations, or multiple leaf targets under the applicable public rules.

### 12.9 Validate non-replay conditions

The verifier MUST validate that the settlement semantics do not permit the same `subtree_root` to produce more than one valid independence result within the same CERTCRYPT System Domain and applicable public-rules domain.

The verifier MUST validate the exact `anti_replay` object carried by the proof, by recomputing both members from the proof's `settlement_ref` and `subtree_root` (§10.9) and requiring exact equality.

If replay cannot be excluded under the applicable public rules, the proof MUST be rejected.

The verifier MUST also reject any context in which more than one `independence_proof` is presented for the same `subtree_root` under the same `system_id` and `rules_version`.

The verifier MUST also reject any context in which the same `subtree_root` yields more than one `independence_proof` across compatible, equivalent, or successor rule domains within the same `system_id`, unless explicit equivalence is defined under public rules.

### 12.10 Validate issuance-time participation

The verifier MUST validate that issuance-time participation in the independence flow was cryptographically bound into the claimed leaf context under the applicable public rules.

For certificates governed by `CCSP/1`, `payload.anchor.root_id` is the only admissible certificate-visible issuance-time participation reference under the public rules that require such a reference.

For certificates governed by `CCCP/1`, the verifier MUST treat the signed anchor and `payload.anchor_commitment_digest_hex` as the non-reconstructible issuance binding that preserves that reference from post-hoc reconstruction.

For `/1`, an admissible `payload.anchor.root_id` MUST equal one exact published system-domain root identifier valid for the selected `rules_version`.

For the active public bootstrap:

- `payload.anchor.root_id` MUST equal `system_root_fingerprint` exactly
- that value MUST resolve to the current published CERTCRYPT bootstrap root identifier under the selected public rules
- no alternative, locally inferred, cloned, forked, or successor root identifier MAY be treated as equivalent unless explicit public equivalence is published

If issuance-time participation is not provable from the leaf and its required proof material without reliance on external historical records, the proof MUST be rejected.

The verifier MUST also reject any proof context in which issuance-time participation is only retrospectively simulated, structurally approximated, or inferred from post-issuance compatibility between later artifacts.

No leaf artifact, settlement artifact, receipt, package wrapper, resolver output, or similar later-produced context MAY be treated as normatively equivalent to an irreproducible issuance-time participation binding that was absent at issuance.

If the issuer, SDK, or issuance workflow failed to bind the required participation reference into the signed issuance-time artifact set in admissible form, no later leaf, settlement, package, resolver, or verifier behavior MAY repair that failure for the purpose of `Independent`.

Optional, ambiguously modeled, heuristically derived, or retrospectively reconstructed issuance markers MUST NOT be treated as normatively equivalent to a valid irreproducible issuance-time participation binding.

If the verifier cannot distinguish original issuance-time participation from a post-hoc compatible reconstruction under the applicable public rules, the proof MUST be rejected.

### 12.11 Produce result

Only if all previous checks succeed MAY the verifier return `Independent`.

Any failed check MUST result in rejection.

Returning `Independent` from proof validation MUST NOT be interpreted as semantic confirmation of issuer assertions.

It means only that the verifier established, under public rules, that the claimed closed leaf validly reached a non-reversible and independently verifiable independence state.

### 12.12 Reject ambiguous or spliced proofs

The verifier MUST reject any proof or proof-context combination in which the supplied materials can be interpreted as:

- mixing valid artifacts from different leaves
- mixing valid artifacts from different settlement contexts
- mixing valid artifacts from different CERTCRYPT System Domains
- producing more than one plausible canonical independence result

Any such ambiguity MUST be treated as invalid, not as partially valid.

---

## 13. Aggregated settlement model

Under the active architecture for `/1`, the only valid settlement model is aggregated settlement.

Accordingly:

- `settlement.profile_id` MUST be the exact aggregated settlement profile the applicable public rules select for the declared `rules_version`
- `batch` MUST be present
- `inclusion_proof` MUST be present
- `anti_replay` MUST be present
- the proof MUST fix one exact aggregated settlement container and MUST NOT rely on a reusable root or receipt value without exact container interpretation
- the proof MUST fix one exact leaf-assignment interpretation within that container
- any ordering, cardinality, leaf-construction, indexing, or positional semantics required for deterministic reconstruction MUST be present or deterministically derivable
- the proof MUST permit deterministic assignment of the relevant capacity consumption to the claimed leaf
- the proof MUST permit validation that the relevant aggregated settlement reached sufficient finality under the applicable public rules
- the applicable rules domain MUST define the exact finality profile required for canonical acceptance of this aggregated model

No direct-settlement interpretation is permitted under `/1`.

---

## 14. Signature semantics

Every `independence_proof` carries the system domain's signature (§10.13).

- it authenticates the members of the signed view (§10.13.1): without it, `consumed_commitment_ids`, `closure_time`, `proof_id`, `anti_replay` and `node_attestation` could be altered undetected
- its absence, or its failure to verify, invalidates the proof for `Independent`
- it MUST NOT be treated as the ontological source of independence: independence derives from the leaf binding, the settlement binding, the capacity validation and the finality defined in §6–§13, which the verifier validates on their own
- its presence MUST NOT rescue an otherwise invalid proof

---

## 15. Managed interfaces

CERTCRYPT MAY expose convenience interfaces for:

- retrieval
- delivery
- inspection
- formatting
- indexing

of `independence_proof`.

Such interfaces:

- MUST be non-authoritative
- MUST be optional
- MUST NOT be required for proof existence
- MUST NOT be required for proof validation
- MUST NOT redefine the proof semantics
- MUST NOT be able to change the validation result by serving inconsistent managed copies

Any managed copy of an `independence_proof` MUST be treated as an operational convenience layer only.

---

## 16. Failure semantics

### 16.1 Missing settlement data

If settlement data required for validation is missing, the proof MUST fail validation.

### 16.2 Missing inclusion proof

If aggregated settlement is used and inclusion proof is absent or invalid, the proof MUST fail validation.

### 16.3 Mismatched `subtree_root`

If the `subtree_root` does not match the claimed leaf, the proof MUST fail validation.

### 16.4 Invalid capacity

If capacity validity cannot be established, the proof MUST fail validation.

### 16.5 Unattributable system domain

If the proof cannot be attributed to the CERTCRYPT domain, the proof MUST fail validation.

### 16.6 Ambiguous result

If validation cannot determine a single deterministic independence result, the proof MUST fail validation.

### 16.7 Unsupported result marker

If `independence_result` is not exactly the string `independent` (§10.10), the proof is malformed and MUST be rejected; no other value, including one that names a failure state, is read as a result.

---

## 17. Security properties

A conforming `independence_proof` model MUST preserve the following properties:

1. leaf-binding integrity
2. settlement-binding integrity
3. capacity-binding integrity
4. non-replay
5. deterministic verifiability
6. offline verifiability
7. system-domain attribution
8. rules-domain attribution
9. independence from live CERTCRYPT infrastructure
10. canonical semantic coherence across serializations
11. sufficient settlement finality before acceptance
12. rejection of spliced or ambiguous proof contexts
13. authenticity of the signed view under the system-domain Level-1 key

Any implementation that weakens any of these properties MUST be considered non-conformant.

---

## 18. Privacy and data-minimization

An `independence_proof` SHOULD minimize disclosure beyond what is strictly necessary for deterministic independence validation.

An `independence_proof` MUST NOT require inclusion of:

- original certified payload material
- semantic content beyond what is necessary to validate leaf binding
- internal CERTCRYPT operational state
- historical CERTCRYPT database identifiers

The proof model MUST remain compatible with the zero-data system design.

`node_attestation` (§10.15), when present, discloses which recognized node carried the leaf's submission and when its recognition was checked. It identifies a transport, never the issuer, and it travels only in the proof, never on the settlement substrate. Certificates carried through the same node therefore share a visible `node_id`; this correlation lives on the artifact surface, where a party holding several proofs may already correlate them, and the proof MUST NOT disclose any other node or any register of nodes.

---

## 19. Relationship to verification package

The `verification_package` is the transport and verification container sufficient to verify `Independent` in practice.

The `independence_proof` is the canonical independence artifact within that package.

A `verification_package` MAY contain additional materials, but it MUST NOT redefine the semantics of `independence_proof`.

If any conflict exists between packaging convenience and independence semantics, the semantics defined by this specification SHALL prevail.

---

## 20. Relationship to base certificates

The `independence_proof` does not alter the base certificate.

It MUST NOT:

- rewrite the base certificate
- upgrade semantic truth claims
- modify issuer statements
- change issuance meaning retroactively

It fixes issuer-attributed declarations into a non-reversible and independently verifiable state.

It thereby enables third parties to evaluate, verify, or refute those declarations under public rules without relying on the issuer or on CERTCRYPT as a live authority.

It only proves that the relevant leaf validly reached `Independent` under public rules.

Although the independence result is established at the leaf level, the verdict is evaluated per individual base certificate anchored into that leaf, as defined in §7.10. A base certificate reaches `Independent` only if the leaf that carries it validly reached `Independent` and the certificate is bound, through the hybrid emission binding of §7.10, to one accepted commitment that includes into the leaf's `subtree_root`.

Failure of `independence_proof` validation MUST NOT invalidate the cryptographic validity of the base certificate as `Issued`.

---

## 21. Anti-retroactivity rule

An `independence_proof` MUST NOT validly exist for a certificate or leaf that did not declare participation in the independence flow at issuance time under the relevant public rules.

If issuance-time participation cannot be established, the proof MUST fail validation.

This prevents retroactive independence fabrication.

Issuance-time participation MUST be cryptographically bound into the `subtree_root` or into proof material inseparably tied to that commitment.

Where `CCSP/1` and `CCCP/1` govern the certificate path, that requirement MUST be satisfied through the issuance-time envelope reference and signed anchor binding defined by those specifications, not through later settlement, packaging, or resolver behavior.

It MUST be verifiable without reliance on external historical records.

Retroactive construction of leaf artifacts that simulate issuance-time participation MUST be rejected.

---

## 22. Conformance

An implementation conforms to `independence.proof/1` if and only if:

- it preserves all mandatory semantics defined in this document
- it validates all required bindings
- it rejects invalid or incomplete proofs deterministically
- it does not require live CERTCRYPT infrastructure for validation
- it does not reinterpret operational convenience as ontological truth

Partial implementations MUST NOT claim full conformance.

---

## 23. Future evolution

Future versions of this model MAY:

- add new serialization formats
- add new settlement adapters
- add new proof transport forms
- add new optional integrity fields

Future versions MUST NOT:

- remove leaf binding
- remove settlement binding
- remove capacity validation
- remove offline verifiability
- remove system-domain attribution
- relax parser strictness in a way that permits ambiguous semantics
- permit canonical ambiguity across equivalent serializations
- permit acceptance before required settlement finality
- reintroduce dependency on live CERTCRYPT infrastructure

Any such change would require a non-compatible new model version.

---

## 24. Final normative statement

A valid `independence_proof` is the canonical, deterministic, offline-verifiable artifact by which a verifier can establish that a specific leaf reached `Independent` under CERTCRYPT public rules through valid settlement and valid CERTCRYPT capacity, without requiring CERTCRYPT as a live authority.

---

## 25. Versioning & extensibility

This `/1` specification defines the current active public contract for `independence.proof/1`.

Once frozen, this version MUST NOT be modified in place in any way, including editorial, typographic or clarifying changes that would leave its normative meaning unchanged. Any change MUST be published under a new version identifier.

---

## 26. References

- CERTCRYPT Specifications
    - [security-model/1 — CERTCRYPT Security Model](../../../foundation/security-model/1/index.md)
    - [system-domain/1 — CERTCRYPT System Domain](../../../foundation/system-domain/1/index.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../../foundation/rules-domain/1/index.md)
    - [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../../protocols/CCCP/1/index.md)
    - [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../../protocols/CCSP/1/index.md)
    - [CCVP/1 — CERTCRYPT Consistency Verification Protocol](../../../protocols/CCVP/1/index.md)
    - [composite-signature/1 — CERTCRYPT Composite Signature Profile](../../../foundation/composite-signature/1/index.md)
    - [system-foundation/1 — CERTCRYPT System Foundation](../../../foundation/system-foundation/1/index.md)
    - [settlement.aggregated.xrpl/1 — CERTCRYPT XRPL Aggregated Settlement Profile](../../../ecosystem/settlement/settlement.aggregated.xrpl/1/index.md)
    - [capacity.commitment/1 — CERTCRYPT Capacity Commitment Specification](../../../ecosystem/settlement/capacity.commitment/1/index.md)
    - [capacity.evidence/1 — CERTCRYPT Capacity Evidence](../../../ecosystem/settlement/capacity.evidence/1/index.md)
    - [settlement.binding/1 — CERTCRYPT Aggregated Settlement Binding](../../../ecosystem/settlement/settlement.binding/1/index.md)
    - [submission-set/1 — CERTCRYPT Submission Set Protocol](../../../protocols/settlement/submission-set/1/index.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
    - [RFC 8785 — JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785)
    - [RFC 3339 — Date and Time on the Internet: Timestamps](https://www.rfc-editor.org/rfc/rfc3339)

---

**End of independence.proof/1**
