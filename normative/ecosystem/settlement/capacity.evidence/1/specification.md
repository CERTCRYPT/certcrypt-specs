# CERTCRYPT Capacity Evidence Specification (capacity.evidence/1)

**Identifier:** `capacity.evidence/1`

**Label:** CERTCRYPT Capacity Evidence Specification (capacity.evidence/1)

**Type:** Ecosystem Specification

**Status:** Frozen

**Layer:** Layer 3 — Ecosystem

**Depends on:** `system-manifest/1`, `system-domain/1`, `rules-domain/1`, `CCCP/1`, `holder-keyset.merkle-sha3-256/1`, `capacity.commitment/1`, `capacity.holder-authorization/1`

**Naming convention:**
`capacity.evidence/1` is the formal identifier.
CERTCRYPT Capacity Evidence Specification (capacity.evidence/1) is the human-readable label.

**Audience:** Implementers, verifiers, ecosystem integrators, auditors.

**Purpose:** Define the offline-transportable, zero-data, zero-PII projection of a holder's authorized-and-signed capacity commitment, so that an offline verifier can re-run the capacity authorization proof for a single certificate's commitment — verifying the system-domain authorization and the holder signature for real — without receiving any personal data or business identifier in clear (business identifiers are operation-scoped pseudonyms). The linkability boundary — the stable `holder_key_set_root` travels in clear on the artifact surface by design — is defined in §9.

