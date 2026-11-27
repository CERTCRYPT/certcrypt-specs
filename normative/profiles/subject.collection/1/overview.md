# CERTCRYPT Collection Subject Canonicalization Profile (`subject.collection/1`) — overview

**Identifier:** `subject.collection/1`

**Label:** CERTCRYPT Collection Subject Canonicalization Profile v1

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

> This document is **informative**.
> The normative requirements for `subject.collection/1` are defined exclusively in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `subject.collection/1`?

`subject.collection/1` defines how issuer-declared collection subjects are reduced to deterministic canonical bytes under CERTCRYPT public rules.

It treats the collection subject as a declared structural object.

It does not inspect hidden leaves, infer semantic meaning from them, or validate whether the hidden material is materially consistent with the issuer declaration.

The profile exists for cases where an issuer needs to commit, without disclosing leaf contents, to:

- one exact collection root
- one exact collection commitment scheme
- one exact declared cardinality
- one exact subject-profile identifier per leaf, together with that leaf's commitment

Minimal example (the same values as the specification's §7.6 example):

```json
{
  "commitment_scheme": "collection.merkle-sha3-256/1",
  "root": "e63f94e416ea16b06ab43a58f1a8d7fb5d0c78aa26683beb72c6af1b2d16225c",
  "declared_cardinality": "4",
  "leaves": [
    {
      "profile": "subject.text/1",
      "commitment_digest_hex": "fa93083e13e2b27d57b39ce70a44d6e9cd12aa4d2ffe1683a2d833d947acba80"
    },
    {
      "profile": "subject.binary/1",
      "commitment_digest_hex": "052e490f5c6c2c14a8e2b5e84a49503e1875108f3ca770f879f3b06687251b87"
    },
    {
      "profile": "subject.email/1",
      "commitment_digest_hex": "3732762944f4b29585a88260b0f2ccfdbdf8b0a4a6ea9d1b0f0859d49988ea60"
    },
    {
      "profile": "subject.binary/1",
      "commitment_digest_hex": "9c8ecb5cef3db30635331421895e96112e93ea82a5e08f9e7836237058c4dbc8"
    }
  ]
}
```

Each leaf declares its own profile, so a single collection may bind elements of
different kinds. The leaf profile determines how that leaf's bytes are canonicalized
before hashing, which is why it is part of the signed object rather than a value
supplied alongside it.

The example above is illustrative only.

In particular, `declared_cardinality` is represented as a canonical decimal string, not as a JSON number, so the declared value remains exact under deterministic JSON canonicalization.

Under `/1`, the object is also intentionally closed:

- `declared_cardinality` must be greater than `0`, and must equal the number of entries in `leaves`
- additional fields are not permitted

---

## Why this specification exists

Some workflows need to represent a collection of externally addressable elements without disclosing those elements to CERTCRYPT.

Treating such a collection as a single opaque binary subject remains valid under [subject.binary/1](../../subject.binary/1/index.md), but that path commits only one opaque byte sequence.

`subject.collection/1` exists for a different declarative purpose:

- make collection structure explicit
- bind declared collection cardinality cryptographically
- preserve zero-data boundaries
- allow later rules and verification workflows to reason about the declared collection structure without granting CERTCRYPT semantic authority over hidden content

This profile does not authorize content inspection as a workaround.

It exists precisely so that collection-level structure can be declared without breaking zero-data design.

---

## Scope boundaries

`subject.collection/1` defines:

- the exact collection subject input boundary
- the required structural fields of the collection declaration
- the fact that `/1` is a closed object shape with no additional members
- how `canonical_bytes(subject)` are produced
- which transformations are forbidden
- how profile-level verification remains subordinate to the broader CERTCRYPT architecture

It deliberately does not define:

- issuance
- independence
- pricing or quantity rules
- semantic truth of the hidden leaves
- universal inclusion-proof semantics
- legal meaning
- institutional approval

---

## Core guarantees

Under `/1`, the profile preserves:

- exact declared collection structure under deterministic canonicalization
- closed object shape with no additional members beyond those required by §7
- profile-bound leaf semantics through the per-leaf declared profile (`leaves[].profile`)
- explicit `declared_cardinality` binding to the committed root
- zero-data compatibility with hidden leaves
- interpretation boundaries between declared structure and any higher-layer semantic, legal, or institutional outcome

---

## Relationship to other CERTCRYPT specifications

`subject.collection/1` is one of several subject profiles in the active corpus. The most relevant cross-references are listed in the subsections below.

### Relationship to `subject.binary/1`

`subject.binary/1` and `subject.collection/1` serve different declarative roles.

`subject.binary/1` commits one opaque byte sequence.

`subject.collection/1` commits one declared collection structure.

That difference matters because a container file or archive submitted as `subject.binary/1` remains one opaque subject.

A `subject.collection/1` subject, by contrast, explicitly declares that one committed root is intended to represent a collection under an exact declared structure.

This profile does not reinterpret binary containers as collections.

The issuer must choose the declaration model explicitly.

---

### Relationship to quantity rules

`subject.collection/1` does not define pricing, fairness, or capacity-consumption rules.

Those rules belong to the applicable public rules domain, including quantity semantics and economically relevant declaration handling.

What this profile contributes is narrower and structural:

- it binds the exact profile each leaf declares inside the canonicalized object
- it makes `declared_cardinality` explicit
- it binds that declaration to the collection root
- it preserves that binding under deterministic canonicalization

Any higher-layer use of that declared cardinality remains governed by separate public rules.

Acceptance of a valid `subject.collection/1` subject does not mean CERTCRYPT validated that the hidden collection materially contains the declared number of meaningful or distinct elements.

Conforming CERTCRYPT issuance or verification workflows must also reject unsupported `commitment_scheme` identifiers unless the applicable rules domain explicitly allows them and an applicable public specification defines them.

---

### Relationship to verification

CERTCRYPT certificates do not embed hidden collection leaves.

Verification against a collection subject therefore depends on the applicable path:

- collection-level evaluation may require only the collection subject declaration itself
- per-element evaluation may additionally require exact leaf material and exact scheme-specific inclusion-proof material

That remains fully compatible with independent evaluation.

It does not justify live CERTCRYPT lookup, hosted truth services, or semantic resolver authority.

---

### Anti-authority boundary

`subject.collection/1` must not be read as a content-validation profile.

It defines declared collection-subject canonicalization only.

It does not define:

- semantic validation of leaves
- proof that the hidden collection is truthful
- proof that the hidden collection is complete
- proof that the hidden collection is authoritative
- proof that the subject is `Independent`

This profile also does not close the interoperable semantics of any particular collection commitment scheme by itself.

If a rules domain relies on a scheme such as `collection.merkle-sha3-256/1`, that scheme still requires its own applicable public specification for leaf hashing, internal-node hashing, ordering, proof interpretation, and root derivation.

For the active public architecture, that closure is provided by [collection.merkle-sha3-256/1](../../../protocols/commitment/collection.merkle-sha3-256/1/index.md).

If a collection subject later participates in an `Independent` path, that meaning comes from higher-layer issuance, leaf, settlement, proof, and verifier semantics, not from this profile alone.

---

## Reading guide

Recommended order for implementers and auditors:

1. [foundation](../../../foundation/index.md)
2. [CCCP/1](../../../protocols/CCCP/1/index.md)
3. [CCSP/1](../../../protocols/CCSP/1/index.md)
4. [subject.collection/1/specification](./specification.md)
5. [collection.merkle-sha3-256/1](../../../protocols/commitment/collection.merkle-sha3-256/1/index.md)
6. [subject.binary/1](../../subject.binary/1/index.md)
7. [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md)

---

## Versioning

- **Specification identifier:** `subject.collection`
- **Specification version:** `/1`

Version `/1` defines the first canonical declarative collection-subject canonicalization profile under the active corpus.

Changes that alter the closed object shape, the canonicalization rule, the structural-field set, the forbidden-transformation list, or the boundary between declared structure and higher-layer semantics require a new major version.

Later versions do not retroactively reinterpret already valid collection canonicalizations governed by `/1`.

---

## One-line summary

**`subject.collection/1` defines the canonical declarative profile that lets an issuer commit to one exact collection structure (commitment scheme, root, declared cardinality, per-leaf profiles in `leaves[].profile`) without disclosing leaves, producing deterministic `canonical_bytes(subject)` while preserving zero-data and refusing semantic authority over hidden content.**

---

## Normative reference

This overview is informational only.

All definitive rules and constraints are defined in:

- [subject.collection/1/specification](./specification.md)
- [collection.merkle-sha3-256/1](../../../protocols/commitment/collection.merkle-sha3-256/1/index.md)

In case of discrepancy, the specification prevails.
