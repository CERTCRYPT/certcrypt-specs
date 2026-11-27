# CERTCRYPT Plain Text Subject Canonicalization Profile (`subject.text/1`)

**Identifier:** `subject.text/1`

**Label:** CERTCRYPT Plain Text Subject Canonicalization Profile v1

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
`subject.text/1` is the formal identifier.  
CERTCRYPT Plain Text Subject Canonicalization Profile v1 is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.

**Audience:** Protocol implementers, verifiers, auditors

**Purpose:** Define the normative subject-profile canonicalization semantics for `subject.text/1` within the active CERTCRYPT public architecture.

**Intended use:** `subject.text/1` is intended to be the authoritative public specification for deriving deterministic `canonical_bytes(subject)` for subjects declaring this profile under CERTCRYPT public rules.

**Scope:** Defines canonicalization boundaries, allowed transformations, and interpretation limits for `subject.text/1`; higher-layer proof, settlement, and consistency semantics remain out of scope except where explicitly referenced.

**Non-goals:** `subject.text/1` does not prove truth, semantic validity, legal validity, issuer authenticity, or Proof of Independence by itself, and MUST NOT be interpreted as a trust mark, notarization mechanism, or live service authority.

> This document is **normative**.
> All requirements expressed using MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in RFC 8174.

---

## 1. Background & rationale
`subject.text/1` defines how plain text subjects are reduced to deterministic `canonical_bytes(subject)` under CERTCRYPT public rules.

It exists to provide a narrowly bounded textual canonicalization profile for content that can safely be treated as plain text without semantic interpretation.

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

`subject.text/1` defines:

- the acceptable text input boundary
- the canonicalization rule for plain text subjects
- the exact line-ending normalization model
- the final newline rule
- the boundary between profile-level verification and higher-layer evaluation

`subject.text/1` does not define:

- envelope structure
- hashing algorithm choice
- commitment construction
- subject meaning
- semantic equivalence beyond the exact canonicalization rule
- proof-of-existence, notarization, or timestamping semantics

Those concerns remain defined elsewhere in the architecture.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

Additional terms:

- **Text subject:** A subject that can safely be treated as plain text under this profile.
- **Canonical bytes:** The deterministic byte sequence produced by this profile.
- **CR:** Carriage Return (`0x0D`).
- **LF:** Line Feed (`0x0A`).
- **CRLF:** The byte sequence `0x0D 0x0A`.

---

## 4. Design principles

`subject.text/1` is designed around the following principles:

- **Minimal normalization:** Only the explicit normalization rule defined by the profile MAY alter the input text.
- **Deterministic canonicalization:** The same valid text input MUST always produce the same `canonical_bytes(subject)`.
- **Zero-data by design:** Certificates derived from this profile MUST remain compatible with a zero-data architecture.
- **Proof without data custody:** Verification depends on the certificate, public rules, and verifier-held original text, not on platform-held data.
- **Infrastructure neutrality:** Canonicalization semantics MUST remain stable across platforms and export environments.
- **Interpretation boundaries:** This profile defines canonicalization only. It does not determine meaning, truth, or independence.

---

## 5. Profile-specific rationale

Plain text content is often subject to benign representation differences across systems, including:

- line-ending variations
- trailing newline inconsistencies
- platform-specific export behavior

Raw byte hashing of text without minimal normalization can therefore produce unnecessary divergence across environments.

`subject.text/1` defines a deliberately narrow canonicalization model that:

- normalizes line endings deterministically
- enforces exactly one final CRLF
- preserves all other bytes exactly
- avoids semantic transformations
- remains reproducible offline

This profile is intentionally conservative.

---

## 6. Architectural role

`subject.text/1` is subordinate to the current architecture:

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

No implementation MAY present `subject.text/1` as a standalone proof, trust mark, or notarization mechanism.

---

## 7. Canonicalization constraints

`subject.text/1` is governed by:

- determinism
- minimal normalization
- cross-platform stability
- no semantic inference
- offline reproducibility
- strict separation from higher-layer meaning

Only explicitly defined transformations are permitted.

---

## 8. Relationship to CCCP and CCSP

`subject.text/1` is a subject-specific profile under [CCCP/1](../../../protocols/CCCP/1/index.md).

Its output constitutes `canonical_bytes(subject)` for use by CCCP-governed hashing and commitment construction.

`subject.text/1` MUST NOT redefine, weaken, or bypass any CCCP requirement.

When referenced from certificates serialized under [CCSP/1](../../../protocols/CCSP/1/index.md), the subject's declared `profile` identifies this specification and nothing more: it confers no authority and asserts nothing about the subject's content.

The presence of `subject.text/1` in a certificate envelope does not upgrade the envelope into any specific higher-layer meaning.

