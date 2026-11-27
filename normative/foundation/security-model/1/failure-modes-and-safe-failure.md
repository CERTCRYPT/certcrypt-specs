# CERTCRYPT Security Model - Failure Modes and Safe Failure (security-model/1)

**Identifier:** `security-model/1 - Failure Modes and Safe Failure`

**Label:** Security Model v1 - Failure Modes and Safe Failure

**Type:** Foundation Component

**Status:** Frozen

**Layer:** Layer 0 - Foundation

**Depends on:**
- [security-model/1 - CERTCRYPT Security Model Specification](specification.md)
- [security-model/1 - Security Invariants](security-invariants.md)
- [security-model/1 - Security Guarantees and Non-Claims](security-guarantees-and-non-claims.md)

**Audience:** Protocol designers, implementers, verifiers, security auditors, legal and forensic analysts

**Purpose:** Define how CERTCRYPT fails and why those failures are safe by design, ensuring that failure never escalates into implicit trust, silent acceptance, or ambiguous outcomes.

**Intended use:** Constrain verifier and implementation behavior such that invalid, missing, unsupported, or ambiguous inputs result only in non-verification, never in degraded acceptance.

**Scope:** Applies to all CERTCRYPT verification implementations and all deployment environments that claim compatibility with `security-model/1`.

**Non-goals:** This document does not define recovery procedures, transport behavior, or operational playbooks.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background and rationale

CERTCRYPT assumes a hostile, long-lived environment where:

- inputs may be incomplete, corrupted, or adversarial
- infrastructure may be unavailable or gone
- ecosystems may drift or attempt compatibility theater
- verifiers may be pressured to "make it pass"

In most certification systems, the critical security failure is not that verification fails, but that verification degrades.

CERTCRYPT rejects degradation.

Failure is designed to be:

- explicit
- deterministic
- non-escalatory
- non-overridable

---

## 2. Scope

This document governs failure behavior across all CERTCRYPT verification contexts.

It constrains:

- how verifiers classify and report failure
- what outcomes are permitted when inputs are missing or invalid
- what fallbacks are forbidden
- what conditions are not failures because they are out of scope

Any implementation that violates these failure semantics is not CERTCRYPT-compatible.

---

## 3. Defined failure modes

CERTCRYPT verification MAY fail for reasons including, but not limited to:

- modified or corrupted certificate bytes
- malformed certificate structure or missing required fields
- unsupported or unknown identifiers or versions
- ambiguous canonicalization or parser interpretation
- invalid issuer-authenticity material
- invalid or mismatched leaf bindings
- invalid or mismatched proof context
- invalid or insufficiently final settlement evidence for `Independent`
- invalid or missing capacity evidence for `Independent`
- cross-issuer, cross-scope, or cross-version artifact reuse
- inability to evaluate mandatory evidence required by the claimed state

These failures are expected safety boundaries, not exceptional behavior.

**Normative constraints**

- Verifiers MUST treat malformed, incomplete, unsupported, or ambiguous inputs as non-verifying.
- Verifiers MUST NOT repair, auto-correct, or infer missing normative fields.
- Verifiers MUST NOT treat unknown identifiers or versions as "close enough".

---

## 4. Safe failure properties

### 4.1 Fail-closed

Verification returns negative or indeterminate, never positive, when required proof cannot be established.

**Normative constraints**

- Implementations MUST fail closed.
- Implementations MUST NOT return a positive verification outcome when any required check fails or cannot be evaluated.

### 4.2 No fallback trust

No issuer, resolver, operator, UI, or user preference can override failure.

**Normative constraints**

- Implementations MUST NOT introduce trust-based override modes.
- Implementations MUST NOT treat reputation, branding, ecosystem claims, payment status, or service responses as substitutes for verification.

### 4.3 No semantic degradation

Failure of one state or dimension cannot be rebranded as success of another stronger state.

**Normative constraints**

- Implementations MUST NOT upgrade a partial outcome to a stronger outcome by ignoring missing inputs.
- Implementations MUST preserve the distinction between `Issued` and `Independent`.
- Failure of `Independent` conditions MUST NOT retroactively invalidate `Issued` if `Issued` remains valid.

### 4.4 No silent acceptance

Ambiguous or malformed data never verifies successfully.

**Normative constraints**

- Implementations MUST produce explicit negative or indeterminate outcomes.
- Implementations MUST NOT silently coerce types, normalize unsupported encodings, or guess canonicalization.

---

## 5. Required failure reporting semantics

CERTCRYPT does not require a single reporting format, but it requires strict semantics.

**Normative constraints**

- Implementations MUST ensure that failure of a required check is never represented as success.
- Implementations MUST distinguish "unknown", "not proven", and "invalid" where the distinction matters to the claimed state.
- Implementations MUST NOT collapse "unknown" into "valid".

When a multi-state outcome is reported:

- `Issued` MUST be reported independently from `Independent`
- lack of proof for `Independent` MUST NOT be mislabeled as tampering with `Issued` unless tampering with `Issued` is actually detected

---

## 6. Non-failure conditions

The following conditions are not CERTCRYPT failures.

They are out of scope by design and MUST NOT be treated as protocol defects:

- inability to interpret content truth
- inability to assess honesty, intent, or authorship
- lack of legal recognition in a jurisdiction
- absence of optional convenience services
- distrust of an issuer as a social actor

However, if a claimed verification state requires specific evidence, absence of that mandatory evidence is a verification failure for that state.

Example:

- absence of settlement evidence is not a defect in `Issued`
- absence of required settlement evidence is a failure for `Independent`

---

## 7. Adversarial implications

Any attack that forces CERTCRYPT verification to fail results only in non-verification, not silent compromise.

Attackers gain no standards-compliant advantage from inducing errors, ambiguity, or missing inputs because:

- there is no "accept anyway" path
- there is no authority fallback path
- there is no degraded mode that can be exploited into `Independent`

**Normative constraints**

- Implementations MUST preserve safe-failure behavior under parsing failures, unsupported identifiers, ambiguous serializations, and external-data unavailability.
- Implementations MUST NOT weaken failure semantics for operational convenience.

---

## 8. Compatibility note

Safe-failure semantics are part of CERTCRYPT compatibility.

**Normative constraints**

- Any implementation that introduces fallback trust, degraded acceptance, or silent repair is not CERTCRYPT-compatible.
- Any system claiming CERTCRYPT compatibility MUST preserve the failure properties defined in this document.

---

## 9. Closing statement

CERTCRYPT does not degrade.

When required proof cannot be established, the claimed state does not verify.

---

## 10. References

- [security-model/1 - CERTCRYPT Security Model Specification](specification.md)
- [security-model/1 - Security Invariants](security-invariants.md)
- [security-model/1 - Security Guarantees and Non-Claims](security-guarantees-and-non-claims.md)
- [RFC 8174 - Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
