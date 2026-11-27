# CERTCRYPT Composite Signature Profile (composite-signature/1)

**Identifier:** `composite-signature/1`

**Label:** CERTCRYPT Composite Signature Profile (composite-signature/1)

**Type:** Foundation Specification

**Status:** Frozen

**Layer:** Layer 0 — Foundation

**Depends on:** See References *(active normative dependencies are listed below)*

**Naming convention:**
`composite-signature/1` is the formal identifier.
CERTCRYPT Composite Signature Profile (composite-signature/1) is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.

**Audience:** Protocol designers, specification authors, implementers, verifiers, auditors

**Purpose:** Define the normative semantics, message derivation, ordering, and verification rules of the composite signature used by the CERTCRYPT permanent trust chain, so that conforming implementations in any language produce and verify byte-interoperable composite signatures.

**Intended use:** composite-signature/1 is intended to be the authoritative public specification used by conforming implementers, verifiers, auditors, and ecosystem tooling when producing or verifying any composite signature in the CERTCRYPT architecture.

**Scope:** Defines the derived message `M'`, the ordered component layout, the AND verification rule with its fail-closed condition, the anti-stripping and anti–cross-profile bindings, the registered profiles, and the component encodings. The artifacts that CARRY composite signatures (emission certificate, system-foundation root, `independence_proof`, the capacity Level-1 authorization binding) define their own object layout and signing targets in their own specifications and reference this one.

**Non-goals:** composite-signature/1 does not define key management, key rotation, the system manifest, or any artifact layout. It does not prove truth, semantic validity, or service authority by itself, and MUST NOT be interpreted as a substitute for Proof of Independence.

> This document is **normative**.
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale

The CERTCRYPT permanent trust chain — the emission certificate, the system-foundation root, the `independence_proof`, and the system-domain Level-1 authorization binding — must remain non-forgeable for the lifetime of the artifacts it anchors, which is indefinite. A signature over those artifacts therefore faces two independent failure modes:

- **A future cryptographically-relevant quantum computer.** A purely classical signature (e.g. ECDSA or Ed25519 alone) would become forgeable, allowing an adversary to fabricate emissions or proofs over old artifacts ("harvest-now, forge-later").
- **An as-yet-undiscovered classical/cryptanalytic break of the post-quantum scheme.** A purely post-quantum signature (e.g. ML-DSA-65 alone) offers no fallback if the lattice scheme — comparatively young — is later weakened by a classical attack.

A **composite** signature closes both: every component signs the SAME derived message, and the composite is valid only if ALL components verify (AND). The post-quantum component provides the quantum floor; the classical component provides a hedge against a post-quantum break. Neither component alone is ever a verdict.

The derived message `M'` defined here is a profile-specific construction. The profiles and identifiers of this version are fixed (§7). Adopting different component identifiers requires registering a new profile identifier or publishing a successor version of this specification; it never changes the meaning of an identifier registered here.

---

## 2. Scope

A composite signature under this profile is REQUIRED wherever a CERTCRYPT specification states that an artifact field is composite-signed. As of this version that includes the emission certificate signature, the system-foundation root statement signature, the `IndependenceProofV1` signature, and the capacity Level-1 authorization binding signature.

This profile does NOT apply to ephemeral, single-use signatures. In particular, the holder operation-key (Level-3) signature over a projected capacity commitment is a non-reused per-operation leaf signature and is **ML-DSA-65 (pure)**, NOT composite; its own specification states so explicitly.

---

## 3. Terminology

The keywords MUST, MUST NOT, SHOULD, and MAY are to be interpreted as described in RFC 8174.

- **Component signature** — one named signature (e.g. an ECDSA P-256 signature, or an ML-DSA-65 signature) over the derived message `M'`.
- **Composite signature** — the ordered set of component signatures that together form a single, inseparable cryptographic assertion under a registered profile, verified with AND semantics.
- **Profile** — a registered composite algorithm identifier (`composite_alg_id`) fixing the exact set and order of components (§7).
- **`M'`** — the domain-separated derived message every component signs (§4).
- **Classical component** — the non-post-quantum component (ECDSA P-256 in the canonical profile).
- **PQC component** — the post-quantum component (ML-DSA-65).

