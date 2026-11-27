# CERTCRYPT Consistency Verification Protocol - Verifier Consistency Tree (CCVP/1)

**Identifier:** CCVP/1/verifier-consistency-tree

**Type:** Normative Protocol Artifact

**Status:** Frozen

**Layer:** Layer 1 — Protocols

**Depends on:**

- [CCVP/1](specification.md)
- [CCCP/1](../../CCCP/1/index.md)
- [CCSP/1](../../CCSP/1/index.md)

> This document is **normative**.
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative.

---

## Purpose

This document defines the **normative verifier-side consistency flow** for verifying issuance consistency under [CCVP/1](specification.md).

It specifies **how verifiers MUST select context snapshots and resolve consistency outcomes**, without requiring online validation services or runtime endpoints.

This flow defines one CCVP/1 verification for one target certificate under one declared context namespace.

If a verifier assesses the same certificate under a different declared context namespace, that assessment is a separate CCVP/1 verification with its own independent outcome.

This document defines no canonical aggregate result across multiple declared contexts.

---

## Inputs

The verifier receives:

- A target CERTCRYPT certificate **C**.
- Zero or more candidate certificates offered as context snapshots.

The verifier uses the rules of [CCVP/1](specification.md); where this flow and the specification differ, the [specification](specification.md) prevails.

Notation: **C** is the target certificate and **S** a context snapshot certificate, as in the specification. Timestamps are compared as instants, never as strings ([CCVP/1](specification.md) Section 6.3).

---

## Preconditions

Before executing this consistency flow:

- **C** MUST be `Issued`-valid under the `Issued` route of [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md) ([CCVP/1](specification.md) Section 5.3). If it is not, the flow terminates and any reported outcome is `consistency-unknown`.
- [CCVP/1](specification.md) consistency verification MUST NOT influence or override the `Issued` or `Independent` verdict
- Absence of context snapshot data MUST NOT invalidate the certificate
- If `C.payload.context` does not carry the namespace triple (`snapshot_issuer_id`, `snapshot_issuer_fingerprint_digest_hex`, `context_set_id`) in the form of [CCVP/1](specification.md) Section 5.2, consistency verification MUST resolve to `consistency-unknown`

---

## Stage 1 — snapshot certificate verification

For each candidate certificate, the verifier MUST:

1. Verify it under the `Issued` route, exactly as any base certificate ([CCVP/1](specification.md) Section 5.1, requirement 1)
2. Discard every candidate that is not `Issued`-valid

A discarded candidate MUST NOT participate in consistency verification.

---

## Stage 2 — namespace collection

For each remaining candidate, the verifier MUST derive the snapshot issuer identity from its verified issuer signature — `signer.id` and the composite key fingerprint of `signer.pub_p256_b64` and `signer.pub_mldsa_b64` ([CCVP/1](specification.md) Section 8.1) — and MUST keep only the candidates that:

- carry `payload.snapshot` or a `subject.context-snapshot/1` subject (the others are not context snapshots and are ignored)
- have the snapshot issuer identity (`C.payload.context.snapshot_issuer_id`, `C.payload.context.snapshot_issuer_fingerprint_digest_hex`)
- have `S.payload.snapshot.context_set_id` identical to `C.payload.context.context_set_id`

The snapshot issuer identity MUST NOT be read from any field inside `payload`. A candidate signed by another key is outside the namespace whatever its `signer.id`.

Each kept candidate is then checked against [CCVP/1](specification.md) Section 5.1: the snapshot object of Section 6 with its timestamps in the form of Section 6.3 and its entries in the form of Section 7.1, and exactly one `subject.context-snapshot/1` subject whose commitment equals the recomputed commitment of `S.payload.snapshot`. A candidate that fails is a non-conformant snapshot and is handled in Stage 3.

### Implementation limits (Defensive consideration)

Verifiers **MAY** impose implementation-defined limits on the number of context snapshots processed, provided that:

- all snapshots considered eligible under [CCVP/1](specification.md) snapshot selection rules remain eligible
- snapshot selection semantics defined in this document are preserved
- no snapshot is preferred or excluded based on source, ordering, or convenience

