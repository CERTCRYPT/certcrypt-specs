# CERTCRYPT Consistency Verification Protocol (CCVP/1)

**Identifier:** CCVP/1

**Label:** CCVP v1

**Type:** Protocol

**Status:** Frozen · optional verification plane, outside the `Issued` and `Independent` path

**Layer:** Layer 1 — Protocols

**Depends on:**

- [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../CCCP/1/index.md)
- [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../CCSP/1/index.md)
- [composite-signature/1 — CERTCRYPT Composite Signature Profile](../../../foundation/composite-signature/1/index.md)
- [subject.context-snapshot/1 — CERTCRYPT Context Snapshot Subject Canonicalization Profile](../../../profiles/subject.context-snapshot/1/index.md)

**Naming convention:**
`CCVP/1` is the **formal protocol identifier**.
`CCVP v1` is the **human-readable label**.  

**Audience:** Protocol implementers, verifiers, consistency auditors  

**Purpose:** Define how issuance declared context is represented and verified in CERTCRYPT using certified context snapshots.

**Intended use:** Offline, time-bound consistency verification based on certified issuance declared context, without central authorities, APIs, CRLs, or online validation services.

**Scope:** Defines declared context certificate semantics, context snapshot structure, issuer and key consistency entries, snapshot selection logic, and consistency verification outcomes.

**Non-goals:** CCVP/1 does not issue fact certificates, does not validate facts, does not provide real-time consistency services, and MUST NOT be interpreted as a certificate authority (CA), trust service, decision service provider, or legal validation mechanism.

> This document is **normative**.
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative.

---

CCVP/1 is a **declarative consistency-verification protocol** that defines how to represent and verify **historical issuance context** in CERTCRYPT using **certified context snapshots** ([CCSP/1](../../CCSP/1/index.md) certificates whose payload describes a declared context at an effective time).

CCVP/1 defines:

- **The declared context object:** the meaning of a context snapshot as a **signed historical declaration** (not as a service).
- **The declared context model:** how a snapshot declares *who* (issuer identity) and *what* (composite issuer key, by fingerprint) was in scope, **from when** and **until when**, to **issue** certain certificates.
- **Offline verification:** how a verifier selects the applicable snapshot **by effective time** and computes a consistency outcome (`consistency-match`, `consistency-mismatch`, `consistency-unknown`) without inference.
- **Non-retroactivity:** how consistency outcomes apply **forward only**, preserving long-term auditability without reliance on living infrastructure.
- **Federation without an arbiter:** how multiple declared context sets and snapshot issuers can coexist without any implicit “root” or global precedence.
- **Optional declarative policy references:** how a context snapshot MAY bind external declarative policy artifacts without changing CCVP/1 consistency logic.

CCVP/1 **does not grant authority**.
It defines how declared context is **expressed as signed context** and how structural alignment may be **verified**, leaving acceptance entirely to the verifier (opt-in).

Any implementation, UX surface, or market presentation that turns declared context into a visible trust badge, endorsement marker, or institutional seal is non-conformant with CCVP/1.

Consistency verification MUST NOT be confused with cryptographic verification.
Cryptographic verification establishes authenticity.
Consistency verification establishes alignment with declared context.

> **Canonical definition**
>
> **CCVP/1 verifies whether a certificate issuance is structurally consistent with one declared context at one point in time.**
>
> It does not determine truth, trust, approval, compliance, or authority.
>
> A `consistency-match` means only that the issuance matched the selected declared context under the applicable snapshot-selection rules.
>
> CCVP/1 may expose consistency with declared context, but it does not prove policy compliance.
>
> Different declared contexts may yield different consistency outcomes for the same certificate.
>
> CCVP/1 therefore exposes contextual alignment, not institutional validation.
>
> A single CCVP/1 verification operates against one declared context namespace only.
>
> A verifier MAY run multiple independent CCVP/1 verifications for the same certificate under different declared contexts.
>
> CCVP/1 defines no canonical aggregate outcome across multiple declared contexts.

---

## 0. Conformance, interpretation boundaries, and normative structure

This section defines the **normative reading model**, **interpretation boundaries**, and **structural organization** of CCVP/1.

It establishes **what CCVP/1 declares**, **what CCVP/1 explicitly does and does not decide**, and **the frozen axioms that govern its interpretation**.

This section does not introduce new field-level requirements or validation rules.

All normative rules referenced in this section are defined exclusively in later sections of this specification.

### 0.1 What CCVP/1 expresses (Nuclear definition)

**CCVP/1 declares the act of issuance, not the truth, validity, or effects of the issued certificate.**

A context snapshot declares only this:

> A specific issuer signing key, bound to a specific issuer identity, was eligible during a defined time interval to issue CERTCRYPT certificates within a defined declared context.