---

## 9. Subject informational attributes

A certificate or higher-layer artifact MAY carry informational attributes associated with a `subject.text/1` subject.

Such attributes:

- MUST be informational only
- MUST NOT affect `canonical_bytes(subject)`
- MUST NOT participate in CCCP commitment computation unless another normative specification explicitly says so
- MUST NOT be used to infer semantic equivalence, truth, or authority

Profile conformance MUST be determined from the subject bytes and declared profile only, not from informational metadata.

---

## 10. Input constraints

A subject using `subject.text/1`:

- MUST represent plain text content
- MUST be treated as a sequence of bytes
- MUST NOT require parser-dependent interpretation to determine canonical bytes
- MUST NOT require structured, markup, or binary parsing to determine canonical bytes

### 10.1 Byte-exact processing model

Canonicalization under `subject.text/1` operates **directly on the raw input bytes**. The `subject` canonicalization context is, at the CCCP layer, an opaque byte sequence (CCCP/1 §6.2); CCCP/1 §5.1's UTF-8 and BOM-absence requirements govern CCCP-defined textual/JSON contexts (e.g. `payload`) and do NOT apply to `subject.text/1` input.

Consequently:

- The input is NOT required to be valid UTF-8. Ill-formed byte sequences MUST be preserved exactly.
- Implementations MUST NOT decode the input into a platform string type and re-encode it if that round trip can alter bytes — for example replacing ill-formed sequences with U+FFFD (`EF BF BD`), substituting lone surrogates, applying Unicode normalization (NFC/NFD), or truncating at an embedded NUL (`0x00`). Line-ending normalization (§11.2) MUST be performed on the byte sequence itself.
- A leading byte-order mark (`EF BB BF`) is ordinary leading content and MUST be preserved; it MUST NOT be stripped.
- There is no maximum length. `canonical_bytes` is derived from the complete ordered byte sequence regardless of how it is read (streamed or buffered).

If the subject cannot be safely treated as plain text without ambiguity, parser discretion, or semantic interpretation, implementations MUST use [subject.binary/1](../../subject.binary/1/index.md) instead.

---

## 11. Canonicalization rules

Canonicalization MUST proceed in the following order: line-ending normalization (§11.2), then final-CRLF enforcement (§11.3). Each step is defined as an exact byte procedure; implementations MUST NOT substitute predicate- or regex-based rewriting whose result could differ from the procedure below.

### 11.1 Definitions

- **CR** is the byte `0x0D`; **LF** is the byte `0x0A`; **CRLF** is the two-byte sequence `0x0D 0x0A`.

### 11.2 Line-ending normalization

Normalize every line ending to CRLF with a single left-to-right scan over the **original** input bytes, never re-reading bytes already emitted. Maintaining an output buffer, at each position `i`:

1. if the next two bytes are `0x0D 0x0A` (CRLF): append `0x0D 0x0A`, advance `i` by 2;
2. else if the next byte is `0x0D` (lone CR): append `0x0D 0x0A`, advance `i` by 1;
3. else if the next byte is `0x0A` (lone LF): append `0x0D 0x0A`, advance `i` by 1;
4. else: append the byte unchanged, advance `i` by 1.

Because the scan reads the original bytes and the CRLF case (1) takes precedence over the lone-CR/lone-LF cases, the result is deterministic for every input. No other bytes are modified during this step.

### 11.3 Final-CRLF enforcement

Let `S` be the output of §11.2.

- If `S` ends with one or more `0x0D 0x0A` sequences, remove the maximal trailing run of `0x0D 0x0A` and then append exactly one `0x0D 0x0A`.
- Otherwise, append exactly one `0x0D 0x0A`.

As consequences:

- an empty text subject canonicalizes to exactly one CRLF (`0x0D 0x0A`);
- a subject consisting only of CRLF sequences canonicalizes to exactly one CRLF.

### 11.4 Byte preservation

Except for the transformations defined in §11.2 and §11.3:

- all bytes MUST be preserved exactly
- whitespace MUST NOT be collapsed
- tabs MUST NOT be converted to spaces
- character encoding MUST NOT be transformed or validated
- Unicode normalization MUST NOT be applied
- a byte-order mark MUST NOT be removed
- embedded NUL (`0x00`) MUST be preserved
- no trimming of leading or internal whitespace is permitted

### 11.5 Conformance vectors

The following input → output pairs are normative; a conforming implementation MUST reproduce each exactly. Bytes are shown as space-separated lowercase hex.

