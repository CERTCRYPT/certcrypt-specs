# CERTCRYPT Context Snapshot Subject Canonicalization Profile (`subject.context-snapshot/1`)

**Identifier:** `subject.context-snapshot/1`

**Label:** CERTCRYPT Context Snapshot Subject Canonicalization Profile v1

**Type:** Profile Specification

**Status:** Frozen

**Layer:** Layer 2 — Profiles

**Depends on:**
- [system-domain/1](../../../foundation/system-domain/1/index.md)
- [rules-domain/1](../../../foundation/rules-domain/1/index.md)
- [security-model/1](../../../foundation/security-model/1/index.md)
- [CCCP/1](../../../protocols/CCCP/1/index.md)
- [CCSP/1](../../../protocols/CCSP/1/index.md)
- [CCVP/1](../../../protocols/CCVP/1/index.md)

**Naming convention:**  
`subject.context-snapshot/1` is the formal identifier.  
CERTCRYPT Context Snapshot Subject Canonicalization Profile v1 is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.

**Audience:** Protocol implementers, verifiers, auditors

**Purpose:** Define the normative subject-profile canonicalization semantics for `subject.context-snapshot/1` within the CERTCRYPT public architecture.

**Intended use:** `subject.context-snapshot/1` is intended to be the authoritative public specification for deriving deterministic `canonical_bytes(subject)` for subjects declaring this profile under CERTCRYPT public rules.

**Scope:** Defines canonicalization boundaries, allowed transformations, and interpretation limits for `subject.context-snapshot/1`; higher-layer proof, settlement, and consistency semantics remain out of scope except where explicitly referenced.

**Non-goals:** `subject.context-snapshot/1` does not prove truth, semantic validity, legal validity, issuer authenticity, or Proof of Independence by itself, and MUST NOT be interpreted as a trust mark, notarization mechanism, or live service authority.

> This document is **normative**.
> All requirements expressed using MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in RFC 8174.

---

## 1. Background & rationale

`subject.context-snapshot/1` defines how context snapshot subjects are reduced to deterministic `canonical_bytes(subject)` under CERTCRYPT public rules.

It exists to provide a narrow canonicalization profile for context snapshot artifacts used by [CCVP/1](../../../protocols/CCVP/1/index.md).

The profile defines canonicalization only.

It does not define:

- issuance semantics
- independence semantics
- consistency outcome semantics
- settlement or capacity semantics
- truth, legal validity, or institutional endorsement

The term "context" is declarative and does not imply authority, enforcement, or compliance.

---

## 2. Scope

`subject.context-snapshot/1` defines:

- the exact context-snapshot subject boundary
- the canonicalization rule for context snapshot subjects
- forbidden transformations
- the boundary between profile-level verification and higher-layer consistency verification

`subject.context-snapshot/1` does not define:

- envelope structure
- hashing algorithm choice
- commitment construction
- declared context namespace selection
- consistency resolution
- trust, truth, or authority semantics

Those concerns remain defined elsewhere in the architecture.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

Additional terms:

- **Context snapshot subject:** The exact context snapshot JSON value intended to be certified under this profile.
- **Snapshot object:** The JSON object governed by this profile, typically carried as `payload.snapshot` in a context snapshot certificate.
- **Canonical bytes:** The deterministic byte sequence produced by applying this profile.
- **JCS serialization:** UTF-8 bytes of the context snapshot JSON value canonicalized under RFC 8785.

---

## 4. Design principles

`subject.context-snapshot/1` is designed around the following principles:

- **Governed JSON exactness:** The governed snapshot JSON value MUST be canonicalized exactly as carried, without reconstruction or heuristic reinterpretation.
- **Deterministic canonicalization:** The same valid context snapshot JSON value MUST always produce the same `canonical_bytes(subject)`.
- **Zero-data by design:** Context-snapshot certification MUST remain compatible with a zero-data architecture.
- **Proof without data custody:** Verification depends on the certificate and public rules, not on retained platform state.
- **Interpretation boundaries:** Canonicalization does not create authority, compliance, or consistency outcomes by itself.

---

## 5. Architectural role

`subject.context-snapshot/1` is subordinate to the architecture:

- `system-domain/1` determines which system is being evaluated
- `rules-domain/1` determines which exact public rules apply
- `security-model/1` defines the interpretation and fail-closed boundary
- `CCCP/1` defines canonicalization contexts, hashing, and commitment semantics
- `CCSP/1` defines certificate envelope structure
- `CCVP/1` defines context snapshot meaning and verifier-side consistency behavior

Under `/1`, this profile contributes only `canonical_bytes(subject)`.

It MUST NOT be interpreted as sufficient to establish:

- `Issued`
- `Independent`
- `consistency-match`
- settlement validity
- truth of issuer assertions

No implementation MAY present `subject.context-snapshot/1` as a standalone proof, trust mark, or authority mechanism.

---

## 6. Context snapshot input boundary

For `subject.context-snapshot/1`, the subject input MUST be one complete context snapshot JSON object.

