# CERTCRYPT Verifier Toolkit Specification (verifier-toolkit/1)

**Identifier:** `verifier-toolkit/1`  

**Label:** CERTCRYPT Verifier Toolkit Specification (verifier-toolkit/1)  

**Type:** Ecosystem Specification

**Status:** Frozen

**Layer:** Layer 3 — Ecosystem

**Depends on:** See References *(active normative dependencies are listed below)*  

**Naming convention:**  
`verifier-toolkit/1` is the formal identifier.  
CERTCRYPT Verifier Toolkit Specification (verifier-toolkit/1) is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.  

**Audience:** Implementers, verifiers, ecosystem integrators, auditors  

**Purpose:** Define the normative semantics, constraints, and interpretation boundary of verifier-toolkit/1 within the active CERTCRYPT public architecture.  

**Intended use:** verifier-toolkit/1 is intended to be the authoritative public specification used by conforming implementers, verifiers, auditors, and ecosystem tooling when handling this artifact or behavior.  

**Scope:** Defines the active normative behavior of verifier-toolkit/1; adjacent protocols, profiles, operational tooling, and product behavior remain out of scope except where explicitly referenced.  

**Non-goals:** verifier-toolkit/1 does not prove truth, semantic validity, legal validity, or live service authority by itself, and MUST NOT be interpreted as a substitute for cryptographic authenticity, Proof of Independence, or managed-service behavior outside its own normative scope.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale
This specification defines the minimum conformance boundary for `verifier-toolkit` within CERTCRYPT.

`verifier-toolkit` is the reference offline verifier toolkit for CERTCRYPT artifacts.

It does not emit certificates, does not perform fixation, does not execute settlement, and does not act as a live authority.

Its function is to verify `Issued` and `Independent` results using the certificate, original material when the applicable verification path requires it, and the artifacts required by the applicable public rules.

Verification under this specification MUST NOT depend on:

- the issuer as a live service
- CERTCRYPT as a live authority
- a CERTCRYPT API
- a CERTCRYPT dashboard
- a managed resolver as a required verification dependency

---

## 2. Scope

This specification applies to all implementations, libraries, CLIs, SDKs, verifier services, hosted verifier surfaces, and reference tools that claim conformance with `verifier-toolkit/1`.

Any implementation claiming conformance with `verifier-toolkit/1` MUST:

- support the minimum verification targets defined here
- implement the mandatory standard offline verification baseline for `Independent`
- fail closed when that baseline cannot be completed
- avoid introducing semantic inflation beyond applicable public rules

This specification does **not** redefine:

- certificate issuance semantics
- `independence_proof` semantics
- `verification_package` semantics
- system-domain attribution rules
- rules-domain selection rules
- complete verification against original material

Those concerns remain governed by their own public specifications.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

---

## 4. Design principles

`verifier-toolkit/1` is designed around the following principles:

- **Deterministic verification:** Given the same inputs and the same public rules, every conforming toolkit implementation MUST return the same result: the same result code, the same resolved target and the same set of failed check identifiers (§9.5–§9.7). This is a requirement on each implementation, checked one implementation at a time against the public conformance suite (§17); it holds for any implementation in any language that claims conformance, and does not depend on how many implementations exist.
- **Fail-closed adversarial posture:** Plausibility, compatibility, or hosted convenience MUST NOT replace exact validation under public rules.
- **Proof without data custody:** Verification MUST rely on certificates, carried artifacts, public rules, and verifier-local original material where required, not on platform-held data.
- **Institutional independence:** Verification outcomes MUST remain obtainable without dependence on continued issuer, operator, or managed CERTCRYPT service existence.
- **Infrastructure neutrality:** The toolkit contract MUST remain stable across local, hosted, packaged, and independently assembled verification flows.
- **Interpretation boundaries:** The toolkit enables independent evaluation under formal rules. It does not determine truth, legal meaning, or semantic validation.

Within that boundary, a standard verifier validates `Independent` at the proof level from canonical offline artifacts under public rules.

An advanced auditor MAY additionally inspect or reconstruct deeper settlement-layer material, raw economic substrate, or publication-layer context.

Such deeper inspection MAY reinforce auditability, but it is not a prerequisite for the standard conforming verifier path.

---

## 5. Core thesis

`verifier-toolkit` is **not**:

- a source of authority independent of the artifacts it validates
- a semantic upgrade of `independence_proof`
- a hosted verification dependency
- a proof generator
- a replacement for complete verification against original material

`verifier-toolkit` **is**:

- the minimum fail-closed reference verifier behavior for CERTCRYPT artifacts
- the verifier baseline by which `Issued` and `Independent` can be evaluated offline under public rules
- a tooling boundary intended to make correct verification easier than degraded verification

No conforming toolkit MAY return, present, or imply `INDEPENDENT_VALID` unless the mandatory standard offline verification baseline for `Independent` has actually been executed successfully.

---

## 6. Minimum supported verification targets

The minimum conforming toolkit MUST support these two verification routes:

- `Issued`
- `Independent`

It MUST support those routes from either:

- a `verification_package` used as an offline convenience container
- or an equivalent independently supplied artifact set under the same public rules

`verification_package` is OPTIONAL as an input mechanism.

If the same required artifacts are available independently under the same public rules, a conforming toolkit MUST accept that equivalent artifact set and MUST NOT require the package as the only valid entry path.

Implementations SHOULD prefer deterministic artifact completeness over convenience packaging assumptions.

Package convenience MUST NOT be used to excuse omitted inputs, implicit artifact discovery, or heuristic reconstruction of a supposedly offline-complete verification path.

Each artifact has exactly one source in a request. When a `verification_package` is the input, the artifacts it carries are read from it and from nowhere else; an artifact supplied beside the package, or a package supplied beside an independently supplied artifact set, is `REJECTED` (`INPUT_COMBINATION_VALID`) rather than resolved by choosing one copy. A toolkit identifies each supplied artifact by the slot it was supplied in — a package member's name, or the input the caller named — and never by inspecting its content to guess what it is. An interface built on a toolkit that lets a person supply loose files without naming their slots MAY assign each file to a slot by recognizing its kind, provided that a file is assigned only when exactly one kind recognizes it, that the assignment is shown before the result is presented, and that an archive is read by entry name only (`verification-package/1` §22.2).

---

## 7. Normative toolkit principles

A conforming toolkit MUST satisfy all of the following.

### 7.1 Fail closed

If:

- a required check is omitted
- a required artifact is missing
- a required version is unsupported
- parsing is ambiguous
- a fallback or compatibility heuristic would be required
- the verifier path is only partial

then the toolkit MUST NOT return `INDEPENDENT_VALID`.

A conforming toolkit MUST NOT offer any configuration, mode or option under which a signature is accepted without being cryptographically verified — not for testing, not for conformance runs, not with a warning. Test configurations change which keys, roots and rules domains are trusted; they never change whether a signature is verified.

### 7.2 No heuristics

The toolkit MUST NOT:

- choose `rules_version` heuristically
- accept parser downgrade
- rescue artifacts through structural plausibility
- substitute “compatible enough” interpretation for exact rules-domain or system-domain validation

Every JSON input the toolkit reads — each artifact, and the material of a JSON subject profile — MUST be parsed as strict JSON: RFC 8259, and no object at any depth repeating a member name, compared after escape decoding ([CCSP/1](../../../../protocols/CCSP/1/specification.md) Section 8.1). An input that repeats a member name is `REJECTED` (subject material: the profile does not apply), never read by keeping one of the duplicates. A toolkit that accepts artifacts already parsed by its caller MUST state that the caller is responsible for parsing them strictly.