| input | canonical output |
|---|---|
| (empty) | `0d 0a` |
| `61` (`"a"`) | `61 0d 0a` |
| `61 0a` (`"a\n"`) | `61 0d 0a` |
| `61 0d` (`"a\r"`) | `61 0d 0a` |
| `61 0d 0a` (`"a\r\n"`) | `61 0d 0a` |
| `0d 0a 0d 0a` | `0d 0a` |
| `61 0a 0a` (`"a\n\n"`) | `61 0d 0a` |
| `0d 0d` (`"\r\r"`) | `0d 0a` |
| `0d 0d 0a` (`"\r\r\n"` — §11.2 precedence: lone CR, then CRLF = two breaks) | `0d 0a` |
| `0a 0d` (`"\n\r"` — two line breaks, not one) | `0d 0a` |
| `61 0d 0a 62` (`"a\r\nb"`) | `61 0d 0a 62 0d 0a` |
| `ef bb bf 61` (BOM + `"a"`) | `ef bb bf 61 0d 0a` |
| `61 00 62` (`"a"` NUL `"b"`) | `61 00 62 0d 0a` |

---

## 12. Forbidden transformations

Implementations applying `subject.text/1` MUST NOT:

- interpret or normalize markup
- collapse whitespace
- apply Unicode normalization
- infer semantic equivalence
- perform encoding transcoding
- treat text canonicalization as authentication
- strip BOMs
- trim leading or trailing non-newline whitespace
- reinterpret structured text formats through parser-specific canonicalization

`subject.text/1` defines canonicalization only.

Human-perceived textual equivalence MUST NOT be treated as normatively equivalent to canonical identity under `/1`.

Implementations MUST NOT infer canonical equivalence from:

- visually similar rendering
- equivalent wording after local recoding
- editor-driven normalization
- copy/paste reserialization
- parser- or platform-specific text abstractions

If a workflow cannot preserve the exact byte sequence within the canonicalization boundary defined here, it MUST NOT claim that apparent textual sameness is sufficient for profile-level equivalence.

---

## 13. Verification boundary

Profile-level verification under `subject.text/1` is limited to verifying that:

- the declared `profile` is `subject.text/1`
- the supplied bytes are processed under the exact canonicalization rule defined here
- the resulting canonical bytes are the bytes expected by the applicable higher-layer path

This profile does not define a standalone verifier outcome taxonomy for `Issued` or `Independent`.

Those outcomes are defined by higher-layer public rules and verifier behavior, including:

- [security-model/1](../../../foundation/security-model/1/index.md)
- [verification-package/1](../../../ecosystem/verification/verification-package/1/index.md)
- [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md)

No implementation MAY claim profile success under `subject.text/1` as if that alone established valid independence, truth, or authority.

---

## 14. Anti-notarization boundary

`subject.text/1` MUST NOT be described, implemented, or marketed as a notarization, timestamping, anchoring, or proof-of-existence system.

This profile:

- does not prove that text existed at a time
- does not prove that text is true
- does not prove that text is authoritative
- does not prove `Independent`

It defines only how a plain text subject is transformed into deterministic canonical bytes for use by higher-layer CERTCRYPT semantics.

If a system can reproduce the same claim using only `hash + anchor + verify`, that claim does not come from `subject.text/1` as defined here.

---

## 15. Security & interpretation boundaries

`subject.text/1`:

- does not prove authorship
- does not prove intent
- does not prove identity
- does not prove legal validity
- does not validate content truthfulness
- does not assert semantic equivalence beyond the exact canonicalization rule defined here

It produces a deterministic byte representation suitable for cryptographic commitment only.

All interpretation remains external to higher-layer verification semantics.

---

## 16. Versioning & extensibility

- **Profile identifier:** `subject.text`
- **Profile version:** `/1`

Any change that alters canonical byte output, text-input boundary, or permitted normalization behavior MUST require a new major version.

No optional canonicalization behavior is permitted under `/1`.

---

## 17. References

- CERTCRYPT Specifications
    - [security-model/1 — CERTCRYPT Security Model](../../../foundation/security-model/1/index.md)
    - [system-domain/1 — CERTCRYPT System Domain](../../../foundation/system-domain/1/index.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../../foundation/rules-domain/1/index.md)
    - [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../../protocols/CCCP/1/index.md)
    - [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../../protocols/CCSP/1/index.md)
    - [verification/verification-package/1 — verification-package/1 · CERTCRYPT Verification Package Specification](../../../ecosystem/verification/verification-package/1/index.md)
    - [verification/verifier-toolkit/1 — verifier-toolkit/1 · CERTCRYPT Verifier Toolkit Specification](../../../ecosystem/verification/verifier-toolkit/1/index.md)
    - [subject.binary/1 — CERTCRYPT Binary Subject Canonicalization Profile](../../subject.binary/1/index.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)

---

**End of subject.text/1**
