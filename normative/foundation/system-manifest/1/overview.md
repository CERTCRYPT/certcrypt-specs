# CERTCRYPT System Manifest (system-manifest/1) — overview

**Identifier:** `system-manifest/1`

**Label:** CERTCRYPT System Manifest Specification (system-manifest/1)

**Page:** Informative overview

**Specification type:** Foundation Specification

**Layer:** Layer 0 — Foundation

**Status:** Frozen

**Depends on:**

- public rules capable of defining algorithm identifiers and signature semantics
- a canonical JSON serialization model (JCS, RFC 8785) for deterministic digest derivation
- a digest function (SHA3-256) for canonical fingerprint computation
- `system-foundation/1` for the bootstrap statement that anchors the bootstrap manifest version

> This document is **informative**.
> All normative rules are defined exclusively in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `system-manifest/1`?

`system-manifest/1` defines the canonical model for the artifact by which one CERTCRYPT System Domain declares its identity and the chain of public keys authorized to sign on its behalf across time.

It is a specification of identity and key-chain semantics. It is not a publication artifact, not a balance API, not a settlement receipt, and not a proof of independence.

It does not make a leaf `Independent`.

It defines the artifact by which a conforming implementation can establish that:

- a system domain has a stable invariant identifier (`system_id`) that does not change across rotations
- a system domain has a deterministic digest (`system_root_fingerprint`) computed over a closed canonical artifact
- the active entry of the system domain at any given time — the key set whose quorum authorizes the next rotation — is the manifest entry whose half-open active interval includes that time
- a rotation produces a successor manifest version without changing the bootstrap fingerprint every artifact carries
- equivocation by a predecessor entry is detectable as evidence whenever conflicting successor signatures converge at a single conforming verifier

---

## Why this specification exists

CERTCRYPT separates:

- system identity
- bootstrap publication
- rules-domain selection
- key rotation and continuity
- artifact attribution and signature validation

Deriving `system_root_fingerprint` directly from a single public key would make root-key rotation indistinguishable from system-domain replacement: any rotation would invalidate every prior artifact bound to the old fingerprint, because verifiers would have no canonical mechanism to recognize the rotated key as belonging to the same system domain. `system-manifest/1` exists to avoid that.

`system-manifest/1` resolves that problem by separating two concerns:

- the **identity** of the system domain, expressed as the digest of a manifest that catalogs its key material across time
- the **active entry** at any given moment — the key set whose quorum authorizes rotation — which is one entry inside that manifest

Without that separation, an implementation could incorrectly treat:

- a rotated-out public key
- a key declared without authorization lineage from a known predecessor
- a manifest fork accepted in isolation

as if it were the canonical signing authority of the system domain.

The specification prevents that collapse.

---

## Scope boundaries

Within the current architecture, `system-manifest/1` sits below the bootstrap statement and above artifact-level signature validation.

Its role is to define:

- the canonical artifact whose digest is the system root identifier
- the append-only chain of authorized public keys
- the deterministic rotation operation that authorizes new keys
- the rule that every artifact carries the bootstrap fingerprint, which no rotation changes
- the equivocation-evidence model under which a compromised predecessor key is converted into detectable terminal invalidity

Under `/1`, the manifest authorizes attribution and signature validation. It does not complete the path to `Independent`. Settlement, capacity consumption, and proof of independence are evaluated by other specifications under the rules domain selected by the artifact.

---

## Core guarantees

`system-manifest/1` governs:

- the meaning of a system manifest under `/1`
- the closed schema of the manifest and of every entry
- the canonical serialization and digest derivation
- the bootstrap procedure for the first manifest version of a system domain
- the rotation procedure that produces successor manifest versions
- the manifest validation requirements that any conforming verifier MUST satisfy
- the rule that a rotation changes who may authorize the next rotation, never the fingerprint artifacts carry
- the statement that operational artifacts are signed by the Level-1 capacity key of the bootstrap statement, not by manifest members
- the equivocation-evidence and fail-closed properties that make compromise detectable rather than silently accepted
- failure semantics and conformance

It does **not** govern:

- bootstrap publication, which is governed by `system-foundation/1`
- publication transport, which is governed by publication profiles such as `arweave.publication/1` (an optional publication profile, not part of the published corpus)
- rules-domain associations, which are governed by `system-foundation/1`, `system-domain/1`, and `rules-domain/1`
- provenance and discovery metadata, which live in adjacent layers
- settlement orchestration, capacity semantics, or independence proofs

---

## Relationship to other CERTCRYPT specifications

`system-manifest/1` depends conceptually on:

- `system-foundation/1` for the bootstrap statement that signs and publishes the bootstrap manifest version
- a canonical JSON serialization model (RFC 8785 JCS) for deterministic digest derivation
- a digest function (SHA3-256) for canonical fingerprint computation
- the algorithm identifiers permitted by the deployment, declared inside each manifest entry

It is referenced by:

- `system-foundation/1` for the embedded bootstrap manifest model
- `system-domain/1` for the bootstrap-vs-current fingerprint distinction and for the rotation mechanism
- any specification that resolves the active entry of a system domain at a given time

It remains authoritative for the manifest artifact itself.

If any later workflow, SDK, or convenience layer treats:

- a key not cataloged in a valid manifest version as if it were the active signing authority
- a manifest fork accepted in isolation as if it were the canonical chain
- a compromised predecessor's conflicting signatures as if they were merely operational anomalies

that later layer is in conflict with [specification.md](./specification.md).

---

## Reading guide

Recommended reading order for implementers and auditors:

1. [Specification](./specification.md)
2. [system-foundation/1](../../system-foundation/1/specification.md)
3. [system-domain/1](../../system-domain/1/specification.md)
4. [rules-domain/1](../../rules-domain/1/specification.md) and the active registry entry under [system-domain/1/registry/certcrypt/rules/](../../system-domain/1/registry/certcrypt/rules/index.md)

---

## Versioning

- **Specification identifier:** `system-manifest`
- **Specification version:** `/1`

Version `/1` is defined for the current CERTCRYPT system-domain identity architecture.

Changes that alter the closed manifest schema, the canonical digest derivation, the rotation procedure, the equivocation-evidence model, the attribution of artifacts to the bootstrap fingerprint, or the boundary between identity and provenance require a new major version.

Later versions do not retroactively reinterpret already valid manifest versions governed by `/1`.

---

## One-line summary

`system-manifest/1` defines the canonical identity-only artifact whose bootstrap digest is the `system_root_fingerprint` of one CERTCRYPT System Domain, and catalogs the append-only chain of quorums authorized to rotate it, without changing the fingerprint artifacts carry.

---

## Normative reference

This overview is informational in nature.

All definitive rules and constraints are defined in:

- [system-manifest/1/specification](./specification.md)

In case of discrepancy, the specification prevails.
