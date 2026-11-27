# CERTCRYPT Operator Recognition Credential Specification (operator.recognition/1)

**Identifier:** `operator.recognition/1`

**Label:** CERTCRYPT Operator Recognition Credential Specification (operator.recognition/1)

**Type:** Ecosystem Specification

**Status:** Frozen

**Layer:** Layer 3 — Ecosystem

**Depends on:** `system-domain/1`, `rules-domain/1`, `CCCP/1`, `submission-set/1`

**Naming convention:**
`operator.recognition/1` is the formal identifier.
CERTCRYPT Operator Recognition Credential Specification (operator.recognition/1) is the human-readable label.

**Audience:** Node operators, implementers of a fixation service, auditors.

**Purpose:** Define the credential a node presents to the fixation service to show that its operator key is recognised under the CERTCRYPT System Domain, how the operator identifier derives from that key, how the fixation service checks the credential together with a proof of possession of the key, and how messages signed by the operator key are kept apart.

**Intended use:** The fixation service checks the credential when a node submits a submission set (`submission-set/1` §9.4) or registers an `operator.domain-binding/1` statement. An issuer does not check it: for the issuer the node is a transport, and what the issuer and any verifier learn about the node is the `node_attestation` of the proof (`independence.proof/1` §10.15), authentic through the proof signature.

**Scope:** Defines the operator key and identifier, the credential object, its identifier and signature, its validity window, the checks the fixation service performs, and the domain separation of operator-key signatures. How the fixation service decides to recognise an operator, and how it stops admitting one, is internal to it (`submission-set/1` §9.4) and out of scope.

**Non-goals:** This specification does not define a registry or list of operators, does not participate in the verification of an `independence.proof/1`, and does not rate, rank, endorse or certify any operator.

> This document is **normative**.
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale

A node transports an issuer's submission sets to the fixation service. The fixation service admits submissions only from nodes whose operator key it recognised: when a node submits, it presents its credential and proves, with the same submission, that it holds the operator key (`submission-set/1` §9.4).

No other party relies on the credential, and no party trusts the node:

- **the issuer** treats the node as a transport. It hands its submission sets to the node and need not believe anything the node says: what an issuance yields is an `independence.proof/1` signed by the CERTCRYPT System Domain, which any verifier checks offline. A node that is not recognised gets nothing admitted; a node that misbehaves can delay or drop a submission, never forge or alter what is signed;
- **the verifier** of an `independence.proof/1` learns which node carried the submission from the `node_attestation` the proof may carry, signed by the system domain, naming the operator identifier the fixation service recognised (`independence.proof/1` §10.15). That attestation is authentic through the proof signature; a verifier consults no credential, registry or service to validate it, and its presence or absence does not condition `Independent` (§11).

Recognition is structural: a cryptographic identity and a validity window. It says nothing about the quality, volume, commercial terms or trustworthiness of an operator (§12).

---

## 2. Conformance

A conforming node MUST present credentials and possession proofs exactly as defined here.
A conforming fixation service MUST perform every check of §9 and MUST fail closed when any check fails.

---

## 3. Operator key and operator identifier

### 3.1 Operator key

The operator key is an ML-DSA-65 key pair (FIPS 204). Its algorithm identifier is `ml-dsa-65-fips204-v1`. The public key is carried in standard base64 (RFC 4648 §4, with padding) of its 1952-byte encoding.

The operator key is the identity of the operator. Every instance of a node that acts as the same operator uses the same key; independent installations generate independent keys.

### 3.2 Operator identifier

The operator identifier is derived from the public key and from nothing else:

```text
operator_id = "op:" || STANDARD_NO_PAD( SHA3-256( operator_public_key_bytes )[0..16] )
```

where `operator_public_key_bytes` is the decoded 1952-byte public key, `[0..16]` takes the first 16 bytes of the digest, and `STANDARD_NO_PAD` is the RFC 4648 §4 base64 alphabet without padding. The result is `op:` followed by exactly 22 characters of `A`–`Z`, `a`–`z`, `0`–`9`, `+`, `/`: the same form as `node_attestation.node_id` (`independence.proof/1` §10.15).

Every implementation MUST derive the identifier exactly this way. Anyone holding the public key can recompute it; no registry is needed to relate the two.

### 3.3 Key change

Because the identifier is derived from the key, a new operator key is a new operator identifier. There is no identifier that survives a change of key. An operator that replaces its key obtains a credential for the new identifier; the previous identifier ends when its credential expires or when the fixation service stops admitting it. Artifacts produced under the previous identifier keep their meaning.

