# CERTCRYPT Submission Set Specification (submission-set/1)

**Identifier:** `submission-set/1`  

**Label:** CERTCRYPT Submission Set Specification (submission-set/1)  

**Type:** Protocol

**Status:** Frozen

**Layer:** Layer 1 — Protocols

**Depends on:** See References *(active normative dependencies are listed below)*  

**Naming convention:**  
`submission-set/1` is the formal identifier.  
CERTCRYPT Submission Set Specification (submission-set/1) is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.  

**Audience:** Protocol implementers, verifiers, auditors  

**Purpose:** Define the normative semantics, constraints, and interpretation boundary of submission-set/1 within the active CERTCRYPT public architecture.  

**Intended use:** submission-set/1 is intended to be the authoritative public specification used by conforming implementers, verifiers, auditors, and ecosystem tooling when handling this artifact or behavior.  

**Scope:** Defines the active normative behavior of submission-set/1; adjacent protocols, profiles, operational tooling, and product behavior remain out of scope except where explicitly referenced.  

**Non-goals:** submission-set/1 does not prove truth, semantic validity, legal validity, or live service authority by itself, and MUST NOT be interpreted as a substitute for cryptographic authenticity, Proof of Independence, or managed-service behavior outside its own normative scope.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale

This specification defines the canonical execution request and validation boundary for submitting a set of capacity commitments to CERTCRYPT for fixation.

A `submission_set` is the protocol artifact by which one or more autonomous commitments are presented to CERTCRYPT for deterministic structural, cryptographic, economic, and rule-level evaluation under public rules. The set is a transport container: its members are evaluated and fixed independently, and the set itself is not a unit of coherence.

This document defines:

- what a `submission_set` is
- the set envelope and the exact derivation of its identity
- what each member commitment MUST bind to
- the closed list of preconditions that concern the set as a whole
- what the fixation service MUST validate mechanically per member before accepting it
- how the accepted subset forms a settlement leaf
- how idempotency, replay resistance, and uniqueness MUST be enforced per member
- what a per-member accepted or rejected outcome, and a set-level verdict, MAY and MUST NOT mean

This document does **not** define:

- certificate issuance
- semantic truth of issuer assertions
- the canonical artifact that proves `Independent`
- complete offline verification against original material
- backend-specific settlement execution choreography beyond the public proof-material contract fixed by the selected `settlement_profile_id`
- the full capacity-authorization format

Those concerns belong to separate specifications.

---

## 2. Scope

This specification applies to all systems, implementations, SDKs, issuer-side nodes, fixation services, settlement adapters, and managed layers that:

- construct
- transmit
- receive
- validate
- retry
- audit

a `submission_set` claiming conformity with CERTCRYPT.

Any implementation that uses `submission_set` as the execution boundary for a CERTCRYPT independence path MUST conform to this specification.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

---

## 4. Design principles

`submission-set/1` is designed around the following principles:

- **Transport container, not an atomic unit:** A `submission_set` is a set of autonomous commitments presented together for convenience. It has no coherence requirement between members and no shared fixation outcome: once the set itself is admissible, members succeed or fail independently.
- **A closed set of set-level conditions:** What concerns the set as a whole — its envelope and identity, its rules domain, the operator carrying it, the single issuer it belongs to, and whether that issuer's capacity covers it — is decided once for the set, from a closed list (§8.1, §9.4, §11.2). Nothing outside that list may refuse a whole set.
- **Per-member evaluation:** Replay handling, binding integrity, the dual temporal condition, and protocol conformity of each member's chain MUST be evaluated mechanically and reproducibly for each member, independently of the other members.
- **No member tumbles the set:** A member that fails a per-member rule MUST NOT cause an otherwise-valid member to be rejected. The fixation service MUST accept the valid subset and reject only the members that fail.
- **Separation from proof:** Submission does not produce Proof of Independence and MUST NOT be interpreted as `Independent`.
- **Institutional independence:** Submission semantics MUST be defined by public rules rather than by managed-service framing, operator discretion, or hosted convenience.
- **Interpretation boundaries:** An accepted member expresses that a commitment entered a fixation path under public rules. It does not prove truth, semantic validity, or final independence state.

---

## 5. Architectural role

Within the current CERTCRYPT architecture:

- issuers emit base certificates
- CERTCRYPT does not emit certificates
- participation is fixed from issuance according to the applicable rules
- CERTCRYPT operates fixation only
- valid settlement and valid capacity remain required for `Independent`
- `independence_proof` remains the canonical artifact of independence, produced per accepted commitment
- verification remains possible offline and MUST NOT require CERTCRYPT as a live authority

`submission-set/1` defines the execution request for fixation. It does not define a competing canonical independence artifact.

### 5.1 Integrator path (Informative)

The following operational mental model is informative:

1. build one or more commitments
2. submit them together as one submission set
3. receive either one verdict on the set as a whole (a refused precondition, or insufficient capacity) or a per-member outcome: each commitment is independently accepted into a fixation path or returned an actionable fail-closed reason
4. for each accepted commitment, obtain its `independence_proof` (per the independence path) or a clear non-positive result

A submission set MAY carry a single commitment; the single-member case is the degenerate set and follows the same per-member rules. Tooling SHOULD present the per-member outcome plainly: which commitments were accepted and which were rejected, and why.

### 5.2 Unit of acceptance

The submission set is a transport container whose members are autonomous: a single invalid member does not reject the others, and the accepted subset forms the settlement leaf (§9.3). Conforming implementations targeting the commitment sub-tree model MUST use `submission-set/1`.

---

## 6. Definitions

For the purposes of this specification:

- **fixation service** means the party that performs fixation for a rules domain:
  the recipient of a submission set, and the only party that accepts or rejects
  its members. This specification states its obligations without naming it,
  because which party holds the role is a property of the rules domain, not of
  this protocol: the applicable registry entry declares it.
- **fixation** means the operation by which a closed leaf of accepted members, together with the
  issuer declarations it carries and the exact rules domain applied, is fixed into an independently
  auditable and later verifiable state. Fixation determines whether a member satisfies the
  structural, cryptographic, economic and rule-level conditions required to proceed; it does not
  evaluate whether the issuer's declarations are true, and it does not make them true (Section 13).
  Its unit is the settlement leaf, not the submission set (`independence.proof/1` §6)
