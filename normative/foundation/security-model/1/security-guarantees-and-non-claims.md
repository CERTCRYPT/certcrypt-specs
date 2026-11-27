# CERTCRYPT Security Model - Security Guarantees and Non-Claims (security-model/1)

**Identifier:** `security-model/1 - Security Guarantees and Non-Claims`

**Label:** Security Model v1 - Security Guarantees and Non-Claims

**Type:** Foundation Component

**Status:** Frozen

**Layer:** Layer 0 - Foundation

**Depends on:**
- [security-model/1 - CERTCRYPT Security Model Specification](specification.md)
- [security-model/1 - Security Invariants](security-invariants.md)
- [security-model/1 - Threat Model](threat-model.md)

**Audience:** Protocol designers, implementers, verifiers, security auditors, legal and forensic analysts

**Purpose:** Define what CERTCRYPT explicitly guarantees and, equally importantly, what CERTCRYPT explicitly does not claim.

**Intended use:** This document MUST be interpreted together with `security-model/1`. It defines the guarantee and non-claim boundaries governing interpretation of verification outcomes within the current CERTCRYPT architecture.

**Scope:** Applies to all certificates governed by `security-model/1` and to all specifications declaring conformance to it.

**Non-goals:** This document does not define protocol mechanics, cryptographic algorithm specifications, message formats, governance workflows, operational controls, or implementation guidance.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background and rationale

In hostile long-lived environments, the most common failure mode is not cryptographic breakage but claim inflation.

Artifacts gradually acquire meanings they were never designed to support, such as ownership, authorship, legality, trustworthiness, intent, consent, or economic righteousness.

The leaf-based architecture introduces one more inflation risk: treating `Independent` as if it meant "CERTCRYPT says this is true" or "CERTCRYPT is online and confirms it".

This document fixes the guarantee boundary and the non-claim boundary so that those errors remain out of scope permanently.

---

## 2. Scope

The guarantees and non-claims in this document apply universally and without exception.

They constrain:

- what issuers may claim about certificates
- what verifiers may claim about verification outcomes
- what ecosystems may claim about compliance and governance
- what operators may claim about economic actions
- what third parties may claim about legal effect

---

## 3. Security guarantees

The following properties are guaranteed by CERTCRYPT, assuming standard cryptographic primitives remain secure and the certificate is verified according to the applicable CERTCRYPT specifications.

### 3.1 Deterministic verifiability

Given the same inputs, the same rules, and a conforming implementation, independent verifiers reach the same outcome.

**Normative constraints**

- Verification rules MUST be deterministic and reproducible.
- Verification MUST NOT depend on privileged live infrastructure or issuer cooperation.

### 3.2 Tamper evidence

Any modification to required verification material invalidates the corresponding verification outcome.

**Normative constraints**

- Verification MUST fail if integrity bindings do not match.
- Implementations MUST NOT accept modified inputs as valid.

### 3.3 Offline verification

Verification of both `Issued` and `Independent` is designed to remain reproducible without live CERTCRYPT authority, given the required verification inputs.

**Normative constraints**

- Implementations MUST NOT introduce mandatory live CERTCRYPT dependencies as trust anchors.
- Optional online retrieval MAY exist, but MUST remain convenience only.

### 3.4 Structural state separation

CERTCRYPT distinguishes `Issued` from `Independent`.

`Issued` reflects valid issuer-local issuance under the applicable rules.  
`Independent` reflects the additional structural conditions defined by the architecture.

**Normative constraints**

- Verification outcomes MUST preserve the distinction between `Issued` and `Independent`.
- Failure of `Independent` conditions MUST NOT be misreported as failure of `Issued` when `Issued` remains valid.

### 3.5 Independence is publicly constrained

`Independent` cannot validly exist without issuance-time participation, valid leaf semantics, valid capacity, valid settlement with sufficient finality, and offline-verifiable proof conditions under public rules.

**Normative constraints**

- Higher-layer specifications MUST preserve these structural conditions.

### 3.6 Zero-data core boundary

CERTCRYPT core semantics do not require document, identity, personal-data, or directly identifying content-hash retention.

**Normative constraints**

- Core semantics MUST NOT require those classes of retained data for verification meaning.

### 3.7 Authority minimization

No issuer, operator, resolver, dashboard, or managed service can unilaterally force a verifier to accept an invalid result while remaining compatible with CERTCRYPT.

**Normative constraints**

- Verification outcomes MUST depend only on cryptographic correctness and protocol-defined rules.
- No third party may override a verifier's negative result through trust or convenience channels.

---

## 4. Explicit non-claims

CERTCRYPT explicitly does not claim, provide, or guarantee any of the following.

### 4.1 Content truthfulness or semantic correctness

CERTCRYPT does not prove whether content is true, accurate, honest, or correct.

### 4.2 Legal validity by itself

CERTCRYPT does not claim legal validity in any jurisdiction by default.

### 4.3 Identity verification or human authentication

CERTCRYPT does not perform identity proofing, KYC, or human identity authentication.

### 4.4 Intent, consent, or authorship proof

CERTCRYPT does not prove intent, consent, authorship, or human action.

### 4.5 Trustworthiness of issuers, operators, or verifiers

CERTCRYPT does not claim trust, reputation, quality, or honesty.

### 4.6 Protection against false inputs

CERTCRYPT does not prevent issuers from certifying misleading statements or false claims.

### 4.7 Ownership, possession, or entitlement

Certificates do not confer rights, control, exclusivity, or property status.

### 4.8 Economic payment as truth or authority

Payment, settlement, or capacity expenditure do not create truth, legitimacy, trust, or legal effect.

Important distinction:

- `Issued` MUST NOT depend on payment, settlement, or accounting state for its basic cryptographic meaning.
- `Independent` DOES depend on valid capacity and valid settlement under public rules, but only as structural conditions of that state.

That dependency MUST NOT be reinterpreted as:

- a statement that payment proves truth
- a statement that settlement grants authority
- a statement that economic participation cures invalid issuance

### 4.9 Live revocation or live authority

CERTCRYPT does not define a live authority that verifiers must trust in order to determine whether a certificate is valid.

### 4.10 Managed-service truth

Resolvers, dashboards, mirrors, and managed copies are not authoritative truth sources for verification semantics.

### 4.11 Retroactive reinterpretation

Later policy, governance, branding, or service behavior does not retroactively change the meaning of past certificates governed by a frozen Security Model version.

---

## 5. Interpretation boundary

CERTCRYPT verification establishes cryptographic and structural facts only; it enables independent evaluation of them.

At this layer:

- `Issued` means valid issuer-local issuance under the governing rules
- `Independent` means that the additional public structural conditions of independence were satisfied

Neither state means:

- truth
- ownership
- authorship
- legal validity
- institutional endorsement
- live online approval

**Normative constraints**

- Verifiers and issuers MUST treat semantic interpretation beyond these limits as out of scope for CERTCRYPT verification.

---

## 6. Closing statement

CERTCRYPT guarantees bounded structural meaning.  
It does not guarantee truth, trust, authority, or legal effect.

---

## 7. References

- [security-model/1 - CERTCRYPT Security Model Specification](specification.md)
- [security-model/1 - Security Invariants](security-invariants.md)
- [security-model/1 - Threat Model](threat-model.md)
- [RFC 8174 - Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
