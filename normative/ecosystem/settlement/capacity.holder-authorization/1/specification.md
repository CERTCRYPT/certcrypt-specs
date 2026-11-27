# CERTCRYPT Capacity Holder Authorization Specification (capacity.holder-authorization/1)

**Identifier:** `capacity.holder-authorization/1`

**Label:** CERTCRYPT Capacity Holder Authorization Specification (capacity.holder-authorization/1)

**Type:** Ecosystem Specification

**Status:** Frozen

**Layer:** Layer 3 — Ecosystem

**Depends on:** `system-manifest/1`, `system-domain/1`, `rules-domain/1`, `capacity.commitment/1`

**Naming convention:**
`capacity.holder-authorization/1` is the formal identifier.
CERTCRYPT Capacity Holder Authorization Specification (capacity.holder-authorization/1) is the human-readable label.

**Audience:** Implementers, verifiers, ecosystem integrators, auditors.

**Purpose:** Define the normative semantics of the offline-transportable artifact by which an attributed key under the CERTCRYPT System Domain delegates to a commitment-holder's key set the authority to sign `capacity.commitment/1` artifacts within a validity window.

**Intended use:** `capacity.holder-authorization/1` is the canonical means by which a verifier resolves, offline and without contacting CERTCRYPT, that a given `capacity.commitment/1` was signed by a key authorized to do so.

**Scope:** Defines the signed authorization binding, its binding requirements, validity, the scope checked by the fixation service, signature chain anchoring, and verifier obligations. Adjacent protocols, operational tooling, payment/topup mechanisms, and revocation profiles remain out of scope except where explicitly referenced.

**Non-goals:** This specification does not prove truth, semantic validity, or consumption. It does not authorize Independent. It does not introduce a live revocation mechanism.

> This document is **normative**.
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).
>
> The model in §1–§9 of this document is closed. The bytes signed at Level 1 are the insertion-ordered serialization of `level1_binding` fixed by [capacity.evidence/1 §6.1](../../capacity.evidence/1/specification.md) (NOT JCS); the Level-1 signature is composite per §4.

---

## 1. Background & rationale

The CERTCRYPT capacity commitment model splits responsibility across four signature levels:

- **Level 0 — `system-manifest/1`:** root attribution material.
- **Level 1 — system-domain signing key:** delegated by the manifest. Its kid is `authorization_issuer_kid`.
- **Level 2 — `capacity.holder-authorization/1`:** signed by the Level 1 key. Declares the holder key material authorized to sign `capacity.commitment/1` (§1.1).
- **Level 3 — `capacity.commitment/1`:** signed by an authorized holder key.

This document defines Level 2.

### 1.1 Holder key material

An authorization declares a `holder_key_set_root` — a Merkle commitment to a set of per-operation holder keys ([holder-keyset.merkle-sha3-256/1](../../../../protocols/commitment/holder-keyset.merkle-sha3-256/1/index.md)). Each `capacity.commitment/1` is signed by a distinct, non-reused leaf key whose membership in that root is proven per operation. The offline verifier re-verifies the holder signature for itself without ever receiving a stable holder verification key, which would correlate all of that holder's certificates.

There is no stable holder key and no holder key identifier: a stable holder key is precisely the cross-certificate correlator this design removes. Anti-splicing between Level 2 and Level 3 is enforced through the operation-scoped holder and authorization pseudonyms and per-operation Merkle membership in the `holder_key_set_root` (`capacity.evidence/1` §8).

CERTCRYPT does **not** sign `capacity.commitment/1` directly. It signs the Level-1 binding of §3, which authorizes a holder's key set. The holder signs the commitment.

A verifier offline MUST resolve commitment authority through this artifact, not through live CERTCRYPT services, managed dashboards, registries, allowlists, branding, or heuristic identity matching.

### 1.2 What travels and what does not

The authorization has two parts with different audiences:

- the **Level-1 binding** (§3): the exact object the system domain signs. It carries no holder identifier and nothing that correlates a holder across certificates, and it travels inside every `capacity.evidence/1`, where an offline verifier checks it;
- the **issuance record**: what the fixation service keeps about the authorization it issued — the holder and the contract it was issued for, and its internal identifier. It is not signed, does not travel, and is checked only by the fixation service when a submission consumes capacity under the authorization (§6).

---

## 2. Conformance

A conforming implementation MUST implement every MUST in this document.
A conforming verifier MUST fail closed when any MUST is unsatisfied.

---

## 3. The signed object: the Level-1 binding

The system domain signs exactly this object, with members in this order:

```text
level1_binding {
  system_id:                <system identifier, e.g. "certcrypt">
  rules_version:            <e.g. "rules/2026-01">
  system_root_fingerprint:  <manifest root fingerprint>
  authorized_role:          "capacity_commitment_holder"
  authorization_issuer_kid: <system-domain Level-1 key id>
  valid_from:               <RFC 3339 UTC>
  valid_until:              <RFC 3339 UTC>
  holder_key_set_root:      <root of the authorized per-operation key set>
}
```

Its signing bytes are the insertion-ordered serialization fixed by [capacity.evidence/1 §6.1](../../capacity.evidence/1/specification.md). It carries no holder, contract, pool or issuer identifier: those would correlate the holder's certificates, and none of them can be checked by a third party.

The binding travels inside `capacity.evidence/1` as `projected_authorization.level1_binding`, next to its signature `projected_authorization.level1_signature`. `projected_authorization` repeats each binding member at its top level and adds the operation-scoped `authorization_pseudonym` and `holder_pseudonym` (CCCP/1 §7.4), which replace the authorization's and the holder's identifiers.

### 3.1 Identity

The fixation service identifies an authorization internally; that identifier never travels. In the evidence the authorization is identified by its pseudonym, and in the settlement material by `resolved_authorization_digest` = SHA3-256 of the binding's signing bytes ([`rules/2026-01`](../../../../foundation/system-domain/1/registry/certcrypt/rules/2026-01.md) §13).

### 3.2 Anti-splicing

`system_id`, `rules_version` and `system_root_fingerprint` declare the cryptographic context. The `projected_commitment` of the same evidence MUST carry exactly equal values, and its `holder_pseudonym` and `authorization_pseudonym` MUST equal those of `projected_authorization`. The leaf key that signed the commitment MUST prove membership in `holder_key_set_root`. Any mismatch MUST result in fail-closed verification.

---

## 4. Signature & anchoring (Level 1)

The binding MUST be signed by the system-domain Level-1 key identified by `authorization_issuer_kid`, attributable to the CERTCRYPT System Domain through `system-manifest/1`. The signature is a **composite signature** (`composite-signature/1`, canonical profile `certcrypt-composite-p256-mldsa65-v1`): classical and ML-DSA-65 components over the same message, AND, fail-closed on the post-quantum component. It is not a single ML-DSA-65 value. (The per-operation holder signature over the commitment is, by contrast, ML-DSA-65 pure — `capacity.evidence/1` §4.)

Verifiers MUST NOT accept a signature that does not verify under the system domain's Level-1 composite key.

The signature profile is constrained by the rules domain; under `rules/2026-01` it is the composite profile above.

---

## 5. Validity & expiry

### 5.1 Authorization-level validity

`valid_from` and `valid_until` define the temporal window during which a `capacity.commitment/1` MAY be signed under this authorization. The window is inclusive at both ends and compared as instants: a commitment whose `issued_at` falls outside `[valid_from, valid_until]` MUST be rejected by verifiers (`capacity.evidence/1` §8).

### 5.2 No live revocation

There is no live revocation mechanism in `/1`. Authorization validity is bounded exclusively by `valid_from`/`valid_until` and by the system domain's Level-1 key.

A verifier MUST NOT consult any live revocation source, CRL, OCSP-equivalent, or status endpoint when validating this artifact. Future revocation profiles MAY be defined as additional offline-transportable artifacts; they MUST NOT introduce live verification dependencies.