Such limits are intended solely to protect verifier implementations against resource exhaustion and **MUST NOT** alter consistency semantics.

---

## Stage 3 — snapshot selection (Normative)

Among the conformant snapshots in the namespace, the verifier MUST select a snapshot **S** such that:

- `S.payload.snapshot.issued_at <= C.payload.anchor.issued_at`
- `S.payload.snapshot.issued_at` is the **greatest** instant satisfying the above condition

If no such snapshot exists:

- outcome = `consistency-unknown`
- the consistency process terminates

If more than one snapshot in the namespace has the same maximal `S.payload.snapshot.issued_at`:

- and their `S.payload.snapshot` values produce identical canonical bytes under [`subject.context-snapshot/1`](../../../profiles/subject.context-snapshot/1/index.md), the verifier MAY treat them as the same effective snapshot
- otherwise the verifier MUST resolve the outcome as `consistency-unknown`

A non-conformant snapshot in the namespace resolves the outcome as `consistency-unknown` unless its effective time is a well-formed timestamp that is later than `C.payload.anchor.issued_at` or earlier than the effective time of the selected snapshot ([CCVP/1](specification.md) Section 9.1). The verifier MUST NOT skip it in order to select an earlier snapshot.

---

## Stage 4 — entry matching

Using the selected snapshot **S**, the verifier MUST search `S.payload.snapshot.entries` for an entry that satisfies every requirement of [CCVP/1](specification.md) Section 8 against the issuer signature of **C**:

1. `entry.issuer_id` is identical to `signer.id`
2. `entry.pub_fingerprint_digest_hex` equals the composite key fingerprint of the signer's two public keys
3. if `entry.kid` is present, the issuer signature carries an identical `kid`
4. `entry.status` is `"active"`
5. `entry.valid_from <= C.payload.anchor.issued_at`, and, if `entry.valid_to` is not null, `C.payload.anchor.issued_at < entry.valid_to` (instants)
6. if `entry.roles` is present, it contains `"issuer"`
7. if `entry.scope.subject_profiles` is present, at least one element of `C.payload.anchor.subjects` has a `profile` identical to one of its elements

---

## Stage 5 — consistency resolution

The verifier MUST resolve consistency verification as follows:

- If a matching entry exists → `consistency-match`
- If no matching entry exists → `consistency-mismatch`

---

## Output

The verifier MUST expose one CCVP/1 consistency outcome for the verification unit it executed.

Consistency verification:

- refines structural interpretation only
- never overrides cryptographic validity
- introduces no runtime dependency

If a context snapshot contains optional `policy_refs`, a verifier MAY display those references or their metadata for informational purposes only.

Such display MUST NOT:

- modify the consistency outcome
- be presented as proof of policy compliance
- be presented as proof that the issuer followed its own policy
- be collapsed into `Independent`, trust, approval, or institutional endorsement

If the verifier executes this flow more than once for the same certificate under different declared context namespaces, each resulting outcome remains independent.

This document defines no canonical merge or aggregate result across those independent decisions.

---

## Forbidden verifier behaviors

Under [CCVP/1](specification.md), a verifier MUST NOT:

- select the latest context snapshot without time comparison
- apply retroactive consistency outcomes
- infer consistency outcomes from cryptographic validity
- let a consistency outcome change an `Issued` or `Independent` verdict
- require online validation services or endpoints
- infer declared-context inputs from `payload.anchor.*` fields, or from any field [CCVP/1](specification.md) does not define
- take a snapshot issuer identity from a field inside `payload` instead of from the verified issuer signature
- compare CCVP/1 timestamps as strings
- rank or comparatively prefer context snapshot issuers based solely on CCVP/1 outcomes
- treat `policy_refs` as evidence of compliance
- parse referenced policy artifacts heuristically to modify consistency outcomes

---

This document defines the normative verifier-side consistency-verification flow for [CERTCRYPT Consistency Verification Protocol version CCVP/1](specification.md).
Any change that alters this flow requires a new major version.
