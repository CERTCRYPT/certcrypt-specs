# CERTCRYPT AI-Decision Subject Canonicalization Profile (`subject.ai-decision/1`)

**Identifier:** `subject.ai-decision/1`

**Label:** CERTCRYPT AI-Decision Subject Canonicalization Profile v1

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
`subject.ai-decision/1` is the formal identifier.
CERTCRYPT AI-Decision Subject Canonicalization Profile v1 is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.

**Audience:** Protocol implementers, verifiers, auditors

**Purpose:** Define the normative subject-profile canonicalization semantics for `subject.ai-decision/1` within the active CERTCRYPT public architecture.

**Intended use:** `subject.ai-decision/1` is intended to be the authoritative public specification for deriving deterministic `canonical_bytes(subject)` for a record of one observable AI-model invocation and decision under CERTCRYPT public rules. The profile can supply tamper-evident technical evidence for record-keeping, traceability, human-oversight review and audit workflows, including workflows shaped by current AI-governance frameworks. It makes **no** claim of conformance with, or classification under, any such framework: it records circumstances observed and declared by the issuer, not the decision's or system's regulatory status. It does not replace the documentation, risk-management, oversight, retention, impact-assessment or data-protection processes that may apply in a particular jurisdiction. Nor is it the GDPR Art. 22 sense of "automated decision-making": the profile makes no claim about human involvement or legal effect on a person.

**Scope:** Defines the decision-record structure, canonicalization, and interpretation limits for `subject.ai-decision/1`; higher-layer proof, settlement, and evaluation semantics remain out of scope except where explicitly referenced.

**Non-goals:** `subject.ai-decision/1` does not prove that the decision is correct, fair, lawful, unbiased, reproducible, or that the model behaved as claimed, and MUST NOT be interpreted as a trust mark, a model-quality attestation, a notarization mechanism, or a live service authority.

> This document is **normative**.
> All requirements expressed using MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in RFC 8174.

---

## 1. Background & rationale

`subject.ai-decision/1` defines how an issuer-declared record of one AI decision is reduced to deterministic `canonical_bytes(subject)` under CERTCRYPT public rules. The declaration may identify an AI model or model-driven system, but the profile does not establish that the named system executed or caused the declared output.

It exists so that an issuer can commit to the exact, structured circumstances it observed for one model invocation and decision (which declared model, at which observation boundary, under which bound parameters and context, over which ordered inputs, producing which ordered outputs, by which actor, and at which declared instants) in a form any party can later verify against the held material, without CERTCRYPT retaining the input, output, or any model internals.

The profile defines canonicalization only.

It does not define:
- whether the decision was correct, fair, or lawful
- whether the model is accurate, safe, or unbiased
- whether the same inputs would reproduce the same output
- issuance, independence, settlement, or consistency semantics
- model identity, provider authentication, or hidden provider/runtime behavior

---

## 2. Scope

`subject.ai-decision/1` defines:
- the exact AI-decision record input boundary
- the required and optional structural fields of a valid decision record
- the canonicalization rule (RFC 8785 JCS, string-only)
- the syntax and bounds of identifiers, media types, part commitments, input/output profiles, timestamps and contextual maps a record carries
- forbidden transformations
- the boundary between profile-level verification and higher-layer evaluation

`subject.ai-decision/1` does not define:
- the semantics or schema of the decision input or output (carried only as salted commitments)
- model evaluation, scoring, benchmarking, or quality assertion
- reproducibility guarantees
- proof-of-existence, notarization, or timestamping semantics

Those concerns remain defined elsewhere, or outside the architecture entirely.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — BCP 14.

Additional terms:

- **Decision record:** The exact JSON object intended to be certified under this profile.
- **Material descriptor:** A closed object that identifies one ordered input or output part and carries its role, media type, subject profile, independently generated material nonce and CCCP/1 commitment. The material itself is NOT part of the record (zero-data).
- **Actor:** The opaque identifier of the party that operated the model and issued the decision.
- **Observation scope:** The boundary at which the issuer observed the invocation: `client` or `runtime`. It identifies a recording boundary, not the completeness of what was observable there.
- **JCS serialization:** UTF-8 bytes of the decision-record JSON value canonicalized under RFC 8785.

