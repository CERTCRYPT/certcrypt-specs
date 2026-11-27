# Registered system domain: `certcrypt`

**Identifier:** `certcrypt`

**Type:** Registered System-Domain Instance

**Layer:** Layer 0 — Foundation

**Status:** Frozen

**Registry profile:** `system-domain/1`

**Naming convention:** `certcrypt` is the formal `system_id` of this concrete
system-domain instance. The instance is registered under the `system-domain/1`
profile and is governed by [system-domain/1/specification.md](../../specification.md).

**Audience:** Implementers, verifiers, ecosystem integrators, auditors

**Purpose:** Define the exact root material and bootstrap parameters of the
CERTCRYPT System Domain under the active public architecture.

**Intended use:** This document is the authoritative public registry entry for
the `certcrypt` system domain. Conforming implementers, verifiers, auditors and
ecosystem tooling MUST use the exact values defined here when attributing an
artifact to that domain.

**Scope:** Defines the concrete parameters of the `certcrypt` system domain
exclusively. Generic system-domain semantics, attribution rules, rotation
validation and fork boundaries remain governed by
[system-domain/1/specification.md](../../specification.md). In case of conflict, the
generic specification prevails on questions of mechanism; this entry prevails on
questions of concrete parameter values for `certcrypt`.

**Non-goals:** This registry entry does not redefine, extend or override the
generic semantics of `system-domain/1`. It does not prove truth, semantic
validity, legal validity or live service authority by itself.

> This document is **normative**.
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale

`certcrypt` is the concrete system domain registered for the active CERTCRYPT
public architecture. Only this registry entry defines its root material.

This entry exists to keep the generic `system-domain/1/specification.md` free of
the parameters of any one installation. Those parameters belong here so that:

- the generic specification remains stable across the lifecycle of any individual
  system domain, and carries no state of any one installation
- a further system domain can be registered by adding a registry entry, without
  modifying the generic specification
- there is a single canonical source of truth for the bootstrap of `certcrypt`

The distinction this separation preserves is the one `system-domain/1` Section 13
already draws: the specifications are CERTCRYPT's work and carry its name, but a
**system domain** is an installation — an identifier, root material, and a
bootstrap. A system that reuses the document structures without valid root
attribution is a distinct external system, which is only meaningful because the
model admits more than one domain.

---

## 2. Scope

This registry entry applies to all systems, implementations, SDKs, verifiers,
APIs, publishers and auditors that attribute a CERTCRYPT artifact to the
`certcrypt` system domain, or that evaluate such an attribution.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as
described in RFC 8174.

For the purposes of this entry, the terms `system domain`, `root material`,
`bootstrap`, `manifest version` and `rotation` are to be interpreted exactly as
defined in [system-domain/1/specification.md](../../specification.md) and
[system-manifest/1](../../../../system-manifest/1/specification.md).

---

## 4. System-domain identifier

The exact `system_id` of this system domain is:

```text
certcrypt
```

This identifier is invariant. Any artifact claiming attribution to this system
domain MUST carry exactly this string. No abbreviated, prefixed or otherwise
transformed form is permitted.

---

## 5. Current public bootstrap

For the active public architecture, the current published bootstrap of the
`certcrypt` system domain is fixed as follows:

- `foundation_profile_id = "system-foundation/1"`
- `foundation_statement_id = "certcrypt.foundation.bootstrap/2026-10-18"`
- `system_id = "certcrypt"`
- `bootstrap_system_root_fingerprint = "24a0ed1bc18463a060fd04ff255244b4512340696997c9c3fc9f3d3f3079f69a"`
- `foundation_payload_digest = "d68370b6e6242478c0088a0b4aefa0055bbfba89009f64481157a704ce13468f"`
- `published_rules_versions = ["rules/2026-01"]`

`foundation_payload_digest` is `SHA3-256(UTF-8(JCS(payload)))`, lowercase hexadecimal, over the canonical unsigned statement payload of [`system-foundation/1`](../../../../system-foundation/1/specification.md) Section 9: the exact value the bootstrap quorum signed. It fixes every signed member of the one bootstrap statement, including the Level-1 capacity key.

The bootstrap fingerprint is the digest of the bootstrap manifest version
(`manifest_sequence = 0`) under [`system-manifest/1`](../../../../system-manifest/1/specification.md)
Section 10.

Under the active public rules, `rules/2026-01` belongs to this system domain if
and only if it resolves to that exact bootstrap fingerprint.

