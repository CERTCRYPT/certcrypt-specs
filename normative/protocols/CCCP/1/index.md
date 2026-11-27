# CCCP/1 · CERTCRYPT Canonicalization Commitment Protocol

**Identifier:** CCCP/1

**Label:** CCCP v1

**Page:** Informative version index

**Specification type:** Protocol

**Layer:** Layer 0 — Protocols

**Status:** Frozen

**Depends on:**
- None *(Root canonicalization protocol)*  

> This document is **informative**.
> All normative rules are defined exclusively in [CCCP/1/specification](specification.md).
> In case of discrepancy, the [specification](specification.md) always prevails.

---
## What is [CCCP/1](specification.md)?

[CCCP/1 (CERTCRYPT Canonicalization Commitment Protocol)](specification.md) defines the **foundational, subject-agnostic rules** for canonicalization, encoding, hashing, and commitment construction used across all CERTCRYPT protocols and profiles.

It is the **cryptographic bedrock** of CERTCRYPT.

All CERTCRYPT protocols and profiles depend on [CCCP/1](specification.md) to guarantee that:

- identical canonical subject material always produces identical cryptographic results
- verification is deterministic and reproducible
- verification relies exclusively on cryptographic material and, where a subject commitment is checked, the original source data held by the verifier

---
## Role within CERTCRYPT

[CCCP/1](specification.md) does **not** process concrete subjects by itself.  
Instead, it defines the **shared semantics** that every other CERTCRYPT document set inherits.

Where this sits: [the normative corpus index](../../../index.md) describes the
five planes and what each one is for. This document belongs to the protocol
plane, and every plane above it inherits the canonicalization and hashing
semantics defined here.


All protocols that derive or verify hashes rely on [CCCP/1](specification.md) for canonicalization and hashing rules.

While [CCCP/1](specification.md) itself is consistency-verification-agnostic, protocols that involve consistency verification (e.g. [CCVP/1](../../CCVP/1/index.md)) rely on [CCCP/1](specification.md) semantics to verify signed, offline context snapshots deterministically.

While [CCCP/1](specification.md) defines canonicalization and hashing semantics, verifier-side fail-closed behavior is defined in [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/specification.md), and the foundational security boundary that constrains every verifier output is defined in [security-model/1](../../../foundation/security-model/1/specification.md).

---
## Normative documents

This protocol consists of the following documents:

- [Overview](overview.md)
  Informative explanation and architectural context intended for readers and implementers.

- [Specification](specification.md)
  The authoritative and **only normative** definition of canonicalization contexts, hashing rules, and commitment construction.

In case of discrepancy, **[specification](specification.md) always prevails**.

---
## Versioning

- **Protocol identifier:** `CCCP/1`
- CCCP versions are independent of subject profile versions.

No normative changes are permitted.

Any modification that alters canonicalization, hashing, or commitment semantics **results in a new major version**.

[CCCP/1](specification.md) is valid indefinitely.

---
## One-line summary

[CCCP/1](specification.md) defines the deterministic, zero-data canonicalization and hashing rules that make all CERTCRYPT verification possible.
