# CERTCRYPT Binary Subject Canonicalization Profile (`subject.binary/1`)

**Identifier:** `subject.binary/1`

**Label:** CERTCRYPT Binary Subject Canonicalization Profile v1

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
`subject.binary/1` is the formal identifier.  
CERTCRYPT Binary Subject Canonicalization Profile v1 is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.

**Audience:** Protocol implementers, verifiers, auditors

**Purpose:** Define the normative subject-profile canonicalization semantics for `subject.binary/1` within the active CERTCRYPT public architecture.

**Intended use:** `subject.binary/1` is intended to be the authoritative public specification for deriving deterministic `canonical_bytes(subject)` for subjects declaring this profile under CERTCRYPT public rules.

**Scope:** Defines canonicalization boundaries, allowed transformations, and interpretation limits for `subject.binary/1`; higher-layer proof, settlement, and consistency semantics remain out of scope except where explicitly referenced.

**Non-goals:** `subject.binary/1` does not prove truth, semantic validity, legal validity, issuer authenticity, or Proof of Independence by itself, and MUST NOT be interpreted as a trust mark, notarization mechanism, or live service authority.

> This document is **normative**.
> All requirements expressed using MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in RFC 8174.

---

## 1. Background & rationale
`subject.binary/1` defines how opaque binary subjects are reduced to deterministic `canonical_bytes(subject)` under CERTCRYPT public rules.

It exists to provide a conservative canonicalization profile for binary material whose structure, encoding, or serialization must not be transformed during canonicalization.

The profile defines canonicalization only.

It does not define:

- issuance semantics
- independence semantics
- consistency semantics
- verification-package semantics
- settlement or capacity semantics
- truth, legal validity, or institutional endorsement

---

## 2. Scope

`subject.binary/1` defines:

- the exact binary input boundary
- the canonicalization rule for opaque binary subjects
- forbidden transformations
- the boundary between profile-level verification and higher-layer evaluation

`subject.binary/1` does not define:

- envelope structure
- hashing algorithm choice
- commitment construction
- subject meaning
- semantic equivalence across different byte serializations
- proof-of-existence, notarization, or timestamping semantics

Those concerns remain defined elsewhere in the architecture.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

Additional terms:

- **Binary subject:** An external subject treated as an opaque byte sequence.
- **Input bytes:** The exact byte sequence supplied for canonicalization under this profile.
- **Canonical bytes:** The deterministic byte sequence produced by applying this profile.
- **Opaque treatment:** Processing in which bytes are not parsed, normalized, or semantically transformed.

---

## 4. Design principles

`subject.binary/1` is designed around the following principles:

- **Deterministic canonicalization:** The same valid binary input MUST always produce the same `canonical_bytes(subject)`.
- **Byte preservation:** This profile MUST avoid semantic reinterpretation or structural rewriting of opaque binary material.
- **Zero-data by design:** Certificates and commitments derived from this profile MUST remain compatible with a zero-data architecture.
- **Proof without data custody:** Verification depends on the certificate, public rules, and verifier-held original material, not on platform custody of the binary subject.
- **Interpretation boundaries:** This profile defines canonicalization only. It does not determine meaning, truth, or independence.

---

## 5. Architectural role

`subject.binary/1` is subordinate to the current architecture:

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
- consistency outcomes
- truth of issuer assertions

No implementation MAY present `subject.binary/1` as a standalone proof, trust mark, or notarization mechanism.

---

## 6. Binary input boundary

For `subject.binary/1`, the subject input MUST be the exact byte sequence intended to be certified or verified.

Implementations MUST derive `canonical_bytes(subject)` directly from that byte sequence and MUST NOT reconstruct it from:

- decoded text
- rendered previews
- extracted container members
- parsed internal objects
- filesystem metadata
- transport wrappers
- content-management exports
- storage backends or resolver responses

If the verifier or issuer does not possess the exact intended byte sequence, the profile cannot be applied correctly and the relevant higher-layer operation MUST fail or be treated as incomplete.

---

## 7. Canonicalization rule

`subject.binary/1` defines a single canonicalization model.

For all subjects governed by `subject.binary/1`:

- `canonical_bytes(subject)` MUST equal the exact input bytes
- implementations MUST treat the subject as an opaque byte array
- implementations MUST NOT decode, transcode, normalize, decompress, reserialize, reinterpret, or mutate any bytes
- implementations MUST NOT inspect internal structure in a way that affects canonical output

There are no alternative canonicalization modes under `/1`.

### 7.1 Edge cases

- **Empty subject.** The zero-length byte sequence is a valid `subject.binary/1` subject. Its canonical bytes are the zero-length sequence; `subject_local_digest_hex = SHA3-256("")` = `a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a`.
- **No length limit.** The profile imposes no maximum size. `canonical_bytes` is the complete ordered byte sequence regardless of how it is read (streamed or buffered); implementations MUST NOT truncate. Because `canonical_bytes` are the input bytes, a digest computed in chunks equals a digest of the whole sequence; this is what lets a verifier deliver a digest in place of the bytes under [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md) §8.5.7.
- **Embedded NUL and arbitrary bytes.** Every byte value, including `0x00`, is preserved verbatim; implementations MUST NOT treat any byte as a terminator.

