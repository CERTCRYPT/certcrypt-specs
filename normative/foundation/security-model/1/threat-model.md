# CERTCRYPT Security Model - Threat Model (security-model/1)

**Identifier:** `security-model/1 - Threat Model`

**Label:** Security Model v1 - Threat Model

**Type:** Foundation Component

**Status:** Frozen

**Layer:** Layer 0 - Foundation

**Depends on:**
- [security-model/1 - CERTCRYPT Security Model Specification](specification.md)
- [security-model/1 - Security Invariants](security-invariants.md)

**Audience:** Protocol designers, implementers, verifiers, security auditors, legal and forensic analysts

**Purpose:** Define the threat boundaries of CERTCRYPT by explicitly stating which classes of attacks and failures are structurally mitigated, which are constrained by lower-layer specifications, and which remain out of scope.

**Intended use:** This document MUST be interpreted together with `security-model/1`. It defines the threat boundaries governing interpretation of guarantees within the current CERTCRYPT architecture.

**Scope:** Applies to all certificates governed by `security-model/1` and to all specifications declaring conformance to it.

**Non-goals:** This document does not define protocol mechanics, operational procedures, monitoring systems, governance enforcement, or implementation guidance.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background and rationale

CERTCRYPT assumes a hostile, long-lived environment.

Most failures in digital certification systems arise not from broken cryptography, but from incorrect assumptions about what the system protects, what it guarantees, and what it implicitly claims.

The current architecture adds another critical requirement: adversaries must not be able to fabricate or simulate `Independent` by combining valid-looking but mismatched artifacts, by relying on ambiguous serialization, or by forcing trust in live CERTCRYPT infrastructure.

This threat model fixes those boundaries explicitly.

---

## 2. Scope

This threat model applies universally and without exception.

**Normative constraints**

- All CERTCRYPT protocols MUST operate within the threat boundaries defined in this document.
- Implementations MUST NOT claim mitigation of threats explicitly listed as out of scope.
- Verification results MUST NOT imply protection against threats not mitigated by design.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

For the purposes of this document:

- **Threat class** means a category of attacks or failure modes.
- **Structural mitigation** means mitigation achieved by protocol invariants, not by discretionary operations.
- **Out of scope** means threats CERTCRYPT explicitly does not attempt to solve at the foundation layer.

---

## 4. Assets under protection

At the foundation layer, CERTCRYPT protects the following technical assets:

- integrity of issuer-emitted certificates
- determinism of canonicalization and parsing
- integrity of leaf closure
- integrity of `independence_proof` binding
- integrity of capacity attribution
- integrity of settlement attribution and finality handling
- reproducibility of offline verification
- correctness of state interpretation for `Issued` and `Independent`
- zero-data and stateless-core guarantees
- non-authoritative status of managed layers

**Normative constraints**

- CERTCRYPT MUST preserve the integrity and verifiability of these assets.
- CERTCRYPT MUST NOT claim protection of assets not listed above at the foundation layer.

CERTCRYPT explicitly does not protect content truthfulness, identity truth, authorship, legal validity, or general infrastructure availability.

---

## 5. Adversarial model

CERTCRYPT assumes adversaries MAY:

- control networks, storage, and delivery channels
- manipulate or replay artifacts
- exploit serialization ambiguity or parser differences
- mix artifacts from different leaves, issuers, scopes, or versions
- attempt settlement timing abuse or rely on insufficient finality
- operate malicious managed services or resolvers
- censor, delay, or selectively refuse convenience services
- exploit side channels
- socially or legally misrepresent what `Independent` means
- fork or clone the protocol

CERTCRYPT MUST NOT assume trusted infrastructure, trusted operators, trusted storage, trusted verifiers, issuer honesty, or legal goodwill.

Only cryptographic primitives and explicitly stated security assumptions defined in this document are assumed secure.

---

## 6. Threat classes mitigated by design

### 6.1 Certificate forgery

**Structural outcome**  
Forgery without valid issuer authority is infeasible.

**Normative constraints**

- Base certificates MUST be cryptographically attributable to an issuer.
- Verifiers MUST reject certificates that fail signature or equivalent issuer-authenticity checks.

### 6.2 Certificate, leaf, or proof tampering

**Structural outcome**  
Modification of required verification material is detectable.

**Normative constraints**

- Verification MUST fail if issuer, leaf, proof, capacity, or settlement bindings do not match the claimed context.

### 6.3 Canonicalization and commitment malleability

