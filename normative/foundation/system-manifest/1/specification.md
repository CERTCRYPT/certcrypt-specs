# CERTCRYPT System Manifest (system-manifest/1)

**Identifier:** `system-manifest/1`

**Label:** CERTCRYPT System Manifest Specification (system-manifest/1)

**Type:** Foundation Specification

**Status:** Frozen

**Layer:** Layer 0 — Foundation

**Depends on:** See References *(active normative dependencies are listed below)*

**Naming convention:**
`system-manifest/1` is the formal identifier.
CERTCRYPT System Manifest Specification (system-manifest/1) is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.

**Audience:** Protocol designers, specification authors, implementers, verifiers, auditors

**Purpose:** Define the normative semantics, constraints, and interpretation boundary of system-manifest/1 within the active CERTCRYPT public architecture.

**Intended use:** system-manifest/1 is intended to be the authoritative public specification used by conforming implementers, verifiers, auditors, and ecosystem tooling when handling this artifact or behavior.

**Scope:** Defines the active normative behavior of system-manifest/1; adjacent protocols, profiles, operational tooling, and product behavior remain out of scope except where explicitly referenced.

**Non-goals:** system-manifest/1 does not prove truth, semantic validity, legal validity, or live service authority by itself, and MUST NOT be interpreted as a substitute for cryptographic authenticity, Proof of Independence, or managed-service behavior outside its own normative scope.

> This document is **normative**.
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale

This specification defines the canonical CERTCRYPT system manifest.

The system manifest is the canonical artifact whose deterministic digest is the `system_root_fingerprint` referenced by `system-foundation/1`, `system-domain/1`, `independence.proof/1`, `verification-package/1`, and any other artifact that claims attribution to the CERTCRYPT System Domain.

Deriving `system_root_fingerprint` directly from a single public key would make root-key rotation indistinguishable from system-domain replacement: any rotation would invalidate every prior artifact bound to the old fingerprint, because verifiers would have no canonical mechanism to recognize the rotated key as belonging to the same system domain.

`system-manifest/1` resolves that problem by separating two concerns:

- the **identity** of the system domain, expressed as the digest of a manifest that catalogs its key material across time
- the **active entry** at any given moment — the key set whose quorum authorizes rotation — which is one entry inside that manifest

A manifest contains an append-only chain of entries, where each successor entry is authorized by a quorum of the immediately preceding entry. Adding an entry produces a new manifest version with a new digest, while every earlier entry remains cataloged.

The identity of the system domain is its **bootstrap fingerprint**: the digest of the bootstrap manifest version, which no rotation changes. Under `/1` every artifact attributed to the system domain carries the bootstrap fingerprint ([`system-domain/1`](../../system-domain/1/specification.md) Section 16.1), and no manifest entry signs operational artifacts (Section 15). A rotation therefore changes who may authorize the next rotation; it does not change what an artifact verifier accepts — unless equivocation evidence accumulates against the bootstrap entry under Section 12.5, which makes the system domain terminally invalid.

This specification defines:

- one exact manifest model with a closed schema
- one exact append-only key chain semantics
- one exact derivation of `system_root_fingerprint` from a manifest instance
- one exact rotation operation that binds each rotation to the predecessor manifest version and sequence
- one exact validation of any manifest version, and the part of it an artifact verifier performs under `/1` (Section 13)
- one exact equivocation-evidence and fail-closed model under which compromise of a predecessor entry produces detectable terminal invalidity rather than silent fork acceptance

It does **not** define:

- truth semantics
- independence semantics
- certificate validity by itself
- settlement execution
- the canonical bootstrap statement under which a manifest is published — that concern belongs to `system-foundation/1`
- the publication transport — that concern belongs to publication profiles such as `arweave.publication/1` (an optional publication profile, not part of the published corpus)
- the association between a system root identifier and any rules-domain version — that concern belongs to `system-foundation/1`, `system-domain/1`, and `rules-domain/1`
- provenance, discovery, or publication metadata about a manifest version — that concern belongs to publication and statement layers, not to the manifest itself

Those concerns belong to other specifications. The manifest under `/1` is deliberately reduced to identity-only material so that its digest is stable across rotations of provenance, publication, and rules associations.

---

## 2. Scope

This specification applies to all systems, implementations, verifiers, publishers, auditors, caches, mirrors, and package builders that:

- construct
- publish
- cache
- transport
- validate
- inspect
- extend
- reconcile

a CERTCRYPT system manifest claiming conformity with `system-manifest/1`.

Any implementation that uses a system manifest as the source of `system_root_fingerprint` for CERTCRYPT-domain attribution MUST conform to this specification.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

For the purposes of this specification:

- **system manifest** means the canonical CERTCRYPT artifact cataloged under this profile
- **manifest entry** means one exact public-key record inside a manifest
- **active entry** means the manifest entry whose half-open active interval includes the current time and whose `successor_kid` is `null`
- **half-open active interval** means the interval `[valid_from, valid_until)` for a rotated-out entry, or `[valid_from, +∞)` for an entry with `valid_until = null`
- **rotation** means the operation by which a new entry is appended to a manifest, authorized by a quorum of the previous active entry's members over a payload bound to the predecessor manifest version and sequence
- **quorum** means the `(k, n)` threshold of an entry: the `n` composite member keys authorized to sign on its behalf and the minimum `k` of them that MUST sign to authorize a rotation away from it
- **member** means one composite signing key (`member_kid` plus its two component public keys) listed in an entry's `members` array
- **successor quorum** means the `(quorum, members)` pair the predecessor authorizes for the successor entry, carried in the successor-binding payload and reproduced in the successor entry
- **manifest version** means a particular fully-formed manifest instance, identified by its `system_root_fingerprint` and `manifest_sequence`
- **manifest sequence** means the non-negative integer that counts rotations from the bootstrap manifest version, equal to the count of entries minus one
- **bootstrap fingerprint** means the `system_root_fingerprint` of the bootstrap manifest version: the identity of the system domain, invariant across rotations, and under `/1` the only `system_root_fingerprint` an artifact carries
- **equivocation** means the authorization by a predecessor entry's quorum of two or more distinct successor quorums over the same `(predecessor_manifest_fingerprint, predecessor_manifest_sequence)` pair — that is, two successor entries each carrying a valid quorum of predecessor signatures (Section 12.3) but differing in their successor quorum or other bound successor fields
- **equivocation evidence** means the set of conflicting successor entries observed by a conforming verifier that constitutes proof of equivocation under Section 12.5
- **terminal invalidity** means the fail-closed state of a manifest version, and any manifest version that descends from it, after equivocation evidence has been accumulated against it

---

## 4. Design principles

`system-manifest/1` is designed around the following principles:

- **Identity-only artifact:** The manifest under `/1` carries only the material required to identify the system domain and its key chain. Provenance, publication, and rules-domain associations are excluded by construction. This separation is what makes the digest stable: a change in provenance, publication, or rules associations MUST NOT change `system_root_fingerprint`.
- **Append-only history:** A conforming manifest MUST NOT remove or rewrite entries. Rotation extends the chain; it never replaces history.
- **Closed schema:** The manifest and its entries admit no unknown members under `/1`. The canonical digest depends on the entire object; permissive parsing would produce divergent fingerprints.
- **Deterministic digest:** `system_root_fingerprint` MUST be derived mechanically from the canonical serialization of the manifest, with no implementation freedom in canonicalization.
- **Self-anchored authorization:** Every successor entry MUST be authorized by a quorum of the immediate predecessor entry's members (Section 12.3), signing a payload that binds the exact predecessor manifest version and sequence. The chain is its own authority; no external trust source is required.
- **Rotation without re-attribution:** A rotation changes who may authorize the next rotation. It does not change the fingerprint artifacts carry or the key that verifies them (Sections 14 and 15), so no artifact verifier has to follow the chain to keep verifying.
- **Identity stability:** The system domain remains the same across rotations. The `system_id` field and the bootstrap fingerprint are invariant. The digest of the current manifest version changes with each rotation; artifacts never carry it under `/1`.
- **Equivocation-evidence model:** A predecessor key compromise cannot be prevented by `/1` alone. The model converts compromise into detectable evidence: any verifier that observes two conflicting successor signatures over the same predecessor manifest state MUST treat the implicated manifest versions as terminally invalid and MUST persist that evidence.
- **Interpretation boundaries:** The manifest authorizes attribution and signature validation. It MUST NOT be interpreted as evidence of independence, settlement, or content endorsement.

---

## 5. Manifest profile identifier

The exact `manifest_profile_id` of this profile is:

```text
system-manifest/1
```

---

## 6. Required manifest model

A conforming `system-manifest/1` instance is a closed identity-only artifact: it carries exactly the material required to identify a CERTCRYPT System Domain and to validate the chain of public keys authorized to sign on its behalf. Provenance metadata, publication metadata, and rules-domain associations are deliberately excluded from this artifact. They MUST live in adjacent specifications such as `system-foundation/1` (statement-level metadata) or `arweave.publication/1` (an optional publication profile, not part of the published corpus) (publication-level metadata).

A conforming `system-manifest/1` instance MUST be a JSON object containing exactly the following top-level members, in any order, and no others:

- `manifest_profile_id`
- `system_id`
- `manifest_sequence`
- `entries`

All four top-level members participate in canonical serialization (Section 8) and therefore in the manifest digest (Section 10). There are no informational, provenance, or publication-derived top-level members under `/1`.

Each element of `entries` MUST be a JSON object containing exactly the following members, in any order, and no others:

- `kid`
- `algorithm`
- `quorum`
- `members`
- `valid_from`
- `valid_until`
- `predecessor_kid`
- `successor_kid`
- `predecessor_signatures`
- `predecessor_manifest_fingerprint`

The schema is closed. Implementations MUST reject any manifest, entry, `quorum` object, `members` element, or `predecessor_signatures` element that contains a member not listed in this specification. No top-level extension, no per-entry extension, and no parser-specific accommodation is permitted under `/1`. Future versions MAY introduce additional members under their own version identifier.

Each manifest entry authorizes a **quorum** of composite signing keys rather than a single key. The `quorum` member declares a threshold `k` of `n`; the `members` member lists the `n` authorized composite keys; and `predecessor_signatures` carries the set of composite signatures by which the predecessor entry's quorum authorizes this entry. The single-key model is not representable under `/1`: every entry MUST declare `quorum.k ≥ 2`.

The `quorum` member MUST be a JSON object containing exactly the members `k` and `n`, each a JSON number that is a positive integer, with `2 ≤ k ≤ n`.

The `members` member MUST be a JSON array of exactly `n` elements. Each element MUST be a JSON object containing exactly the members `member_kid`, `public_key_p256_b64`, and `public_key_mldsa_b64`, and no others.

`manifest_sequence` MUST be a JSON number that is a non-negative integer. The bootstrap manifest version MUST have `manifest_sequence = 0`. Every successor manifest version MUST have `manifest_sequence` exactly one greater than the manifest version from which it was rotated.

`manifest_profile_id` MUST be the exact literal string `"system-manifest/1"`.

`system_id` MUST be a non-empty ASCII string identifying the CERTCRYPT System Domain. It MUST be invariant across rotations of the same system domain.

---

## 7. Entry field semantics

### 7.1 `kid`

Identifies the manifest entry uniquely within the manifest.

`kid` MUST be a non-empty ASCII string that is unique across all entries of the manifest. It MUST be stable for the lifetime of the entry. It MUST NOT be reused for any other entry, including after the entry has been rotated out.

### 7.2 `algorithm`

Identifies the exact composite signature profile of the entry.

The value MUST be one exact composite profile identifier registered by `composite-signature/1` (e.g. `certcrypt-composite-p256-mldsa65-v1`). Implementations MUST reject manifests whose entry uses a profile not supported by the implementation, but MUST NOT silently substitute another profile. Every member of the entry's quorum (§7.3) is a composite key under this one profile; all `n` members of a single entry MUST share the same `algorithm`.

### 7.3 `quorum` and `members`

`quorum` and `members` together declare the set of composite keys authorized to sign on behalf of this entry, and the threshold required.

`quorum` MUST be a JSON object `{ "k": <int>, "n": <int> }` with `2 ≤ k ≤ n`. `k` is the minimum number of distinct member signatures required to authorize a rotation away from this entry (§12); `n` is the number of members. The single-key case (`k = 1`) is not permitted under `/1`.

`members` MUST be a JSON array of exactly `n` elements. Each element is one authorized composite key:

- `member_kid` — a non-empty ASCII string identifying the member uniquely within the entry. It MUST be unique across all members of the entry, stable for the lifetime of the entry, and MUST NOT be reused for any other member of the same entry.
- `public_key_p256_b64` — the classical component (ECDSA P-256), RFC 4648 base64 with padding, in the SEC1 **uncompressed** encoding: 65 bytes, the first byte `0x04`. This is the only encoding of this field (`composite-signature/1` Section 9.1); a compressed point or an SPKI structure carrying the same key is malformed, because each encoding would give the manifest a different digest.
- `public_key_mldsa_b64` — the post-quantum component (ML-DSA-65, FIPS 204 pkEncode, 1952 bytes), RFC 4648 base64 with padding.

