# CERTCRYPT System Foundation Specification (system-foundation/1)

**Identifier:** `system-foundation/1`  

**Label:** CERTCRYPT System Foundation Specification (system-foundation/1)  

**Type:** Foundation Specification

**Status:** Frozen

**Layer:** Layer 0 — Foundation

**Depends on:** See References *(active normative dependencies are listed below)*  

**Naming convention:**  
`system-foundation/1` is the formal identifier.  
CERTCRYPT System Foundation Specification (system-foundation/1) is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.  

**Audience:** Protocol designers, specification authors, implementers, auditors  

**Purpose:** Define the normative semantics, constraints, and interpretation boundary of system-foundation/1 within the active CERTCRYPT public architecture.  

**Intended use:** system-foundation/1 is intended to be the authoritative public specification used by conforming implementers, verifiers, auditors, and ecosystem tooling when handling this artifact or behavior.  

**Scope:** Defines the active normative behavior of system-foundation/1; adjacent protocols, profiles, operational tooling, and product behavior remain out of scope except where explicitly referenced.  

**Non-goals:** system-foundation/1 does not prove truth, semantic validity, legal validity, or live service authority by itself, and MUST NOT be interpreted as a substitute for cryptographic authenticity, Proof of Independence, or managed-service behavior outside its own normative scope.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale
This specification defines the canonical CERTCRYPT foundation statement.

The foundation statement is the canonical artifact by which CERTCRYPT root material MAY be published, transported, cached, and validated under public rules.

Under the active corpus, root material is declared as an embedded `system-manifest/1` bootstrap manifest version, not as a standalone public key. The statement signs exactly that bootstrap manifest. Successor manifest versions are produced by rotation under `system-manifest/1` Section 12; they are never re-wrapped in a new `system-foundation/1` statement, and they do not change the fingerprint artifacts carry, which is always the bootstrap fingerprint this statement attests (`system-manifest/1` Section 14).

This specification defines:

- one exact foundation profile identifier
- one exact foundation-statement model that embeds a bootstrap `system-manifest/1` manifest version
- one exact derivation of `system_root_fingerprint` from the embedded bootstrap manifest
- one exact bootstrap signature model anchored by the bootstrap entry of the embedded manifest
- one exact boundary between immutable publication and normative validation

It does **not** define:

- truth semantics
- independence semantics
- certificate validity by itself
- settlement execution
- mandatory live retrieval behavior

Those concerns belong to other specifications.

---

## 2. Scope

This specification applies to all systems, implementations, verifiers, publishers, auditors, caches, mirrors, and package builders that:

- construct
- publish
- cache
- transport
- validate
- inspect

a CERTCRYPT foundation statement claiming conformity with `system-foundation/1`.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

---

## 4. Design principles

`system-foundation/1` is designed around the following principles:

- **Bootstrap exactness:** A foundation statement MUST provide one exact bootstrap declaration model for root material and attribution context.
- **Manifest-anchored identity:** Root material is declared by embedding one exact `system-manifest/1` bootstrap manifest version. The statement signs that bootstrap manifest exclusively; successor manifest versions are not signed, wrapped, or republished by `system-foundation/1`.
- **Bootstrap finality:** A `system-foundation/1` statement is produced exactly once per system domain. It is never refreshed, ratified, or re-issued. Continuity of the system domain across rotations is provided exclusively by `system-manifest/1`.
- **Deterministic derivation:** Root-fingerprint derivation and validation MUST be mechanically reproducible from the embedded manifest and applicable public rules.
- **Offline verifiability:** Verification of a foundation statement MUST remain possible without live CERTCRYPT infrastructure.
- **Publication without authority:** Publication can reinforce auditability and historical traceability, but it MUST NOT be treated as a source of truth, independence, or semantic authority.
- **Infrastructure neutrality:** The bootstrap model MUST remain interpretable across environments without dependence on one provider, service wrapper, or managed delivery layer.
- **Interpretation boundaries:** `system-foundation/1` supports attribution bootstrap only. It does not replace `system-domain/1`, `rules-domain/1`, `system-manifest/1` rotation semantics, settlement validation, or Proof of Independence.

---

## 5. Foundation profile identifier