- **fixation path** means the sequence of steps by which one leaf is fixed, from acceptance of its
  members to the point where fixation is complete. It ends where the substrate's part begins:
  settlement, finality and capacity consumption are outside it, and the whole end-to-end sequence
  including them is the independence path (`independence.proof/1` §7.8)
- **submission set** means the canonical execution request transporting one or more autonomous commitments
- **member** means one commitment carried in a submission set, evaluated independently
- **submission set identity** means the deterministic identifier of the transported set (`submission_set_id`, §8.3), used for idempotency and bound by the transporting operator's possession proof; it is NOT the value the proof or settlement anchors
- **set-level precondition** means one of the conditions of §8.1 and §9.4, which concern the set as a whole and are decided once for it
- **accepted subset** means the members that passed per-member validation and entered a fixation path
- **settlement leaf** means the accepted subset of one submission set (§9.3), whose Merkle root over its members' `commitment_id` values (`subtree_root`) the proof anchors (see independence.proof/1 §10.4 and settlement.binding/1 §7)
- **commitment replay identity** means the digest of what the holder signed for one commitment (`capacity.evidence/1` §7.2), the key on which replay and exclusivity are enforced (§9.1)
- **structural validation** means validation of protocol, integrity, coherence, binding, scope, and rule conformity that CERTCRYPT can check mechanically
- **complete verification** means later verification against original material, certificates, verification package material, and public rules
- **positive independence completion** means successful completion of the independence path for an accepted member, culminating in a canonical `independence_proof`

### 6.1 Subject-level orthogonality

`submission-set/1` operates at submission and fixation level. It does not constrain subject-level structure beyond the per-member declarations the applicable rules require.

---

## 7. Member composition

### 7.1 Canonical member composition

A member's canonical transport representation MUST contain exactly the following fields, and no others:

- `capacity_evidence` — the issuer-signed `capacity.evidence/1` artifact for this commitment. It carries the projected commitment, the projected authorization, the operation-scoped pseudonyms, and the public `operation_salt` under which those pseudonyms were derived. Every object inside it is closed as `capacity.evidence/1` and `holder-keyset.merkle-sha3-256/1` §11 define it.
- `operative` — the cleartext operative context, an object containing exactly `holder_id` and `pool_id`, each a non-empty string of printable ASCII.

A conforming producer MUST NOT introduce fields outside this set. A conforming consumer MUST reject a member carrying additional fields, at any depth, since the canonical representation is the preimage of `submission_set_id` (§8.3) and an unconstrained member makes that identifier irreproducible across implementations. Because a member that does not have this exact shape leaves the set without a reproducible identity, that rejection is a set-level precondition (§9.4), not a per-member outcome.

### 7.2 Why `operative` is carried in clear

`capacity_evidence` identifies the holder and pool only as operation-scoped pseudonyms, derived from the stable identifiers under `operation_salt`. Pseudonym derivation is one-way: a consumer holding only the evidence cannot determine which capacity account the operation consumes from. `operative` supplies exactly that routing fact, and nothing more.

Carrying it in clear does not weaken the projection, because it is not accepted on assertion. A consumer MUST re-derive the holder and pool pseudonyms from the cleartext `operative` values under the evidence's own `operation_salt`, and MUST reject the member when either derived value differs from the corresponding pseudonym in the signed evidence. The relayed operative therefore cannot diverge from what the issuer signed, and a transporting operator cannot redirect consumption to another account.

The disclosure is also bounded: `(holder_id, pool_id)` is integration-scoped context already established at onboarding between the issuer and CERTCRYPT. It says which integration is operating, never what is being certified.

### 7.3 No issuer-chosen member label

The canonical member carries no issuer-chosen identifier for the certificate, and a conforming producer MUST NOT introduce one.

Such a label would be the only value in the member selected freely by the issuer and describing the certified fact rather than the operation, and it would enter the `submission_set_id` preimage — a value derived from data the protocol does not need and cannot verify.

It is also unnecessary. The three purposes such a field could serve are met without it:

- **Per-member correlation of request to outcome** is carried by the member's position in the transported set (its zero-based index in `certificates`), which every outcome reports (§11). The issuer maps that position to whatever local identifier it keeps; that mapping stays with the issuer.
- **Replay and exclusivity** are enforced on the commitment, not on any label (§9.1). That enforcement is cryptographic, holds across sets, operators and time, and does not depend on an issuer-supplied value.
- **Within-set duplicate detection** by label would be neither sufficient nor necessary: a producer resubmitting the same commitment is caught by §9.1 regardless of labeling, and distinct labels on the same commitment would defeat a label-based check while §9.1 still holds.

An issuer that needs a human-meaningful reference for its own records keeps one locally, associated with the member position or with the returned operation identifier.

---

## 8. Submission set envelope and identity

A submission set is one JSON object, its envelope (§8.2), carrying the members of §7 and a deterministic identity, `submission_set_id` (§8.3).

`submission_set_id`:

- MUST be reproducible by any implementation from the envelope alone (§8.3)
- MUST serve as the idempotency anchor together with the caller's request identifier: a resubmission of the same set under the same request identifier resolves to the original outcome, and the same set under a different request identifier is refused as a duplicate (§9.4)
- is the value the transporting operator's possession proof binds, together with the request identifier (§9.4)
- MUST NOT be anchored by an `independence_proof` or by settlement; those anchor the per-leaf `subtree_root` (§10)

The submission set identity covers the transported set, including members that are subsequently rejected. It is therefore distinct from any settlement leaf's `subtree_root`, which covers only an accepted subset.

### 8.1 Set cardinality bound

A conforming submission set MUST contain at least one member and at most **64** members. The lower bound (≥ 1) follows from a set being a settlement-leaf grouping that needs at least one commitment; the upper bound is a fixed protocol constant:

```text
MAX_SUBMISSION_SET_MEMBERS = 64
```