Declared context is expressed exclusively through payload-level fields: `C.payload.context`, defined by this specification (Section 5.2), and `C.payload.anchor.subjects[].profile`, defined by [CCSP/1](../../CCSP/1/index.md):

- `C.payload.context.snapshot_issuer_id`
- `C.payload.context.snapshot_issuer_fingerprint_digest_hex`
- `C.payload.context.context_set_id`
- `C.payload.anchor.subjects[].profile`

CCVP/1 is an optional verification plane. Its outcome is reported beside the `Issued` and `Independent` verdicts and never changes either of them (Section 0.3, axioms 3 and 7).

### 0.2 What CCVP/1 does not decide (Non-claims)

CCVP/1 MUST NOT be interpreted as deciding, asserting, or conferring:

- the truth of any certified statement
- cryptographic validity of any certificate
- legal validity, legal effect, or enforceability
- economic compliance, settlement, payment execution, or consideration
- whether a referenced policy was followed
- whether a referenced policy was enforceable
- whether a referenced policy was satisfied in practice
- whether the issuer complied with its own declared policy
- present-time decision applicability (“still applicable now”)
- intent, diligence, or good faith
- retroactive invalidation of previously applicable issuance
- exclusivity of any declared context set
- global authority of any context snapshot issuer
- proximity to `Independent`
- premium validation status
- stronger verification semantics than those defined by the applicable proof and settlement rules
- institutional endorsement or a CERTCRYPT-issued trust status

### 0.3 Frozen axioms

1. **Declarative and opt-in**  
   Verifiers MUST treat context snapshots as signed artifacts they may accept or ignore by policy. CCVP/1 MUST NOT introduce implicit trust anchors.

2. **Historical, not a service**
   Verifiers MUST NOT require network availability to perform CCVP/1 consistency verification.

3. **Does not replace cryptography**  
   Consistency outcomes MUST NOT alter [CCSP/1](../../CCSP/1/index.md) cryptographic verification outcomes.

4. **Non-retroactive**  
   Declared context changes reflected in context snapshots MUST apply only forward from the effective time of the snapshot.

5. **No circular dependencies**  
   CCVP/1 MUST NOT require validation of economics, settlement, or consensus to function, and MUST NOT create protocol circularity.

6. **[CCSP/1](../../CCSP/1/index.md) coherence**  
   CCVP/1 MUST remain compatible with [CCSP/1](../../CCSP/1/index.md) categories and separation of concerns, and MUST NOT redefine envelope, signatures, or [CCSP/1](../../CCSP/1/index.md) semantics.

7. **Consistency is not independence**
   A consistency outcome, including `consistency-match` under any CERTCRYPT declared context namespace, MUST NOT be interpreted as creating, strengthening, approximating, or pre-validating `Independent`.

8. **Consistency is not an institutional seal**
   No context snapshot, `consistency-match` outcome, or consistency-verification result MAY be presented as an institutional endorsement, trust mark, certification tier, or “trusted by CERTCRYPT” style conclusion.

9. **Consistency UX is not a trust surface**
   No verifier UI, widget, dashboard, package viewer, or hosted delivery layer MAY use consistency results, issuer/key alignment, or `consistency-match` status to imply premium trust, endorsement, or proximity to `Independent`.

10. **Consistency is not a ranking system**
   Verifiers, SDKs, dashboards, package viewers, and third-party tooling MUST NOT assign comparative trust, ranking, preference, or quality ordering across context snapshot issuers based solely on CCVP/1 outcomes or namespace presence.

---

## 1. Background & rationale

Traditional centralized authorization systems rely on live authorities and infrastructure (including revocation services) and often support retroactive invalidation. These dependencies introduce operational assumptions that do not hold over long time horizons and undermine offline verification.

CERTCRYPT adopts a different approach:

- cryptographic validity is self-contained
- issuance consistency is verified against a **certified historical context**, not as a runtime service
- consistency outcomes apply **forward only**

CCVP/1 formalizes this model by defining context snapshots as immutable certificates that describe which issuers and keys were eligible at a given effective time. Certificates are verified exclusively against the declared context that existed at issuance time.

---

## 2. Scope

CCVP/1 defines:

- context snapshot identity and structure
- entry semantics for issuer/key consistency
- snapshot selection rules at verification time
- consistency outcomes for verifiers
- the unit of one CCVP/1 verification as one target certificate under one declared context namespace

CCVP/1 does not define:

- certificate envelope structure or serialization rules ([CCSP/1](../../CCSP/1/index.md))
- canonicalization, hashing, or commitment construction ([CCCP/1](../../CCCP/1/index.md))
- a canonical verifier output object
- any canonical aggregate result across multiple declared contexts

All timestamps used for CCVP/1 consistency verification are payload-level data and MUST be interpreted exclusively according to their semantic domain.

Envelope-level metadata timestamps, if present, are informational only and MUST NOT be used for consistency verification, issuer identity binding, context snapshot selection, or any temporal comparison.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

