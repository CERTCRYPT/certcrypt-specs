# CERTCRYPT Email Subject Canonicalization Profile (`subject.email/1`)

**Identifier:** `subject.email/1`

**Label:** CERTCRYPT Email Subject Canonicalization Profile v1

**Type:** Profile Specification

**Status:** Frozen

**Layer:** Layer 2 — Profiles

**Depends on:**
- [system-domain/1](../../../foundation/system-domain/1/index.md)
- [rules-domain/1](../../../foundation/rules-domain/1/index.md)
- [security-model/1](../../../foundation/security-model/1/index.md)
- [CCCP/1](../../../protocols/CCCP/1/index.md)
- [CCSP/1](../../../protocols/CCSP/1/index.md)

**Naming convention:**  
`subject.email/1` is the formal identifier.  
CERTCRYPT Email Subject Canonicalization Profile v1 is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.

**Audience:** Protocol implementers, verifiers, auditors

**Purpose:** Define the normative subject-profile canonicalization semantics for `subject.email/1` within the active CERTCRYPT public architecture.

**Intended use:** `subject.email/1` is intended to be the authoritative public specification for deriving deterministic `canonical_bytes(subject)` for subjects declaring this profile under CERTCRYPT public rules.

**Scope:** Defines canonicalization boundaries, allowed transformations, and interpretation limits for `subject.email/1`; higher-layer proof, settlement, and consistency semantics remain out of scope except where explicitly referenced.

**Non-goals:** `subject.email/1` does not prove truth, semantic validity, legal validity, issuer authenticity, or Proof of Independence by itself, and MUST NOT be interpreted as a trust mark, notarization mechanism, or live service authority.

> This document is **normative**.
> All requirements expressed using MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in RFC 8174.

---

## 1. Background & rationale
`subject.email/1` defines how complete email-message subjects are reduced to deterministic `canonical_bytes(subject)` under CERTCRYPT public rules.

It exists to provide a narrowly bounded email canonicalization profile for complete messages that can safely be treated under explicit RFC 5322-oriented rules without semantic reinterpretation.

The profile defines canonicalization only.

It does not define:

- issuance semantics
- independence semantics
- consistency semantics
- verification-package semantics
- settlement or capacity semantics
- sender authenticity, delivery evidence, or institutional endorsement

---

## 2. Scope

`subject.email/1` defines:

- the acceptable input boundary for one complete email message
- deterministic header and body canonicalization rules
- the exact transformations permitted for stable canonical bytes
- the boundary between profile-level verification and higher-layer evaluation

`subject.email/1` does not define:

- envelope structure
- hashing algorithm choice
- commitment construction
- sender identity, delivery, receipt, or mailbox semantics
- proof-of-existence, notarization, or timestamping semantics

Those concerns remain defined elsewhere in the architecture.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

Additional terms:

- **Message:** One complete RFC 5322 email message represented as bytes.
- **Headers:** The header section ending at the first header/body delimiter.
- **Body:** The byte sequence after the header/body delimiter, which may be empty.
- **Canonical bytes:** The deterministic byte sequence produced by this profile.
- **CR:** Carriage Return (`0x0D`).
- **LF:** Line Feed (`0x0A`).
- **CRLF:** The byte sequence `0x0D 0x0A`.
- **WSP:** Space (`0x20`) or horizontal tab (`0x09`).

---

## 4. Design principles

`subject.email/1` is designed around the following principles:

- **Bounded message model:** The profile applies to one complete email message under a narrow, explicit input boundary.
- **Deterministic canonicalization:** Equivalent valid inputs under this profile MUST converge on the same `canonical_bytes(subject)`.
- **Minimal normalization:** Only the transformations explicitly defined by the profile MAY be applied; semantic reinterpretation of message meaning is forbidden.
- **Zero-data by design:** Certificates derived from this profile MUST remain compatible with a zero-data architecture.
- **Proof without data custody:** Verification depends on the certificate, public rules, and the verifier-held original message, not on platform-held mailbox or custody systems.
- **Interpretation boundaries:** This profile defines canonicalization only. It does not prove sender identity, delivery, truth, or independence.