The upper bound keeps a set of zero-data members, each carrying post-quantum signature material, within request sizes that common transports accept, so an oversized set gets the actionable set-level rejection defined here rather than a transport-level error.

#### Member byte-size is bounded and independent of subject content

A submission-set member transports a `capacity.evidence/1` — never a base certificate and never subject content. The certified subjects live in the issuer's base certificate, which is reduced to a single `certificate_commitment_digest` inside the evidence; a collection subject (`subject.collection/1`) is likewise reduced to one digest plus its `declared_cardinality` integer. Consequently a member's transported size is bounded by fixed-size cryptographic material (the post-quantum and classical component public keys and signatures, the per-operation pseudonyms, and the holder-key-set Merkle inclusion proof whose length grows only with the logarithm of the holder key set) and does **not** grow with the number of subjects in a certificate, nor with a collection's declared cardinality. The member cap therefore bounds the submission payload directly; no separate per-certificate subject-count limit is required by this profile to keep the payload finite. (Limits on subject count or on `declared_cardinality` for reasons other than transport size — capacity accounting, base-certificate size in a `verification-package/1` — are the concern of the profiles and specifications that govern those artifacts, not of this cardinality bound.)

The bound is normative and fail-closed. A submission set whose member count exceeds `MAX_SUBMISSION_SET_MEMBERS` MUST be rejected **as a whole**, before any per-member evaluation (§9) and before any capacity is consumed. This is distinct from the per-member rejection model of §9: an over-cardinality set is malformed at the set level, so the partial-acceptance rule does not apply — the entire set is refused with an actionable reason.

The bound exists to keep set assembly, identity computation, per-member evaluation, and the settlement-leaf `subtree_root` (§10) bounded in cost, and to prevent a single oversized request from exhausting acceptance-path resources. It is a property of `submission-set/1`; a future version MAY revise the constant under a new version identifier, but MUST NOT remove the requirement that a finite, declared maximum exists.

Every producer and every acceptor on the path MUST enforce this bound: the assembling component (issuer SDK or node) MUST refuse to construct a set larger than the maximum, and the accepting component (the fixation service's submission endpoint) MUST independently reject one. Enforcement at the producer is an ergonomics and fail-fast measure; enforcement at the acceptor is the authoritative, fail-closed gate.

### 8.2 Envelope

A submission set MUST be a JSON object with exactly the following members, and no others:

| Member | Value |
|---|---|
| `schema` | the string `submission-set/1` |
| `system_id` | the system identifier of the system domain the set is submitted under (`system-domain/1`); `certcrypt` for the active registry entry |
| `rules_version` | the rules domain version every member is evaluated under (`rules-domain/1`) |
| `system_root_fingerprint` | the system domain's root fingerprint, 64-character lowercase hexadecimal |
| `submission_set_id` | the set identity (§8.3), as 64-character lowercase hexadecimal |
| `closure_time` | the instant the producer closed the set: an RFC 3339 timestamp in UTC with the `Z` designator and whole seconds, with no fractional part |
| `certificates` | a JSON array of 1 to 64 members (§8.1), each exactly as §7.1 defines |

Homogeneity: every member's `capacity_evidence.projected_commitment` and `capacity_evidence.projected_authorization` MUST carry the envelope's `rules_version` and `system_root_fingerprint`. A set is evaluated under one rules domain and one system domain, never a mixture.

`closure_time` is the issuer side's declaration of when the set closed, the value the fixation service compares against each member's `expires_at` at admission (`capacity.commitment/1` §11.2) and the value the derived proof carries (`independence.proof/1` §10.4.3). It is not a time seal and carries no temporal authority of its own. Whole seconds are required so that every implementation serializes it, and therefore digests it, identically.

### 8.3 Identity derivation

`submission_set_id` is computed as:

```text
submission_set_id = lowercase_hex( SHA3-256( RFC8785-JCS( envelope without submission_set_id ) ) )
```

The preimage is the envelope object of §8.2 with the `submission_set_id` member removed and every other member present — `schema`, `system_id`, `rules_version`, `system_root_fingerprint`, `closure_time` and `certificates`, each member's `capacity_evidence` and `operative` included in full — serialized under the JSON Canonicalization Scheme ([RFC 8785](https://www.rfc-editor.org/rfc/rfc8785)), which sorts object members lexicographically. SHA3-256 is CCCP/1 §7.1.

A receiver MUST recompute `submission_set_id` from the received envelope and MUST refuse the set when the result differs from the carried value (§9.4).

The identity covers the members' signatures. ML-DSA-65 signatures are hedged, so two assemblies of the same commitments with freshly made signatures have different identities; the identity names one transported set, not the commitments it carries. What names a commitment is its replay identity (§9.1).

### 8.4 Test vector

The conformance suite pins this derivation: `fixtures/primitives/submission-set/` carries a complete envelope (`artifacts/submission-set.json`) whose embedded signatures are fixed placeholder values, so that the identity is reproducible, together with its `expected_submission_set_id`. A conforming implementation recomputes that value from that envelope byte for byte. The placeholder evidence is not a valid chain; the vector pins the identity derivation only.

---

## 9. Per-member acceptance model

Once the set-level preconditions hold (§8.1, §9.4) and the set's capacity verdict admits it (§11.2), the fixation service MUST evaluate each member of the submission set independently. For each member it MUST validate the cryptographic bindings of its chain (the Level-1 anchoring of its authorization, the membership of its operation key, the holder's signature over its commitment, and the operation-scoped pseudonyms re-derived from its `operative` context, §7.2), the existence of the authorization it references, the dual temporal condition, replay and exclusivity (§9.1), and all other mechanically verifiable per-member rules defined by the architecture.

A member MUST be accepted if and only if it passes every applicable per-member rule. A member that fails any applicable rule MUST be rejected individually with an actionable reason.

The fixation service MUST NOT reject an otherwise-valid member because a different member of the same submission set failed a per-member rule. The accepted subset is exactly the members that individually passed.

### 9.1 Replay and exclusivity per member

Replay resistance and capacity exclusivity MUST be enforced per member. A member whose commitment was already consumed, is already claimed by another in-flight attempt, or was already submitted, MUST be rejected individually as a replay; it MUST NOT cause the rejection of other members.

