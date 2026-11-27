# CERTCRYPT Canonicalization Commitment Protocol (CCCP/1)

**Identifier:** CCCP/1  

**Label:** CCCP v1  

**Type:** Protocol

**Status:** Frozen

**Layer:** Layer 0 — Protocols

**Depends on:** None *(Root canonicalization protocol)*  

**Naming convention:**  
`CCCP/1` is the **formal protocol identifier**.  
`CCCP v1` is the **human-readable label** and may be used in titles, filenames, UI labels, and documentation headings.  

**Audience:** Protocol implementers, forensic engineers, verifiers  

**Purpose:** Define the common canonicalization, encoding, hashing, and commitment rules shared by all CERTCRYPT subject protocols and profiles.  

**Intended use:** CCCP/1 defines shared, subject-agnostic rules for canonicalization, encoding, hashing, and commitment construction across all CERTCRYPT subject protocols and profiles. It is intended exclusively as a foundational layer for deterministic structural binding, forensic reproducibility, and higher-layer CERTCRYPT protocols that require non-malleable commitment semantics.  

**Scope:** Defines core semantics only; subject extraction and subject-specific normalization are out of scope.  

**Non-goals:** CCCP/1 does not define subject extraction rules, content semantics, identity binding, authentication, consistency outcome evaluation, or legal validity by itself. CCCP/1 MUST NOT be interpreted as defining issuance eligibility, authorization, or consistency outcomes, which are defined exclusively by higher-layer consistency-verification protocols (e.g. CCVP/1). It MUST NOT be interpreted as a notarization, timestamping, or blockchain-proof protocol by itself, and it MUST NOT be used as a substitute for digital signatures, PKI, trusted timestamping services, or identity verification mechanisms.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & Rationale

Issuers create certificates governed by CERTCRYPT specifications that must remain verifiable across different systems, implementations, and long time horizons, without requiring CERTCRYPT to store or retain the original subject material. In practice, raw digital subject material (emails, documents, registry objects) is frequently represented in multiple byte-level variants due to transport, export tools, filesystem behaviors, or harmless formatting differences. Without a strict canonicalization foundation, two parties can hold the same source material for independent evaluation but produce different digests, breaking reproducibility.

**CCCP/1** exists to provide that foundation: a single, shared set of subject-agnostic rules for encoding, canonicalization contexts, hashing, and commitment construction. Subject-specific profiles (e.g., [subject.binary/1](../../../profiles/subject.binary/1/index.md) for opaque binary subjects, [subject.text/1](../../../profiles/subject.text/1/index.md) for plain text, and [subject.collection/1](../../../profiles/subject.collection/1/index.md) for issuer-declared collections) can then focus exclusively on how to derive `canonical_bytes(subject)` for their own kind of subject material, while inheriting the exact same cryptographic semantics and zero-data constraints.

CCCP/1 is designed around forensic reproducibility and independent verification:

- **Deterministic outcomes:** The same canonical inputs MUST produce the same canonical bytes and derived hashes everywhere.  
- **Separation of concerns:** CCCP/1 defines core semantics (canonicalization contexts, hashing, commitments). Subject profiles define subject extraction rules only.  
- **Zero-data operation:** CERTCRYPT certificates do not embed subject content or identities; verifying a subject commitment depends on the verifier having the original source material.  
- **Unlinkability by design:** Commitments bind a certificate instance to a subject via a per-certificate nonce, without revealing the subject hash and without enabling cross-certificate correlation.

In short, CCCP/1 ensures that all CERTCRYPT subject profiles speak the same cryptographic “language”, so verifier-local subject material can be independently reproduced and checked without introducing centralized custody, hidden normalization, or format-dependent ambiguity.

CCCP/1 does not define a self-sufficient proof system and MUST NOT be marketed, described, or implemented as if `canonicalize + hash + commit` were enough to reproduce CERTCRYPT `Independent` semantics.

---

## 2. Scope