### 5.3 Distinct timescales

Authorization validity MAY align with long contractual windows. It is independent of the TTL applied to individual `capacity.commitment/1` artifacts. The commitment-level `expires_at` is governed by `rules-domain/1` and is unrelated to `valid_until` of the authorization.

Implementations MUST NOT collapse the two timescales: the authorization's `valid_until` is NOT a substitute for the commitment's `expires_at`, and a commitment's `expires_at` is not required to fall inside the authorization's window.

---

## 6. Scope (checked by the fixation service)

The fixation service issues an authorization for one holder and one contract, and keeps that scope in the issuance record (§1.2). The scope is not signed and does not travel, so it is not an offline check: a third party has no contract, pool or issuer identifier to compare it with, and under the zero-data model none is ever published.

When a submission consumes capacity under an authorization, the fixation service MUST refuse it unless the authorization was issued for the contract the submission is made under. There is no implicit broadening, override or fallback.

---

## 7. Verifier obligations (Offline)

Given a `capacity.evidence/1`, a conforming verifier MUST, fail-closed, perform the steps of `capacity.evidence/1` §8 that concern the authorization:

1. Resolve the system domain's Level-1 composite key and verify `level1_signature` over the signing bytes of `level1_binding` (§4).
2. Check that every `level1_binding` member equals its `projected_authorization` counterpart, and that `authorized_role` is `capacity_commitment_holder`.
3. Check the anti-splicing bindings of §3.2.
4. Check that the commitment's `issued_at` falls in `[valid_from, valid_until]` (§5.1).

Any failure MUST result in fail-closed verification of the dependent commitment.

The verifier MUST NOT contact CERTCRYPT live services. It MUST NOT use local allowlists, branding heuristics, managed dashboards, or registries outside the manifest chain.

---

## 8. Non-goals

This specification does **not** define:

- topup or grant ingestion mechanics
- holder-internal accounting (how the holder tracks granted, outstanding, consumed and released capacity)
- holder-side safety policy (reserves, exposure limits, circuit breakers)
- CERTCRYPT operational ledger schema
- live revocation, CRL, or OCSP-equivalent mechanics
- pricing, billing, periodic credit, wallet, or balance semantics
- consumption — that is governed by `capacity.commitment/1` and the settlement path

These concerns are operational or are governed by sibling specifications.

---

## 9. Interpretation boundaries

`capacity.holder-authorization/1` does **not** by itself prove:

- that the holder is solvent
- that any specific commitment will eventually fix
- that a commitment signed under this authorization is `Independent`
- the truth of any claim made by the issuer
- the ordering of real-world events

It establishes only that, within the indicated window, the keys of the indicated key set are authorized to sign `capacity.commitment/1` artifacts under the active CERTCRYPT System Domain.

---

## 10. Versioning

- **Specification identifier:** `capacity.holder-authorization`
- **Specification version:** `/1`

Any change that alters:

- the signed-field set or its order
- scope semantics
- signature anchoring
- the layered relationship with `system-manifest/1` or `capacity.commitment/1`

requires a new major version. Already valid authorizations under `/1` are not retroactively reinterpreted by later versions.

---

## 11. Wire format

The wire form of the binding, of its signature and of `projected_authorization` is the one `capacity.evidence/1` §5 fixes. No other serialization of this artifact exists.

---

## 12. References

- `system-manifest/1`
- `system-domain/1`
- `rules-domain/1` (registry entry `rules/2026-01`)
- `capacity.commitment/1`
- `independence.proof/1`
- [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../../../protocols/CCCP/1/index.md)
- [capacity.evidence/1 — CERTCRYPT Capacity Evidence](../../capacity.evidence/1/index.md)
- [composite-signature/1 — CERTCRYPT Composite Signature Profile](../../../../foundation/composite-signature/1/index.md)
- [holder-keyset.merkle-sha3-256/1 — CERTCRYPT Holder Operation-Key Set Commitment Scheme](../../../../protocols/commitment/holder-keyset.merkle-sha3-256/1/index.md)
