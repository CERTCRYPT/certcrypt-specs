# CERTCRYPT Certificate Serialization Protocol (CCSP/1) — overview

**Identifier:** CCSP/1

**Label:** CCSP v1

**Page:** Informative overview

**Specification type:** Protocol

**Layer:** Layer 1 — Protocols

**Status:** Frozen

**Depends on:** 
- [CCCP/1](../../CCCP/1/index.md)  

> This document is **informative**.
> All normative rules are defined exclusively in [CCSP/1/specification](specification.md).
> In case of discrepancy, the [specification](specification.md) always prevails.

---

## What is `CCSP/1`?

**[CCSP/1](specification.md)** defines the **canonical envelope and serialization rules** used by all CERTCRYPT certificates.

It specifies how a certificate is structurally organized, serialized, and prepared for canonicalization, hashing, signing, storage, and exchange.

[CCSP/1](specification.md) ensures that CERTCRYPT certificates are:

- structurally consistent  
- canonically serializable  
- interoperable across implementations  
- suitable for long-term, offline verification  

---

## Why this specification exists

Without a strict envelope definition:

- certificates diverge structurally across implementations  
- canonicalization and hashing become ambiguous  
- signatures become unverifiable over time  
- interoperability degrades silently  

[CCSP/1](specification.md) eliminates these risks by defining a **stable, protocol-level certificate container** that all CERTCRYPT specifications rely on.

---

## Scope boundaries

[CCSP/1](specification.md) defines the **certificate envelope and serialization rules** used by all CERTCRYPT certificates.

Meaning, trust, verification logic, canonicalization, and temporal interpretation are defined by the **governing protocol or profile**, not by the envelope itself.

[CCSP/1](specification.md) exists to ensure that certificates are **structurally consistent, interoperable, and canonically serializable**, independent of their semantic domain.

[CCSP/1](specification.md) fixes the form of one timestamp, `payload.anchor.issued_at`: the issuance-time instant of the certificate, signed as part of the anchor, in RFC 3339 UTC with the `Z` suffix. It fixes the form only. What that instant is used for, and any other timestamp in the payload, is defined by the governing protocol or profile.

Envelope metadata timestamps, if present, are informational only and are not used for temporal interpretation.

---

## Core guarantees

By fixing a single, protocol-level certificate envelope, [CCSP/1](specification.md) ensures that:

- certificates are structurally consistent across implementations
- canonicalization and hashing inputs are unambiguous
- structural mutations are always detectable
- certificates remain verifiable offline over long periods of time
- envelope rules are independent of subject and consistency semantics

These guarantees arise from structural constraints, not from trust, policy, or operational controls.

---

## Envelope, not semantics

[CCSP/1](specification.md) defines an **envelope**, not meaning.

It does not define:

- subject canonicalization  
- verification logic  
- trust semantics  
- legal interpretation  
- ownership or entitlement  

---

## Canonical-by-design

[CCSP/1](specification.md) is the **canonical-by-design certificate envelope layer**, meaning that its structure is **designed to be canonically serialized and hashed exclusively under CCCP-defined rules**.

[CCSP/1](specification.md) is designed so that:

- certificates are always serialized as UTF-8 JSON  
- cryptographic operations always operate on canonical forms ([RFC 8785](https://www.rfc-editor.org/rfc/rfc8785)), as defined by [CCCP/1](../../CCCP/1/index.md)
- field ordering never affects verification  
- structural mutations are always detectable  

---

## Relationship to other CERTCRYPT specifications

[CCSP/1](specification.md) is the **canonical-by-design certificate envelope layer** of CERTCRYPT.

It does not define canonicalization, hashing, or trust semantics. Instead, it defines **how certified data, commitments, and signatures are structurally contained and serialized** in a CERTCRYPT certificate.

Relationship overview:

- **[CCCP/1](../../CCCP/1/index.md)**  
    Defines canonicalization contexts, encoding rules, hashing semantics, and commitment construction.  
    [CCCP/1](../../CCCP/1/index.md) provides the cryptographic foundations that all certificates rely on.
    
- **[CCSP/1](specification.md)**  
    Defines the canonical certificate envelope and serialization rules used to structurally contain certified payloads, cryptographic commitments, and signatures.  
    [CCSP/1](specification.md) relies on [CCCP/1](../../CCCP/1/index.md) for all canonicalization and hashing semantics, but defines no semantic, temporal, or verification meaning itself.
    
- **Subject Profiles (e.g. [subject.email/1](../../../profiles/subject.email/1/index.md), [subject.binary/1](../../../profiles/subject.binary/1/index.md), [subject.text/1](../../../profiles/subject.text/1/index.md), [subject.collection/1](../../../profiles/subject.collection/1/index.md))**
    Define how to extract and normalize one kind of subject material in order to produce `canonical_bytes(subject)`.  
    Subject profiles inherit canonicalization and hashing rules from [CCCP/1](../../CCCP/1/index.md) and envelope constraints from [CCSP/1](specification.md).
    
- **Artifact formats (e.g. [verification-package/1](../../../ecosystem/verification/verification-package/1/index.md))**
    Define how artifacts derived from CCSP/1-compliant certificates are represented, packaged, or delivered after issuance, without modifying the certificate envelope or introducing new envelope semantics.
    
- **Protocols (e.g. [CCVP/1](../../CCVP/1/index.md))**  
    Define their own subject or consistency models while relying on:
    
    - [CCCP/1](../../CCCP/1/index.md) for canonicalization, hashing, and commitment guarantees
    - [CCSP/1](specification.md) for certificate envelope structure and serialization

No protocol or profile redefines or weakens the envelope rules defined by [CCSP/1](specification.md).

---

## Reading guide

Recommended reading order for implementers and auditors:

1. [Specification](specification.md)
2. [CCCP/1](../../CCCP/1/specification.md)
3. [CCVP/1](../../CCVP/1/specification.md)
4. the active subject profiles under [profiles/](../../../profiles/index.md)

---

## Versioning

- **Specification identifier:** `CCSP`
- **Specification version:** `/1`

Version `/1` defines the first canonical CERTCRYPT certificate envelope and serialization rules under the active corpus.

Changes that alter envelope structure, serialization rules, the canonical signature payload, or the boundary between envelope structure and external semantic outcomes require a new major version.

Later versions do not retroactively reinterpret already valid certificates governed by `/1`.

---

## One-line summary

`CCSP/1` defines the canonical CERTCRYPT certificate envelope and serialization rules that make every CERTCRYPT certificate structurally consistent, canonically serializable, and offline-verifiable, without itself defining trust, semantics, or temporal interpretation.

---

## Normative reference

This overview is informational in nature.

All definitive rules and constraints are defined in:

- [CCSP/1/specification](specification.md)

In case of discrepancy, the specification **always prevails**.