**Intended use:** `capacity.evidence/1` is the artifact a verifier consumes (under `supporting_material.capacity_evidence` of a `verification-package/1`, bound to the commitment it backs because its digest IS that commitment's `commitment_id` — §7.1) to satisfy input 7 of `independence.proof/1 §9` on the zero-data path.

**Scope:** Defines the object layout, the canonicalization rules, the signature targets, and the offline verification procedure. The Merkle key-set primitive and the pseudonym derivation it relies on are defined by their own specifications and referenced here. Settlement, consumption, pricing, and `Independent` acceptance are out of scope.

**Non-goals:** `capacity.evidence/1` does not prove consumption (that is settlement-bound, `capacity.commitment/1 §9`), does not prove `Independent`, and does not authorize anything by itself. It establishes that consumption was **authorized** and that the commitment was **signed by an authorized holder key**, with neither the holder's stable key nor stable identifiers exposed.

> This document is **normative**.
> All requirements expressed using MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in RFC 8174.

---

## 1. Background & rationale

The capacity authorization chain (system-domain → holder-authorization → holder-signed commitment) is verified online at submit. For the offline verifier to re-verify it — which is what the anti-notarization property requires at the surface where the public promise is made — the verifier needs the holder's verification key. But a stable holder key, reused across commitments, correlates all of that holder's certificates.

`capacity.evidence/1` resolves that: it is the **projected, derived** view of one `capacity.commitment/1` (and the `capacity.holder-authorization/1` that authorizes it), in which stable identifiers become operation-scoped pseudonyms and the stable holder key becomes a non-reused per-operation leaf key proven to belong to a system-domain-authorized key-set root.

Its `projected_commitment` is the only wire form of `capacity.commitment/1` (`capacity.commitment/1 §8.2`): a minimal object carrying only what the offline capacity proof needs and no stable personal or business identifier. The enclosing evidence still carries the stable `holder_key_set_root`; the resulting artifact-side correlation boundary is defined in §9.

---

## 2. Conformance

A conforming implementation MUST implement every MUST in this document.
A conforming verifier MUST fail closed when any MUST is unsatisfied. Incomplete redaction (a missing salt, a pseudonym that does not match, a membership proof that does not bind, a signature that does not verify, a digest that does not match) MUST fail the evidence, never yield partial success. In a `verifier-toolkit/1` result the evidence is reported under `CAPACITY_EVIDENCE_VALID` (§10): evidence that is supplied and does not verify is `INDEPENDENT_INVALID`; evidence, or the material needed to check it, that is not supplied is `INCOMPLETE`.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** follow RFC 8174 (BCP 14).

Additional terms:

- **Projected commitment:** the zero-PII / pseudonymous view of a `capacity.commitment/1`, signed by a per-operation leaf key (business identifiers projected to operation-scoped pseudonyms; see the linkability boundary in §9).
- **Projected authorization:** the zero-PII / pseudonymous view of the `capacity.holder-authorization/1`, carrying the system-domain-signed `holder_key_set_root` (a stable key-set identifier — see the linkability boundary in §9).
- **Operation leaf key:** one non-reused signing key from the holder's authorized operation-key set (`holder-keyset.merkle-sha3-256/1`).
- **Operation salt:** the public per-operation salt under which all pseudonyms in one evidence object are derived.
- **Evidence digest:** the canonical digest of the whole evidence object; in the zero-data profile it IS the commitment's `commitment_id` (§7, §7.1).
- **Signed commitment digest:** the digest of the projected commitment's signing bytes; the identity of the commitment the holder signed, on which replay and exclusivity are enforced (§7.2).

---

## 4. Object layout

A `capacity.evidence/1` object MUST contain exactly:

- `profile` — the zero-data profile marker, the exact string `zero-data.unlinkable`. This is a mode marker, not an artifact identifier; the governing specification is `capacity.evidence/1` itself.
- `operation_salt_hex` — the public per-operation salt, lowercase hexadecimal. Pseudonyms are recomputed under it.
- `projected_authorization` — §5.
- `projected_commitment` — §6.
- `operation_key` — the operation-key disclosure (`holder-keyset.merkle-sha3-256/1 §11`): `{ leaf_index, public_key_b64, inclusion_proof, tree_size }`.
- `commitment_signature_b64` — the holder's **ML-DSA-65 (pure)** signature over the projected commitment's signing bytes (§6.1), made with the disclosed leaf key. This is the ephemeral, single-use operation-key (Level-3) signature: it is deliberately pure ML-DSA-65, NOT a composite signature (the composite profile governs the permanent trust chain only — see `composite-signature/1 §2`). Base64 (standard alphabet, with padding).

## 5. `projected_authorization`

The publishable projection of the Level-2 authorization. It MUST contain, in this exact field order (the order is the signing-bytes order for the embedded Level-1 binding; see §5.1):

- `system_id`, `rules_version`, `system_root_fingerprint`
- `authorized_role`
- `authorization_issuer_kid` — the Level-1 system-domain kid (public by design; it is the manifest key, it does not correlate holders)
- `valid_from`, `valid_until`
- `holder_key_set_root` — the Merkle root committing to the holder's operation-key set, replacing the stable holder public key
- `level1_binding` — the exact binding object the system-domain signed (§5.1)
- `level1_signature` — system-domain Level-1 **composite signature** (`composite-signature/1`) over `level1_binding`'s signing bytes; the trust anchor that proves `holder_key_set_root` was authorized, not fabricated. It is the composite wire object `{ alg, mode, signatures[] }` (classical + ML-DSA-65, AND, fail-closed), NOT a single base64 value — the Level-1 key is part of the permanent trust chain.
- `authorization_pseudonym`, `holder_pseudonym` — operation-scoped pseudonyms (CCCP/1 §7.4) that MUST match the projected commitment's

### 5.1 `level1_binding`

The exact fields the system-domain signs once, offline, when it authorizes the holder's operation-key root. It is the signed sub-object of the zero-data `capacity.holder-authorization/1` (not a standalone artifact, so it carries no version tag of its own). It MUST contain, in this exact order: `system_id`, `rules_version`, `system_root_fingerprint`, `authorized_role`, `authorization_issuer_kid`, `valid_from`, `valid_until`, `holder_key_set_root`.

## 6. `projected_commitment`

The publishable projection of the `capacity.commitment/1`, signed by the operation leaf key. It MUST contain, in this exact field order (the signing-bytes order; §6.1):

- `commitment_version` — the exact string `capacity.commitment/1`
- `system_id`, `system_root_fingerprint`, `rules_version`
- `authorization_pseudonym`, `holder_pseudonym`, `pool_pseudonym` — operation-scoped pseudonyms (CCCP/1 §7.4), replacing `authorization_id` / `holder_id` / `pool_id`
- `certificate_commitment_digest` — the certificate content digest (publishable in clear)
- `consumed_quantity` — the consumed capacity quantity string
- `declared_effective_units` — the issuer-declared effective units for this commitment's subject, counted per subject (`submission-set/1 §13.2`): a non-collection subject declares `"1"`, a collection subject declares its `declared_cardinality`. A canonical decimal / unsigned-integer string, never a number. This is the per-subject economic quantity the settlement leaf's `cost_commitment` preimage binds; it is distinct from `consumed_quantity` (the burned capacity). Carried here, in the signed artifact path, so it is not supplied only through a separate unbound channel (`submission-set/1 §13.3`). An Independent-path verifier MUST bind this value to the certified subjects of the base certificate — it MUST equal the sum of per-subject effective declared units — and fail closed under `EFFECTIVE_UNITS_BINDING_VALID` when it understates them (`capacity.commitment/1 §13.1.1`)
- `issued_at`, `expires_at` — RFC 3339, reduced precision (truncated to second), carried so the verifier can run the temporal conditions

This object deliberately carries no logical field of the commitment model that is unnecessary for the capacity proof or that would correlate; `capacity.commitment/1` §15 maps each of them.

### 6.1 Signing bytes (insertion order, NOT JCS)

The bytes signed by the operation leaf key are the JSON serialization of `projected_commitment` in its exact declared field order (insertion-ordered, NOT RFC 8785 JCS). The same applies to `level1_binding` for the Level-1 signature (§5.1). Field order IS the contract; a verifier MUST reproduce insertion order and MUST NOT reorder keys for these signed objects.

Rationale: an ML-DSA-65 signature covers these exact bytes, so they must be byte-stable in declaration order. This is distinct from the evidence digest (§7), which is JCS.

The signature is **hedged** (randomized): the contract pins the signing bytes, never the signature value. A verifier MUST verify the signature against the signing bytes; it MUST NOT pin or compare a fixed signature value.

---

## 7. Evidence digest (JCS)

The evidence digest is:

```text
evidence_digest = SHA3-256( RFC8785-JCS(capacity.evidence object) )
```

The whole evidence object is canonicalized with RFC 8785 JCS (keys sorted) — NOT insertion order. Rationale: unlike the signed sub-objects (§6.1), this digest is not covered by any signature; it only needs to be deterministic and identical across languages. The object is deeply nested, so depending on declaration order would diverge between implementations; JCS sorts keys canonically on both sides.

A verifier MUST recompute this digest. In the zero-data profile it IS the commitment's `commitment_id` (§7.1), so the verifier requires it to equal the `commitment_id` carried in the verified certificate's per-commitment inclusion path — binding the evidence to the exact commitment the leaf admitted (anti-splicing).

### 7.1 Evidence digest as the commitment identifier (Zero-data profile)

A stable commitment identifier would correlate, so `projected_commitment` (§6) carries none. The settlement leaf must nonetheless identify the commitment it carries: the sub-tree of accepted commitments (`settlement.binding/1 §7`) is built over `commitment_id` values, and the per-commitment inclusion path binds the verified certificate's commitment into the `subtree_root` (`independence.proof/1 §7.10`).

In this profile, therefore, the `commitment_id` of a commitment is its `capacity_evidence_digest` (§7): the canonical digest of the capacity evidence IS the identifier under which that commitment is admitted to the leaf and listed in the proof's `consumed_commitment_ids`.

A verifier MUST, for the certificate it evaluates, recompute the evidence digest (§7) and require it to equal the `commitment_id` carried by that commitment's inclusion path. This is what ties the supplied evidence to the exact commitment the leaf admitted: without it, the evidence-to-proof digest binding (§7) and the commitment-to-`subtree_root` inclusion binding would each hold in isolation while leaving the supplied evidence and the admitted commitment unbound to each other. The commitment has no other public identifier (`capacity.commitment/1` §15).

### 7.2 Signed commitment digest (replay identity)

The evidence digest covers the whole evidence, `operation_key` included, and no signature covers `operation_key`: the disclosure is unsigned, and its `tree_size` is not committed to by the holder key set root (`holder-keyset.merkle-sha3-256/1` §11.4, §12.2). One signed commitment can therefore travel in evidences with different bytes, each of which verifies under §8 and each with its own evidence digest. The evidence digest identifies one evidence, which is what the leaf admits and the proof binds (§7.1); it does not identify the commitment the holder signed.

That commitment is identified by:

```text
signed_commitment_digest = lowercase_hex( SHA3-256( signing bytes of projected_commitment ) )   (§6.1)
```

It depends only on what the holder signed: not on the disclosure, and not on the signature value, which is hedged. A party that enforces single use of a commitment — the fixation service at submission (`submission-set/1` §9.1) — MUST key that enforcement on `signed_commitment_digest`, not on the evidence digest. An offline verifier, which holds no global state, does not enforce single use and does not need it.

> Do not confuse the two canonicalizations: insertion order for the signed sub-objects (§6.1); JCS for the evidence digest (§7). Applying JCS to the signing bytes, or insertion order to the digest, breaks verification silently.

---

## 8. Verification procedure (Offline)

Given a `capacity.evidence/1` object, the resolved system-domain public key, and the expected `commitment_id` (the value carried in the verified certificate's inclusion path; §7.1), a conforming verifier MUST, fail-closed:

1. **Profile + salt present.** `profile` is exactly `zero-data.unlinkable`; `operation_salt_hex` decodes to a non-empty salt.
2. **Authorization window.** `valid_from <= projected_commitment.issued_at <= valid_until`, comparing instants and inclusive at both ends, where `valid_from` and `valid_until` are those of `level1_binding`. A bound or `issued_at` that cannot be read as an RFC 3339 instant fails. The window governs when a commitment may be issued; `expires_at` is the commitment's own deadline, evaluated against the settlement (`settlement.binding/1` §9), and is not required to fall inside the window.
3. **Level-1 trust anchor.** `level1_binding.holder_key_set_root` equals `projected_authorization.holder_key_set_root`; every `level1_binding` field equals its `projected_authorization` counterpart; `authorized_role` is exactly `capacity_commitment_holder` (`capacity.holder-authorization/1` §7 step 2); and the `level1_signature` composite (`composite-signature/1`) verifies against the resolved system-domain composite key over `level1_binding`'s signing bytes (§5.1, §6.1) — AND over all components, fail-closed on the ML-DSA-65 component. This proves the root was authorized by the system-domain, not fabricated.
4. **Leaf membership.** The disclosed `operation_key` proves membership in `holder_key_set_root` (`holder-keyset.merkle-sha3-256/1 §12`).
5. **Commitment signature.** `commitment_signature_b64` verifies (ML-DSA-65) against the disclosed leaf key over `projected_commitment`'s signing bytes (§6.1). Real re-verification, not an opaque commitment.
6. **Pseudonym bindings.** `projected_commitment.holder_pseudonym == projected_authorization.holder_pseudonym` and `…authorization_pseudonym` likewise; and `(system_id, rules_version, system_root_fingerprint)` agree between the two. Anti-splicing on pseudonyms, not on cleartext ids.
7. **Evidence digest.** The recomputed evidence digest (§7) equals the expected `commitment_id` (§7.1) — i.e. the commitment this evidence backs is the one the verified certificate includes into the `subtree_root`.

Steps 2–7 establish **authorized** capacity. They do not establish consumption; consumption is settlement-bound and validated separately (`independence.proof/1 §12.6–§12.7`). The capacity authorization (this artifact) MUST be validated before settlement, as its precondition (`independence.proof/1 §12.5`).

---

## 9. Privacy and unlinkability

The object MUST carry no original material and no personal data in clear. The stable holder/pool/authorization business identifiers appear only as operation-scoped pseudonyms (CCCP/1 §7.4) under a fresh `operation_salt` per operation; the stable holder verification key is never carried — only non-reused per-operation leaf keys appear. This is the **zero-PII** guarantee.

`(tree_size, leaf_index)` in the operation-key disclosure is acceptable public metadata (`holder-keyset.merkle-sha3-256/1 §11.5`): position carries order, not identity.

**Linkability boundary (by design).** The `holder_key_set_root` (§5, in `projected_authorization`) is a STABLE identifier that DOES travel in clear: it is the Merkle root the system-domain Level-1 binding signs, and the anchor against which the verifier checks operation-key membership. It does NOT rotate per operation (it identifies the authorized key-set), so rotating the operation leaf + `operation_salt` does NOT make two operations of the same key-set unlinkable to an observer who holds both evidence objects. This is intentional, not a leak: such correlation lives on the **artifact surface** (the verification-package circulating off the protocol surface), which is exactly where third-party correlation is permitted and where a recipient holding two packages MAY recognize them as issued under the same authorized key-set. It is NOT on the **protocol surface**: the `holder_key_set_root` is never anchored on-chain (the settlement memo binds only the aggregated `settlement_root`) and CERTCRYPT operates no per-issuer feed/log/aggregator over it.

So this profile guarantees: **zero-PII**, and **structural unlinkability of the protocol surface** — nothing CERTCRYPT emits or publishes on the protocol surface correlates a holder's operations. It does NOT guarantee observer-side unobservability of a received artifact: an observer with multiple evidence objects of the same key-set MAY correlate them. The offline verifier holds no global state and cannot detect operation-leaf or `operation_salt` reuse; non-reuse is a holder emission invariant.

---

## 10. Failure conditions

Verification MUST fail if: `profile` is wrong or `operation_salt` is missing; `issued_at` falls outside the authorization window or the window cannot be read; the Level-1 binding fields do not match the projected authorization, `authorized_role` is not `capacity_commitment_holder`, or the Level-1 signature does not verify; the operation key is not a member of the root; the commitment signature does not verify against the leaf; the pseudonym or system-context bindings disagree; or the recomputed evidence digest does not match the expected `commitment_id` (§7.1). No partial or best-effort acceptance is permitted.

A `verifier-toolkit/1` verifier reports the outcome under the check `CAPACITY_EVIDENCE_VALID`:

| Situation | Result |
|---|---|
| The evidence verifies | `CAPACITY_EVIDENCE_VALID` passes |
| The evidence is supplied and any condition above fails | `INDEPENDENT_INVALID` |
| The proof consumes a commitment but no evidence, no inclusion path to bind it, or no system-domain Level-1 key to check it is supplied | `INCOMPLETE` |

---

## 11. Versioning & extensibility

- **Specification identifier:** `capacity.evidence`
- **Specification version:** `/1`

Any change that alters the object layout, the signing-bytes order, the canonicalization rules, the signature targets, or the verification procedure requires a new major version. Already valid evidence under `/1` is not retroactively reinterpreted.

---

## 12. References

- [CCCP/1 §7.4](../../../../protocols/CCCP/1/index.md) — operation-scoped pseudonym derivation
- [holder-keyset.merkle-sha3-256/1](../../../../protocols/commitment/holder-keyset.merkle-sha3-256/1/index.md) — operation-key set root and membership proof
- [capacity.commitment/1](../../capacity.commitment/1/index.md) — the base commitment this projects (§8.2)
- [capacity.holder-authorization/1](../../capacity.holder-authorization/1/index.md) — the authorization this projects
- [independence.proof/1](../../../../models/independence.proof/1/index.md) — binds this evidence by its digest = `commitment_id` (§9 input 7, §12.5)
- [verification-package/1](../../../verification/verification-package/1/index.md) — carries this under `supporting_material.capacity_evidence`
- [verifier-toolkit/1](../../../verification/verifier-toolkit/1/index.md) — consumes it
- [composite-signature/1 — CERTCRYPT Composite Signature Profile](../../../../foundation/composite-signature/1/index.md)
- [rules-domain/1 — CERTCRYPT Rules Domain](../../../../foundation/rules-domain/1/index.md)
- [settlement.binding/1 — CERTCRYPT Aggregated Settlement Binding](../../settlement.binding/1/index.md)
- [submission-set/1 — CERTCRYPT Submission Set Protocol](../../../../protocols/settlement/submission-set/1/index.md)
- [system-domain/1 — CERTCRYPT System Domain](../../../../foundation/system-domain/1/index.md)
- [system-manifest/1 — CERTCRYPT System Manifest](../../../../foundation/system-manifest/1/index.md)
