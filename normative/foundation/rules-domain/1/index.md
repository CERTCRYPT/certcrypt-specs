# rules-domain/1 · CERTCRYPT Rules Domain

**Identifier:** `rules-domain/1`

**Label:** CERTCRYPT Rules Domain Specification (rules-domain/1)

**Page:** Informative version index

**Specification type:** Foundation Specification

**Layer:** Layer 0 — Foundation

**Status:** Frozen

> This document is **informative**.
> The normative requirements for `rules-domain/1` are defined by its [Specification](./specification.md).
> In case of discrepancy, the specification prevails.

---

## What is `rules-domain/1`?

`rules-domain/1` defines how CERTCRYPT implementations determine the exact public ruleset under which an artifact, proof, or evaluation context is interpreted.

It does not define:

- system identity
- truth semantics
- proof validity by itself
- settlement execution
- capacity authorization or consumption

It defines:

- exact rules-domain identity
- deterministic rules-domain selection
- rejection of heuristic, fallback, or parser-dependent rule choice
- the boundary for equivalence and successor-rule handling
- cross-artifact rule-domain consistency requirements

---

## Role within CERTCRYPT

Within the CERTCRYPT foundation:

- `system-domain` defines which system is being evaluated
- `rules-domain` defines which exact public rules govern that evaluation
- `security-model` defines which foundational properties must hold under those rules

`rules-domain/1` is therefore the bridge between system attribution and normative evaluation.

Under the active public corpus, `rules-domain/1` publishes its concrete rules-domain instances as registry entries under [`system-domain/1/registry/certcrypt/rules/`](../../system-domain/1/registry/certcrypt/rules/index.md). The registered instance is:

- [`rules/2026-01`](../../system-domain/1/registry/certcrypt/rules/2026-01.md)

Only registry entries listed in this section are registered under the active corpus. Any unlisted `rules_version` MUST NOT be accepted by conforming verifiers.

---

## Normative documents

- [Specification](./specification.md)

---

## See also

- [Overview](./overview.md)
- [system-foundation/1](../../system-foundation/1/specification.md)
- [system-domain/1](../../system-domain/1/specification.md)
- [security-model/1](../../security-model/1/specification.md)

---

## Versioning

- **Identifier:** `rules-domain/1`

Version `rules-domain/1` defines the active public contract for this document. Any non-backward-compatible semantic or structural change requires a new major version.

## One-line summary

`rules-domain/1` defines how CERTCRYPT selects and constrains the exact public rules under which artifacts are evaluated.