---

## 4. The derived message `M'`

Every component of a composite signature MUST sign the exact same byte string `M'`:

```
M' = ASCII(domain_prefix) || 0x00 || ASCII(composite_alg_id) || 0x00 || ASCII(payload_canon_digest_hex)
```

where:

- `domain_prefix` is the fixed ASCII string **`CERTCRYPT-Composite-Signature-v1`**.
- `composite_alg_id` is the registered profile identifier (§7) under which the signature is produced.
- `payload_canon_digest_hex` is the lowercase hexadecimal SHA3-256 digest of the carrying artifact's canonical signing target, as defined by that artifact's own specification.
- `0x00` is a single zero byte used as a field separator.

Rules:

- Implementations MUST construct `M'` with the two `0x00` separators between the three fields, in this exact order.
- The three fields are ASCII text and MUST NOT contain a `0x00` byte, so the separation is unambiguous (the split into three fields is injective). A conforming verifier therefore cannot be induced to accept a different `(domain_prefix, composite_alg_id, digest)` triple as the same `M'`.
- Components MUST NOT sign anything other than `M'` (no component-private salt, context, or wrapper).

### 4.1 Binding the profile into `M'` (anti–cross-profile)

`composite_alg_id` is bound **inside** `M'`. This makes the profile part of the cryptographic identity of the signed message, which is a load-bearing security property:

- A composite signature produced under one profile MUST NOT verify under any other profile (the `M'` differs).
- An adversary MUST NOT be able to "downgrade" a signature to a weaker profile, reinterpret it under a different component set, or rename the composite algorithm, without invalidating every component signature.

A verifier MUST compute `M'` using the SAME `composite_alg_id` it requires for the context, and MUST reject a signature whose declared profile does not match (§6).

---

## 5. Component message handling

Each component signs `M'` under its own algorithm's standard message handling:

- **ML-DSA-65 (FIPS 204):** the component signs `M'` directly (pure ML-DSA-65, empty context). It MUST NOT apply a pre-hash.
- **ECDSA P-256 (secp256r1):** the component signs `SHA3-256(M')`. CERTCRYPT uses **SHA3-256** as its stack-wide hash; ECDSA is hash-agnostic and reduces the 32-byte digest modulo the group order. Conforming implementations therefore hash `M'` with SHA3-256 (not SHA-2) before the ECDSA operation.
- **Ed25519 (additional profile only):** the component signs `M'` directly per RFC 8032.

---

## 6. Verification (AND, fail-closed, composite-only)

To verify a composite signature over a `payload_canon_digest_hex` under a required `composite_alg_id`, a conforming verifier MUST:

1. **Profile match.** Reject unless the signature's declared profile equals the required `composite_alg_id`, and its mode is `AND` (§8).
2. **Recompute `M'`** per §4 using the required `composite_alg_id`.
3. **Exact component layout.** Reject unless the signature object carries `alg`, `mode` and `signatures` and no member other than those and the ones its carrying artifact defines (§8); `signatures` holds exactly the components of the registered profile, no more and no fewer, in the profile's order (§7, §8); and each component carries exactly the members §8 lists for its algorithm, with the fixed values of §9. The classical component is the first element and the PQC component the second. A verifier MUST NOT search the array for a component, skip an unrecognized or duplicated one, or tolerate an additional member.
4. **PQC floor (fail-closed).** Reject unless the PQC (ML-DSA-65) component is present AND verifies. A composite that omits its PQC component, or whose PQC runtime is unavailable, MUST be rejected — never accepted on the classical component alone.
5. **Classical component.** Reject unless the classical component is present AND verifies under §5, with the public key in the one encoding the carrying artifact fixes for it (§9).
6. **AND result.** The composite is valid if and only if EVERY component in the profile verified over `M'`.

### 6.1 Composite-only

The composite signature is a single inseparable assertion. A conforming verifier MUST NOT treat the verification of any individual component as a trust verdict on its own. There is no "classical-only" or "PQC-only" acceptance path. Per-component verifiers MAY exist as low-level primitives (for tests, debugging, conformance vectors, fuzzing), but MUST NOT be exposed or used as a trust-verdict API.

### 6.2 Malformed vs failing

