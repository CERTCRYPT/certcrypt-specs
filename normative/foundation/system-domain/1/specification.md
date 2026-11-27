# CERTCRYPT System Domain Specification (system-domain/1)

**Identifier:** `system-domain/1`  

**Label:** CERTCRYPT System Domain Specification (system-domain/1)  

**Type:** Foundation Specification

**Status:** Frozen

**Layer:** Layer 0 — Foundation

**Depends on:** See References *(active normative dependencies are listed below)*  

**Naming convention:**  
`system-domain/1` is the formal identifier.  
CERTCRYPT System Domain Specification (system-domain/1) is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.  

**Audience:** Protocol designers, specification authors, implementers, auditors  

**Purpose:** Define the normative semantics, constraints, and interpretation boundary of system-domain/1 within the active CERTCRYPT public architecture.  

**Intended use:** system-domain/1 is intended to be the authoritative public specification used by conforming implementers, verifiers, auditors, and ecosystem tooling when handling this artifact or behavior.  

**Scope:** Defines the active normative behavior of system-domain/1; adjacent protocols, profiles, operational tooling, and product behavior remain out of scope except where explicitly referenced.  

**Non-goals:** system-domain/1 does not prove truth, semantic validity, legal validity, or live service authority by itself, and MUST NOT be interpreted as a substitute for cryptographic authenticity, Proof of Independence, or managed-service behavior outside its own normative scope.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale
This specification defines the CERTCRYPT system-domain model.

The system domain establishes the identity and exact rule universe under which CERTCRYPT artifacts are interpreted, evaluated, and accepted or rejected under public rules.

This specification operates within the CERTCRYPT model of Proof of Independence.

It defines:

- what the CERTCRYPT System Domain is
- how an exact foundation artifact MAY carry the current bootstrap root material
- how system attribution MUST be established
- how the rules domain MUST be selected
- what root material MUST anchor system attribution
- what system-domain binding enables and what it MUST NOT be interpreted as

It does not define:

- certificate issuance semantics
- submission-set semantics
- capacity authorization, locking, or consumption semantics
- settlement execution semantics
- independence semantics
- verification-package transport semantics

Those concerns belong to separate specifications.

---

## 2. Scope

This specification applies to all systems, implementations, SDKs, verifiers, and artifacts that:

- reference or imply a `system_id`
- claim to belong to the CERTCRYPT System Domain
- select or apply CERTCRYPT public rules
- evaluate CERTCRYPT proofs or verification artifacts

Any implementation that interprets CERTCRYPT artifacts MUST conform to this specification for system attribution and system-domain rule selection.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

---

## 4. Design principles

`system-domain/1` is designed around the following principles:

- **Identity, not authority:** The system domain establishes identity and rule attribution only. It MUST NOT be interpreted as a source of truth, semantic validation, or institutional authority.
- **Deterministic attribution:** System attribution and rules-domain selection MUST be exact, reproducible, and fail closed. Heuristic matching, fallback naming, and clone-compatible interpretation are forbidden.
- **Separation from proof:** System-domain attribution does not create `Issued`, does not create `Independent`, and does not substitute for settlement, capacity, or proof validation.
- **Offline verifiability:** A conforming verifier MUST be able to establish system attribution and applicable rules-domain context from public material without requiring live CERTCRYPT infrastructure.
- **Anti-spoofing boundary:** The system domain MUST distinguish authentic CERTCRYPT attribution from external, cloned, mixed-domain, or cosmetically similar systems without relying on branding or transport context.

---

## 5. Relationship to proof of Independence

The system domain does not create, finalize, or declare independence.

Independence is derived under the applicable public rules from valid settlement, valid CERTCRYPT capacity consumption, and the exact leaf commitment, as defined by the relevant specifications.

Within that model:

- the system domain identifies which system is being evaluated
- the rules domain identifies which exact public rules govern that evaluation
- the proof model determines whether a valid independence result exists under those rules

Public claims of independence evaluated through this attribution model are therefore claims of `Independent` under the CERTCRYPT System Domain, not generic trust or portability claims detached from domain attribution.