The exact `foundation_profile_id` of this profile is:

```text
system-foundation/1
```

---

## 6. Required statement model

A conforming `system-foundation/1` statement is a JSON object that MUST contain:

- `foundation_profile_id`
- `foundation_statement_id`
- `system_id`
- `system_root_fingerprint`
- `system_manifest`
- `root_fingerprint_derivation`
- `system_domain_capacity_key_p256_b64`
- `system_domain_capacity_key_mldsa_b64`
- `published_rules_versions`
- `statement_issued_at`
- `statement_signatures`

It MAY also contain:

- `publication_refs`
- `successor_binding_observations`

and no other member. A verifier MUST reject a statement that carries a member not listed in this section.

`publication_refs`, if present, MUST be treated as provenance and discovery aids only.

They MUST NOT alter the meaning of the foundation statement.

`successor_binding_observations`, if present, is evidence a holder of the statement attaches to it, not part of the statement: it is outside the signed payload (Section 9), so attaching, removing, or reordering observations never affects signature validity. It is a non-empty JSON array; each element is an object with exactly two members, `successor_binding` — a successor-binding payload of `system-manifest/1` Section 9 — and `predecessor_signatures` — the array of `{ signer_member_kid, signature }` objects that authorizes it. A verifier MUST validate every element before relying on any of them, exactly as `system-manifest/1` Section 12.5 requires: the binding MUST name the embedded bootstrap entry as predecessor (its `kid`, the bootstrap fingerprint, and sequence `0`), and at least `system_manifest.entries[0].quorum.k` distinct bootstrap members MUST carry a verifying composite signature over it (`system-manifest/1` Section 12.3). An element that fails either check makes the whole statement fail: an unauthenticated observation is not evidence, and it is not silently dropped either. Two authenticated elements that conflict establish equivocation under `system-manifest/1` Section 12.5, and the statement MUST then be rejected as terminally invalid.

Formats:

- `foundation_statement_id` MUST be a string of 1 to 128 characters drawn from `A`–`Z`, `a`–`z`, `0`–`9`, `.`, `_`, `/` and `-`. It names the statement; it carries no other meaning.
- `statement_issued_at` MUST be an RFC 3339 timestamp in UTC with the explicit zone designator `Z` (for example `2026-10-18T18:01:06Z`).
- `system_id` MUST be the `system_id` of the embedded manifest.

`system_manifest` MUST be the exact `system-manifest/1` bootstrap manifest version whose canonical digest equals the declared `system_root_fingerprint`. The manifest embedded in a `system-foundation/1` statement is **always** the bootstrap manifest version, that is, the unique manifest version with `manifest_sequence = 0` and exactly one entry under that system domain. Implementations MUST NOT embed any successor manifest version inside a `system-foundation/1` statement. Successor manifest versions are anchored to the system domain through this bootstrap manifest (`system-manifest/1` Section 13.10); they are never re-wrapped in a new `system-foundation/1` statement.

`published_rules_versions` MUST be a JSON array of strings, each identifying one rules-domain version that this foundation statement declares as active under the embedded manifest. When the deployment declares no rules versions for the statement, `published_rules_versions` MUST be the empty array `[]`. The list is statement-level metadata under `system-foundation/1`; it is deliberately not part of the canonical manifest under `system-manifest/1`, so that rules-version associations never change the manifest digest. It records which rules versions were declared when the statement was produced, and nothing more. Because the statement is produced once and never re-issued (Section 4), the list cannot grow: a rules version registered later is absent from it by construction. A verifier therefore MUST NOT reject an artifact, or the statement, because the artifact's `rules_version` is absent from this list. The normative bind between a rules version and a system domain is the rules registry of that system domain, governed by `system-domain/1` Section 16.1 (step 2) and `rules-domain/1`.

Under `/1`, the **root** algorithm and root key bytes are declared only inside `system_manifest.entries[0]`. The statement carries no separate top-level root-key material fields.