**Structural outcome**  
Ambiguous serialization must not yield valid but conflicting interpretations.

**Normative constraints**

- Specifications MUST define deterministic canonicalization.
- Verifiers MUST reject ambiguous or conflicting representations.

### 6.4 Mixed-package or cross-context substitution

**Structural outcome**  
Artifacts from one leaf, issuer, scope, or version do not validate another.

**Normative constraints**

- Verification MUST fail when proof material is spliced across contexts.

### 6.5 Replay and context misuse

**Structural outcome**  
Replayed artifacts do not grant new structural meaning outside their bound context.

**Normative constraints**

- Verification MUST NOT assign meaning outside the artifact's protocol-defined context.

### 6.6 Post-hoc promotion to `Independent`

**Structural outcome**  
Structural independence cannot be manufactured after issuance if issuance-time participation was absent.

**Normative constraints**

- Specifications MUST forbid retroactive promotion into `Independent`.

### 6.7 Settlement finality abuse

**Structural outcome**  
Reversible or insufficiently final settlement evidence must not support `Independent`.

**Normative constraints**

- Structural independence MUST require settlement evidence with sufficient finality.

### 6.8 Cross-issuer or cross-scope reuse

**Structural outcome**  
Valid-looking artifacts from one issuer or scope do not satisfy another.

**Normative constraints**

- Namespace and scope binding MUST be explicit and verifiable.

### 6.9 Managed-service equivocation

**Structural outcome**  
A resolver or mirror cannot become the authority that makes invalid artifacts verify.

**Normative constraints**

- Verification MUST remain reproducible without trusting managed-service responses as authoritative truth.

### 6.10 Infrastructure compromise or disappearance

**Structural outcome**  
Verification remains possible without live CERTCRYPT authority.

**Normative constraints**

- Verification MUST be possible without mandatory live services.

### 6.11 Privacy leakage and correlation

**Structural outcome**  
The architecture must not require document, identity, or correlatable-content storage in core semantics.

**Normative constraints**

- CERTCRYPT MUST NOT require storage of documents, identities, personal data, or directly identifying content hashes as part of core semantics.

### 6.12 Side-channel exploitation

**Structural outcome**  
Avoidable leakage must be minimized and must not be mistaken for acceptable behavior under zero-data claims.

**Normative constraints**

- Specifications and implementations SHOULD minimize avoidable leakage through size, timing, retry, or auxiliary metadata patterns.

### 6.13 Malicious issuers

**Structural outcome**  
CERTCRYPT exposes which issuer key signed and whether structural conditions were met, not whether claims are true.

**Normative constraints**

- Verification results MUST NOT imply content truthfulness or issuer honesty.

### 6.14 Malicious verifiers

**Structural outcome**  
Verification remains reproducible and auditable; verifiers cannot redefine semantics without leaving the standard.

**Normative constraints**

- Verification logic MUST be deterministic.
- Verifiers MUST NOT claim discretionary authority over normative interpretation.

### 6.15 Protocol cloning

**Structural outcome**  
Cloning does not weaken security guarantees if the semantics are preserved, and incompatible clones cannot honestly claim equivalence.

**Normative constraints**

- Protocol secrecy MUST NOT be assumed for security.

---

## 7. Threats explicitly out of scope

At the foundation layer, CERTCRYPT does not mitigate:

- content truthfulness
- identity proofing
- authorship or intent proof
- legal interpretation
- social engineering
- key compromise after issuance
- compromise of the system domain's Level-1 capacity key
- supply-chain compromise of specific implementations
- insider abuse in optional managed services
- business-model viability
- general availability guarantees

**Normative constraints**

- Systems MUST NOT claim CERTCRYPT mitigates out-of-scope threats merely because they coexist with CERTCRYPT.

---

## 8. Security assumptions

CERTCRYPT assumes:

- cryptographic primitives remain secure
- hash functions retain their required resistance properties
- signature or equivalent issuer-authentication mechanisms remain unbroken
- randomness is sufficient where required
- settlement evidence used for `Independent` can be evaluated under a public finality rule

Failure of these assumptions invalidates the relevant guarantees of all comparable digital certification systems.

---

## 9. Closing statement

CERTCRYPT does not prevent every attack.  
It prevents classes of silent security failure that would otherwise let invalid meaning masquerade as valid verification.

---

## 10. References

- [security-model/1 - CERTCRYPT Security Model Specification](specification.md)
- [security-model/1 - Security Invariants](security-invariants.md)
- [RFC 8174 - Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
