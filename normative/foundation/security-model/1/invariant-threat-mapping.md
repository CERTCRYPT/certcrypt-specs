# CERTCRYPT Security Model - Invariant-Threat Mapping (security-model/1)

**Identifier:** `security-model/1 - Invariant-Threat Mapping`

**Label:** Security Model v1 - Invariant-Threat Mapping

**Type:** Foundation Component

**Status:** Frozen

**Layer:** Layer 0 - Foundation

**Depends on:**
- [security-model/1 - CERTCRYPT Security Model Specification](specification.md)
- [security-model/1 - Security Invariants](security-invariants.md)
- [security-model/1 - Threat Model](threat-model.md)

**Audience:** Protocol designers, implementers, verifiers, security auditors, legal and forensic analysts

**Purpose:** Define the explicit mapping between CERTCRYPT security invariants and the threat classes they structurally mitigate.

**Intended use:** To show that CERTCRYPT security properties arise from specification design, not from operational trust, governance discretion, or live infrastructure.

**Scope:** Applies to all CERTCRYPT specifications and constrains how security guarantees may be claimed or interpreted.

**Non-goals:** This document does not introduce new invariants, new threats, or new mitigation mechanisms.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background and rationale

CERTCRYPT security is structural, not discretionary.

Each security invariant exists to neutralize one or more well-defined threat classes. Conversely, no threat mitigation exists that is not grounded in an invariant.

This document exists to prevent:

- implicit or inflated security claims
- assumption of protections not provided
- misinterpretation of `Independent` as authority
- audit ambiguity about why a property holds

---

## 2. Scope

This mapping applies universally and without exception.

**Normative constraints**

- Security claims MUST be justified by one or more invariants listed in [Security invariants](security-invariants.md).
- No threat MAY be claimed as mitigated unless explicitly mapped in this document.
- Implementations MUST NOT claim protection based solely on operational, economic, or governance measures.

---

## 3. Nature of the mapping

This document establishes an authoritative but non-exhaustive relationship between:

- what CERTCRYPT guarantees structurally, and
- what threat classes those guarantees neutralize

**Normative constraints**

- The absence of a mapping MUST be interpreted as absence of structural mitigation at this layer.
- This mapping MUST NOT be extended by interpretation, marketing, governance, or deployment context.

---

## 4. Invariant-threat mapping

### 4.1 Certificates are not owned

**Mitigated threat classes**

- ownership disputes
- certificate transfer abuse
- exclusivity or entitlement claims
- assetization of certificates

### 4.2 CERTCRYPT does not emit certificates

**Mitigated threat classes**

- issuer-accountability confusion
- authority laundering through CERTCRYPT branding
- false attribution of base issuance to CERTCRYPT

### 4.3 Public certificate states are limited to `Issued` and `Independent`

**Mitigated threat classes**

- uncontrolled state inflation
- silent semantic tiering
- pseudo-authoritative states introduced by convenience layers

### 4.4 `Independent` is structural, not authoritative

**Mitigated threat classes**

- trust inflation
- semantic overreach
- institutional or legal over-interpretation
- conversion of structural proof into authority claims

### 4.5 Issuance-time participation is mandatory for Independence

**Mitigated threat classes**

- post-hoc retro-certification
- replay-based promotion to `Independent`
- later attachment of independence semantics to non-participating issuance

### 4.6 Leaf-first structural integrity

**Mitigated threat classes**

- per-certificate shortcut reinterpretation
- loss of structural context
- false independence based on incomplete leaf semantics

### 4.7 Leaf closure is immutable

**Mitigated threat classes**

- leaf mutation after closure
- hidden reordering or substitution
- silent change of the material supposedly fixed

### 4.8 Canonicalization is deterministic and unambiguous

**Mitigated threat classes**

- canonicalization malleability
- parser differentials
- commitment mismatches
- verification ambiguity

### 4.9 Versioning and parsing are strict

**Mitigated threat classes**

- protocol downgrade
- silent legacy fallback
- unsupported-version acceptance
- "close enough" parsing abuse

### 4.10 Proof and package artifacts are anti-splicing

**Mitigated threat classes**

- mixed-package substitution
- cross-leaf proof assembly
- cross-version artifact reuse
- issuer-context splicing

### 4.11 Capacity is a condition of structural Independence

**Mitigated threat classes**

- fake independence without valid capacity
- capacity laundering
- structural claims detached from CERTCRYPT economic domain

### 4.12 Settlement is a condition of structural Independence

**Mitigated threat classes**

- fake independence without valid settlement
- settlement-free independence claims
- semantic collapse of `Independent` into mere publication

### 4.13 Sufficient finality is required

**Mitigated threat classes**

- premature independence claims
- reversible-settlement abuse
- reorg-based invalidation of recently claimed independence

### 4.14 Proof of Independence must be offline-verifiable

**Mitigated threat classes**

- live-authority dependency
- resolver monopoly
- verification censorship through service removal

### 4.15 Verification is deterministic and fail-closed

**Mitigated threat classes**

- silent acceptance
- degraded verification
- trust-based override
- ambiguous-positive outcomes

### 4.16 Zero-data and stateless core behavior are preserved

**Mitigated threat classes**

- content-retention drift
- identity retention drift
- surveillance-by-core-semantics
- live-state dependency

### 4.17 Managed services are optional and non-authoritative

**Mitigated threat classes**

- managed-service equivocation becoming authoritative
- central delivery dependency
- dashboard or API authority inflation

### 4.18 Namespace and authorization scope are explicit

**Mitigated threat classes**

- cross-issuer namespace confusion
- delegated-authorization abuse
- scope leakage across leaves or operational domains

### 4.19 Side-channel leakage must be minimized

**Mitigated threat classes**

- metadata reconstruction
- timing-based leakage
- leaf-shape inference
- leakage inconsistent with zero-data claims

### 4.20 No implicit legal claims

**Mitigated threat classes**

- regulatory misclassification
- implied legal validity
- legal authority laundering through technical semantics

### 4.21 Invariants cannot be overridden

**Mitigated threat classes**

- protocol dilution
- incompatible forks claiming equivalence
- silent weakening of guarantees

---

## 5. Closing statement

Every structural guarantee in CERTCRYPT must be traceable to an invariant.  
If a threat is not neutralized by an invariant, it is not structurally solved at this layer.

---

## 6. References

- [security-model/1 - CERTCRYPT Security Model Specification](specification.md)
- [security-model/1 - Security Invariants](security-invariants.md)
- [security-model/1 - Threat Model](threat-model.md)
- [RFC 8174 - Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