---

## 4. Design principles

- **Records the circumstances, not the judgment:** The profile binds *what was decided, by which model, under which parameters, over which committed input* — never an assertion that the decision is right.
- **Zero-data by design:** Inputs and outputs are carried only as descriptors and salted commitments; their content and model internals are never embedded. Certification stays compatible with a zero-data architecture.
- **Deterministic canonicalization:** The same valid decision record MUST always produce the same `canonical_bytes(subject)`.
- **String-only scalar values:** Every scalar value is a JSON string. Arrays exist only for ordered input and output material descriptors, so RFC 8785 number serialization never applies (§7.1) — the single hardest source of cross-language JCS divergence is removed by construction.
- **Interpretation boundaries:** This profile defines canonicalization only. It does not determine correctness, fairness, or independence.

---

## 5. Architectural role

`subject.ai-decision/1` is subordinate to the current architecture:

- `system-domain/1` determines which system is being evaluated
- `rules-domain/1` determines which exact public rules apply
- `security-model/1` defines the interpretation and fail-closed boundary
- `CCCP/1` defines canonicalization contexts, hashing, and commitment semantics
- `CCSP/1` defines certificate envelope structure

Under `/1`, this profile contributes only `canonical_bytes(subject)`.

It MUST NOT be interpreted as sufficient to establish `Issued`, `Independent`, settlement validity, consistency outcomes, or the truth/quality of the decision.

No implementation MAY present `subject.ai-decision/1` as a standalone proof, trust mark, model-quality attestation, or notarization mechanism.

---

## 6. Decision-record input boundary

For `subject.ai-decision/1`, the subject input MUST be one complete decision-record JSON object.

Implementations MUST derive `canonical_bytes(subject)` from that exact JSON value and MUST NOT reconstruct it from rendered summaries, logs, transport wrappers, external storage wrappers, derived indexes, resolver responses, or human-readable exports.

If the issuer or verifier does not possess the exact decision-record JSON value intended to be certified, this profile cannot be applied correctly and the relevant higher-layer operation MUST fail or be treated as incomplete.

### 6.1 The record is verbatim original material — how field identity is guaranteed

The whole decision record is the verifier-held original material for this subject, exactly as the `.eml` is for an email subject or the descriptor object is for a collection. The issuer commits its `subject_local_digest`; the holder presents the record; the verifier recomputes. There is no path by which a verifier obtains the individual fields (`model`, `parameters`, `decided_at`, `decision`, …) separately and reassembles them — it receives the one JSON value and canonicalizes it. "The fields are identical between issuer and verifier" is therefore not a goal to be achieved but a consequence of the verifier hashing the same value it was given.

Two consequences fix the only divergence vectors, by construction rather than by issuer discipline:

- **Format is irrelevant; JCS neutralizes it.** Because canonical bytes are the RFC 8785 (JCS) serialization of the *parsed value* (§8), any difference in key order, whitespace, indentation, or re-serialization between the issuer's storage and the verifier's copy produces the **same** canonical bytes. A record re-saved by a different JSON tool still verifies. No field needs a per-field canonicalization the way the out-of-record input/output material does.

- **Scalar values are opaque strings, compared byte-for-byte unless this profile defines syntax.** `parameters.temperature = "0.0"` is the four bytes `0.0` — not the number zero; `"0"`, `"0.0"`, and `"0.00"` are three distinct values. The profile interprets only the closed syntactic fields and the timestamp ordering that §7.3 expressly defines. It does not normalize other strings or infer semantic equivalence.

A divergence in a non-input/output field can therefore arise only if a party **regenerates** the record from parts instead of transmitting it verbatim — which §6 forbids. Transmit the record; do not rebuild it.

### 6.2 Part commitments and disclosure