---

## 5. Profile-specific rationale

Exports of the *same emitted message* by different local tooling may differ because of:

- line-ending differences across platforms and export tools
- RFC 5322 header folding applied at different points by different export libraries
- an added, removed, or repeated final line terminator on save

Raw byte hashing of email without bounded canonicalization can therefore produce unnecessary divergence across these environments. This profile reconciles exactly those three benign differences (§11.2, §11.4, §11.5) and no others; transit mutation (relay-added headers, re-encoding) and message regeneration are out of scope by design (§12.1).

`subject.email/1` defines a conservative canonicalization model that:

- requires one complete message as input
- applies deterministic global line-ending normalization
- treats headers and body through explicit, bounded rules
- avoids semantic MIME or mailbox reinterpretation
- remains reproducible offline

---

## 6. Architectural role

`subject.email/1` is subordinate to the current architecture:

- `system-domain/1` determines which system is being evaluated
- `rules-domain/1` determines which exact public rules apply
- `security-model/1` defines the interpretation and fail-closed boundary
- `CCCP/1` defines canonicalization contexts, hashing, and commitment semantics
- `CCSP/1` defines certificate envelope structure

Under `/1`, this profile contributes only `canonical_bytes(subject)`.

It MUST NOT be interpreted as sufficient to establish:

- `Issued`
- `Independent`
- settlement validity
- consistency outcomes
- truth of issuer assertions

No implementation MAY present `subject.email/1` as a standalone proof, trust mark, or notarization mechanism.

---

## 7. Canonicalization constraints

`subject.email/1` is governed by:

- determinism
- minimal explicit normalization
- cross-tool reproducibility
- bounded envelope treatment
- no semantic MIME reserialization
- offline reproducibility
- strict separation from higher-layer meaning

Only explicitly defined transformations are permitted.

---

## 8. Relationship to CCCP and CCSP

`subject.email/1` is a subject-specific profile under [CCCP/1](../../../protocols/CCCP/1/index.md).

Its output constitutes `canonical_bytes(subject)` for use by CCCP-governed hashing and commitment construction.

`subject.email/1` MUST NOT redefine, weaken, or bypass any CCCP requirement.

When referenced from certificates serialized under [CCSP/1](../../../protocols/CCSP/1/index.md), the subject's declared `profile` identifies this specification and nothing more: it confers no authority and asserts nothing about the subject's content.

The presence of `subject.email/1` in a certificate envelope does not upgrade the envelope into any specific higher-layer meaning.

---

## 9. Subject informational attributes

A certificate or higher-layer artifact MAY carry informational attributes associated with a `subject.email/1` subject.

Such attributes:

- MUST be informational only
- MUST NOT affect `canonical_bytes(subject)`
- MUST NOT participate in CCCP commitment computation unless another normative specification explicitly says so
- MUST NOT be used to infer semantic equivalence, truth, or authority

Profile conformance MUST be determined from the message bytes and declared profile only, not from informational metadata.

---

## 10. Input constraints

For `subject.email/1`, the subject input MUST be the exact byte sequence of one complete RFC 5322 message.

The input MUST NOT include enclosing container or transport bytes such as:

- mbox separator lines (the line beginning with the five bytes `46 72 6f 6d 20`, i.e. `From` followed by SP) and mbox extraction padding
- `.emlx` framing (the leading byte-count line and the trailing property-list metadata)
- Maildir metadata
- JSON export wrappers
- HTTP response framing
- API envelope objects
- mailbox database records
- SMTP transparency and end-of-`DATA` framing (dot-stuffing of body lines beginning with `.`, and the terminating `CRLF . CRLF`)

Extraction from an mbox store MUST reverse the store's `From`-quoting convention where that convention is known (mboxrd, in which a body line matching one or more `>` characters followed by `From` and SP is un-quoted by removing one leading `>`); where the quoting convention is unknown (mboxo, which does not reverse), the extraction does not establish the exact message byte stream and MUST NOT be claimed as such.

