# CERTCRYPT Collection Subject Canonicalization Profile (`subject.collection/1`)

**Identifier:** `subject.collection/1`

**Label:** CERTCRYPT Collection Subject Canonicalization Profile v1

**Type:** Profile Specification

**Status:** Frozen

**Layer:** Layer 2 — Profiles

**Depends on:**
- [system-domain/1](../../../foundation/system-domain/1/index.md)
- [rules-domain/1](../../../foundation/rules-domain/1/index.md)
- [security-model/1](../../../foundation/security-model/1/index.md)
- [CCCP/1](../../../protocols/CCCP/1/index.md)
- [CCSP/1](../../../protocols/CCSP/1/index.md)

**Naming convention:**  
`subject.collection/1` is the formal identifier.  
CERTCRYPT Collection Subject Canonicalization Profile v1 is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.

**Audience:** Protocol implementers, verifiers, auditors

**Purpose:** Define the normative subject-profile canonicalization semantics for `subject.collection/1` within the active CERTCRYPT public architecture.

**Intended use:** `subject.collection/1` is intended to be the authoritative public specification for deriving deterministic `canonical_bytes(subject)` for issuer-declared collection subjects under CERTCRYPT public rules.

**Scope:** Defines collection-subject canonicalization boundaries, required structural fields, allowed transformations, and interpretation limits for `subject.collection/1`; higher-layer proof, settlement, quantity, and verifier-policy semantics remain out of scope except where explicitly referenced.

**Non-goals:** `subject.collection/1` does not prove truth, semantic validity, legal validity, issuer authenticity, collection completeness, collection distinctness, or Proof of Independence by itself, and MUST NOT be interpreted as a trust mark, notarization mechanism, or live service authority.

> This document is **normative**.
> All requirements expressed using MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in RFC 8174.

---

## 1. Background & rationale

`subject.collection/1` defines how issuer-declared collection subjects are reduced to deterministic `canonical_bytes(subject)` under CERTCRYPT public rules.

It exists to provide a bounded canonicalization profile for subjects that commit to hidden collections without disclosing the leaves to CERTCRYPT.

The profile defines canonicalization only.

It does not define:

- issuance semantics
- independence semantics
- inclusion-proof semantics
- verification-package semantics
- settlement or capacity semantics
- pricing or quantity rules
- truth, legal validity, or institutional endorsement

---

## 2. Scope

`subject.collection/1` defines:

- the exact collection subject input boundary
- the required structural fields of a valid collection subject
- the canonicalization rule for issuer-declared collection subjects
- forbidden transformations
- the boundary between profile-level verification and higher-layer evaluation

`subject.collection/1` does not define:

- envelope structure
- hashing algorithm choice for CCCP commitment construction
- leaf ordering semantics beyond what the declared collection commitment scheme defines
- universal inclusion-proof format
- semantic equivalence of hidden leaves
- proof-of-existence, notarization, or timestamping semantics

Those concerns remain defined elsewhere in the architecture.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

Additional terms:

- **Collection subject:** The exact JSON object intended to be certified under this profile.
- **Collection root:** The cryptographic root value committed by the collection subject.
- **Commitment scheme:** The exact versioned scheme identifier declaring how hidden leaves are committed into the collection root.
- **Declared cardinality:** The issuer-declared number of collection elements represented by the collection subject.
- **Leaf profile:** The exact subject-profile identifier declared for leaves when later workflows require leaf-level evaluation.
- **Canonical bytes:** The deterministic byte sequence produced by applying this profile.
- **JCS serialization:** UTF-8 bytes of the collection subject JSON value canonicalized under RFC 8785.

---

## 4. Design principles

`subject.collection/1` is designed around the following principles:

- **Declared structure, not discovered structure:** The profile relies on issuer-declared structure cryptographically bound into the subject. It MUST NOT depend on inspecting hidden leaves.
- **Bound declaration, not verified fact:** A declared collection cardinality MAY be bound and later relied on by other applicable public rules without becoming a semantic fact validated by CERTCRYPT.
- **Deterministic canonicalization:** The same valid collection subject MUST always produce the same `canonical_bytes(subject)`.
- **Zero-data by design:** Collection-subject certification MUST remain compatible with a zero-data architecture.
- **Proof without data custody:** Verification depends on the certificate, public rules, and verifier-held original material where required, not on retained platform data or CERTCRYPT custody of hidden leaves.
- **Interpretation boundaries:** This profile defines canonicalization only. It does not determine meaning, truth, completeness, or independence.

---

## 5. Architectural role

`subject.collection/1` is subordinate to the current architecture:

- `system-domain/1` determines which system is being evaluated
- `rules-domain/1` determines which exact public rules apply
- `security-model/1` defines the interpretation and fail-closed boundary
- `CCCP/1` defines canonicalization contexts, hashing, and commitment semantics
- `CCSP/1` defines certificate envelope structure

Under `/1`, this profile contributes only `canonical_bytes(subject)`.

It MUST NOT be interpreted as sufficient to establish:

- `Issued`
- `Independent`
- settlement validity
- quantity sufficiency
- consistency outcomes
- truth of issuer assertions

No implementation MAY present `subject.collection/1` as a standalone proof, trust mark, or notarization mechanism.

---

## 6. Collection subject input boundary

For `subject.collection/1`, the subject input MUST be one complete collection-subject JSON object.

That object MUST contain exactly the members defined by this specification for `/1`.

Implementations MUST derive `canonical_bytes(subject)` from that exact JSON value and MUST NOT reconstruct it from:

- rendered summaries
- extracted leaf lists
- unpacked archives
- inferred member counts
- transport wrappers
- external storage wrappers
- derived indexes or caches
- resolver responses
- human-readable exports

If the issuer or verifier does not possess the exact collection-subject JSON value intended to be certified, this profile cannot be applied correctly and the relevant higher-layer operation MUST fail or be treated as incomplete.

---

## 7. Required structural fields

For a valid `subject.collection/1` subject, the input JSON object MUST contain exactly the following fields, and MUST NOT contain any additional members:

- `commitment_scheme`
- `root`
- `declared_cardinality`
- `leaves`

### 7.1 `commitment_scheme`

`commitment_scheme` MUST be present.

It MUST be a string.

It MUST identify one exact versioned scheme or profile under which the hidden collection root is to be interpreted.

This specification binds the declared identifier exactly as provided.

It does not define the semantics of every possible declared scheme.

Profile-level canonicalization MAY still process unknown, unsupported, or unrecognized `commitment_scheme` identifiers as declared JSON values under this profile.

However, any conforming CERTCRYPT issuance or verification workflow MUST reject unsupported `commitment_scheme` identifiers unless their use is explicitly allowed by the applicable rules domain and backed by an applicable public specification defining that exact identifier.

### 7.2 `root`

`root` MUST be present.

It MUST represent the exact committed collection root value under the declared `commitment_scheme`.

This profile binds the declared root exactly.

It does not independently prove that the hidden leaves are materially consistent with that root.

Where the declared `commitment_scheme` is supported by the applicable workflow or otherwise defined by an applicable public specification, `root` MUST satisfy the exact encoding and length requirements defined for that scheme.

If `commitment_scheme` is `collection.merkle-sha3-256/1`, then `root` MUST be a 64-character lowercase hexadecimal string.

The `root` is a **salted** commitment to the hidden leaves: every leaf preimage binds the collection salt (§8), so the same leaf set produces a DIFFERENT `root` under a different salt. Because the salt is the certificate anchor's `nonce_hex`, a `root` is meaningful only relative to the certificate that declares it, and two certificates over identical leaves do not share a root. Neither `root` nor any individual `leaf_hash` is a stable fingerprint of the leaf material across certificates, and neither MAY be used as a content identifier, a deduplication key, or a cross-issuer correlator. This is what allows leaf hashes to be carried inside a `verification-package/1` (§11 of that specification) without creating correlatable identifiers on the protocol surface.