The decoded byte length of each component public key MUST match the length required by its component algorithm under the entry's declared `algorithm` profile. If any decoding fails, any length or encoding does not match, `member_kid` values are not unique, or the number of `members` elements is not exactly `n`, validation of the manifest MUST fail. Each member's two component keys together form one composite signer key referenced by `composite-signature/1`; neither component alone is a verification key (composite-only).

### 7.4 `valid_from`

Declares the first instant at which this entry is considered the active signing entry.

`valid_from` MUST be an RFC 3339 timestamp with explicit UTC zone (`Z`).

For the first entry of the manifest, `valid_from` MAY equal the manifest creation time.

For any successor entry, `valid_from` MUST be strictly greater than the `valid_from` of its predecessor.

### 7.5 `valid_until`

Declares the exclusive upper bound of the interval during which this entry is treated as the active signing entry.

`valid_until` MUST be either an RFC 3339 timestamp with explicit UTC zone, or the literal JSON value `null`.

A `null` value means the entry has not yet been rotated out and is currently the active entry. At most one entry of a manifest MAY have `valid_until = null`. That entry MUST be the last entry of `entries`.

The active interval of an entry is half-open: a rotated-out entry is active during `[valid_from, valid_until)`, and an entry with `valid_until = null` is active during `[valid_from, +∞)`. The exact `valid_until` instant is **not** within the active interval of the rotated-out entry; it is within the active interval of the successor entry.

When a successor entry is appended, the predecessor’s `valid_until` MUST be set to the successor’s `valid_from`. The two timestamps MUST be exactly equal. The half-open interval rule defined in this section ensures there is no overlap at the boundary instant: the boundary belongs exclusively to the successor.

### 7.6 `predecessor_kid`

Identifies the predecessor entry within the same manifest.

For the first entry of the manifest, `predecessor_kid` MUST be the literal JSON value `null`.

For any successor entry, `predecessor_kid` MUST equal the `kid` of the entry that immediately precedes it in `entries`.

### 7.7 `successor_kid`

Identifies the successor entry within the same manifest.

For the active entry of the manifest, `successor_kid` MUST be the literal JSON value `null`.

For any rotated-out entry, `successor_kid` MUST equal the `kid` of the entry that immediately follows it in `entries`.

### 7.8 `predecessor_signatures`

Carries the quorum of composite signatures by which the predecessor entry authorizes this entry.

For the first entry of the manifest, `predecessor_signatures` MUST be the literal JSON value `null`. The first entry is self-anchored through `system-foundation/1`; no in-manifest predecessor signatures are possible.

For any successor entry, `predecessor_signatures` MUST be a JSON array. Each element MUST be a JSON object containing exactly the members `signer_member_kid` and `signature`, and no others:

- `signer_member_kid` — the `member_kid` of the predecessor entry member that produced this signature.
- `signature` — a composite signature (`composite-signature/1` wire object — `alg`, `mode`, ordered `signatures[]`) produced by that member's composite signing key over the canonical unsigned successor-binding payload defined in Section 9.

The array MUST contain at least the predecessor entry's `quorum.k` elements. The manifest is accepted only if at least `k` of these signatures verify under **distinct** predecessor members, by the quorum verification rule of Section 12.3. Each composite signature verifies AND over all components, fail-closed on the post-quantum component. If fewer than `k` distinct members verify, the manifest MUST be rejected.

Two or more elements with the same `signer_member_kid` count as **one** member toward the threshold. An element whose `signer_member_kid` is not a `member_kid` of the predecessor entry does not count toward the threshold; its presence is not by itself fatal, but it never contributes to reaching `k`.

### 7.9 `predecessor_manifest_fingerprint`

Identifies the exact manifest version that the predecessor entry was the active entry of, immediately before this entry was appended.

For the first entry of the manifest, `predecessor_manifest_fingerprint` MUST be the literal JSON value `null`. The bootstrap manifest has no predecessor manifest version.

For any successor entry, `predecessor_manifest_fingerprint` MUST carry the lowercase 64-character hexadecimal `system_root_fingerprint` of the manifest version that existed immediately before this rotation. That value is the digest computed under Section 10 over the canonical bytes of the predecessor manifest version, in which the predecessor entry was the active entry (its `valid_until` was `null` and its `successor_kid` was `null`).

This field binds each successor entry to the exact manifest state under which the predecessor authorized the rotation. It is the normative anchor of the anti-equivocation rules of Section 12.5.

---

## 8. Canonical serialization

The canonical serialization of a system manifest is:

```text
canonical_bytes(manifest) = UTF-8( JCS( manifest ) )
```

where:

- `JCS` means RFC 8785 JSON Canonicalization Scheme over the manifest object as a parsed JSON value
- `UTF-8` means UTF-8 encoding of the resulting string

Implementations MUST canonicalize the parsed JSON value. They MUST NOT canonicalize the raw source bytes received over any transport.

`predecessor_signatures` and `successor_kid` are part of the canonical manifest. They participate in the manifest digest exactly as defined here.

The canonical bytes MUST be reproducible bit-for-bit by any conforming implementation given the same parsed manifest value.

---

## 9. Successor-binding payload

The canonical unsigned successor-binding payload over which every element of `predecessor_signatures` is computed is the exact JSON object:

```json
{
  "binding_profile": "system-manifest/1:successor-binding",
  "system_id": "<system_id>",
  "predecessor_kid": "<predecessor_kid>",
  "predecessor_manifest_fingerprint": "<digest_of_predecessor_manifest_version>",
  "predecessor_manifest_sequence": <integer_manifest_sequence_of_predecessor>,
  "successor_kid": "<kid_of_new_entry>",
  "successor_algorithm": "<composite_profile_of_new_entry>",
  "successor_quorum": { "k": <int>, "n": <int> },
  "successor_members": [
    {
      "member_kid": "<member_kid>",
      "public_key_p256_b64": "<p256_public_key>",
      "public_key_mldsa_b64": "<mldsa_public_key>"
    }
  ],
  "successor_valid_from": "<valid_from_of_new_entry>"
}
```

in that exact member order and with no additional members, canonicalized under Section 8. `successor_quorum` and `successor_members` declare the **entire successor quorum** the predecessor authorizes: the same `quorum` object and `members` array that will appear in the successor entry (Section 7.3). `successor_members` MUST list exactly `successor_quorum.n` elements, each with exactly the three members shown, in the same element order they will hold in the successor entry.

Every signature in the successor entry's `predecessor_signatures` (Section 7.8) MUST be a composite signature (`composite-signature/1`) produced by a predecessor member's composite signing key over `M'( SHA3-256( UTF-8( JCS( payload ) ) ) )` — the one identical canonical payload. Binding the whole successor quorum into the signed payload means the predecessor quorum attests to *which set of keys* succeeds it, not merely to a single successor key; a verifier rejects any successor entry whose `quorum`/`members` differ from what the binding signed.