Implementations MUST NOT reconstruct the message from:

- parsed mailbox objects
- decoded MIME trees
- header maps
- body text strings
- character-decoded intermediates
- non-byte-identical storage abstractions

A MIME stream generated on demand from a store that does not retain the message as MIME is a reconstruction under this section, **even when the platform labels it "original" or serves it as an `.eml` download**. This includes, without limitation: Microsoft Graph `GET /messages/{id}/$value`, EWS `MimeContent`, Exchange-backed IMAP/POP, and webmail "download" features that serialize server-side from a MAPI/property store; and clients that rebuild cleartext MIME from an encrypted or decomposed store. Such a stream is not the exact message byte stream, need not be byte-stable across server versions, and MUST NOT be presented as a `subject.email/1` subject; if the exact regenerated bytes are to be certified, they are their own [subject.binary/1](../../subject.binary/1/index.md) subject with no claim of equivalence to any other copy.

A stored copy into which a mail store or client has injected metadata header fields — for example `X-Mozilla-Status`, `X-Mozilla-Status2`, `X-Mozilla-Keys`, `Status`, `X-Status`, `X-UID`, `X-IMAPbase`, `X-Keywords`, or a store-added `Content-Length` — is not the exact byte sequence of the message. Implementations MUST NOT present such a copy as the certified subject's original material and MUST NOT remove the injected fields to "repair" it (removing headers is non-conformant, §13); an issuance workflow SHOULD capture the message before store injection (for example via a raw IMAP fetch rather than extraction of the on-disk store file).

If an implementation cannot establish the exact message byte stream, it MUST NOT claim deterministic `subject.email/1` canonicalization of that input.

If a workflow cannot safely establish a complete message under these rules, implementations MUST use [subject.binary/1](../../subject.binary/1/index.md) instead.

The requirements of this section constrain the acquisition of the input and are not observable from `canonical_bytes(subject)` alone: a black-box comparison of input and output cannot tell whether the bytes were a faithful capture or a byte-identical reconstruction. Conformance testing under this profile therefore covers §11 only; conformance to this section is asserted by the implementer. This profile performs no container sniffing and does not itself reject a malformed or contaminated input — establishing that the input is the exact message byte stream is the caller's responsibility.

---

## 11. Canonicalization model

`subject.email/1` canonicalizes a message in five steps, applied strictly in order:

1. global line-ending normalization (§11.2)
2. header/body split (§11.3)
3. header unfolding (§11.4)
4. body trailing-terminator normalization (§11.5)
5. final assembly (§11.6)

This model is intentionally conservative. It normalizes only what is required to achieve stable canonical bytes and does not interpret meaning, validate authenticity, or reserialize MIME structures. Each step is a byte procedure operating on raw bytes; implementations MUST NOT decode to a platform string type and re-encode if that round trip can alter bytes.

Canonicalization is idempotent: applying §11 to a value already produced by §11 MUST reproduce it unchanged.

### 11.1 Definitions