Additional terms:

- **Context Snapshot:** a CERTCRYPT certificate whose payload defines an issuance declared context at a specific effective time.
- **Declared Context Set:** a declared context namespace identified by `S.payload.snapshot.context_set_id`.
- **Entry:** a context record for a specific issuer identity and signing key.
- **Composite key fingerprint:** for an issuer signature under [CCSP/1](../../CCSP/1/index.md) Section 7.4, `SHA3-256(pub_p256_bytes || pub_mldsa_bytes)` encoded as lowercase hexadecimal (Section 8.1).
- **Snapshot issuer identity:** the pair (`signer.id`, composite key fingerprint) of the issuer signature of a context snapshot certificate.
- **Declared context namespace:** the triple (`snapshot_issuer_id`, `snapshot_issuer_fingerprint_digest_hex`, `context_set_id`) declared by a target certificate (Section 5.2).

For the purposes of CCVP/1, the terms *context snapshot* and *declared context snapshot* are equivalent.

---

## 4. Design principles

CCVP/1 is designed around the following principles:

- **Declared-context verification only:** CCVP/1 verifies alignment with one declared context at one point in time. It does not create authority, approval, or compliance.
- **Temporal non-retroactivity:** Snapshot selection MUST be time-bounded and non-retroactive.
- **Deterministic verification:** Given the same certificate, declared context namespace, candidate snapshots, and public rules, conforming verifiers MUST converge on the same consistency outcome.
- **Zero-data by design:** CCVP/1 MUST remain compatible with a zero-data architecture and MUST NOT require retained documents, identities, or platform-held operational records.
- **Proof without data custody:** Consistency verification relies on certificates, context snapshots, and public rules, not on internal CERTCRYPT systems.
- **Institutional independence:** Consistency verification MUST remain possible without the continued existence of any issuer, snapshot publisher, or managed CERTCRYPT service.
- **Infrastructure neutrality:** Different runtimes, transports, or deployment environments MAY carry different artifacts, but they MUST NOT change CCVP/1 meaning.
- **Interpretation boundaries:** CCVP/1 exposes contextual alignment only. It does not prove truth, trust, legal meaning, or semantic validity.

---

## 5. Context snapshot certificate identification

A **Context Snapshot** is represented as a standard CERTCRYPT certificate ([CCSP/1](../../CCSP/1/index.md)) and MUST:

- conform to the [CCSP/1](../../CCSP/1/index.md) envelope
- inherit canonicalization, hashing, and commitment semantics from [CCCP/1](../../CCCP/1/index.md)
- be identifiable as a **context snapshot certificate** for CCVP/1 purposes using payload-level snapshot semantics and subject typing

CCVP/1 defines snapshot typing and collection rules exclusively through `payload.snapshot`, `payload.anchor.subjects`, and the verified issuer signature.

### 5.1 Required snapshot semantics for context snapshot certificates

A context snapshot certificate **S** MUST satisfy all of the following:

1. **S** MUST be `Issued`-valid: its envelope, its issuer signature and its subject profiles verify under the rules domain named by `S.payload.rules_version`, as the `Issued` route of [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md) evaluates any base certificate.

2. `S.payload.snapshot` MUST be present and MUST be a JSON object conforming to Section 6.

3. `S.payload.anchor.subjects` MUST contain exactly one element whose `profile` is `"subject.context-snapshot/1"`, and that element's `commitment_digest_hex` MUST equal the [CCCP/1](../../CCCP/1/index.md) subject commitment of `S.payload.snapshot`:

   `SHA3-256(ASCII(S.payload.anchor.nonce_hex) || ASCII(SHA3-256(canonical_bytes(S.payload.snapshot))))`

   where `canonical_bytes` is defined by [`subject.context-snapshot/1`](../../../profiles/subject.context-snapshot/1/index.md). The commitment is recomputed by the verifier; it binds the snapshot the certificate carries to the subject the issuer signed.

   The [`subject.context-snapshot/1`](../../../profiles/subject.context-snapshot/1/index.md) subject is a classification marker only. It does not represent a certified real-world subject or fact, and MUST NOT be interpreted as asserting truth, occurrence, or evidentiary content.

4. The snapshot issuer identity MUST be derived from the issuer signature of **S** that step 1 verified: `signer.id` and the composite key fingerprint of `signer.pub_p256_b64` and `signer.pub_mldsa_b64` (Section 8.1). It MUST NOT be taken from any field inside `payload`, including `payload.snapshot`.

A certificate that carries neither `payload.snapshot` nor a `subject.context-snapshot/1` subject is not a context snapshot certificate, and CCVP/1 ignores it. A certificate that carries either of them and does not satisfy every requirement above is a **non-conformant context snapshot** (Section 9.1).

### 5.2 Target certificate declared context