If the binding payload contains members other than those listed, if any required member is missing, or if `successor_members` does not match `successor_quorum.n` in length, validation MUST fail.

The `predecessor_manifest_fingerprint` and `predecessor_manifest_sequence` members bind the rotation to the exact predecessor manifest state. They are the normative inputs against which the anti-equivocation rules of Section 12.5 are evaluated.

---

## 10. Manifest digest

For `system-manifest/1`, the exact `system_root_fingerprint` derivation is:

```text
system_root_fingerprint = SHA3-256( canonical_bytes(manifest) )
```

where `canonical_bytes(manifest)` is defined in Section 8.

The output representation MUST be lowercase hexadecimal without prefix. The output MUST be exactly 64 hexadecimal characters.

The exact `root_fingerprint_derivation` identifier under `/1` is:

```text
sha3-256-system-manifest-jcs-v1
```

Any artifact whose root material is governed by `system-manifest/1` MUST use this derivation identifier.

---

## 11. Bootstrap

The first manifest version of a system domain is constructed by:

1. choosing the founding quorum threshold `k` and member count `n`, with `2 ≤ k ≤ n`, and generating `n` composite key pairs under one exact composite profile (`composite-signature/1`): each a classical (ECDSA P-256) and a post-quantum (ML-DSA-65) component, each derived from its own master seed held by a distinct member custody
2. assigning a stable `kid` to the entry, and a stable unique `member_kid` to each of the `n` members
3. constructing the first entry with all closed-schema members of Section 6 set as follows:
   - `kid` = the chosen stable identifier
   - `algorithm` = the composite profile id shared by all member key pairs
   - `quorum` = `{ "k": <chosen k>, "n": <chosen n> }`
   - `members` = the array of the `n` member objects, each `{ member_kid, public_key_p256_b64, public_key_mldsa_b64 }` with base64-encoded component public keys
   - `valid_from` = the chosen activation timestamp under Section 7.4
   - `valid_until` = `null`
   - `predecessor_kid` = `null`
   - `successor_kid` = `null`
   - `predecessor_signatures` = `null`
   - `predecessor_manifest_fingerprint` = `null`
4. constructing the manifest object with all closed-schema top-level members of Section 6 set as follows:
   - `manifest_profile_id` = `"system-manifest/1"`
   - `system_id` = the chosen system domain identifier
   - `manifest_sequence` = `0`
   - `entries` = the JSON array containing exactly the first entry constructed in step 3
5. canonicalizing the manifest under Section 8
6. computing `system_root_fingerprint` under Section 10

The bootstrap manifest MUST be wrapped in a `system-foundation/1` statement. The `system-foundation/1` statement MUST be authorized by a quorum of the bootstrap entry's members: at least `k` distinct members of the bootstrap entry MUST each produce a composite signature over the statement, and the statement is self-anchored only if at least `k` distinct member signatures verify. No in-manifest `predecessor_signatures` are required or possible for the first entry.

The `system_root_fingerprint` of the bootstrap manifest is the bootstrap fingerprint of the system domain. Subsequent manifest versions of the same system domain are produced exclusively by rotation under Section 12.

---

## 12. Rotation operation

Rotation is the only operation by which a manifest version MAY be superseded by a later manifest version of the same system domain.

### 12.1 Rotation procedure

A conforming rotation MUST proceed as follows. Steps that compute or assign values are normative; the order is mandatory where one step depends on the output of another.

1. **Compute the predecessor manifest fingerprint and sequence.** Take the current valid manifest version of the system domain. Canonicalize it under Section 8 and compute its `system_root_fingerprint` under Section 10. Let `P_fp` be that fingerprint and `P_seq` be the current manifest’s `manifest_sequence`. Both values are inputs to step 4 and step 6.

