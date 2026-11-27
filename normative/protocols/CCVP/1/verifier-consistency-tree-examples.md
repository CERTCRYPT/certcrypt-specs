# CERTCRYPT Consistency Verification Protocol - Verifier Consistency Tree Examples (CCVP/1)

**Identifier:** CCVP/1/verifier-consistency-tree-examples

**Type:** Informative Protocol Artifact (Examples)

**Status:** Frozen

**Layer:** Layer 1 — Protocols

**Depends on:**

- [CCVP/1/verifier-consistency-tree](verifier-consistency-tree.md)

> This document is **informative**.

---

## Purpose

This document provides **informative examples** illustrating how the verifier consistency tree defined in [CCVP/1](specification.md) is applied in practice.

These examples are **non-normative** and are intended to clarify expected verifier behavior under common conditions.

Optional `policy_refs` carried by a context snapshot do not affect snapshot selection, binding, or consistency outcomes under CCVP/1.

If present, they remain informational only unless another applicable public specification explicitly defines additional semantics outside CCVP/1.

> **Note on timestamps used in examples**
>
> In all examples:
>
> - Certificate issuance time **T1** refers to `C.payload.anchor.issued_at`
> - Context snapshot time **T0 / T2** refers to `S.payload.snapshot.issued_at`
> - Timestamps are compared as instants, never as strings
> - `F_G` is the composite key fingerprint of the key of **G** (CCVP/1 Section 8.1), and **C** and every snapshot are `Issued`-valid unless stated otherwise

---

## Example 1 — context snapshot available, eligible issuer

**Scenario**

- Certificate **C** issued at time **T1**
- `C.payload.context.snapshot_issuer_id = G`
- `C.payload.context.snapshot_issuer_fingerprint_digest_hex = F_G`
- `C.payload.context.context_set_id = partner-context-eu`
- Context snapshot **S** issued at time **T0**, where `T0 < T1`
- Snapshot **S** is signed by the key of **G** (fingerprint `F_G`)
- `S.payload.snapshot.context_set_id = partner-context-eu`
- Snapshot **S** contains an active entry whose `issuer_id` is the `signer.id` of **C** and whose `pub_fingerprint_digest_hex` is the composite key fingerprint of the key that signed **C**

**Verification**

- Namespace selection resolves to `(G, F_G, partner-context-eu)`
- Snapshot selection chooses **S**
- Entry matching succeeds

**Result**

- outcome = `consistency-match`

---

## Example 2 — context snapshot available, issuer not listed

**Scenario**

- Certificate **C** issued at time **T1**
- `C.payload.context.snapshot_issuer_id = G`
- `C.payload.context.snapshot_issuer_fingerprint_digest_hex = F_G`
- `C.payload.context.context_set_id = partner-context-eu`
- Context snapshot **S** issued at time **T0**, where `T0 < T1`
- Snapshot **S** is signed by the key of **G** (fingerprint `F_G`)
- `S.payload.snapshot.context_set_id = partner-context-eu`
- Snapshot **S** does **not** contain any entry matching the issuer/key used by **C**

**Verification**

- Namespace selection resolves to `(G, F_G, partner-context-eu)`
- Snapshot selection chooses **S**
- No matching entry is found

**Result**

- outcome = `consistency-mismatch`

---

## Example 3 — snapshot effective only after the certificate

**Scenario**

- Certificate **C** issued at time **T1**
- `C.payload.context.snapshot_issuer_id = G`
- `C.payload.context.snapshot_issuer_fingerprint_digest_hex = F_G`
- `C.payload.context.context_set_id = partner-context-eu`
- The only available context snapshot **S** was issued at time **T2**, where `T2 > T1`
- Snapshot **S** is signed by the key of **G** (fingerprint `F_G`)
- `S.payload.snapshot.context_set_id = partner-context-eu`

**Verification**

- Namespace selection resolves to `(G, F_G, partner-context-eu)`
- No snapshot satisfies `S.payload.snapshot.issued_at <= C.payload.anchor.issued_at`

**Result**

- outcome = `consistency-unknown`

---

## Example 4 — no context snapshot provided

**Scenario**

- Certificate **C** issued at time **T1**
- `C.payload.context.snapshot_issuer_id = G`
- `C.payload.context.snapshot_issuer_fingerprint_digest_hex = F_G`
- `C.payload.context.context_set_id = partner-context-eu`
- No context snapshot certificates are available to the verifier

**Verification**

- Context snapshot collection yields no applicable snapshots

**Result**

- outcome = `consistency-unknown`

---

## Example 5 — key revoked after certificate issuance

**Scenario**

