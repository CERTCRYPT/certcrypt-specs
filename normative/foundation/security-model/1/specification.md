# CERTCRYPT Security Model Specification (security-model/1)

**Identifier:** `security-model/1`

**Label:** Security Model v1

**Type:** Foundation Specification

**Status:** Frozen

**Layer:** Layer 0 — Foundation

**Depends on:** None *(foundational security framework)*

**Naming convention:**  
`security-model/1` is the formal identifier.  
Security Model v1 is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.

**Audience:** Protocol designers, specification authors, implementers, auditors, governance bodies, legal and forensic analysts

**Purpose:** Define the foundational security invariants, threat boundaries, guarantees, interpretation limits, and failure semantics that constrain all CERTCRYPT protocols, profiles, models, ecosystem documents, governance texts, and implementations.

**Intended use:** `security-model/1` defines the axiomatic security boundary of the current leaf-based CERTCRYPT architecture. It governs the interpretation of both `Issued` and `Independent`.

**Scope:** Defines foundational security invariants, threat boundaries, interpretation constraints, and evolution rules applicable to the entire CERTCRYPT architecture.

**Non-goals:** `security-model/1` does not define protocol message formats, canonicalization algorithms, proof field layouts, submission-set transport, settlement adapter mechanics, capacity issuance workflows, governance procedures, economic plans, legal validity, or implementation deployment guidance.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 0. Foundational security framework

`security-model/1` defines the foundational security framework of CERTCRYPT.

It is not a protocol, not a profile, not a settlement adapter, not a managed-service policy, and not a product operating manual.

It defines the immutable security boundary within which all those components must operate.

All other CERTCRYPT specifications:

- MUST be interpreted within the limits defined by this model
- MUST NOT expand semantic meaning beyond those limits
- MUST NOT introduce guarantees inconsistent with its invariants
- MUST NOT reintroduce authority through convenience infrastructure
- MUST be sufficient, together with other applicable public specifications, to determine conforming behavior without reliance on undisclosed architectural intent

The Security Model is trans-layer and foundational.

It applies to:

- issuer-local base certificate issuance semantics
- `Issued` verification semantics
- `Independent` verification semantics
- leaf-based structural integrity
- capacity-bound and settlement-bound independence
- offline-verifiable proof artifacts
- resolver and managed-service boundaries
- implementation behavior
- ecosystem representation

No specification at any layer MAY weaken, override, reinterpret, or selectively apply the constraints defined in `security-model/1`.

The Security Model defines necessary but not sufficient conditions for valid certificate interpretation within CERTCRYPT.

---

## 1. Background & rationale

CERTCRYPT is designed to operate in a hostile, long-lived environment where:

- infrastructure may disappear
- issuers may change
- governance may evolve
- ecosystems may fork
- legal interpretation may shift
- economic pressure may distort semantics

Digital certification systems usually fail through semantic overreach, hidden dependencies, fallback trust, or retroactive reinterpretation.

The current CERTCRYPT architecture adds a second major risk:

- structural independence may be misrepresented as authority, truth, or live-service status

`security-model/1` exists to prevent those failures.

It defines what CERTCRYPT is allowed to mean and, equally importantly, what it is not allowed to mean.

---

## 2. Scope

This specification defines the foundational security properties of CERTCRYPT.

It applies to:

- all certificates governed by `security-model/1`
- all protocol specifications
- all subject and delivery profiles
- all models, including `independence.proof`
- all ecosystem and governance documents
- all conforming implementations

This specification:

- MUST constrain all higher-layer specifications
- MUST NOT be overridden by governance, branding, economics, or implementation convenience
- MUST be interpreted as a trans-layer normative authority
- MUST constrain verifier UX, widget semantics, hosted verification presentation, and managed-service framing with the same force as protocol behavior

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are to be interpreted as described in RFC 8174.

For the purposes of this specification:

- **Issued** means a certificate validly emitted by the issuer under the applicable rules.
- **Independent** means a structural state reached only when issuance-time participation, valid leaf inclusion, valid CERTCRYPT capacity, valid settlement with sufficient finality, and offline-verifiable proof conditions all hold under public rules.
- CERTCRYPT MUST NOT be semantically reducible to hashing, anchoring, timestamping, or blockchain-proof publication alone.
- Sufficient settlement finality MUST be explicitly parameterized by the applicable rules domain for each permitted settlement mode and MUST NOT be left to discretionary operational judgment.
- Operational capacity availability, top-up visibility, or managed status views MUST NOT be interpreted as semantically equivalent to attributable CERTCRYPT capacity authorization plus settlement-backed consumption under the CERTCRYPT System Domain.
- Standard `Independent` verification MUST validate settlement, settlement-bound capacity consumption, and sufficient finality from canonical offline proof material, without requiring direct live validation of balances, supply, or equivalent live economic substrate.
- **Security Meaning Boundary** means the explicit limit of what CERTCRYPT guarantees and what it does not guarantee.
- **Leaf Closure** means the point after which the leaf contents, ordering, and committed material are no longer mutable for the purpose of proving `Independent`.
- **Managed Layer** means any optional retrieval, indexing, delivery, or convenience interface built on top of the core architecture.
- **Retroactive Effect** means any change that alters the interpretation, validity, or meaning of a certificate after issuance.