### 7.3 `declared_cardinality`

`declared_cardinality` MUST be present.

It MUST be a string containing one canonical unsigned base-10 integer.

It MUST NOT contain a sign.

It MUST NOT contain leading zeros.

Its numeric value MUST be greater than `0`.

Its numeric value MUST be less than or equal to `18446744073709551615` (2^64 − 1), so every conforming implementation can parse it into a fixed-width unsigned 64-bit integer for the commitment-scheme leaf-count check without overflow or arbitrary-precision divergence. A value exceeding this bound is non-conformant (the profile does not apply; fail-closed).

Under this profile, `declared_cardinality` is a cryptographically bound issuer declaration.

It MUST NOT be interpreted, by itself, as proof that hidden leaves are truthful, distinct, complete, or materially countable in that amount under an external semantic standard.

Under other applicable public rules, `declared_cardinality` MAY be used as an input to deterministic economic, admissibility, or quantity semantics.

Such use MUST NOT be interpreted as CERTCRYPT validating the semantic truthfulness, completeness, distinctness, or external countability of the underlying hidden elements.

It means only that the issuer committed to that declaration in a form later workflows MAY rely on under their own exact public rules.

Explicit `declared_cardinality` is specific to `subject.collection/1` under `/1`.

Its presence here MUST NOT be interpreted as requiring all other subject profiles to carry an equivalent fixed cardinality field merely to contribute one effective declared unit under separate public quantity rules.

### 7.4 `leaves`

`leaves` MUST be present.

It MUST be a JSON array with at least one entry. An empty array is invalid (the scheme
prohibits empty trees).

Each entry MUST be a JSON object containing EXACTLY the following members, and MUST NOT
contain any additional members:

- `profile`
- `commitment_digest_hex`

Entries MUST be in leaf order. The position of an entry IS the leaf index used by
`collection.merkle-sha3-256/1` inclusion proofs.

#### 7.4.1 `leaves[].profile`

`leaves[].profile` MUST be a string identifying one exact declared subject-profile
identifier, matching the same token grammar as `subjects[].profile` in
[CCSP/1](../../../protocols/CCSP/1/index.md).

Each leaf declares its OWN profile. A collection MAY therefore be **heterogeneous**:
different leaves MAY declare different profiles, and there is no collection-wide leaf
profile. There is no abbreviated form for the homogeneous case — a collection whose
leaves all share one profile still declares it per entry, so implementations have a
single code path.

The declared profile is load-bearing, not descriptive: it determines how that leaf's
bytes are canonicalized before hashing (`subject.text/1` normalizes line endings,
`subject.binary/1` is byte-identity), and it is bound into the leaf preimage
(`collection.merkle-sha3-256/1` §10). A verifier MUST use the profile declared for
that leaf and MUST NOT substitute another.

#### 7.4.2 `leaves[].commitment_digest_hex`

`leaves[].commitment_digest_hex` MUST be a JSON string of exactly 64 lowercase hex
characters matching `^[0-9a-f]{64}$`.

It is the leaf's `leaf_hash` under `collection.merkle-sha3-256/1` §10.

**This is NOT computed like `subjects[].commitment_digest_hex`.** The names are
deliberately parallel — each entry declares what it is and its commitment — but the
constructions differ:

```text
subject: SHA3-256(ASCII(nonce_hex) || ASCII(SHA3-256(canonical_bytes)))   [CCCP/1]
leaf:    SHA3-256(tag || salt || profile || canonical_bytes)              [§10]
```

The leaf construction carries a domain-separation tag (it is folded into a Merkle tree
and MUST be distinguishable from a node hash) and binds the profile inside the
preimage. An implementation MUST NOT compute a leaf commitment with the CCCP/1 subject
formula.

