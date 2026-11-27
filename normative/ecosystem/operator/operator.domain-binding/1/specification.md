# CERTCRYPT Operator Domain Binding Specification (operator.domain-binding/1)

**Identifier:** `operator.domain-binding/1`

**Label:** CERTCRYPT Operator Domain Binding Specification (operator.domain-binding/1)

**Type:** Ecosystem Specification

**Status:** Frozen

**Layer:** Layer 3 — Ecosystem

**Depends on:** `operator.recognition/1`, `CCCP/1`

**Naming convention:**
`operator.domain-binding/1` is the formal identifier.
CERTCRYPT Operator Domain Binding Specification (operator.domain-binding/1) is the human-readable label.

**Audience:** Node operators, implementers of services that display operator association, auditors, third parties that hold independence proofs.

**Purpose:** Define an optional, mutual declaration between a node's operator key and an HTTPS origin, by which a node operator can be associated with that origin's host name; how the declaration is signed, published and checked; and what a service that displays such an association may and may not say.

**Intended use:** A node operator that wants to be recognisable publishes a statement signed by its operator key on an HTTPS origin it controls. Anyone holding the operator identifier — for example from the `node_attestation` of an independence proof — can check that the origin and the key declare each other.

**Scope:** Defines the binding statement, its signature and identity, its validity and sequencing, its publication under `/.well-known/`, the checks a third party performs, the requirements on a service that displays the association, and the security considerations for fetching. It does not define any service's internal schedule or storage.

**Non-goals:** The binding is not identity proofing, endorsement, certification or rating of an operator. It is not part of an independence proof and plays no role in its verification.

> This document is **normative**.
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale

An independence proof may name, in its `node_attestation`, the operator identifier of the node that carried the submission (`independence.proof/1` §10.15). The identifier is stable for as long as the operator keeps its key, so an operator that wants to be recognisable can make it known. This specification gives that a verifiable form.

The binding is **mutual**:

- the **operator key** signs a statement naming the domain (§6), so no domain can claim a node that did not consent;
- the **domain** publishes that statement on its HTTPS origin (§8), so no node can claim a domain that did not consent. TLS validation under the Web PKI authenticates the origin's host name.

The coincidence of both is a technical association of a key with an origin. It is not a statement about the legal identity of whoever operates the node.

Binding is optional. A node without a binding operates, transports and appears in proofs exactly as one with a binding.

---

## 2. Conformance

A conforming node MUST produce statements exactly as defined here.
A conforming third party and a conforming displaying service MUST perform every check of §9 and MUST fail closed: when any check fails, no association exists.

---

## 3. Invariants with respect to independence proofs

`operator.domain-binding/1`:

- is not a member of `independence_proof` and is not part of its signed view;
- is not an input to `verification-package/1`;
- is not an input, check, result code or verdict of any verifier conforming to `verifier-toolkit/1`;
- MUST NOT change the result of verifying any independence proof, whether a binding exists, does not exist, has expired, or cannot be fetched;
- does not alter `node_attestation`, which keeps exactly `node_id` and `recognized_at` (`independence.proof/1` §10.15).

---

## 4. The binding statement

A statement is a JSON object with exactly the following members:

| Member | Type | Content |
|---|---|---|
| `artifact_type` | string | `"operator.domain-binding/1"` |
| `intent` | string | `"bind"` or `"unbind"` (§7.3) |
| `domain_binding_method` | string | `"https-well-known"` (§8) |
| `operator_id` | string | The operator identifier (`operator.recognition/1` §3.2) |
| `operator_public_key` | string | The operator public key, standard base64 (`operator.recognition/1` §3.1) |
| `domain_ascii` | string | The bound host name (§5) |
| `sequence` | string | Decimal sequence number (§7.2) |
| `issued_at` | string | RFC 3339 UTC with whole seconds (`YYYY-MM-DDTHH:MM:SSZ`) |
| `valid_until` | string | Same format (§7.1) |
| `signature_alg` | string | `"ml-dsa-65-fips204-v1"` |
| `signature_b64` | string | The signature (§6), standard base64 |

No other member MAY appear. A consumer MUST reject a statement with a missing member, an additional member, a duplicate member name, a member of the wrong type, or a value outside the ones listed.

`domain_binding_method` MUST equal `"https-well-known"` in `/1`. Any other value MUST be rejected. The member is part of the signed payload, so the node fixes the method under its signature and no consumer can substitute another.

---

## 5. The bound host name

`domain_ascii` is a fully qualified host name in its ASCII form:

- produced from the operator's input by IDNA processing under UTS #46 with non-transitional processing, `CheckHyphens`, `CheckBidi`, `CheckJoiners`, `UseSTD3ASCIIRules` and `VerifyDnsLength` all enabled;
- every label in its A-label form, all lowercase, without a trailing dot;
- the exact name declared. It is never reduced to a registrable domain or extended to a parent: `node.example.org` and `example.org` are different bindings.

A consumer MUST reject a `domain_ascii` that:

- is empty, or is an IP address literal in any form;
- is a single label, or falls under a top-level name that never resolves in the public DNS: `localhost` and `invalid` and `test` (RFC 6761), `local` (RFC 6762), `arpa` including `home.arpa` (RFC 8375), `onion` (RFC 7686), `alt` (RFC 9476), and `internal` (reserved by ICANN for private use);
- has an all-numeric top-level label;
- contains a wildcard label, an underscore, a control or bidirectional formatting character, or anything that is not valid under the processing above;
- is itself a public suffix in the ICANN section of the Public Suffix List.

The name is not the address of the node. It is the name under which the operator chooses to be associated; the node itself is never contacted (§10.4).

---

## 6. Signature and identity

The **signed payload** is the RFC 8785 (JCS) canonical form of the statement without `signature_alg` and `signature_b64`:

```text
signed_payload_jcs = JCS( statement − {signature_alg, signature_b64} )
signed message     = "certcrypt:operator-domain-binding:1|" || signed_payload_jcs
```

The prefix is the ASCII bytes shown. The signature is an ML-DSA-65 signature (FIPS 204) by the operator key over the signed message. This context is registered in `operator.recognition/1` §10 and MUST NOT be signed in any other form.

The statement's identity is the pair (`operator_id`, `sequence`) together with:

```text
statement_digest = SHA3-256( signed_payload_jcs )
```

A consumer verifies a statement with the key it carries: it decodes `operator_public_key`, recomputes `operator_id` from it (`operator.recognition/1` §3.2), rejects the statement if they differ, and verifies the signature under that key. No registry is needed.

---

## 7. Validity, sequencing and intent

### 7.1 Validity

`issued_at` MUST be strictly earlier than `valid_until`. For `intent = "bind"`, `valid_until` MUST NOT be more than 90 days after `issued_at`. A consumer MUST reject a `bind` statement outside its window, and a statement whose `issued_at` lies in the future beyond a tolerance of five minutes.

### 7.2 Sequence

`sequence` is a decimal string without leading zeros, from `"1"` up to `"9007199254740991"` (2^53 − 1). It orders the statements of one operator identifier.

A party that keeps state about an operator identifier — such as a displaying service — MUST apply, for each statement it accepts:

| Received | Result |
|---|---|
| `sequence` equal to an accepted one, same `statement_digest` | idempotent: nothing changes, also when `sequence` is lower than the highest accepted |
| `sequence` equal to an accepted one, different `statement_digest` | rejected as a conflict |
| `sequence` lower than the highest accepted for that `operator_id`, and equal to none accepted | rejected |
| `sequence` higher than the highest accepted | accepted as a candidate |

The rows are read in this order and the first that applies decides. A statement already accepted can therefore be presented again at any time without effect, whatever was accepted after it.

An accepted statement consumes its sequence number even if it never becomes effective. A node MUST keep its sequence durably with its key, and MUST never reuse or decrease it.

### 7.3 Intent

- `bind` declares that the operator key is associated with `domain_ascii` from the moment the binding is first verified (§10).
- `unbind` withdraws the association of the operator key with `domain_ascii`, and only to that name. It never opens an association. Its `valid_until` limits the time during which it may first be accepted; once accepted, its effect is permanent and an expired `unbind` never revives a binding. A service MAY refuse an `unbind` for a host name the operator key never bound: there is nothing to withdraw.

---

## 8. Publication

### 8.1 Location and format

The statement is published at:

```text
https://<domain_ascii>/.well-known/certcrypt-node.json
```

The resource is a JSON object with exactly one member, `bindings`, an array of one to eight statements. The body MUST NOT exceed 65 536 bytes after any content decoding.

Every element of `bindings` MUST be a well-formed statement: exactly the members of §4, each of its type, and no duplicate member name. A resource with any element that is not is malformed as a whole, and no statement in it matches (§8.3). The other checks of §4 to §7.1 — values, host name, signature, validity — decide only whether a given statement matches.

The origin MAY list statements of more than one operator identifier — for example two during a change of operator key, each signed by its own key. A host name is associated with at most one active binding per operator identifier.