When a target certificate **C** intends to participate in CCVP/1 consistency verification, it MUST carry that declared context in:

`C.payload.context`

`C.payload.context` is a JSON object. CCVP/1 defines three members:

- `snapshot_issuer_id` (string): the `signer.id` of the snapshot issuer
- `snapshot_issuer_fingerprint_digest_hex` (64 lowercase hexadecimal characters): the composite key fingerprint of the snapshot issuer (Section 8.1)
- `context_set_id` (non-empty string)

Other members of `C.payload.context` are not defined by CCVP/1 and MUST NOT affect a consistency outcome.

If `C.payload.context` is absent or is not a JSON object, or if any of the three members is absent or not of the type above, CCVP/1 consistency verification for that certificate MUST resolve to `consistency-unknown`.

`C.payload.context` is part of the signed payload of **C**: the issuer of **C** chooses, at issuance, both the declared context set and the key whose snapshots govern it. Naming the snapshot issuer by key fingerprint, not by label alone, is what makes the namespace unforgeable: `signer.id` is an untrusted label ([CCSP/1](../../CCSP/1/index.md) Section 7.4.2) that anyone can put on a certificate signed with their own key, and a namespace keyed by that label alone would let any third party publish snapshots in it.

`C.payload.context` expresses declarative issuance context only.

It MUST NOT be interpreted as:

- proof of settlement
- proof of payment
- proof of compliance
- proof of truth
- proof of `Independent`

CCVP/1 defines one verification unit per declared context namespace.

That namespace is fixed by the exact triple:

- `C.payload.context.snapshot_issuer_id`
- `C.payload.context.snapshot_issuer_fingerprint_digest_hex`
- `C.payload.context.context_set_id`

A verifier MAY execute additional independent CCVP/1 verifications for the same certificate under other declared contexts, but CCVP/1 itself defines no canonical aggregate outcome across those separate verifications.

### 5.3 The target certificate must be `Issued`-valid

CCVP/1 binds entries to the issuer signature that established the issuance authenticity of **C** (Section 8). A target certificate that is not `Issued`-valid has no such signature: CCVP/1 MUST NOT produce `consistency-match` or `consistency-mismatch` for it. A verifier that reports a consistency outcome for such a certificate MUST report `consistency-unknown`, and MUST NOT present it as anything other than the absence of a verification unit.

## 6. Declared context set and snapshot model

Each context snapshot certificate represents one immutable declared-context state belonging to a **declared context set**.

A context snapshot payload MUST include a `snapshot` object whose fields define snapshot identity and content.

The `S.payload.snapshot` object MUST include:

- `context_set_id` (non-empty string)
- `snapshot_id` (non-empty string; ULID RECOMMENDED)
- `issued_at` (timestamp, Section 6.3) — **the effective context time of this snapshot**
- `entries` (array of entry objects, Section 7) — the list of issuance consistency entries for this snapshot (may be empty)

The `S.payload.snapshot` object MAY include:

- `policy_refs` (array, Section 6.2)

Members not defined by this specification are canonicalized with the snapshot ([`subject.context-snapshot/1`](../../../profiles/subject.context-snapshot/1/index.md) Section 9) and MUST NOT affect a consistency outcome.

`S.payload.snapshot` MUST satisfy the preconditions of [`subject.context-snapshot/1`](../../../profiles/subject.context-snapshot/1/index.md): strict JSON with no repeated member name, and no JSON number at any depth. Booleans and nulls are permitted.

`S.payload.snapshot.issued_at` represents the **effective context time** of the context snapshot and is independent from certificate envelope metadata timestamps.

`snapshot_id` identifies the snapshot within its declared context set. It does not take part in selection (Section 9); because it is part of the canonical snapshot bytes, two snapshots that differ only in `snapshot_id` are distinct snapshots.

The `S.payload.snapshot.context_set_id` identifies a declared context namespace and MUST NOT be interpreted as global authority, hierarchy, or precedence.

### 6.1 Declared context namespace interpretation

The value of `S.payload.snapshot.context_set_id` identifies a declared context namespace **only in conjunction with the snapshot issuer identity** (Section 5.1, requirement 4).

Verifiers MUST NOT interpret `S.payload.snapshot.context_set_id` as:

- a globally unique identifier
- a global authority namespace
- a standalone trust anchor

Context snapshots sharing the same `S.payload.snapshot.context_set_id` but signed by different keys MUST NOT be assumed to belong to the same contextual authority, even when their `signer.id` labels are equal.

### 6.2 Policy references

`policy_refs`, when present, identify external declarative policy artifacts associated with the declared context expressed by the snapshot.

Such references are informational and declarative within CCVP/1.

CCVP/1 MUST NOT interpret, enforce, or validate the contents of referenced policy artifacts.

The presence, absence, or contents of `policy_refs` MUST NOT by themselves change a consistency outcome.

