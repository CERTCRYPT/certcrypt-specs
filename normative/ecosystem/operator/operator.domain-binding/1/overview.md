# operator.domain-binding/1 · CERTCRYPT Operator Domain Binding Specification · Overview

**Identifier:** `operator.domain-binding/1`

**Label:** CERTCRYPT Operator Domain Binding Specification (operator.domain-binding/1)

**Page:** Informative overview

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `operator.domain-binding/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## Why it exists

An independence proof can name the node that carried a submission by its operator identifier, `op:…`. That identifier is opaque. An operator that wants to be recognisable — a sector body running a node for its members, for instance — needs a way to say "this key is ours" that anyone can check without asking CERTCRYPT.

---

## How it works

```text
operator key  ──signs──▶  statement { operator_id, domain_ascii, sequence, valid_until, … }
                                │
HTTPS origin  ──publishes──▶  https://<domain_ascii>/.well-known/certcrypt-node.json
```

- The key's signature shows the node consents; the origin's publication, under a valid TLS certificate, shows the domain consents. Both are required.
- The statement carries the public key, so anyone can derive the `op:` and check the signature.
- A sequence number and a bounded validity protect against replay; an `unbind` statement withdraws a binding.
- A service that displays the association starts it at the first successful check, never backdates it, and never changes the association of a past item except by an auditable correction.
- The node is never contacted, so a node on a private network can be bound to a public host name.

---

## What it is not

- It is not part of an independence proof and never changes a verification result.
- It does not prove the legal identity of an operator.
- It is not an endorsement: a service shows the host name as neutral text, the same for every operator, and shows nothing when there is no binding.

---

## Normative documents

- [Specification](./specification.md)

---

## Related documents

- [operator.recognition/1](../../operator.recognition/1/index.md)
- [independence.proof/1](../../../../models/independence.proof/1/index.md)

---

## Versioning

- **Specification identifier:** `operator.domain-binding`
- **Specification version:** `/1`

---

## One-line summary

`operator.domain-binding/1` lets a node operator be associated with an HTTPS origin through a statement its key signs and the origin publishes, outside independence proofs and without any endorsement.
