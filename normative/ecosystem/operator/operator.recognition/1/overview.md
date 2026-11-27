# operator.recognition/1 · CERTCRYPT Operator Recognition Credential Specification · Overview

**Identifier:** `operator.recognition/1`

**Label:** CERTCRYPT Operator Recognition Credential Specification (operator.recognition/1)

**Page:** Informative overview

**Specification type:** Ecosystem Specification

**Layer:** Layer 3 — Ecosystem

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `operator.recognition/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## Why it exists

An issuer hands its submission sets to a node, and the node carries them to the fixation service. The fixation service admits them only from a node whose operator key it recognised: the node presents its credential and, in the same request, proves that it holds the operator key. The issuer trusts no node: for it the node is a transport, and what an issuance yields is a proof signed by the CERTCRYPT System Domain, which any verifier checks offline. Which node carried a submission reaches the issuer and any verifier as the `node_attestation` of the proof, signed by the system domain.

---

## How it fits

```text
operator key (ML-DSA-65)
  → operator_id = "op:" + base64(SHA3-256(public key)[0..16])     derived, never assigned
  → operator.recognition/1 credential                              signed by the recognition sub-key
      checked by the fixation service on each submission, with a proof of possession
  → node_attestation.node_id in an independence proof              authentic through the proof signature
```

- The operator identifier is derived from the key. A new key is a new identifier.
- The credential has a finite validity window and no live revocation. The fixation service can stop admitting an operator earlier; that decision is internal to it.
- A verifier of an independence proof never consults the credential. A node's presence or absence does not condition `Independent`.

---

## Normative documents

- [Specification](./specification.md)

The specification defines:

- the operator key and the derivation of the operator identifier
- the credential object, its identifier and its signature
- how the fixation service resolves the recognition sub-key
- the validity window
- the proof of possession
- the checks the fixation service performs
- the domain separation of operator-key signatures
- the claims boundary

---

## Related documents

- [submission-set/1](../../../../protocols/settlement/submission-set/1/index.md)
- [independence.proof/1](../../../../models/independence.proof/1/index.md)
- [operator.domain-binding/1](../../operator.domain-binding/1/index.md)
- [system-domain/1](../../../../foundation/system-domain/1/index.md)

---

## Versioning

- **Specification identifier:** `operator.recognition`
- **Specification version:** `/1`

---

## One-line summary

`operator.recognition/1` lets the fixation service check that a node holds an operator key recognised under CERTCRYPT rules, and says nothing else about the operator.