#### 7.4.3 Cardinality agreement

`declared_cardinality` MUST equal the number of entries in `leaves`. A mismatch MUST be
rejected as structurally invalid.

Both are retained deliberately: `declared_cardinality` is the value the economic layer
reads (`capacity.commitment/1`), and that dependency should not have to count an array.
Redundant-and-checked is safer than derived-and-assumed.

#### 7.4.4 What `leaves` discloses

Because every leaf declares its profile, the descriptor reveals the collection's
**composition by profile** — for example, that a set of eight holds three texts and
five binaries. This is more than a single collection-wide leaf profile disclosed.

This is accepted and intentional. The cardinality was already public, every leaf
commitment is salted per operation (`§8`), and composition by profile does not permit
content recovery or cross-certificate correlation. Implementations MUST NOT treat leaf
profiles as confidential.

---

### 7.5 No additional fields

The input JSON object MUST NOT contain members other than:

- `commitment_scheme`
- `root`
- `declared_cardinality`
- `leaves`

Implementations MUST reject any input object containing additional members.

### 7.6 Minimal example

The following JSON object is a minimal illustrative example of a `subject.collection/1` subject:

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

The example is heterogeneous deliberately: a homogeneous collection is the easier read,
and an implementer who only ever sees one profile is the one who hard-codes it.

As declared inside the certificate subject that commits to it:

```json
{
  "profile": "subject.collection/1",
  "commitment_digest_hex": "93fa5f1b5115b0563dce76c3d07e99d29886cc1b819d7ee2bc92c857a549c892",
  "collection": { "...": "the object above" }
}
```

This example is informative only.

Profile conformance is determined by the rules above, not by this example.

---

## 8. Collection salt

`collection.merkle-sha3-256/1` requires a salt bound into every leaf preimage but
does not define its origin. Under `subject.collection/1`, that salt MUST be the
certificate anchor's `nonce_hex`, taken as its exact ASCII bytes.

The salt is NOT a structural field of the collection subject. It MUST NOT appear in
the canonicalized subject object, and the field set in §7 is exhaustive.

Consequences that implementations and readers MUST expect:

- The same ordered list of leaf values under the same per-leaf profiles produces a
  DIFFERENT `root` in a different operation, because the anchor nonce differs. A root
  is therefore meaningful only relative to the certificate that declares it, and two
  certificates over identical content are not expected to share a root.
- A `leaf_hash` is not a stable identifier of its leaf value across certificates. It
  MUST NOT be treated as a content identifier, a deduplication key, or a cross-issuer
  correlator.
- A verifier that recomputes leaf hashes MUST take the salt from the anchor of the
  certificate under verification, never from a value supplied alongside the leaves.

This binding is what allows leaf hashes to be published inside a
`verification-package/1` without creating correlatable content identifiers on the
protocol surface.

---

## 9. Canonicalization rule

`subject.collection/1` defines a single canonicalization model.

Field-set conformance (§7, including the exact four-member set of §7.5) is a **precondition of canonicalization**, not a separable later check. `canonical_bytes(subject)` is defined ONLY for an object satisfying §7 in full; for any other object the profile does not apply and the implementation MUST fail closed. A conforming issuer and a conforming verifier therefore never agree on a commitment over a non-conformant object.

For all subjects governed by `subject.collection/1`:

- the input subject MUST be a valid JSON object satisfying §7
- the source material MUST be parsed as strict JSON: if any object in it, at any depth, contains the same member name twice — names compared after their escape sequences are decoded, so `"root"` and `"r\u006fot"` are the same name — the material is non-conformant and the profile does not apply (fail-closed). No first-wins, last-wins, or merge reading is permitted. Repeated elements of an array are ordinary data, not repeated members ([CCSP/1](../../../protocols/CCSP/1/specification.md) Section 8.1 applies the same rule to certificates)
- `canonical_bytes(subject)` MUST equal the UTF-8 bytes of the RFC 8785 JCS canonical serialization of that JSON value
- implementations MUST canonicalize the parsed JSON value, not the original source bytes
- implementations MUST preserve the exact string, boolean, array, object, and null semantics of the input JSON value
- the object contains no JSON number tokens (every field of §7 is a string), so RFC 8785 number serialization never applies under this profile