A commitment is identified, for replay and exclusivity, by what its holder signed: its commitment replay identity, the SHA3-256 digest of its projected commitment's signing bytes (`capacity.evidence/1` §6.1, §7.2). The fixation service MUST enforce replay and exclusivity on that identity, across submission sets, operators and time. It MUST NOT enforce them only on the evidence digest (`commitment_id`), on the transported bytes, or on anything else that covers material no signature covers: the operation-key disclosure is unsigned and its `tree_size` is not committed to by the holder key set root (`holder-keyset.merkle-sha3-256/1` §11.4), so one signed commitment can travel in evidences with different bytes and different `commitment_id` values, each verifying offline. A second evidence carrying an already-submitted signed commitment is a replay, whatever its `commitment_id`.

### 9.2 Empty accepted subset

If no member is accepted, the submission set forms no settlement leaf and produces no fixation. This is an operational outcome reported per member, not a single set-level error: each member carries its own rejection reason.

### 9.3 Leaf grouping

The accepted subset of one submission set forms exactly one settlement leaf. Its bound value is the `subtree_root` over its members' `commitment_id` values (§10).

All members of a leaf share one issuer scope, because a set whose members resolve to more than one issuer is refused as a whole (§9.4). A leaf MAY carry members under different capacity authorizations of that issuer: the settlement material then carries one authorization-to-consumption bridge per distinct authorization in the leaf, and a verifier selects, for each member, the bridge whose resolved authorization digest matches that member's evidence, as the selected settlement profile and the rules domain define it (§16.1).

### 9.4 Set-level preconditions

The following conditions concern the set as a whole. The fixation service MUST evaluate them before any per-member evaluation and before any capacity is committed, and MUST refuse the whole set, with one actionable reason and nothing persisted for any member, when any of them fails. This list is closed: a failure not listed here MUST be handled per member (§9, §12) and MUST NOT refuse the set.

1. **Envelope and identity.** The set is exactly the envelope of §8.2, with 1 to 64 members (§8.1), each member exactly as §7.1 defines it at every depth, and its `submission_set_id` recomputes (§8.3). A member that does not parse into its closed shape leaves the set without a reproducible identity, so it refuses the set.
2. **One rules domain, one system domain.** Every member carries the envelope's `rules_version` and `system_root_fingerprint` (§8.2), and that `rules_version` is one the fixation service settles and still supports at the time of submission. A rules version outside that set, or past its support window, cannot reach finality under this service and MUST be refused.
3. **Recognized operator.** The operator transporting the set is recognized by the fixation service and proves possession of its operator key over the request identifier and the `submission_set_id`. How the fixation service recognizes operators is internal to it; this specification publishes no registry of them. What reaches the verifier is the attestation the derived proof may carry (`independence.proof/1` §10.15), signed by the system domain and verifiable offline.
4. **One issuer.** Every member's authorization that the fixation service knows resolves to the same issuer, and at least one does. A set is fixed for one issuer; members of several issuers belong in several sets.
5. **Holder binding.** Each member's `operative.holder_id` is the holder its authorization was issued to. A set whose accounting identity disagrees with what was signed is refused rather than attributed to either.
6. **Issuer standing.** The issuer the set resolves to is admitted to fixation by the fixation service at the time of submission.
7. **Idempotency.** A request identifier already used for different content is refused as a conflict; the same set already submitted under another request identifier is refused as a duplicate. A resubmission of the same set under the same request identifier is not a refusal: it resolves to the original outcome. An `insufficient_capacity` verdict (§11.2) leaves no outcome to resolve to, so a resubmission after it is evaluated afresh.
8. **Settlement path.** Where the fixation service lets the caller elect a settlement path for the set, the elected path exists and can close before the earliest `expires_at` among the members; a path that cannot is refused here rather than accepted into a settlement that would have to expire.

The capacity verdict (§11.2) is decided after these preconditions and also concerns the set as a whole.

---

## 10. Relationship to settlement and proof

The submission set itself is not anchored by settlement or by an `independence_proof`. Each settlement leaf formed from the accepted subset is anchored by its `subtree_root` — the Merkle root over the `commitment_id` values of the accepted members of that leaf.

A member's `independence_proof` binds, through the hybrid emission binding (independence.proof/1 §7.10), the member's base certificate to its commitment, and that commitment's inclusion into the leaf's `subtree_root`. The `submission_set_id` plays no role in that anchoring chain.

---

## 11. Outcome classes

A submission produces either one set-level outcome (§11.2), when a set-level precondition fails or the set's capacity verdict refuses it, or a per-member outcome for each transported member. For each member, the per-member outcome MUST be exactly one of:

- **accepted** — the member passed per-member validation and entered a fixation path; an operation identifier MUST be returned for it
- **rejected** — the member failed per-member validation; an actionable reason MUST be returned for it
- **replay_detected** — the member's commitment was already consumed, already claimed, or already submitted (§9.1; a specialization of rejection with a distinct reason)

When members were evaluated, the submission response MUST carry the per-member outcomes such that a caller can determine, for every member it submitted, whether that member was accepted (and its operation identifier) or rejected (and why). The response MUST NOT collapse a partially-accepted set into a single set-level pass or fail that hides per-member outcomes. A set-level outcome is returned only when no member was evaluated.

Acceptance of a member MUST NOT be interpreted as `Independent`. The positive independence result for a member is the member's `independence_proof`, produced later on the independence path.

### 11.1 Terminal outcome after acceptance

An accepted member's fixation attempt MUST NOT remain open indefinitely. It MUST end in exactly one terminal outcome:

- **independent** — the positive path completed; the member's `independence_proof` was produced under the applicable rules
- **expired** — the positive path can no longer complete under public rules, and nothing was consumed for the member; an actionable reason MUST be returned for it

The canonical case of **expired** is a member whose capacity commitment would expire before its settlement could reach finality. `settlement.binding/1` makes a settlement whose final inclusion time is after the commitment's `expires_at` (`capacity.commitment/1` §11.2) fail validation, so the implementation MUST NOT broadcast that settlement and MUST classify the member as expired instead of leaving it accepted-for-processing.