`policy_refs` allow a context snapshot issuer to bind one or more external declarative policy artifacts to the declared context at the time of the snapshot.

Each element of `S.payload.snapshot.policy_refs` MUST be an object containing:

- `profile` (string, REQUIRED)
- `commitment_digest_hex` (string, REQUIRED)

This shape is defined so that `policy_refs` can be produced and read consistently. A verifier does not evaluate `policy_refs`: their shape affects neither the conformance of the snapshot nor the verification result.

Each element MAY additionally contain:

- `label` (string)
- `role` (string)

Each `policy_refs` element identifies a referenced subject artifact by `profile + commitment_digest_hex`.

Recommended subject profiles for policy references include:

- `subject.text/1`
- `subject.binary/1`

A policy artifact MAY describe issuer-declared operating conditions, internal issuance practices, container preferences, or other self-declared rules, but CCVP/1 does not determine whether such policies were followed.

Referenced policy artifacts MAY contain issuer-declared constraints, preferences, limits, or operating rules.

Within CCVP/1, such content remains declarative only.

No consistency outcome MUST be upgraded, downgraded, or reinterpreted on the basis of policy text or binary policy artifacts alone.

Illustrative snapshot example:

```json
{
  "context_set_id": "certcrypt-email-issuance",
  "snapshot_id": "01JAFK8Z7V3YJ8T2R6M4N9QW1X",
  "issued_at": "2026-04-12T10:00:00Z",
  "policy_refs": [
    {
      "profile": "subject.text/1",
      "commitment_digest_hex": "<POLICY_TEXT_COMMITMENT_HEX>",
      "label": "issuer-email-policy-v1",
      "role": "issuer-policy"
    }
  ],
  "entries": [
    {
      "issuer_id": "mail.example",
      "pub_fingerprint_digest_hex": "<COMPOSITE_KEY_FINGERPRINT_HEX>",
      "roles": ["issuer"],
      "scope": {
        "subject_profiles": ["subject.email/1"]
      },
      "status": "active",
      "valid_from": "2026-01-01T00:00:00Z",
      "valid_to": null,
      "revoked_at": null,
      "revocation_reason": null
    }
  ]
}
```

### 6.3 Timestamps

Every CCVP/1 timestamp — `S.payload.snapshot.issued_at` and an entry's `valid_from`, `valid_to` and `revoked_at` — MUST be a JSON string in the form [CCSP/1](../../CCSP/1/index.md) Section 7.3.1 fixes for `anchor.issued_at`: [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339) in UTC, `YYYY-MM-DDTHH:MM:SS[.fraction]Z`, uppercase `T` and `Z`, no numeric offset, one to nine fractional digits when a fraction is present, naming a real calendar instant with seconds from `00` to `59`. A timestamp in any other form makes the snapshot that carries it non-conformant (Section 9.1).

Timestamps are compared as **instants**, never as strings. A verifier reads each timestamp as a count of nanoseconds since `1970-01-01T00:00:00Z`, padding the fraction on the right with zeros to nine digits, and compares those counts. `2026-04-12T10:00:00Z` and `2026-04-12T10:00:00.000Z` therefore name the same instant: neither precedes the other, and two snapshots with those effective times tie (Section 9). String comparison is non-conformant: it orders values with different fraction lengths differently from the instants they name, and two verifiers comparing strings could select different snapshots.

---

## 7. Consistency entries

Each context snapshot contains zero or more entries.
Each entry declares the applicability of exactly one issuer signing key for issuance acts within the declared context.

Entries are contained in:

`S.payload.snapshot.entries`

### 7.1 Entry structure

Each entry MUST be a JSON object and MUST contain:

- `issuer_id` (non-empty string)
- `pub_fingerprint_digest_hex` (64 lowercase hexadecimal characters): the composite key fingerprint of the issuer key (Section 8.1)
- `status` (string)
- `valid_from` (timestamp, Section 6.3)

Each entry MAY contain:

- `kid` (string; an ASCII token of at most 128 characters, as in [CCSP/1](../../CCSP/1/index.md) Section 7.4.1)
- `roles` (array of strings)
- `scope` (object, Section 7.3)
- `valid_to` (timestamp or null)
- `revoked_at` (timestamp or null)
- `revocation_reason` (string or null)

An entry that is not a JSON object, lacks a required member, or carries a member defined above with a value of another type or form makes the snapshot non-conformant (Section 9.1). Members not defined above MUST NOT affect a consistency outcome.

Example (illustrative):

```json
{
  "issuer_id": "partner.example",
  "pub_fingerprint_digest_hex": "<COMPOSITE_KEY_FINGERPRINT_HEX>",
  "roles": ["issuer"],
  "scope": {
    "subject_profiles": ["subject.binary/1"]
  },
  "status": "active",
  "valid_from": "YYYY-MM-DDTHH:MM:SSZ",
  "valid_to": null,
  "revoked_at": null,
  "revocation_reason": null
}
```