A verifier MUST NOT accept independence semantics from systems that do not match the exact system-domain attribution and exact rules-domain required by the proof under public rules.

### 7.3 Offline by default

The standard verification path MUST NOT require:

- live CERTCRYPT infrastructure
- live issuer infrastructure
- a managed resolver
- a managed storage dependency
- discretionary assistance from any authority

### 7.4 No authority inflation

Neither:

- `verification_package`
- an optional delivery signature
- the mandatory proof signature (independence.proof/1 §10.13)
- a node attestation (independence.proof/1 §10.15)
- a hosted viewer
- a resolver response

may be treated as the ontological source of `Independent`.

### 7.5 No semantic inflation

`Independent` MUST NOT be presented by the toolkit as:

- truth
- legitimacy
- legal validity
- institutional endorsement
- complete verification against original material

It means only structural independence under public rules.

---

## 8. Minimum supported inputs

### 8.1 For `Issued`

The minimum conforming toolkit MUST support:

- `base_certificate`
- original material only when the applicable verification path requires comparison against subject bindings or issuer-declared properties

### 8.2 For `Independent`

The minimum conforming toolkit MUST support:

- `base_certificate`
- `independence_proof`
- the supporting proof material required by the proof model and applicable public rules
- for each base certificate, its per-commitment inclusion path binding the certificate's accepted commitment into the claimed `subtree_root`, together with the zero-data capacity evidence for that commitment, sufficient to run the hybrid emission binding (independence.proof/1 §7.10, §12.4)
- `settlement_ref` or settlement-derived proof material satisfying the settlement-material contract of the aggregated settlement profile the applicable public rules select for the declared `rules_version`
- `inclusion_proof`
- the `system-foundation/1` statement of the system domain, as system-domain attribution material
- the exact applicable public rules

The `system-foundation/1` statement is public rules material. The verifier obtains it on its own — from the publication of the system domain, or from its own configuration — and never from a `verification_package` or from the party presenting the artifacts. It accepts the statement only when its recomputed system root fingerprint, its `foundation_statement_id` and the digest of its signed payload are exactly the `bootstrap_system_root_fingerprint`, `foundation_statement_id` and `foundation_payload_digest` the registry entry of the system domain declares ([system-domain/1](../../../../foundation/system-domain/1/specification.md) Section 16.1); a conforming toolkit holds those three values in its configuration and compares them, so a statement of the right shape with another root, another identifier or any other signed content is `REJECTED`. A toolkit SHOULD also ship the statement itself, which the registry entry publishes, and use it whenever a request supplies none; a statement supplied with a request is checked against the same three values.

`published_rules_versions` inside the statement is metadata ([system-foundation/1](../../../../foundation/system-foundation/1/specification.md) Section 6): a toolkit MUST NOT reject because the applicable `rules_version` is absent from it. Which rules versions a system domain admits is fixed by its rules registry and by the toolkit's configuration.

The toolkit MUST treat capacity as settlement-bound, CERTCRYPT-domain-bound, and non-reconstructible from outside the certified settlement context.

No local estimate, external economic guess, detached authorization artifact, or settlement-like approximation MAY be treated as normatively equivalent to settlement-bound CERTCRYPT capacity validation under the applicable public rules.

No toolkit MAY treat authorization as consumed merely because a commitment exists.

The toolkit MUST validate the exact authorization-to-consumption bridge required by the selected `settlement_profile_id`.

### 8.3 When `verification_package` is used

The package MUST be treated as a container only.

The toolkit MUST validate the contents under the package semantics defined by `verification-package/1`.

The package MUST NOT be treated as a source of truth independent of its artifacts.

### 8.4 Collection evidence discipline

When a verification target involves a certified subject governed by `subject.collection/1`, a conforming toolkit MUST preserve the semantic distinction between:

- one opaque non-collection subject proof
- one collection-level subject proof
- one element-level inclusion verification path

For such targets, a conforming toolkit MUST NOT:

- present one opaque non-collection subject as if it were many independently proven records
- present one collection-level root commitment as if element-level verification had already occurred
- ignore the profile a leaf declares when an element-level workflow requires leaf interpretation
- treat an unsupported `commitment_scheme` or an unsupported leaf profile as warning-only success for an element-level claim

If an element-level workflow requires collection inclusion proof semantics, the toolkit MUST support the exact declared `commitment_scheme` and every profile the leaves declare, or fail closed as `UNSUPPORTED`, `INCOMPLETE`, or `REJECTED` as applicable.

#### 8.4.1 Element-level inclusion operation

A conforming toolkit MUST expose an element-level inclusion operation for the collection commitment scheme it supports: given ONE declared leaf of a `subject.collection/1` subject — the leaf's value under the profile that leaf declares — together with that leaf's inclusion proof object and the collection's declared `root` and `declared_cardinality`, the operation MUST confirm whether that one leaf belongs to the declared root **without requiring the rest of the collection**. This is the operation that lets any declared part of a collection be checked on its own against the committed whole.

When `commitment_scheme` is `collection.merkle-sha3-256/1`, this operation MUST follow the inclusion-proof object model and verification procedure of that scheme exactly (`collection.merkle-sha3-256/1` §14 proof object, §15 verification procedure), and MUST reject under §16 of that scheme for a false leaf, a false or reordered inclusion path, a proof carrying too few or too many sibling hashes for the tree shape, a `leaf_index` that is missing, non-canonical, or out of the declared bounds, a `proof_version` that is not exactly the scheme identifier, or a recomputed root that differs from the declared `root`. The operation MUST be fail-closed: adversary-controlled proof material MUST NOT be accepted, and MUST NOT cause the toolkit to fall back to any other scheme or to a whole-set reconstruction.

A positive element-level result MUST reconstruct the identical `root` the whole-set root construction (§8.5.3) would compute over the full ordered leaf set; the two MUST NOT diverge. This operation establishes membership of one declared element only; it does not, by itself, establish that the full hidden collection is complete, truthful, or semantically accepted (that remains governed by §8.5.4 and the applicable economic-layer rules). It is distinct from the settlement-layer Merkle of `settlement.binding/1` (§8.5.3): the toolkit MUST NOT substitute one for the other.

#### 8.4.2 Element-level inclusion from the package alone

Because a `subject.collection/1` subject declares its leaves inside the SIGNED
certificate (`subject.collection/1` §7.4), a conforming toolkit MUST be able to perform
the §8.4.1 operation from the certificate and the leaf value alone, with no
inclusion-proof object supplied by any party.

Given the certificate and the bytes of ONE leaf value, the toolkit MUST:

0. verify the certificate under the `Issued` route (§11.1). The leaves are trustworthy only because they are signed: a certificate that is not `Issued`-valid yields no inclusion outcome, positive or negative;
1. fold the `commitment_digest_hex` values of `collection.leaves` per the declared
   scheme and require the result to equal the declared `root`. A failure here is
   `REJECTED`: the descriptor is signed, so a root that does not reconstruct means the
   artifact is internally inconsistent — not that the leaf is absent;
2. compute the salted commitment of the supplied value, salted with the anchor
   `nonce_hex` (`subject.collection/1` §8). Because leaves MAY declare DIFFERENT
   profiles, the toolkit MUST try the distinct profiles that `collection.leaves`
   declares; it MUST NOT assume one profile for the whole collection, and it MUST NOT
   require the caller to state which leaf they hold;
3. locate that commitment among `collection.leaves`. Its position IS the `leaf_index`.
   If it is absent under every declared profile, the leaf does not belong to the
   declared collection and the result is a negative inclusion outcome — NOT an error;