2. **Generate the successor quorum material.** Choose the successor threshold `k'` and member count `n'` (`2 ≤ k' ≤ n'`; they need not equal the predecessor's). Generate `n'` new composite key pairs under one exact composite profile (each a P-256 and an ML-DSA-65 component). Assign one new stable `kid` to the successor entry that is unique across all entries of the current manifest and across every prior `kid` ever used by the system domain, and a stable unique `member_kid` to each successor member.

3. **Choose the successor activation timestamp.** Choose `successor_valid_from` as an RFC 3339 timestamp with explicit UTC zone, strictly greater than the current active entry’s `valid_from`.

4. **Construct the unsigned successor-binding payload.** Construct the JSON object defined in Section 9, with values:
   - `binding_profile` = `"system-manifest/1:successor-binding"`
   - `system_id` = the system domain’s `system_id`
   - `predecessor_kid` = the current active entry’s `kid`
   - `predecessor_manifest_fingerprint` = `P_fp` from step 1
   - `predecessor_manifest_sequence` = `P_seq` from step 1
   - `successor_kid` = the `kid` chosen in step 2
   - `successor_algorithm` = the composite profile of the key pairs generated in step 2
   - `successor_quorum` = `{ "k": k', "n": n' }` from step 2
   - `successor_members` = the array of `n'` member objects from step 2
   - `successor_valid_from` = the timestamp chosen in step 3

5. **Sign the binding payload with the predecessor quorum.** Have at least `k` distinct members of the **current active entry** each compute a **composite** signature (`composite-signature/1`) over `M'( SHA3-256( UTF-8( JCS( payload ) ) ) )` using that member's composite signing key, over the one identical canonical payload. Each member may sign on its own custody host. Let the result be the set of `{ signer_member_kid, signature }` objects.

6. **Construct the successor entry.** Construct a JSON object containing exactly the 10 closed-schema entry members of Section 6, with values:
   - `kid` = the `kid` chosen in step 2
   - `algorithm` = the composite profile of the key pairs generated in step 2
   - `quorum` = `{ "k": k', "n": n' }` from step 2
   - `members` = the array of `n'` member objects from step 2
   - `valid_from` = the timestamp chosen in step 3
   - `valid_until` = `null`
   - `predecessor_kid` = the current active entry’s `kid`
   - `successor_kid` = `null`
   - `predecessor_signatures` = the array of `{ signer_member_kid, signature }` objects from step 5 (at least `k` distinct predecessor members)
   - `predecessor_manifest_fingerprint` = `P_fp` from step 1

7. **Mutate the previous active entry.** In the new manifest version, the previous active entry’s `valid_until` MUST be set equal to the successor entry’s `valid_from`, and its `successor_kid` MUST be set equal to the successor entry’s `kid`. All other members of the previous active entry MUST be preserved exactly as they were in the predecessor manifest version.

8. **Construct the new top-level manifest object.** Construct a JSON object containing exactly the 4 closed-schema top-level members of Section 6, with values:
   - `manifest_profile_id` = `"system-manifest/1"`
   - `system_id` = the same `system_id` as the predecessor manifest version
   - `manifest_sequence` = `P_seq + 1`
   - `entries` = the array consisting of all entries of the predecessor manifest version (with the previous active entry mutated as in step 7) followed by the successor entry from step 6, in that exact order

9. **Canonicalize and digest the new manifest.** Canonicalize the new manifest under Section 8. Compute its `system_root_fingerprint` under Section 10.

10. **Publish.** Publish the new manifest version through the same mechanisms used for the previous manifest version.

A conforming rotation MUST produce all of: the canonicalized new manifest bytes, the new `system_root_fingerprint`, and the new `manifest_sequence` value. Any rotation tool that omits any of these outputs is non-conformant.

### 12.2 Rotation frequency

This specification does not impose a mandatory rotation frequency.

Conforming deployments SHOULD rotate the active entry at intervals appropriate to their threat model and operational policy.

Deployments operating under post-quantum signature algorithms with no known cryptanalytic concern MAY operate without scheduled rotation. In that case, rotation is triggered exclusively by operational events such as suspected compromise, custody loss, policy change, or algorithm deprecation.

Conforming verifiers MUST NOT reject a manifest version solely because its active entry has been active for an extended period. Operational staleness is a deployment concern; it is not a normative validity concern under this specification.

### 12.3 Rotation authorization (quorum verification rule)

A rotation is authorized exclusively by a quorum of valid composite signatures from the previous active entry's members over the successor-binding payload. To accept a successor entry `S` authorized by the previous active entry `P`, a conforming verifier MUST:

1. recover `P`'s `quorum.k` and its `members` array (the `n` authorized composite keys);
2. reconstruct the canonical unsigned successor-binding payload (Section 9) from `S`'s own `kid`, `algorithm`, `quorum`, `members`, and `valid_from`, together with `P`'s `kid`, `S`'s `predecessor_manifest_fingerprint`, and `P`'s `manifest_sequence`, and compute `M'( SHA3-256( UTF-8( JCS( payload ) ) ) )`;
3. for each element of `S`'s `predecessor_signatures`, locate the member of `P` whose `member_kid` equals the element's `signer_member_kid`, and verify the element's composite signature under that member's two component public keys (AND over all components, fail-closed on the post-quantum component);
4. count the number of **distinct** `P` members for which a signature verified; accept the rotation if and only if that count is `≥ k`.

The following rules apply to the count:

- Multiple verifying signatures attributed to the same `signer_member_kid` count as **one** member.
- A signature whose `signer_member_kid` is not a `member_kid` of `P` never contributes to the count.
- A signature that does not verify never contributes to the count.

No rotation MAY be authorized by:

- any non-active manifest entry
- any entry of a different system domain
- any external authority not represented in the predecessor entry's `members`
- any out-of-band statement that is not the canonical successor-binding payload

If fewer than `k` distinct predecessor members verify, the resulting manifest MUST be rejected. Any ambiguity in attribution or verification MUST be resolved as rejection (fail-closed).

### 12.4 Post-rotation properties

After a valid rotation:

- the previous active entry MUST be marked rotated-out by `valid_until` and `successor_kid` exactly as required by Section 12.1
- the previous active entry remains cataloged, unchanged except for the two members of Section 12.1 step 7, and no longer authorizes rotations
- the new active entry becomes the only entry of the manifest with `valid_until = null` and `successor_kid = null`
- the new manifest version has `manifest_sequence` exactly one greater than the predecessor manifest version
- the digest of the current manifest version changes to the digest of the new manifest version; the bootstrap fingerprint, which identifies the system domain and which every artifact carries (`system-domain/1` Section 16.1), does not change

### 12.5 Anti-equivocation properties under `/1`

The successor-binding payload of Section 9 binds each rotation to one exact predecessor manifest state, expressed as `predecessor_manifest_fingerprint` and `predecessor_manifest_sequence`. This binding makes equivocation by the predecessor entry **detectable as evidence**, but does not, under `/1`, prevent equivocation globally.

A predecessor entry whose quorum is compromised — at least `k` of its members' private keys obtained, or at least `k` members acting maliciously — retains the capability to authorize two or more distinct successor quorums, each carrying a valid quorum of predecessor signatures, all sharing the same `predecessor_manifest_fingerprint` and `predecessor_manifest_sequence`, but each authorizing a different `successor_kid`, `successor_quorum`, or `successor_members`. Each such successor entry, taken in isolation, will pass Section 13 validation. The set of resulting manifest versions form incompatible branches of the same predecessor.

Under `/1`, the property defined here is **linearity verifiable under available evidence**, not transparency-backed global non-equivocation. Specifically:

1. **Detection rule.** Equivocation is established whenever a conforming verifier holds two or more distinct successor-binding observations, each carrying a valid predecessor quorum under the same predecessor entry (at least `k` distinct predecessor members verifying per Section 12.3), indexed under the same `(system_id, predecessor_manifest_fingerprint, predecessor_manifest_sequence, predecessor_kid)`, but differing in any of `successor_kid`, `successor_quorum`, `successor_members`, `successor_algorithm`, or `successor_valid_from`. Detection is based on the verifier’s persisted observation set, not solely on simultaneous arrival.

2. **Observation persistence (mandatory).** A conforming verifier MUST persist every successor-binding observation it accepts as valid under Section 13.6. Each persisted observation MUST be indexed by the tuple `(system_id, predecessor_manifest_fingerprint, predecessor_manifest_sequence, predecessor_kid)` and MUST record at least the successor entry’s `kid`, `algorithm`, `quorum`, `members`, `valid_from`, and the exact bytes of the `predecessor_signatures` array. The verifier MUST persist these observations across sessions. Silent discarding of observations is a non-conformant operational state.

   The obligation falls on the verifier as deployed: the application that runs verifications over time and owns their storage. A verification library is stateless; it evaluates the observations supplied in one input, including any its host persisted earlier, and reports the ones it authenticated. The host persists those and supplies them with every later input. A deployment that keeps no store detects only conflicts inside a single input; it MUST NOT present that as the cross-session detection this section defines.

3. **Comparison rule (mandatory at validation time).** Before accepting any new manifest version or any new successor-binding observation as valid, the verifier MUST look up persisted observations under the same index tuple as each successor entry being validated. If a persisted observation differs from the new observation in any of `successor_kid`, `successor_quorum`, `successor_members`, `successor_algorithm`, or `successor_valid_from`, equivocation is established under the detection rule above and the consequence rule below applies. If no persisted observation exists for the index tuple, the new observation MUST be persisted exactly as defined in this section before the manifest version or observation is accepted.

4. **Fail-closed consequence.** Upon detection of equivocation, the verifier MUST treat the predecessor manifest version, and every manifest version that descends from any of the conflicting successor entries, as **terminally invalid** for the purpose of attributing artifacts to the CERTCRYPT System Domain. The verifier MUST reject any artifact bound to those manifest versions thereafter, regardless of whether the artifact’s direct signature would otherwise verify. The conflicting observations themselves MUST be retained as the canonical evidence of terminal invalidity; they MUST NOT be reduced or compressed in a way that loses the ability to reproduce the conflict.

5. **Scope.** The detection rule operates on observations that converge at a single verifier. Two verifiers holding disjoint observation sets without ever exchanging information will not detect equivocation between themselves. `/1` does not promise that property. Operational measures intended to maximize the probability of observation convergence are deployment concerns and lie outside this specification.

6. **Recovery.** `/1` does not define a recovery path from terminal invalidity. A system domain whose predecessor entry has been observed equivocating MUST be replaced by a new system domain with a new bootstrap manifest. Any continuity between the old and the new system domain is a deployment concern and is not normatively bridged by this specification.

7. **Honest-rotation invariant.** A predecessor entry whose quorum has not equivocated MUST authorize at most one successor quorum for any given pair `(predecessor_manifest_fingerprint, predecessor_manifest_sequence)`. Conforming implementations of the rotation procedure (Section 12.1) MUST refuse to assemble a second, differing successor binding for the same pair if one has already been assembled, even if the operators request it. Because authorization requires `k` distinct members, producing a conflicting binding outside the conforming implementation requires the cooperation or compromise of at least `k` members; the quorum threshold raises the cost of equivocation but does not by itself prevent it. This refusal is a defense in depth.

**What an artifact verifier observes under `/1`.** An artifact verifier holds the bootstrap manifest version, embedded in the `system-foundation/1` statement, and nothing later (Section 13). The observations it can authenticate are therefore those whose predecessor is the bootstrap entry: the first rotation, the only one the bootstrap members may authorize (`system-foundation/1` Section 9). They travel attached to the statement as `successor_binding_observations` (`system-foundation/1` Section 6). Equivocation in a later rotation does not implicate the bootstrap manifest version that artifacts carry; detecting it is a matter for whoever validates those later manifest versions under Section 13.

This section makes the equivocation surface of `/1` explicit. The quorum model raises the bar for *producing* equivocation from one compromised key to `k` compromised members; it does not prevent or detect it on its own. Stronger non-equivocation guarantees, such as transparency logs or witness quorums, remain out of scope of `/1`.

---

## 13. Manifest validation

This section defines when a manifest version is valid. It binds whoever validates a manifest version: a rotation tool before it publishes one (Section 12.1), and any party that checks a published rotation.

An **artifact verifier** under `/1` validates exactly one manifest version — the bootstrap version embedded in the `system-foundation/1` statement, to which every check below applies with a single entry — and the successor-binding observations attached to that statement (Sections 12.5 and 13.6). It does not need, and is not required to obtain, any later manifest version, because no artifact binds to one (Section 14).

A conforming verifier validating a system manifest MUST perform all of the following checks. Validation MUST fail if any check fails. No partial success state MAY substitute for a failed required check.

### 13.1 Profile identifier

Validate `manifest_profile_id = "system-manifest/1"`.

### 13.2 Canonical serialization

Recompute `canonical_bytes(manifest)` under Section 8. Recompute `system_root_fingerprint` under Section 10. The result MUST equal the digest by which the verifier obtained the manifest. If a verifier obtained the manifest by digest, that digest MUST equal the recomputed value.

### 13.3 Entry ordering

Validate that `entries` is a non-empty array. Validate that the first entry has `predecessor_kid = null` and `predecessor_signatures = null`. Validate that every subsequent entry has `predecessor_kid` equal to the `kid` of the immediately preceding entry. Validate that every entry except the last has `successor_kid` equal to the `kid` of the immediately following entry. Validate that the last entry has `successor_kid = null`.

### 13.4 Validity window continuity

Validate that for every entry except the last, `valid_until` is non-null and equal to the `valid_from` of the immediately following entry. Validate that the last entry has `valid_until = null`. Validate that for every entry, `valid_from` is strictly greater than the `valid_from` of its predecessor (if any).

### 13.5 Quorum, members, and key bytes

For every entry, validate that `algorithm` is supported; that `quorum` is `{ k, n }` with `2 ≤ k ≤ n`; that `members` has exactly `n` elements; that every `member_kid` is unique within the entry; and that each member's `public_key_p256_b64`/`public_key_mldsa_b64` decodes to the byte length required by `algorithm`.

### 13.6 Predecessor quorum

For every entry except the first, validate `predecessor_signatures` against the predecessor entry's quorum by the rule of Section 12.3: reconstruct the canonical successor-binding payload of Section 9, verify each element's composite signature under the predecessor member identified by its `signer_member_kid`, and require at least the predecessor's `quorum.k` distinct members to verify. Duplicate `signer_member_kid` values count once; signatures not attributable to a predecessor member do not count.

The successor-binding payload reconstructed for verification MUST use the entry's declared `predecessor_manifest_fingerprint` and the predecessor manifest version's `manifest_sequence` as the values for `predecessor_manifest_fingerprint` and `predecessor_manifest_sequence` in the payload, and the entry's own `kid`, `algorithm`, `quorum`, `members`, and `valid_from` as the `successor_*` values.

### 13.7 Predecessor manifest fingerprint consistency

For every entry except the first, validate that `predecessor_manifest_fingerprint` equals the digest, computed under Section 10, of the unique intermediate manifest version that existed when the predecessor entry was the active entry.

Under the closed schema of Section 6, the intermediate manifest version is fully determined by its index in the chain. It is constructed by:

- `manifest_profile_id` = `"system-manifest/1"`
- `system_id` = the same `system_id` as the manifest under validation
- `manifest_sequence` = the predecessor entry’s position in `entries`, where the bootstrap entry has position `0`
- `entries` = the array containing exactly the entries `[entry_0, entry_1, ..., entry_predecessor]`, with `entry_predecessor` modified so that `valid_until = null`, `successor_kid = null`, and all other members preserved exactly as declared in the manifest under validation

Because the schema is closed and provenance metadata is excluded from the manifest under Section 6, the intermediate manifest version is derivable without ambiguity from the manifest under validation alone. No external state, no deployment policy, and no per-version metadata is required for this reconstruction.

The verifier MUST canonicalize the intermediate manifest version under Section 8 and compute its digest under Section 10. If the recomputed digest does not equal the entry’s declared `predecessor_manifest_fingerprint`, validation MUST fail.

For the first entry, validate that `predecessor_manifest_fingerprint = null`.

### 13.8 Active entry uniqueness

Validate that exactly one entry has `valid_until = null` and `successor_kid = null`, and that this entry is the last entry of `entries`.

### 13.9 Manifest sequence continuity

Validate that the manifest’s `manifest_sequence` equals the count of entries minus one. The bootstrap manifest version (one entry) has `manifest_sequence = 0`; each rotation increments the sequence by exactly one.

### 13.10 Bootstrap signature

For the bootstrap manifest version: validate that it is wrapped in a `system-foundation/1` statement authorized by a quorum of its entry: at least that entry's `quorum.k` distinct members MUST have produced verifying composite signatures over the statement.

For a later manifest version: validate that the intermediate manifest version of sequence `0`, reconstructed under Section 13.7, has the digest of a bootstrap manifest version embedded in a `system-foundation/1` statement that the verifier has validated. A later manifest version carries no statement of its own; it is anchored to the system domain only through its bootstrap entry.

### 13.11 Successor-binding observation persistence and equivocation comparison

The verifier MUST apply the comparison rule of Section 12.5 to every successor entry under validation. For each successor entry of the manifest:

1. derive the index tuple `(system_id, predecessor_manifest_fingerprint, predecessor_manifest_sequence, predecessor_kid)` from the entry and the predecessor manifest version reconstructed under Section 13.7
2. look up the verifier’s persisted observations under that index tuple
3. if a persisted observation differs from the new observation in any of `successor_kid`, `successor_quorum`, `successor_members`, `successor_algorithm`, or `successor_valid_from`, the manifest MUST be rejected as terminally invalid under Section 12.5 and the conflicting observations MUST be retained
4. if no persisted observation exists for the index tuple, the new observation MUST be persisted as defined in Section 12.5 before the manifest is accepted; persistence MUST occur atomically with acceptance

If any successor entry of the manifest descends from a manifest version previously recorded as terminally invalid by the verifier, the manifest MUST be rejected as terminally invalid regardless of the outcome of the preceding validation steps.

---

## 14. Later manifest versions and artifact attribution

Under `/1` no artifact binds to a manifest version other than the bootstrap version. Every artifact attributed to the system domain carries the bootstrap fingerprint (`system-domain/1` Section 16.1), and the key that signs operational artifacts is carried by the bootstrap statement, not by a manifest entry (Section 15). A verifier MUST NOT accept, as the `system_root_fingerprint` of an artifact, the digest of any later manifest version.

Reconciliation between manifest versions for the purpose of attributing artifacts, and the transport of later manifest versions inside verification packages, are not defined by this version. A successor specification that lets artifacts bind to later manifest versions defines them together with the succession of operational keys.

---

## 15. Keys that sign operational artifacts

The members of a manifest entry sign **rotation and bootstrap** (Sections 11–13): changing or founding the system domain's key chain requires `k` distinct members of the active entry. Manifest members do **not** sign operational artifacts.

The operational artifacts of the system domain — the Level-1 capacity-authorization binding and the `independence.proof/1` signature — are signed by the system-domain **Level-1 capacity key**: the composite key pair `system_domain_capacity_key_p256_b64` / `system_domain_capacity_key_mldsa_b64` carried at statement level by the bootstrap [`system-foundation/1`](../../system-foundation/1/specification.md) statement (Section 6 of that specification). That key is authenticated by the bootstrap quorum signature over the statement, not by a manifest entry, and it is deliberately kept out of the manifest so that it does not enter the `system_root_fingerprint`.

A verifier validating an operational artifact therefore:

1. obtains the bootstrap `system-foundation/1` statement of the system domain and validates it under that specification, including its quorum signature
2. takes the Level-1 capacity key from that statement
3. validates the artifact's composite signature under that key and the signature profile the governing rules domain fixes for that artifact, per `composite-signature/1`

If any step fails, the artifact MUST be rejected. An operational artifact carries no manifest `kid` or member identifier, and a verifier MUST NOT resolve its signing key from the manifest.

Under `system-manifest/1` the Level-1 capacity key does not rotate: the bootstrap statement is produced once and never re-issued (`system-foundation/1` Section 4), so the key it carries is the key for every operational artifact of the system domain. A rotation of the manifest (Sections 11–13) changes who may authorize the next rotation; it does not change the Level-1 capacity key. A lifecycle for operational keys — succession, validity intervals, retirement — is not defined by this version and requires a successor specification. Compromise of the Level-1 capacity key is outside the threat model of the foundation layer ([`security-model/1` threat model](../../security-model/1/threat-model.md), Section 7).

---

## 16. Interpretation boundary

A valid `system-manifest/1` artifact MAY be used to:

- catalog the historical and current public keys of one CERTCRYPT System Domain
- derive the canonical `system_root_fingerprint` of that system domain
- resolve which entry's quorum governs rotation of that system domain at a given time

A valid `system-manifest/1` artifact MUST NOT be used to:

- prove truth
- prove `Independent`
- prove settlement
- endorse issuer claims semantically
- replace `submission-set/1` validation
- replace `independence.proof/1` validation
- replace `verification-package/1` validation
- become a substitute for the rules domain governing any individual artifact

---

## 17. Failure conditions

Validation MUST fail if any of the following hold:

- `manifest_profile_id` differs from `"system-manifest/1"`
- canonicalization is ambiguous or parser-dependent
- the manifest, any element of `entries`, any `quorum` object, any `members` element, or any `predecessor_signatures` element contains a member not listed in this specification
- any required member of the manifest or of an entry is absent
- the recomputed `system_root_fingerprint` differs from any value by which the manifest was retrieved or referenced
- `manifest_sequence` is absent, negative, non-integer, or does not equal the count of entries minus one
- `entries` is empty
- the first entry’s `predecessor_kid`, `predecessor_signatures`, or `predecessor_manifest_fingerprint` is not `null`
- any successor entry’s `predecessor_kid` does not match the immediately preceding entry’s `kid`
- any successor entry’s `predecessor_manifest_fingerprint` does not equal the digest of the predecessor manifest version reconstructed as defined in Section 13.7
- any non-last entry’s `successor_kid` does not match the immediately following entry’s `kid`
- the last entry’s `successor_kid` or `valid_until` is not `null`
- any entry’s `valid_from` is not strictly greater than its predecessor’s
- any rotated-out entry’s `valid_until` does not equal the immediately following entry’s `valid_from`
- any entry declares an unsupported `algorithm`, a `quorum` with `k < 2` or `k > n`, a `members` array whose length is not `n`, non-unique `member_kid` values, or a member `public_key_p256_b64`/`public_key_mldsa_b64` whose decoded length does not match `algorithm`
- any successor entry’s `predecessor_signatures` fails to reach the predecessor’s `quorum.k` distinct verifying members (Section 12.3) over the canonical successor-binding payload, where the payload includes `predecessor_manifest_fingerprint` and `predecessor_manifest_sequence` exactly as declared by the successor entry and the predecessor manifest version
- more than one entry has `valid_until = null` or `successor_kid = null`
- the bootstrap manifest version is not wrapped in a `system-foundation/1` statement authorized by at least its entry’s `quorum.k` distinct verifying members, or a later manifest version is not anchored to such a statement (Section 13.10)
- an artifact carries the digest of a later manifest version as its `system_root_fingerprint` (Section 14)
- the comparison rule of Section 12.5 detects a conflict between a new successor-binding observation and a persisted observation under the same index tuple, or the manifest version, or any manifest version it descends from, has been previously recorded by the verifier as terminally invalid
- the verifier fails to persist a new successor-binding observation atomically with acceptance

No partial success state MAY substitute for a failed required condition.

---

## 18. Security properties

A conforming `system-manifest/1` instance MUST preserve the following properties:

1. append-only history of public keys
2. self-anchored chain authority through predecessor signatures
3. deterministic digest under canonical serialization, with a closed schema that admits no unknown members
4. uniqueness of the active entry within any manifest version
5. half-open continuity of validity windows across rotations, where the rotation boundary instant belongs to the successor
6. invariance of the bootstrap fingerprint, which identifies the system domain and is the only `system_root_fingerprint` an artifact carries under `/1`
7. no manifest entry signs operational artifacts (Section 15)
8. invariance of `system_id` across rotations
9. rejection of any rotation not authorized by a quorum of the immediate predecessor entry's members (Section 12.3) over a successor-binding payload that binds the exact predecessor manifest version and sequence
10. rejection of any rotation authorized by an entry outside its half-open active interval
11. equivocation by a predecessor entry MUST be detectable as evidence whenever two or more conflicting successor observations over the same index tuple `(system_id, predecessor_manifest_fingerprint, predecessor_manifest_sequence, predecessor_kid)` are present in a single conforming verifier’s persisted observation set, and MUST cause fail-closed terminal invalidity of the implicated manifest versions
12. every successor-binding observation accepted as valid MUST be persisted across verifier sessions, indexed under the tuple defined in Section 12.5; observation persistence is mandatory and not contingent on detected conflict
13. equivocation evidence, once accumulated, MUST NOT be silently discarded or compressed in a way that loses the ability to reproduce the conflict

This specification provides linearity verifiable under available evidence, and a quorum threshold that raises the cost of equivocation to the compromise of `k` members. It does not provide transparency-backed global non-equivocation; that property (transparency logs, witness quorums) is reserved for a future version of this specification if operationally justified.

Any implementation that weakens any of these properties MUST be considered non-conformant.

---

## 19. Privacy and data-minimization

A `system-manifest/1` instance discloses only the operational key material and validity windows necessary to validate signatures bound to the system domain.

It MUST NOT require inclusion of:

- original certified payload material
- semantic content of any certified subject
- internal CERTCRYPT operational databases as a source of truth
- any issuer-identifying material

The manifest MUST remain compatible with the CERTCRYPT zero-data architecture.

---

## 20. Conformance

An implementation conforms to `system-manifest/1` if and only if:

- it constructs or validates the exact manifest model defined here
- it derives `system_root_fingerprint` exactly as defined here
- it performs rotation exclusively under Section 12
- it validates manifests under Section 13 without partial success states
- as an artifact verifier, it accepts only the bootstrap fingerprint as an artifact's `system_root_fingerprint` (Section 14)
- it resolves the key of operational artifacts under Section 15, never from a manifest entry
- it does not collapse manifest semantics into trust-authority semantics
- it does not treat publication anchors as a substitute for manifest validation

Partial implementations MUST NOT claim full conformance.

---

## 21. Future evolution

Future versions of this model MAY:

- introduce additional algorithm identifiers
- let artifacts bind to later manifest versions, with an offline reconciliation mechanism and its transport, together with the succession of operational keys
- introduce structured deprecation metadata for retired algorithms
- introduce transparency-log or witness-quorum mechanisms that strengthen the equivocation surface beyond the local-evidence model defined in Section 12.5

Future versions MUST NOT:

- permit removal or rewriting of historical entries
- permit rotation authorized by anything other than a quorum of the immediate predecessor entry's members (Section 12.3)
- permit ambiguous canonicalization
- permit unknown members in the manifest or in entries, except under an explicit and named extension registry defined by that future version
- collapse the manifest into authority over independence or settlement
- permit re-derivation of `system_root_fingerprint` by any rule that ignores any portion of the canonical manifest
- weaken the equivocation-evidence and fail-closed properties of Section 12.5

Any such change would require a new non-compatible version identifier.

---

## 22. Final normative statement

A valid `system-manifest/1` instance is the canonical artifact whose deterministic digest is the `system_root_fingerprint` of one CERTCRYPT System Domain, catalogs the append-only chain of quorums authorized to rotate that system domain across time, and keeps the bootstrap fingerprint — the identity every artifact carries — invariant, unless equivocation evidence accumulated against the bootstrap entry makes the system domain terminally invalid, without itself proving truth, settlement, consumption, or `Independent`.

---

## 23. Versioning & extensibility

This `/1` specification defines the current active public contract for `system-manifest/1`.

Once frozen, this version MUST NOT be modified in place in any way, including editorial, typographic or clarifying changes that would leave its normative meaning unchanged. Any change MUST be published under a new version identifier.

---

## 24. References

- CERTCRYPT Specifications
    - [security-model/1 — CERTCRYPT Security Model](../../security-model/1/index.md)
    - [system-foundation/1 — CERTCRYPT System Foundation](../../system-foundation/1/index.md)
    - [system-domain/1 — CERTCRYPT System Domain](../../system-domain/1/index.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../rules-domain/1/index.md)
    - [composite-signature/1 — CERTCRYPT Composite Signature Profile](../../composite-signature/1/index.md)
    - [independence.proof/1 — CERTCRYPT Independence Proof Model](../../../models/independence.proof/1/index.md)
    - [submission-set/1 — CERTCRYPT Submission Set Protocol](../../../protocols/settlement/submission-set/1/index.md)
    - [verification-package/1 — CERTCRYPT Verification Package Specification](../../../ecosystem/verification/verification-package/1/index.md)
- **External**
    - [RFC 3339 — Date and Time on the Internet: Timestamps](https://www.rfc-editor.org/rfc/rfc3339)
    - [RFC 4648 — The Base16, Base32, and Base64 Data Encodings](https://www.rfc-editor.org/rfc/rfc4648)
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
    - [RFC 8785 — JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785)

---

**End of system-manifest/1**