### 7.2 Role semantics

If `roles` is present, it constrains which issuance roles are applicable for this entry.

If `roles` is absent, verifiers MUST treat the entry as applicable only to issuance under the `issuer` role.

Verifiers MUST NOT infer roles beyond what is declared.

Under [CCSP/1](../../CCSP/1/index.md) every certificate carries exactly one signature, whose role is `issuer`. An entry with a `roles` array that does not contain `"issuer"` therefore applies to no [CCSP/1](../../CCSP/1/index.md) certificate.

### 7.3 Scope semantics

If `scope` is present, it constrains which certificates this entry is applicable to.

`entry.scope` MUST be a JSON object. It MAY contain:

- `subject_profiles` (array of strings)

Members of `entry.scope` not defined above MUST NOT affect a consistency outcome.

Scope matching MUST be performed as follows:

1. Subject-profile constraint
   If `entry.scope.subject_profiles` is present, then the certificate MUST contain at least one subject in `C.payload.anchor.subjects` whose `profile` exactly matches one element of `entry.scope.subject_profiles`.
   If `entry.scope.subject_profiles` is absent, the entry MUST be treated as having no subject-profile constraint. An empty `subject_profiles` array matches no certificate.

Verifiers MUST perform exact, byte-for-byte string matching. Verifiers MUST NOT apply wildcard matching unless a future major version defines explicit wildcard rules.

Scope constrains how the issuance act is verified against the declared context only.
It MUST NOT be interpreted as proof of compliance, truth, or validity.

Claims of context participation remain representation-layer claims only unless an exact applicable normative path explicitly verifies them.

---

## 8. Consistency binding

An entry is applicable to a certificate **C** if and only if all of the following hold, where "the issuer signature" is the one issuer signature of **C** ([CCSP/1](../../CCSP/1/index.md) Section 7.4) that established its issuance authenticity (Section 5.3):

1. **Issuer identity binding**
   `entry.issuer_id` MUST be identical to `signer.id` of the issuer signature.

2. **Public key binding**
   `entry.pub_fingerprint_digest_hex` MUST equal the composite key fingerprint (Section 8.1) of `signer.pub_p256_b64` and `signer.pub_mldsa_b64` of the issuer signature.

3. **Key label constraint (if present)**
   If `entry.kid` is present, the issuer signature MUST carry a `kid` identical to it. If `entry.kid` is absent, the `kid` of the issuer signature, present or not, plays no part.

4. **Status constraint**
   `entry.status == "active"`

5. **Temporal constraints**
   `entry.valid_from <= C.payload.anchor.issued_at`
   If `entry.valid_to` is present and not null: `C.payload.anchor.issued_at < entry.valid_to`
   Both comparisons are between instants (Section 6.3).

6. **Role scope constraint (if present)**
   If `entry.roles` is present, it MUST contain the signature role under which **C** is issued (as defined by [CCSP/1](../../CCSP/1/index.md) signature role semantics), which is `issuer`.

7. **Declared-context scope constraint (if present)**
   If `entry.scope` is present, verifiers MUST verify `entry.scope` using Section 7.3.
   If the scope constraint fails, the entry MUST be treated as non-matching.

The binding rests on the issuer label and the key fingerprint. `kid` is a non-normative label under [CCSP/1](../../CCSP/1/index.md) Section 7.4.1 and MUST NOT be used as an identity: requirement 3 can only exclude an entry that requirements 1 and 2 would admit, never admit one they exclude. An entry therefore never matches a certificate signed by another key, whatever `kid` either of them carries.

### 8.1 Composite key fingerprint computation

The fingerprint of an issuer key is computed over the two component public keys the issuer signature carries ([CCSP/1](../../CCSP/1/index.md) Section 7.4.2):

```
SHA3-256( pub_p256_bytes || pub_mldsa_bytes )
```

encoded as lowercase hexadecimal, where `pub_p256_bytes` is the 65-byte SEC1 uncompressed point decoded from `signer.pub_p256_b64` and `pub_mldsa_bytes` is the raw FIPS 204 public key decoded from `signer.pub_mldsa_b64`. This is the construction [composite-signature/1](../../../foundation/composite-signature/1/specification.md) Section 10 defines for a composite key: classical first, over the decoded bytes, never over the base64 text or any other encoding of the same keys.

The same computation gives the snapshot issuer fingerprint (Section 5.1, requirement 4), compared with `C.payload.context.snapshot_issuer_fingerprint_digest_hex`, and the issuer fingerprint of **C**, compared with `entry.pub_fingerprint_digest_hex`.

---

## 9. Context snapshot selection

For the purposes of CCVP/1, the certificate issuance time is defined exclusively as:

`C.payload.anchor.issued_at`

Note: CCVP/1 intentionally distinguishes between:

- `C.payload.anchor.issued_at` — the issuance time carried by the target certificate, and
- `S.payload.snapshot.issued_at` — the effective context time of the snapshot.

These timestamps serve different semantic purposes and MUST NOT be conflated, substituted, or compared outside the rules defined in this section.

This value is the only timestamp that MUST be used for context snapshot selection and non-retroactive consistency verification.

For the purposes of CCVP/1, the applicable declared context namespace of the target certificate is defined exclusively as the exact triple of Section 5.2. If it is absent or malformed, CCVP/1 consistency verification MUST resolve to `consistency-unknown`.

This exact triple defines one CCVP/1 verification unit.

If a verifier wishes to assess the same certificate under a different declared context, that assessment MUST be treated as a separate CCVP/1 verification with its own independent outcome.

CCVP/1 defines no canonical merge, ranking, tie-break, or aggregate result across outcomes produced under different declared context namespaces.

Issuance consistency verification MUST be performed against the context snapshot whose effective context time (`S.payload.snapshot.issued_at`) is less than or equal to the certificate issuance time.

Given issuance time `T_cert`:

1. Verify each candidate certificate under the `Issued` route (Section 5.1, requirement 1) and discard those that are not `Issued`-valid. Anyone can produce a certificate that fails verification; such a certificate has no issuer and takes no part.

2. Keep the context snapshot certificates in the namespace: those whose snapshot issuer identity (Section 5.1, requirement 4) is the pair (`C.payload.context.snapshot_issuer_id`, `C.payload.context.snapshot_issuer_fingerprint_digest_hex`) and whose `S.payload.snapshot.context_set_id` is identical to `C.payload.context.context_set_id`. A certificate signed by another key is outside the namespace whatever its `signer.id`, and takes no part.

3. Apply Section 9.1 to the non-conformant context snapshots in the namespace.

4. Select the context snapshot **S** such that:

   - `S.payload.snapshot.issued_at <= T_cert`
   - `S.payload.snapshot.issued_at` is maximal among candidates

If no such snapshot exists, consistency verification MUST result in `consistency-unknown`.

If more than one context snapshot in the namespace has the same maximal `S.payload.snapshot.issued_at` (the same instant, Section 6.3):

- and their `S.payload.snapshot` values produce identical `canonical_bytes` under [`subject.context-snapshot/1`](../../../profiles/subject.context-snapshot/1/index.md), verifiers MAY treat them as the same effective snapshot
- otherwise, the situation MUST be treated as context equivocation and consistency verification MUST result in `consistency-unknown`

Verifiers MUST NOT break such ties heuristically based on source ordering, arrival order, transport origin, or local preference.

Because step 2 admits only snapshots signed by the key **C** names, equivocation can come only from the holder of that key.

### 9.1 Non-conformant snapshots in the namespace

A non-conformant context snapshot (Section 5.1) is in the namespace when it is `Issued`-valid, its snapshot issuer identity is the namespace's, and `S.payload.snapshot` is a JSON object whose `context_set_id` is identical to `C.payload.context.context_set_id`.

Such a snapshot is signed by the key the target certificate names, and says something about its declared context that a verifier cannot read under these rules. It is set aside only when its effective time is readable and shows it cannot govern the target:

- if its `S.payload.snapshot.issued_at` is a timestamp in the form of Section 6.3 and is later than `T_cert`, it takes no part (it is not effective at issuance time);
- if its `S.payload.snapshot.issued_at` is a timestamp in the form of Section 6.3 and is earlier than the effective time of the snapshot selected in step 4, it takes no part (a later snapshot supersedes it);
- otherwise — its effective time is unreadable, or falls between the selected snapshot's effective time (inclusive) and `T_cert` (inclusive), or no snapshot is selected — consistency verification MUST result in `consistency-unknown`.

A verifier MUST NOT skip such a snapshot and select an earlier one instead: that would let an unreadable declaration be replaced by an older one it may have been meant to supersede.

---

## 10. Consistency verification

Using the selected context snapshot **S**:

- If a valid matching entry exists: `consistency-match`
- If no matching entry exists: `consistency-mismatch`
- If no eligible snapshot exists: `consistency-unknown`

Absence of context snapshots MUST NOT invalidate cryptographic validity.

Consistency outcomes such as `consistency-match` MUST NOT be interpreted as:

- a partial or pending form of `Independent`
- a stronger trust class than cryptographic validity and declared context verification justify
- proof of settlement, capacity consumption, payment, or economic execution
- a substitute for `independence_proof` or any higher-layer verification artifact

CCVP/1 may expose consistency with declared context, but it does not prove policy compliance.

---

## 11. Revocation model

Revocation is performed only by issuing new context snapshots.

