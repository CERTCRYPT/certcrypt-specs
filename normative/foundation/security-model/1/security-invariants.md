# CERTCRYPT Security Model - Invariants (security-model/1)

**Identifier:** `security-model/1 - Invariants`

**Label:** Security Model v1 - Invariants

**Type:** Foundation Component

**Status:** Frozen

**Layer:** Layer 0 - Foundation

**Depends on:**
- [security-model/1 - CERTCRYPT Security Model Specification](specification.md)

**Audience:** Protocol designers, implementers, verifiers, security auditors, legal and forensic analysts

**Purpose:** Define the non-negotiable security invariants that form a normative component of the CERTCRYPT Security Model.

**Intended use:** This document MUST be interpreted together with `security-model/1`. It defines the invariant constraints governing certificate semantics and verification interpretation within the current CERTCRYPT architecture.

**Scope:** Applies to all certificates governed by `security-model/1` and to all specifications declaring conformance to it.

**Non-goals:** This document does not define protocol mechanics, cryptographic algorithms, message formats, governance workflows, compliance programs, or implementation guidance.

> This document is **normative**.  
> The keywords MUST, MUST NOT, SHOULD, and MAY are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background and rationale

CERTCRYPT assumes a hostile, long-lived environment.

Most failures in digital certification systems arise not from broken cryptography, but from semantic drift: artifacts gradually acquire meanings they were never designed to support, such as ownership, authorship, legality, trust, or authority.

The current CERTCRYPT architecture adds a second axis of risk: `Independent` can be misrepresented as if it were merely "published", "online", or "approved by CERTCRYPT".

These invariants exist to prevent both classes of failure.

They are not implementation choices or policy preferences.

They are structural constraints that limit what the architecture can mean, regardless of issuer behavior, verifier intent, governance structure, economic model, or elapsed time.

---

## 2. Scope

The invariants defined in this document apply universally and without exception.

They constrain interpretation and verification semantics as defined by `security-model/1`.

They are not optional and cannot be selectively applied.

Any system that violates these invariants is not CERTCRYPT-compatible.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

For the purposes of this document:

- **Invariant** means a non-negotiable security property that constrains certificate semantics and verification outcomes across all CERTCRYPT layers.
- **Issued** means a certificate validly emitted by the issuer under the applicable rules.
- **Independent** means a structural state that exists only when all public independence conditions are satisfied.
- **Verifier** means any independent system or party performing CERTCRYPT verification.

---

## 4. Nature of invariants

Security invariants are protocol truths, not configuration options.

They:

- apply across all CERTCRYPT layers
- cannot be overridden
- cannot be contextualized into weaker local meanings
- cannot be weakened by governance, economics, branding, or implementation behavior

Any incompatible change requires a new major version of the Security Model.

---

## 5. Security invariants

### 5.1 Certificates are not owned

CERTCRYPT certificates do not have an owner.

They are not assets, not transferable, and not controlled or possessed.

**Normative constraints**

- Certificates MUST NOT have an owner.
- Certificates MUST NOT be treated as assets or property.
- Certificates MUST NOT imply control, exclusivity, or entitlement.
- Any party MAY present a certificate.

### 5.2 CERTCRYPT does not emit certificates

Base certificates are emitted by issuers, not by CERTCRYPT.

**Normative constraints**

- CERTCRYPT MUST NOT be modeled as the certificate issuer.
- Higher-layer specifications MUST preserve issuer accountability for base issuance.

### 5.3 Public certificate states are limited to `Issued` and `Independent`

CERTCRYPT does not permit uncontrolled proliferation of public certificate states.

**Normative constraints**

- Public certificate-state semantics MUST be limited to `Issued` and `Independent`.
- No specification MAY invent an intermediate or superior public state that changes the foundational meaning boundary without a new major Security Model version.

### 5.4 `Independent` is structural, not authoritative

`Independent` proves that structural conditions were satisfied under public rules. It does not prove truth, legitimacy, endorsement, or legal effect.

**Normative constraints**

- `Independent` MUST NOT be interpreted as authority, trust, truth, or legal recognition.
- Specifications MUST preserve `Independent` as a structural state only.

### 5.5 Issuance-time participation is mandatory for Independence

Structural independence cannot be added retroactively to an issuance that did not participate in the applicable independence flow at issuance time.

**Normative constraints**

- A certificate MUST NOT be promoted to `Independent` if issuance-time participation was absent.
- No later workflow MAY substitute for missing issuance-time participation.

### 5.6 Leaf-first structural integrity

The relevant unit of structural independence is the leaf, not a later per-certificate convenience interpretation.

**Normative constraints**

- Specifications defining `Independent` semantics MUST preserve leaf-first integrity.
- Verification MUST NOT collapse leaf semantics into an issuer-signed certificate-only shortcut.

### 5.7 Leaf closure is immutable

Once a leaf closure is established for proving `Independent`, the committed leaf contents and ordering cannot be silently mutated.

**Normative constraints**