Each material descriptor carries a fresh `material_nonce_hex` and the CCCP/1 commitment derived from that nonce and the part's subject-local digest. The record therefore reveals salted commitments and their nonces, not the raw subject-local digests. Provided the nonce-generation and non-reuse requirements of §7.3 are followed, the same material does not expose a stable cross-record fingerprint.

Disclosure still has limits. Once a party receives the record, it receives each part nonce and commitment and can test candidate material by canonicalizing it under the declared profile and recomputing the commitment. Low-entropy or otherwise guessable material remains vulnerable to candidate-dictionary testing after disclosure. A holder MUST therefore treat every material descriptor as belonging to the material it commits to and disclose or withhold it under the same access controls as that material. Salting prevents a stable fingerprint absent nonce reuse; it does not make disclosed commitments confidential or turn guessable content into high-entropy content.

---

## 7. Required structural fields

A valid `subject.ai-decision/1` record MUST contain exactly the following members (and the optional members of §7.2), and MUST NOT contain any other member.

### 7.1 Value discipline (string scalars; two ordered arrays)

Every scalar value in the record MUST be a JSON string. The only JSON arrays permitted anywhere are the top-level `input` and `output` arrays, whose elements are the closed material-descriptor objects of §7.2. The values of `model`, `parameters` and `context` are JSON objects as defined in §7.2; no other object or array shape is permitted. The record MUST NOT contain any JSON number, boolean, or null token at any depth. Any numeric-looking quantity an issuer chooses to bind MUST be carried as a string. A record containing any other array, a nested object not expressly permitted by §7.2, a JSON number, boolean, or null token is non-conformant and the profile does not apply (fail-closed).

With no JSON number tokens present, RFC 8785 reduces to deterministic object-key ordering, array-order preservation and string escaping. Input and output order is part of the record and MUST NOT be sorted or otherwise changed. This profile is stricter than `subject.context-snapshot/1` §7.1, which preserves booleans and nulls because its shape belongs to a higher-layer protocol.

### 7.2 Members

Required:

- `profile` — MUST be the string `subject.ai-decision/1`.
- `decision_id` — stable, issuer-declared identifier for this decision, satisfying the same canonical token syntax as a part `id` (§7.3). It is non-empty and opaque. It does not prove global uniqueness, external identity, or recognition by any provider or authority.
- `decided_at` — canonical UTC timestamp string of when the decision was issued, in the syntax of §7.3.
- `model` — object with required non-empty string members `id` (e.g. `"example-model-1"`) and `provider` (e.g. `"example-provider"`); OPTIONAL non-empty string member `version`. No other members. All three values are opaque issuer declarations: `provider` can name a public hosted provider, a private runtime, or a local operator, and none of the values is resolved or authenticated by this profile. An absent `version` means only that no version was bound.
- `observation_scope` — MUST be exactly `client` or `runtime`. `client` states that the issuer observed the invocation at the calling-client boundary. `runtime` states that it observed the invocation inside the model runtime or a directly controlled execution boundary. Neither value authenticates the provider or model, proves completeness, or exposes behavior hidden from that boundary.
- `input` — non-empty ordered array of material descriptors.
- `output` — non-empty ordered array of material descriptors.
- `decision` — a non-empty opaque outcome label string (e.g. `"approved"`, `"rejected"`, `"escalated"`). Its meaning is issuer-defined; this profile does not interpret it. Its byte length is bounded only by the whole-record limit of §8.

Each material descriptor in `input` and `output` MUST contain exactly these six string members and no others:

- `id` — part identifier satisfying §7.3 and globally unique across both arrays.
- `role` — non-empty opaque issuer-defined role. The profile binds but does not interpret it.
- `media_type` — lowercase MIME media-type essence without parameters, satisfying §7.3. It is declarative and MUST NOT select or override canonicalization; `profile` alone does that.
- `profile` — the subject-profile identifier under which that part is canonicalized, one of §7.4.
- `material_nonce_hex` — an independently generated, unpredictable 32-byte nonce represented as exactly 64 lowercase hexadecimal characters.
- `commitment_digest_hex` — the part commitment, represented as exactly 64 lowercase hexadecimal characters and computed under the declared `profile` exactly as:

  ```text
  subject_local_digest_hex = SHA3-256(canonical_bytes(material))
  commitment_digest_hex = SHA3-256(ASCII(material_nonce_hex) || ASCII(subject_local_digest_hex))
  ```

  Both operands are their 64-character lowercase hexadecimal representations concatenated as raw ASCII bytes, without decoding, separators, prefixes or framing. This is the CCCP/1 §8.1 commitment construction, with `material_nonce_hex` as the nonce for this part.

The combined number of descriptors in `input` and `output` MUST be between 1 and 256 inclusive. Independently, both arrays MUST be non-empty; the intersection of those requirements means that a conforming record contains between 2 and 256 descriptors.

Optional:

- `parameters` — an OPAQUE, issuer-defined object whose members are all JSON strings, recording whatever invocation parameters the issuer holds and chooses to bind. The base profile fixes **no** parameter names and presumes **no** model shape: a decision may come from an LLM (`temperature`, `top_p`, `top_k`, `seed`, …), a local runtime with a different parameter set, a classifier with none, a multi-stage pipeline, or an agent — and the issuer may not even have a given parameter at emission time. The base profile therefore neither requires nor interprets any specific parameter; it only requires that every member value is a string — never a nested object or array — and it canonicalizes them as-is. A parameter whose natural form is a list or a structure (a list of stop sequences, a set of tool definitions) is bound as one string the issuer chooses, such as its canonical JSON text. `parameters` MAY be absent (the issuer bound none); an empty object is distinct from absence and both are valid. Naming is issuer guidance (§13) and never makes a parameter required.
- `started_at` — canonical UTC timestamp string of when the observed invocation started, in the same syntax as `decided_at`. If present, it MUST denote an instant earlier than or equal to `decided_at` (§7.3).
- `context` — OPAQUE issuer-defined object with at most 128 members, each a string key mapped to a string value. It can bind technical references used by record-keeping, traceability, human-oversight or audit workflows, such as purpose, case, oversight or risk references. It defines no legal vocabulary and the profile does not interpret it. It SHOULD NOT contain personal data beyond opaque handles or references needed by the issuer's own controls. Absence and an empty object are distinct.
- `actor_id` — opaque string identifying the operating party. It SHOULD NOT carry personal data beyond an opaque handle or reference needed by the issuer's own controls. This is disclosure guidance: the profile does not inspect or semantically validate the string and conformance does not establish that it contains no personal data.
- `policy_ref` — opaque string referencing the decision policy under which the actor operated; declarative only, not interpreted by this profile.

`parameters`, when present, MUST contain at most 128 members. Every member value is a string; nested objects and arrays are prohibited. Absence and an empty object are distinct.

The input and output parts are canonicalized like CERTCRYPT subjects under their declared profiles, then bound through individual CCCP/1 commitments. The record binds only descriptors, per-part nonces and commitments; the materials and their raw subject-local digests are never embedded — the materials are verifier-held original material (verifier-toolkit/1 §8.5). A verifier recomputes `SHA3-256(canonical_bytes(material))` under each descriptor's profile and derives the commitment from the descriptor's `material_nonce_hex`. Neither hexadecimal field carries an algorithm prefix; the algorithm and construction are fixed by CCCP/1 (SHA3-256).

This descriptor set has collection-like properties: the record binds multiple ordered parts and their exact cardinality. It is nevertheless one non-collection `subject.ai-decision/1` subject representing one observable invocation and one decision, and therefore contributes one economic unit under rules that count a non-collection subject as one. It is NOT a `subject.collection/1` subject and defines no Merkle tree, root or element-inclusion proof. JCS over the complete record already binds the order and cardinality of every descriptor, while each nested part has no certificate-level nonce or independently certified collection envelope.

