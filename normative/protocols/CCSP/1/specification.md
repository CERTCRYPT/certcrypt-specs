# CERTCRYPT Certificate Serialization Protocol (CCSP/1)

**Identifier:** CCSP/1  

**Label:** CCSP v1  

**Type:** Protocol

**Status:** Frozen

**Layer:** Layer 1 — Protocols

**Depends on:** 
- [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../CCCP/1/index.md)
- [composite-signature/1 — CERTCRYPT Composite Signature Profile](../../../foundation/composite-signature/1/index.md)

**Naming convention:**
`CCSP/1` is the **formal protocol identifier**.
`CCSP v1` is the **human-readable label** and may be used in titles, filenames, UI labels, and documentation headings.  

**Audience:** Certificate issuers, protocol implementers, verifier developers, archival and forensic systems  

**Purpose:** Define the canonical certificate envelope structure and serialization rules shared by all CERTCRYPT certificates.  

**Intended use:** CCSP/1 defines a stable, protocol-level container for CERTCRYPT certificates, ensuring deterministic serialization, interoperability across implementations, and long-term offline verifiability. It is intended exclusively as a structural layer: it defines envelope constraints and emission-classification requirements, and it defines verifier obligations for envelope validation and signing-target handling; it does not define canonicalization procedures, cryptographic algorithms, or network validation logic (see [CCCP/1](../../CCCP/1/index.md) and verifier implementations).

**Scope:** Defines certificate envelope structure and serialization constraints only.  

**Non-goals:** CCSP/1 does **not** define cryptographic algorithms, signature verification algorithms, trust models, or identity verification mechanisms. It DOES define certificate envelope constraints, signature-object structure, and verifier obligations for classifying inputs as Protocol Emissions. It MUST NOT be used as a substitute for canonicalization, hashing, or commitment construction ([CCCP/1](../../CCCP/1/index.md)), PKI, trusted timestamping services, economic settlement systems, or legal/evidentiary frameworks.

> This document is **normative**.
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative.

---

## 0. Conformance, interpretation boundaries, and normative structure

This section defines the **normative reading model**, **interpretation boundaries**, and **structural organization** of CCSP/1.

It establishes **how this specification MUST be interpreted**, **where authoritative rules are defined**, and **what CCSP/1 explicitly does and does not claim**.

This section does **not** introduce new field-level requirements or validation rules.

All normative rules referenced in this section are defined exclusively in later sections of this specification.

### 0.1 Protocol emission concept

A **Protocol Emission** is a CCSP/1 certificate that:

- conforms structurally to this specification, and
- carries exactly one signature object, the issuer signature (`role = "issuer"`), and that signature verifies under the signature profile fixed by the rules domain the certificate names, as defined in Section 7.4.

Protocol Emission status is a **purely technical classification**.

Whether an issuer signature is considered cryptographically valid is verifier-local, as algorithm support and cryptographic capabilities may vary between implementations.  This locality does not alter the normative classification model, which is defined exclusively in Section 10.

It indicates only that:

- the certificate envelope is structurally valid, and
- the issuer has produced a verifiable cryptographic signature over the canonicalized payload.

Protocol Emission status:

- MUST NOT be interpreted as proof of truth, correctness, trust, authority, legality, or economic participation.
- MUST NOT be interpreted as evidence of settlement, payment, or value transfer.

Protocol Emission status is a **necessary but not sufficient condition** for any higher-level classification.

Classification, labeling, and reporting of Protocol Emissions follow Section 10, which also fixes how the classification is read from a [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md) result.

Protocol Emission qualification is **verifier-relative**.

Protocol Emission qualification is verifier-relative **only with respect to cryptographic verification capabilities** (supported algorithms and correct canonicalization/hashing implementation). Structural validity is deterministic under this specification.

Whether an input qualifies as a Protocol Emission depends on the verifier’s supported cryptographic algorithms, canonicalization implementation, and validation rules as defined by this specification.

Structural validity and field-level constraints in Sections 6–9 are not verifier-relative; implementations that deviate from them are non-conformant verifiers and produce non-authoritative results.

No actor, issuer, or system MAY assert that an input “is a Protocol Emission” without
reference to a specific verifier implementation or an explicitly defined verification
capability set.

An input MAY qualify as a Protocol Emission under one verifier and fail under another
without constituting a specification violation.

### 0.2 Normative separation of concerns

CCSP/1 enforces a strict separation between:

- **envelope structure**,
- **payload semantics**,
- **transaction context definitions** (e.g. leaf-scoped issuance models defined by subject profiles),
- **post-issuance state definitions**, and
- **reporting / classification logic**.

This separation is intentional and normative.

#### 0.2.1 Envelope vs. semantics

CCSP/1 defines:

- where data lives,
- how it is serialized,
- what is signed, and
- what is ignored.

CCSP/1 does **not** define:

- subject meaning,
- subject canonicalization,
- commitment construction,
- trust semantics,
- legal or evidentiary claims.

All semantic meaning is defined by:

- [CCCP/1](../../CCCP/1/index.md),
- subject profiles,
- registry or authorization protocols,
- any leaf-level or `fixation` specifications that apply outside the certificate.

#### 0.2.2 Structural validity vs. external state outcomes

Structural validity under CCSP/1 and any external `fixation`, anchoring, settlement, or equivalent post-issuance state are **orthogonal** concepts.

A certificate MAY be:

- a valid Protocol Emission, yet
- not fixed,
- not independently verifiable,
- not in any post-issuance state defined outside the certificate envelope.

External state outcomes:

- is never inferred from structure alone,
- is never inferred from the presence of fields,
- is never inferred from protocol compatibility.

CCSP/1 does not define `Independent`, `fixed`, anchoring-complete, settlement-complete, or any equivalent leaf-level outcome.

### 0.3 Interpretation boundaries

Unless explicitly stated otherwise, nothing in CCSP/1:

- implies trust,
- implies endorsement,
- implies authority,
- implies legal standing,
- implies evidentiary admissibility,
- implies economic value.

In particular:

- The presence of signed envelope fields does not imply `Independent`, `fixed`, anchored, or settled status.
- The presence of subject commitments does not imply any leaf-level or CERTCRYPT-operated outcome.

All such interpretations are explicitly bounded and constrained by Sections **9** and **10**.

### 0.4 Single source of truth rule

For the avoidance of ambiguity:

- Field-level validation, presence, and dependency rules for `payload.anchor` and `payload.anchor.subjects` are defined **exclusively** in **Section 7.3**.
- Reserved field names and external-state boundaries are defined **exclusively** in **Section 9**.
- CCSP/1 does not define claim-based certificate classes, ecosystem participation labels, fixation, anchoring, or settlement compliance requirements.
- Reporting categories, classification rules, and labeling constraints are defined **exclusively** in **Section 10**.

No rule may be inferred, duplicated, or overridden outside its defining section.

CCSP/1 defines one validation behavior (standard mode) and admits no tolerances: an input that deviates from Sections 6–9 is rejected, never repaired (Section 0.4.1).

Any verifier result intended to support normative higher-layer evaluation under CERTCRYPT public rules MUST be grounded in CCSP/1 standard-mode semantics.

In standard CCSP/1 mode, verifiers MUST NOT reject otherwise valid certificates solely due to the presence of unknown, additional, or extension fields, except where this
specification explicitly forbids additional members.

Unknown members inside `payload` and `metadata` MUST NOT be treated as structural violations **except inside objects explicitly defined as closed by CCSP/1 (`payload.anchor`, the issuer signature object, its `signer` and its component objects).**

Implementations MAY offer stricter validation modes (e.g. “strict” or “profile-locked”),
but such modes:

- MUST be explicitly labeled and documented,
- MUST NOT alter reporting category semantics defined in Section 10,
- MUST NOT reclassify a valid Protocol Emission as Category 0 (Not a Protocol Emission) solely due to unknown fields,
- MAY only introduce additional sub-status or error annotations (e.g. “strict rejection”).

Forward-compatibility applies to additional members inside `payload` and `metadata`,
and to the optional top-level `extensions` object (if present),
but not to any other top-level envelope members, which are strictly closed as defined in Section 6.

Strict modes are implementation-local and MUST NOT be assumed by default.

Strict modes MUST NOT produce divergent higher-layer semantic outcomes from the same certificate unless the certificate is explicitly rejected or flagged as non-standard.

This requirement exists to preserve verifier convergence across implementations, not merely local parser correctness.

A certificate ecosystem in which multiple implementations are only “mostly compatible” but reach different higher-layer outcomes is non-conformant with CCSP/1, even if each implementation appears locally reasonable.

No higher-layer security model, verifier policy, SDK discipline, or product wording rescues an implementation that violates this convergence requirement.

If envelope parsing, unknown-field treatment, or forward-compatibility behavior causes higher-layer meaning to diverge, the implementation is non-conformant and MUST fail closed for the affected normative path.

In particular, no such mode MAY change:

- protocol-emission qualification,
- the signed payload extracted for canonicalization,
- protocol or profile selection inputs,
- issuance-time participation interpretation,
- leaf-level or independence-capable path interpretation,
- or any verifier output later presented as normative under referenced higher-layer public rules.

#### 0.4.1 No tolerances

CCSP/1 contemplates no tolerances. An input that would need semantic inference, heuristic recovery, parser-dependent reconstruction, or any repair to be read is rejected.

In particular, a UTF-8 byte-order mark before the JSON text and a repeated member name in any object, `metadata` and `extensions` included, are rejected (Section 8.1). Neither is stripped, dropped, or resolved by keeping one of the duplicates.

Forward compatibility is acceptable only to the extent that it preserves exact normative convergence for higher-layer interpretation. It MUST NOT be used to justify “80% compatible” verifier behavior in which signatures still validate but higher-layer meaning diverges across implementations.

### 0.5 Absence of implicit semantics

CCSP/1 is intentionally hostile to implicit meaning.

Implementations MUST NOT infer semantics from:

- field names,
- field presence,
- protocol compatibility,
- structural similarity,
- extensions,
- metadata,
- UI labels,
- filenames,
- transport context,
- or out-of-band statements.

Only explicitly defined, signed payload fields and referenced normative sections may be used for interpretation.

CERTCRYPT explicitly forbids UI or API rebranding of classification outcomes.

Protocol Emission (Category 1) MUST NOT be presented, labeled, or marketed as a “CERTCRYPT certificate” or as equivalent to any leaf-level or CERTCRYPT-operated outcome.

Any presentation that omits category qualifiers or implies leaf-level state, endorsement, or economic participation where none exists is considered a misrepresentation of CCSP/1 semantics.

### 0.6 Forward compatibility and defensive design

CCSP/1 is designed to remain valid under:

- future subject profiles,
- leaf-level `fixation` specifications,
- future anchoring mechanisms,
- future signature algorithms.

This is achieved by:

- strict envelope constraints,
- explicit ignore rules,
- and strict separation between structure, post-issuance state, and reporting.

Any future extension that alters envelope structure, serialization rules, or signing semantics requires a new major CCSP version.

---

## 1. Background & rationale

CERTCRYPT certificates are designed to be **portable, durable, and independently verifiable** without depending on the continued availability or authority of managed tooling, operators, or infrastructure.

Without a strictly defined certificate envelope:

- implementations diverge structurally across systems  
- canonicalization and hashing inputs become ambiguous  
- signatures degrade over time  
- verification becomes tooling-dependent  

To eliminate these risks, CCSP/1 defines a **single, protocol-level certificate envelope** and strict serialization constraints shared by all CERTCRYPT certificates.

---

## 2. Scope

CCSP/1 defines **certificate envelope structure and serialization rules only**.

It does **not** define:

- subject canonicalization  
- hashing or commitment construction  
- verification logic  
- trust, authority, or legal semantics  

These concerns are defined by:

- **[CCCP/1](../../CCCP/1/index.md)** — canonicalization, hashing, and commitment construction  
- subject profiles (e.g. `subject.email/1`, `subject.binary/1`, `subject.text/1`, `subject.collection/1`, `subject.ai-decision/1`)
- context consistency protocols (e.g. `CCVP/1`)  

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

**JSON string**
A value encoded as a JSON string type as defined by [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259).
Fields defined as strings in CCSP/1 MUST be encoded as JSON strings and MUST NOT be encoded as numbers, booleans, null, arrays, or objects.

**ASCII string**
A JSON string whose characters are restricted to US-ASCII code points 0x20–0x7E.
Unless explicitly stated otherwise, ASCII string comparisons in CCSP/1 MUST be performed byte-for-byte on the UTF-8 encoded JSON string content, without trimming, normalization, case folding, Unicode processing, or locale-dependent transformations.

**ASCII token**  
A JSON string restricted to US-ASCII code points 0x21–0x7E (printable ASCII excluding SPACE) and additionally excluding HTAB (0x09), LF (0x0A), and CR (0x0D). ASCII token comparisons MUST be byte-for-byte without trimming, normalization, case folding, Unicode processing, or locale-dependent transformations.

**Lowercase hex string**  
A JSON string of lowercase hexadecimal characters (`0-9a-f`). When a fixed length is required, it MUST match the exact length and MUST be validated byte-for-byte (no trimming or normalization).