The statement does, however, carry one piece of **non-root** key material at statement level: the system-domain Level-1 capacity key, as the pair `system_domain_capacity_key_p256_b64` and `system_domain_capacity_key_mldsa_b64`. This is the composite signing key (ECDSA P-256 + ML-DSA-65, under the same composite profile as the root) against which the system domain's operational Level-1 signatures are validated — specifically the Level-1 capacity-authorization binding and the `independence_proof` signature governed by adjacent specifications. It is **distinct from the root quorum**: the root authorizes rotation and bootstrap (a quorum event), whereas the Level-1 capacity key is a single operational key the bootstrap statement authorizes once.

This material is carried at statement level, and **not** inside `system_manifest`, by design. The manifest under `system-manifest/1` is identity-only: its digest is the `system_root_fingerprint`, which MUST remain stable across rotations of operational, provenance, and rules associations. Embedding the Level-1 capacity key in the manifest would make every Level-1 key change alter the system-domain identity fingerprint, which is prohibited. Carrying it at statement level keeps it out of the identity digest while still binding it under the bootstrap quorum signature (Section 9), so that it cannot be substituted without invalidating the statement.

`system_domain_capacity_key_p256_b64` MUST be the classical component (ECDSA P-256, SEC1 **uncompressed** encoding: 65 bytes, first byte `0x04`) and `system_domain_capacity_key_mldsa_b64` MUST be the post-quantum component (ML-DSA-65, FIPS 204 pkEncode, 1952 bytes), each RFC 4648 base64 with padding. These are the only encodings of these fields (`composite-signature/1` Section 9.1): a compressed point or an SPKI structure carrying the same key is malformed. Both members are REQUIRED. A statement that omits either, or whose either component fails to decode to the required length, is non-conformant.

---

## 7. Canonical current root-material model

For `/1`, the current root-material model is one exact embedded bootstrap `system-manifest/1` model.

Under that model:

- `system_manifest` MUST be a complete and conforming `system-manifest/1` bootstrap manifest version, validated under `system-manifest/1` Section 13
- `system_manifest.manifest_sequence` MUST equal `0`. A `system-foundation/1` statement that embeds any other manifest version is non-conformant; successor manifest versions are not embedded in `system-foundation/1` statements, and no artifact carries their digest (`system-manifest/1` Section 14)
- `system_manifest.entries` MUST be an array of length exactly `1`, containing the bootstrap entry
- the algorithm and the authorized signing keys of the bootstrap entry are carried inside `system_manifest.entries[0]`, specifically as `entries[0].algorithm`, `entries[0].quorum`, and `entries[0].members[*]` (each member's composite component public keys), per `system-manifest/1` Section 7
- `system_root_fingerprint` MUST be derived from `system_manifest` exactly as defined in Section 8 of this specification, and MUST equal the bootstrap fingerprint of the system domain

No implementation MAY treat:

- a publication transaction id
- an account-creation transaction
- an account name
- a live resolver response
- a dashboard presentation
- any bootstrap entry member’s public keys taken in isolation, decoupled from the embedded manifest

as normatively equivalent to the embedded `system_manifest` unless a later public successor version defines that equivalence explicitly.

---

## 8. Exact root-fingerprint derivation

For `system-foundation/1`, the exact current root-fingerprint derivation is:

```text
system_root_fingerprint = SHA3-256( UTF-8( JCS( system_manifest ) ) )
```

where:

- `JCS` means RFC 8785 JSON Canonicalization Scheme over the parsed JSON value of `system_manifest` as defined in `system-manifest/1` Section 8
- `UTF-8` means UTF-8 encoding of the canonicalized string
- `SHA3-256` means SHA3-256 over those exact bytes
- the output representation MUST be lowercase hexadecimal without prefix
- the output MUST be exactly 64 hexadecimal characters

The exact `root_fingerprint_derivation` identifier under `/1` is:

```text
sha3-256-system-manifest-jcs-v1
```

If the declared `root_fingerprint_derivation` differs from `sha3-256-system-manifest-jcs-v1`, validation MUST fail.

If recomputation of `system_root_fingerprint` from the embedded `system_manifest` yields any different value, validation MUST fail.

The `system_root_fingerprint` derived in this section is the **bootstrap fingerprint** of the system domain. The current `system_root_fingerprint` of the system domain at any given time may differ from the bootstrap fingerprint if rotations have occurred under `system-manifest/1` Section 12; that current fingerprint is derived from the current manifest version and is not carried by this statement. A `system-foundation/1` statement attests exclusively to the bootstrap fingerprint.

---

## 9. Exact statement signature model

The current signature model under `/1` is one exact self-anchored bootstrap-quorum statement model.

That means:

- the statement is authorized by a **quorum** of the bootstrap entry's members, carried in `statement_signatures`: a non-empty JSON array of objects with exactly the two members `signer_member_kid` and `signature`, one per signing member; an element of any other shape is malformed and makes the statement fail
- each `signer_member_kid` MUST identify a member of `system_manifest.entries[0].members`; each `signature` MUST verify under that member's composite component public keys
- the statement is self-anchored only if at least `system_manifest.entries[0].quorum.k` **distinct** members produce verifying signatures over the canonical unsigned statement payload defined below
- the signature algorithm MUST be the exact algorithm identified by `system_manifest.entries[0].algorithm`; each member `signature` is the composite wire object `{ alg, mode, signatures[] }` and the verifier MUST validate it per `composite-signature/1` (AND over all components, fail-closed on the ML-DSA-65 component). The bootstrap root of the active CERTCRYPT System Domain is composite-signed by a quorum of its members.
- the counting rules of `system-manifest/1` Section 12.3 apply: duplicate `signer_member_kid` values count once; a signature not attributable to a bootstrap member never contributes to the threshold.

The canonical unsigned statement payload under `/1` is the exact JSON object containing:

- `foundation_profile_id`
- `foundation_statement_id`
- `system_id`
- `system_root_fingerprint`
- `system_manifest`
- `root_fingerprint_derivation`
- `system_domain_capacity_key_p256_b64`
- `system_domain_capacity_key_mldsa_b64`
- `published_rules_versions`
- `statement_issued_at`

with no additional members. The embedded `system_manifest` is a complete `system-manifest/1` JSON object; the unsigned statement payload includes it inline. The canonical serialization of the unsigned statement payload MUST be `UTF-8( JCS( payload ) )` under RFC 8785; because canonicalization is by RFC 8785 JCS (lexicographic member ordering), the listing order above is for human readability and does not affect the signed bytes.

`system_domain_capacity_key_p256_b64` and `system_domain_capacity_key_mldsa_b64` are part of the signed payload so that the system-domain Level-1 capacity key is **authenticated by the bootstrap quorum**, not merely co-published in the same JSON. An adversary who substitutes the Level-1 capacity key in a published statement, leaving the `statement_signatures` intact, MUST cause validation to fail: the substituted key changes the canonical payload, so no quorum of bootstrap-member signatures over the original payload verifies. This closes the substitution path by which a forged Level-1 key could otherwise authorize a fabricated `independence_proof` or capacity binding.

`publication_refs`, if present, MUST NOT affect signature validity.

If the signature does not verify, validation MUST fail.

`system-foundation/1` signs exactly one bootstrap manifest version. It does not sign, wrap, refresh, ratify, or republish successor manifest versions. A successor version is valid only if it is anchored to this bootstrap manifest through valid `system-manifest/1` rotations (Sections 12 and 13); under `/1` it never replaces the bootstrap fingerprint as the identity artifacts carry.

The bootstrap member private keys participate in two distinct normative operations under the active corpus, and only those two:

1. a quorum of at least `entries[0].quorum.k` distinct members MUST produce the `statement_signatures` of this `system-foundation/1` statement
2. a quorum of at least `entries[0].quorum.k` distinct members MAY produce the `predecessor_signatures` of the first rotation under `system-manifest/1` Section 12, if and when that first rotation occurs; those signatures are the in-manifest predecessor quorum for the rotation from `manifest_sequence = 0` to `manifest_sequence = 1`

These two operations are normatively distinct. The statement quorum and the successor-binding quorum are produced over different canonical payloads under different specifications, and neither MAY substitute for the other. A conforming implementation MUST NOT treat one as evidence of the other.

The bootstrap member private keys MUST NOT be used to produce any additional `system-foundation/1` statement signatures, and MUST NOT be used to authorize any rotation other than the first rotation from `manifest_sequence = 0`.

Retention and destruction of the bootstrap member private keys are governed by the following rule, applied per member:

- the bootstrap member private keys MUST be retained at least until either of the two terminating events below occurs
- **terminating event A**: the first `system-manifest/1` rotation from `manifest_sequence = 0` is produced under the rotation procedure of `system-manifest/1` Section 12.1; after the `predecessor_signatures` quorum of that first rotation has been produced and persisted, the bootstrap member private keys MUST be destroyed
- **terminating event B**: the deployment takes an explicit and irreversible decision not to rotate from `manifest_sequence = 0`; after that decision has been recorded under the deployment’s operational governance, the bootstrap member private keys MUST be destroyed

Destruction of the bootstrap member private keys MUST NOT be performed merely on the basis that the bootstrap statement has been signed and published. Destruction is a function of the rotation lifecycle, not of statement publication. Implementations MUST NOT collapse the two events into one rule. A deployment that destroys enough bootstrap member private keys to fall below the rotation quorum prematurely permanently forfeits the ability to perform the first rotation from `manifest_sequence = 0`; under `system-manifest/1`, that consequence is irreversible.

Implementations MAY consolidate the bootstrap statement ceremony and the first rotation, when scheduled, into a single physical ceremony, but MUST NOT treat the bootstrap statement signature as substitutable for the first in-manifest predecessor signature, nor vice versa.

---

## 10. Publication anchors

A conforming `system-foundation/1` statement MAY be published through one or more immutable publication layers.

Under the active public architecture, publication MAY use:

- `arweave.publication/1` (an optional publication profile, not part of the published corpus)

If a `publication_ref` is present and claims `arweave.publication/1`, it MUST
satisfy that publication profile. `arweave.publication/1` is not part of the
published corpus; since `publication_refs` are provenance and discovery aids
that MUST NOT affect signature validity (Section 6), no conformance outcome
defined by this specification depends on it.

Publication anchors MAY help:

- discover the statement
- audit its public-history presence
- confirm immutable publication lineage

Publication anchors MUST NOT:

- become the system root identifier by implication alone
- replace root-material validation
- replace statement-signature validation
- become required live dependencies for normative validation

No conforming verifier MAY require live Arweave access merely to validate a `system-foundation/1` statement whose contents are already locally available.

---

## 11. Offline validation model

A conforming verifier validating a `system-foundation/1` statement MUST be able to do so from a local copy supplied by any non-authoritative channel, including:

- a verification package
- a local cache
- a mirror
- direct file transport
- a previously retrieved immutable publication copy

The verifier MUST:

1. validate that the statement carries every required member and no member other than those of Section 6, and `foundation_profile_id = "system-foundation/1"`
2. validate `system_id`, and the formats of `foundation_statement_id` and `statement_issued_at` (Section 6)
3. validate `root_fingerprint_derivation = "sha3-256-system-manifest-jcs-v1"`
4. validate that the embedded `system_manifest` is a conforming bootstrap manifest version under `system-manifest/1` Section 13 and that `system_manifest.manifest_sequence = 0` and `length(system_manifest.entries) = 1`
5. recompute `system_root_fingerprint` from the embedded `system_manifest` under Section 8 of this specification and verify it matches the carried value
6. validate that `system_domain_capacity_key_p256_b64` and `system_domain_capacity_key_mldsa_b64` are both present and each decodes to the byte length required by its component algorithm under the composite profile carried at `system_manifest.entries[0].algorithm`
7. validate `statement_signatures` over the canonical unsigned statement payload — which includes the two `system_domain_capacity_key_*` members (Section 9): at least `system_manifest.entries[0].quorum.k` distinct members of `system_manifest.entries[0].members` MUST each have a verifying composite signature, under the algorithm carried at `system_manifest.entries[0].algorithm`, per the quorum rule of `system-manifest/1` Section 12.3
8. if `successor_binding_observations` is present, validate every element and compare them for equivocation (Section 6, `system-manifest/1` Section 12.5)
9. validate any claimed `publication_ref` only as optional provenance

`published_rules_versions` is not a validation step: it is metadata (Section 6).

If any required validation step fails, the foundation statement MUST be rejected.

Normative validation under this profile MUST NOT depend on:

- live CERTCRYPT infrastructure
- live Arweave retrieval
- a managed resolver
- a publication-indexing service

---

## 12. Interpretation boundary

A valid `system-foundation/1` statement MAY be used to:

- identify one exact CERTCRYPT root-material statement
- derive one exact `system_root_fingerprint`
- record, as metadata, the rules versions declared when the statement was produced
- support immutable public-history anchoring

A valid `system-foundation/1` statement MUST NOT be used to:

- prove truth
- prove `Independent`
- prove settlement
- endorse issuer claims semantically
- replace higher-layer verifier evaluation

---

## 13. Failure conditions

Validation under this profile MUST fail if:

- `foundation_profile_id` differs from `"system-foundation/1"`
- the statement carries a member not listed in Section 6
- `foundation_statement_id` is absent or does not have the format of Section 6
- `statement_issued_at` is absent or is not an RFC 3339 UTC timestamp with the `Z` designator
- `system_id` is absent or differs from the embedded manifest's `system_id`
- `system_manifest` is absent, is not a conforming `system-manifest/1` instance, or fails any check of `system-manifest/1` Section 13
- the embedded `system_manifest` has `manifest_sequence` other than `0`
- the embedded `system_manifest` has `entries` of length other than `1`
- `entries[0].algorithm` is absent or unsupported by the verifier
- `entries[0].quorum` is malformed (not `2 ≤ k ≤ n`), `entries[0].members` length is not `n`, or any member component public key cannot be decoded exactly
- `root_fingerprint_derivation` differs from `"sha3-256-system-manifest-jcs-v1"`
- `system_root_fingerprint` does not match recomputation from the embedded `system_manifest`
- `system_domain_capacity_key_p256_b64` or `system_domain_capacity_key_mldsa_b64` is absent, or either fails to decode to the byte length required by its component algorithm under the bootstrap entry's composite profile
- an element of `successor_binding_observations` is malformed, does not name the bootstrap entry as predecessor, or is not authorized by the bootstrap quorum, or two elements establish equivocation (`system-manifest/1` Section 12.5)
- `statement_signatures` does not reach the bootstrap entry's `quorum.k` distinct verifying members under the algorithm declared by the bootstrap entry of the embedded manifest, over the canonical unsigned statement payload that includes the two `system_domain_capacity_key_*` members
- a publication anchor is treated as a substitute for statement validation
- live retrieval is required to establish meaning of otherwise locally available statement contents

No partial success state MAY substitute for failed required validation.

---

## 14. Conformance

An implementation conforms to `system-foundation/1` if and only if:

- it constructs or validates the exact statement model defined here
- it derives `system_root_fingerprint` exactly as defined here
- it validates the exact statement signature model defined here
- it preserves offline validation independence from live publication infrastructure
- it does not elevate immutable publication into semantic or trust authority

---

## 15. One-line summary

`system-foundation/1` defines one exact canonical bootstrap artifact by which CERTCRYPT root material MAY be published immutably while remaining offline-verifiable under public rules.

---

## 16. Versioning & extensibility

This `/1` specification defines the current active public contract for `system-foundation/1`.

Once frozen, this version MUST NOT be modified in place in any way, including editorial, typographic or clarifying changes that would leave its normative meaning unchanged. Any change MUST be published under a new version identifier.

---

## 17. References

- CERTCRYPT Specifications
    - [security-model/1 — CERTCRYPT Security Model](../../security-model/1/index.md)
    - [system-manifest/1 — CERTCRYPT System Manifest](../../system-manifest/1/index.md)
    - [system-domain/1 — CERTCRYPT System Domain](../../system-domain/1/index.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../rules-domain/1/index.md)
    - CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol
    - CCSP/1 — CERTCRYPT Certificate Serialization Protocol
    - CCVP/1 — CERTCRYPT Consistency Verification Protocol
    - [composite-signature/1 — CERTCRYPT Composite Signature Profile](../../composite-signature/1/index.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
    - [RFC 4648 — The Base16, Base32, and Base64 Data Encodings](https://www.rfc-editor.org/rfc/rfc4648)
    - [RFC 8785 — JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785)

---

**End of system-foundation/1**