---

## 6. Materialization

That bootstrap MUST be materialized by exactly one
[`system-foundation/1`](../../../../system-foundation/1/specification.md) statement
whose semantic equivalents include at least:

- `foundation_profile_id = "system-foundation/1"`
- `foundation_statement_id = "certcrypt.foundation.bootstrap/2026-10-18"`
- `system_id = "certcrypt"`
- `system_root_fingerprint = "24a0ed1bc18463a060fd04ff255244b4512340696997c9c3fc9f3d3f3079f69a"` (equal to the bootstrap fingerprint above)
- `system_manifest = <the bootstrap system-manifest/1 instance with manifest_sequence = 0>`
- `published_rules_versions = ["rules/2026-01"]`

The `system-foundation/1` statement is produced exactly once per system domain.
It is not refreshed, ratified or re-issued under any future rules version.

A verifier MUST hold that the statement it validates for this system domain is
that one statement: after validating it under `system-foundation/1`, it MUST
reject the statement unless its `foundation_statement_id` and its
`foundation_payload_digest` equal the values of Section 5. A second statement
over the same bootstrap manifest — even one correctly signed by the bootstrap
quorum — is therefore never accepted, so the bootstrap statement cannot be
replaced by signing another.

The signed statement is published in the specification repository beside this
entry, as `normative/foundation/system-domain/1/registry/certcrypt/system-foundation.json`,
byte for byte as the bootstrap quorum signed it. That file is a distribution copy: its authenticity comes
from validating it under `system-foundation/1` and from the two values above,
never from where it was obtained. It is not part of the set certified by any
corpus proof (`rules-domain/1` Section 13.3). A conforming verifier SHOULD ship
it, so that a verification needs no CERTCRYPT service to obtain the Level-1
capacity key.

Such a statement MAY be published through `arweave.publication/1` (an optional publication profile, not part of the published corpus). That
publication MAY improve provenance and public-history traceability. It MUST NOT
become a required live dependency for normative system-domain validation.

---

## 7. Attribution and rotation

Any artifact that carries `system_root_fingerprint` and claims attribution to
this system domain MUST carry exactly the bootstrap fingerprint. No verifier MAY
treat another root identifier as equivalent, including the digest of a later
manifest version produced by rotation ([system-domain/1](../../specification.md)
Section 16.2, `system-manifest/1` Section 14).

If that value is absent where required, differs from the bootstrap fingerprint,
or is paired with a conflicting `rules_version`, attribution to this system
domain MUST fail.

---

## 8. Failure conditions

Attribution to the `certcrypt` system domain MUST fail if any of the following
hold:

- the artifact carries a `system_id` other than `"certcrypt"`
- the carried or implied `system_root_fingerprint` differs from the bootstrap
  fingerprint
- the `system-foundation/1` statement presented for this system domain carries a
  `foundation_statement_id` or a `foundation_payload_digest` other than those of
  Section 5
- the resolution order of [system-domain/1](../../specification.md) Section 16.1
  cannot be completed deterministically

No partial success state MAY substitute for a failed required condition.

---

## 9. Immutability

This registry entry is frozen: its bootstrap MUST NOT change in place under any
circumstance.

Root rotation is expressed exclusively through `system-manifest/1`, never by
editing this entry — a rotation must be provable, not declared. A rotation does
not change the bootstrap fingerprint artifacts carry, nor the Level-1 capacity
key the bootstrap statement carries (`system-manifest/1` Sections 14 and 15).

---

## 10. Registered rules domains

The rules domains registered under this system domain are listed in
[rules/](./rules/index.md). A rules domain belongs to exactly one system domain
(`rules-domain/1` Section 7), so they are registered here rather than under the
generic `rules-domain/1` specification.

---

## 11. One-line summary

**`certcrypt` is the registered system domain of the active CERTCRYPT public
architecture, identified by `system_id = "certcrypt"` and anchored by exactly one
`system-foundation/1` bootstrap statement whose embedded manifest fixes its root
fingerprint.**

---

## 12. References

- CERTCRYPT Specifications
    - [system-domain/1 — CERTCRYPT System Domain](../../specification.md)
    - [system-foundation/1 — CERTCRYPT System Foundation](../../../../system-foundation/1/specification.md)
    - [system-manifest/1 — CERTCRYPT System Manifest](../../../../system-manifest/1/specification.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../../../rules-domain/1/specification.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
