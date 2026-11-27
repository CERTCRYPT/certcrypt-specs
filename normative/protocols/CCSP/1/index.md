# CCSP/1 · CERTCRYPT Certificate Serialization Protocol

**Identifier:** CCSP/1

**Label:** CCSP v1

**Page:** Informative version index

**Specification type:** Protocol

**Layer:** Layer 1 — Protocols

**Status:** Frozen

**Depends on:**
- [CCCP/1](../../CCCP/1/index.md)

> This document is **informative**.
> All normative rules are defined exclusively in [CCSP/1/specification](specification.md).
> In case of discrepancy, the [specification](specification.md) always prevails.

---

## What is [CCSP/1](specification.md)?

[CCSP/1 (CERTCRYPT Certificate Serialization Protocol)](specification.md) defines the **canonical envelope structure and serialization rules** used by all CERTCRYPT certificates, independently of subject or consistency protocol.

[CCSP/1](specification.md) is the canonical-by-design certificate envelope layer of CERTCRYPT.

It specifies **how certificates are shaped**, not what they mean.

---

## Role within CERTCRYPT

[CCSP/1](specification.md) defines certificate envelope structure and serialization semantics, and sits between canonicalization and verification.

Where this sits: [the normative corpus index](../../../index.md) describes the
five planes and what each one is for. This document belongs to the protocol
plane, and every plane above it inherits the envelope rules defined here.

No protocol or profile redefines envelope rules.

---

## Normative documents

This protocol consists of the following documents:

- [Overview](overview.md)  
  Informative explanation of the certificate envelope, its role within CERTCRYPT, and design principles.

- [Specification](specification.md)  
  The authoritative and **only normative** definition of the CERTCRYPT certificate envelope, serialization rules, and canonical structure.

In case of discrepancy, **[specification](specification.md) always prevails**.

---

## Versioning

- **Protocol identifier:** `CCSP/1`

No normative changes are permitted.

Any modification that alters the certificate envelope structure or serialization rules **results in a new major version**.

[CCSP/1](specification.md) is valid indefinitely.

---

## One-line summary

[CCSP/1](specification.md) defines the stable, canonical envelope used to serialize all CERTCRYPT certificates.
