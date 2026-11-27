# CERTCRYPT System Foundation (`system-foundation/1`) — overview

**Identifier:** `system-foundation/1`

**Label:** CERTCRYPT System Foundation Specification (system-foundation/1)

**Page:** Informative overview

**Specification type:** Foundation Specification

**Layer:** Layer 0 — Foundation

**Status:** Frozen

> This document is **informative**.
> All normative rules are defined exclusively in [specification.md](./specification.md).

---

## What is `system-foundation/1`?

`system-foundation/1` defines the canonical foundation artifact that carries the root material used by the active CERTCRYPT bootstrap.

It makes the bootstrap artifact explicit and verifiable, rather than leaving the root-material basis as an unexplained constant or a live-service dependency.

---

## Why this specification exists

A published root fingerprint is useful, but a bare fingerprint by itself can look like a static string rather than a verifiable bootstrap artifact.

`system-foundation/1` exists to fix:

- the canonical statement that carries the root material
- the exact derivation of the system-root fingerprint from that material
- the boundary between publication provenance and normative validation

---

## Scope boundaries

`system-foundation/1` applies only to the canonical foundation artifact carrying the CERTCRYPT bootstrap root material.

It does:

- define the bootstrap artifact boundary
- permit local or packaged validation of that artifact
- keep publication and discovery outside the normative validation core

It does not:

- replace `system-domain/1`
- replace `rules-domain/1`
- create authority by publication
- produce proof or `Independent`

---

## Core guarantees

Under `/1`, the system-foundation layer preserves:

- one exact bootstrap artifact boundary
- deterministic derivation of the system-root fingerprint
- offline-capable validation
- institutional independence from live publication infrastructure
- interpretation boundaries between publication provenance and system meaning

---

## Relationship to other CERTCRYPT specifications

`system-foundation/1` does not replace:

- `system-domain/1`, which defines exact system attribution
- `rules-domain/1`, which defines exact rules-domain selection
- `security-model/1`, which defines foundational fail-closed behavior

Instead:

- `system-foundation/1` answers: "What exact artifact carries the bootstrap root material?"
- `system-domain/1` answers: "Which exact system does that artifact identify?"
- `rules-domain/1` answers: "Which exact rules belong to that system?"

---

## Reading guide

Recommended reading order for implementers and auditors:

1. [Specification](./specification.md)
2. [system-manifest/1](../../system-manifest/1/specification.md)
3. [system-domain/1](../../system-domain/1/specification.md)
4. [rules-domain/1](../../rules-domain/1/specification.md)
5. [security-model/1](../../security-model/1/specification.md)

---

## Versioning

- **Specification identifier:** `system-foundation`
- **Specification version:** `/1`

Version `/1` is defined for the current CERTCRYPT leaf-based independence architecture and embeds one bootstrap `system-manifest/1` manifest version.

Changes that alter the embedded root-material model, the bootstrap signature procedure, the derivation of `system_root_fingerprint`, or the dual-use rule of the bootstrap private key require a new major version.

Later versions do not retroactively reinterpret already valid statements governed by `/1`.

---

## One-line summary

`system-foundation/1` defines the canonical bootstrap artifact that embeds and signs the bootstrap `system-manifest/1` of one CERTCRYPT System Domain, exactly once, while remaining offline-verifiable under public rules.

---

## Normative reference

This overview is informational in nature.

All definitive rules and constraints are defined in:

- [system-foundation/1/specification](./specification.md)

In case of discrepancy, the specification prevails.