---

## 4. Design principles

`security-model/1` is built on the following principles:

- **Zero-data by design:** The architecture MUST avoid dependence on retained documents, identities, or operational history as a condition of validity.
- **Proof without data custody:** Verification MUST rely on certificates, public rules, proof artifacts where applicable, and, when the verifier compares it, original material the verifier supplies, not on platform-held data or internal systems.
- **Unlinkability:** The system MUST avoid introducing stable references that enable cross-certificate subject correlation or reconstructable subject activity beyond what public rules explicitly require.
- **Deterministic verification:** Given the same inputs and the same rules, conforming verifiers MUST converge on the same result.
- **Institutional independence:** Valid verification and Proof of Independence MUST NOT depend on the continued existence of an issuer, operator, or managed CERTCRYPT service.
- **Infrastructure neutrality:** Normative meaning MUST remain stable across runtimes, hosts, providers, chains, publication layers, and deployment models.
- **Interpretation boundaries:** CERTCRYPT preserves verifiability under formal rules. It does not determine truth, semantic validity, legal meaning, or institutional endorsement.

CERTCRYPT does not retain history as a normative requirement.

Public history MAY emerge from external publication layers, but such layers are optional, non-authoritative, and not required for conforming verification.

When such layers are used, they MAY support public transparency, including economic transparency, without becoming the source of validity.

---

## 5. Normative authority

This specification is the foundational normative authority of CERTCRYPT.

In case of conflict, `security-model/1` MUST prevail.

---

## 6. Foundational security boundary

The foundational security boundary of CERTCRYPT is this:

1. CERTCRYPT does not emit certificates.
2. The issuer emits base certificates.
3. Public observable certificate states are limited to `Issued` and `Independent`.
4. `Independent` is not an authority claim, but a structural state under public rules.
5. `Independent` requires all of:
   - issuance-time participation in the independence flow
   - valid leaf structure
   - immutable post-closure leaf semantics
   - valid CERTCRYPT capacity
   - valid settlement with sufficient finality
   - offline-verifiable proof material
   - correct cross-layer binding between issuance-time participation reference, leaf path, and proof path under public rules
6. CERTCRYPT may participate in producing `Independent`, but MUST NOT become a live verification authority.
7. Verification of both `Issued` and `Independent` MUST remain reproducible without live CERTCRYPT authority.
8. Managed services and resolvers MAY exist, but MUST remain optional and non-authoritative.
9. Canonicalization, parsing, and version interpretation MUST be strict enough to prevent ambiguous verification.
10. Verification artifacts MUST resist cross-leaf, cross-issuer, and cross-version splicing.
11. Public claims of `Independent` MUST be interpreted as claims under the attributed CERTCRYPT System Domain, not as generic system-independent trust categories.
12. No external system that only provides hashing, anchoring, timestamping, or equivalent publication semantics MAY be treated as sufficient to reproduce a valid `Independent` state.

---

## 7. Interpretation boundaries

This specification:

- MUST NOT be interpreted as asserting legal validity
- MUST NOT be interpreted as asserting factual truth
- MUST NOT be interpreted as granting trust
- MUST NOT be interpreted as conferring ownership
- MUST NOT be interpreted as institutional endorsement
- MUST NOT be interpreted as making payment equivalent to truth or validity
- MUST NOT be interpreted as making managed-service availability equivalent to verification
- MUST NOT be interpreted as making branding, compliance status, trademark usage, or policy-participation claims equivalent to proof, validity, or CERTCRYPT-domain conformance

`Independent` means structural independence only.

Canonicalization and commitment protocols can provide non-malleable structural binding, but they do not by themselves define the meaning of participation in `Independent`.

Anchoring, timestamping, or external publication can reinforce auditability or `non-reversibility`, but they MUST NOT be interpreted as ontologically sufficient to produce `Independent`.

That meaning exists only when issuance-time reference material, leaf-level semantics, and proof semantics are aligned under the applicable public rules.

It also means domain-attributed structural independence only.

It does not mean:

- content truth
- issuer legitimacy
- legal enforceability
- institutional endorsement
- higher semantic correctness
- present online availability of any CERTCRYPT-operated service
- generic portability across non-equivalent external systems

### 7.1 Anti-clone boundary

