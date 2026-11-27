# CERTCRYPT Aggregated Settlement Binding (settlement.binding/1)

**Identifier:** `settlement.binding/1`  

**Label:** CERTCRYPT Aggregated Settlement Binding (settlement.binding/1)  

**Type:** Ecosystem Specification

**Status:** Frozen

**Layer:** Layer 3 — Ecosystem

**Depends on:** See References *(active normative dependencies are listed below)*  

**Naming convention:**  
`settlement.binding/1` is the formal identifier.  
CERTCRYPT Aggregated Settlement Binding (settlement.binding/1) is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.  

**Audience:** Implementers, verifiers, ecosystem integrators, auditors  

**Purpose:** Define the substrate-independent cryptographic binding shared by every CERTCRYPT aggregated settlement profile.

**Intended use:** `settlement.binding/1` is intended to be the authoritative public specification for how an aggregated settlement container is bound, hashed, and proven — independently of which public ledger carries it.

**Scope:** Defines the anchor format, the Merkle derivations, the leaf-assignment interpretation, and the temporal property of aggregated settlement. It does NOT define how a settlement is carried on any particular substrate.

**Non-goals:** `settlement.binding/1` does not define a settlement event, a settlement reference, or a finality profile. Those are substrate-specific and belong to the settlement profile that selects this binding. It does not prove truth, semantic validity, or legal validity by itself.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale

CERTCRYPT settles consumed capacity by destroying supply on a public, permissionless ledger, and binds that settlement to an aggregated container of consumption records.

Two things happen in that sentence, and they are of different kinds:

- **The binding** — how a batch of consumption is aggregated, hashed into a Merkle root, and committed to an anchor. This is arithmetic over the batch's own data. No ledger is involved: every digest is computed before any transaction exists.
- **The carrying** — how that anchor reaches a public ledger, how the settlement is referenced, and what makes it final. This is entirely a property of the substrate.

This document defines the first. A **settlement profile** defines the second, and selects this binding by reference.

### 1.1 Why the separation is normative, not editorial

The binding is what a verifier recomputes offline. If two profiles stated it separately, a divergence between the statements would not surface as a specification conflict — it would surface as a digest that does not match, on a certificate that should have validated, possibly years later.

Stating it once removes that failure mode by construction. A profile that restates any derivation in this document, rather than referencing it, is non-conforming even if the restatement is currently identical.

### 1.2 What a profile still owns

This binding is deliberately incomplete on its own. A conforming settlement profile MUST additionally define, per `settlement-material/1` §6:

- the qualifying settlement event on its substrate
- the method for resolving `settlement_ref`
- the finality profile
- the capacity-consumption interpretation specific to its action shape
- the authorization-to-consumption bridge

A profile that selects `settlement.binding/1` inherits sections 5 through 9 of this document unchanged and MUST NOT vary them.

---

## 2. Scope

This specification defines:

- the batch binding anchor format and its canonical preimage
- the `settlement_root` derivation
- the `subtree_root` derivation
- the leaf-assignment interpretation
- the temporal property of aggregated settlement

It does not define, and a reader MUST NOT infer from it: the settlement event, the settlement reference, the finality profile, key custody, or any managed-service behavior.

---

## 3. Terminology

Terms not defined here carry the meaning assigned in `settlement-material/1`.

- **Settlement profile** — a specification that selects this binding and defines how settlement is carried on one substrate. It is identified by an exact `settlement_profile_id`.
- **Container** — one aggregated settlement: one anchor, one `settlement_root`, one or more leaves.
- **Leaf** — one issuer's consumption within a container, itself covering one or more commitments.

---

## 4. Design principles

- Every digest MUST be computable from the batch's own data alone, before any transaction exists.
- Canonical form MUST be exact: no field order, encoding, or padding may be left to implementation choice.
- The binding MUST be unique: one anchor MUST NOT validly apply to a second container.
- Failure MUST be closed: any derivation mismatch fails validation rather than degrading to a warning.

---

## 5. Batch binding anchor

Every aggregated settlement is bound by one exact anchor.

The anchor MUST equal:

```text
ccab1:<batch_binding_digest_hex>
```

Where `batch_binding_digest_hex` is the lowercase hexadecimal SHA3-256 digest of the UTF-8 bytes of the canonical JSON object:

```json
{
  "v": "ccab1",
  "system_id": "<system_id>",
  "rules_version": "<rules_version>",
  "settlement_profile_id": "<settlement_profile_id>",
  "batch_id": "<batch_id>",
  "window_id": "<window_id>",
  "leaf_count": "<leaf_count>",
  "total_quantity": "<total_quantity>",
  "settlement_root": "<settlement_root>"
}
```

Canonical JSON under this binding MUST:

- use UTF-8
- use LF line endings when materialized
- use object member order exactly as shown above
- contain no additional members
- encode all values as strings

### 5.1 The profile identifier is inside the digest

`settlement_profile_id` is a member of the preimage, so the anchor is **bound to the profile that produced it**. Two profiles settling the same batch produce different anchors, by construction.

This is intentional and MUST NOT be treated as an inconsistency: an anchor is evidence of a settlement under exact rules, and the rules are part of what is being committed to. It also means an anchor produced under one profile can never be replayed as evidence under another.

The `settlement_root` itself is NOT affected: it is derived from the batch's leaves and is identical across profiles for identical input.

### 5.2 Anchor placement

The profile MUST define where the anchor is carried on its substrate, and that placement MUST be immutable once the settlement is final. A placement that the settling party can later alter is not evidence.

### 5.3 Verifier obligations

The verifier MUST recompute `batch_binding_digest_hex` from `batch_binding_preimage` and reject the settlement context if:

- the anchor differs
- the digest differs
- the preimage fields differ from the claimed proof context
- the same anchor could validly apply to another `settlement_root`
- the same anchor could validly apply to another `batch_id`

This anchor binding is the exact batch-level binding.

No implementation MAY replace it with:

- node-local batch memory
- retry memory
- dashboard state
- managed-service assertions
- a weaker prefix match

---

## 6. `settlement_root` derivation

The exact `settlement_root` is the lowercase hexadecimal encoding of the Merkle root derived from the ordered batch leaves.

Leaves MUST be ordered by ascending `leaf_index` starting at `0`.

For each leaf, the canonical `leaf_preimage` object MUST be:

```json
{
  "v": "ccab1-leaf",
  "system_id": "<system_id>",
  "rules_version": "<rules_version>",
  "settlement_profile_id": "<settlement_profile_id>",
  "batch_id": "<batch_id>",
  "leaf_index": "<leaf_index>",
  "subtree_root": "<subtree_root>",
  "cost_commitment": "<cost_commitment>",
  "consumed_quantity": "<consumed_quantity>"
}
```

Canonical JSON for this preimage MUST follow the same rules as §5 (UTF-8, LF, exact member order as shown, no additional members, string values).

Leaf and node derivation MUST be:

- `leaf_hash = SHA3-256(0x00 || canonical_leaf_preimage_bytes)`
- `parent_hash = SHA3-256(0x01 || left_child_hash || right_child_hash)`

When a tree level has odd cardinality, the final child on that level MUST be promoted unchanged to the next level.

It MUST NOT be duplicated, rehashed alone, or paired with itself.

The `cost_commitment` carried in the `leaf_preimage` is opaque to this binding beyond its inclusion in the canonical leaf bytes. Its value is the digest defined by [submission-set/1 §13.2](../../../../protocols/settlement/submission-set/1/specification.md); this binding neither recomputes its preimage nor defines its contents. A producer MUST derive `cost_commitment` per that section; any divergence surfaces as a `leaf_hash` mismatch under the derivation above.

The `sibling_hashes` array in `submission_assignment_proof` MUST be ordered bottom-up, starting from the leaf level and ending at the final level below the root.

At each level, the verifier MUST interpret the current level using the exact current width derived from `leaf_count`.

