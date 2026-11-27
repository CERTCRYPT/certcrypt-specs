# CERTCRYPT Canonicalization Commitment Protocol (CCCP/1) — overview

**Identifier:** CCCP/1

**Label:** CCCP v1

**Page:** Informative overview

**Specification type:** Protocol

**Layer:** Layer 0 — Protocols

**Status:** Frozen

**Depends on:**
- None *(Root canonicalization protocol)*  

> This document is **informative**.
> All normative rules are defined exclusively in [CCCP/1/specification](specification.md).
> In case of discrepancy, the [specification](specification.md) always prevails.

---
## What is `CCCP/1`?

The [CERTCRYPT Canonicalization Commitment Protocol (CCCP/1)](specification.md) defines the **foundational, subject-agnostic rules** used by all CERTCRYPT certification protocols and profiles to achieve deterministic, reproducible cryptographic verification.

It establishes a shared cryptographic baseline for:

- canonicalization
- encoding
- hashing
- subject commitment construction

All subject-specific protocols and profiles (emails, documents, registries, etc.) rely on [CCCP/1](specification.md) to ensure that the same canonical subject material produces the same cryptographic result, regardless of system, implementation, or time.

---
## Why this specification exists

Digital subject material rarely exists as a single, stable byte sequence.  
Harmless variations introduced by transport, storage, export tools, or operating systems can alter raw bytes without changing meaning.

Without a strict canonicalization foundation:

- identical subject material can hash differently
- verification becomes non-reproducible
- verification shifts from public rules to tooling

[CCCP/1](specification.md) eliminates this ambiguity by defining **exact, protocol-level rules** that all CERTCRYPT implementations follow.

---
## Scope boundaries

[CCCP/1](specification.md) focuses exclusively on **canonicalization, encoding, hashing, and commitment construction**.

Concerns such as subject extraction, content interpretation, identity binding, legal validity, or issuance-consistency verification are intentionally handled by other layers of the CERTCRYPT specification.

This separation ensures that [CCCP/1](specification.md) remains a **pure, subject-agnostic cryptographic foundation**, stable across use cases and time.

---
## Core guarantees

[CCCP/1](specification.md) enforces the following non-negotiable properties:

- **Determinism**  
  Identical inputs always yield identical canonical bytes and hashes.

- **Zero-data operation**  
  No subject content or identities are embedded or retained.

- **Forensic reproducibility**  
  Independent parties can reproduce verification results without coordination.

- **Independent verification**  
  Verification relies exclusively on cryptographic material, context snapshots where applicable, and, where a subject commitment is checked, original source data held by the verifier, without requiring deference to any party, toolchain, implementation, or infrastructure component.

- **Unlinkability**  
  Subject commitments bind subject material to a certificate instance without enabling cross-certificate correlation.

---
## Relationship to other CERTCRYPT specifications

[CCCP/1](specification.md) is the **core canonicalization layer** of CERTCRYPT.

It does not operate on specific kinds of subject material directly. Instead, it provides the shared semantics that all CERTCRYPT protocols and profiles inherit.

**[CCSP/1](../../CCSP/1/index.md) acts as the canonical certificate envelope layer**, responsible for structurally containing canonicalized data, commitments, and signatures derived under [CCCP/1](specification.md) semantics.

Relationship overview:

- [CCCP/1](specification.md) 
  Defines canonicalization contexts, encoding rules, hashing semantics, and commitment construction.

- **[CCSP/1](../../CCSP/1/index.md)**  
  Defines the canonical certificate envelope structure and serialization rules used to contain canonicalized data, commitments, and signatures. 
  CCSP/1 relies on CCCP/1 for all canonicalization and hashing semantics, but does not define them itself.   

- **Subject Profiles (e.g. [subject.email/1](../../../profiles/subject.email/1/index.md), [subject.binary/1](../../../profiles/subject.binary/1/index.md), [subject.text/1](../../../profiles/subject.text/1/index.md), [subject.collection/1](../../../profiles/subject.collection/1/index.md))**
  Define how to extract and normalize one kind of subject material in order to produce `canonical_bytes(subject)`.

- **Artifact formats (e.g. [verification-package/1](../../../ecosystem/verification/verification-package/1/index.md))**
  Define how artifacts derived from CCCP-compliant certification and verification are represented, packaged, or delivered, without introducing new subjects or altering canonicalization, hashing, or verification semantics.

- **Protocols (e.g. [CCVP/1](../../CCVP/1/index.md))**
  Define their own subject models while relying on [CCCP/1](specification.md) for canonicalization and hashing guarantees.

---
## How `CCCP/1` is used

In practice, [CCCP/1](specification.md) is never used alone.

An implementation typically:

1. Applies a subject profile (e.g. [subject.email/1](../../../profiles/subject.email/1/index.md), [subject.text/1](../../../profiles/subject.text/1/index.md)) to derive `canonical_bytes(subject)`
2. Applies [CCCP/1](specification.md) canonicalization and hashing rules
3. Constructs a subject commitment using a per-certificate nonce
4. Embeds only derived cryptographic values in the certificate
5. Enables later verification of the subject commitment by whoever holds the original source material

---

## Reading guide

Recommended reading order for implementers and auditors:

1. [Specification](specification.md)
2. [CCSP/1](../../CCSP/1/specification.md)
3. [CCVP/1](../../CCVP/1/specification.md)
4. the active subject profiles under [profiles/](../../../profiles/index.md)

---

## Versioning

- **Specification identifier:** `CCCP`
- **Specification version:** `/1`

Version `/1` defines the foundational canonicalization, encoding, hashing, and commitment-construction rules used by all CERTCRYPT certification protocols and profiles.

Changes that alter canonicalization contexts, encoding rules, hashing semantics, or the commitment-construction model require a new major version.

Later versions do not retroactively reinterpret already valid commitments governed by `/1`.

---

## One-line summary

`CCCP/1` defines the canonical, subject-agnostic canonicalization, encoding, hashing, and commitment-construction rules that all CERTCRYPT certification protocols and profiles inherit, ensuring that the same canonical subject material produces the same cryptographic result.

---

## Normative reference

This overview is informational in nature.

All definitive rules, requirements, and constraints are defined in:

- [CCCP/1](specification.md)

In case of discrepancy, the specification **always prevails**.
