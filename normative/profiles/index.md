# profiles · CERTCRYPT subject profiles

**Identifier:** `profiles`

**Type:** Profile Collection Index

**Layer:** Profiles

> This document is **informative**.
> Normative rules are defined only by the versioned profile documents listed below.

---

## Purpose

This page indexes the active CERTCRYPT subject-profile families.

Subject profiles define how each kind of subject material is reduced to deterministic canonical bytes under the active public rules.

## Active families

- [subject.binary](./subject.binary/index.md)
- [subject.collection](./subject.collection/index.md)
- [subject.text](./subject.text/index.md)
- [subject.email](./subject.email/index.md)
- [subject.context-snapshot](./subject.context-snapshot/index.md)
- [subject.ai-decision](./subject.ai-decision/index.md)

## Recommended reading order

1. [subject.binary](./subject.binary/index.md)
2. [subject.collection](./subject.collection/index.md)
3. [subject.text](./subject.text/index.md)
4. [subject.email](./subject.email/index.md)
5. [subject.context-snapshot](./subject.context-snapshot/index.md)
6. [subject.ai-decision](./subject.ai-decision/index.md)

## Boundary

Subject profiles define canonicalization boundaries only.
They do not define issuance, consistency outcomes, Proof of Independence, truth, or authority semantics by themselves.

## One-line summary

The CERTCRYPT profile layer defines how each supported kind of subject material becomes deterministic canonical bytes under the active public rules.