### 8.2 Fetching rules

A party that fetches the resource MUST:

- use `https` on port 443 to exactly `domain_ascii`, with that name for SNI and certificate validation, and validate the certificate chain under the Web PKI;
- refuse any redirection;
- refuse the fetch when the name resolves to any address that is not publicly routable (§13.1);
- refuse a body over the limit of §8.1 and any JSON with duplicate member names.

### 8.3 Matching

A statement in the resource matches when its `domain_ascii` equals the fetched host name, its signature verifies (§6), and it is within its validity (§7.1). Other statements in the resource are ignored.

A party that looks for one statement, identified by its `statement_digest`, and finds an entry with that digest which does not match — its signature does not verify, or it fails a check of §4 to §7.1 such as an `issued_at` beyond the tolerance — treats the resource as **malformed** for that statement. That is an unknown state: the origin serves the statement's bytes in a form that cannot be checked, which is neither a successful check nor evidence that the statement was withdrawn (§10.2). An entry with that digest whose only defect is that `valid_until` has passed is outside its validity; the association already ended at `valid_until` (§10.2).

---

## 9. Checks

To establish that an operator identifier is bound to a host name, a party MUST, fail-closed:

1. Fetch the resource of §8 under the rules of §8.2.
2. Find a matching statement (§8.3) whose `operator_id` is the identifier in question and whose `intent` is `bind`.
3. If the party keeps state for that identifier, apply the sequence rules of §7.2 and check that no accepted `unbind` with a higher sequence names the same host name.

**Freshness limit.** A party without state — for example one that checks a binding for the first time — cannot know whether a statement with a higher sequence was accepted elsewhere. It can establish that the origin currently serves a valid statement signed by the key, not that this statement is the latest. `valid_until` bounds that exposure; it does not remove it.

---

## 10. Requirements on a displaying service

A service that displays an operator association derived from this specification MUST meet the following requirements.

### 10.1 Coverage in time

- An association starts at the first successful check of §9 after the statement was accepted, never at `issued_at`, and is never extended backwards.
- A service SHOULD keep checking the operator's newest accepted statement, if it is a `bind` that is still valid and whose host has not yet served it, at a bounded interval, so that serving the resource later starts the association without a new statement. Until then nothing is associated.
- An item processed at instant `t` (for example a submission received from the node) is associated with the host name only if an association interval `[effective_from, coverage_until)` contains `t`. Intervals are half-open; at most one host name is associated per operator identifier and instant.
- After a gap in successful checks longer than the service's grace period, a later successful check opens a new interval from that check; the gap stays unassociated.
- The grace period MUST be finite. During it, an association may outlive a withdrawal the service has not yet observed; the service MUST state its grace period in its documentation.
- An association already shown for a past item MUST NOT change because of later renewals, withdrawals or fetch failures. It MAY be withdrawn only by an authenticated, auditable correction (for example after a key compromise), and the service MUST keep a record of every such correction.

### 10.2 Ending an association

An interval ends:

- at once, when an `unbind` for the host name is accepted;
- at the binding's `valid_until`;
- when a fetch over valid TLS returns HTTP 410 for the resource;
- when the matching statement is absent (HTTP 404, or a valid resource that carries no entry with its `statement_digest`) in two observations separated by at least 30 minutes; the interval ends at the second observation;
- when the grace period after the last successful check runs out;
- when the service stops admitting the operator, for example when the integration under which it transports is deactivated, or when its `operator.recognition/1` credential is no longer valid.

A timeout, a server error, or a DNS or TLS failure is not evidence of withdrawal: it neither ends nor extends an interval. Neither is a resource that is malformed — one refused under §8.1 or §8.2, or malformed for the statement under §8.3: it neither ends nor extends an interval, and the grace period applies.

### 10.3 Presentation

- The host name is shown in its A-label form, left-to-right, as text, never as a link.
- It is shown as neutral secondary text, for example `Operator domain: node.example.org`. It MUST NOT be shown as a badge, seal, check mark, colour, icon, ordering preference or any other visual distinction, and MUST NOT be described as verified, official, approved or certified.
- Every operator is presented the same way, including any operated by CERTCRYPT.
- The absence of a binding MUST NOT be marked in any way.
- The method of §4 MUST NOT be shown.

### 10.4 Independence from the node

- The service never contacts the node to check a binding: it fetches the host name's origin. A node on a private network can be bound to a public host name.
- No synchronous path of the service (receiving submissions, answering reads) may depend on fetching a binding.
- The service MUST NOT offer a public lookup from operator identifier to host name.