### 7.2 Commitment construction is defined by CCCP/1

This profile produces only `canonical_bytes(subject)`. Hashing and commitment are defined by [CCCP/1](../../../protocols/CCCP/1/index.md) and MUST NOT be re-derived here. In particular, CCCP/1 §8.1 requires the commitment to concatenate the **ASCII bytes of the lowercase hex strings** `nonce_hex` and `subject_local_digest_hex` — the hex strings MUST NOT be decoded to their 32 raw bytes before concatenation. This is the most common cross-language commitment error; implementers working in byte-oriented languages MUST follow CCCP/1 §8.1 exactly.

---

## 8. Forbidden transformations

Implementations applying `subject.binary/1` MUST NOT:

- normalize line endings
- strip BOMs
- change character encoding
- decompress compressed payloads
- unpack archives or containers
- reorder internal members
- rewrite metadata
- canonicalize JSON, XML, PDF, office, media, archive, or executable internals
- infer semantic equivalence across different byte serializations

If a workflow requires any of those transformations, that workflow is outside `subject.binary/1`.

---

## 9. Informational attributes

A certificate or higher-layer artifact MAY carry informational attributes associated with a `subject.binary/1` subject.

Such attributes:

- MUST be informational only
- MUST NOT affect `canonical_bytes(subject)`
- MUST NOT participate in CCCP commitment computation unless another normative specification explicitly says so
- MUST NOT be used to infer semantic equivalence, truth, or authority

Profile conformance MUST be determined from the subject bytes and declared profile only, not from informational metadata.

---

## 10. Relationship to CCCP and CCSP

`subject.binary/1` is a subject-specific profile under [CCCP/1](../../../protocols/CCCP/1/index.md).

Its output constitutes `canonical_bytes(subject)` for use by CCCP-governed hashing and commitment construction.

`subject.binary/1` MUST NOT redefine, weaken, or bypass any CCCP requirement.

When referenced from certificates serialized under [CCSP/1](../../../protocols/CCSP/1/index.md), the subject's declared `profile` identifies this specification and nothing more: it confers no authority and asserts nothing about the subject's content.

The presence of `subject.binary/1` in a certificate envelope does not upgrade the envelope into any specific higher-layer meaning.

---

## 11. Verification boundary

Profile-level verification under `subject.binary/1` is limited to verifying that:

- the declared `profile` is `subject.binary/1`
- the supplied bytes are processed under the exact canonicalization rule defined here
- the resulting canonical bytes are the bytes expected by the applicable higher-layer path

This profile does not define a standalone verifier outcome taxonomy for `Issued` or `Independent`.

Those outcomes are defined by higher-layer public rules and verifier behavior, including:

- [security-model/1](../../../foundation/security-model/1/index.md)
- [verification-package/1](../../../ecosystem/verification/verification-package/1/index.md)
- [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md)

No implementation MAY claim profile success under `subject.binary/1` as if that alone established valid independence, truth, or authority.

---

## 12. Anti-notarization boundary

`subject.binary/1` MUST NOT be described, implemented, or marketed as a notarization, timestamping, anchoring, or proof-of-existence system.

This profile:

- does not prove that bytes existed at a time
- does not prove that bytes are true
- does not prove that bytes are authoritative
- does not prove `Independent`

It defines only how an opaque binary subject is transformed into deterministic canonical bytes for use by higher-layer CERTCRYPT semantics.

If a system can reproduce the same claim using only `hash + anchor + verify`, that claim does not come from `subject.binary/1` as defined here.

---

## 13. Security and interpretation boundaries

`subject.binary/1`:

- does not prove authorship
- does not prove identity
- does not prove intent
- does not prove legal validity
- does not validate factual correctness
- does not assert semantic equivalence

Two artifacts that appear semantically similar but differ at the byte level are different subjects under this profile.

Any interpretation beyond exact-byte canonicalization remains outside this profile and MUST be handled, if at all, by other layers under their own public rules.

---

## 14. Versioning & extensibility

- **Profile identifier:** `subject.binary`
- **Profile version:** `/1`

Any change that alters canonical byte output, binary-input boundary, or forbidden-transformation behavior MUST require a new major version.

No optional canonicalization behavior is permitted under `/1`.

---

## 15. References

- CERTCRYPT Specifications
    - [security-model/1 — CERTCRYPT Security Model](../../../foundation/security-model/1/index.md)
    - [system-domain/1 — CERTCRYPT System Domain](../../../foundation/system-domain/1/index.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../../foundation/rules-domain/1/index.md)
    - [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../../protocols/CCCP/1/index.md)
    - [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../../protocols/CCSP/1/index.md)
    - [verification/verification-package/1 — verification-package/1 · CERTCRYPT Verification Package Specification](../../../ecosystem/verification/verification-package/1/index.md)
    - [verification/verifier-toolkit/1 — verifier-toolkit/1 · CERTCRYPT Verifier Toolkit Specification](../../../ecosystem/verification/verifier-toolkit/1/index.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)

---

**End of subject.binary/1**