CCCP/1 defines the **subject-agnostic canonicalization, encoding, hashing, and commitment rules** that apply to all CERTCRYPT subject protocols and profiles.

CCCP/1 applies whenever a CERTCRYPT specification requires:

- deterministic canonical byte derivation  
- cryptographic hashing of canonicalized data  
- construction or verification of subject commitments  

CCCP/1 does **not** define subject extraction or subject-specific normalization rules.  
Those rules are defined exclusively by the corresponding CERTCRYPT subject profile or protocol.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

---

## 4. Design Principles

CCCP/1 is built on the following principles:

- **Determinism:** Identical canonicalization inputs under the same CCCP version MUST produce identical canonical bytes and derived hashes.
- **Zero-data:** No subject content, identities, or hashes of user-identifiable material are embedded or persisted by the protocol. Only privacy-preserving commitments derived from verifier-local hashes may appear in certificates.
- **Forensic reproducibility:** Canonicalization MUST be stable across systems, implementations, and time.  
- **Independent verification:** Verification relies exclusively on cryptographic material, context snapshots where CCVP/1 is evaluated, and, where a subject commitment is checked, original material available to the verifier, without requiring deference to any party, toolchain, implementation, or infrastructure component.

CCCP/1's determinism is necessary but not sufficient for overall CERTCRYPT convergence.

If higher-layer protocols, parsers, or verifiers apply tolerant, heuristic, or parser-dependent interpretation on top of CCCP/1 outputs, CCCP/1 does not rescue that divergence.

Implementations MUST NOT treat CCCP/1 correctness as a justification for lax higher-layer compatibility behavior.

---

## 5. Encoding Rules

### 5.1 Text Encoding

