# system-foundation/1 · CERTCRYPT System Foundation

**Identifier:** `system-foundation/1`

**Label:** CERTCRYPT System Foundation Specification (system-foundation/1)

**Page:** Informative version index

**Specification type:** Foundation Specification

**Layer:** Layer 0 — Foundation

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `system-foundation/1` are defined by its [Specification](./specification.md).
> In case of discrepancy, the specification prevails.

---

## What is `system-foundation/1`?

`system-foundation/1` defines the canonical bootstrap artifact by which CERTCRYPT root material can be published, cached, transported, and validated under public rules.

It does not define:

- truth semantics
- independence semantics
- settlement execution
- certificate validity by itself

It defines:

- one exact foundation statement model
- one exact root-fingerprint derivation model
- one exact offline validation boundary for that statement
- how immutable publication anchors remain optional provenance rather than live authority

---

## Role within CERTCRYPT

Within the CERTCRYPT foundation:

- `system-foundation` defines how the bootstrap artifact itself is modeled
- `system-domain` defines which system is being evaluated
- `rules-domain` defines which exact public rules govern that evaluation

Under the active public architecture, a `system-foundation/1` statement MAY be published through `arweave.publication/1` (an optional publication profile, not part of the published corpus), but verifier conformance MUST remain decidable from local artifact validation under public rules.

---

## Normative documents

- [Specification](./specification.md)

---

## See also

- [Overview](./overview.md)
- [system-domain/1](../../system-domain/1/specification.md)
- [rules-domain/1](../../rules-domain/1/specification.md)
- `arweave.publication/1` — named by this specification as an optional publication profile; not part of the published corpus

---

## Versioning

- **Identifier:** `system-foundation/1`

Version `system-foundation/1` defines the active public contract for this document. Any non-backward-compatible semantic or structural change requires a new major version.

## One-line summary

`system-foundation/1` defines the canonical bootstrap artifact by which CERTCRYPT root material can be published immutably while remaining offline-verifiable.