`leaf_count` is the value of `batch_binding_preimage.leaf_count`, which the anchor of §5 binds. A width carried anywhere else — in `independence_proof.batch.size` (outside its signed view) or in `batch_manifest` — is accepted only when it equals that value, and the claimed `leaf_index` MUST be lower than it. A verifier MUST NOT derive the width from any other source.

If the current node is the odd rightmost node of that level, that level contributes no sibling-hash entry and the current hash is promoted unchanged.

Otherwise:

- if the current node index is even, the current node is the left child and the sibling hash is the right child
- if the current node index is odd, the current node is the right child and the sibling hash is the left child

No implementation MAY treat sibling order as unspecified, transport-dependent, or heuristically recoverable.

The `settlement_root` in `batch_manifest`, `batch_binding_preimage`, and any dependent proof material MUST match exactly.

`batch_manifest` is not covered by the anchor of §5. Every member it shares with `batch_binding_preimage` MUST equal the preimage's value exactly: the preimage carries the anchored values, and the manifest's copies are accepted only when they repeat them. A verifier MUST NOT take any of them from the manifest.

---

## 7. `subtree_root` derivation

A leaf's `subtree_root` is the lowercase hexadecimal Merkle root over the commitments accepted into that leaf, ordered by ascending `commitment_index` starting at `0`. A leaf MUST cover at least one accepted commitment.

For each accepted commitment, the canonical commitment leaf preimage MUST be:

```json
{
  "v": "ccab1-commit",
  "commitment_id": "<commitment_id>"
}
```

Canonical JSON for this preimage MUST follow the same rules as the batch leaf preimage (UTF-8, LF, exact member order as shown, no additional members, string values).

Under the zero-data capacity profile, the `commitment_id` in this preimage is the commitment's `capacity_evidence_digest` (`capacity.evidence/1 §7.1`): the commitment has no other public identifier in that profile (`capacity.commitment/1` §15), so the evidence digest is the identifier under which the commitment is admitted to the leaf. A verifier evaluating a certificate under this profile MUST require the supplied capacity evidence to recompute to the `commitment_id` carried in its inclusion path, binding the evidence to the exact commitment the leaf admitted.

Commitment leaf and node derivation MUST reuse the exact rules of §6:

- `commitment_leaf_hash = SHA3-256(0x00 || canonical_commitment_leaf_preimage_bytes)`
- `parent_hash = SHA3-256(0x01 || left_child_hash || right_child_hash)`
- odd rightmost child promoted unchanged

This is the same Merkle construction as the batch level; the two levels differ only in what they hash. A single-commitment leaf's `subtree_root` is that one commitment leaf hash.

The `commitment_siblings` array in `commitment_inclusion_proof` MUST be ordered bottom-up against this sub-tree, under the same odd-promotion interpretation as §6. The verifier MUST recompute `commitment_leaf_hash` from `commitment_id` and reject the path if the recomputed leaf hash, the inclusion path, or the resulting root differs from the `subtree_root` the proof anchors.

If any root derivation step differs, validation MUST fail.

This Merkle construction is specialized to aggregated settlement containers.

It MUST NOT be assumed to be interchangeable with subject-level collection commitment schemes such as `collection.merkle-sha3-256/1`, which use different leaf models, binding fields, and proof interpretation boundaries.

---

## 8. Leaf assignment interpretation

This binding is aggregated.

Accordingly:

- one settlement MAY settle multiple leaves
- one valid proof path MUST still correspond to one and only one claimed `subtree_root`
- the `inclusion_proof` MUST determine one exact membership path
- the `leaf_preimage` MUST bind one exact `subtree_root`

The verifier MUST reject any context in which:

- the same `leaf_preimage` could validly support another leaf assignment
- the same `settlement_ref` and `inclusion_proof` could support another plausible container interpretation
- the same `subtree_root` could be assigned to more than one leaf under the same claimed container without the exact rules permitting and uniquely resolving that assignment

---

## 9. Temporal property

The temporal property of aggregated settlement is an attribute of the **settlement of consumed capacity**, not an assertion about a document.