- Certificate **C** issued at time **T1**
- `C.payload.context.snapshot_issuer_id = G`
- `C.payload.context.snapshot_issuer_fingerprint_digest_hex = F_G`
- `C.payload.context.context_set_id = partner-context-eu`
- Snapshot **S1** issued at time **T0**, where `T0 < T1`, applies to the issuer/key
- Snapshot **S1** is signed by the key of **G** (fingerprint `F_G`)
- `S1.payload.snapshot.context_set_id = partner-context-eu`
- Snapshot **S2** issued at time **T2**, where `T2 > T1`, revokes the same key
- Snapshot **S2** is signed by the key of **G** (fingerprint `F_G`)
- `S2.payload.snapshot.context_set_id = partner-context-eu`

**Verification**

- Namespace selection resolves to `(G, F_G, partner-context-eu)`
- Snapshot selection chooses **S1** based on `S.payload.snapshot.issued_at <= C.payload.anchor.issued_at`
- Revocation in **S2** is not applicable retroactively

**Result**

- outcome = `consistency-match`

---

## Example 6 — certificate missing declared context namespace inputs

**Scenario**

- Certificate **C** issued at time **T1**
- One of `C.payload.context.snapshot_issuer_id`, `C.payload.context.snapshot_issuer_fingerprint_digest_hex` or `C.payload.context.context_set_id` is absent
- One or more context snapshot certificates may still be available to the verifier

**Verification**

- Preconditions fail to resolve an applicable declared context namespace
- Consistency verification terminates without snapshot selection

**Result**

- outcome = `consistency-unknown`

---

## Example 7 — conflicting snapshots at the same effective time

**Scenario**

- Certificate **C** issued at time **T1**
- `C.payload.context.snapshot_issuer_id = G`
- `C.payload.context.snapshot_issuer_fingerprint_digest_hex = F_G`
- `C.payload.context.context_set_id = partner-context-eu`
- Two context snapshots **S1** and **S2** are signed by the key of **G** (fingerprint `F_G`)
- `S1.payload.snapshot.context_set_id = partner-context-eu`
- `S2.payload.snapshot.context_set_id = partner-context-eu`
- `S1.payload.snapshot.issued_at = S2.payload.snapshot.issued_at = T0`, where `T0 < T1`
- `S1` and `S2` are both cryptographically valid but their governed snapshot JSON values differ

**Verification**

- Namespace selection resolves to `(G, F_G, partner-context-eu)`
- Snapshot selection finds more than one eligible snapshot with the same maximal effective context time
- Because the governed snapshot subjects are not canonical-byte identical, the situation is context equivocation

**Result**

- outcome = `consistency-unknown`

---

## Example 8 — snapshot from another key under the same label

**Scenario**

- Certificate **C** issued at time **T1**
- `C.payload.context.snapshot_issuer_id = G`
- `C.payload.context.snapshot_issuer_fingerprint_digest_hex = F_G`
- `C.payload.context.context_set_id = partner-context-eu`
- Context snapshot **S** issued at time **T0**, where `T0 < T1`, with `S.payload.snapshot.context_set_id = partner-context-eu`
- **S** is `Issued`-valid and its `signer.id` is `G`, but it is signed by another key, whose fingerprint is not `F_G`
- **S** contains an active entry matching the issuer and key of **C**

**Verification**

- **S** is outside the namespace: the snapshot issuer identity comes from the verified signature, label and key fingerprint together, and the fingerprint is not `F_G`
- No snapshot remains in the namespace

**Result**

- outcome = `consistency-unknown`

---

## Example 9 — entry restricted to another subject profile

**Scenario**

- Certificate **C** issued at time **T1**, whose only subject has profile `subject.binary/1`
- `C.payload.context.snapshot_issuer_id = G`
- `C.payload.context.snapshot_issuer_fingerprint_digest_hex = F_G`
- `C.payload.context.context_set_id = partner-context-eu`
- Context snapshot **S** issued at time **T0**, where `T0 < T1`, signed by the key of **G** (fingerprint `F_G`)
- The only entry of **S** that matches the issuer and key of **C** carries `scope.subject_profiles = ["subject.email/1"]`

**Verification**

- Snapshot selection chooses **S**
- The entry fails the scope constraint (CCVP/1 Section 7.3): **C** has no `subject.email/1` subject

**Result**

- outcome = `consistency-mismatch`

---

## Notes

- Consistency verification never affects cryptographic validity
- Absence of context snapshot data does not invalidate certificates
- Consistency outcomes apply **forward only**
- Consistency outcomes do not justify ranking context snapshot issuers

---

This document provides **illustrative examples only** for [CERTCRYPT Consistency Verification Protocol version CCVP/1](specification.md).

It introduces no normative requirements and does not alter verification semantics.