System attribution MUST NOT be interpreted as:

- semantic correctness
- partial or implied independence
- successful fixation
- acceptance of issuer-declared properties

---

## 6. Definitions

### 6.1 System domain

The **system domain** is the unique identity-and-rules boundary within which CERTCRYPT artifacts are interpreted.

A system domain includes:

- one exact system identity
- one exact attribution boundary
- one exact root-material basis for system attribution
- one or more public rules domains that belong to that system identity

### 6.2 Rules domain

The **rules domain** is the exact versioned public ruleset that governs interpretation of artifacts within a system domain.

The rules domain MUST determine, where applicable:

- artifact syntax and canonicalization
- validation requirements
- settlement and finality semantics
- capacity semantics
- proof semantics

The rules domain MUST be selected deterministically and MUST NOT be inferred heuristically.

Compatible, successor, fallback, or parser-preferred rule sets MUST NOT be used as substitutes unless public rules explicitly define them as equivalent for the specific evaluation path.

### 6.3 System attribution

**System attribution** is the process by which an implementation determines that an artifact belongs to the CERTCRYPT System Domain and that the correct rules domain is being applied.

### 6.4 Root material

**Root material** is the verifiable material by which the CERTCRYPT System Domain is anchored.

Under the active corpus, root material is declared as a `system-manifest/1` instance: a closed identity-only artifact whose entries catalog the append-only chain of public keys authorized to sign on behalf of the system domain across time. The bootstrap manifest version (`manifest_sequence = 0`) is embedded inside one `system-foundation/1` statement; successor manifest versions are produced by rotation under `system-manifest/1` Section 12 and change who may authorize the next rotation, not the attribution of artifacts (`system-manifest/1` Section 14).

Public rules MAY accept additional verifiable attribution primitives only where explicitly defined; under `/1`, the `system-manifest/1` model is the exact root-material model.

### 6.5 System-domain root identifier

The **system-domain root identifier** is the exact canonical identifier of the root material instance by which the CERTCRYPT System Domain is attributed.

Under the active corpus, the root identifier is the `system_root_fingerprint` of a `system-manifest/1` instance, derived as `SHA3-256( UTF-8( JCS( manifest ) ) )` per `system-manifest/1` Section 10. The output is a 64-character lowercase hexadecimal string.

The system domain has at any given time:

- one **bootstrap fingerprint**, equal to the digest of the bootstrap manifest version (`manifest_sequence = 0`), declared by the `system-foundation/1` statement and invariant for the lifetime of the system domain
- one **current fingerprint**, equal to the digest of the current manifest version (the most recent manifest version produced by valid rotation under `system-manifest/1` Section 12), which equals the bootstrap fingerprint when no rotation has occurred and otherwise reflects the latest valid rotation

Where this specification refers to `system_root_fingerprint` without qualification, it means the **bootstrap fingerprint**. It is also the only root identifier an artifact carries under `/1`: the current fingerprint identifies a manifest version, never an artifact's system domain (`system-manifest/1` Section 14). Operational artifacts are not signed by manifest entries: they are signed by the Level-1 capacity key of the bootstrap statement (`system-manifest/1` Section 15).

### 6.6 Foundation statement

A **foundation statement** is the canonical bootstrap artifact by which CERTCRYPT root material MAY be declared, published immutably, cached, transported, and validated under public rules.

For the active public architecture, the applicable foundation-statement profile is:

```text
system-foundation/1
```

---

## 7. System identity

### 7.1 `system_id`

Every CERTCRYPT artifact whose meaning depends on system attribution MUST include or deterministically imply a `system_id`.

The exact `system_id` of a registered system domain is declared by its registry
entry (Section 16), never by this specification. For the active CERTCRYPT public
architecture it is declared in [registry/certcrypt/index.md](registry/certcrypt/index.md).

The `system_id` MUST:

- identify the CERTCRYPT System Domain unambiguously
- remain stable across conforming implementations
- be bound to valid root material under public rules

### 7.2 `system_id` is not sufficient alone