The distinction between a valid CERTCRYPT independence path and an approximation of one does not rest on commodity cryptography, commodity anchoring, commodity storage, or publication alone.

It rests on making invalid any artifact set that only appears similar to a valid CERTCRYPT independence path while omitting one or more required structural conditions.

Therefore, a system MUST NOT be treated as semantically equivalent to CERTCRYPT if it permits any of the following:

- retroactive production of an apparently valid independence result without issuance-time participation
- derivation of `Independent` from hashing, anchoring, publication, or receipt material alone
- verifier dependence on a live issuer or live provider as a required validation dependency
- acceptance of reusable, ambiguous, or externally reconstructed capacity evidence
- replay or recontextualization of proof material across leaves or settlement contexts
- acceptance of visually similar or partially compatible proof paths as if they were exact CERTCRYPT semantics

The verifier boundary, proof boundary, and public rules MUST together make such approximations fail closed.

---

## 8. Security properties required by the architecture

All conforming CERTCRYPT specifications MUST preserve at least these properties:

1. issuer-local certificate issuance
2. deterministic and fail-closed verification
3. no retroactive promotion from non-independent issuance into `Independent`
4. leaf-first structural integrity
5. immutable leaf semantics after closure
6. strict versioning and unambiguous canonicalization
7. anti-splicing of proof and verification artifacts
8. valid capacity as a condition of structural independence
9. valid settlement with sufficient finality as a condition of structural independence
10. offline-verifiable proof of independence
11. non-replay of structural independence results
12. verifiable attribution to the CERTCRYPT System Domain
13. namespace and authorization-scope discipline
14. zero-data and stateless core behavior
15. no authority fallback through APIs, resolvers, dashboards, or signatures
16. minimization of avoidable side-channel leakage
17. no semantic dependence on displaced operational state outside the core
18. no semantic collapse of CERTCRYPT capacity into generic prepaid-service balance semantics
19. no economic truth derived from manipulated or node-local capacity state outside publicly attributable authorization and settlement semantics
20. no successful `Independent` result derived from partial, fallback, downgraded, or heuristically substituted verification paths
21. no conforming `Independent` verification claim without full execution of the mandatory standard offline verification baseline
22. no conforming standard verification path that requires direct online inspection of balances, supply, or equivalent live economic substrate when canonical offline proof material should suffice under public rules
23. no essential CERTCRYPT conformance distinction that exists only in undisclosed material and cannot be reproduced from applicable public specifications and public verification tooling
24. no preview, demo, compatibility, or partial verification mode represented as semantically equivalent to conforming `Independent` verification
25. no conforming verifier, widget, UI, or hosted verification surface may present `Independent` as institutional trust, governance endorsement, or semantic truth of issuer declarations
26. no conforming operating model may turn managed retrieval, resolver mediation, or hosted verification into the de facto required path for ordinary `Independent` verification where the public offline path is expected to suffice

Stateless core behavior does not mean that no operational state may exist anywhere in the surrounding ecosystem.

It means that:

- no persistent authoritative core state is required for validity
- no internal CERTCRYPT historical memory is required for verification
- no displaced cache, queue, log, node journal, or managed helper state may become a substitute source of semantic truth

---

## 9. Relationship to other specifications

The CERTCRYPT Security Model v1 consists of the following normative components:

- [Security invariants](security-invariants.md)
- [Threat model](threat-model.md)
- [Invariant-Threat Mapping](invariant-threat-mapping.md)
- [Security guarantees and non-claims](security-guarantees-and-non-claims.md)
- [Failure modes and safe failure](failure-modes-and-safe-failure.md)
- [Evolution and freeze policy](evolution-and-freeze-policy.md)

Each component MUST be interpreted as part of this specification.

The following documents are informative:

- [Index](index.md)
- [Overview](overview.md)

---

## 10. Layer architecture

Within the CERTCRYPT layered architecture:

- Layer 0 - Foundation: `security-model/1`
- Layer 1 - Protocols
- Layer 2 - Profiles
- Layer 3 - Models
- Layer 4 - Ecosystem
- Layer 5 - Governance

All layers above Layer 0 MUST conform to this specification.

---

## 11. Adversarial security review

*This section is informative.* Conformance to this corpus is established by the normative requirements of each specification and by the conformance vectors, never by the fact that a review took place.

---

## 12. Versioning & extensibility

This `/1` specification defines the current active public contract for `security-model/1`.

Once frozen, this version MUST NOT be modified in place in any way, including editorial, typographic or clarifying changes that would leave its normative meaning unchanged. Any change MUST be published under a new version identifier.

---

## 13. References

- CERTCRYPT Specifications
    - [system-domain/1 — CERTCRYPT System Domain](../../system-domain/1/index.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../rules-domain/1/index.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)

---

**End of security-model/1**
