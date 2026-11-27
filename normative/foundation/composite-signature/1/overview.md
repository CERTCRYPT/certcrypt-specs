# CERTCRYPT Composite Signature Profile (composite-signature/1) — overview

**Identifier:** `composite-signature/1`

**Label:** CERTCRYPT Composite Signature Profile (composite-signature/1)

**Page:** Informative overview

**Specification type:** Foundation Specification

**Layer:** Layer 0 — Foundation

**Status:** Frozen

**Depends on:**

- a post-quantum signature scheme (ML-DSA-65, FIPS 204)
- a classical signature scheme (ECDSA P-256 in the canonical profile; Ed25519 in the additional profile)
- a digest function (SHA3-256) for the derived-message and ECDSA pre-hash
- the carrying artifact's own canonical signing target (`payload_canon_digest_hex`)

> This document is **informative**.
> All normative rules are defined exclusively in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## Why composite

A CERTCRYPT certificate, foundation root, or `independence_proof` must stay non-forgeable indefinitely. Two independent risks bear on that:

- a future quantum computer breaks classical signatures (forge old artifacts);
- an undiscovered classical attack weakens the young post-quantum scheme.

A single-algorithm signature can only defend against one of these. The composite defends against both by requiring BOTH a post-quantum and a classical signature over the same message, with AND verification. The post-quantum component is the floor and can never be skipped; the classical component is the hedge.

## The inseparable-assertion property

The composite is not "two signatures side by side". Both components sign one derived message `M'`, and `M'` binds the profile identifier itself. As a consequence:

- a signature produced under one profile does not verify under another (no cross-profile reuse);
- a signature cannot be downgraded to a weaker profile or to a single component;
- there is no "classical-only" or "post-quantum-only" acceptance — only the whole composite is ever a verdict.

This is what distinguishes a composite from a naive hybrid: lifting one component out and replaying it alone does not produce a valid CERTCRYPT signature.

## What it is not

It is not key management, not an artifact format, and not a proof of independence. It does not make a leaf `Independent`. The ephemeral per-operation holder signature (Level-3) is deliberately ML-DSA-65 (pure), not composite, because it is single-use and not part of the permanent chain.

## Relationship to the IETF

This profile defines one inseparable assertion with AND semantics and anti-stripping. Adopting different component algorithm identifiers requires a new profile identifier or a successor specification and does not change this profile's meaning.
