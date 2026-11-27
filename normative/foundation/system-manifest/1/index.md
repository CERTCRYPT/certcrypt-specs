# system-manifest/1 · CERTCRYPT System Manifest

**Identifier:** `system-manifest/1`

**Label:** CERTCRYPT System Manifest Specification (system-manifest/1)

**Page:** Informative version index

**Specification type:** Foundation Specification

**Layer:** Layer 0 — Foundation

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `system-manifest/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `system-manifest/1`?

`system-manifest/1` defines the canonical artifact whose deterministic digest is the `system_root_fingerprint` of one CERTCRYPT System Domain.

A system manifest is an identity-only artifact: it carries the append-only chain of public keys authorized to sign on behalf of the system domain across time, and nothing else. Provenance metadata, publication metadata, and rules-domain associations are deliberately excluded from the manifest, so that the digest of the manifest is stable across changes that do not affect the key chain itself.

It does **not** define:

- truth semantics
- independence semantics
- certificate validity by itself
- settlement execution
- the canonical bootstrap statement under which a manifest is published — that concern belongs to `system-foundation/1`
- the publication transport — that concern belongs to publication profiles such as `arweave.publication/1` (an optional publication profile, not part of the published corpus)
- the association between a system root identifier and any rules-domain version — that concern belongs to `system-foundation/1`, `system-domain/1`, and `rules-domain/1`

It defines:

- one exact manifest model with a closed schema
- one exact append-only key chain semantics
- one exact derivation of `system_root_fingerprint` from a manifest instance
- one exact rotation operation that binds each rotation to the predecessor manifest version and sequence
- one exact validation of a manifest version, and the part of it an artifact verifier performs
- one exact equivocation-evidence and fail-closed model

Under `/1`, a system manifest is the canonical source of system-domain identity and of the entry whose quorum authorizes rotation at any given time. It is not proof of `Independent`, not proof of consumption, and not a substitute for settlement.

---

## Role within CERTCRYPT

`system-manifest/1` sits at the foundation of the CERTCRYPT corpus, immediately below `system-foundation/1` and adjacent to `system-domain/1`.

Within the current architecture:

- `system-manifest/1` defines the canonical key-chain artifact whose digest is the system root identifier
- `system-foundation/1` embeds and signs exactly one bootstrap manifest version of one system domain
- `system-domain/1` defines what it means for an artifact to belong to the CERTCRYPT System Domain, and how attribution is resolved across rotations
- `rules-domain/1` and its registry define the public ruleset under which any given artifact is evaluated

A system manifest does not consume capacity, prove independence, or endorse any issuer claim. It defines the canonical reference for determining which keys are authorized to sign on behalf of this system domain, today and in the past.

---

## Normative documents

The normative component of `system-manifest/1` is:

- [Specification](./specification.md)

The specification defines:

- the closed manifest model
- canonical serialization and digest
- entry field semantics
- the successor-binding payload
- the bootstrap procedure
- the rotation procedure and post-rotation properties
- anti-equivocation properties under `/1`
- manifest validation
- later manifest versions and artifact attribution
- the keys that sign operational artifacts
- failure conditions, security properties, and conformance

---

## See also

- [Overview](./overview.md)
- [system-foundation/1](../../system-foundation/1/index.md)
- [system-domain/1](../../system-domain/1/index.md)
- [rules-domain/1](../../rules-domain/1/index.md)

---

## Versioning

- **Specification identifier:** `system-manifest`
- **Specification version:** `/1`

Version `/1` defines the first canonical system-manifest model for the current CERTCRYPT architecture.

Any change that alters:

- the closed manifest schema
- the canonical serialization or digest derivation
- the rotation procedure
- the equivocation-evidence model
- the rule that artifacts carry the bootstrap fingerprint
- the boundary between identity and provenance

requires a new major version.

Already valid manifest versions under `/1` are not retroactively reinterpreted by later versions.

---

## One-line summary

`system-manifest/1` defines the canonical identity-only artifact whose bootstrap digest is the `system_root_fingerprint` of one CERTCRYPT System Domain, and catalogs the append-only chain of quorums authorized to rotate it, without changing the fingerprint artifacts carry.
