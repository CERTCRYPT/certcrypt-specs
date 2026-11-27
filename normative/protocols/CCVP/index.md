# CCVP · CERTCRYPT Consistency Verification Protocol Family

**Identifier:** `CCVP`

**Type:** Protocol Family Index

**Layer:** Layer 0-2 — Protocols

> This document is **informative**.
> Normative rules are defined only by the versioned documents listed below.

---

## Purpose

This page is the public family index for `CCVP`.

It identifies the versioned documents that currently define this CERTCRYPT family and points readers to each version's entry point.

## Versions

| Version | Status | Entry point |
|---|---|---|
| `CCVP/1` | Frozen (optional plane) | [CCVP/1](./1/index.md) |

## Boundary

CCVP defines declared-context consistency evaluation only. It is an optional verification plane: it does not determine subject accuracy, certificate issuance, settlement, or Proof of Independence evaluation, and its outcome never changes an `Issued` or `Independent` verdict.

## One-line summary

**CCVP is the protocol family for declared-context consistency evaluation at issuance time.**
