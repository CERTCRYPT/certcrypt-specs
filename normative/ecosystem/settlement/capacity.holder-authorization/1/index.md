# capacity.holder-authorization/1 · CERTCRYPT Capacity Holder Authorization Specification

**Identifier:** `capacity.holder-authorization/1`

**Label:** CERTCRYPT Capacity Holder Authorization Specification (capacity.holder-authorization/1)

**Page:** Informative version index

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `capacity.holder-authorization/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `capacity.holder-authorization/1`?

`capacity.holder-authorization/1` is the offline-transportable artifact by which a key attributable to the CERTCRYPT System Domain delegates, to one commitment-holder's key set, the authority to sign `capacity.commitment/1` artifacts within a validity window.

It is the missing link between the system-manifest root and the holder key that signs individual commitments.

It does **not** define:

- holder-internal accounting or safety policy
- topup, grant ingestion, or payment mechanics
- live revocation
- consumption or settlement
- wallet, balance, prepaid credit, or any SaaS-balance semantics

---

## Why it exists

Without this artifact, a verifier cannot resolve, offline, that a given `capacity.commitment/1` was signed by a key actually authorized to sign it under the active CERTCRYPT System Domain.

CERTCRYPT does not sign `capacity.commitment/1` directly. It signs the Level-1 binding of `capacity.holder-authorization/1`, which authorizes a set of per-operation holder keys. The holder, in turn, signs each commitment with a fresh key from that set. The verifier resolves the chain offline:

```
system-manifest/1
  → system-domain signing key       (Level 1, kid = authorization_issuer_kid)
    → capacity.holder-authorization/1   (Level 2, holder_key_set_root)
      → capacity.commitment/1            (Level 3, signed by an operation key of that set)
```

The Level-1 key id identifies the system-domain key and MUST NOT be confused with any holder-level key; holder keys carry no stable identifier.

---

## Role within CERTCRYPT

`capacity.holder-authorization/1` sits between system-domain attribution and commitment signing.

Within the current architecture:

- `system-manifest/1` provides root attribution material.
- The system-domain signing key delegates to a holder's key set by signing the `capacity.holder-authorization/1` binding.
- The holder signs `capacity.commitment/1` for individual certificates entering the Independent flow.
- `submission-set` validates structural consumability of those commitments against the chain.
- Settlement fixes whether valid CERTCRYPT capacity was actually consumed.
- `independence.proof/1` defines the artifact a verifier evaluates offline to establish whether the resulting independence state holds under public rules.

`capacity.holder-authorization/1` does not by itself prove `Independent`, does not consume capacity, and does not bind to a specific certificate.

---

## Normative documents

The normative component of `capacity.holder-authorization/1` is:

- [Specification](./specification.md)

The specification defines:

- the signed binding and its field order
- anti-splicing requirements with `capacity.commitment/1`
- signature anchoring through `system-manifest/1`
- validity windows, and the scope the fixation service checks
- offline verifier obligations
- non-goals and interpretation boundaries

---

## Related documents

- [capacity.commitment/1](../../capacity.commitment/1/index.md)
- [system-manifest/1](../../../../foundation/system-manifest/1/index.md)
- [system-domain/1](../../../../foundation/system-domain/1/index.md)
- [rules-domain/1](../../../../foundation/rules-domain/1/index.md)
- [independence.proof/1](../../../../models/independence.proof/1/index.md)

---

## Versioning

- **Specification identifier:** `capacity.holder-authorization`
- **Specification version:** `/1`

Any change to the signed-field set or its order, scope semantics, signature anchoring, or the layered relationship with the manifest or commitment specs requires a new major version.

---

## One-line summary

`capacity.holder-authorization/1` defines the canonical offline-transportable artifact by which the CERTCRYPT System Domain delegates to a commitment-holder's key set the authority to sign `capacity.commitment/1` within a time-bounded window.