There are no alternative canonicalization modes under `/1`.

Because `declared_cardinality` is required to be represented as a canonical unsigned integer string, implementations MUST NOT reinterpret it numerically in a way that changes the canonical JSON value or collapses distinct invalid representations into one accepted value.

---

## 10. Forbidden transformations

Implementations applying `subject.collection/1` MUST NOT:

- infer `declared_cardinality` from hidden leaves
- recompute `declared_cardinality` by unpacking archives or containers
- normalize or rewrite the declared `commitment_scheme`
- for supported or otherwise publicly defined schemes, accept a `root` encoding or length that does not satisfy the declared `commitment_scheme`
- substitute another leaf profile for the one a leaf declares
- accept additional members not defined by this profile
- canonicalize only a subset of the collection-subject object
- reconstruct the collection subject from a non-authoritative source
- treat semantically similar hidden collections as equivalent if their declared collection subject differs

If a workflow requires any of those transformations, that workflow is outside `subject.collection/1`.

---

## 11. Informational attributes

A certificate or higher-layer artifact MAY carry informational attributes associated with a `subject.collection/1` subject.

Such attributes:

- MUST be informational only
- MUST NOT affect `canonical_bytes(subject)`
- MUST NOT participate in CCCP commitment computation unless another normative specification explicitly says so
- MUST NOT be used to infer truth, authority, or independence by themselves

Profile conformance MUST be determined from the exact collection-subject JSON value and declared profile only, not from informational metadata.

---

## 12. Relationship to CCCP and CCSP

`subject.collection/1` is a subject-specific profile under [CCCP/1](../../../protocols/CCCP/1/index.md).

Its output constitutes `canonical_bytes(subject)` for use by CCCP-governed hashing and commitment construction.

`subject.collection/1` MUST NOT redefine, weaken, or bypass any CCCP requirement.

When referenced from certificates serialized under [CCSP/1](../../../protocols/CCSP/1/index.md), the subject's declared `profile` identifies this specification and nothing more: it confers no authority and asserts nothing about the subject's content.

The presence of `subject.collection/1` in a certificate envelope does not by itself make that certificate trustworthy, complete, or independent.

---

## 13. Verification boundary

Profile-level verification under `subject.collection/1` is limited to verifying that:

- the declared `profile` is `subject.collection/1`
- the supplied collection-subject JSON value is processed under the exact canonicalization rule defined here
- the required structural fields are present and well-formed under this profile
- any scheme-specific `root` constraints applicable to the declared `commitment_scheme` are satisfied where that scheme is supported or otherwise defined by an applicable public specification
- the input object contains no additional members
- the resulting canonical bytes are the bytes expected by the applicable higher-layer path

This profile does not define a standalone verifier outcome taxonomy for `Issued` or `Independent`.

This profile also does not define a universal leaf-inclusion verifier algorithm.

Any workflow claiming element-level evaluation MUST additionally rely on:

- the exact declared `commitment_scheme`
- the exact profile each leaf declares
- any applicable higher-layer public rules defining leaf-level proof material
- verifier-held leaf material where required by that workflow

No implementation MAY claim profile success under `subject.collection/1` as if that alone established valid independence, truth, completeness, or authority.

---

## 14. Relationship to `subject.binary/1`

`subject.collection/1` MUST NOT be used to reinterpret arbitrary opaque binary subjects as collections after the fact.

If the intended subject is one opaque byte sequence, implementations MUST use [subject.binary/1](../../subject.binary/1/index.md) or another applicable subject profile.