A component whose encoding is malformed (bad base64, wrong length, invalid point/encoding), a public key in an encoding other than the one fixed for its field, and a layout that step 3 rejects are STRUCTURAL defects and MUST be reported as such by the carrying artifact's verification (typically `REJECTED`), distinct from a well-formed component signature that does not verify.

---

## 7. Registered profiles and identifiers

A profile fixes the ordered component set. Components are listed **classical-first, PQC-second**. The order is load-bearing: it is the order of `signatures` on the wire (§8) and the order in which component public keys are concatenated by the composite key fingerprint (§10).

| `composite_alg_id` | Classical component | PQC component | Status |
|---|---|---|---|
| `certcrypt-composite-p256-mldsa65-v1` | `ECDSA-P256-SHA3-256` | `ML-DSA-65` | **Canonical** |
| `certcrypt-composite-ed25519-mldsa65-v1` | `Ed25519` | `ML-DSA-65` | Additional |

### 7.1 Identifier conventions

- The **profile** identifier (`composite_alg_id`) is a CERTCRYPT identifier and carries the suffix `-v1`. It is NOT a normative-specification version: the `/N` suffix is reserved for versioned specifications (e.g. `composite-signature/1`).
- The **component** algorithm identifiers are descriptive, industry-aligned names. `ECDSA-P256-SHA3-256` is a CERTCRYPT profile component identifier — it deliberately reflects the SHA3-256 hash domain and is NOT a standard JOSE/COSE name (the common `ES256` uses SHA-2). It is aligned with CERTCRYPT's hash domain, not with an IANA registry.

The canonical profile is `certcrypt-composite-p256-mldsa65-v1`; conforming producers SHOULD use it. The additional Ed25519 profile MAY be used where an environment cannot run ECDSA P-256, but MUST NOT be the default of a system-foundation root.

---

## 8. Wire representation

A composite signature is serialized as a JSON object with detached, named component signatures (NOT a single binary blob):

```json
{
  "alg": "certcrypt-composite-p256-mldsa65-v1",
  "mode": "AND",
  "signatures": [
    { "alg": "ECDSA-P256-SHA3-256", "encoding": "raw-rs-64", "low_s": true, "sig_b64": "…" },
    { "alg": "ML-DSA-65", "sig_b64": "…" }
  ]
}
```

- `alg` is the profile identifier (§7); `mode` MUST be `"AND"`.
- `signatures` is an ordered array, classical-first. The order is normative and load-bearing: a verifier MUST NOT reorder it, and MUST reject a composite signature whose component order does not match the registered profile.
- The ECDSA P-256 component carries exactly `alg`, `encoding`, `low_s` and `sig_b64`. The Ed25519 and ML-DSA-65 components carry exactly `alg` and `sig_b64`. `sig_b64` is base64, RFC 4648 standard alphabet, with padding; NOT url-safe.
- The composite object carries `alg`, `mode` and `signatures`. A carrying artifact MAY place these three members in an object of its own that also carries members it defines — the issuer `signer` of CCSP/1, the `signing_kid` of `independence.proof/1` — and then defines that object's closed member set; where it defines none, the object carries exactly these three. A component carries exactly the members listed above. Any other member, in the object or in a component, makes the signature malformed (§6.2).
- The representation is detached (named components), not an ASN.1/CMS blob.

> **Future serializations** MAY define equivalent binary encodings without changing the composite cryptographic semantics defined here. The current serialization uses detached component signatures.

---

## 9. Component encodings

### 9.1 ECDSA P-256

- Curve: P-256 / secp256r1.
- Signature encoding: **`raw-rs-64`** — the concatenation `r || s`, 64 bytes (32 + 32), big-endian. DER MUST NOT be used. The `encoding` field MUST be `"raw-rs-64"`.
- **Low-s is normative.** A producer MUST emit a low-s signature (`s ≤ n/2`). A verifier MUST reject a high-s signature; it MUST NOT normalize a high-s value to low-s and accept it. The `low_s` field MUST be `true`.
- Public key encoding: the carrying artifact MUST define **exactly one** canonical public-key encoding for each public-key field it carries; a verifier MUST NOT accept alternative equivalent encodings for that field. (Permitting multiple encodings for one field would open equivalence ambiguities across artifacts: the same key would have several byte forms, and every digest or fingerprint over it several values.) Every P-256 public-key field of the active corpus — the members and the Level-1 capacity key of `system-foundation/1` and `system-manifest/1`, the issuer key of CCSP/1, and the keys CCVP/1 fingerprints — uses the **SEC1 uncompressed** encoding: 65 bytes, the first byte `0x04`. A compressed point (33 bytes) or an SPKI DER structure in one of those fields is malformed (§6.2), even when it encodes the same key.