A matching `system_id` string is not sufficient proof of system attribution.

A verifier MUST NOT accept an artifact as belonging to a system domain solely because it contains or implies that domain's `system_id`. The identifier is a claim, not an attribution: only root material validates it.

Valid attribution requires successful binding to the applicable root material and deterministic rule selection under public rules.

Public system-domain conformance MUST be decidable from applicable public specifications and verifier behavior.

No implementation MAY claim CERTCRYPT-domain equivalence merely by copying field shapes, naming conventions, transport wrappers, or superficially similar outputs if public attribution, root binding, and applicable public rules do not validate that claim.

No implementation MAY establish or imply CERTCRYPT-domain equivalence through:

- branding
- trademark usage
- policy-participation claims
- compatibility marketing
- dashboard or hosted-service representation

if public attribution, root binding, and applicable public rules do not validate that claim.

---

## 8. Rules-domain binding

Any artifact whose semantics depend on a rules domain MUST be interpreted under one and only one exact rules domain within the CERTCRYPT System Domain.

That rules domain MUST be:

- explicitly present, or
- deterministically derivable without heuristic choice

An implementation MUST reject evaluation if:

- multiple rule domains could validly apply
- rule selection depends on fallback behavior
- rule selection depends on parser discretion
- rule selection depends on managed-service preference

System-domain attribution and rules-domain selection MUST remain consistent across all related artifacts in the same evaluation context.

Cross-artifact evaluation MUST fail if related artifacts require different system domains or different non-equivalent rules domains.

---

## 9. Root material requirements

A valid CERTCRYPT System Domain MUST be anchored to verifiable root material.

That root material MUST:

- be deterministically derivable or otherwise obtainable without reliance on discretionary authority under public rules
- uniquely identify the CERTCRYPT System Domain
- expose or deterministically imply one exact system-domain root identifier
- allow rejection of cloned, forked, or spoofed systems
- remain usable without requiring a live CERTCRYPT authority

That root material MUST NOT:

- act as a semantic authority
- override proof semantics
- override settlement semantics
- replace artifact validation
- create or imply independence on its own

If root material cannot be validated or derived deterministically, system attribution MUST fail.

System-domain attribution MUST NOT influence the outcome of proof validation beyond determining the correct rules domain and the correct system-attribution context under public rules.

When a `system-foundation/1` statement is supplied, the verifier MUST validate that statement under its own profile rather than treating it as an informal hint.

---

## 10. Artifact binding requirements

Any artifact that depends on system attribution MUST bind to the CERTCRYPT System Domain in a way that allows deterministic evaluation under public rules.

This includes, where applicable:

- `submission-set`
- `capacity_commitment`
- `independence_proof`
- `verification_package`
- any settlement- or capacity-dependent supporting artifact

Artifacts from different system domains MUST NOT be mixed in a single evaluation path.

An implementation MUST reject any context in which system-domain mixing would allow:

- proof splicing
- cross-system replay
- cloned-system acceptance
- heuristic interpretation of external artifacts as CERTCRYPT artifacts

---

## 11. Deterministic validation model

A verifier MUST use the system domain to:

- establish the exact system identity being evaluated
- select the exact applicable rules domain
- obtain or derive the correct root attribution basis
- reject alternative or fallback interpretations

Validation MUST fail if system attribution is:

- ambiguous
- unverifiable
- spoofed
- dependent on live discretionary responses
- dependent on non-public interpretation logic

The system domain MUST support offline-verifiable attribution.

Live APIs, resolvers, dashboards, or managed services MAY assist with artifact discovery or operational convenience, but MUST NOT be required to determine the system domain or the applicable rules domain.

If a verifier receives a locally available `system-foundation/1` statement, it MUST be able to validate that statement offline without requiring live retrieval from Arweave, CERTCRYPT, or any managed resolver.

---

## 12. Managed services and resolver boundaries

Managed services, mirrors, resolvers, dashboards, and operational endpoints MAY expose convenience views of system-domain material.

They MUST remain optional and non-authoritative.

Managed services MUST NOT be required to obtain system-domain root material.

