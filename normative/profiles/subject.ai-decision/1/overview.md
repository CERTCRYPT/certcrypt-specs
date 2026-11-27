# CERTCRYPT AI-Decision Subject Canonicalization Profile (`subject.ai-decision/1`) — overview

**Identifier:** `subject.ai-decision/1`

**Label:** CERTCRYPT AI-Decision Subject Canonicalization Profile v1

**Page:** Informative overview

**Specification type:** Profile Specification

**Layer:** Layer 2 — Profiles

**Status:** Frozen

**Depends on:**
- [system-domain/1](../../../foundation/system-domain/1/index.md)
- [rules-domain/1](../../../foundation/rules-domain/1/index.md)
- [security-model/1](../../../foundation/security-model/1/index.md)
- [CCCP/1](../../../protocols/CCCP/1/index.md)
- [CCSP/1](../../../protocols/CCSP/1/index.md)

> This document is **informative**.
> The normative requirements for `subject.ai-decision/1` are defined exclusively in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `subject.ai-decision/1`?

`subject.ai-decision/1` defines how a record of one AI decision is reduced to deterministic canonical bytes under CERTCRYPT public rules.

It exists for the case where an issuer wants to commit to the exact, structured circumstances it observed for one model invocation and decision — which declared model, under which bound parameters, over which ordered inputs, producing which ordered outputs, by which actor, at which instant, and at which observation boundary — so any party can later verify that record against the held material.

The record is a JSON object. Its canonical bytes are the UTF-8 of its RFC 8785 (JCS) serialization. Every scalar value is a string; the only arrays are the ordered `input` and `output` descriptor arrays. The exact object shapes, array bounds, identifiers, per-part nonces and commitments, media types, profiles, timestamp and total canonical size are checked before anything is hashed.

---

## What it commits, and what it does not

It commits **the circumstances**:

- the declared model (`id`, `provider`, optional `version`)
- whether the record observes the invocation at the `client` or `runtime` boundary
- the invocation `parameters` the issuer chose to bind
- one or more ordered inputs and outputs, each as a closed material descriptor with `id`, `role`, `media_type`, `profile`, `material_nonce_hex` and `commitment_digest_hex` — never the content
- the stable issuer-declared `decision_id`, the outcome label (`decision`), the decision instant (`decided_at`), and optionally the observed start (`started_at`), opaque `context`, `actor_id` and `policy_ref`

It does **not** commit, assert, or imply:

- that the decision is correct, fair, lawful, or unbiased
- that the provider or model identity is authenticated, or that hidden provider/runtime behavior was observed
- that the model is accurate or safe
- that re-running the model would reproduce the output
- any evaluation of the decision's merit

This is the verification-versus-evaluation boundary: CERTCRYPT can make it independently checkable that *this exact record — this declared model, observation scope, ordered content descriptors, actor handle, and outcome — was committed under these rules*. It does not judge the decision itself or prove that the declared model caused the output.

---

## Why salted commitments, not content

The input and output materials stay out of the certificate. The issuer binds only their descriptors and salted commitments; the materials are presented later as verifier-held original material (verifier-toolkit/1 §8.5). This keeps AI-decision certification compatible with CERTCRYPT's zero-data architecture: the protocol never holds the decision's content.

Every input and output part is canonicalized under the `profile` in its descriptor and reduced to `subject_local_digest_hex = SHA3-256(canonical_bytes(material))`. That digest is not embedded. Instead, an independently generated 32-byte `material_nonce_hex` and the CCCP/1 commitment `SHA3-256(ASCII(material_nonce_hex) || ASCII(subject_local_digest_hex))` are embedded. A verifier reuses the same per-profile canonicalization and CCCP/1 commitment machinery to recompute and compare.

A verifier that holds any declared part delivers it with the record under that part's globally unique `id`, and the verifier toolkit derives and compares its part commitment under the declared profile (verifier-toolkit/1 §8.5.6). The profile is one of `subject.text/1`, `subject.binary/1`, `subject.email/1` or `subject.ai-decision/1`. A collection is not supported because its root depends on the certificate nonce that carries it, while nested material has no certificate nonce.

The record has collection-like ordered-part semantics, but it is NOT `subject.collection/1`: JCS over the complete record binds descriptor order and cardinality without a Merkle root, and there is no element-inclusion proof. One record remains one non-collection economic unit for one observable invocation and decision.

The disclosed record contains each salt and commitment. A recipient can therefore test guessed candidate material; salting does not make low-entropy material confidential. Fresh, independently generated nonces prevent a stable cross-record fingerprint for the same material absent nonce reuse, and duplicate material nonces inside a record are rejected.

The record is also suitable as a technical evidence artifact for logging, traceability, human-oversight review and audit workflows: it binds a stable issuer-declared decision identifier and what the issuer observed and chose to record at a precise boundary. It does not establish that any legal logging, oversight, documentation, risk-management, retention, impact-assessment or audit obligation was satisfied, and it carries no jurisdiction-specific compliance field.

---

## Worked example

A decision record. The prompt and the output are synthetic `subject.text/1` materials; their descriptors carry distinct synthetic material nonces and the corresponding CCCP/1 commitments:

```json
{
  "profile": "subject.ai-decision/1",
  "decision_id": "synthetic-event-01",
  "decided_at": "2026-06-17T10:30:00.000Z",
  "started_at": "2026-06-17T10:29:58.000Z",
  "model": {
    "id": "synthetic-model",
    "provider": "synthetic-runtime",
    "version": "synthetic-model-v1"
  },
  "observation_scope": "client",
  "parameters": {
    "temperature": "0.0",
    "max_tokens": "4096",
    "top_p": "0.95"
  },
  "context": {
    "case_ref": "synthetic-case-01",
    "oversight_route": "synthetic-route-01"
  },
  "input": [
    {
      "id": "prompt",
      "role": "user",
      "media_type": "text/plain",
      "profile": "subject.text/1",
      "material_nonce_hex": "5f4775fbfb02640a026c6478ca4621c966d143c4de56d9a967d620f2e76ba623",
      "commitment_digest_hex": "7004872e8bd94944e730be517ce5f7fa15da9fdf4af0e7ff1d69083b6bfc61be"
    }
  ],
  "output": [
    {
      "id": "result",
      "role": "assistant",
      "media_type": "text/plain",
      "profile": "subject.text/1",
      "material_nonce_hex": "50b2f5bea4b03cca160d70476c1a57f6e63d3239eec7c4075e0758b343e3b066",
      "commitment_digest_hex": "c933ea2ce3977a2454fc8da3ae921fbc2cbe8eb018ab037d1497800f6712056d"
    }
  ],
  "decision": "category-a"
}
```

Every identifier, reference, material value, nonce and commitment in this example is a synthetic public fixture and denotes no real provider, model, person, case or decision. The prompt is `Classify synthetic sample alpha.` and the output is `label: category-a`; their exact canonical bytes, part commitments and the record commitment are pinned in [specification.md](./specification.md) §8.1.

---

## One-line summary

**`subject.ai-decision/1` records one observable model invocation and decision as deterministic canonical bytes — committing the declared model, observation boundary and ordered material descriptors, never whether the decision was right.**