---

## 4. The credential object

The credential is a JSON object with exactly the following members:

| Member | Type | Content |
|---|---|---|
| `artifact_type` | string | `"operator.recognition/1"` |
| `system_id` | string | `"certcrypt"` |
| `rules_version` | string | The rules domain instance under which the credential was issued (`rules-domain/1`), for example `"rules/2026-01"` |
| `system_root_fingerprint` | string | The system root fingerprint of the CERTCRYPT System Domain (`system-domain/1`), lowercase hex |
| `recognition_id` | string | The credential identifier (§5), lowercase hex |
| `operator_id` | string | The operator identifier (§3.2) |
| `operator_public_key` | string | The operator public key (§3.1) |
| `operator_key_alg` | string | `"ml-dsa-65-fips204-v1"` |
| `valid_from` | string | Start of the validity window (§7), RFC 3339 UTC with whole seconds (`YYYY-MM-DDTHH:MM:SSZ`) |
| `valid_until` | string | End of the validity window (§7), same format |
| `recognition_issuer` | object | `{ "kid": string, "manifest_sequence": integer }` (§6.2) |
| `signature` | object | `{ "signature_alg": "ml-dsa-65-fips204-v1", "signature_b64": string }` (§6) |

No other member MAY appear, at any depth. The fixation service MUST reject a credential with a missing member, an additional member, a duplicate member name, or a member of the wrong type.

`manifest_sequence` is a positive integer the issuing service records next to `kid`. It carries no verification meaning in `/1`, and the fixation service MUST NOT use it to locate the signing key.

---

## 5. Credential identifier

`recognition_id` is the lowercase hex SHA3-256 digest of the RFC 8785 (JCS) canonical form of the credential object **without** `recognition_id` and **without** `signature`:

```text
recognition_id = hex( SHA3-256( JCS( credential − {recognition_id, signature} ) ) )
```

The fixation service MUST recompute `recognition_id` and MUST reject a credential whose carried value differs. Two credentials differing in any member, the validity window included, have different identifiers: renewing a credential produces a new `recognition_id`.

---

## 6. Signature

### 6.1 Signing bytes and algorithm

The signing bytes are the RFC 8785 (JCS) canonical form of the credential object **without** `signature` (and with `recognition_id` present). The signature is a single ML-DSA-65 signature (FIPS 204) over those bytes, carried in `signature.signature_b64` as standard base64. `signature.signature_alg` MUST be `ml-dsa-65-fips204-v1`.

The signature is made by the **recognition sub-key**: a key of the CERTCRYPT System Domain dedicated to signing operator credentials. It MUST NOT be the key that signs independence proofs or capacity holder authorizations, and it MUST NOT sign anything other than `operator.recognition/1` credentials. Because that key signs a single kind of object, the signing bytes carry no domain prefix.

### 6.2 Resolving the recognition sub-key

The credential names its signer only by `recognition_issuer.kid`; it does not carry the sub-key's public key. The fixation service verifies the credential against its own recognition sub-key for that `kid` and MUST NOT accept a public key offered by the node. A change of sub-key always comes with a new `kid`: a credential whose `kid` names a sub-key the service holds but that does not verify under it MUST be rejected.

Which sub-keys the fixation service accepts, and how it rotates them, is internal to it: no other party pins or resolves the recognition sub-key.

---

## 7. Validity window

The credential is valid at instant `t` when `valid_from ≤ t < valid_until`. `valid_from` MUST be strictly earlier than `valid_until`. The issuing service chooses the length of the window; it MUST be finite.

There is no revocation of the credential itself in `/1`: it is not checked against a status endpoint, list or registry, and it keeps verifying until `valid_until`.

The fixation service can stop admitting submissions from an operator before that instant, for example when the integration under which the operator transports is deactivated. That decision is internal to the fixation service (`submission-set/1` §9.4) and does not change the credential.

---

## 8. Proof of possession

A credential alone proves nothing about who presents it: it is public material and can be copied. The node proves that it holds the operator key in the same request that presents the credential, by signing, with that key, the message the operation defines: the submission possession message (`submission-set/1` §9.4), or the statement itself for an `operator.domain-binding/1` registration. The fixation service verifies that signature under the credential's `operator_public_key`.

---

## 9. Checks by the fixation service

Given a node's credential and the request that presents it, the fixation service MUST, fail-closed:

1. Check the credential object against §4 (members, types, fixed values).
2. Check that `system_root_fingerprint` is the fingerprint of the CERTCRYPT System Domain it serves.
3. Check that `rules_version` is a rules domain instance it accepts.
4. Decode `operator_public_key`, recompute `operator_id` (§3.2), and check that it equals the credential's `operator_id` and the operator the request names.
5. Recompute `recognition_id` (§5) and check it.
6. Resolve the recognition sub-key (§6.2) and verify `signature` over the signing bytes (§6.1).
7. Check that the instant of the request lies in the validity window (§7).
8. Verify the proof of possession of the request (§8) under `operator_public_key`.

It MUST NOT admit a submission or register a statement from a node that fails any check, and MUST NOT use allowlists, branding or reputation signals in place of these checks.

---

## 10. Domain separation of operator-key signatures

The operator key signs messages in several contexts. Every message it signs MUST be distinct from every message of every other context, so that a signature obtained in one context is never valid in another. In particular, a node MUST NOT sign bytes chosen by a third party without a context prefix.

The contexts defined by the public specifications are:

| Context | Signed message | Defined in |
|---|---|---|
| Submission possession | `<request_id> "." <submission_set_id>`, where `request_id` is a ULID | `submission-set/1` §9.4 |
| Domain binding | `"certcrypt:operator-domain-binding:1\|" \|\| signed_payload_jcs` | `operator.domain-binding/1` §6 |

The submission possession message carries no textual prefix; it is kept apart because a ULID never contains `:` and never starts with `{`. Any other context in which a deployment asks the operator key to sign MUST use its own prefix of the form `certcrypt:<context>:<version>|`, or sign a JCS object (whose bytes start with `{`), and MUST NOT reuse a prefix listed here.

---

## 11. Relationship with verification

- A verifier of `independence.proof/1` MUST NOT consult this credential or any list of credentials. `node_attestation`, when present, is authentic through the proof signature (`independence.proof/1` §10.15).
- The presence, absence, expiry or later withdrawal of a credential MUST NOT change the result of verifying a proof already produced.
- *Issuance-time participation* (`independence.proof/1` §12.10) is the cryptographic binding of a certificate into the independence flow at issuance. It is unrelated to operator recognition.

---

## 12. Claims boundary

Recognition is an identity recognised under CERTCRYPT rules. It MUST NOT be presented as approval, certification, validation or endorsement of an operator, of its infrastructure, or of the issuers whose submissions it carries.

The credential carries no tier, category, score, volume, quality metric, price, brand or ranking, and no implementation MAY add one. Any association of an operator with an organisation or a host name lives outside this credential (`operator.domain-binding/1`).

---

## 13. Non-goals

This specification does **not** define:

- how the fixation service decides to recognise an operator, or to stop admitting one
- a registry, directory or list of operators
- revocation lists, status endpoints or other live checks
- how a node protects its operator key
- any reputational, commercial or quality signal about operators

---

## 14. Versioning

- **Specification identifier:** `operator.recognition`
- **Specification version:** `/1`

Any change to the member set of the credential, to the derivation of `operator_id` or `recognition_id`, to the signing bytes or algorithms, or to the domain-separation rule requires a new major version once this specification is frozen.

---

## 15. Wire format

A credential, with abbreviated values:

```json
{
  "artifact_type": "operator.recognition/1",
  "system_id": "certcrypt",
  "rules_version": "rules/2026-01",
  "system_root_fingerprint": "24a0ed1b…",
  "recognition_id": "5f3c…",
  "operator_id": "op:<22 characters>",
  "operator_public_key": "<standard base64 of 1952 bytes>",
  "operator_key_alg": "ml-dsa-65-fips204-v1",
  "valid_from": "2026-11-18T10:00:00Z",
  "valid_until": "2027-11-18T10:00:00Z",
  "recognition_issuer": { "kid": "<recognition sub-key kid>", "manifest_sequence": 1 },
  "signature": { "signature_alg": "ml-dsa-65-fips204-v1", "signature_b64": "<standard base64>" }
}
```

---

## 16. References

- [system-domain/1 — CERTCRYPT System Domain](../../../../foundation/system-domain/1/index.md)
- [rules-domain/1 — CERTCRYPT Rules Domain](../../../../foundation/rules-domain/1/index.md)
- [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../../../protocols/CCCP/1/index.md)
- [submission-set/1](../../../../protocols/settlement/submission-set/1/index.md)
- [independence.proof/1](../../../../models/independence.proof/1/index.md)
- [operator.domain-binding/1](../../operator.domain-binding/1/index.md)
- [RFC 8785 — JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785)
- [FIPS 204 — Module-Lattice-Based Digital Signature Standard](https://csrc.nist.gov/pubs/fips/204/final)