---

## 11. Claims boundary

The binding associates an operator key with an HTTPS origin. It MUST NOT be presented as proof of the legal identity of an operator, or as approval, certification, validation or endorsement of an operator, of its infrastructure, or of the issuers whose submissions it carries. A host name under a public suffix of a multi-tenant platform is associated exactly as declared and says nothing about the platform.

---

## 12. Privacy

Publishing a binding makes the relation between an operator identifier and a host name public, and lets anyone holding several proofs carried by the same node relate them to that host name. An operator that does not want that relation known publishes no binding. Nothing in a statement reveals the network location of the node.

---

## 13. Security considerations

### 13.1 Fetching

Any recognised operator can cause a fetcher to request a public host name of its choice, on port 443 and a fixed path. A fetcher MUST treat this as untrusted outbound traffic. Beyond §8.2 it SHOULD: disable environment and system proxies; pin the connection to the validated address and check the peer address; reject private, loopback, link-local, shared (CGNAT), NAT64, IPv4-embedded IPv6, multicast, unspecified, documentation and reserved ranges; disable automatic decompression or bound the decoded size; bound header size and read time; send no cookies or credentials; limit concurrency globally and per host; and enforce the same address rules at the network level.

### 13.2 Look-alike names

Displaying A-labels prevents a Unicode look-alike of a host name from being shown as the original.

### 13.3 Replay and rollback

A stateful party rejects any sequence below the highest accepted (§7.2). A stateless party is subject to the freshness limit of §9, bounded by `valid_until`.

### 13.4 Key compromise

Whoever holds an operator key can sign `bind` and `unbind` statements for it, but can only obtain an association for a host name whose origin it controls. When an operator key is compromised, the operator stops using it and the service stops admitting it (§10.2); associations made during the exposure may be withdrawn by an auditable correction (§10.1). The operator binds its new key, which has a new identifier, again.

---

## 14. Non-goals

This specification does **not** define:

- identity proofing of organisations
- a registry or directory of operators or of host names
- the internal schedule, storage or interfaces of a displaying service
- binding methods other than `https-well-known`
- any reputational, commercial or quality signal about operators

---

## 15. Versioning

- **Specification identifier:** `operator.domain-binding`
- **Specification version:** `/1`

Admitting a new value of `domain_binding_method`, or changing the member set, the signed message, the sequence rules, the publication location or the coverage requirements, requires a new major version once this specification is frozen.

---

## 16. Wire format

The published resource, with abbreviated values:

```json
{
  "bindings": [
    {
      "artifact_type": "operator.domain-binding/1",
      "intent": "bind",
      "domain_binding_method": "https-well-known",
      "operator_id": "op:<22 characters>",
      "operator_public_key": "<standard base64 of 1952 bytes>",
      "domain_ascii": "node.example.org",
      "sequence": "7",
      "issued_at": "2026-11-18T10:00:00Z",
      "valid_until": "2027-02-16T10:00:00Z",
      "signature_alg": "ml-dsa-65-fips204-v1",
      "signature_b64": "<standard base64>"
    }
  ]
}
```

---

## 17. References

- [operator.recognition/1](../../operator.recognition/1/index.md)
- [independence.proof/1](../../../../models/independence.proof/1/index.md)
- [verification-package/1](../../../verification/verification-package/1/index.md)
- [verifier-toolkit/1](../../../verification/verifier-toolkit/1/index.md)
- [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../../../protocols/CCCP/1/index.md)
- [RFC 8785 — JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785)
- [RFC 8615 — Well-Known Uniform Resource Identifiers](https://www.rfc-editor.org/rfc/rfc8615)
- [RFC 6761 — Special-Use Domain Names](https://www.rfc-editor.org/rfc/rfc6761)
- [RFC 6762 — Multicast DNS](https://www.rfc-editor.org/rfc/rfc6762)
- [RFC 7686 — The ".onion" Special-Use Domain Name](https://www.rfc-editor.org/rfc/rfc7686)
- [RFC 8375 — Special-Use Domain 'home.arpa.'](https://www.rfc-editor.org/rfc/rfc8375)
- [RFC 9476 — The .alt Special-Use Top-Level Domain](https://www.rfc-editor.org/rfc/rfc9476)
- [UTS #46 — Unicode IDNA Compatibility Processing](https://www.unicode.org/reports/tr46/)
- [Public Suffix List](https://publicsuffix.org/)
- [FIPS 204 — Module-Lattice-Based Digital Signature Standard](https://csrc.nist.gov/pubs/fips/204/final)