If the intended subject is an issuer-declared committed collection, implementations MAY use `subject.collection/1` provided the input satisfies the requirements of this specification.

Submitting an archive, container, or other opaque binary artifact under `subject.binary/1` does not implicitly create or declare a `subject.collection/1` subject.

---

## 15. Relationship to leaf semantics

`subject.collection/1` operates at subject level.

It defines a canonicalized declared subject structure only.

It MUST NOT be interpreted as:

- a leaf
- a submission-set unit
- a leaf-closure artifact
- a settlement container
- a fixation request

Leaf semantics remain governed by the applicable leaf and settlement specifications.

`subject.collection/1` and leaf semantics MUST remain orthogonal.

Accordingly:

- a collection subject MAY participate in a leaf
- a leaf MAY contain zero, one, or multiple collection subjects under the applicable rules
- leaf-level aggregation MUST NOT, by itself, redefine the declared cardinality of a collection subject
- leaf inclusion of a collection subject MUST NOT convert that subject into a leaf-equivalent artifact

This profile does not define the fixation unit.

It defines only one subject-level declarative structure that MAY later be bound into a leaf under other applicable public rules.

---

## 16. Anti-authority boundary

`subject.collection/1` MUST NOT be described, implemented, or marketed as a collection-validation, notarization, timestamping, anchoring, or proof-of-existence system.

This profile:

- does not prove that hidden leaves are true
- does not prove that hidden leaves are complete
- does not prove that hidden leaves are distinct
- does not prove that hidden leaves are authoritative
- does not prove `Independent`

It defines only how an issuer-declared collection subject is transformed into deterministic canonical bytes for use by higher-layer CERTCRYPT semantics.

If a system can reproduce the same claim using only hidden parsing, heuristic counting, or private inspection of subject internals, that claim does not come from `subject.collection/1` as defined here.

---

## 17. Versioning & extensibility

- **Profile identifier:** `subject.collection`
- **Profile version:** `/1`

Any change that alters canonical byte output, required field set, collection-subject input boundary, or forbidden-transformation behavior MUST require a new major version.

No optional canonicalization behavior is permitted under `/1`.

Additional collection commitment schemes MAY be recognized by other applicable public specifications without changing this profile, provided they do not alter the canonicalization model defined here.

---

## 18. References

- CERTCRYPT Specifications
    - [security-model/1 — CERTCRYPT Security Model](../../../foundation/security-model/1/index.md)
    - [system-domain/1 — CERTCRYPT System Domain](../../../foundation/system-domain/1/index.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../../foundation/rules-domain/1/index.md)
    - [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../../protocols/CCCP/1/index.md)
    - [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../../protocols/CCSP/1/index.md)
    - [subject.binary/1 — CERTCRYPT Binary Subject Canonicalization Profile](../../subject.binary/1/index.md)
    - [collection.merkle-sha3-256/1 — CERTCRYPT Merkle Collection Commitment Scheme](../../../protocols/commitment/collection.merkle-sha3-256/1/index.md)
    - [settlement/submission-set/1 — submission-set/1 · CERTCRYPT Submission Set Specification](../../../protocols/settlement/submission-set/1/index.md)
    - [settlement/capacity.commitment/1 — capacity.commitment/1 · CERTCRYPT Capacity Commitment Specification](../../../ecosystem/settlement/capacity.commitment/1/index.md)
    - [verification/verifier-toolkit/1 — verifier-toolkit/1 · CERTCRYPT Verifier Toolkit Specification](../../../ecosystem/verification/verifier-toolkit/1/index.md)
    - [subject.text/1 — CERTCRYPT Plain Text Subject Canonicalization Profile](../../subject.text/1/index.md)
    - [verification-package/1 — CERTCRYPT Verification Package Specification](../../../ecosystem/verification/verification-package/1/index.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
    - [RFC 8785 — JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785)

---

**End of subject.collection/1**