Under `CCVP/1`, that object is **exactly `payload.snapshot`** — the complete JSON value at that member of the context snapshot certificate, with no other member added or removed. Implementations MUST NOT canonicalize the enclosing `payload`, a superset, or a subset; the subject boundary is the `payload.snapshot` value in full.

That governed JSON value MAY include fields that are not used directly by CCVP/1 consistency outcome rules, including optional declarative references such as `policy_refs`.

Implementations MUST derive `canonical_bytes(subject)` from that exact JSON value and MUST NOT reconstruct it from:

- rendered summaries
- extracted table rows
- partial fields
- transport wrappers
- external storage wrappers
- derived indexes or caches
- resolver responses
- human-readable exports

If the issuer or verifier does not possess the exact context snapshot JSON value intended to be certified, this profile cannot be applied correctly and the relevant higher-layer operation MUST fail or be treated as incomplete.

---

## 7. Canonicalization rule

`subject.context-snapshot/1` defines a single canonicalization model.

For all subjects governed by `subject.context-snapshot/1`:

- the input subject MUST be a valid JSON object
- the source material MUST be parsed as strict JSON: if any object in it, at any depth, contains the same member name twice — names compared after their escape sequences are decoded, so `"status"` and `"st\u0061tus"` are the same name — the material is non-conformant and the profile does not apply (fail-closed). No first-wins, last-wins, or merge reading is permitted. Repeated elements of an array are ordinary data, not repeated members ([CCSP/1](../../../protocols/CCSP/1/specification.md) Section 8.1 applies the same rule to certificates)
- `canonical_bytes(subject)` MUST equal the UTF-8 bytes of the RFC 8785 JCS canonical serialization of that JSON value
- implementations MUST canonicalize the parsed JSON value, not the original source bytes
- implementations MUST preserve the exact string, boolean, array, object, and null semantics of the input JSON value

### 7.1 Number discipline

JSON number serialization is the hardest part of RFC 8785 to reproduce byte-identically across languages (large integers beyond 2^53, exponent and trailing-zero formatting, `-0`). To guarantee cross-language convergence, every numeric-looking value in the snapshot object MUST be carried as a **JSON string**, not a JSON number. A conforming snapshot object MUST NOT contain any JSON number token at any depth (in members, array elements, or nested objects). A snapshot carrying a JSON number is non-conformant and the profile does not apply to it (fail-closed). Booleans and nulls are not numbers: they are permitted and preserved as such (§7, §8).

This mirrors the discipline of [subject.collection/1](../../subject.collection/1/index.md), where quantities such as `declared_cardinality` are strings. It removes the only practical RFC 8785 divergence vector for this profile: with no JSON numbers present, JCS reduces to deterministic key ordering and string escaping, which conforming RFC 8785 libraries implement identically.

There are no alternative canonicalization modes under `/1`.

---

## 8. Forbidden transformations

Implementations applying `subject.context-snapshot/1` MUST NOT:

- drop fields from the snapshot object
- add fields to the snapshot object
- rewrite strings semantically
- coerce booleans or nulls into strings, or strings into booleans or nulls
- sort or reorder arrays
- merge duplicate semantic entries
- normalize timestamps beyond ordinary JSON string preservation
- canonicalize only a subset of the snapshot object
- reconstruct the snapshot object from a non-authoritative source
- assign normative meaning to fields not defined by the governing higher-layer protocol solely because they are present in the subject JSON

Array order is significant: JCS does not reorder array elements, so the issuer's element order is bound into `canonical_bytes`. Two snapshots with identical element content but different array order produce different canonical bytes and are distinct snapshots. The issuer is responsible for emitting a stable, deterministic array order; likewise a single deterministic RFC 3339 spelling for any timestamp string, since `2026-04-12T10:00:00Z` and `2026-04-12T10:00:00.000Z` are different byte strings under this profile.

If a workflow requires any of those transformations, that workflow is outside `subject.context-snapshot/1`.

---

## 9. Informational attributes

A certificate or higher-layer artifact MAY carry informational attributes associated with a `subject.context-snapshot/1` subject.

Such attributes:

- MUST be informational only
- MUST NOT affect `canonical_bytes(subject)`
- MUST NOT participate in CCCP commitment computation unless another normative specification explicitly says so
- MUST NOT be used to infer truth, authority, or consistency outcome by themselves

Profile conformance MUST be determined from the governed snapshot JSON value and declared profile only, not from informational metadata.

Fields present in the governed snapshot JSON value but not defined normatively by the applicable higher-layer protocol remain part of canonicalization if present, but MUST NOT receive independent normative interpretation unless another applicable public specification explicitly defines that meaning.

Canonicalization of such fields, including optional `policy_refs`, does not imply semantic enforcement, policy compliance, or policy validation.

---

## 10. Relationship to CCCP and CCSP

`subject.context-snapshot/1` is a subject-specific profile under [CCCP/1](../../../protocols/CCCP/1/index.md).

Its output constitutes `canonical_bytes(subject)` for use by CCCP-governed hashing and commitment construction.

`subject.context-snapshot/1` MUST NOT redefine, weaken, or bypass any CCCP requirement.

