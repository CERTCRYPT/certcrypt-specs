# system-domain/1 · registered system domains

**Identifier:** `system-domain/1/registry`

**Type:** System-Domain Registry Index

**Layer:** Foundation

> This document is **informative**.
> Normative rules for the registered instances are defined exclusively in their respective registry entries listed below.

---

## Purpose

This page indexes the system-domain instances registered under
[system-domain/1](../specification.md) for the active CERTCRYPT public corpus.

Each registered entry defines the concrete parameters of one system domain: its
`system_id`, its bootstrap root material, the `system-foundation/1` statement
that materializes it, and the rules versions it publishes.

The separation is deliberate. `system-domain/1` defines what a system domain is
and how attribution to one is validated; it holds the parameters of none. A
generic specification carrying one installation's root fingerprint would also
carry that installation's lifecycle state, and a second domain could not be
registered without editing the model.

## Active registered instances

- [`certcrypt`](certcrypt/index.md)

## Boundary

Only registry entries listed in this page are registered under the active corpus.
Any unlisted `system_id` MUST NOT be accepted as a registered system domain: it
is a distinct external system under [system-domain/1](../specification.md)
Section 13, whatever document structures or field names it reuses.

A registered entry's bootstrap is immutable once frozen. Root rotation is
expressed through `system-manifest/1`, never by editing an entry — a rotation
must be provable, not declared.

## One-line summary

**The system-domain registry indexes the concrete system domains registered under
`system-domain/1` for the active CERTCRYPT public corpus, of which `certcrypt` is
currently the only registered entry.**