The other case is a fixation attempt the fixation service cannot complete from the material it accepted — an internal fault that the checks made at acceptance are meant to make unreachable. It also ends **expired**, with a reason that names the fault, because the member passed validation when it was accepted and nothing was consumed for it.

An **expired** outcome:

- is an outcome of the fixation attempt, not a certificate state. The certificate remains `Issued`; it MUST NOT be presented as invalid, revoked, or as a third public certificate state between `Issued` and `Independent`
- MUST NOT be presented as a validation failure or as **rejected**: the member passed per-member validation when it was accepted
- consumed no capacity; any capacity committed for the member MUST be released
- does not prevent the same certificate from becoming `Independent` later, but only through a new submission with a fresh capacity commitment under a valid authorization

### 11.2 Set-level outcomes

A set-level outcome is one answer for the whole set. No member is evaluated, nothing is persisted for any member, and no capacity is committed. It is exactly one of:

- **refused** — a set-level precondition failed (§8.1, §9.4); an actionable, deterministic reason naming the failed precondition MUST be returned
- **insufficient_capacity** — the issuer's capacity at the time of submission does not cover what the set requires. The verdict MUST carry `required` (the capacity the set requires), `available` (the capacity the issuer can cover at the time of submission) and `missing` (the difference), as decimal strings

`insufficient_capacity` is evaluated once the preconditions of §9.4 hold, before any member is persisted, over the whole set. It is the only capacity information the fixation service returns to an issuer: the protocol defines no capacity read outside this verdict, and `available` appears only alongside a refusal. The same set MAY be submitted again once capacity has been added; nothing from the refused submission is held.

---

## 12. Fail-closed conditions

The fixation service MUST reject a member, individually, when any of the following holds for that member:

- a broken or unverifiable cryptographic binding in the member's chain, including operation-scoped pseudonyms that do not re-derive from its `operative` context
- an authorization the fixation service does not know
- failure of the dual temporal condition
- replay or exclusivity violation (§9.1)
- any other mechanically verifiable per-member rule failure defined by the architecture

The structural and schema conditions of a member, and its holder binding, are set-level preconditions (§9.4), and capacity is a set-level verdict (§11.2); neither is a per-member outcome.

A rejection MUST carry an actionable, deterministic reason. A member rejection MUST NOT be silent, and MUST NOT be inferred from the absence of an accepted outcome: when members were evaluated, every submitted member MUST receive an explicit outcome.

---

## 13. Declarative integrity and economic commitment

This section defines the declarative-integrity and economic-commitment doctrine for the per-member submission-set model. The unit it governs is the per-leaf accepted subset (the settlement leaf), not the transported set.

### 13.1 Commitment model

When the applicable public rules require an economic commitment for a settlement leaf, the field name `cost_commitment`, where used, MUST be interpreted as a cryptographic commitment to the protocol-valid economically relevant assertion set used by public economic rules.

`cost_commitment` MUST NOT be interpreted as evidence that CERTCRYPT recomputed the semantic truth of the underlying asserted properties from the original material.

`cost_commitment` MUST bind at least:

- the exact `subtree_root` of the settlement leaf
- the applicable economic rule or metric schema identifier
- the economically relevant assertion set accepted by the protocol for fixation
- the canonicalization or serialization domain used for that commitment

`cost_commitment` is a structural artifact.

It MAY commit issuer-declared values, but it is not itself an issuer declaration and therefore MUST NOT use the `declared_` prefix.

Acceptance of a valid `cost_commitment` MUST NOT be interpreted as confirmation that the committed economic assertions reflect the actual properties of the original material. It MUST also NOT be interpreted as license to move those economically relevant declarations out of the committed artifact path and into an authoritative but unbound API-side parameter layer.

### 13.2 Canonical preimage

The requirements in §13.1 fix what `cost_commitment` MUST bind. This section fixes the exact preimage so that an independent producer and an independent verifier derive byte-identical commitments.

`cost_commitment` MUST be computed as the SHA3-256 digest, lowercase-hex encoded, of the canonical preimage object serialized under JSON Canonicalization Scheme (JCS, [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785)). JCS is REQUIRED here — and distinguished from the insertion-ordered serialization used by the settlement leaf and batch-binding preimages — because `cost_commitment` is a structural commitment artifact in the same family as the capacity-commitment artifacts, not a Merkle-tree preimage.

The canonical preimage object MUST contain exactly the following members, and no others:

- `v` — the preimage version tag. For this revision the value is the string `cccc1`.
- `subtree_root` — the exact `subtree_root` of the settlement leaf (the Merkle root over the leaf's accepted commitments), lowercase-hex.
- `rule_schema_id` — the identifier of the public ruleset whose economic interpretation governs this commitment. This is the exact `rules_version` in force for the submission set: under the active architecture the versioned rules domain (`rules-domain/1`), not the settlement contract, is the seat of the economic rule and metric schema. A conforming implementation MUST NOT substitute the `settlement_profile_id` here; that identifier selects the settlement contract, not the economic quantity model.
- `economically_relevant_assertion_set` — an object exposing the protocol-valid economically relevant assertion set accepted for fixation, in the exact declarative form required by §13.3. The members present MUST be exactly the set that the rules domain named by `rule_schema_id` recognizes as economically relevant; that membership is a deterministic function of `rule_schema_id` and is derived from the published rules domain, not chosen by the producer. An independent verifier derives the expected membership from the same `rule_schema_id`, not from the received object. Under the primary quantity model the set exposes `declared_effective_units`: the effective declared units are counted **per subject**, where a recognized non-collection subject profile contributes one effective declared unit and a collection subject contributes units derived from its **declared element cardinality** (`declared_cardinality`), never from submission-set composition or member count. Where the rules domain named by `rule_schema_id` also uses canonical-byte guardrails, the set MUST additionally expose `declared_total_canonical_bytes`.
- `canonicalization_domain` — the string `jcs/rfc8785`, naming the serialization domain of this commitment. A verifier MUST treat this as a fixed expected value, not as a producer-selected serialization selector.

All quantitative values inside `economically_relevant_assertion_set` — including `declared_effective_units`, `declared_total_canonical_bytes`, and any other count or quantity — MUST be encoded as canonical decimal strings (or unsigned-integer strings where the rules domain defines the quantity as integral), never as JSON numbers, so that the committed value remains exact and byte-identical under JCS. This follows the same discipline `subject.collection/1` fixes for `declared_cardinality`.

A conforming producer MUST NOT introduce members outside this set, and MUST NOT rely on key order, since JCS sorts members lexicographically. The `economically_relevant_assertion_set` committed here MUST be the same set bound into the accepted leaf, not a separately supplied parameter.

A verifier consuming a settlement profile that carries `cost_commitment` inside a leaf preimage treats the value as opaque beyond the cross-field and leaf-hash checks defined by that profile; recomputation of this preimage is the producer's obligation, and any divergence surfaces as a leaf-hash mismatch under the consuming profile.

### 13.3 Issuer-asserted economic properties and declarative fields

Economically relevant properties carried for a member MAY be asserted by the issuer. Such values MUST be treated as issuer assertions, never as facts validated by CERTCRYPT.

Fields that carry issuer assertions, where used by the rule set, SHOULD use the `declared_` naming prefix so they are structurally distinguishable from CERTCRYPT-computed or protocol-structural fields. A field with the `declared_` prefix MUST be treated as an issuer declaration; a structural commitment artifact (such as `cost_commitment`) MUST NOT use that prefix.

Any economically relevant declarative field required by the applicable rules MUST be cryptographically bound into the accepted leaf (through the `cost_commitment` or an equivalent binding the rules define) and MUST remain part of the canonical artifact path. It MUST NOT be supplied only through a second, unbound API-side or transport channel.

### 13.4 Structural verifiability of assertions

The fixation service MUST validate, where applicable: presence of required declarative economic fields; their canonical structure; their coherence with the rest of the accepted leaf; their cryptographic binding to the exact members being fixed; and issuer attribution where the protocol requires issuer-authenticated declaration material.

The fixation service MUST reject a member whose economically relevant assertion set is malformed, missing when required, inconsistently bound, ambiguously serialized, incompatible with the declared rule set, or inconsistent with the subject-level unit model recognized by the applicable public rules.

The coherence of a declared per-subject quantity with the subject-level unit model is not merely an issuance-time obligation: an Independent-path verifier MUST enforce the effective-declared-units equality against the certified subjects of the base certificate, failing closed under `EFFECTIVE_UNITS_BINDING_VALID` when the declared units understate them. That enforcement, including the offline-verifier rationale (only the verifier holds both the certified subjects and the declared units under the zero-data profile), is specified normatively in `capacity.commitment/1 §13.1.1`.

### 13.5 Consequences of false declared values

False `declared_*` values:

- MUST NOT be treated as semantic truth validated by CERTCRYPT
- MUST NOT, by themselves, invalidate fixation of a member if all protocol conditions required for fixation are satisfied
- MUST remain later checkable during complete verification where the applicable public rules and original material allow such checking

If a `declared_*` value is later shown to be inconsistent with original material under complete verification, that failure MUST NOT be represented as CERTCRYPT having validated the semantic truth of that declaration.

An issuer assertion MAY be materially false while remaining structurally valid. Fixation does not transform issuer assertions into facts; it fixes them into an independently auditable and later verifiable state. Issuer attribution to the declarations fixed into the accepted member MUST remain preserved under the applicable issuance and submission-binding rules, so that a later verification failure of a false issuer assertion remains attributable to the issuer; cryptographic attribution MUST remain intact.

Fixation and verification are distinct outcomes, and the distinction is load-bearing here. That a false `declared_*` value does not by itself prevent fixation MUST NOT be read as leaving it without consequence: where the applicable public rules define an enforcement point for a given declaration, a value inconsistent with the certified material fails there. For `declared_effective_units` that point is the Independent-path verifier, which holds both the certified subjects and the declared units and MUST enforce their equality under `EFFECTIVE_UNITS_BINDING_VALID` (`capacity.commitment/1 §13.1.1`). A member so declared is fixed and remains attributable, and the certificate does not reach `Independent`.

This is what makes the declarative model sound without semantic inspection. An issuer declaring fewer effective units than the subjects it certified — for example to be priced for fewer — does not obtain the same result more cheaply; it obtains a certificate that no conforming verifier accepts. The economic quantity is therefore self-enforcing at the only plane that holds both operands, and CERTCRYPT never inspects the certified material to achieve it.

---

## 14. Capacity enforcement and economic rule application

### 14.1 Public economic application model

The fixation service MAY apply public economic rules to the protocol-valid economically relevant declaration set committed for a member. That application MUST be deterministic.

### 14.2 No semantic recalculation of original-material truth

The fixation service MUST NOT be required to inspect the original material in order to determine whether an issuer's economically relevant declaration is semantically true.

The fixation service MUST NOT recompute "the truth of cost" from original content as a precondition of fixation.

The fixation service MUST NOT guarantee that economically relevant declared values correspond to the actual properties of the original material.

Economic rule application is performed over committed declarations, not over independently validated measurements of the underlying material.

### 14.3 What CERTCRYPT actually checks

For economic enforcement, the fixation service MUST check mechanically:

- that the required declarative fields exist
- that required `declared_*` fields, where used by the rule set, are correctly named and scoped according to the applicable schema
- that they are well-formed
- that they are bound into the accepted member
- that they are attributable where attribution is required
- that they are coherent with the declared rule set
- that required capacity application under public rules can be derived deterministically from them

### 14.4 What CERTCRYPT does not check

For economic enforcement, the fixation service MUST NOT be interpreted as checking:

- whether the original file, message, or subject truly has the issuer-asserted real-world properties
- whether the issuer has described the original material honestly in semantic terms
- whether the issuer's declaration would survive later complete verification against original material

### 14.5 Consequence of economic lies

If the issuer binds a materially false economically relevant declaration into a member and that declaration is structurally valid for fixation:

- The fixation service MAY still apply public economic rules to that committed declaration set if the protocol conditions are satisfied
- later complete verification MAY show that the declaration is unsustainable against original material under public rules
- such later failure MUST NOT be represented as CERTCRYPT having previously validated the semantic truth of that declaration
- such later failure MAY still carry public-rule consequences for economic fairness, reconciliation, regularization, or future authorization eligibility where those consequences are defined outside semantic truth validation

This means a member MAY validly reach `Independent` while later complete verification shows that economically relevant issuer declarations were materially unsustainable. Such a result does not break the structural independence semantics of the member. It does mean that the economically relevant declaration set was not materially sustainable, with whatever later fairness or pricing consequences the applicable public rules define.

---

## 15. Structural validation discipline

CERTCRYPT validates mechanically checkable protocol conditions; it does not perform semantic policing. Every check below is applied per member, against the member's own chain and the accepted leaf it joins.

### 15.1 Binding integrity

The fixation service MUST validate, for each member:

- that the member's declaration and commitment artifacts form one coherent set
- that the member's identity is bound consistently across its artifacts
- that any declarative economic assertion set is bound to the same member
- that any settlement-context binding required by the execution mode remains bound to the same system and issuer scope

A member whose settlement-context binding drifts across system or issuer scope MUST be rejected; binding MUST NOT cross those scopes.

### 15.2 Capacity validity (Authorization lineage, not operational state)

The fixation service MUST validate, for each member:

- that the referenced capacity authorization material exists where required by the applicable model
- that it is valid for the same system and issuer scope
- that it is applicable to the member under the public economic rules
- that the required capacity derived from the protocol-valid economic assertion set does not exceed what the member is authorized to use
- that no local balance snapshot, cached availability state, dashboard view, API response, or node-internal accounting surrogate is being treated as authoritative capacity evidence in place of the referenced authorization material

Acceptance MUST depend on publicly interpretable authorization material under the applicable rules domain, not on trust in node-local operational state. If capacity applicability or sufficiency can be established only by trusting manipulated, local-only, or non-portable operational state, the member MUST be rejected.

Node-local caches, retry queues, optimistic reservation views, or other operational estimates MAY exist for performance or coordination, but they MUST NOT be treated as establishing "almost valid" capacity if that apparent availability cannot be reproduced from the referenced authorization lineage under the same public rules. If local operational state and publicly interpretable authorization lineage diverge, the lineage governs and any apparent local sufficiency MUST be discarded as non-authoritative.

### 15.3 Rule-domain exactness

The fixation service MUST validate, for each member:

- that the member conforms to the declared public rule set
- that required economic declarations for that rule set are present, structurally valid, and correctly bound
- that the protocol-accepted economic rule application can be executed deterministically on the committed assertion set
- that the rules domain actually applied during fixation is exactly the declared `rules_version` or its deterministically bound equivalent

The fixation service MUST NOT accept a member if the declared `rules_version`, the effective fixation rules domain, and the rules domain required for the derived `independence_proof` could diverge. The rules domain applied during fixation MUST be exactly the same rules domain that governs any derived `independence_proof`. The fixation service MUST NOT interpret rule conformity as semantic confirmation of the truth of the issuer's original-material assertions.

### 15.4 Subject-level orthogonality and cardinality

`submission-set/1` operates at submission and fixation level and MUST remain orthogonal to subject-level collection semantics such as [subject.collection/1](../../../../profiles/subject.collection/1/index.md). Accordingly:

- a submission set MAY carry members whose declared subjects are collection subjects
- a submission set MUST NOT be interpreted as a collection merely because it carries multiple members or multiple collection subjects
- submission-set-level aggregation MUST NOT, by itself, create, replace, or redefine subject-level declared cardinality
- acceptance of a member for fixation MUST NOT be interpreted as converting the submission set into a subject-level declarative structure

Where the applicable rules domain uses issuer-declared economically relevant properties derived from subject structure, those properties MUST still be declared and bound under the applicable subject and member rules rather than inferred from submission-set aggregation alone.

---

## 16. Settlement and fixation discipline

### 16.1 Settlement profile completeness

Every positive independence path derived from an accepted member MUST be governed by one exact `settlement_profile_id` under the same exact `rules_version`. That settlement profile MUST define, under public rules:

- one exact settlement mode
- one exact settlement-material contract
- one exact finality profile sufficient for canonical acceptance
- one exact leaf-assignment interpretation
- one exact capacity-consumption interpretation
- one exact authorization-to-consumption bridge

A member MUST fail closed for any positive path if the selected `settlement_profile_id` does not fully define all of the above. No implementation MAY accept a member and later rely on node-local memory, discretionary settlement-adapter behavior, managed-service interpretation, or post-hoc operational reconstruction to supply missing settlement-proof semantics for canonical `Independent`.

### 16.2 Finality and operational ambiguity

No positive independence completion derived from an accepted member MAY be treated as final unless the applicable settlement evidence satisfies the relevant finality rule, fully defined by the exact applicable rules domain and never supplied by implementation-local policy, heuristic defaults, or ad hoc shortcuts. If settlement finality is delayed or probabilistic, implementations MAY expose operational internal states, but those states MUST NOT be treated as `Independent`, MUST NOT be represented as canonical independence results, and MUST NOT create a new public certificate state between `Issued` and `Independent`.

When an implementation exposes an operational state, the state MUST be distinguishable from `Issued` and `Independent`, and replaying the same request identifier with the same content MUST resolve idempotently to the original outcome. Operational states MUST NOT weaken the finality requirements above or supply evidence that the canonical artifacts do not carry.

### 16.3 No trust-anchor shortcut; execution is not semantic result

CERTCRYPT signatures, API responses, dashboards, managed copies, transport acknowledgments, or submission receipts MUST NOT be treated as substitutes for valid settlement, valid finality, or a canonical `independence_proof`.

Execution of fixation MUST NOT be interpreted as semantic validation of a member or of its declared properties. A successful execution path does not imply that issuer assertions are true, that economic declarations reflect actual material properties, or that the member would pass complete verification against original material. Execution only determines whether the member satisfies the structural, cryptographic, economic, and rule-level conditions required to proceed toward a valid independence result under public rules.

---

## 17. Output and response discipline

### 17.1 Synchronous-first response contract

When an implementation exposes the submission surface through a request-response integration as the primary happy-path API, that implementation SHOULD behave as a synchronous-first endpoint. Under that model:

- the endpoint SHOULD consume an explicit implementation-defined latency budget before responding
- if sufficient settlement finality for a member's positive path is established within that budget, the endpoint SHOULD return either the member's `independence_proof` or the exact authoritative result material from which it is deterministically derived under public rules
- if sufficient settlement finality is not established within that budget, the endpoint MAY return, for that member, an accepted-for-processing classification together with one exact stable retrieval identifier for the fixation attempt

Where such an endpoint accepts a canonical submission set as its primary request body, it SHOULD present that set and its members as the authoritative submission unit. It SHOULD NOT reframe mandatory economically relevant declarations as first-class billing knobs separate from the committed member path when those declarations normatively belong inside it. No implementation MAY return a positive `Independent` result for a member before sufficient settlement finality exists under the selected `settlement_profile_id`, treat a transport/queue/batch acknowledgment or managed-service promise as a substitute for canonical positive completion, or block indefinitely merely to avoid returning an accepted-for-processing classification.

### 17.2 Processing classification semantics

When an implementation returns accepted-for-processing for a member under a synchronous-first model, the response MUST remain operational only: it MUST NOT declare `Independent`, MUST NOT create a third public certificate state between `Issued` and `Independent`, and MUST NOT require the client to interpret internal queue, batch, or settlement machinery to preserve semantic correctness.

Such a per-member response MUST include one exact stable retrieval identifier for the member's fixation attempt. The members of one set accepted together form one leaf (§9.3) and MAY share that identifier. The response is not required to carry the leaf's `subtree_root`: the leaf is composed after acceptance, and its `subtree_root`, together with the `rules_version` and the settlement reference it was fixed under, is carried by the member's `independence_proof` once the attempt completes. The `rules_version` is the one the set declared (§8.2), and the settlement profile is the one that rules version selects.

An accepted-for-processing classification MUST eventually resolve, through that retrieval identifier, to one of the terminal outcomes of §11.1: to the member's `independence_proof`, or to `expired` with its reason.

### 17.3 Retrieval guarantees

Retrieval by the stable identifier MUST return the current classification of the attempt and, once it is terminal, its terminal outcome; repeating it MUST NOT change that outcome. A fixation service SHOULD also let an issuer that lost the identifier recover the outcome from the member's `certificate_commitment_digest`, under the same issuer authentication.

Secondary retrieval mechanisms (webhook delivery, push delivery) MAY exist as convenience layers over the same fixation result. They MUST NOT alter the canonical positive artifact, the fail-closed meaning of submission, or the rule that only sufficient settlement plus canonical proof material may produce `Independent`.

This specification defines these guarantees, not a transport. It fixes no HTTP routes, status codes or bodies for the fixation service. The interface an issuer-side node exposes to its issuers is described informatively by that node's interface description (§20); it is not a normative part of this protocol.

---

## 18. Offline verification and non-authority

### 18.1 Offline principle

Complete verification against original material MAY require the original material, but it MUST NOT require live CERTCRYPT authority. The verifier MAY use original material after fixation; CERTCRYPT is not required to inspect that original material during fixation.

### 18.2 Non-authority clause

A submission (of a set or of any member within it):

- MUST NOT be interpreted as validation of certificate content
- MUST NOT imply endorsement by CERTCRYPT
- MUST NOT imply that CERTCRYPT semantically audited issuer declarations
- MUST NOT alter base certificate validity
- MUST NOT by itself prove `Independent`

It only represents a request to execute fixation for the transported members under valid protocol conditions, evaluated per member.

---

## 19. Security considerations

- submissions MUST preserve zero-data constraints
- the fixation service MUST NOT be required to inspect original payload material during fixation
- replay MUST be prevented at the per-member commitment replay identity — what the holder signed (§9.1) — not at the level of the evidence bytes, the evidence digest, or the transported bytes
- post-acceptance mutation of a member's bound material MUST be rejected deterministically
- parser ambiguity and version downgrade MUST fail closed
- capacity authorization MUST remain scope-bound
- settlement drift across member, issuer, or system contexts MUST be rejected
- side-channel leakage SHOULD be minimized in retries, logging, and operational metadata

Additionally:

- false issuer declarations MUST NOT become semantic truth merely because fixation succeeded
- false issuer declarations MAY become irreversibly fixed and later verifiably unsustainable under complete offline verification
- no managed-service response MAY become the source of truth for independence

---

## 20. References

- [independence.proof/1](../../../../models/independence.proof/1/specification.md)
- [settlement.aggregated.xrpl/1](../../../../ecosystem/settlement/settlement.aggregated.xrpl/1/specification.md)
- [settlement-material/1](../../../../ecosystem/settlement/settlement-material/1/specification.md)
- [settlement.binding/1](../../../../ecosystem/settlement/settlement.binding/1/specification.md)
- [capacity.commitment/1](../../../../ecosystem/settlement/capacity.commitment/1/specification.md)
- [capacity.evidence/1](../../../../ecosystem/settlement/capacity.evidence/1/specification.md)
- [holder-keyset.merkle-sha3-256/1](../../../commitment/holder-keyset.merkle-sha3-256/1/specification.md)
- [CCCP/1](../../../CCCP/1/specification.md)
- [system-domain/1](../../../../foundation/system-domain/1/specification.md)
- [rules-domain/1](../../../../foundation/rules-domain/1/specification.md)

Informative:

- Issuer-side node interface description (OpenAPI), [`openapi/node.openapi.yaml`](https://github.com/CERTCRYPT/certcrypt-node/blob/main/openapi/node.openapi.yaml) in the `certcrypt-node` repository. It describes how one node implementation exposes submission, per-member outcomes, set-level verdicts and retrieval to its issuers. It is an implementation's interface, not part of this protocol.
- [subject.collection/1 — CERTCRYPT Collection Subject Canonicalization Profile](../../../../profiles/subject.collection/1/index.md)
- [verification-package/1 — CERTCRYPT Verification Package Specification](../../../../ecosystem/verification/verification-package/1/index.md)