When referenced from certificates serialized under [CCSP/1](../../../protocols/CCSP/1/index.md), the subject's declared `profile` identifies this specification and nothing more: it confers no authority and asserts nothing about the subject's content.

The presence of `subject.context-snapshot/1` in a certificate envelope does not by itself make that certificate consistency-valid, trustworthy, or independent.

---

## 11. Relationship to CCVP

`subject.context-snapshot/1` does not replace [CCVP/1](../../../protocols/CCVP/1/index.md).

It exists only to define the canonical subject boundary for context snapshot artifacts carried under CCVP/1.

[CCVP/1](../../../protocols/CCVP/1/specification.md) uses this profile in three places, and only there:

- **Classification.** A context snapshot certificate carries exactly one subject whose `profile` is `subject.context-snapshot/1` (CCVP/1 Section 5.1).
- **Binding.** That subject's `commitment_digest_hex` MUST equal the [CCCP/1](../../../protocols/CCCP/1/index.md) commitment `SHA3-256(ASCII(nonce_hex) || ASCII(SHA3-256(canonical_bytes(payload.snapshot))))`, recomputed by the verifier from the `payload.snapshot` the certificate carries. A snapshot that fails the preconditions of Section 7 — a repeated member name at any depth, or a JSON number anywhere — has no canonical bytes, so the commitment cannot be recomputed and the certificate is a non-conformant context snapshot under CCVP/1. Booleans and nulls are ordinary values: CCVP/1 uses `null` for an open `valid_to`, and both are preserved by canonicalization.
- **Tie comparison.** When two snapshots tie on effective time, CCVP/1 compares the canonical bytes this profile produces (CCVP/1 Section 9).

The profile assigns no meaning to any field of the snapshot. In particular:

- the snapshot issuer is the key that signed the certificate ([CCVP/1](../../../protocols/CCVP/1/specification.md) Section 5.1), never a field inside the snapshot
- declared context namespace selection remains defined by `CCVP/1`
- context snapshot eligibility remains defined by `CCVP/1`
- verifier-side consistency outcomes remain defined by `CCVP/1`

This profile MUST NOT be treated as a second consistency protocol.

---

## 12. Verification boundary

Profile-level verification under `subject.context-snapshot/1` is limited to verifying that:

- the declared `profile` is `subject.context-snapshot/1`
- the supplied JSON value is treated as one complete context snapshot subject
- the resulting canonical bytes are the bytes expected by the applicable higher-layer path

This profile does not define a standalone verifier outcome taxonomy for `Issued`, `Independent`, or consistency outcomes.

Those outcomes are defined by higher-layer public rules and verifier behavior, including:

- [security-model/1](../../../foundation/security-model/1/index.md)
- [CCVP/1](../../../protocols/CCVP/1/index.md)
- [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md)

No implementation MAY claim profile success under `subject.context-snapshot/1` as if that alone established valid independence, truth, or contextual authority.

---

## 13. Anti-authority boundary

`subject.context-snapshot/1` MUST NOT be described, implemented, or marketed as an authority layer, notarization, timestamping, or proof-of-existence system.

This profile:

- does not prove that the context snapshot is true
- does not prove that the context snapshot is institutionally authoritative
- does not prove that issuance was consistent
- does not prove `Independent`

It defines only how a context snapshot subject is transformed into deterministic canonical bytes for use by higher-layer CERTCRYPT semantics.

---

## 14. Security and interpretation boundaries

`subject.context-snapshot/1`:

- does not prove authorship by itself
- does not prove declared-context legitimacy by itself
- does not prove legal validity
- does not validate factual correctness
- does not convert declared context into subject truth

Any interpretation beyond exact context-snapshot canonicalization remains outside this profile and MUST be handled, if at all, by other layers under their own public rules.

---

## 15. Versioning & extensibility

- **Profile identifier:** `subject.context-snapshot`
- **Profile version:** `/1`

Future versions MAY refine the profile only through a new major version.

Any change that alters canonical byte output, context-snapshot input boundary, or forbidden-transformation behavior MUST require a new major version.

---

## 16. References

- CERTCRYPT Specifications
    - [security-model/1 — CERTCRYPT Security Model](../../../foundation/security-model/1/index.md)
    - [system-domain/1 — CERTCRYPT System Domain](../../../foundation/system-domain/1/index.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../../foundation/rules-domain/1/index.md)
    - [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../../protocols/CCCP/1/index.md)
    - [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../../protocols/CCSP/1/index.md)
    - [CCVP/1 — CERTCRYPT Consistency Verification Protocol](../../../protocols/CCVP/1/index.md)
    - [verification/verifier-toolkit/1 — verifier-toolkit/1 · CERTCRYPT Verifier Toolkit Specification](../../../ecosystem/verification/verifier-toolkit/1/index.md)
    - [subject.collection/1 — CERTCRYPT Collection Subject Canonicalization Profile](../../subject.collection/1/index.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
    - [RFC 8785 — JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785)

---

**End of subject.context-snapshot/1**