No conforming implementation MAY treat a live service response as stronger system-domain evidence than the root material and public rules.

A managed-service response MUST NOT:

- redefine system attribution
- select a different rules domain by policy preference
- override a conflicting offline-verifiable result
- introduce a new authority layer for system identity

If a live service response conflicts with offline-verifiable system-domain evidence, the offline-verifiable evidence MUST prevail.

Immutable publication layers such as `arweave.publication/1` (an optional publication profile, not part of the published corpus) MAY anchor a valid foundation statement.

They MUST remain optional and non-authoritative for normative system-domain validation.

---

## 13. Forks, clones, and external systems

Any system that:

- reuses the document structures of a registered system domain
- copies its field names
- reuses a registered `system_id`
- imitates its artifact shapes

without valid root-material attribution to that domain MUST be treated as a distinct external system.

Such systems:

- MUST NOT be considered equivalent to CERTCRYPT
- MUST NOT share CERTCRYPT independence semantics
- MUST NOT be accepted as valid CERTCRYPT system-domain artifacts

Explicit equivalence across distinct systems MUST NOT be assumed.

It MAY exist only if public rules define it explicitly and verifiably.

---

## 14. Failure conditions

System-domain validation MUST fail if:

- root material cannot be validated
- root material cannot be deterministically derived
- system attribution is ambiguous
- `system_id` is spoofed or unverifiable
- the rules domain cannot be determined exactly
- multiple non-equivalent rules domains could apply
- system-domain mixing is detected across related artifacts
- live service dependency is required to establish attribution

Failure to establish the system domain MUST be treated as a validation failure, not as a recoverable fallback condition.

---

## 15. Security properties

A conforming `system-domain/1` model MUST preserve:

1. deterministic system attribution
2. deterministic rules-domain selection
3. separation between identity and truth
4. separation between attribution and independence
5. resistance to cloned-system acceptance
6. resistance to cross-domain replay and splicing
7. compatibility with offline verification
8. no authority fallback through APIs, resolvers, or managed services
9. public decidability of non-conformance for systems that are only superficially “compatible enough”

---

## 16. Registered system domains

This specification defines the generic `system-domain/1` model. It does not
define the concrete root material, identifier, or bootstrap of any specific
system domain.

Concrete system domains are published as registry entries under
[system-domain/1/registry/](./registry/index.md). Each entry defines exactly one
`system_id` and provides the bootstrap parameters this specification's Sections 7
and 16.1 require for that domain.

The registry is the single canonical source of truth for the parameters of any
concrete system domain. Implementers MUST NOT infer them from this generic
specification, from defaults, or from any source other than the registry entry
whose `system_id` exactly matches the artifact under evaluation.

For the active CERTCRYPT public architecture, the registered system domain is:

- [`certcrypt`](registry/certcrypt/index.md)

Only registry entries listed in this section are registered under the active
corpus. Any unlisted `system_id` MUST NOT be accepted as a CERTCRYPT system
domain, and is a distinct external system under Section 13.

### 16.1 Bootstrap resolution order

For the active public bootstrap, a conforming verifier MUST resolve attribution in the following order:

1. determine one exact `rules_version`
2. resolve the published bootstrap mapping of the claimed system domain for that `rules_version`, from its registry entry
3. validate that `system_id` equals the `system_id` of the registered system domain being claimed
4. if a `system-foundation/1` statement is supplied, validate it under `system-foundation/1`
5. derive or obtain one exact `system_root_fingerprint` from the artifact under evaluation
6. accept system-domain attribution if and only if the carried or implied `system_root_fingerprint` equals the published bootstrap fingerprint of the system domain exactly (lowercase 64-character hexadecimal, byte-for-byte equal), and no equivocation evidence held by the verifier implicates the bootstrap manifest version (`system-manifest/1` Section 12.5)
7. reject if step 6 does not hold, or if any earlier step yields ambiguity, mismatch, or clone-compatible interpretation

