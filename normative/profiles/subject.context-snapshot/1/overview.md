# CERTCRYPT Context Snapshot Subject Canonicalization Profile (`subject.context-snapshot/1`) — overview

**Identifier:** `subject.context-snapshot/1`

**Label:** CERTCRYPT Context Snapshot Subject Canonicalization Profile v1

**Page:** Informative overview

**Specification type:** Profile Specification

**Layer:** Layer 2 — Profiles

**Status:** Frozen

**Depends on:**
- [system-domain/1](../../../foundation/system-domain/1/index.md)
- [rules-domain/1](../../../foundation/rules-domain/1/index.md)
- [security-model/1](../../../foundation/security-model/1/index.md)
- [CCCP/1](../../../protocols/CCCP/1/index.md)
- [CCSP/1](../../../protocols/CCSP/1/index.md)
- [CCVP/1](../../../protocols/CCVP/1/index.md)

> This document is **informative**.
> The normative requirements for `subject.context-snapshot/1` are defined exclusively in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `subject.context-snapshot/1`?

`subject.context-snapshot/1` defines how context snapshot subjects are reduced to deterministic canonical bytes under CERTCRYPT public rules.

It exists for the narrow case where a certificate is being used to carry a signed context snapshot artifact for offline consistency verification under [CCVP/1](../../../protocols/CCVP/1/index.md).

It does not define authority by itself.
It does not define truth, trust, or `Independent`.

The term "context" is declarative and does not imply authority, enforcement, or compliance.

---

## Why this specification exists

`CCVP/1` classifies context snapshot certificates using a declared `profile` in `payload.anchor.subjects[]`.

Under [CCSP/1](../../../protocols/CCSP/1/index.md), those values are profile identifiers, not ad hoc strings.

`subject.context-snapshot/1` therefore exists to make that classification structurally coherent:

- the declared `profile` corresponds to a real public profile
- the profile defines one exact canonicalization boundary
- the context snapshot certificate remains subordinate to higher-layer CCVP semantics

---

## Scope boundaries

`subject.context-snapshot/1` defines:

- the exact context-snapshot subject boundary
- how `canonical_bytes(subject)` are produced
- which transformations are forbidden
- how profile-level verification remains subordinate to the broader CERTCRYPT architecture

It deliberately does not define:

- issuance eligibility
- consistency outcome semantics
- settlement, payment, or capacity execution
- semantic truth of the snapshot contents
- legal meaning
- institutional endorsement
- trust or authority

Those meanings remain outside the profile.

---

## Core guarantees

Under `/1`, the profile preserves:

- exact context-snapshot subject canonicalization under deterministic JSON serialization
- profile-bound subject identification consistent with `CCSP/1` subject-profile semantics
- zero-data compatibility for context-snapshot payloads, with no cross-certificate correlation introduced by the profile itself
- subordination to `CCVP/1` for any consistency outcome
- interpretation boundaries between canonicalization and any higher-layer authority, trust, or compliance claim

---

## Relationship to other CERTCRYPT specifications

`subject.context-snapshot/1` is not a standalone verification system.

It sits below higher-layer consistency verification:

- `system-domain/1` decides which system is being evaluated
- `rules-domain/1` decides which exact public rules apply
- `security-model/1` decides which fail-closed boundaries must hold
- `CCCP/1` supplies the commitment semantics
- `CCSP/1` supplies certificate envelope structure
- `CCVP/1` defines context snapshot meaning, namespace selection, and consistency resolution

This profile contributes only one thing:

`canonical_bytes(subject)`

It does not by itself produce `consistency-match`, `consistency-mismatch`, `Issued`, or `Independent`.

---

### Zero-data and correlation boundary

`subject.context-snapshot/1` is unusual among subject profiles because the subject is a context snapshot artifact, not a real-world payload such as an email or binary document.

That means:

- it does not expose subject-level personal data by design
- it may still expose issuance-program or declared-context correlation at the certificate level
- any such correlation comes from higher-layer CCVP fields, not from this profile itself

This profile MUST NOT be interpreted as weakening CCCP subject unlinkability for ordinary certified subjects.

---

### Relationship to verification

Under `CCVP/1` a context snapshot certificate carries the snapshot object in `payload.snapshot`, and exactly one `subject.context-snapshot/1` subject whose commitment is the CCCP commitment of that object's canonical bytes. A `CCVP/1` verifier recomputes that commitment from `payload.snapshot`; the snapshot the certificate carries is therefore the snapshot its issuer signed. The snapshot issuer is the key that signed the certificate, never a field inside the snapshot.

When the applicable path requires subject recomputation under this profile, the verifier uses the exact context snapshot JSON value governed by the profile and canonicalizes it deterministically.

That remains fully offline-capable.

It does not justify:

- hosted context interpretation services
- resolver authority
- managed interpretation shortcuts
- semantic upgrades from convenience tooling

---

### Anti-authority boundary

`subject.context-snapshot/1` must not be read as an authority profile.

It defines canonicalization only.

It does not define:

- declared-context legitimacy by itself
- timestamping authority
- proof-of-existence semantics
- proof-of-independence semantics

If a context snapshot later participates in verifier-side consistency verification, that meaning comes from [CCVP/1](../../../protocols/CCVP/1/index.md), not from this profile alone.

---

## Reading guide

Recommended order for implementers and auditors:

1. [foundation](../../../foundation/index.md)
2. [CCCP/1](../../../protocols/CCCP/1/index.md)
3. [CCSP/1](../../../protocols/CCSP/1/index.md)
4. [CCVP/1](../../../protocols/CCVP/1/index.md)
5. [subject.context-snapshot/1/specification](./specification.md)

---

## Versioning

- **Specification identifier:** `subject.context-snapshot`
- **Specification version:** `/1`

Version `/1` defines the first canonical context-snapshot subject canonicalization profile.

Changes that alter the input boundary, the canonicalization rule, the forbidden-transformation list, or the boundary between canonicalization and `CCVP/1` consistency semantics require a new major version.

Later versions do not retroactively reinterpret already valid context-snapshot canonicalizations governed by `/1`.

---

## One-line summary

`subject.context-snapshot/1` defines the canonical canonicalization profile for context-snapshot subjects carried in CERTCRYPT certificates, producing deterministic `canonical_bytes(subject)` for offline `CCVP/1` consistency verification, without itself producing trust, authority, or `Independent`.

---

## Normative reference

This overview is informational only.

All definitive rules and constraints are defined in:

- [subject.context-snapshot/1/specification](./specification.md)

In case of discrepancy, the specification prevails.
