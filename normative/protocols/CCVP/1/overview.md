# CERTCRYPT Consistency Verification Protocol (CCVP/1) — overview

**Identifier:** CCVP/1

**Label:** CCVP v1

**Page:** Informative overview

**Specification type:** Protocol

**Layer:** Layer 1 — Protocols

**Status:** Frozen · optional verification plane, outside the `Issued` and `Independent` path

**Depends on:**
- [CCCP/1](../../CCCP/1/index.md)
- [CCSP/1](../../CCSP/1/index.md)

> This document is **informative**.
> All normative rules are defined exclusively in [CCVP/1/specification](specification.md).
> In case of discrepancy, the [specification](specification.md) always prevails.

---

## What is `CCVP/1`?

**[CCVP/1](specification.md)** defines how CERTCRYPT represents **issuance declared context** through **context snapshots** expressed as standard CERTCRYPT certificates.

A context snapshot is:

- a CERTCRYPT certificate ([CCSP/1](../../CCSP/1/index.md))
- an immutable representation of declared context state
- time-scoped via its payload-defined effective timestamp
- offline-capable (snapshot acquisition is out of scope)
- non-retroactive in effect

It certifies which issuer identities and keys were eligible within a declared context namespace at a specific moment.

In CCVP/1:

- target-certificate declared context is carried in `C.payload.context`
- target-certificate declared context namespace is selected by the exact triple `snapshot_issuer_id + snapshot_issuer_fingerprint_digest_hex + context_set_id`: the snapshot issuer is named by its label and by the fingerprint of its composite key, so nobody else can publish snapshots in that namespace
- issuer identity and key binding are taken from the valid issuer signature under [CCSP/1](../../CCSP/1/index.md): `signer.id` plus the composite key fingerprint `SHA3-256(pub_p256_bytes || pub_mldsa_bytes)`; a `kid`, when an entry names one, only narrows the match
- context snapshots remain ordinary CERTCRYPT certificates with snapshot payloads, verified under the `Issued` route like any other certificate, and their issuer is the key that signed them, never a field they carry
- every CCVP/1 timestamp uses the UTC form of `anchor.issued_at` and is compared as an instant
- the plane is optional: its outcome is reported beside `Issued` and `Independent` and never changes either

CCVP/1 verifies issuance consistency against a declared context at a given time. It does not enforce policy, validate intent, or determine compliance.

Context snapshots MAY include optional declarative `policy_refs`, but CCVP/1 does not interpret, enforce, or validate those referenced policy artifacts.

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

## Why this specification exists

Traditional issuance-authorization systems typically depend on live infrastructure:

- centralized authorities or hierarchies
- revocation lists and online responders (CRL / OCSP)
- retroactive invalidation
- operational availability over long time horizons

These dependencies degrade offline and long-term verifiability.

CERTCRYPT adopts a different model:

- cryptographic validity is self-contained
- issuance consistency is verified against certified historical context
- consistency outcomes apply forward only

---

## Scope boundaries

[CCVP/1](specification.md) defines how **consistency verification is performed against historical declared context**, using certified context snapshots.

It deliberately avoids real-time validation, retroactive control, or operational dependencies.
Issuance consistency is verified **offline**, relative to the declared context that existed at certificate issuance time.

[CCVP/1](specification.md) complements cryptographic verification but never replaces it.

Optional `policy_refs` remain declarative only under CCVP/1 and do not alter consistency outcomes by themselves.

---

## Core guarantees

Under `/1`, CCVP/1 preserves:

- offline-capable consistency verification under one exact declared context namespace at one exact point in time
- non-retroactive consistency outcomes that apply forward only
- separation between cryptographic verification and consistency verification
- separation between consistency outcome and policy interpretation
- absence of canonical aggregate outcome across multiple declared contexts
- absence of any institutional endorsement or trust authority through consistency results

Consistency outcomes do not override cryptographic validity, do not certify policy compliance, and do not produce or strengthen `Independent`.

---

## How consistency verification works

Given an `Issued`-valid certificate with issuance time `C.payload.anchor.issued_at`, and declared context namespace `(C.payload.context.snapshot_issuer_id, C.payload.context.snapshot_issuer_fingerprint_digest_hex, C.payload.context.context_set_id)`, a verifier:

1. Verifies every offered snapshot certificate under the `Issued` route and discards the invalid ones
2. Keeps the snapshots signed by the key the namespace names, for the declared `context_set_id`, and checks each one's snapshot object and its `subject.context-snapshot/1` commitment
3. Selects the snapshot whose `S.payload.snapshot.issued_at <= T_cert` and with the greatest instant
4. Verifies issuer/key consistency against that snapshot only, including the role and the exact subject-profile scope when present

Absence of context snapshot data never invalidates cryptographic validity.

If any member of that namespace triple is absent, consistency verification resolves to `consistency-unknown`.

If a verifier wants to assess the same certificate under a different declared context, that is a separate CCVP/1 verification, not part of the same one.

CCVP/1 does not define a canonical aggregate outcome across multiple declared contexts.

---

## Offline capability

[CCVP/1](specification.md) defines an offline-capable consistency-verification model.

Verifiers can obtain context snapshots from any source (including on-chain, mirrors, or prepackaged containers).

Snapshot acquisition and distribution are out of scope.

[CCVP/1](specification.md) operates without online validation services (e.g., OCSP/CRL endpoints) and introduces no runtime dependency beyond the snapshots provided.

---

## Relationship to other CERTCRYPT specifications

[CCVP/1](specification.md) depends structurally on:

- [CCCP/1](../../CCCP/1/index.md) for canonicalization and hashing semantics
- [CCSP/1](../../CCSP/1/index.md) for certificate-envelope structure
- [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md) for fail-closed verifier behavior in implementations that adopt the reference toolkit
- [verification-package/1](../../../ecosystem/verification/verification-package/1/index.md) when consistency verification is packaged for offline transport

[CCVP/1](specification.md) does not define subject canonicalization or a canonical verifier output object.

It defines only the semantic outcomes:

- `consistency-match`
- `consistency-mismatch`
- `consistency-unknown`

Verifiers MAY expose those outcomes through their own result objects, diagnostics, package viewers, or multi-context comparison surfaces.

CCVP/1 itself defines no canonical report schema and no canonical aggregate output across multiple declared contexts.

Consistency outcomes do not override cryptographic validity.

---

## Reading guide

Recommended reading order for implementers and auditors:

1. [Specification](specification.md)
2. [CCCP/1](../../CCCP/1/specification.md)
3. [CCSP/1](../../CCSP/1/specification.md)
4. [verifier-consistency-tree](verifier-consistency-tree.md) (normative annex)
5. [verifier-consistency-tree-examples](verifier-consistency-tree-examples.md) (informative annex)

---

## Versioning

- **Specification identifier:** `CCVP`
- **Specification version:** `/1`

Version `/1` defines the first canonical consistency-verification protocol for CERTCRYPT issuance against historical declared context.

Changes that alter context-snapshot semantics, snapshot selection, the consistency outcome set, or the boundary between consistency and cryptographic verification require a new major version.

Later versions do not retroactively reinterpret already valid consistency outcomes governed by `/1`.

---

## One-line summary

`CCVP/1` defines the canonical declarative consistency-verification protocol that aligns CERTCRYPT issuance with one historical declared context at one moment in time, offline and forward-only, without itself certifying policy compliance, trust, or `Independent`.

---

## Normative reference

This overview is informational in nature.

All definitive rules and constraints are defined in:

- [CCVP/1/specification](specification.md)

In case of discrepancy, **[specification](specification.md) always prevails**.