4. derive the sibling path for that index and verify inclusion exactly as §8.4.1
   requires.

If the same commitment appears at more than one position (a collection MAY contain
identical leaf values under the same profile), the toolkit MUST treat inclusion as established and MUST NOT report a
single canonical index as if the value occurred once.

A declared leaf profile the toolkit does not support prevents a negative outcome
(`UNSUPPORTED`, §8.4) but not a positive one: a match under another declared profile
stands. The operation therefore has exactly these outcomes: the value is a declared
element (with every position it occupies), it is not, the certificate is not
`Issued`-valid, the descriptor is internally inconsistent (`REJECTED`), or a profile or
scheme is unsupported. A conforming toolkit exposes this operation itself; an
application built on the toolkit consumes it rather than re-deriving the path.

A toolkit MUST NOT present a result from this path as stronger than §8.4.1: it
establishes membership of one declared element, not completeness or truthfulness of
the hidden collection.

### 8.5 Original-material delivery format

When the selected verification path requires comparison against original material (subject binding, issuer-declared properties, complete verification — §15), the toolkit MUST accept that material in a deterministic, language-agnostic delivery format so that conforming implementations in any language converge on the same result. This section defines the minimum format; it is an INPUT contract, not a carried artifact (the `verification_package` MUST NOT include original material — `verification-package/1` §10).

The delivery is a **subject-material map**: an association from each subject the certificate commits to (in `base_certificate.payload.anchor.subjects[]`, in order) to the exact bytes the verifier canonicalizes for that subject.

#### 8.5.1 Mapping and ordering

- The map MUST resolve every subject the selected verification path needs, keyed by the subject's **zero-based index** in `anchor.subjects[]`. The certificate is the sole source of cardinality and order. The verifier MUST establish the index → bytes association by reading the certificate's subject indices in strict numeric order (0, 1, …, N-1); it MUST NOT infer order from filesystem listing, archive metadata, modification time, or transport sequence. The logical mapping is normative and MUST be identical across toolkits given identical inputs; the concrete container (a directory keyed by index, a keyed archive, an in-memory map) is an implementation choice, and conformance golden vectors pin the recomputation, not the container.
- The material delivery MUST NOT add, reorder, or redefine subjects. Outcomes for a non-conformant delivery are fixed so toolkits converge: a delivery missing a subject (or, for a collection, a leaf) required by the selected path is `INCOMPLETE`; a delivery whose ordering contradicts the certificate, that keys material to anything other than a subject index `0 … N-1` of the certificate (an index at or beyond the declared subject count, or a key that is not an index), that delivers a non-collection subject as a list of leaves, or whose collection leaf count differs from `declared_cardinality` is `REJECTED`; a subject whose declared `profile`, declared leaf profiles, or `commitment_scheme` the toolkit does not support is `UNSUPPORTED` (no fallback, downgrade, or heuristic reinterpretation under a different profile).
- Two distinct subjects (different indices) MAY carry identical `canonical_bytes`; the toolkit validates each index independently and MUST NOT reject solely on byte-equality across indices.

#### 8.5.2 Per-subject recomputation

For each subject, the toolkit recomputes `canonical_bytes(subject)` under the subject's declared `profile` (the applicable `subject.*` profile), derives the verifier-local `subject_local_digest_hex = SHA3-256(canonical_bytes(subject))`, and recomputes the commitment `SHA3-256(ASCII(nonce_hex) || ASCII(subject_local_digest_hex))` (CCCP/1). It MUST equal the certificate's `commitment_digest_hex` for that subject. A mismatch is `ISSUED_INVALID` under `ORIGINAL_MATERIAL_COMPARISON_VALID`: the comparison belongs to the `Issued` route (§11.1 step 3), it completed, and the material is not the committed one (§9.1). The comparison is a separate plane from the `Independent` baseline: a mismatch does not stop the `Independent` route, and the independence axis is reported on its own (§9.6).

- All hex values (`nonce_hex`, `subject_local_digest_hex`, the commitment digest) are **lowercase hexadecimal**, 64 characters for SHA3-256 (CCCP/1 §7.1). The `ASCII(...)` operands are the byte sequences of those lowercase hex strings (for hex-only strings UTF-8 equals ASCII), concatenated directly — NOT the binary digests.
- A conforming toolkit MUST support at minimum the `subject.binary/1`, `subject.email/1`, and `subject.collection/1` profiles. An unsupported declared profile fails closed as `UNSUPPORTED` (§8.5.1); `subject.email/1` is therefore not an unsupported-profile outcome for a conforming toolkit.
- Material bytes MUST be delivered byte-exact, except where §8.5.7 admits a digest in their place. The toolkit MUST NOT normalize, re-encode, strip a BOM, decompress, or otherwise transform bytes before applying the profile's `canonical_bytes` rule; the profile alone defines any canonicalization (e.g. `subject.binary/1` is byte-identity).

#### 8.5.3 Collection subjects

For a subject governed by `subject.collection/1`, the delivered material is the **ordered set of leaf materials** of the collection. The toolkit recomputes each leaf under the profile THAT leaf declares (leaves MAY differ), reconstructs the root under the declared `commitment_scheme`, and MUST find: (1) the recomputed root equal to the collection's `root`; and (2) the count of **leaf materials that participated in the root computation** equal to the declared `declared_cardinality` (extra items in the delivery container that do not participate in the tree are not leaves and MUST NOT be counted). A leaf, or a root, that does not recompute fails as §8.5.2 defines (`ISSUED_INVALID`): the delivered leaves are not the committed ones. A count that differs from `declared_cardinality` is `REJECTED` (§8.5.1): the delivery does not have the shape the certificate declares. This is what makes the declared cardinality, and the volume it implies for declared collections, checkable.