- Post-closure mutation of committed leaf material MUST invalidate structural independence.
- Verifiers MUST reject artifacts whose independence claim depends on ambiguous or mutable leaf semantics.

### 5.8 Canonicalization is deterministic and unambiguous

Structural security depends on reproducible canonicalization and non-ambiguous parsing.

**Normative constraints**

- Canonicalization MUST be deterministic and fixed per major version.
- Specifications MUST reject ambiguous serializations that could alter verification meaning.
- Two semantically equivalent representations MUST NOT yield conflicting verification results within a version.

### 5.9 Versioning and parsing are strict

Silent downgrade, parser differentials, and "close enough" compatibility are forbidden.

**Normative constraints**

- Required identifiers, versions, and field semantics MUST be interpreted strictly.
- Unknown, unsupported, or ambiguous versions MUST fail closed.
- Verifiers MUST NOT infer weaker semantics from malformed or legacy-looking inputs.

### 5.10 Proof and package artifacts are anti-splicing

No verifier may accept a proof assembled from mismatched leaf, issuer, capacity, settlement, or version contexts.

**Normative constraints**

- Proof artifacts MUST bind to the exact leaf, system domain (`system_id` and `system_root_fingerprint`), rules version, and independence context they claim.
- Mixed-context substitution MUST fail verification.

### 5.11 Capacity is a condition of structural Independence

`Independent` requires valid CERTCRYPT capacity under public rules.

**Normative constraints**

- A certificate MUST NOT verify as `Independent` without valid capacity attributable to the relevant CERTCRYPT domain.
- Lack of valid capacity MUST fail `Independent`, but MUST NOT rewrite `Issued`.

### 5.12 Settlement is a condition of structural Independence

`Independent` requires valid settlement under public rules.

**Normative constraints**

- A certificate MUST NOT verify as `Independent` without valid settlement.
- Settlement semantics MUST be attributable to the relevant CERTCRYPT domain and scope.
- Lack of valid settlement MUST fail `Independent`, but MUST NOT rewrite `Issued`.

### 5.13 Sufficient finality is required

Structural independence cannot rest on settlement references that remain materially reversible under the governing rules.

**Normative constraints**

- `Independent` MUST require settlement evidence with sufficient finality for the governing architecture.
- Specifications MUST define or import a finality rule strict enough to prevent premature independence claims.

### 5.14 Proof of Independence must be offline-verifiable

`Independent` must remain reproducible without live CERTCRYPT authority.

**Normative constraints**

- Proof artifacts for `Independent` MUST support offline verification given the required inputs.
- Live CERTCRYPT APIs, dashboards, or managed services MUST NOT be required as trust anchors.

### 5.15 Verification is deterministic and fail-closed

Ambiguity, unsupported inputs, and missing mandatory evidence do not degrade into acceptance.

**Normative constraints**

- Verification MUST be deterministic.
- Verification MUST fail closed when required conditions cannot be proven.
- Implementations MUST NOT introduce "accept anyway" or reputation-based overrides.

### 5.16 Zero-data and stateless core behavior are preserved

CERTCRYPT is not allowed to become a content-retaining or identity-retaining trust backend.

**Normative constraints**

- CERTCRYPT MUST NOT store documents, identities, personal data, or directly identifying content hashes as part of core semantics.
- Core verification MUST remain stateless with respect to live CERTCRYPT authority.

### 5.17 Managed services are optional and non-authoritative

Resolvers, mirrors, dashboards, and managed copies may exist, but they cannot define truth for verification.

**Normative constraints**

- Managed services MAY assist retrieval and convenience.
- Managed services MUST NOT be authoritative for verification semantics.
- Equivocation by a managed service MUST NOT be able to create valid `Independent` results by itself.

### 5.18 Namespace and authorization scope are explicit

Proofs, settlement references, and capacity references must remain bound to the correct issuer and operational scope.

**Normative constraints**

- Specifications MUST prevent cross-issuer or cross-scope reuse of valid-looking artifacts.
- Delegated authorization, if used, MUST remain tightly scoped to the permitted leaf or operation domain.

### 5.19 Side-channel leakage must be minimized

Zero-data semantics do not excuse avoidable leakage through size, timing, retry patterns, or auxiliary metadata.

**Normative constraints**

- Specifications and implementations SHOULD minimize avoidable side-channel leakage that could reconstruct sensitive facts not intended by the model.
- Convenience layers MUST NOT be treated as exempt from this constraint.

### 5.20 No implicit legal claims

CERTCRYPT remains legally neutral by design.

**Normative constraints**

- Certificates MUST NOT be interpreted as creating legal validity, enforceability, or regulatory compliance by themselves.
- CERTCRYPT MUST NOT be interpreted as a substitute for legally mandated trust services.

### 5.21 Invariants cannot be overridden

Any system that violates these invariants is not CERTCRYPT-compatible.

---

## 6. Closing statement

Certificates are not owned.  
Trust is not granted.  
`Independent` is not authority.

Everything that verifies must verify structurally.

---

## 7. References

- [security-model/1 - CERTCRYPT Security Model Specification](specification.md)
- [RFC 8174 - Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
