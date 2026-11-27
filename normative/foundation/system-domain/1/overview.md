# CERTCRYPT System Domain (`system-domain/1`) — overview

**Identifier:** `system-domain/1`

**Label:** CERTCRYPT System Domain Specification (system-domain/1)

**Page:** Informative overview

**Specification type:** Foundation Specification

**Layer:** Layer 0 — Foundation

**Status:** Frozen

> This document is **informative**.
> All normative rules are defined exclusively in [specification.md](./specification.md).

---

## What is `system-domain/1`?

`system-domain/1` defines exact system attribution for CERTCRYPT artifacts.

It makes system identity, public bootstrap, and root-material attribution first-class foundation concerns rather than naming conventions.

Within the active architecture, it fixes:

- how CERTCRYPT identity is attributed
- how root material anchors that attribution
- how cloned or spoofed systems are rejected
- how the active public bootstrap is resolved

---

## Why this specification exists

A bare `system_id = "certcrypt"` is not enough.

Without a public root-material basis and deterministic bootstrap, a clone could reuse familiar names and artifact shapes while remaining indistinguishable to a weak verifier.

`system-domain/1` exists to prevent that downgrade.

---

## Scope boundaries

`system-domain/1` applies only to exact system attribution and the public bootstrap needed to resolve it.

It does:

- define exact system identity binding
- define the public bootstrap boundary
- require rejection of cloned or spoofed systems

It does not:

- replace `rules-domain/1`
- replace `security-model/1`
- prove truth
- produce `Independent`

---

## Core guarantees

Under `/1`, the system-domain foundation preserves:

- exact system attribution
- anti-spoofing and anti-clone boundaries
- deterministic bootstrap resolution
- institutional independence from live CERTCRYPT infrastructure
- interpretation boundaries between system identity and proof semantics

---

## Relationship to other CERTCRYPT specifications

`system-domain/1` does not replace:

- `system-foundation/1`, which fixes the canonical artifact carrying the root material
- `rules-domain/1`, which defines exact public-rule selection
- `security-model/1`, which defines foundational guarantees and fail-closed behavior

Instead:

- `system-foundation/1` answers: "What exact bootstrap artifact carries the root material?"
- `system-domain/1` answers: "Which exact system does that bootstrap belong to?"
- `rules-domain/1` answers: "Which exact public rules belong to that system?"

---

## Reading guide

Recommended reading order for implementers and auditors:

1. [Specification](./specification.md)
2. [system-foundation/1](../../system-foundation/1/specification.md)
3. [system-manifest/1](../../system-manifest/1/specification.md)
4. [rules-domain/1](../../rules-domain/1/specification.md)
5. [security-model/1](../../security-model/1/specification.md)

---

## Versioning

- **Specification identifier:** `system-domain`
- **Specification version:** `/1`

Version `/1` is defined for the current CERTCRYPT leaf-based independence architecture.

Changes that alter system-domain attribution, root-material binding, the bootstrap-vs-current fingerprint distinction, or the rotation chain through `system-manifest/1` require a new major version.

Later versions do not retroactively reinterpret already valid attributions governed by `/1`.

---

## One-line summary

`system-domain/1` defines exact CERTCRYPT system attribution, anchors it to a public bootstrap fingerprint, and accepts attribution under that bootstrap fingerprint only, which no `system-manifest/1` rotation changes.

---

## Normative reference

This overview is informational in nature.

All definitive rules and constraints are defined in:

- [system-domain/1/specification](./specification.md)

In case of discrepancy, the specification prevails.
