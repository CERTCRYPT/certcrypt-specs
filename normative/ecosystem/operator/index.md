# operator · CERTCRYPT ecosystem · operator category

**Identifier:** `ecosystem/operator`

**Type:** Ecosystem Category Index

**Layer:** Ecosystem

> This document is **informative**.
> Normative rules are defined only by the versioned documents listed below.

---

## Purpose

This page indexes the operator-layer artifacts of the CERTCRYPT ecosystem.

Operator specifications define the credential by which a node shows that its operator key is recognised under CERTCRYPT rules (`operator.recognition/1`) and the optional declaration by which an operator can be associated with an HTTPS origin (`operator.domain-binding/1`).

## Active families

- [operator.recognition](./operator.recognition/index.md)
- [operator.domain-binding](./operator.domain-binding/index.md)

## Recommended reading order

1. [operator.recognition](./operator.recognition/index.md)
2. [operator.domain-binding](./operator.domain-binding/index.md)

## Boundary

Operator specifications concern the relation between issuers, nodes and the fixation service. They define no registry of operators, are not inputs to the verification of an independence proof, and do not rate, rank or endorse operators.

## One-line summary

The operator category defines how a node shows its recognised operator identity and how an operator may be associated with an HTTPS origin, without any role in verification.