- revocation is never retroactive
- certificates issued while a key was applicable under a context snapshot remain context-applicable forever under this model
- consistency outcomes apply forward only

Entries MAY include `revoked_at` for auditability, but verifiers MUST apply revocation only via context snapshot selection and temporal constraints.

---

## 12. Observable context signals (Informative)

CCVP/1 exposes deterministic context signals, not trust conclusions.

Verifiers can compute deterministic, audit-friendly signals from context snapshots, including:

- presence/absence of consistency outcomes (`consistency-match` / `consistency-mismatch` / `consistency-unknown`)
- continuity vs gaps of consistency outcomes over time
- outcome age at issuance time
- revocation frequency and key rotation patterns
- role scope stability across context snapshots
- subject-profile coverage and stability in consistency verification (`anchor.subjects[].profile`)
- context density and context snapshot cadence over time
- presence/absence of `policy_refs`
- continuity of `policy_refs` across snapshot history
- changes in `policy_refs` across context snapshots
- stability of referenced policy artifact commitments across snapshot history

Any interpretation of these signals as trust marks, ratings, certifications, or value judgments is **outside the scope of this protocol** and is left entirely to verifier or third-party policy.

Optional verifier or third-party policy statements MAY describe how those actors interpret context signals for their own reporting, acceptance, or escalation logic.

Such policy statements are informative declarations of local behavior only.

They:

- MUST NOT be treated as part of CCVP/1
- MUST NOT redefine consistency outcomes
- MUST NOT alter certificate validity
- MUST NOT be required for protocol conformance
- MUST NOT be interpreted as delegated CERTCRYPT authority
- MUST NOT be used to rank context snapshot issuers against one another

No conforming CERTCRYPT verifier, package presentation, SDK, or UI MAY collapse context signals together with certificate state or independence state so as to imply an institutional CERTCRYPT endorsement of the certificate, issuer, or result.

---

## 13. Forbidden behaviors

Implementations MUST NOT:

- use the most recent context snapshot without time comparison
- apply retroactive consistency outcomes
- require online validation services
- embed context snapshot URLs or endpoints in certificates
- allow certificates to declare their own consistency outcome or contextual status
- treat `S.payload.snapshot.context_set_id` as a global namespace or trust anchor
- rank, score, or comparatively prefer context snapshot issuers based solely on CCVP/1 outcomes
- infer declared-context inputs from `payload.anchor.*` fields, or from any field this specification does not define
- derive a snapshot issuer identity, or a declared context namespace, from a field inside `payload` instead of from the verified issuer signature
- compare CCVP/1 timestamps as strings
- treat `policy_refs` as evidence of compliance
- treat `policy_refs` as enforceable conditions under CCVP/1
- parse referenced policy artifacts heuristically in order to modify consistency outcomes
- infer policy satisfaction solely from the existence of a referenced policy artifact

---

## 14. Relationship to verifier output

CCVP/1 defines consistency verification semantics only.

It defines the semantic outcomes `consistency-match`, `consistency-mismatch`, and `consistency-unknown`, but it does not define a canonical verifier output object.

Consistency verification outcomes MUST NOT override cryptographic validity.

Where a verifier executes more than one CCVP/1 verification for the same certificate under different declared contexts, each outcome remains independent.

CCVP/1 does not define a canonical aggregate result object or a canonical aggregate interpretation across those outcomes.

If a verifier chooses to display referenced policy artifacts or their metadata, such display MUST remain informational and MUST NOT be collapsed into consistency outcomes.

Policy references MUST NOT be presented as proof that the issuer followed its own policy.

---

## 15. Versioning & extensibility

- **Protocol identifier:** `CCVP/1`
- Any change that alters context snapshot selection, consistency verification or binding semantics, consistency outcomes, or scope interpretation (roles / subject_profiles rules) MUST increment the major version.

---

## 16. References

- CERTCRYPT Specifications
    - [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../CCCP/1/index.md)
    - [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../CCSP/1/index.md)
    - [composite-signature/1 — CERTCRYPT Composite Signature Profile](../../../foundation/composite-signature/1/index.md)
    - [subject.context-snapshot/1 — CERTCRYPT Context Snapshot Subject Canonicalization Profile](../../../profiles/subject.context-snapshot/1/index.md)
    - [verifier-toolkit/1 — CERTCRYPT Verifier Toolkit Specification](../../../ecosystem/verification/verifier-toolkit/1/index.md)
    - [subject.binary/1 — CERTCRYPT Binary Subject Canonicalization Profile](../../../profiles/subject.binary/1/index.md)
    - [subject.text/1 — CERTCRYPT Plain Text Subject Canonicalization Profile](../../../profiles/subject.text/1/index.md)
- **External**
    - [RFC 3339 — Date and Time on the Internet: Timestamps](https://www.rfc-editor.org/rfc/rfc3339)
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)

---

**End of CCVP/1**
