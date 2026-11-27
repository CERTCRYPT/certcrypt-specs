# system-domain/1 · CERTCRYPT System Domain

**Identifier:** `system-domain/1`

**Label:** CERTCRYPT System Domain Specification (system-domain/1)

**Page:** Informative version index

**Specification type:** Foundation Specification

**Layer:** Layer 0 — Foundation

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `system-domain/1` are defined by its [Specification](./specification.md).
> In case of discrepancy, the specification prevails.

---

## What is `system-domain/1`?

`system-domain/1` defines how CERTCRYPT implementations attribute artifacts to the exact CERTCRYPT System Domain and reject cloned or spoofed systems.

It does not define:

- truth semantics
- proof validity by itself
- settlement execution
- capacity authorization or consumption

It defines:

- exact system identity
- exact root-material attribution
- deterministic system bootstrap
- deterministic linkage from system attribution to applicable rules domains

---

## Role within CERTCRYPT

Within the CERTCRYPT foundation:

- `system-domain` defines which system is being evaluated
- `rules-domain` defines which exact public rules govern that evaluation
- `security-model` defines which foundational properties must hold under those rules

The concrete bootstrap of a registered system domain — its `system_id`, its
foundation statement and its root fingerprint — is declared in that domain's
registry entry, never here. For the active CERTCRYPT public architecture see
[registry/certcrypt](./registry/certcrypt/index.md); this specification defines
only how such a domain is resolved and attributed.

---

## Normative documents

- [Specification](./specification.md)
- [Registered system domains](./registry/index.md)

## Reading order

1. [Specification](./specification.md) — the model: what a system domain is and
   how attribution to one is validated
2. [registry](./registry/index.md) — the concrete domains registered under it,
   each with its own root material and bootstrap

---

## See also

- [Overview](./overview.md)
- [system-foundation/1](../../system-foundation/1/specification.md)
- [rules-domain/1](../../rules-domain/1/specification.md)
- [security-model/1](../../security-model/1/specification.md)

---

## Versioning

- **Identifier:** `system-domain/1`

Version `system-domain/1` defines the active public contract for this document. Any non-backward-compatible semantic or structural change requires a new major version.

## One-line summary

`system-domain/1` defines how CERTCRYPT fixes exact system attribution, root-material binding, and the current public bootstrap for deterministic evaluation.