This bootstrap is sufficient to break the circular dependency between system-domain attribution and rules-domain selection for the currently published ruleset. It also survives rotation unchanged: a rotation under `system-manifest/1` Section 12 changes neither the bootstrap fingerprint nor the Level-1 capacity key, so no verifier has to follow the manifest chain to keep attributing artifacts.

### 16.2 Future root rotation under `system-manifest/1`

Future root rotation under the CERTCRYPT System Domain MUST be expressed through `system-manifest/1`. There is no separate equivalence-statement profile under the active corpus; the canonical mechanism for rotation is the in-manifest predecessor quorum authorization defined by `system-manifest/1` Section 12.

A conforming rotation MUST:

- be performed under the rotation procedure of `system-manifest/1` Section 12.1, producing one exact new manifest version with `manifest_sequence = predecessor.manifest_sequence + 1`
- be authorized exclusively by a quorum of the immediate predecessor entry's members, each producing a composite signature over the canonical successor-binding payload of `system-manifest/1` Section 9, under the quorum rule of `system-manifest/1` Section 12.3
- bind the new entry to the exact predecessor manifest fingerprint and sequence, exactly as defined by `system-manifest/1` Section 7.9

A new manifest version MAY be published through `arweave.publication/1` (an optional publication profile, not part of the published corpus) or any other publication transport. Publication alone is not sufficient without a valid in-manifest predecessor quorum authorization and full conformance to `system-manifest/1` Section 13.

A rotation does not change the attribution of artifacts. Every artifact carries the bootstrap fingerprint, and no verifier MAY accept the digest of a later manifest version as an artifact's `system_root_fingerprint` (`system-manifest/1` Section 14). The rotation's only verifier-visible consequence is the successor-binding observation it produces, which a verifier holding the bootstrap statement validates and compares for equivocation (`system-manifest/1` Section 12.5).

The bootstrap fingerprint of the system domain is invariant across all rotations. Successor manifest versions add entries; they never replace or rewrite the bootstrap entry, and they never alter the bootstrap fingerprint. The current fingerprint of the system domain changes with each rotation and identifies a manifest version, not the system domain.

---

## 17. Privacy and data minimization

System-domain attribution MUST NOT require:

- original certified material
- issuer private data
- semantic interpretation of leaf contents
- internal CERTCRYPT databases

System-domain validation MUST remain compatible with the zero-data architecture.

---

## 18. Conformance

An implementation conforms to `system-domain/1` if and only if:

- it establishes CERTCRYPT system attribution deterministically
- it binds artifacts to the correct system domain
- it selects the exact applicable rules domain without heuristic fallback
- it rejects cloned, spoofed, mixed-domain, or ambiguous contexts
- it does not treat system attribution as proof of truth, validity, or independence
- it does not require live CERTCRYPT infrastructure to establish system attribution

---

## 19. Final normative statement

The CERTCRYPT System Domain defines the identity boundary and exact rules-domain context under which CERTCRYPT artifacts are interpreted. It enables deterministic attribution and exact rule selection without acting as a source of truth, semantic authority, or independence. A valid CERTCRYPT artifact MUST therefore be attributable to the CERTCRYPT System Domain through verifiable root material and the applicable public rules, not through naming, formatting, transport context, or live-service assertion.

---

## 20. Versioning & extensibility

This `/1` specification defines the current active public contract for `system-domain/1`.

Once frozen, this version MUST NOT be modified in place in any way, including editorial, typographic or clarifying changes that would leave its normative meaning unchanged. Any change MUST be published under a new version identifier.

---

## 21. References

- CERTCRYPT Specifications
    - [security-model/1 — CERTCRYPT Security Model](../../security-model/1/index.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../rules-domain/1/index.md)
    - [system-foundation/1 — CERTCRYPT System Foundation](../../system-foundation/1/index.md)
    - [system-manifest/1 — CERTCRYPT System Manifest](../../system-manifest/1/index.md)
    - CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol
    - CCSP/1 — CERTCRYPT Certificate Serialization Protocol
    - CCVP/1 — CERTCRYPT Consistency Verification Protocol
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)

---

**End of system-domain/1**