- When `commitment_scheme` is `collection.merkle-sha3-256/1`, the toolkit MUST use the exact leaf-preimage and internal-node construction of that scheme — including the **collection salt**, the domain-separation tags, the big-endian `u64be` length prefixes, the odd-width promotion rule, and the single-leaf rule (a one-leaf collection's root is the leaf hash itself, not re-hashed). This scheme is **distinct from the settlement-layer Merkle** of `settlement.binding/1` (different leaf-preimage, tags, and binding fields); the toolkit MUST NOT substitute one for the other.
- The collection salt MUST be the anchor `nonce_hex` of the certificate under verification, per `subject.collection/1` §8. The toolkit MUST NOT accept a salt supplied alongside the delivered leaves, and MUST NOT reconstruct a root without one: an unsalted reconstruction produces a different root and MUST fail closed rather than be attempted as a fallback.
- A collection declaring `declared_cardinality = 0` is non-conformant (the scheme prohibits empty trees) → `REJECTED`.

#### 8.5.4 Scope of this check

This check establishes only that the delivered material matches what the certificate's subjects committed to, at the resolution the issuer declared. It does NOT inspect the inside of an opaque non-collection subject: an issuer MAY present many records as one opaque `subject.binary/1` (one proof over the container), and §8.5 will confirm that one opaque commitment without decomposing it. Whether such packaging is economically fair — i.e. whether declared volume matches the material's real granularity — is governed by `capacity.commitment/1` quantity rules and issuer-declared properties at the economic layer, not by §8.5. §8.5 makes cardinality and volume checkable for subjects declared as collections; it does not, by itself, force a non-collection subject to reveal internal cardinality.

#### 8.5.5 Locality

This delivery format carries no protocol identity and no aggregate: it is the verifier's own material, used locally to confirm the certificate's commitments. Record-local part IDs used by §8.5.6 identify only descriptors inside the already matched decision record. The certificate's commitments remain opaque, but disclosure of an AI-decision record reveals its part nonces and salted commitments; a recipient can test candidate material. Fresh per-part nonces prevent stable cross-record fingerprints absent nonce reuse, not candidate-dictionary testing after disclosure. The subject-material map, record-local part IDs and every raw `subject_local_digest_hex` the toolkit computes are verifier-local apparatus: a conforming toolkit MUST NOT publish, transmit, or embed them in any certificate, output, or diagnostic surface that enables subject tracking or cross-certificate correlation (CCCP/1 §7.3).

#### 8.5.6 AI-decision subjects: ordered input and output material

For a subject governed by `subject.ai-decision/1`, the delivered subject material is the complete decision record, recomputed exactly as §8.5.2 defines. The delivery MAY additionally carry any subset of the record's declared input and output parts. Nested parts are keyed by the globally unique `id` declared in the record; their association MUST NOT be inferred from a filename, array position, media type, role, or delivery order. A toolkit that supports `subject.ai-decision/1` MUST accept this delivery.

Only after the decision record matches its committed subject, the toolkit, for each delivered part:

1. resolves the part's descriptor by exact `id` from the matched record and reads `profile`, `material_nonce_hex` and `commitment_digest_hex` only from that descriptor;
2. computes `subject_local_digest_hex = SHA3-256(canonical_bytes(material))` under that `profile`, as 64 lowercase hexadecimal characters, or applies the verifier-local digest delivery of §8.5.7 when and only when the descriptor declares `subject.binary/1`;
3. derives `SHA3-256(ASCII(material_nonce_hex) || ASCII(subject_local_digest_hex))` exactly as CCCP/1 §8.1 requires and requires the result to equal the descriptor's `commitment_digest_hex`.

Outcomes are fixed so toolkits converge:

- A part whose recomputed commitment differs from its `commitment_digest_hex` fails closed with the same outcome as a subject whose recomputed commitment differs (§8.5.2).
- A part the declared `profile` cannot canonicalize (for example, bytes that are not UTF-8 under `subject.text/1`) is `REJECTED`.
- A nested delivery with an `id` absent from the matched record, a duplicate delivered `id`, or an attempt to identify a part by anything other than its declared `id` is `REJECTED`.
- Nested material is compared only against a record that matched. A record that is missing is `INCOMPLETE` (§8.5.1) and a record that does not match fails as §8.5.2 defines; in neither case is the nested material opened.
- Delivering no nested parts is valid. The toolkit MUST NOT report a part it did not compare as compared. Omission of one declared part does not prevent comparison of another delivered part.
- The arrays and their descriptor order belong to the matched record. The toolkit MUST NOT reorder them or interpret `role`, `media_type`, `observation_scope`, `provider`, `model`, `version`, `context`, `decision_id` or `decision` as proof of execution causality, provider identity, semantic correctness, or compliance.
- A nested part governed by `subject.ai-decision/1` is compared as one complete decision-record material. Its own nested input and output parts are not opened recursively by this delivery; a caller performs a separate subject-material comparison when it needs to evaluate that chained record's parts.

The input and output profiles a record may declare are fixed by `subject.ai-decision/1` §7.4 and checked as a precondition of the record itself. Descriptor IDs and material nonces are globally unique within the record as that profile requires; a duplicate material nonce makes the record non-conformant and is `REJECTED`. A match establishes only that each held part is the material its descriptor commits to; it establishes nothing about the decision (`subject.ai-decision/1` §12). Nested materials, part IDs and raw subject-local digests are verifier-local apparatus under §8.5.5.

#### 8.5.7 Digest delivery for byte-identity profiles

For a subject, or an AI-decision nested part, whose profile defines `canonical_bytes` as the input bytes unchanged — in the profiles of this corpus, only `subject.binary/1` — the delivery MAY carry, instead of the bytes, the `subject_local_digest_hex` the verifier's own environment computed over them (for example by hashing a file too large to hold at once in chunks). The toolkit:

- requires the digest to be exactly 64 lowercase hexadecimal characters, otherwise `REJECTED`;
- for a certificate subject, recomputes the commitment from it exactly as §8.5.2 does from the bytes, with the same outcome on a mismatch;
- for a nested part under §8.5.6, first requires the parent decision record to match, resolves the descriptor by `id`, requires its profile to be exactly `subject.binary/1`, derives `SHA3-256(ASCII(material_nonce_hex) || ASCII(delivered_subject_local_digest_hex))`, and compares that result with the descriptor's `commitment_digest_hex`, with the same outcome on mismatch as §8.5.6.

A digest delivered for a subject or nested part under any other profile is `REJECTED`: those profiles transform the material before hashing, so a digest of raw bytes is a different value, and comparing it would report a material mismatch where the fault is the delivery. A digest is not accepted in place of a collection leaf (§8.5.3). A result reached from a delivered digest states the same as one reached from bytes only on the condition that the delivering environment hashed the bytes it holds; that environment is the verifier's own, so no third party is trusted. The digest is verifier-local apparatus under §8.5.5.

---

## 9. Output taxonomy

The minimum conforming toolkit MUST expose a strict result taxonomy including at least:

- `ISSUED_VALID`
- `ISSUED_INVALID`
- `INDEPENDENT_VALID`
- `INDEPENDENT_INVALID`
- `INCOMPLETE`
- `UNSUPPORTED`
- `REJECTED`

### 9.1 Output meaning

- `ISSUED_VALID` means the `Issued` path succeeded under applicable public rules.
- `ISSUED_INVALID` means the `Issued` path completed and failed.
- `INDEPENDENT_VALID` means the mandatory standard offline verification baseline for `Independent` completed successfully.
- `INDEPENDENT_INVALID` means the `Independent` path completed and failed under applicable public rules.
- `INCOMPLETE` means the selected path could not be completed because required artifacts or required material were absent.
- `UNSUPPORTED` means the path could not be completed because the applicable version, model, or required capability is not supported by the toolkit.
- `REJECTED` means the input is malformed, ambiguous, parser-dependent, heuristically recoverable only, or otherwise non-conformant for the selected normative path.

### 9.2 Prohibited success

No conforming toolkit MAY return `INDEPENDENT_VALID` if:

- any required check was omitted
- any required artifact was absent
- any fallback or compatibility heuristic was applied
- any required validation remained partial

### 9.3 Output presentation discipline

Conforming toolkits, hosted verifier surfaces, SDK wrappers, widgets, and reports MUST preserve the semantic distinction between:

- `INDEPENDENT_VALID`
- `INDEPENDENT_INVALID`
- `INCOMPLETE`
- `UNSUPPORTED`
- `REJECTED`

Those outcomes MUST NOT be collapsed into a generic success-style presentation such as:

- a single green “verified” result
- a generic “independent” badge
- a trust-style summary that hides incompleteness or unsupported capability

Hosted mediation, exploratory review, preview output, or partial artifact inspection MUST NOT be presented as semantically equivalent to a completed conforming `Independent` verification path.

#### 9.3.1 Attested node

When the proof carries a node attestation (independence.proof/1 §10.15) and the result is `INDEPENDENT_VALID`, a conforming toolkit SHOULD expose the attested `node_id` and `recognized_at` in its result, authenticated by the proof signature and without consulting any register of nodes. On any other result it MUST NOT expose them as attested. A toolkit MUST present the attested node as the transport the submission entered through, never as the issuer, an endorsement, or a time seal of the certified content.

### 9.4 Mandatory rejection classes

At minimum, a conforming toolkit MUST reject any attempted `Independent` verification path belonging to any of the following classes:

1. **Retroactive proof fabrication:** proof material presented for a certificate or leaf that did not validly declare issuance-time participation under the applicable public rules
2. **Hash-plus-anchor reduction:** document hashing, anchoring, publication, or receipt material presented as if it were sufficient to establish `Independent`
3. **Issuer-dependent verification:** any path that still requires the issuer to exist, respond, or reconstruct the proof context as a live dependency
4. **Provider-dependent verification:** any path that requires a live CERTCRYPT API, dashboard, resolver, or managed service to stand in for canonical offline artifacts
5. **Receipt equivalence:** any path in which a publication receipt, settlement transaction reference, or transport acknowledgment is treated as sufficient by itself
6. **Multi-proof ambiguity:** any path in which multiple materially different proof contexts could validate the same claimed independence result under the same system domain and rules domain
7. **Capacity spoofing:** any path in which `Independent` is claimed without settlement-bound consumption of valid CERTCRYPT capacity under public rules
8. **Replay or recontextualization:** any path in which proof material, settlement material, or inclusion material can be reused across another leaf, another settlement context, or another rules or system context
9. **Post-hoc reconstruction without issuance binding:** any path in which later artifacts alone are used to synthesize a valid independence result absent the required issuance-time reference
10. **Compatible-enough acceptance:** any path in which visually similar, partially compatible, externally anchored, or otherwise approximate artifacts are accepted as if they were exact CERTCRYPT proof context

These classes are mandatory negative cases, not illustrative examples only.

No conforming toolkit MAY downgrade any of them into warning-only, preview-only, or compatibility-only success semantics.

To "reject", in this section and in Sections 13 and 14, means to return no `*_VALID` result. Which non-success code is returned is not left to the implementation: it follows from §9.5, and the check that fails is the one §9.7 names. The classes map as follows:

| Class | Failing check (§9.7) | Result code |
|---|---|---|
| 1. Retroactive proof fabrication | `ISSUANCE_PARTICIPATION_VALID`, `SETTLEMENT_NOT_RETROACTIVE` | `INDEPENDENT_INVALID` |
| 2. Hash-plus-anchor reduction | `TARGET_AUTO_RESOLUTION_VALID` or `PROOF_PRESENT` (no proof), `SETTLEMENT_REF_VALID` (no settlement material) | `INCOMPLETE` |
| 3. Issuer-dependent verification | the check whose artifact is absent | `INCOMPLETE` |
| 4. Provider-dependent verification | the check whose artifact is absent | `INCOMPLETE` |
| 5. Receipt equivalence | `SETTLEMENT_REF_VALID` (a reference without settlement material) | `INCOMPLETE` |
| 6. Multi-proof ambiguity | `AGGREGATED_INTERPRETATION_UNIQUE` | `INDEPENDENT_INVALID` |
| 7. Capacity spoofing | `CAPACITY_BINDING_VALID`, `CAPACITY_NOT_RECONSTRUCTED`, `CAPACITY_EVIDENCE_VALID` | `INDEPENDENT_INVALID`; `INCOMPLETE` when the capacity material is absent |
| 8. Replay or recontextualization | `NON_REPLAY_VALID`, `ANTI_SPLICING_VALID`, `LEAF_BINDING_VALID` | `INDEPENDENT_INVALID` |
| 9. Post-hoc reconstruction without issuance binding | `ISSUANCE_PARTICIPATION_VALID` | `INDEPENDENT_INVALID` |
| 10. Compatible-enough acceptance | `SYSTEM_DOMAIN_EXACT`, `SYSTEM_ROOT_BINDING_VALID`, `CLONE_OR_FORK_REJECTED`; `RULES_DOMAIN_EXACT` | `INDEPENDENT_INVALID`; `RULES_DOMAIN_EXACT`: `REJECTED` (another rules version than the certificate's) or `UNSUPPORTED` (a version the toolkit does not evaluate) |

A malformed artifact in any class is `REJECTED` under the structural check of that artifact, before the class is reached.

### 9.5 Result code selection

The result code is a function of the failed checks and of the resolved target:

1. With no failed check, every check the route requires has run, and the result is `ISSUED_VALID` or `INDEPENDENT_VALID` for the resolved target. A required check that did not run is a failure (`INCOMPLETE`), never a pass.
2. Every failed check carries one classification: `REJECTED` (the input is malformed, ambiguous or non-conformant), `INCOMPLETE` (something required was absent), `UNSUPPORTED` (the version, profile, scheme or capability is not implemented), `ISSUED_INVALID` (a check of the `Issued` route completed and the certificate, or its material, is not what it claims) or `INDEPENDENT_INVALID` (a check of the `Independent` route completed and failed).
3. The result code is the highest classification among the failed checks, in this order: `REJECTED` > `INCOMPLETE` > `UNSUPPORTED` > `ISSUED_INVALID` > `INDEPENDENT_INVALID`.
4. When the resolved target is `Issued`, no result is `INDEPENDENT_INVALID`.
5. Before the target is resolved, the result reports the target the request named; a request that names no target (automatic selection, §11.4) and fails before resolution reports `Issued`.

### 9.6 Result object

A conforming toolkit returns its result as an object exposing at least these members, with these names and meanings:

- `result_code` — one of the codes of this section;
- `verification_target_requested` and `verification_target` — the target the request named and the target resolved (`Issued` or `Independent`);
- `input_mode` — `package` or `artifact_set`;
- `failed_check_ids` — the identifiers (§9.7) of every check that failed, each once; the SET is normative, its order is not;
- `required_artifacts_missing` — the artifacts whose absence made the result `INCOMPLETE`;
- `issued_valid` and `independent_valid` — the two axes, each true only when every check of its route passed; `independent_valid` is evaluated on its own, so a failed comparison against original material does not clear it;
- `complete_verification_against_original_material_performed` and `complete_verification_against_original_material_passed` — whether the comparison of §8.5 ran, and whether it matched;
- `subject_scope` — per subject, in anchor order, its declared `profile` and whether it is `opaque` (a single input the verdict does not look inside) or a declared collection (§8.4, §8.5.4);
- `attested_node` — as §9.3.1 defines;
- `production_verification` — whether the configuration is the published production profile of the system domain.

An implementation MAY expose more members. The full shape is published as the `verifier-result` JSON Schema of the public conformance suite (§17); a member that schema declares is not given another meaning.

### 9.7 Check identifiers

A conforming toolkit reports failures under these identifiers, with the classifications listed. An identifier names one requirement of this specification or of the specifications it applies; an implementation MUST NOT report a failure under another identifier, and MUST NOT report it under one of these when the requirement that failed is another.

| Identifier | Route | Requirement | Classifications |
|---|---|---|---|
| `INPUT_TARGET_SUPPORTED` | both | The requested target is `issued`, `independent` or `auto` | `UNSUPPORTED` |
| `INPUT_MODE_SUPPORTED` | both | The input mode is `package` or `artifact_set` | `UNSUPPORTED` |
| `INPUT_COMBINATION_VALID` | both | One source per artifact (§6); every input strict JSON (§7.2) | `REJECTED` |
| `TARGET_AUTO_RESOLUTION_VALID` | both | The target resolves without hiding an incomplete `Independent` verification (§11.4) | `INCOMPLETE` |
| `PACKAGE_STRUCTURE_VALID` | both | The package has the closed member set of `verification-package/1` §9.4 | `REJECTED` |
| `PACKAGE_CONTEXT_COHERENT` | both | The package's declarations agree with its artifacts (`verification-package/1` §13) | `REJECTED` |
| `BASE_CERTIFICATE_PRESENT` | both | A certificate is supplied | `INCOMPLETE` |
| `BASE_CERTIFICATE_STRUCTURE_VALID` | both | CCSP/1 Sections 6–9 | `REJECTED`, `UNSUPPORTED`, `INCOMPLETE` |
| `BASE_CERTIFICATE_AUTHENTIC` | both | The issuer composite signature verifies (both components) | `ISSUED_INVALID`, `REJECTED`, `UNSUPPORTED` |
| `ORIGINAL_MATERIAL_COMPARISON_VALID` | both | §8.5 | `ISSUED_INVALID`, `REJECTED`, `INCOMPLETE`, `UNSUPPORTED` |
| `PROOF_PRESENT` | Independent | A proof is supplied | `INCOMPLETE` |
| `PROOF_VERSION_SUPPORTED` | Independent | §12.2 step 1, version | `UNSUPPORTED` |
| `PROOF_STRUCTURE_VALID` | Independent | §12.2 step 1, structure | `REJECTED` |
| `RULES_DOMAIN_EXACT` | Independent | §12.2 step 2 | `REJECTED`, `UNSUPPORTED` |
| `RULES_CORPUS_COMMITMENT_PRESENT` | Independent | The toolkit holds the certified corpus commitment of the selected rules version ([rules-domain/1](../../../../foundation/rules-domain/1/specification.md) Section 13.3.1) | `REJECTED` |
| `SYSTEM_DOMAIN_EXACT` | Independent | §12.2 step 3, system domain | `INDEPENDENT_INVALID` |
| `SYSTEM_ROOT_BINDING_VALID` | Independent | §12.2 step 3, root binding | `INDEPENDENT_INVALID` |
| `CLONE_OR_FORK_REJECTED` | Independent | §13, clone or fork context | `INDEPENDENT_INVALID` |
| `PROOF_SIGNATURE_VALID` | Independent | §12.2 step 3, proof signature | `INCOMPLETE`, `UNSUPPORTED`, `REJECTED`, `INDEPENDENT_INVALID` |
| `LEAF_BINDING_VALID` | Independent | §12.2 step 4 | `INDEPENDENT_INVALID`, `INCOMPLETE`, `REJECTED` |
| `INCLUSION_PROOF_VALID` | Independent | §12.2 steps 5–6 | `INDEPENDENT_INVALID`, `INCOMPLETE`, `REJECTED` |
| `SETTLEMENT_REF_VALID` | Independent | §12.2 step 7 | `INDEPENDENT_INVALID`, `INCOMPLETE`, `REJECTED` |
| `FINALITY_SUFFICIENT` | Independent | §12.2 step 8 | `INDEPENDENT_INVALID`, `INCOMPLETE`, `REJECTED` |
| `SETTLEMENT_NOT_RETROACTIVE` | Independent | The settlement's `block_timestamp` is not after the commitment's `expires_at` ([settlement.binding/1](../../../settlement/settlement.binding/1/specification.md) §9) | `INDEPENDENT_INVALID`, `REJECTED` |
| `COMMITMENT_TTL_VALID` | Independent | The commitment's `expires_at` equals its `issued_at` plus the commitment TTL the rules domain declares ([capacity.commitment/1](../../../settlement/capacity.commitment/1/specification.md) §11.2) | `INDEPENDENT_INVALID`, `REJECTED` |
| `NON_REPLAY_VALID` | Independent | §12.2 step 9 | `INDEPENDENT_INVALID` |
| `EFFECTIVE_UNITS_BINDING_VALID` | Independent | §12.2 step 10 | `INDEPENDENT_INVALID`, `REJECTED` |
| `CAPACITY_EVIDENCE_VALID` | Independent | The capacity evidence verifies offline ([independence.proof/1](../../../../models/independence.proof/1/specification.md) §12.5) | `INDEPENDENT_INVALID`, `INCOMPLETE` |
| `CAPACITY_BINDING_VALID` | Independent | Settlement-bound consumption of that capacity (§8.2) | `INDEPENDENT_INVALID`, `INCOMPLETE` |
| `CAPACITY_NOT_RECONSTRUCTED` | Independent | No capacity inferred from outside the certified settlement context (§12.2) | `INDEPENDENT_INVALID`, `INCOMPLETE` |
| `AGGREGATED_INTERPRETATION_UNIQUE` | Independent | §14 | `INDEPENDENT_INVALID`, `INCOMPLETE` |
| `ISSUANCE_PARTICIPATION_VALID` | Independent | Issuance-time participation (§10) | `INDEPENDENT_INVALID` |
| `ANTI_SPLICING_VALID` | Independent | §13 | `INDEPENDENT_INVALID` |
| `FOUNDATION_PROFILE_VALID` | both | The statement has the shape of [system-foundation/1](../../../../foundation/system-foundation/1/specification.md) | `REJECTED` |
| `FOUNDATION_SYSTEM_ID_VALID` | both | The statement names the system domain | `REJECTED` |
| `FOUNDATION_FINGERPRINT_RECOMPUTED` | both | Its root fingerprint recomputes | `REJECTED` |
| `FOUNDATION_SIGNATURE_VALID` | both | Its quorum signatures verify | `REJECTED` |
| `FOUNDATION_BOOTSTRAP_MATCHES_RULES` | both | It is the registered bootstrap: root, statement id and signed payload (§8.2) | `REJECTED` |
| `FOUNDATION_SUCCESSOR_QUORUM_VALID` | both | Successor bindings carry their quorum ([system-manifest/1](../../../../foundation/system-manifest/1/specification.md) §12.3) | `REJECTED` |
| `FOUNDATION_EQUIVOCATION_DETECTED` | both | No equivocation among authenticated observations (system-manifest/1 §12.5) | `REJECTED` |

---

## 10. Mandatory standard offline verification baseline

The following minimum verification set is mandatory for any conforming `Independent` implementation:

- exact system-domain attribution
- exact rules-domain selection
- exact leaf binding
- exact settlement binding
- sufficient settlement finality
- settlement-bound capacity validation
- issuance-time participation validation
- anti-replay validation
- anti-splicing validation

This baseline MUST be implemented as a required standard path, not as best effort.

The baseline is atomic.

Partial execution of this baseline MUST be treated as failure, incompleteness, rejection, or unsupported capability under the applicable result taxonomy, not as degraded success.

This mandatory baseline defines the standard conforming verifier path.

A toolkit MAY additionally expose deeper audit capabilities over settlement-layer reconstruction, publication history, or raw economic substrate, but those capabilities MUST remain explicitly distinct from the standard conforming verifier path.

---

## 11. Minimum verification procedure

### 11.1 `Issued` route

For `Issued`, the toolkit MUST:

1. validate package structure if a package is used
2. validate the structure and authenticity of `base_certificate` under [CCSP/1](../../../../protocols/CCSP/1/specification.md) Sections 6–9 (its classification is read from the result as CCSP/1 Section 10.2 defines)
3. perform original-material comparison when the selected verification path requires it

### 11.2 `Independent` route

For `Independent`, the toolkit MUST:

1. validate package structure if a package is used
2. validate package coherence and anti-splicing requirements if a package is used
3. validate `Issued` over the `base_certificate`
4. validate `independence_proof` according to its normative semantics
5. validate all additional material required by that proof and the applicable public rules

The toolkit MUST NOT skip step 3 merely because a package claims `Independent`.

When step 3 fails on the certificate itself (`BASE_CERTIFICATE_STRUCTURE_VALID` or `BASE_CERTIFICATE_AUTHENTIC`), the toolkit MUST NOT run steps 4 and 5: a certificate that is not `Issued`-valid cannot be `Independent`, and checks run over it would report the same defect under other identifiers. A failed comparison against original material (§8.5) is not a failure of the certificate and does not stop the route.

#### 11.2.1 Deterministic aggregated verification flow

For the active aggregated settlement architecture, a conforming toolkit MUST be able to execute a deterministic logical flow equivalent to:

1. bind the base certificate to one accepted commitment through the hybrid emission binding: recompute `SHA3-256(JCS(base_certificate))`, require it to equal the `certificate_commitment_digest` carried by that commitment in the supplied capacity evidence, and verify that the commitment's `commitment_id` includes into `independence_proof.subtree_root` through the per-commitment inclusion path (independence.proof/1 §7.10, §12.4)
2. apply `inclusion_proof` to the claimed `subtree_root` and compare the computed root to `independence_proof.batch.root`
3. resolve the aggregated settlement container from `independence_proof.settlement_ref`, extract the fixed `settlement_root`, and compare it to `independence_proof.batch.root`
4. validate sufficient finality under the exact applicable public rules
5. validate anti-replay and uniqueness constraints

If any step fails, the toolkit MUST NOT return `INDEPENDENT_VALID`.

The toolkit MUST NOT:

- call CERTCRYPT as a live authority in order to rescue a failed standard offline path
- consult internal CERTCRYPT databases
- invent heuristic settlement interpretations
- fall back to another settlement profile

### 11.3 Optional consistency plane ([CCVP/1](../../../../protocols/CCVP/1/specification.md))

A toolkit MAY offer consistency verification under [CCVP/1](../../../../protocols/CCVP/1/specification.md). It is not part of the minimum conformance of Sections 10 and 18: a toolkit that does not offer it is not thereby incomplete.

A toolkit that offers it MUST:

1. take as input the target base certificate and the candidate context snapshot certificates themselves, never pre-extracted snapshot values or a caller-supplied issuer identity
2. require the target certificate to be `Issued`-valid under Section 11.1, and report `consistency-unknown` when it is not
3. verify every candidate snapshot certificate under Section 11.1 and discard those that are not `Issued`-valid
4. derive each snapshot's issuer from its verified issuer signature, as CCVP/1 Section 5.1 defines, and apply the rest of CCVP/1 — namespace, snapshot object, `subject.context-snapshot/1` commitment, instant comparison of timestamps, selection, equivocation, and entry binding with role and scope — without heuristics
5. report the outcome (`consistency-match`, `consistency-mismatch` or `consistency-unknown`) separately from the result code of Section 9

A consistency outcome MUST NOT change a result code, MUST NOT be a precondition of `ISSUED_VALID` or `INDEPENDENT_VALID`, and MUST NOT be presented as stronger verification, endorsement, or proximity to `Independent` ([CCVP/1](../../../../protocols/CCVP/1/specification.md) Section 0.3). CCVP/1 confers no authority on anyone; the outcome states alignment with one declared context and nothing else.

### 11.4 Target selection

A request names its target: `issued`, `independent`, or `auto`. A toolkit that offers `auto` resolves it deterministically: to `Independent` when ANY artifact of the `Independent` route is supplied — the `independence_proof`, settlement material, capacity evidence or a per-commitment inclusion path — and to `Issued` only when none is. Artifacts of the `Independent` route supplied without the `independence_proof` are an incomplete `Independent` verification, `INCOMPLETE` under `TARGET_AUTO_RESOLUTION_VALID`; they are never answered as an `Issued` verification, which would read as an answer about independence. A request for `independent` without a proof is `INCOMPLETE` under the same identifier.

---

## 12. Minimum requirements for `independence_proof`

### 12.1 Minimum supported logical fields

The minimum conforming toolkit MUST support proof models that contain or deterministically imply at least:

- `proof_version`
- `system_id`
- `system_root_fingerprint` when applicable
- `rules_version`
- `proof_id`
- `subtree_root`
- `closure_time`
- `consumed_commitment_ids`
- `settlement_ref`
- `settlement`
- `batch`
- `independence_result`
- `inclusion_proof`
- `anti_replay`
- `proof_digest`
- `signature`
- `node_attestation` when present (optional)

### 12.2 Minimum validation sequence

The toolkit MUST validate, in at least this logical order:

1. supported proof version, and the structural rules of independence.proof/1 §12.1: `proof_id` recomputed from the identity view, `proof_digest` recomputed, `closure_time` in RFC 3339 UTC with whole seconds, `consumed_commitment_ids` well formed, `node_attestation` well formed when present
2. exact rules-domain selection
3. exact system-domain attribution, not merely `system_id = "certcrypt"`, including the proof signature: a composite under the profile the rules select, by the system-domain Level-1 capacity key of the bootstrap statement, over the signed view (independence.proof/1 §10.13, §10.13.1). The signature is mandatory under every rules domain; when it is absent, cannot be verified for want of the key or of a component, or does not verify, the toolkit MUST NOT return `INDEPENDENT_VALID`
4. hybrid emission binding of the base certificate to one accepted commitment whose `commitment_id` includes into `subtree_root` (independence.proof/1 §7.10, §12.4)
5. `inclusion_proof` application to the claimed `subtree_root`
6. equality of computed root and claimed `batch.root`
7. `settlement_ref` resolution and equality of resolved `settlement_root` to claimed `batch.root`
8. sufficient finality under public rules, including the equality of every finality witness of the proof with the settlement material (independence.proof/1 §10.6)
9. anti-replay and uniqueness, recomputing `anti_replay` from `settlement_ref` and `subtree_root` (independence.proof/1 §10.9)
10. effective-declared-units binding: the issuer-declared per-subject quantity (`declared_effective_units`, carried in the bound capacity evidence) equals the sum of per-subject effective declared units over the certified subjects of the base certificate — a `subject.collection/1` subject contributing exactly its `declared_cardinality`, any other subject exactly `1` (`capacity.commitment/1 §13.1`, §13.1.1). The toolkit MUST fail closed under `EFFECTIVE_UNITS_BINDING_VALID` when the declared units understate the certified subjects; where a collection's `declared_cardinality` is not resolvable offline, it MUST at minimum enforce the lower bound implied by the certified-subject count.
11. canonical coherence of all proof fields

The toolkit MUST reject any proof path in which settlement-bound capacity could be reconstructed, approximated, or inferred from outside the exact certified settlement context required by the proof and applicable public rules.

---

## 13. Anti-splicing requirements

The toolkit MUST reject any context in which:

- `base_certificate` and `independence_proof` are individually valid but do not belong to the same exact context
- supporting artifacts resolve to another leaf, another settlement, another rules domain, or another system domain
- an aggregated settlement yields more than one plausible interpretation
- a receipt, inclusion path, root value, or bookkeeping artifact is reusable across multiple plausible assignments

The toolkit MUST also reject any proof context whose claimed independence semantics belong to a clone, fork, or merely similar external system rather than to the exact CERTCRYPT System Domain required by the proof.

The toolkit MUST treat mixed-package substitution as a required negative case, not as an edge condition.

The toolkit MUST also reject any proof path that only appears CERTCRYPT-like because it combines anchoring, receipts, publication artifacts, or externally familiar settlement identifiers without satisfying the exact issuance binding, leaf binding, settlement binding, capacity-consumption binding, and system-attribution requirements of the active public rules.

---

## 14. Aggregated settlement requirements

The active settlement architecture for `/1` is aggregated only.

A conforming toolkit MUST therefore require material sufficient to fix one exact interpretation of:

- the settlement container
- membership
- ordering
- position or equivalent membership coordinates
- leaf assignment

If that unique interpretation cannot be established, the toolkit MUST reject the claimed `Independent` result.

No conforming toolkit MAY silently fall back to:

- another settlement profile
- a direct-settlement interpretation
- heuristic receipt-only validation
- live CERTCRYPT mediation

---

## 15. Original-material boundary

The toolkit MUST distinguish clearly between:

- structural verification of `Independent`
- complete verification against original material

A valid `Independent` result does not prove:

- truth of issuer declarations
- institutional endorsement
- material sustainability of declarations under complete verification

Original material MUST NOT be required by default merely to establish `Independent` under the system's own semantics.

However, when the selected verification path requires original-material comparison, the toolkit MUST request or accept that material independently rather than pretending that package sufficiency already proved it.

---

## 16. Non-goals

The minimum conforming toolkit MUST NOT:

- emit certificates
- fix leaves
- execute settlement
- require live token supply state, live burn inspection, or live balance checks for the standard offline path when canonical offline proof material suffices
- act as an authoritative resolver
- treat the proof signature, or a node attestation, as the source of independence
- present preview, demo, exploratory, compatibility, or partial modes as conforming verification

---

## 17. Minimum conformance suite

A conforming toolkit MUST be accompanied by a public conformance suite including at least:

- positive fixtures, on both routes: `ISSUED_VALID` and `INDEPENDENT_VALID`
- negative fixtures, on both routes: `ISSUED_INVALID` and `INDEPENDENT_INVALID`
- fixtures that supply a `verification_package`, valid and invalid (a member outside the closed set, a missing required member, a declaration contradicting the artifacts)
- target-selection cases (§11.4)
- original-material delivery cases (§8.5): mismatch, a subject index the certificate does not declare, a cardinality that differs
- aggregated-settlement cases
- collection subject cases
- unsupported collection commitment scheme cases
- unsupported leaf profile cases
- opaque subject overread rejection cases
- collection-level vs element-level distinction cases
- mixed-package substitution cases
- system-domain spoofing cases
- insufficient-finality cases
- parser-downgrade cases
- invalid issuance-time participation cases
- clone / fork proof-context rejection cases
- settlement-bound capacity reconstruction rejection cases

The suite MUST be sufficient to expose:

- omitted required checks
- heuristic compatibility behavior
- partial verification falsely reported as success

Each fixture fixes, as its expected result, the `result_code`, the resolved `verification_target` and the exact set of `failed_check_ids` (§9.5–§9.7), and MAY fix further members of §9.6. An implementation passes a fixture only when all of them are equal — no missing failed check and no additional one. The suite fixes the request of every fixture, including whether it supplies a package; it fixes no implementation-specific mode, and no fixture passes under a mode that relaxes verification (§7.1).

The public suite for this specification is the CERTCRYPT Conformance Suite ([certcrypt-conformance](https://github.com/CERTCRYPT/certcrypt-conformance)), which also publishes the JSON Schemas of the request, the result, the `base_certificate`, the settlement material and the `verification_package`.

---

## 18. Conformance claim

An implementation MAY claim minimum conformance with `verifier-toolkit/1` if and only if:

- it implements 100% of the mandatory standard offline verification baseline
- it fails closed
- it uses no semantic compatibility heuristics for the normative path
- it never returns `INDEPENDENT_VALID` with omitted checks
- it passes every fixture of the public conformance suite, at a stated version of that suite, with exact equality (§17)
- it produces result outputs with the members, codes and check identifiers of §9.5–§9.7

A claim names the suite version it was tested against. Convergence between implementations is a consequence of each one passing the suite, not a separate claim.

---

## 19. Summary

`verifier-toolkit/1` defines the minimum fail-closed reference verifier behavior required to evaluate `Issued` and `Independent` under CERTCRYPT public rules without semantic inflation, live-authority dependence, or downgraded verifier shortcuts.

---

## 20. Versioning & extensibility

This `/1` specification defines the current active public contract for `verifier-toolkit/1`.

Once frozen, this version MUST NOT be modified in place in any way, including editorial, typographic or clarifying changes that would leave its normative meaning unchanged. Any change MUST be published under a new version identifier.

---

## 21. References

- CERTCRYPT Specifications
    - [security-model/1 — CERTCRYPT Security Model](../../../../foundation/security-model/1/index.md)
    - [system-domain/1 — CERTCRYPT System Domain](../../../../foundation/system-domain/1/index.md)
    - [system-foundation/1 — CERTCRYPT System Foundation](../../../../foundation/system-foundation/1/index.md)
    - [system-manifest/1 — CERTCRYPT System Manifest](../../../../foundation/system-manifest/1/index.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../../../foundation/rules-domain/1/index.md)
    - [composite-signature/1 — CERTCRYPT Composite Signature](../../../../foundation/composite-signature/1/index.md)
    - [independence.proof/1 — CERTCRYPT Independence Proof](../../../../models/independence.proof/1/index.md)
    - [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../../../protocols/CCCP/1/index.md)
    - [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../../../protocols/CCSP/1/index.md)
    - [CCVP/1 — CERTCRYPT Consistency Verification Protocol](../../../../protocols/CCVP/1/index.md) (the optional consistency plane only)
    - [subject.binary/1 — CERTCRYPT Binary Subject Canonicalization Profile](../../../../profiles/subject.binary/1/index.md)
    - [subject.email/1 — CERTCRYPT Email Subject Canonicalization Profile](../../../../profiles/subject.email/1/index.md)
    - [subject.collection/1 — CERTCRYPT Collection Subject Canonicalization Profile](../../../../profiles/subject.collection/1/index.md)
    - [subject.ai-decision/1 — CERTCRYPT AI-Decision Subject Canonicalization Profile](../../../../profiles/subject.ai-decision/1/index.md)
    - [subject.context-snapshot/1 — CERTCRYPT Context Snapshot Subject Canonicalization Profile](../../../../profiles/subject.context-snapshot/1/index.md)
    - [subject.text/1 — CERTCRYPT Plain Text Subject Canonicalization Profile](../../../../profiles/subject.text/1/index.md)
    - [collection.merkle-sha3-256/1 — CERTCRYPT Merkle Collection Commitment Scheme](../../../../protocols/commitment/collection.merkle-sha3-256/1/index.md)
    - [capacity.commitment/1 — CERTCRYPT Capacity Commitment](../../../settlement/capacity.commitment/1/index.md)
    - [capacity.evidence/1 — CERTCRYPT Capacity Evidence](../../../settlement/capacity.evidence/1/index.md)
    - [settlement.binding/1 — CERTCRYPT Aggregated Settlement Binding](../../../settlement/settlement.binding/1/index.md)
    - [settlement-material/1 — CERTCRYPT Settlement Material](../../../settlement/settlement-material/1/index.md)
    - [settlement.aggregated.xrpl/1 — CERTCRYPT Aggregated XRPL Settlement Profile](../../../settlement/settlement.aggregated.xrpl/1/index.md)
    - [verification-package/1 — CERTCRYPT Verification Package](../../verification-package/1/index.md)
- **Conformance**
    - [certcrypt-conformance — CERTCRYPT Conformance Suite](https://github.com/CERTCRYPT/certcrypt-conformance)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
    - [RFC 8259 — The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259)

---

**End of verifier-toolkit/1**