> **Why each descriptor's `profile` is required, not optional.** The issuer does not control how the verifier later obtains a part. Requiring a declared profile fixes how that material is interpreted — `subject.text/1` to reconcile its defined line-ending differences, `subject.binary/1` for byte-exact opaque material, `subject.email/1` for a message, or `subject.ai-decision/1` for a chained decision record. The declared `media_type` never changes that choice.

### 7.3 Syntax preconditions

The following are preconditions of canonicalization (§8), applied by issuers and verifiers alike. A record that fails any of them is non-conformant and the profile does not apply (fail-closed):

- `decision_id` and every descriptor `id` match `^[a-z][a-z0-9._-]{0,63}$`. Descriptor IDs are compared as exact strings and MUST be globally unique across `input` and `output`; `decision_id` is in a separate namespace and need not differ from a descriptor ID.
- Every descriptor `role` is a non-empty string.
- `decision`, `model.id` and `model.provider` are non-empty strings; `model.version`, when present, is a non-empty string.
- Every descriptor `material_nonce_hex` and `commitment_digest_hex` consists of exactly 64 characters from `0-9a-f`. Uppercase hexadecimal is refused, not compared.
- Every `material_nonce_hex` MUST be generated independently for its part from 32 unpredictable bytes using a CSPRNG. It MUST NOT be reused for another part or another record. Within one record, all `material_nonce_hex` values MUST be distinct; a duplicate across `input` and `output` makes the record non-conformant and MUST be rejected. A verifier can enforce within-record uniqueness but does not thereby establish that an issuer avoided reuse in records it has not received.
- Every descriptor `profile` is one of the profiles of §7.4.
- Every descriptor `media_type` is an RFC 6838 media-type essence consisting of one lowercase ASCII type token, `/`, and one lowercase ASCII subtype token. Parameters, whitespace and uppercase letters are prohibited; both tokens MUST satisfy the RFC 6838 token grammar.
- `decided_at` and `started_at`, when present, each use the canonical millisecond-precision UTC subset of [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339) fixed by this profile. Each value MUST match this grammar in full and with no surrounding whitespace:

  ```text
  YYYY-MM-DD "T" HH:MM:SS "." sss "Z"
  ```

  where every field is ASCII digits, `T` and `Z` are uppercase, the date is a real proleptic-Gregorian calendar date, the hour is `00`–`23`, the minute `00`–`59`, the second is `00`–`59`, and `sss` is exactly three decimal digits representing milliseconds. As a lexical regular expression over the whole string, followed by Gregorian date validation:

  ```text
  ^(?!0000)[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\.[0-9]{3}Z$
  ```

Years range from `0001` through `9999`. The calendar check MUST reject impossible dates, including `2026-02-29` and `2026-02-30`, and MUST apply the Gregorian leap-year rule. If `started_at` is present, its instant MUST be earlier than or equal to `decided_at`. Because both strings are canonical UTC values at millisecond precision, a chronological comparison and a lexicographic comparison over conforming strings produce the same order. The members `decision`, `actor_id`, `policy_ref`, `role`, the `model` members, and the `parameters` and `context` members carry no syntax beyond the rules above and being strings.

### 7.4 Input and output profiles

Every material descriptor's `profile` MUST be one of:

- `subject.text/1`
- `subject.binary/1`
- `subject.email/1`
- `subject.ai-decision/1` — the part is itself one complete decision record, allowing multi-model behavior to be represented by chaining records

`subject.collection/1` is excluded. Its leaf commitments and root use the anchor `nonce_hex` of the certificate that carries the collection; material nested inside a decision record has no certificate nonce of its own. The per-part `material_nonce_hex` defined here binds one material directly and does not create a collection envelope, Merkle root or inclusion-proof context. `subject.context-snapshot/1` is excluded because it is the snapshot subject of CCVP/1, not decision content.

One record describes one observable model invocation and one decision. A multi-model flow is represented by chaining complete `subject.ai-decision/1` records through material descriptors. If an issuer cannot observe a composed system's internal invocations, it records that system as one opaque declared model and MUST NOT invent internal stages or imply that `observation_scope` exposed them.

---