**[RFC 4648](https://www.rfc-editor.org/rfc/rfc4648) base64 string**  
A JSON string encoded using the RFC 4648 base64 alphabet (`A–Z a–z 0–9 + /`) with optional `=` padding. It MUST NOT contain whitespace. URL-safe base64 (`-` and `_`) is NOT RFC 4648 base64 and MUST be rejected unless explicitly allowed.

**No normalization rule (general):**  
For all fields defined by CCSP/1 with fixed-value semantics or syntax constraints, implementations MUST compare and validate the JSON string content byte-for-byte and MUST NOT apply trimming, Unicode normalization, case folding, locale rules, or any other transformations.

---

## 4. Design principles

CCSP/1 is designed according to the following principles:

- **Envelope, not semantics**  
- **Canonical-by-design**  
- **Profile-agnostic**  
- **Zero-data compatible**  
- **Offline-first**  

CCSP/1 defines **where data lives and how it is serialized**, not what it means.

---

## 5. Certificate model overview

A CERTCRYPT certificate is a **self-contained JSON object** composed of:

- schema (discriminator)  
- payload (the certified statement)  
- signatures (the issuer signature)
- optionally, metadata and extensions (non-normative annotations) and a published payload digest  

All certificates MUST conform to this envelope.

---

## 6. Top-level envelope structure

A CERTCRYPT certificate MUST be a JSON object (not an array, string, or number) with the following top-level fields:

- `schema`
- `payload`
- `signatures`

The following top-level fields are OPTIONAL:

- `metadata` (non-normative annotations; Section 7.2)
- `payload_canon_digest_hex` (published canonical payload digest; recomputed and checked as defined in Section 7.5)
- `extensions` (non-normative extensions; Section 6.1)

No other top-level fields are permitted. A certificate carrying any other top-level member MUST be rejected as structurally invalid.

Objects that include bundling, receipt, or transport wrapper fields alongside the certificate fields are not CCSP/1 certificates; such wrappers must exist outside the CCSP/1 object.

All post-issuance artifacts (including but not limited to: receipts, root identifiers, storage proofs, attachment manifests, delivery metadata, and transport acknowledgments) MUST exist only outside the CCSP/1 certificate object.

> **Informative (UI guidance):**
> Implementations MAY offer a privacy-safe presentation that omits `metadata` and `extensions`.
> Such a presentation is a view, not the certificate: it MUST be clearly labeled as a view and MUST NOT be exported, hashed, or verified as the certificate (Section 6.2).

### 6.1 `extensions` (OPTIONAL)

`extensions` MUST be a JSON object.
    
Keys inside `extensions` MUST be namespaced strings (recommended forms):
    
    - reverse-DNS (`com.vendor.feature`)
    - URN-like (`urn:vendor:feature`)
    - spec-id (`profile.xyz/1`)

`extensions` MUST NOT be required for successful verification.

Verifiers MUST ignore `extensions` entirely for:

- protocol selection
- profile selection
- semantic interpretation
- the issuer signature's signing input (Section 7.4)
- signature validation        
- validity assessment

Ignoring `extensions` means not interpreting it. It does not remove `extensions` from the certificate: the emission binding hashes the whole certificate, `extensions` included (Section 6.2).

`extensions` MUST be treated as potentially correlating metadata.

Issuers SHOULD NOT emit `extensions` unless a use requires it: it is potentially correlating, and once emitted it cannot be removed without producing a different certificate (Section 6.2). Where `extensions` is displayed, it MUST be marked as UNSIGNED / NON-NORMATIVE and potentially correlating.

Verifiers, UIs, and APIs MUST NOT use `extensions` to change the reporting category selection rules defined in Section 10.

Verifiers MUST NOT use `extensions` to influence:

- system-domain attribution,
- rules-domain selection,
- issuance-time participation interpretation,
- leaf-path interpretation,
- independence semantics,
- settlement interpretation,
- or any higher-layer verifier outcome.

Verifiers and UIs MAY apply privacy heuristics and MAY warn or restrict display/export if `extensions` appears to contain high-entropy identifiers, fixed-length hex/base64 blobs, or other correlators.

CCSP/1 does not define a reliable method to determine whether an extension value is subject-derived. Therefore, any privacy restrictions on `extensions` beyond ignoring it are implementation-defined.

Extensions MAY include transport- or container-scoped identifiers that are not subject-derived, but verifiers MUST ignore them for verification and compliance, and UIs SHOULD treat them as potentially correlating metadata.

Any extension that is intended to affect verification, compliance, or normative meaning MUST be carried inside the signed `payload` and defined by a referenced normative specification (protocol/profile). Top-level `extensions` are strictly non-normative.

The presence of `extensions` MUST NOT reduce the requirement that possession of the original material (from which subject material can be derived according to the applicable subject profile) remains strictly necessary to verify a subject commitment.

Presence of prohibited `extensions` content MUST NOT alter cryptographic validity, classification, or compliance reporting, but MAY alter UI display or export behavior.

Verifiers MUST NOT use the presence, absence, or content of `extensions` to infer protocol versioning, profile applicability, or economic participation.

`extensions` that is not a JSON object, or that repeats a member name in any of its objects, makes the certificate structurally invalid (Section 8.1).

**Scope of this section**

The rules in this section apply **only** to the top-level member `extensions` (i.e., `certificate.extensions`).

Any member named `extensions` that appears **inside `payload`** is part of the **signed payload** and is **not covered** by the ignore rules of this section.

Such nested `extensions` members MUST be processed according to the applicable normative section governing their parent object, including canonicalization and hashing requirements where applicable.

### 6.2 Certificate identity and the emission binding

The issuer signature covers the canonicalized `payload` only (Section 7.4). The certificate itself is a larger object, and it is fixed as a whole at emission.

Higher layers bind to the entire certificate: the emission binding recomputes `SHA3-256(JCS(certificate))` over the complete certificate object as delivered, every member present included — `schema`, `payload`, `signatures`, and, when present, `metadata`, `extensions` and `payload_canon_digest_hex` ([verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/specification.md) Section 11.2.1, step 1).

Where this specification says that a member is ignored, it means the member is not interpreted. It never means the member is excluded from that digest.

Accordingly:

- adding, removing, or changing any member after emission — including `metadata`, `extensions` or `payload_canon_digest_hex`, which the issuer signature does not cover — produces a different certificate, which no longer matches its emission binding;
- a copy, export, or view that omits or rewrites any member is not the certificate, and MUST NOT be verified or presented as it;
- an issuer decides at emission which optional members the certificate carries.

---

## 7. Top-level fields

### 7.1 `schema`

The `schema` field:

- MUST be present
- MUST be a JSON string with the exact value of `"certcrypt-certificate"` (byte-for-byte)
- is used for structural discrimination only  

Certificates with any other value, or where this field is missing, MUST be rejected as structurally invalid and MUST NOT be treated as CCSP/1 certificates.

The `schema` field MUST NOT be used for versioning, feature negotiation, or behavioral inference.

### 7.2 `metadata`

The `metadata` field is OPTIONAL. When present, it MUST be a JSON object; it MAY be an empty object `{}`.

The `metadata` object contains **purely informative, non-normative envelope annotations**.

`metadata` is not covered by the issuer signature and is never part of its signing input. It is part of the certificate, and the emission binding hashes it with every other member (Section 6.2).

Metadata fields:

- are **not part of any protocol semantics**
- are **not interpreted by verifiers**
- are **not part of the issuer signature's signing input**
- MUST NOT affect signature validity, trust evaluation, or verification outcomes; they are bound, as part of the certificate, by the emission binding (Section 6.2), and nothing more
- MUST be ignored for _normative verification_. Implementations MAY display/log metadata.

Metadata exists solely to support **human readability, UI display, logging, or external system integration**.

#### Common metadata fields

The `metadata` object MAY include arbitrary informational fields intended for
human readability, UI display, logging, or external system correlation.

Unknown metadata fields MUST NOT cause structural rejection or verification failure.
Type mismatches or invalid values inside `metadata` MUST NOT affect verification outcomes. Duplicate member names inside `metadata` MUST be handled as defined in Section 8.1.

All metadata fields:
- are **non-normative**
- are **not interpreted by verifiers**
- are **not part of the issuer signature's signing input**
- **MUST NOT** affect signature validity, verification outcomes, or evidentiary meaning (they are bound as part of the certificate, Section 6.2, and nothing more)

Verifiers **MUST** ignore all metadata fields for protocol selection, profile selection,
semantic interpretation, trust evaluation, and validity assessment.

Verifiers MUST also ignore all metadata fields for:

- system-domain attribution,
- rules-domain selection,
- issuance-time participation interpretation,
- leaf-path interpretation,
- independence semantics,
- settlement interpretation,
- and any higher-layer verifier outcome.

Verifiers MUST NOT copy `metadata` fields into verification outputs as if they were derived or verified facts (e.g., issuer id, subject count, timestamps). If included for display or logging, they MUST be explicitly marked as UNSIGNED / NON-NORMATIVE.

Protocol and profile selection is derived **exclusively** from the signed `payload` structure and declared subject profiles.

CCSP/1 does not define protocol or profile resolution logic beyond structural requirements.

UIs MUST clearly distinguish metadata from signed payload data and MUST NOT present metadata values using authoritative language such as "verified", "authoritative", "CERTCRYPT-issued", "trusted", or equivalent.

Any UI representation that includes metadata MUST label it as "UNSIGNED / NON-NORMATIVE".

### 7.3 `payload`

The `payload` field MUST be a JSON object.

The `payload` object contains the **certified statement**.

**Required fields**

- `anchor` — the issuance anchor (Section 7.3.1)
- `anchor_commitment_digest_hex` — the anchor commitment
- `system_id` — the system domain the certificate is issued under
- `rules_version` — the rules domain the certificate is issued under

**Optional field defined by this specification**

- `anchor_canon_digest_hex` — a published anchor digest

The `payload` object MAY contain additional fields beyond these.
Unknown `payload` fields MUST NOT cause structural rejection, unless explicitly forbidden by a referenced normative specification (in particular the reserved names of Section 9) or unless a verifier explicitly operates in a strict profile-specific mode.

All additional payload fields and semantics are defined exclusively by the applicable CERTCRYPT protocol(s) and profile(s) governing the payload structure (e.g. subject profiles, CCVP).

The `payload` is the sole carrier of all normative, cryptographic, and verification-relevant semantics of a CERTCRYPT certificate.

`anchor_commitment_digest_hex`:

- MUST be present, as a sibling of `anchor` (never inside it)
- MUST be a lowercase hexadecimal string of exactly 64 characters
- MUST equal the anchor commitment `SHA3-256(ASCII(nonce_hex) || ASCII(anchor_canon_digest_hex))` defined by [CCCP/1](../../CCCP/1/index.md) Section 8.2, recomputed by the verifier from `payload.anchor`; a mismatch makes the certificate structurally invalid

`system_id`:

- MUST be present
- MUST be a non-empty ASCII token (Section 3)
- names the system domain under which the certificate is issued ([system-domain/1](../../../foundation/system-domain/1/index.md) Section 7.1); it is signed with the payload, and it is a claim, not an attribution (system-domain/1 Section 7.2)
- a verifier evaluating under a system domain MUST reject a certificate whose `system_id` is not that domain's

`rules_version`:

- MUST be present
- MUST be a non-empty ASCII token (Section 3)
- names the rules-domain instance under which the certificate is issued (for example `rules/2026-01`); that rules domain fixes the issuer signature profile (Section 7.4) and the subject profiles a certificate may declare
- a verifier MUST evaluate the certificate under the rules domain it names and no other. A verifier that does not evaluate that rules domain cannot decide the certificate: it MUST report it as unsupported (`UNSUPPORTED` under verifier-toolkit/1) and MUST NOT evaluate it under another rules domain

`anchor_canon_digest_hex` (OPTIONAL):

- if present, MUST be a lowercase hexadecimal string of exactly 64 characters
- if present, MUST equal `SHA3-256(RFC8785(payload.anchor))` ([CCCP/1](../../CCCP/1/index.md) Section 7.3), recomputed by the verifier; a mismatch makes the certificate structurally invalid
- is never used in place of the recomputed value

#### 7.3.1 The `anchor` object

This section is the normative source of truth for the envelope-level structure of `payload.anchor`.

- MUST be present  
- MUST be a JSON object  
- is the canonical container for issuance-time cryptographic material, including issuance timestamp, optional root participation reference, nonces, and subject commitments

The `issued_at` field:

- MUST be present
- MUST be a JSON string
- MUST be an [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339) timestamp in UTC of the form `YYYY-MM-DDTHH:MM:SS[.fraction]Z`: uppercase `T` and `Z`, no numeric offset, one to nine fractional digits when a fraction is present, seconds from `00` to `59`
- MUST name a real calendar instant (a date the month has, hours `00`–`23`, minutes `00`–`59`)

A value in any other form, including other forms RFC 3339 allows (a lowercase `t` or `z`, a numeric offset, a leap second), makes the certificate structurally invalid, so that every verifier reads the same instant.

`issued_at` is the issuance-time timestamp of the certificate instance.
It belongs to the certificate envelope and is part of the signed `anchor` object.

The `nonce_hex` field:

- MUST be present  
- MUST be a lowercase hexadecimal string of exactly 64 characters
- provides per-certificate entropy for commitment construction

`nonce_hex` MUST satisfy the nonce requirements defined by [CCCP/1](../../CCCP/1/index.md) (including length, CSPRNG generation, and non-reuse).

The `root_id` field:

- MAY be present
- MUST be a lowercase hexadecimal string when present
- MUST be exactly 64 hexadecimal characters when present

`root_id`, when present, is the signed issuance-time root participation reference of the certificate.
CCSP/1 defines only its existence and placement inside `payload.anchor`.
The participation semantics, root-resolution rules, and admissibility constraints associated with `root_id` are defined exclusively by referenced higher-layer normative specifications.

When a referenced higher-layer normative specification requires issuance-time participation in a later leaf-level, `fixation`, or `Independent` path, `payload.anchor.root_id` MUST be the protocol-visible participation reference carried by the certificate envelope.

In such cases:

- `payload.anchor.root_id` MUST be present at issuance time,
- it MUST be bound by the issuer signature as part of the signed `anchor` object,
- it MUST be bound by the anchor commitment defined by [CCCP/1](../../CCCP/1/index.md),
- it MUST NOT be introduced, replaced, or retroactively derived after issuance from subject material, `issued_at`, post-issuance leaf artifacts, settlement artifacts, resolver output, or any other later-produced context alone.

When higher-layer participation semantics depend on `payload.anchor.root_id`, implementations MUST treat the field as an opaque signed issuance-time participation reference. They MUST NOT infer an equivalent participation reference from any other envelope field, from naming conventions, or from post-issuance material.

They MUST also reject any attempt to treat a retrospectively assembled leaf context, settlement context, resolver output, wrapper metadata, or packaging artifact as normatively equivalent to a missing issuance-time participation reference.

If a referenced higher-layer normative specification requires issuance-time participation for a later independence-capable path and `payload.anchor.root_id` is absent or inadmissible under that higher-layer specification, no later artifact MAY validly claim that the certificate participated in that path at issuance time.

Issuance tooling, issuer-side SDKs, and any conforming emission workflow that intends to support such a later independence-capable path MUST therefore treat omission, ambiguity, or post-issuance derivability of `payload.anchor.root_id` as a non-repairable emission failure for that path.

CCSP/1 does not provide any later envelope-level recovery mechanism by which a certificate emitted without that admissible signed participation reference can become validly equivalent to one that carried it at issuance time.

CCSP/1 therefore provides the protocol-visible envelope location for issuance-time participation reference material, but it does not by itself define the full meaning of later `Independent` eligibility.

That later meaning still depends on higher-layer leaf, fixation, and independence specifications that determine:

- whether issuance-time participation was required,
- what makes the reference admissible and irreproducible under public rules,
- and how that signed issuance-time reference must bind to the later leaf-level path.

If those higher-layer specifications require irreproducible issuance-time participation and the signed envelope does not carry it in admissible form at issuance time, CCSP/1 provides no alternative field, recovery path, or equivalent envelope-level substitute.

CCSP/1 defines the existence and placement of the `anchor` object and specifies the envelope-level control fields within it: `issued_at`, optional `root_id`, `nonce_hex`, and `subjects[]`.

`payload.anchor` is a closed object. Its only members are `issued_at`, `nonce_hex`, `subjects` and, optionally, `root_id`. Any other member makes the certificate structurally invalid; in particular the anchor commitment is carried beside the anchor, as `payload.anchor_commitment_digest_hex`, never inside it.
Subject canonicalization, hashing inputs, and commitment construction are defined exclusively by [CCCP/1](../../CCCP/1/index.md) and the referenced subject profiles.

Canonicalization, hashing, nonce requirements, and commitment construction are defined exclusively by **[CCCP/1](../../CCCP/1/index.md)**.

Reserved field names and prohibition rules for `payload.anchor` are defined exclusively in Section 9.
In particular, CCSP/1 does not define `claim` or `economic_policy_id` as valid certificate fields inside `payload.anchor`.

CCSP/1 does not define `issuer_id` or `issuer` as core `payload.anchor` fields.
Core issuer identity for CCSP/1 is carried by the issuer signature material under `signatures[]`, not by a separate envelope-level issuer object inside `anchor`.

The `anchor` object is the signed issuance-time root for protocol-level cryptographic control fields, including `issued_at`, optional `root_id`, the certificate nonce, and the subject commitment set.

#### 7.3.2 The `subjects` array

`payload.anchor.subjects` **MUST** be an array of subject commitment objects.

The `subjects` array is an ordered list of certified subject units. Each entry represents one subject unit for reporting and verification.

The normative subject count for a certificate is `len(payload.anchor.subjects)` exactly.

Verifiers, UIs, APIs, and compliance reports MUST NOT deduplicate `subjects` entries by `profile`, by `commitment_digest_hex`, or by any other heuristic.

The `subjects` array MUST contain at least one subject entry.

Each entry MUST be a JSON object; otherwise the certificate MUST be rejected as structurally invalid. Each entry MUST include at least the following required members:

- `profile`
- `commitment_digest_hex`

Additional members MAY be present and MUST be ignored by CCSP/1 unless a referenced normative specification defines their meaning.

##### `subjects[].profile`

`subjects[].profile` MUST be a non-empty lowercase ASCII token matching `^subject\.[a-z0-9][a-z0-9_.-]{0,63}/[1-9][0-9]*$`.

Subject identifiers are **single-segment by design**.

Multi-segment or path-like subject identifiers (e.g. `subject/email/1`) are intentionally disallowed in CCSP/1 to preserve flat namespace semantics and prevent hierarchical ambiguity.

Future extensions requiring hierarchical subject namespaces require a new subject profile convention or a new CCSP major version.

It IS a **subject profile identifier** (e.g. `subject.binary/1`, `subject.email/1`, `subject.text/1`, `subject.collection/1`, `subject.ai-decision/1`).
Values such as `"document"` or `"email"` (without a `/major` suffix) MUST be rejected as structurally invalid.

Comparison of `subjects[].profile` values MUST be performed byte-for-byte. Implementations MUST NOT apply trimming, normalization, case folding, Unicode processing, or locale-dependent transformations.

Certificates containing invalid `subjects[].profile` values MUST be rejected and MUST NOT be classified as Protocol Emissions.

Subject interpretation, canonicalization rules, and verification behavior are determined exclusively by the subject profile identified by `subjects[].profile`.

##### `subjects[].commitment_digest_hex`

`subjects[].commitment_digest_hex` MUST be a JSON string of exactly 64 lowercase hex characters matching `^[0-9a-f]{64}$`.

Subject-level commitments are scoped **exclusively** to subject certification.
They MUST NOT be interpreted as certificate identifiers or as evidence of consensus or economic activity.

##### Duplicate entries

Multiple entries MAY share the same `profile`.  
Multiple entries MAY also share the same `commitment_digest_hex`.

Such duplicates indicate multiple certified subject units and MUST be preserved as distinct entries.

##### Implementation limits

Verifiers MAY impose implementation-defined limits on the maximum number of subject entries they process, but MUST do so in a way that does not silently change subject counts (e.g., fail with an explicit error).

No metadata field may define, override, or influence subject interpretation.

#### 7.3.3 Reserved envelope-level fixation fields

CCSP/1 does not define envelope-level anchoring or settlement descriptors inside the certificate.
The normative prohibition and reserved-name rules for these fields are defined exclusively in Section 9.

If `payload.consensus` or `payload.economics` is present, the certificate MUST be rejected as structurally invalid under CCSP/1.

External anchoring, settlement, and equivalent post-issuance state belong to leaf-level `fixation` artifacts defined outside CCSP/1.

CCSP/1 reserves the field names `payload.consensus` and `payload.economics` to avoid accidental semantic reuse inside the certificate envelope.

### 7.4 `signatures`

The `signatures` field MUST be an array holding **exactly one** element: the issuer signature object.

A certificate whose `signatures` array is empty, holds more than one element, or holds an element that is not an issuer signature object as defined below MUST be rejected as structurally invalid.

One issuer signature leaves nothing for a verifier to choose. With several, verifiers that support different algorithms could select different signatures and report different issuers for the same certificate, which the convergence requirement of Section 0.4 forbids.

#### 7.4.1 The issuer signature object

The issuer signature is a composite signature as defined by [composite-signature/1](../../../foundation/composite-signature/1/specification.md), carried with the members below. The object is closed: it MUST contain exactly the required members and, optionally, `kid`, and no other member.

| member | requirement |
|---|---|
| `role` | REQUIRED. Exactly `"issuer"`. |
| `alg` | REQUIRED. ASCII token (Section 3): the composite profile identifier ([composite-signature/1](../../../foundation/composite-signature/1/specification.md) Section 7) under which the signature was produced. |
| `mode` | REQUIRED. Exactly `"AND"`. |
| `sig_target` | REQUIRED. Exactly `"payload_canon_digest_hex"` (Section 7.4.3). |
| `signatures` | REQUIRED. The component signatures (Section 7.4.2). |
| `signer` | REQUIRED. The issuer's label and composite public key (Section 7.4.2). |
| `kid` | OPTIONAL. ASCII token of at most 128 characters; a non-normative key label. |

All string members MUST be JSON strings; `signatures` MUST be an array and `signer` a JSON object.

`kid`, if present, MUST be treated as non-normative and MUST NOT be interpreted as an identity claim, used for trust evaluation, issuer attribution, or signature validity. Its presence or absence MUST NOT affect signature validity. A consistency entry under [CCVP/1](../../CCVP/1/index.md) Section 8 MAY name a `kid` as an additional filter; that filter can only exclude an entry the issuer label and key fingerprint already bind, never establish a binding. Issuers SHOULD omit it: it is potentially correlating, and once emitted it is part of the certificate (Section 6.2).

#### 7.4.2 Components and signer

`signatures` MUST hold exactly two component objects, in the order the composite profile fixes: the classical component first, the ML-DSA-65 component second ([composite-signature/1](../../../foundation/composite-signature/1/specification.md) Section 8). Each component object is closed:

- the classical component: `{"alg": "ECDSA-P256-SHA3-256", "encoding": "raw-rs-64", "low_s": true, "sig_b64": …}`, with `sig_b64` the 64-byte `r || s` signature, low-s (composite-signature/1 Section 9.1);
- the post-quantum component: `{"alg": "ML-DSA-65", "sig_b64": …}`, with `sig_b64` the raw FIPS 204 signature (composite-signature/1 Section 9.3).

`signer` is a closed object with exactly these members:

- `id` — REQUIRED. ASCII token of at most 256 characters. An issuer-provided label: it MUST NOT be interpreted as proof of real-world identity, and verifiers and UIs SHOULD treat it as an untrusted label. Issuers SHOULD avoid placing personally identifying information in it.
- `pub_p256_b64` — REQUIRED. The ECDSA P-256 public key as a SEC1 **uncompressed** point (65 bytes, first byte `0x04`). This is the one canonical encoding of this field (composite-signature/1 Section 9.1): a compressed point, SPKI DER, or any other encoding of the same key is malformed here, never an equivalent.
- `pub_mldsa_b64` — REQUIRED. The ML-DSA-65 public key as raw FIPS 204 bytes.

CCSP/1 defines the signer layout for composite profiles whose classical component is ECDSA P-256. A profile with another classical component would need its own signer layout, which this specification does not define.

Every `sig_b64` and every public-key member MUST be an [RFC 4648](https://www.rfc-editor.org/rfc/rfc4648) base64 string (Section 3) with padding, non-empty and without whitespace. URL-safe base64 (`-` and `_`) MUST NOT be accepted; verifiers SHOULD report it with a diagnostic such as `BASE64URL_NOT_ALLOWED`. A value that does not decode, or decodes to the wrong length for its field, is malformed (composite-signature/1 Section 6.2).

#### 7.4.3 Signing input and validity

The issuer signature covers the canonicalized `payload` and nothing else. Every component signs the derived message

`M' = ASCII("CERTCRYPT-Composite-Signature-v1") || 0x00 || ASCII(composite_alg_id) || 0x00 || ASCII(payload_canon_digest_hex)`

defined by [composite-signature/1](../../../foundation/composite-signature/1/specification.md) Section 4, where `payload_canon_digest_hex` is the lowercase hexadecimal `SHA3-256(RFC8785(payload))` computed according to [CCCP/1](../../CCCP/1/index.md), and `composite_alg_id` is the profile the verifier requires (below).

The value `sig_target = "payload_canon_digest_hex"` names this signing target; it is not a reference to the top-level field of the same name. It is the only signing target CCSP/1 defines: verifiers MUST treat any other value as unsupported and MUST NOT infer equivalence, upgrade, or compatibility between signing targets.

Verifiers MUST recompute the canonical payload and its digest. A published digest (Section 7.5, or `payload.anchor_canon_digest_hex`) is checked against the recomputation and is never used as the signing input.

The issuer signature is cryptographically valid only if:

1. `alg` equals the signature profile fixed by the rules domain named in `payload.rules_version` for the base certificate issuer signature (for `rules/2026-01`, Section 18 of that rules domain fixes `certcrypt-composite-p256-mldsa65-v1`). The verifier takes the expected profile from the rules domain, never from the signature: a signature that declares another profile fails, even where it would verify under that other profile;
2. both components verify over `M'` under the AND rule and the post-quantum floor of composite-signature/1 Section 6, with the encodings of its Section 9; and
3. every field-level requirement of this section is satisfied.

Malformed component material (a signature or key that does not decode, has the wrong length, is high-s, or uses a non-canonical key encoding) is a structural defect, distinct from a well-formed signature that does not verify (composite-signature/1 Section 6.2). Both leave the input outside Category 1 (Section 10).

UIs and APIs MUST NOT present a certificate as “signed” or “verified” unless its issuer signature is cryptographically valid.

CCSP/1 does not mandate a trust model or public key infrastructure, and does not determine whether an emission becomes `Independent`, `fixed`, anchored, settled, or compliant with any external policy.

### 7.5 `payload_canon_digest_hex` (OPTIONAL)

`payload_canon_digest_hex` is an OPTIONAL publication of the canonical payload digest.

Rationale: This field MAY be used for UI display, indexing, caching, or transport convenience. It is **non-authoritative**: it is checked against the recomputed digest and never used in its place.

- If present, it MUST be a lowercase hexadecimal string of exactly 64 characters.
- If present, it MUST equal `SHA3-256(c14n(payload))`, where `c14n(payload)` is defined by [CCCP/1](../../CCCP/1/index.md).
- Verifiers MUST recompute the canonical payload bytes and digest according to [CCCP/1](../../CCCP/1/index.md) and MUST NOT rely on this field for signature verification.
- A value that is syntactically invalid, or that does not equal the recomputed digest, makes the certificate structurally invalid ([CCCP/1](../../CCCP/1/index.md) Section 7.3). The issuer signature does not cover this field, but the certificate does (Section 6.2): a value that does not recompute means the certificate was assembled wrongly or altered after emission, and two certificates that differ only in it would otherwise both be accepted while hashing differently.
- Its absence has no effect on classification.

Verifiers MUST NOT use `payload_canon_digest_hex` to bypass, shortcut, or replace canonicalization or hashing as defined by [CCCP/1](../../CCCP/1/index.md).

Even when the published digest matches the recomputed value, it remains non-authoritative and MUST be treated strictly as an informational hint.

UIs MUST NOT present `payload_canon_digest_hex` as authoritative or as proof of verification; it is an informational hint only.

---

## 8. Serialization and canonicalization forms

### 8.1 JSON serialization

Certificates MUST be serialized as:

- UTF-8 encoded JSON,
- without comments or trailing commas.

A UTF-8 byte-order mark MUST NOT be present, and a certificate that starts with one MUST be rejected; it is not stripped.

Certificates MUST be valid JSON as defined by [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259). Non-standard numeric values (e.g. NaN, Infinity) MUST be rejected. Any serialization that violates these requirements MUST be rejected.

**Repeated member names.** No object anywhere in the certificate may contain the same member name twice. The rule applies at every depth and to every object, `metadata` and `extensions` included: all of them are part of the certificate the emission binding hashes (Section 6.2), so a repeated member anywhere makes the certificate's content parser-dependent.

- Member names are compared after their JSON escape sequences are decoded, as the resulting strings, code unit for code unit, without Unicode normalization. `"anchor"` and `"\u0061nchor"` are the same name.
- Only the members of one object are compared with each other. Repeated elements of an array are ordinary data, and the same name in two different objects is not a repetition.

If any object repeats a member name, verifiers MUST reject the certificate. They MUST NOT apply first-wins, last-wins, merge, or any other resolution strategy.

Duplicate-member detection MUST occur **before** any [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) canonicalization step and **before** any [CCCP/1](../../CCCP/1/index.md) hashing or issuer signature verification step, on the input as received.

Implementations MUST use a JSON parsing strategy that exposes every member of every object. If the chosen JSON stack cannot reliably detect repeated member names, the implementation MUST fail verification with an explicit parser-limitation error and MUST NOT treat the input as structurally valid. A value that was parsed elsewhere and handed over already parsed carries no evidence of repetitions; an implementation that accepts such values MUST document that the caller is responsible for strict parsing.

**Recommended error labeling (informative):**

The following identifiers are RECOMMENDED for interoperability and reporting consistency:

- `DUPLICATE_MEMBER` — the input repeats a member name;
- `PARSER_LIMITATION` — the implementation cannot reliably detect repeated member names.

These identifiers are advisory only and do not affect verification outcomes or reporting categories defined in Section 10.

### 8.2 Canonicalization

All hashing and signing inputs MUST be derived from canonical forms produced according to:

- **[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785)**  
- **[CCCP/1](../../CCCP/1/index.md)**

Verifiers MUST NOT re-serialize the `payload` using a non-canonical serializer prior to applying [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) canonicalization. They MUST apply canonicalization to the parsed JSON data model as defined by [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) / [CCCP/1](../../CCCP/1/index.md).

CCSP/1 does not define canonicalization contexts.

When a CERTCRYPT certificate is transported inside any enclosing delivery or bundling structure, CCSP/1 applies exclusively to the embedded certificate object whose `schema` equals `certcrypt-certificate`.

Certificates are intended to be embeddable within external container formats ("containers") that may carry transport metadata, receipts, storage proofs, payment/burn receipts, attachment manifests, or other post-issuance artifacts.
Such containers are out of scope for CCSP/1 and MUST NOT affect canonicalization, hashing, signature verification, or certificate validity.

Enclosing transport, delivery, bundling, receipt, or consumer metadata fields MUST NOT be included in any [CCCP/1](../../CCCP/1/index.md) canonicalization context and MUST NOT be used as signing or hashing inputs for CCSP/1 signatures.

#### 8.2.1 Canonicalization integrity requirements

When canonicalizing the `payload` object for hashing or signature verification, verifiers MUST operate on the exact JSON object as received.

Verifiers MUST NOT:

- remove or ignore fields based on schema expectations,
- perform semantic normalization or interpretation,
- drop unknown, optional, deprecated, or extension fields,
- substitute missing fields with defaults,
- reorder or restructure objects outside [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) canonicalization rules.

Unknown signed payload members MAY remain structurally forward-compatible, but they MUST NOT be used heuristically to infer higher-layer semantics not explicitly defined by a referenced normative specification.

Canonicalization is a purely syntactic transformation.  
Semantic interpretation of `payload` fields MUST NOT influence canonicalization or cryptographic verification.

### 8.3 Field ordering

- JSON field order MUST NOT be relied upon  
- ordering outside canonicalization is non-normative  
- cryptographic comparison relies exclusively on canonical forms  

### 8.4 Size and resource limits

Implementations MAY enforce limits on:
- maximum JSON document size,
- maximum nesting depth,
- maximum string length for any field,
- maximum number of `subjects` entries,
- maximum decoded sizes for signatures and public keys.

If such limits are enforced, implementations MUST fail verification with an explicit error and MUST NOT truncate, normalize, or partially process over-limit inputs.

Implementations SHOULD enforce reasonable maximum decoded sizes for every `sig_b64` and for `signer.pub_mldsa_b64` to mitigate resource-exhaustion attacks.

---

## 9. Reserved envelope-level policy and fixation fields

CCSP/1 does not define envelope-level claim, policy, anchoring, or settlement descriptors inside the certificate.
CCSP/1 does permit an optional root participation reference at `payload.anchor.root_id`, but does not assign policy, declared-context, anchoring, settlement, or fixation-outcome semantics to that field by itself.

When a higher-layer normative specification requires a certificate-visible issuance-time participation reference, `payload.anchor.root_id` is the only CCSP/1 envelope field that MAY carry that role. No other envelope member MAY be treated as an equivalent substitute for that purpose.

Accordingly, the following field names are reserved and MUST NOT be present in a CCSP/1 certificate:

- `payload.anchor.claim`
- `payload.anchor.economic_policy_id`
- `payload.consensus`
- `payload.economics`

If any reserved field above is present, the certificate MUST be rejected as structurally invalid under CCSP/1.

Leaf-level `fixation`, `Independent` state, external anchoring, settlement, and equivalent post-issuance outcomes belong to artifacts defined outside CCSP/1.

CCSP/1 reserves these field names to avoid accidental semantic reuse inside the certificate envelope.

### 9.1 Privacy warnings (Informative guidance)

Verifiers and UIs SHOULD apply privacy heuristics to the signed `payload`.

If fields not defined by a referenced normative specification contain high-entropy identifiers, fixed-length digests, or values that appear to be correlators, implementations SHOULD emit a privacy warning.

Such warnings MUST NOT affect cryptographic validity, Protocol Emission qualification, or reporting category selection.

---

## 10. Verifier reporting and classification

This section defines the CCSP/1 **classification** of an input, how it is read from a [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/specification.md) result, and the **labeling constraints** that prevent false authority inference.

This section does **not** define field-level validation rules.
All field-level rules for `payload.anchor` and `payload.anchor.subjects` are defined exclusively in **Section 7.3**.
Reserved-field prohibitions are defined in **Section 9**.

### 10.1 Categories

Each processed input belongs to **exactly one** of two categories:

0. **Not a Protocol Emission**
1. **Protocol Emission**

An input is in **Category 1** if and only if it is structurally valid under Sections 6–9 and its issuer signature is cryptographically valid under Section 7.4. Every other input — malformed, unparseable, repeating a member name, structurally invalid, carrying a signature that fails or is malformed, or not decidable by the verifier — is in **Category 0**.

CCSP/1 categories do not encode `Independent`, fixation, anchoring, settlement, or any equivalent post-issuance outcome.

### 10.2 Correspondence with verifier-toolkit/1 results

A verifier conforming to [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/specification.md) does not report a separate category field. The category is read from its result:

- **Category 1** if and only if `issued_valid` is `true` — the checks `BASE_CERTIFICATE_STRUCTURE_VALID` and `BASE_CERTIFICATE_AUTHENTIC` both passed;
- **Category 0** otherwise.

The category MUST be read from `issued_valid`, never inferred from `result_code`: the result code also reflects steps beyond the envelope (original-material comparison, the `Independent` path), so a Category 1 certificate can still end in a result code other than `ISSUED_VALID`.

For a Category 0 input, the result code says why it is outside Category 1:

| situation | `result_code` | failing check |
|---|---|---|
| not RFC 8259 JSON, a repeated member name, or a parser limitation | `REJECTED` | input validation |
| a structural defect under Sections 6–9, including a published digest or anchor commitment that does not recompute, a `system_id` that is not the evaluated domain's, or malformed signature material | `REJECTED` | `BASE_CERTIFICATE_STRUCTURE_VALID` or `BASE_CERTIFICATE_AUTHENTIC` |
| a well-formed issuer signature that does not verify, or that declares a profile other than the rules domain's | `ISSUED_INVALID` | `BASE_CERTIFICATE_AUTHENTIC` |
| a `rules_version` the verifier does not evaluate, or a required cryptographic capability it lacks | `UNSUPPORTED` | `BASE_CERTIFICATE_STRUCTURE_VALID` or `BASE_CERTIFICATE_AUTHENTIC` |
| no certificate supplied | `INCOMPLETE` | the presence check |

Implementations MAY report additional diagnostics, provided they do not replace, merge, or obscure the category.

### 10.3 Mandatory labels and export semantics

Verifiers, UIs, APIs, and compliance reports MUST use category-accurate labeling.

They MUST NOT collapse categories into ambiguous labels such as:

- “CERTCRYPT certificate”
- “CERTCRYPT verified”

under CCSP/1 classification alone.

Any API response, export format, filename, or UI label that omits the reporting category qualifier constitutes prohibited rebranding.

A reporting or export format that is not a verifier-toolkit/1 result SHOULD carry the category explicitly rather than leave it to be inferred from other dimensions.

#### Category 0 — not a protocol emission

Systems MUST NOT label the input as a “certificate”, “valid”, “verified”, or “signed”.

#### Category 1 — protocol emission

Systems MAY label the input as:

- “Protocol Emission”
- “CCSP/1 certificate (valid issuer signature)”

Systems MUST NOT label it as `Independent`, fixed, anchored, settled, “CERTCRYPT issued”, “CERTCRYPT certified”, or imply any external policy or post-issuance outcome.

### 10.4 Interpretation boundaries for reporting

Reporting categories express classification outcomes only.

Verifiers, UIs, APIs, and compliance reports MUST NOT infer, assert, or imply from any category:

- legal standing,
- evidentiary admissibility,
- trust, endorsement, or authority,
- authorship or identity truth,
- economic value.

Protocol Emission status MUST NOT be interpreted as conferring trust, endorsement, authority, legal standing, or economic value.

Protocol Emission is verifier-relative; no party may claim universal validity without specifying verifier capabilities/algorithm support.

Protocol Emission classification expresses only structural and cryptographic envelope validity and MUST NOT be interpreted as proof of payment execution, settlement finality, policy compliance, or economic value.

### 10.5 Prohibited inference inputs

Verifiers, UIs, APIs, and compliance reports MUST derive CCSP/1 reporting **only** from envelope structure, canonicalization/signature results, and the referenced normative sections.

They MUST NOT use any of the following to infer `Independent` status, fixation, anchoring, settlement, economic participation, or any equivalent post-issuance outcome:

- protocol compatibility or structural similarity,
- external assertions or out-of-band statements,
- metadata fields,
- extensions (top-level or nested),
- filenames, surrounding transport context, UI labels, or export format,
- out-of-scope external artifacts, container artifacts, or policy artifacts not explicitly incorporated by the applicable non-CCSP specification.

### 10.6 Verifier capability disclosure

Verification outcomes under CCSP/1 are verifier-relative.

A verifier’s minimum supported behavior under CERTCRYPT is governed by [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/specification.md), which defines fail-closed verifier behavior, minimum supported targets, and minimum supported inputs.

A verifier MAY include its `verifier-toolkit/1` conformance status in verification reports, audit records, compliance statements, or exported results.

Such disclosure MUST NOT affect Protocol Emission qualification, reporting category selection, or compliance determination.

Absence of disclosure MUST NOT invalidate verification results.

---

## 11. Hash references

All hash references MUST:

- be computed over exact canonical byte sequences  
- use the hash algorithm defined by [CCCP/1](../../CCCP/1/index.md)  
- be encoded as lowercase hexadecimal  

Implementations MUST NOT compute hashes over non-canonical or tooling-dependent representations.

---

## 12. Subject hash non-disclosure

Verifier-local subject hashes, including `subject_local_digest_hex` or any equivalent value derived from `canonical_bytes(subject)`, MUST NOT be:

- embedded in certificates,
- included in delivery packages,
- exposed in verification reports,
- displayed in user interfaces,
- returned via APIs,
- logged in plaintext,
- exported in diagnostic outputs,
- persisted in any registry or storage layer.

Implementations MAY internally compute verifier-local subject hashes for verification purposes, but MUST treat them as ephemeral and local to the verifier process.

Implementations MUST NOT disclose any value that enables cross-certificate subject correlation without possession of the original material.

Implementations MUST NOT expose any deterministic derivative of verifier-local subject hashes (including truncated, encoded, or rehashed forms).

Disclosure of verifier-local subject hashes constitutes violation of the Zero-Data invariant and renders the implementation non-conformant with CERTCRYPT.

---

## 13. Forbidden behaviors

Implementations **MUST NOT** perform any of the following actions within a CCSP/1 certificate object:

- Embed subject data outside the signed `payload`.
- Add transport-, delivery-, or container-specific metadata inside the certificate object.
- Depend on JSON field ordering for interpretation, hashing, signature verification, or validation.
- Modify any part of the certificate after issuer signature generation.
- Embed any receipt, proof, acknowledgment, or evidence artifact inside the certificate object under any name, unless that artifact is explicitly defined by a referenced normative specification and carried inside the signed `payload` under that specification’s rules.
- Include any economic receipt, payment receipt, burn proof, settlement proof, storage proof, or similar artifact inside the certificate object under any name, unless explicitly defined by a referenced normative specification within `payload`.
- Treat any economic artifact, receipt, storage proof, or settlement indicator as an input to certificate verification, signature validation, or reporting category selection.
- Embed any JSON object with `schema = "certcrypt-certificate"` anywhere inside `payload.anchor`, `payload.anchor.subjects`, or any subject-profile-defined canonical subject structure.
- Present, label, or imply any field as proof, receipt, settlement evidence, storage evidence, or inclusion evidence unless its semantics are explicitly defined by a referenced normative specification.

These restrictions apply **strictly and exclusively** to the CCSP/1 certificate object, regardless of transport, storage, or delivery context.

Any field that is intended, named, or presented as a receipt or proof artifact (regardless of naming convention, prefix, or structure) **MUST** be treated as **non-normative** unless:

- it is explicitly defined by a referenced normative specification, and
- it is carried inside the signed `payload` in accordance with that specification’s rules.

Verifiers, UIs, and APIs **MUST NOT** present such non-normative artifacts as proof of settlement, payment, storage, inclusion, confirmation, or economic execution.

Receipts, storage proofs, delivery metadata, acknowledgments, or post-issuance artifacts **MAY** exist in enclosing delivery, bundling, or transport structures, but **MUST NOT** be included inside the CCSP/1 certificate object itself.

Such external artifacts **MUST NOT** influence:

- certificate interpretation,
- structural validity,
- canonicalization,
- signature verification,
- Protocol Emission qualification, or
- CCSP/1 reporting.

Any such artifacts included inside the certificate MUST be ignored by verifiers for all CCSP/1 structural validity, Protocol Emission qualification, and reporting purposes, unless a referenced normative specification explicitly defines their semantics inside the signed `payload`, and SHOULD be flagged as a bundling violation.

For avoidance of doubt: CCSP/1 defines certificate-envelope semantics only and does **not** recognize any embedded receipt or proof object as authoritative evidence of settlement, storage, inclusion, confirmation, or fixation.

Any receipt or proof artifact embedded inside the certificate object **MUST** be ignored for CCSP/1 validity and **MUST NOT** be used for external-policy or fixation reporting unless a referenced non-CCSP normative specification explicitly defines that artifact as part of the signed payload semantics.

---

## 14. Relationship to other CERTCRYPT specifications

- **[CCCP/1](../../CCCP/1/index.md)** defines canonicalization, hashing, and commitments
- **CCSP/1** defines certificate envelope structure and serialization
- **[verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md)** defines minimum fail-closed verifier behavior under CERTCRYPT
- **[security-model/1](../../../foundation/security-model/1/index.md)** defines the foundational interpretation boundaries that constrain every verifier output
- subject profiles define certified content
- consistency protocols ([CCVP/1](../../CCVP/1/index.md)) define declared-context consistency outcomes

CCSP/1 relies on [CCCP/1](../../CCCP/1/index.md) as the sole authority for the definition and computation of all commitment values referenced by this protocol.

[verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md) does not define certificate validity. It defines the minimum fail-closed verifier behavior that any conforming implementation of CCSP/1 verification logic MUST satisfy.

---

## 15. Versioning & extensibility
 
- **Protocol identifier:** `CCSP/1` (include in logs/evidence metadata).  
- New optional fields MAY be added inside `metadata` or `payload`  
- Existing fields MUST NOT change meaning  
- Breaking envelope changes require a new CCSP major version  
- Any change that alters envelope structure or serialization rules MUST increment the major version 

Forward compatibility under CCSP/1 MUST preserve verifier convergence for normative outcomes.

If newly encountered optional fields or implementation-local modes would cause uncertainty about higher-layer meaning or verifier convergence, the implementation MUST fail closed for that normative evaluation path.

---

## 16. References

- CERTCRYPT Specifications
    - [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../CCCP/1/index.md)
    - [CCVP/1 — CERTCRYPT Consistency Verification Protocol](../../CCVP/1/index.md)
    - [composite-signature/1 — CERTCRYPT Composite Signature Profile](../../../foundation/composite-signature/1/index.md)
    - [system-domain/1 — CERTCRYPT System Domain](../../../foundation/system-domain/1/index.md)
    - [verifier-toolkit/1 — CERTCRYPT verifier toolkit](../../../ecosystem/verification/verifier-toolkit/1/index.md)
    - [subject.email/1 — CERTCRYPT Email Subject Canonicalization Profile](../../../profiles/subject.email/1/index.md)
    - [subject.binary/1 — CERTCRYPT Binary Subject Canonicalization Profile](../../../profiles/subject.binary/1/index.md)
    - [subject.text/1 — CERTCRYPT Plain Text Subject Canonicalization Profile](../../../profiles/subject.text/1/index.md)
    - [subject.collection/1 — CERTCRYPT Collection Subject Canonicalization Profile](../../../profiles/subject.collection/1/index.md)
    - [security-model/1 — CERTCRYPT Security Model](../../../foundation/security-model/1/index.md)
    - [subject.ai-decision/1 — CERTCRYPT AI-Decision Subject Canonicalization Profile](../../../profiles/subject.ai-decision/1/index.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
    - [RFC 8785 — JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785)
    - [RFC 8259 — The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259)
    - [RFC 4648 — The Base16, Base32, and Base64 Data Encodings](https://www.rfc-editor.org/rfc/rfc4648)
    - [RFC 3339 — Date and Time on the Internet: Timestamps](https://www.rfc-editor.org/rfc/rfc3339)

---

**End of CCSP/1**