### 9.2 Ed25519

- Signature: 64 bytes (RFC 8032). Public key: the raw 32-byte encoding of RFC 8032. Under the canonical profile no field carries an Ed25519 key, so a 32-byte key presented where the canonical profile is required is malformed.

### 9.3 ML-DSA-65

- FIPS 204, the deterministic or hedged signature value as produced; the signing bytes are pinned (`M'`), the signature value is not. A verifier MUST verify against `M'` and MUST NOT pin or compare a fixed signature value.
- Signature and public key: raw FIPS-204 bytes, base64. The public key is the 1952-byte `pkEncode` output; the signature is 3309 bytes.

---

## 10. Composite key fingerprint

Where an artifact identifies one composite key by a fingerprint over its component public keys — for example an issuer key under [CCVP/1](../../../protocols/CCVP/1/specification.md) Section 8.1 — the fingerprint MUST be:

```
SHA3-256( classical_pub_bytes || mldsa_pub_bytes )
```

classical-first, matching the component order of §7. `classical_pub_bytes` and `mldsa_pub_bytes` are the **raw bytes** of each public key under the single canonical encoding the carrying artifact defines for that field (§9) — NOT the base64 strings, and NOT any alternative encoding. The order is load-bearing; implementations MUST NOT swap it, and MUST hash the decoded key bytes, not their textual representation.

This fingerprint identifies one key. It is **not** the `system_root_fingerprint` of a system domain: a system root is a quorum of composite keys, and its fingerprint is the digest of the whole manifest that lists them, `SHA3-256(UTF-8(JCS(system_manifest)))` ([`system-foundation/1`](../../system-foundation/1/specification.md) Section 8, [`system-manifest/1`](../../system-manifest/1/specification.md) Section 10). A verifier MUST NOT derive or compare a system root fingerprint with the construction of this section.

---

## 11. Conformance

A conforming implementation MUST:

- construct `M'` exactly as in §4, including the `0x00` separators and the bound `composite_alg_id`;
- apply §5 component message handling;
- verify with AND + the PQC fail-closed rule of §6, and expose only the composite verdict (§6.1);
- take the required profile from the context — the carrying artifact's specification or the governing rules domain — and never from the signature being verified (§4.1);
- reject any layout other than the exact one of §6 step 3 and §8: component count, order, and members;
- enforce the ECDSA `raw-rs-64` + low-s rules of §9.1, including the fixed `encoding` and `low_s` values;
- accept each public key only in the one encoding its field fixes (§9).

Cross-language byte-interoperability is established by the conformance vectors: a composite signature produced by one conforming implementation MUST verify under any other, because all agree on `M'` and on the per-component message handling. (Component signature VALUES are not required to be reproducible across languages — ML-DSA-65 may be hedged — but verification MUST succeed.)

---

## 12. References

- FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA).
- FIPS 186-5 / SEC1 — ECDSA over P-256 (secp256r1).
- RFC 8032 — Ed25519 (additional profile).
- RFC 8785 — JSON Canonicalization Scheme (where the carrying artifact's `payload_canon_digest_hex` is JCS-based).
- RFC 8174 — keyword interpretation.
- `system-foundation/1`, `system-manifest/1` — root material and fingerprint context.
- Artifacts that carry composite signatures define their own signing targets and reference this profile.
- [CCVP/1 — CERTCRYPT Consistency Verification Protocol](../../../protocols/CCVP/1/index.md)
- [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../../protocols/CCSP/1/index.md)
- [independence.proof/1 — CERTCRYPT Independence Proof Model](../../../models/independence.proof/1/index.md)

---

**End of composite-signature/1**