## 8. Canonicalization rule

Field-set conformance (§7, including the value discipline of §7.1, the exact member set of §7.2 and the syntax preconditions of §7.3 and §7.4) is a **precondition of canonicalization**, not a separable later check. `canonical_bytes(subject)` is defined ONLY for a record satisfying §7 in full; for any other object the profile does not apply and the implementation MUST fail closed.

For all subjects governed by `subject.ai-decision/1`:

- the input subject MUST be a valid JSON object satisfying §7
- the source bytes MUST be valid UTF-8 JSON and MUST NOT begin with a byte-order mark
- the source material MUST contain no more than 1,048,576 bytes; a larger source is non-conformant and the profile does not apply (fail-closed), even if parsing and JCS serialization would produce canonical bytes within the canonical-size limit
- the source material MUST be parsed as strict JSON: if any object in it, at any depth, contains the same member name twice — names compared after their escape sequences are decoded, so `"decision"` and `"d\u0065cision"` are the same name — the material is non-conformant and the profile does not apply (fail-closed). No first-wins, last-wins, or merge reading is permitted. Repeated elements of an array are ordinary data, not repeated members ([CCSP/1](../../../protocols/CCSP/1/specification.md) Section 8.1 applies the same rule to certificates)
- `canonical_bytes(subject)` MUST equal the UTF-8 bytes of the RFC 8785 JCS canonical serialization of that JSON value
- `canonical_bytes(subject)` MUST contain no more than 1,048,576 bytes; a larger record is non-conformant and the profile does not apply (fail-closed)
- implementations MUST canonicalize the parsed JSON value, not the original source bytes
- the object contains no JSON number tokens (§7.1), so RFC 8785 number serialization never applies under this profile

There are no alternative canonicalization modes under `/1`.

### 8.1 Conformance vector

The following record is normative; a conforming implementation MUST reproduce its part commitments, canonical bytes and record digest exactly.

The decision input is the text prompt `"Classify synthetic sample alpha."` and the output is the text `"label: category-a"`, each canonicalized under `subject.text/1`, which appends one trailing CRLF. The `parameters` and `context` shown are illustrative, opaque issuer declarations, not required names or legal fields. Every identifier, reference, material value, nonce and commitment in this vector is a synthetic public fixture; none denotes a real provider, model, person, case or decision. Record:

```json
{
  "profile": "subject.ai-decision/1",
  "decision_id": "synthetic-event-01",
  "decided_at": "2026-06-17T10:30:00.000Z",
  "started_at": "2026-06-17T10:29:58.000Z",
  "model": {
    "id": "synthetic-model",
    "provider": "synthetic-runtime",
    "version": "synthetic-model-v1"
  },
  "observation_scope": "client",
  "parameters": {
    "temperature": "0.0",
    "max_tokens": "4096",
    "top_p": "0.95"
  },
  "context": {
    "case_ref": "synthetic-case-01",
    "oversight_route": "synthetic-route-01"
  },
  "input": [
    {
      "id": "prompt",
      "role": "user",
      "media_type": "text/plain",
      "profile": "subject.text/1",
      "material_nonce_hex": "5f4775fbfb02640a026c6478ca4621c966d143c4de56d9a967d620f2e76ba623",
      "commitment_digest_hex": "7004872e8bd94944e730be517ce5f7fa15da9fdf4af0e7ff1d69083b6bfc61be"
    }
  ],
  "output": [
    {
      "id": "result",
      "role": "assistant",
      "media_type": "text/plain",
      "profile": "subject.text/1",
      "material_nonce_hex": "50b2f5bea4b03cca160d70476c1a57f6e63d3239eec7c4075e0758b343e3b066",
      "commitment_digest_hex": "c933ea2ce3977a2454fc8da3ae921fbc2cbe8eb018ab037d1497800f6712056d"
    }
  ],
  "decision": "category-a"
}
```

Canonical bytes (RFC 8785 JCS, UTF-8) — note this is a single line, key-sorted, no spaces; the pretty-printed record above produces exactly these bytes:

```text
{"context":{"case_ref":"synthetic-case-01","oversight_route":"synthetic-route-01"},"decided_at":"2026-06-17T10:30:00.000Z","decision":"category-a","decision_id":"synthetic-event-01","input":[{"commitment_digest_hex":"7004872e8bd94944e730be517ce5f7fa15da9fdf4af0e7ff1d69083b6bfc61be","id":"prompt","material_nonce_hex":"5f4775fbfb02640a026c6478ca4621c966d143c4de56d9a967d620f2e76ba623","media_type":"text/plain","profile":"subject.text/1","role":"user"}],"model":{"id":"synthetic-model","provider":"synthetic-runtime","version":"synthetic-model-v1"},"observation_scope":"client","output":[{"commitment_digest_hex":"c933ea2ce3977a2454fc8da3ae921fbc2cbe8eb018ab037d1497800f6712056d","id":"result","material_nonce_hex":"50b2f5bea4b03cca160d70476c1a57f6e63d3239eec7c4075e0758b343e3b066","media_type":"text/plain","profile":"subject.text/1","role":"assistant"}],"parameters":{"max_tokens":"4096","temperature":"0.0","top_p":"0.95"},"profile":"subject.ai-decision/1","started_at":"2026-06-17T10:29:58.000Z"}
```

- For the input part, `subject_local_digest_hex = d4a14c591baa5b13f81e9325fa8546bb72b1bb4b1478c420064ec4711cb26c8d`; its declared material nonce produces `commitment_digest_hex = 7004872e8bd94944e730be517ce5f7fa15da9fdf4af0e7ff1d69083b6bfc61be`.
- For the output part, `subject_local_digest_hex = c17b46ef5992e0664ce5a0b1b5cf4ecbe6164c3afddd218b5c64a2fd4472f360`; its distinct declared material nonce produces `commitment_digest_hex = c933ea2ce3977a2454fc8da3ae921fbc2cbe8eb018ab037d1497800f6712056d`.
- The decision-record `subject_local_digest_hex` = SHA3-256(canonical bytes) = `febd1f4e8530de217baaddc151573ee91c24722f85b5fb636b17b8d9c188aa2a`.
- Under certificate nonce `abababababababababababababababababababababababababababababababab`, the record's CCCP/1 commitment SHA3-256(ASCII(nonce_hex) || ASCII(subject_local_digest_hex)) = `6443f68707dfdec2194753c524507bdbda60b3576f106b0d86fbd59dd1ce5629`.

---

## 9. Forbidden transformations

Implementations applying `subject.ai-decision/1` MUST NOT:

- add or drop fields, or assign normative meaning to undefined fields
- coerce strings into numbers/booleans/nulls or vice versa
- sort or reorder arrays
- normalize timestamps beyond validating the single canonical UTC form of §7.3
- embed input or output material (only descriptors, per-part nonces and commitments appear)
- interpret `decision_id`, `decision`, `context`, `policy_ref`, `observation_scope`, or any parameter as a quality, correctness, provider-authentication, or compliance signal

---

## 10. Informational attributes

Any field permitted by §7.2 as optional is bound into `canonical_bytes` when present, but MUST NOT receive independent normative interpretation by this profile unless another applicable public specification explicitly defines that meaning. Profile conformance is determined from the record bytes and declared profile only.

---

## 11. Relationship to CCCP and CCSP

`subject.ai-decision/1` is a subject-specific profile under [CCCP/1](../../../protocols/CCCP/1/index.md). Its output constitutes `canonical_bytes(subject)` for CCCP-governed hashing and commitment construction; it MUST NOT redefine, weaken, or bypass any CCCP requirement. When referenced from certificates serialized under [CCSP/1](../../../protocols/CCSP/1/index.md), the declared subject `profile` IS a subject profile identifier only.

---

## 12. Verification boundary