- The sole temporal authority is `finality_proof.block_timestamp`: the consensus time of the final inclusion unit on the substrate. It is established by the public settlement record, not by the issuing system. The issuing system MUST NOT be treated as a source of time for this property, and a time value asserted by the issuing system MUST NOT be required for, or alter, normative evaluation.
- From that time, an issuer derives one — and only one — temporal claim about a certificate whose capacity was consumed in the settlement: that the certificate is **not later than** that instant (an upper bound on the certificate's age). This binding does NOT establish that a document existed at a given time; it does NOT bind, hash, or anchor certificate or subject content into the settlement record. The settlement record binds the aggregated consumption (`settlement_root`), never per-certificate content.
- Non-retroactivity: `block_timestamp` MUST NOT be after the commitment's `expires_at` (`capacity.commitment/1` §11.2). A settlement whose final inclusion time is after the commitment's expiry MUST fail validation. The verifier evaluates this exclusively from `block_timestamp`, not from any issuing-system clock.

Any future second finality witness admitted into the proof material (multi-substrate hardening) MUST be another public, permissionless record under the same rule; a qualified-authority or accredited time-attestation service MUST NOT be admitted as a temporal witness.

The profile defines what "final inclusion unit" means on its substrate, and how its consensus time is obtained and normalized to UTC.

---

## 10. Failure semantics

Any of the following MUST cause validation to fail:

- an anchor that does not equal the recomputed binding
- a preimage whose fields differ from the claimed proof context
- an anchor that could validly apply to another `settlement_root` or `batch_id`
- a Merkle path that does not resolve
- a `subtree_root` that does not match its recomputed commitment tree
- a leaf assignment that is not uniquely determined
- a `block_timestamp` after the commitment's `expires_at`

A verifier MUST NOT downgrade any of these to a warning, and MUST NOT accept a binding provisionally pending later confirmation.

---

## 11. Conformance

An implementation conforms to `settlement.binding/1` if and only if it:

- computes the anchor exactly per §5
- computes `settlement_root` exactly per §6
- computes `subtree_root` exactly per §7
- interprets leaf assignment per §8
- evaluates the temporal property per §9
- fails closed on every condition of §10

An implementation supporting more than one settlement profile MUST produce identical `settlement_root` values for identical batch input under every profile. It MUST NOT be expected to produce identical anchors: §5.1 binds the anchor to the profile.

---

## 12. Versioning & extensibility

A change to any derivation in this document is a new version, never an amendment. Existing anchors are evidence, and evidence cannot be re-derived.

A settlement profile references an exact version of this binding. A profile that references `settlement.binding/1` MUST NOT be interpreted under any later version.

### 12.1 Evidence is evaluated under the substrate its rules domain selects

The binding is the anchor and its Merkle derivations, and neither mentions a
chain. What a substrate contributes is the carrying — how the anchor reached a
public ledger and what made it final — and that contribution is complete once the
settlement is final.

A verifier MUST therefore evaluate a settlement under the settlement profile its
**rules domain** selects, not under whichever substrate a system settles on at the
time of verification. A rules domain selects exactly one settlement profile, so
the substrate a settlement was carried on is always answered by the artifacts
themselves.

Evaluation is offline (`settlement-material/1` §4): it never requires the
substrate to be reachable. A rules domain that selects another substrate is a
successor rules domain ([rules-domain/1](../../../../foundation/rules-domain/1/specification.md) §9) and leaves
evidence produced under its predecessor evaluable under the predecessor's rules.

---

## 13. References

- `settlement-material/1` — the material contract this binding is carried in
- `submission-set/1` §13.2 — the derivation of `cost_commitment`
- `capacity.evidence/1` §7.1 — the evidence digest used as `commitment_id` under the zero-data profile
- `independence.proof/1` — the proof this settlement supports
- [capacity.commitment/1 — CERTCRYPT Capacity Commitment Specification](../../capacity.commitment/1/index.md)
- [collection.merkle-sha3-256/1 — CERTCRYPT Merkle Collection Commitment Scheme](../../../../protocols/commitment/collection.merkle-sha3-256/1/index.md)
- [rules-domain/1 — CERTCRYPT Rules Domain](../../../../foundation/rules-domain/1/index.md)
