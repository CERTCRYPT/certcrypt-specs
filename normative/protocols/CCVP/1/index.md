# CCVP/1 · CERTCRYPT Consistency Verification Protocol

**Identifier:** CCVP/1

**Label:** CCVP v1

**Page:** Informative version index

**Specification type:** Protocol

**Layer:** Layer 1 — Protocols

**Status:** Frozen · optional verification plane, outside the `Issued` and `Independent` path

**Depends on:**

- [CCCP/1](../../CCCP/1/index.md)
- [CCSP/1](../../CCSP/1/index.md)

> This document is **informative**.
> All normative rules are defined exclusively in [CCVP/1/specification](specification.md).
> In case of discrepancy, the [specification](specification.md) always prevails.

---

## What is [CCVP/1](specification.md)?

[CCVP/1 (CERTCRYPT Consistency Verification Protocol)](specification.md) defines how **issuance declared context** is represented and verified in CERTCRYPT using **certified context snapshots**.

It defines how issuance context is expressed as certified context snapshots, not how cryptography is performed.

CCVP/1 verifies issuance consistency against a declared context at a given time. It does not enforce policy, validate intent, or determine compliance.

Context snapshots MAY include optional declarative `policy_refs`, but CCVP/1 does not interpret, enforce, or validate those referenced policy artifacts.

Consistency verification MUST NOT be confused with cryptographic verification.
Cryptographic verification establishes authenticity.
Consistency verification establishes alignment with declared context.

> **Canonical definition**
>
> **CCVP/1 verifies whether a certificate issuance is structurally consistent with one declared context at one point in time.**
>
> It does not determine truth, trust, approval, compliance, or authority.
>
> A `consistency-match` means only that the issuance matched the selected declared context under the applicable snapshot-selection rules.
>
> CCVP/1 may expose consistency with declared context, but it does not prove policy compliance.
>
> Different declared contexts may yield different consistency outcomes for the same certificate.
>
> CCVP/1 therefore exposes contextual alignment, not institutional validation.

---

## Role within CERTCRYPT

[CCVP/1](specification.md) defines the CERTCRYPT protocol for representing and verifying **issuance consistency** using certified context snapshots.

[CCVP/1](specification.md) operates within the constraints defined by the [CERTCRYPT Security Model](../../../foundation/security-model/1/index.md) (`security-model/1`), including non-retroactivity, verifier independence, and absence of trust delegation.

It operates on top of the canonical foundations provided by:

- [CCCP/1](../../CCCP/1/index.md) for canonicalization, hashing, and commitment semantics
- [CCSP/1](../../CCSP/1/index.md) for certificate envelope structure and serialization rules

[CCVP/1](specification.md) does not define subject semantics or a canonical verifier output object.

[CCVP/1](specification.md) defines only the semantic consistency outcomes `consistency-match`, `consistency-mismatch`, and `consistency-unknown`.

[CCVP/1](specification.md) operates at **Layer 1 — Protocols**, producing consistency outcomes that are consumed by verifiers, without defining verification behavior or external interpretation.

Declared context on the target certificate is carried in `payload.context`, which names the snapshot issuer by label and composite key fingerprint. Issuer identity and key binding — of the target and of every snapshot — are derived from the valid issuer signature under [CCSP/1](../../CCSP/1/index.md), never from a field the certificate carries.

CCVP/1 is optional. A verifier that runs it reports the consistency outcome beside the `Issued` and `Independent` verdicts; the outcome never changes either of them, and a verifier that does not run it is not thereby incomplete. The public conformance suite carries vectors for it (`ccvp-consistency`).

Explicit non-claims of CCVP/1 are documented in [§0.2 of the specification](specification.md) (What CCVP/1 Does Not Decide), and the foundational non-claims that constrain every CERTCRYPT verifier output are defined in [security-model/1](../../../foundation/security-model/1/specification.md).

---

## Normative documents

This protocol consists of the following documents:

- [Overview](overview.md)
  Informative explanation of context snapshots and consistency-verification rationale.

- [Specification](specification.md)
  The authoritative definition of context snapshot certificate semantics, snapshot selection, and consistency-verification rules.

- [Verifier Consistency Tree](verifier-consistency-tree.md)
  Normative verifier flow for resolving CCVP/1 consistency outcomes.

- [Verifier Consistency Tree — Examples](verifier-consistency-tree-examples.md)
  Informative worked examples of that flow.

In case of discrepancy, **[specification](specification.md) always prevails**.

---

## Versioning

- **Protocol identifier:** `CCVP/1`

Any modification that alters consistency-verification semantics, snapshot selection rules, or outcome interpretation **results in a new major version**.

[CCVP/1](specification.md) is the consistency-verification protocol of CERTCRYPT until superseded. Running it is optional for every verifier.

---

## One-line summary

**[CCVP/1](specification.md) defines issuance consistency as declared-context alignment verified at issuance time.**
