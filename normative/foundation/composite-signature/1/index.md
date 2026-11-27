# composite-signature/1 · CERTCRYPT Composite Signature Profile

**Identifier:** `composite-signature/1`

**Label:** CERTCRYPT Composite Signature Profile (composite-signature/1)

**Page:** Informative version index

**Specification type:** Foundation Specification

**Layer:** Layer 0 — Foundation

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `composite-signature/1` are defined in [specification.md](./specification.md).
> In case of discrepancy, the normative specification prevails.

---

## What is `composite-signature/1`?

`composite-signature/1` defines the composite signature used by the CERTCRYPT permanent trust chain: every component (a classical signature and a post-quantum signature) signs the same domain-separated derived message `M'`, and the composite verifies only if ALL components verify (AND). It exists so that a CERTCRYPT signature stays non-forgeable under both a future quantum attacker (the post-quantum component is the floor) and a hypothetical classical break of the post-quantum scheme (the classical component is the hedge).

It does **not** define:

- key management or key rotation (see `system-manifest/1`)
- any artifact layout (the artifacts that carry composite signatures define their own object and signing targets)
- the ephemeral holder operation-key (Level-3) signature, which is ML-DSA-65 (pure), not composite

## Reading order

1. [overview.md](./overview.md) — informative orientation.
2. [specification.md](./specification.md) — the authoritative normative rules.