- **CR** = `0x0D`; **LF** = `0x0A`; **CRLF** = `0x0D 0x0A`.
- **WSP** = a single SP (`0x20`) or HTAB (`0x09`) byte; no other byte (e.g. VT `0x0B`, FF `0x0C`, NBSP, Unicode spaces) is WSP.
- The input is treated as raw bytes; it is NOT required to be valid UTF-8 (CCCP/1 §6.2 — the `subject` context is an opaque byte sequence; CCCP/1 §5.1's UTF-8/BOM rules govern CCCP-defined textual/JSON contexts, not this input).
- No byte is stripped or transcoded. In particular a leading UTF-8 BOM (`0xEF 0xBB 0xBF`) is preserved as the first three bytes of the input and becomes part of the first header field; a BOM (or any charset transcoding) is evidence that a text editor re-saved the artifact, so such an input should be treated as failing the §10 boundary rather than silently normalized.

### 11.2 Global line-ending normalization

Normalize every line ending to CRLF across the entire message with a single left-to-right scan over the **original** bytes, never re-reading emitted bytes. At each position `i`:

1. if the next two bytes are `0x0D 0x0A` (CRLF): append `0x0D 0x0A`, advance by 2;
2. else if the next byte is `0x0D` (lone CR): append `0x0D 0x0A`, advance by 1;
3. else if the next byte is `0x0A` (lone LF): append `0x0D 0x0A`, advance by 1;
4. else: append the byte unchanged, advance by 1.

This step is byte-level and MUST NOT depend on MIME interpretation or character decoding. It applies to the whole message including the body; a body carrying binary or encoded content whose line endings differ is therefore normalized. If byte-exact preservation of arbitrary binary content is required, use [subject.binary/1](../../subject.binary/1/index.md) instead.

This step reconciles only single line breaks each represented as one of `CR`, `LF`, or `CRLF`. It does **not** reconcile a rewrite that represents one line break as more than one break — for example a double conversion that turns each `CRLF` into `CR CR LF`, which this scan expands into two `CRLF` sequences and which can therefore shift where the first `CRLF CRLF` delimiter falls (§11.3). Such a rewrite is a different subject, and the profile does not pretend otherwise.

### 11.3 Header and body split

Let `M` be the output of §11.2. Split `M` at the **first** occurrence of `CRLF CRLF` (`0x0D 0x0A 0x0D 0x0A`):

- `headers` = the bytes before that first `CRLF CRLF` (no trailing CRLF; the full four-byte delimiter is removed from both sides);
- `body` = the bytes after that first `CRLF CRLF`.

Only the first `CRLF CRLF` is the delimiter. Any further CRLF bytes belong to the body and MUST be preserved; implementations MUST NOT consume additional blank lines.

If `M` contains no `CRLF CRLF`, then `headers` = `M` and `body` is empty.

A message beginning with `CRLF CRLF` has an empty `headers` section; this is in-boundary and canonicalizes normally.

### 11.4 Header unfolding

Apply unfolding to the `headers` section **only** (never to the body, and never across the delimiter). This is exactly the unfolding of RFC 5322 §2.2.3: scan `headers` left to right; each time a `CRLF` is immediately followed by a WSP byte, delete that `CRLF` (the two bytes `0x0D 0x0A`) and preserve the following WSP byte or bytes unchanged. The `CRLF` is removed; the WSP that RFC 5322 folding inserted the `CRLF` in front of is retained byte-for-byte, including its identity (SP vs HTAB) and run length. A `CRLF` that is not immediately followed by a WSP byte is preserved. WSP that precedes a `CRLF` (trailing whitespace on a line) is not part of a fold and MUST be preserved.

This rule is the exact inverse of RFC 5322 folding, which inserts a `CRLF` immediately before an existing WSP. Two independently produced foldings of the same header that each insert `CRLF` before existing WSP therefore unfold to the identical bytes. The rule intentionally does **not** collapse or rewrite the WSP itself: a header carrying `"a" HTAB "b"` and its folded form `"a" CRLF HTAB "b"` both unfold to `"a" HTAB "b"`, preserving the HTAB. (§12.2 states the boundary of what this reconciles and what it does not.)

Implementations MUST also:

- preserve header field order exactly as supplied;
- preserve header field names and values as bytes except for the unfolding above;
- NOT semantically decode, reinterpret, validate, or rewrite header values or names;
- NOT add, remove, synthesize, or reorder header fields.

Header-field-name syntax is not parsed: unfolding is purely byte-mechanical and identifies no field boundaries. A malformed header section is not rejected by this profile; it is unfolded and assembled as-is.

### 11.5 Body trailing-terminator normalization

Apply this step to the `body` from §11.3 **only** (never to `headers`, and never to the delimiter). Let `B` be the §11.3 `body`:

- if `B` is empty, it is unchanged (empty);
- otherwise, remove every trailing `CRLF` from the end of `B` (a maximal run of zero or more `CRLF` sequences at the end), then append exactly one `CRLF`.

The effect is that a non-empty body ends in exactly one `CRLF` regardless of whether the supplied export omitted the final line terminator, included exactly one, or included several (for example the extra blank line a naive mailbox-container extractor leaves before the next record). This is the single benign difference most likely to arise between two exports of the identical emitted message, and it is the only body transformation this profile performs; the interior bytes of the body are otherwise preserved exactly (§11.2 line-ending normalization aside).

This step applies to the body as one opaque byte run. If byte-exact preservation of a body whose meaningful content ends without a `CRLF`, or whose trailing blank lines are significant, is required, use [subject.binary/1](../../subject.binary/1/index.md) instead.

### 11.6 Final assembly

Canonical bytes are assembled by exact byte concatenation:

```text
canonical_bytes(subject) = headers_unfolded || CRLF CRLF || body_terminated
```

where `headers_unfolded` is the §11.4 output, `body_terminated` is the §11.5 output (possibly empty), and the delimiter is exactly the four bytes `0x0D 0x0A 0x0D 0x0A`. The delimiter is always present, even when `headers_unfolded` is empty, even when `body_terminated` is empty, and even when the input had no `CRLF CRLF` (a headers-only message gains the delimiter and an empty body in its canonical form).

Two independently conforming implementations given the same input bytes MUST produce identical `canonical_bytes(subject)`.

### 11.7 Conformance vectors

The following input → output pairs are normative; a conforming implementation MUST reproduce each exactly. Bytes are space-separated lowercase hex.

| input | canonical output |
|---|---|
| `41 3a 62 0d 0a 0d 0a 63` (`"A:b" CRLF CRLF "c"`) | `41 3a 62 0d 0a 0d 0a 63 0d 0a` |
| `41 3a 62 0a 0a 63` (`"A:b" LF LF "c"`) | `41 3a 62 0d 0a 0d 0a 63 0d 0a` |
| `41 3a 62` (`"A:b"`, no delimiter) | `41 3a 62 0d 0a 0d 0a` |
| `41 3a 62 0d 0a 20 63 0d 0a 0d 0a 64` (`"A:b" CRLF SP "c" CRLF CRLF "d"` — folded header, SP preserved) | `41 3a 62 20 63 0d 0a 0d 0a 64 0d 0a` |
| `41 3a 62 0d 0a 09 63 0d 0a 0d 0a 64` (`"A:b" CRLF HTAB "c" CRLF CRLF "d"` — folded at HTAB, **HTAB preserved**) | `41 3a 62 09 63 0d 0a 0d 0a 64 0d 0a` |
| `41 3a 62 0d 0a 20 20 09 63 0d 0a 0d 0a` (`"A:b" CRLF SP SP HTAB "c" CRLF CRLF` — the fold's whole WSP run is preserved; the delimiter is the final CRLF CRLF, so the body is empty) | `41 3a 62 20 20 09 63 0d 0a 0d 0a` |
| `0d 0a 0d 0a 62 6f 64 79` (`CRLF CRLF "body"` — empty headers) | `0d 0a 0d 0a 62 6f 64 79 0d 0a` |
| `41 3a 62 0d 0a 0d 0a 0d 0a 63` (`"A:b" CRLF CRLF CRLF "c"` — 3 CRLFs; body `CRLF "c"` gains one trailing CRLF) | `41 3a 62 0d 0a 0d 0a 0d 0a 63 0d 0a` |
| *(empty input, 0 bytes)* | `0d 0a 0d 0a` |
| `0d 0d` (lone `CR CR` → two line breaks → delimiter) | `0d 0a 0d 0a` |
| `0a 0d` (`LF CR` → two line breaks, not one) | `0d 0a 0d 0a` |
| `41 3a 62 0d 0d 0a 42 3a 63 0d 0d 0a 0d 0d 0a 64` (double-conversion `\r\r\n`: §11.2 makes each `CR CR LF` two CRLFs, so the first `CRLF CRLF` falls after `"A:b"` and `"B:c"` becomes body) | `41 3a 62 0d 0a 0d 0a 42 3a 63 0d 0a 0d 0a 0d 0a 0d 0a 64 0d 0a` |
| `41 3a 62 0d 0a 20 63` (folded header, **no** delimiter → whole input is headers) | `41 3a 62 20 63 0d 0a 0d 0a` |
| `41 3a 62 0d 0a 20 0d 0a 0d 0a 63` (fold run truncated by end of headers: `CRLF SP` then the delimiter) | `41 3a 62 20 0d 0a 0d 0a 63 0d 0a` |
| `41 3a 62 0d 0a 0d 0a 20 63` (SP after the delimiter belongs to the body; **no** unfolding) | `41 3a 62 0d 0a 0d 0a 20 63 0d 0a` |
| `41 00 42` (embedded NUL preserved; no delimiter) | `41 00 42 0d 0a 0d 0a` |
| `41 3a 62 0d 0a 0d 0a` (a value already produced by §11 — idempotence) | `41 3a 62 0d 0a 0d 0a` |

The last vector illustrates idempotence (§11): re-canonicalizing a canonical value reproduces it. Note that the empty input, `CR CR`, and `LF CR` all converge on `0d 0a 0d 0a`; this is intended.

---

## 12. What this profile certifies: the message as bytes, at emission

This profile canonicalizes **one exact message byte sequence**. It is essential to understand which byte sequence that is, because it determines what a certificate over a `subject.email/1` subject does and does not establish.

### 12.1 The subject is the emitted message, not the received one

`subject.email/1` certifies the message **as the issuer canonicalized it at emission time** — the exact `.eml` the issuer held and committed to. It is NOT designed to reconcile a sender's message with a copy reconstructed from a recipient's mailbox after transport.

This is a deliberate design choice between two incompatible goals, not an accident. A message is transformed in transit: each relay prepends `Received:` headers; gateways rewrite `Content-Type` boundaries, re-encode bodies between `base64` and `quoted-printable`, re-wrap or re-fold headers, and add `DKIM-Signature:`, `Authentication-Results:`, `X-*`, and `Return-Path:` lines.

- **Cross-hop stability** — making a sent message and a transit-mutated copy hash alike — is achievable, but only by *discarding* the volatile parts: an allowlist of stable headers, lowercased field names, collapsed whitespace, reordered fields (the approach DKIM takes for the subset it signs). The cost is **lossy**: the canonical object is no longer the message, but a projection of it, from which the original bytes cannot be recovered.
- **Forensic fidelity** — the canonical object IS the message, recoverable byte-for-byte except for (i) the `CR`/`LF`/`CRLF` flavor of each line break, (ii) the presence and position of RFC 5322 header folds, and (iii) the number of trailing `CRLF` sequences after the body — requires preserving every header and the body as delivered to the profile. The cost is that a transit-mutated copy will not match. Because §11.4 preserves the folding whitespace itself (SP vs HTAB, run length), the residual loss is only the fold positions, not the header content; a message the issuer already canonicalized at emission is its own canonical form.

`subject.email/1` chooses **forensic fidelity**: it preserves the complete supplied message (§13) and commits those exact bytes. This is consistent with CERTCRYPT's material-in-hand model (§12.3) — the holder presents the exact certified `.eml`, so a lossy projection would buy stability the model does not need while destroying the fidelity it does. A workflow that genuinely needs cross-hop reconciliation is choosing the other trade-off and belongs to a different, allowlist-based profile, not to `subject.email/1`.

### 12.2 What the canonicalization does buy

The line-ending normalization (§11.2), header unfolding (§11.4), and body trailing-terminator normalization (§11.5) are not aimed at transit. They reconcile the **benign** differences that arise when the *same emitted message* is stored, exported, and re-opened across tools: a `.eml` whose `CRLF`s became `LF`s in one editor; whose headers were re-folded by one export library inserting a `CRLF` before existing whitespace (RFC 5322 §2.2.3 folding, which §11.4 inverts exactly); or which acquired or lost a final line terminator on save. Within that boundary — the same message, re-serialized by different local tooling in those three specific ways — any two conforming toolkits in any language converge on the same `canonical_bytes` (the §11.7 vectors pin this). That is the determinism this profile guarantees, and the whole of it.

It does **not** reconcile transformations that alter bytes beyond those three. In particular, the following produce a different `canonical_bytes` and indicate the export tooling regenerated rather than re-serialized the message: a re-fold that inserts a `CRLF` and whitespace where the original had **no** whitespace (encoded-word re-chunking, forced folding of an over-long unbreakable token, comma-folding of an address list that adds a space); a re-fold that adds or changes whitespace **adjacent to** existing whitespace, changing the run length; any MIME re-encoding, boundary rewrite, or header reordering. These are the mark of a regenerated message stream (§10), not of the same message stored differently.

### 12.3 Consequence for verification (the material model)

Because the subject is the emitted bytes, the original material a verifier needs for complete verification (verifier-toolkit/1 §8.5, §15) is **that exact emitted `.eml`**, delivered out of band alongside the certificate — not a message pulled from a mailbox after delivery. Under that model the profile serves anyone who holds the certified `.eml`, consistent with CERTCRYPT's zero-data, material-in-hand architecture: CERTCRYPT never retains the message; the holder presents it. A verifier presented with a transit-mutated copy will, correctly, compute a different digest — the copy is a different byte sequence, and the profile does not pretend otherwise.

If a workflow needs to certify "the email a recipient received," that is a different subject (the recipient's exact received bytes, certified as ITS own `subject.email/1` or `subject.binary/1` subject), not a reconciliation with the sender's.

Emission capture is only correct at a point where the issuer possesses the exact message byte stream: a message the issuer itself serialized as MIME, the byte stream submitted over SMTP, or a store that returns the message byte-faithfully (for example a mailbox that serves the stored raw RFC 5322 bytes over IMAP or an equivalent raw-retrieval API). A client or API that holds the message as a non-MIME item and regenerates MIME on demand does not provide such a point unless its contract guarantees byte-faithful retention of the emitted stream. The same applies to a webmail download or to any client that rebuilds MIME from an encrypted or decomposed store (§10). Such an issuer must capture the message where it authored or submitted it, or certify the exact regenerated bytes under [subject.binary/1](../../subject.binary/1/index.md) with no claim that they match any other copy.

A conforming verifier toolkit MUST support `subject.email/1` original material (verifier-toolkit/1 §8.5.2). It recomputes `canonical_bytes` under §11 and applies the original-material comparison defined by verifier-toolkit/1 §8.5.2. A toolkit MUST NOT return `UNSUPPORTED` merely because the declared profile is `subject.email/1`.

---

## 13. Header treatment boundary

`subject.email/1` does not attempt to infer which headers are operationally meaningful or disposable.

Under `/1`, the canonicalization boundary is the complete supplied message.

This means:

- header presence in the supplied message remains part of the subject boundary
- deterministic canonicalization is preferred over any heuristic attempt to reconstruct an imagined “true” email
- parser-dependent header selection, header dropping, or mailbox-policy cleanup is non-conformant

The profile MUST NOT be implemented as:

- “keep whatever headers seem meaningful”
- “drop whatever looks volatile”
- “use local policy to decide retained fields”
- “repair the message into a cleaner email before canonicalizing”

Any such heuristic behavior is non-conformant.

---

## 14. Forbidden transformations

Implementations applying `subject.email/1` MUST NOT:

- decode MIME entities and then reserialize them
- normalize or reinterpret structured payloads embedded in the message
- use mailbox metadata as message content
- add, drop, or reorder headers based on local policy
- infer semantic equivalence between different messages
- treat canonicalization as proof of sender authenticity
- treat canonicalization as proof of delivery, receipt, acceptance, or mailbox policy outcome
- market the profile as notarization, anchoring, or timestamping

`subject.email/1` defines canonicalization only.

---

## 15. Verification boundary

Profile-level verification under `subject.email/1` is limited to verifying that:

- the declared `profile` is `subject.email/1`
- the supplied bytes are processed under the exact canonicalization rule defined here
- the resulting canonical bytes are the bytes expected by the applicable higher-layer path

This profile does not define a standalone verifier outcome taxonomy for `Issued` or `Independent`.

Those outcomes are defined by higher-layer public rules and verifier behavior, including:

- [security-model/1](../../../foundation/security-model/1/index.md)
- [verification-package/1](../../../ecosystem/verification/verification-package/1/index.md)
- [verifier-toolkit/1](../../../ecosystem/verification/verifier-toolkit/1/index.md)

No implementation MAY claim profile success under `subject.email/1` as if that alone established valid independence, truth, or authority.

---

## 16. Anti-notarization boundary

`subject.email/1` MUST NOT be described, implemented, or marketed as a notarization, timestamping, anchoring, or proof-of-existence system.

This profile:

- does not prove that a message existed at a time
- does not prove that a message is true
- does not prove that a message is authoritative
- does not prove `Independent`

It defines only how a complete email message is transformed into deterministic canonical bytes for use by higher-layer CERTCRYPT semantics.

If a system can reproduce the same claim using only `hash + anchor + verify`, that claim does not come from `subject.email/1` as defined here.

---

## 17. Security & interpretation boundaries

`subject.email/1`:

- does not prove sender identity
- does not prove authorship
- does not prove delivery
- does not prove receipt
- does not prove legal validity
- does not validate factual correctness
- does not assert semantic equivalence beyond the exact canonicalization rule defined here

It produces a deterministic byte representation suitable for cryptographic commitment only.

All interpretation remains external to higher-layer verification semantics.

Human-perceived message equivalence MUST NOT be treated as normatively equivalent to canonical identity under `/1`.

Implementations MUST NOT infer canonical equivalence from:

- visually identical rendering
- semantically similar body text
- regenerated or re-exported mailbox artifacts
- MIME-decoded and reserialized message representations
- parser-level header maps or reconstructed message objects

If the preserved artifact is not byte-equivalent within the canonicalization boundary defined by this profile, implementations MUST treat that difference as potentially verification-relevant even when the messages appear identical to a human reader.

---

## 18. Versioning & extensibility

- **Profile identifier:** `subject.email`
- **Profile version:** `/1`

Any change that alters canonical byte output, message-input boundary, header/body canonicalization rules, or permitted normalization behavior MUST require a new major version.

No optional canonicalization behavior is permitted under `/1`.

---

## 19. References

- CERTCRYPT Specifications
    - [security-model/1 — CERTCRYPT Security Model](../../../foundation/security-model/1/index.md)
    - [system-domain/1 — CERTCRYPT System Domain](../../../foundation/system-domain/1/index.md)
    - [rules-domain/1 — CERTCRYPT Rules Domain](../../../foundation/rules-domain/1/index.md)
    - [CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol](../../../protocols/CCCP/1/index.md)
    - [CCSP/1 — CERTCRYPT Certificate Serialization Protocol](../../../protocols/CCSP/1/index.md)
    - [verification/verification-package/1 — verification-package/1 · CERTCRYPT Verification Package Specification](../../../ecosystem/verification/verification-package/1/index.md)
    - [verification/verifier-toolkit/1 — verifier-toolkit/1 · CERTCRYPT Verifier Toolkit Specification](../../../ecosystem/verification/verifier-toolkit/1/index.md)
    - [subject.binary/1 — CERTCRYPT Binary Subject Canonicalization Profile](../../subject.binary/1/index.md)
    - [subject.collection/1 — CERTCRYPT Collection Subject Canonicalization Profile](../../subject.collection/1/index.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)
    - [RFC 5322 — Internet Message Format](https://www.rfc-editor.org/rfc/rfc5322) (the message-input boundary in §10 and the header unfolding of §11.4 are defined in terms of this format)
    - RFC 5321 — Simple Mail Transfer Protocol (informative; SMTP transparency referenced in §10)
    - RFC 2045 / RFC 2049 — MIME (informative; the MIME concepts referenced in §12.1)
    - RFC 6376 — DomainKeys Identified Mail (DKIM) Signatures (informative; the transit-signature example in §12.1)

---

**End of subject.email/1**