- All textual data MUST be encoded as UTF-8.  
- UTF-8 BOM MUST NOT be present.  
- If input originates as text, implementations MUST ensure a non-lossy UTF-8 conversion, compatible with [RFC 6532](https://www.rfc-editor.org/rfc/rfc6532) where applicable.
- These rules govern CCCP-defined textual and JSON contexts (§6.1, §6.2). They do NOT govern the `subject` context, which is an opaque byte sequence whose canonicalization — including any encoding or BOM treatment — is defined exclusively by the applicable subject profile (§6.2, §5.2).

### 5.2 Binary Data

- Binary subjects MUST be treated as opaque byte sequences.  
- No transcoding, decoding, re-serialization, or content transformation is permitted at the CCCP layer.

---

## 6. Canonicalization Rules

### 6.1 JSON Canonicalization

When these JSON values are present in the CERTCRYPT certificate payload or defined by a CERTCRYPT protocol or profile, they MUST be canonicalized using [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785):

- `payload`  
- `payload.anchor`  

Any JSON-based subject defined by a CERTCRYPT protocol or profile (e.g., context snapshots) MUST also be canonicalized using [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785).

Canonicalization of `payload` is required for signature verification, even when no payload-level commitment is constructed.

In CCCP/1, `payload` refers exclusively to the certified payload object and not to any enclosing delivery or transport structure.

In CCCP/1, `anchor` refers exclusively to `payload.anchor` as defined by CCSP/1.

### 6.2 Canonicalization Contexts

CCCP/1 defines the following canonicalization contexts:

| Context | Description |
|-------|-------------|
| payload | Entire certificate payload |
| anchor | Anchor object inside the payload |
| subject | External subject bytes supplied by the verifier |

The `subject` canonicalization context does not imply JSON canonicalization.  
Canonicalization rules for the `subject` context are defined exclusively by the applicable subject profile or protocol; at the CCCP layer, the subject is treated as an opaque canonical byte sequence.

Subject commitments embedded within JSON structures (e.g. within `anchor.subjects`) are fixed hash values derived from subject canonicalization performed according to the applicable subject profile.

Verifying that a commitment corresponds to a specific subject instance requires the verifier to possess the original material and to compute `canonical_bytes(subject)` as defined by the applicable subject profile.

Each context MUST be canonicalized independently prior to hashing.

---

## 7. Hashing Rules

### 7.1 Hash Algorithm

- Hash algorithm: **SHA3-256**  
- Digest length: **32 bytes** (64 lowercase hexadecimal characters when serialized)  
- Output encoding: **lowercase hexadecimal**, without prefix  

### 7.2 Hash Inputs

- Hash input MUST be the exact canonical byte sequence produced by the applicable canonicalization rules.  
- No additional whitespace, metadata, framing, or transformation is permitted.

### 7.3 Defined Hash Schemes

| Name | Scheme |
|-----|--------|
| payload_canon_digest_hex | SHA3-256( RFC8785(payload) ) |  
| anchor_canon_digest_hex | SHA3-256( RFC8785(anchor) ) |  
| subject_local_digest_hex | SHA3-256( canonical_bytes(subject) ) |

The value `subject_local_digest_hex` represents the **subject-local hash**.

During certificate issuance, the issuer computes the subject-local hash as part of commitment construction.  
During verification, the verifier independently recomputes the subject-local hash from the original material and compares the derived commitment to the one embedded in the certificate.

The subject-local hash is a verifier-local value and **MUST NOT** be published, embedded, or disclosed in any CERTCRYPT certificate, nor exposed in any form that enables subject tracking, fingerprinting, or cross-certificate correlation.

Any use of verifier-local hashes outside the verifier context is explicitly out of scope for CERTCRYPT semantics.
#### Publication and Verification Semantics

The following hash values **MAY** be published in a CERTCRYPT certificate, at the locations [CCSP/1](../../CCSP/1/index.md) defines for them (the top-level `payload_canon_digest_hex` and `payload.anchor_canon_digest_hex`):

- `payload_canon_digest_hex`
- `anchor_canon_digest_hex`

When present:

- `payload_canon_digest_hex` **MUST** represent the SHA3-256 digest of the canonicalized certificate payload.
- `anchor_canon_digest_hex` **MUST** represent the SHA3-256 digest of the canonicalized anchor.

Published hash values are non-authoritative and exist solely as verification aids.

Verifiers **MUST NOT** rely on published hash values as authoritative.  
All hash values **MUST** be recomputed independently by the verifier from canonicalized inputs.

Any mismatch between a published hash value and a recomputed hash MUST fail verification: the artifact carrying it is structurally invalid. Verifiers MUST NOT downgrade the mismatch to a warning, and MUST NOT treat the published value as authoritative. A single outcome is fixed so that every verifier reaches the same result for the same artifact.

### 7.4 Operation-Scoped Pseudonym Derivation

Some CERTCRYPT protocols and profiles need to bind to a stable internal identifier (for example, a holder, pool, or authorization identifier) without disclosing that identifier and without enabling cross-certificate correlation. CCCP/1 defines one shared derivation for that purpose:

```text
pseudonym = SHA3-256( framed(operation_salt) || framed(domain_tag) || framed(stable_id) )
framed(x) = u64_big_endian(byte_length(x)) || x
```

Rules:

- The hash algorithm is **SHA3-256** (§7.1); the output is the full 32-byte digest, lowercase hexadecimal.
- Each input field MUST be absorbed with an **8-byte big-endian length prefix** (framing). This length-framing is a deliberate, scheme-specific exception to the no-framing rule of §7.2, which governs subject canonicalization inputs; it is required here so that field boundaries are unambiguous (without it, `("ab","c")` and `("a","bc")` would collide).
- `operation_salt` MUST be a per-operation value unique to the operation in which the pseudonym appears. Reusing a salt across operations defeats unlinkability.
- `domain_tag` MUST be one of the values defined by the consuming protocol or profile and MUST separate namespaces, so that the same `stable_id` yields unrelated pseudonyms under different domains. A new tag is added in the consuming specification, never ad hoc.
- `stable_id` is the internal identifier being projected. It MUST NOT appear in clear in any published artifact.

Properties this derivation guarantees: it is **deterministic** (a verifier that holds `operation_salt`, `domain_tag`, and `stable_id` recomputes the same pseudonym, with no issuer secret), **unlinkable across operations** (a fresh `operation_salt` makes the same `stable_id` produce unrelated pseudonyms), and **non-invertible** (the salted digest does not reveal `stable_id` to an observer who does not already hold it).

A pseudonym is a binding aid, not a verification authority: it lets a consuming protocol check that two artifacts refer to the same projected identifier without exposing it. It does not replace any signature, commitment, or membership check defined by the consuming specification.

---

## 8. Commitments Construction
### 8.1 Subject Commitment

CCCP/1 defines the commitment construction used by all CERTCRYPT subject profiles and protocols:

`commitment = SHA3-256( ASCII(nonce_hex) || ASCII(subject_local_digest_hex) )`

Both values are concatenated as ASCII byte sequences of their hexadecimal representations. The hexadecimal strings MUST NOT be decoded prior to concatenation.

Where the `||` operator represents **binary concatenation of ASCII byte sequences**.

Implementations MUST concatenate the raw ASCII byte sequences of `nonce_hex` and `subject_local_digest_hex` as bytes, with no separators.

The **subject-local hash** refers to the SHA3-256 digest of the canonical subject bytes as defined in Section 7.3. Any reference to a subject hash within CERTCRYPT specifications refers exclusively to the subject-local hash.

#### Subject Commitment Representation

A commitment MAY be represented as a labeled value.

When carried inside a CERTCRYPT certificate governed by [CCSP/1](../../CCSP/1/index.md), the subject commitment field name MUST be:

- `payload.anchor.subjects[].commitment_digest_hex`

When a label or prefix is present (e.g. `CCCP/1:<hex>`), it identifies the commitment construction protocol used to produce the value.

The prefix is purely identificatory and MUST NOT be interpreted as a resolvable reference, protocol locator, network identifier, or retrieval mechanism.

#### Properties

- The commitment binds a subject to a specific certificate instance.  
- The subject hash remains private to the verifier (zero-data).  
- Commitments are unlinkable across certificates due to per-certificate nonces.

Subject commitments are the only mechanism defined by CERTCRYPT for binding certified objects to certificates.

Subject profiles MUST NOT introduce alternative identifiers, hashes, or bindings that enable stable identification, tracking, or correlation of subjects across certificates.
### 8.2 Anchor Commitment

CCCP/1 defines an anchor-level commitment used to bind the canonicalized certificate anchor to a specific certificate instance.

The anchor commitment is constructed as follows:

`anchor_commitment_digest_hex = SHA3-256( ASCII(nonce_hex) || ASCII(anchor_canon_digest_hex) )`

`anchor_commitment_digest_hex` is the **certificate-level commitment** for CCCP/1.  
CCCP/1 defines no other certificate-level commitment field name, and no other field may be interpreted as a certificate-level commitment under CCCP/1 semantics.

Where:

- `nonce_hex` is the per-certificate nonce defined in Section 10
- `anchor_canon_digest_hex` is the SHA3-256 digest of the canonicalized anchor as defined in Section 7.3

The `||` operator represents binary concatenation of ASCII byte sequences, with no separators.
#### Anchor Commitment Representation

When published in a CERTCRYPT certificate, the anchor commitment MUST be represented as:

- `payload.anchor_commitment_digest_hex`

`payload.anchor_commitment_digest_hex` **MUST** be interpreted as the certificate-level commitment defined by this section, when present.

When referenced outside the certificate, the value MAY be labeled using the prefix:

`CCCP/1:<hex>`

The prefix is purely identificatory and MUST NOT be interpreted as a resolvable reference, protocol locator, network identifier, or retrieval mechanism.

#### Properties

- The anchor commitment binds the certificate payload to a unique issuance instance.
- The anchor commitment binds the canonicalized anchor as a whole, including the subject commitments contained within it and any other issuance-time control fields defined in `payload.anchor`.
- When `payload.anchor` contains a higher-layer issuance-time participation reference such as `payload.anchor.root_id`, the anchor commitment binds that reference to the same unique issuance instance.
- The anchor commitment is not a naked subject hash and MUST NOT be treated as a stable public identity of the certified content.
- The anchor commitment does not reveal subject-local hashes or subject metadata.

#### 8.2.1 Anchor Commitment Interpretation Boundary

The value `payload.anchor_commitment_digest_hex` MUST be interpreted exclusively as the structural certificate-level commitment defined by CCCP/1.

It binds the canonicalized anchor to a specific issuance instance and nothing more.

CCCP/1 alone does not define whether a certificate validly participated in any later `Independent`-capable path.

That meaning boundary depends on higher-layer specifications that:

- define which signed anchor fields carry issuance-time participation intent,
- define when such participation references are admissible,
- and bind those references to the relevant leaf-level or independence-level path under public rules.

Because the canonicalized anchor includes subject commitments and issuance-time structural fields, `payload.anchor_commitment_digest_hex` is structurally dependent on both the certified subject bindings and the anchor-level issuance conditions.

When higher-layer normative specifications use signed anchor fields to establish issuance-time participation in a later leaf-level, `fixation`, or `Independent` path, CCCP/1 contributes the non-reconstructible issuance binding by combining:

- the signed canonical anchor,
- the per-certificate CSPRNG nonce `nonce_hex`,
- and the resulting anchor commitment over that issuance-time anchor state.

Accordingly, if a higher-layer participation reference required for later `Independent` eligibility was absent from the signed anchor at issuance time, neither `payload.anchor_commitment_digest_hex` nor any later container, settlement, resolver, transport, or packaging artifact MAY be interpreted as retroactively creating that missing issuance-time participation state.

However, it MUST NOT be interpreted as either:

- a naked subject hash, or
- a stable public identity of the certified content.

`payload.anchor_commitment_digest_hex` MUST NOT be interpreted as:

- evidence of economic execution, payment, burn, or settlement,
- evidence of contextual authorization or entitlement,
- proof of legal validity or regulatory compliance,
- evidence of trust, endorsement, or institutional backing,
- a subject-level commitment substitute.

Implementations MUST NOT interpret the anchor commitment as authorization to reconstruct, simulate, or infer missing issuance-time participation context from post-issuance artifacts alone.

When a higher-layer specification requires issuance-time participation for later `Independent` eligibility, implementations MUST also reject any post-issuance artifact set that is only retrospectively compatible with that missing participation state.

Structural compatibility after issuance is not a substitute for an issuance-time participation reference that was actually present in the signed anchor and bound by the per-certificate nonce and anchor commitment at issuance time.

Accordingly, issuer-side SDKs, emission services, and certificate production workflows MUST treat failure to place the required admissible participation reference into the signed anchor at issuance time as a non-recoverable failure for any later independence-capable path governed by higher-layer public rules.

No economic policy, token model, consistency protocol, implementation, UI, API, or ecosystem layer MAY redefine or extend the meaning of the anchor commitment beyond the structural binding semantics defined by CCCP/1.

Any such reinterpretation constitutes non-conformance with CCCP/1.

### 8.3 No in-certificate anchoring binding

CCCP/1 defines no binding between the anchor commitment and any anchoring, consensus, or settlement field inside the certificate. [CCSP/1](../../CCSP/1/index.md) reserves `payload.consensus` and rejects a certificate that carries it. Anchoring and settlement are carried by artifacts outside the certificate, which bind to the certificate as their own specifications define.

---

## 9. Generic Commitment Labeling

A commitment MAY be represented as a labeled value.

When a label (expressed as a prefix, e.g. `CCCP/1:<hex>`) is present, it identifies the commitment construction protocol used to produce the value.

The prefix is purely identificatory and MUST NOT be interpreted as a resolvable reference, protocol locator, network identifier, or retrieval mechanism.

---

## 10. Nonce Requirements

- Length: **256 bits**  
- Representation: **lowercase hexadecimal** (64 hex characters)  
- Generation: MUST use a **cryptographically secure random number generator (CSPRNG)**  
- Reuse: A nonce MUST NOT be reused across certificates.

---

## 11. Determinism and Verification

- Canonicalization and hashing MUST be fully deterministic.  
- Independent implementations processing identical input MUST produce identical canonical bytes and hashes.  
- Verifiers MAY re-canonicalize any context to validate derived hashes.
- Published hash values are informational only and MUST NOT be treated as authoritative verification inputs.

---

## 12. Error Handling

- Invalid encoding, invalid canonicalization, or hash mismatch MUST result in verification failure.  
- Unknown or unsupported subject profiles MUST result in **subject verification failure** for that certificate.  
- However, they MUST NOT prevent verification of CCCP-defined contexts (e.g., `payload`, `anchor`) when those contexts are present and supported.

If a verifier does not support the subject profile required to interpret and canonicalize the certified subject:

- subject verification MUST fail for that certificate  
- cryptographic verification of CCCP-defined contexts MAY still succeed  
- verifiers MUST NOT infer subject validity through heuristics or fallback mechanisms

---

## 13. Zero-Data Principle

CCCP/1 enforces the CERTCRYPT zero-data model:

- No subject data is embedded in certificates.  
- No identities are stored by the protocol.  
- Verifying a subject against its commitment requires the original material, which only the verifier supplies.

---

## 14. Relationship to Certificate Envelopes, Subject Profiles, and Protocols

CERTCRYPT Certificate Serialization Protocol ([CCSP/1](../../CCSP/1/index.md)) defines the canonical certificate envelope structure and serialization rules.

[CCSP/1](../../CCSP/1/index.md) does not define canonicalization or hashing semantics.  
All canonicalization, encoding, hashing, and commitment semantics used by [CCSP/1](../../CCSP/1/index.md) are defined exclusively by CCCP/1, including:

- canonicalization contexts  
- encoding rules  
- hashing semantics  
- subject commitment construction  

Subject-specific specifications under the CERTCRYPT framework include:

- **Profiles**, such as [subject.binary/1](../../../profiles/subject.binary/1/index.md), [subject.text/1](../../../profiles/subject.text/1/index.md), and [subject.collection/1](../../../profiles/subject.collection/1/index.md), which apply CCCP/1 to specific kinds of subject material.
- **Protocols**, such as [CCVP/1](../../CCVP/1/index.md), which define their own subject models while relying on CCCP/1 core semantics.

All CERTCRYPT subject protocols and profiles:

- MUST conform to CCCP/1  
- MUST explicitly declare dependency on a specific CCCP version  
- MAY introduce additional constraints, but MUST NOT weaken CCCP guarantees  

CCCP/1 is the sole authority for canonicalization and commitment semantics within CERTCRYPT.  
No envelope, profile, or protocol may redefine or weaken the guarantees established by CCCP/1.

---

## 15. Versioning & Extensibility

- **Protocol identifier:** `CCCP/1`  
- CCCP versions are independent from subject protocol versions.  
- Any change that alters canonicalization, hashing, or commitment semantics MUST increment the CCCP major version.

---

## 16. References

- CERTCRYPT Specifications
    - [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../CCSP/1/index.md)
    - [CCVP/1 — CERTCRYPT Consistency Verification Protocol](../../CCVP/1/index.md)
    - [subject.binary/1 — CERTCRYPT Binary Subject Canonicalization Profile](../../../profiles/subject.binary/1/index.md)
    - [subject.text/1 — CERTCRYPT Plain Text Subject Canonicalization Profile](../../../profiles/subject.text/1/index.md)
    - [subject.collection/1 — CERTCRYPT Collection Subject Canonicalization Profile](../../../profiles/subject.collection/1/index.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
    - [RFC 8785 — JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785)

---

**End of CCCP/1**