Profile-level verification under `subject.ai-decision/1` establishes only that the held decision record matches the certificate's committed subject — i.e. that *this exact issuer-declared decision identifier, model descriptor, observation scope, ordered material descriptors, parameters, context, outcome label and timestamps* were committed. It does NOT establish global uniqueness of `decision_id`, provider or model identity, completeness of observation, execution causality, correctness, or reproducibility.

Verification against input and output material is defined by verifier-toolkit/1 §8.5.6. A verifier may deliver any declared part, keyed by its `id`, together with the record. Once the record has matched the certificate's commitment, the toolkit canonicalizes each delivered part under the `profile` its descriptor declares, computes `subject_local_digest_hex = SHA3-256(canonical_bytes(material))`, derives the CCCP/1 commitment using that descriptor's `material_nonce_hex`, and requires equality with its `commitment_digest_hex`. Delivering no parts is valid: comparisons not performed are never reported as passed. A match confirms only that the held material is the material the committed descriptor commits to; it says nothing about the decision's merit or whether the declared model produced one part from another.

---

## 13. Parameter names

The profile fixes no parameter names and publishes no per-model list of them. Which invocation parameters a model or runtime has, and what they are called, belongs to that model's interface, changes outside this specification, and is not something a CERTCRYPT specification can state on a provider's behalf.

For comparability across issuers of the same model, an issuer SHOULD bind each parameter under the name the model's own interface uses, spelled as that interface spells its value, and SHOULD keep one spelling for each value across its records (§6.1: `"0"` and `"0.0"` are different values). An issuer that does not hold a parameter at emission time omits it. None of this is checked: the canonicalization (§8), the member set (§7) and every boundary (§12, §14) are unchanged, a verifier needs only this profile, and an unknown key is an ordinary string member of `parameters`.

---

## 14. Anti-authority boundary

`subject.ai-decision/1` MUST NOT be described, implemented, or marketed as proof that an AI decision is correct, safe, fair, lawful, or authoritative, nor as a model audit, compliance certification, accreditation, provider attestation, or proof that a legal obligation was satisfied. It records structured technical evidence about one observed invocation and decision as deterministic bytes for cryptographic commitment. It can support record-keeping, traceability, human-oversight review and audit workflows, but does not replace required AI-system documentation, risk management, oversight measures, retention policies, fundamental-rights impact assessments, data-protection impact assessments, or any jurisdiction-specific procedure. All evaluation of the decision's merit and regulatory sufficiency remains external to this profile and to CERTCRYPT.

---

## 15. Versioning & extensibility

- **Profile identifier:** `subject.ai-decision`
- **Profile version:** `/1`

Any change that alters canonical byte output, the member set, the value discipline, or the permitted normalization behavior MUST require a new major version. No optional canonicalization behavior is permitted under `/1`.

---

## 16. References

- CERTCRYPT Specifications
    - [security-model/1](../../../foundation/security-model/1/index.md)
    - [system-domain/1](../../../foundation/system-domain/1/index.md)
    - [rules-domain/1](../../../foundation/rules-domain/1/index.md)
    - [CCCP/1](../../../protocols/CCCP/1/index.md)
    - [CCSP/1](../../../protocols/CCSP/1/index.md)
    - [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md)
    - [subject.text/1](../../subject.text/1/index.md)
    - [subject.binary/1](../../subject.binary/1/index.md)
    - [subject.email/1](../../subject.email/1/index.md)
    - [subject.collection/1](../../subject.collection/1/index.md)
    - [subject.context-snapshot/1](../../subject.context-snapshot/1/index.md)
    - [CCVP/1 — CERTCRYPT Consistency Verification Protocol](../../../protocols/CCVP/1/index.md)
- **External**
    - [RFC 3339 — Date and Time on the Internet: Timestamps](https://www.rfc-editor.org/rfc/rfc3339)
    - [RFC 8785 — JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785)
    - [RFC 6838 — Media Type Specifications and Registration Procedures](https://www.rfc-editor.org/rfc/rfc6838)
    - [RFC 8174 — BCP 14](https://www.rfc-editor.org/rfc/rfc8174)

---

**End of subject.ai-decision/1**
