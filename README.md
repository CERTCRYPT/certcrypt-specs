# CERTCRYPT normative specifications

**This repository contains the public CERTCRYPT specifications. Normative
specifications define the rules against which conforming implementations and
verifiers are evaluated.**

This repository is the normative corpus: the public rules a verifier applies to
decide whether an artifact is `Independent`.

A document is part of the corpus once it is published here. Nothing outside it
carries normative weight, however closely it describes the same model.

The Markdown documents under `normative/` are the authoritative source texts.
Published HTML, exact-text TXT, and PDF representations are derived from those
documents. If a derived representation differs from its source, the Markdown
document in this repository governs.

## Anyone can reach the same verdict

A verifier that has neither the issuer's systems nor CERTCRYPT's can reach the same
verdict on the same artifact, offline, by applying these rules. That is the whole
purpose of publishing them: the rules are public, resolvable by version, and named
by every artifact bound to them.

The corpus defines interpretation and verification boundaries, and nothing beyond
them. It does not prove that a claim is true, does not replace cryptographic
authenticity, and does not by itself produce `Independent` — that is a verdict a
verifier reaches by applying these rules, not a status the corpus confers.

## Layout

The corpus has five planes, each family versioned independently.

| Plane | Contents |
| --- | --- |
| [`normative/foundation/`](./normative/foundation/index.md) | The plane the rest builds on: system manifest and foundation statements, system and rules domains, the composite signature profile, the security model. |
| [`normative/protocols/`](./normative/protocols/index.md) | Canonicalization and commitment, certificate envelope serialization, consistency verification, and the submission set. |
| [`normative/profiles/`](./normative/profiles/index.md) | How each kind of subject is reduced to deterministic canonical bytes. |
| [`normative/models/`](./normative/models/index.md) | How independence is derived from a fixed leaf and settled capacity. |
| [`normative/ecosystem/`](./normative/ecosystem/index.md) | The artifacts and contracts binding authorization, settlement and verification, and the operator specifications. |

[`verification/rules/`](./verification/rules/README.md) is where the corpus proof of
each registered rules domain is published, with the procedure for checking that the
specification text in this repository is the text that governs a certificate you
hold. Every file of this repository is also certified as it is published:
[`verification/`](./verification/README.md) holds those certifications and the
procedure for checking one.

Start at [`normative/index.md`](./normative/index.md), which states the recommended
reading order.

## Versioning

Every artifact carries the `rules_version` in force when it was issued, and a
verifier resolves that exact version from here. Later versions do not re-evaluate an
older artifact, do not supersede it, and cannot break it.

That is what makes the corpus additive: publishing a new version extends what is
readable without moving the rules any existing artifact is already bound to.

Freezing a version is a formal step with stated conditions. Publication does not
confer it — each version states its own status.

[`frozen-versions.json`](./frozen-versions.json) lists the versions that are frozen
and commits to their exact bytes: one SHA3-256 over the sorted paths and contents
of every file in a frozen set. Run `python3 scripts/check-frozen-versions.py` to
confirm that no frozen text has changed by a single byte; it fails if one has.

The repository itself is versioned too: [`VERSION`](./VERSION) and
[`CHANGELOG.md`](./CHANGELOG.md) identify each published snapshot of the corpus as
a whole, so a reader can cite exactly which corpus was published at a given time.
That version is independent of the version of any specification.

## Language

These documents are published in English only.

A verifier resolves one text from an artifact's `rules_version`, and the corpus
proof commits to the bytes of that text. There is therefore exactly one version of
each document and no translated rendering of it. A translation would either be
uncertified, or a second normative text — both defeat the purpose.

## Implementing these specifications

The corpus states the rules; it does not ship an implementation of them.

Byte-level agreement between independent implementations is established against the
published conformance vectors, which are the reference a reimplementation checks
itself against. Where a specification and an implementation disagree, the
specification governs — but a disagreement with the vectors is worth reporting, as
it usually means the text is ambiguous.

## Reporting problems

A defect in the rules — a specification that would let an invalid artifact verify,
or that omits a check a sound verifier needs — is a security issue. See
[SECURITY.md](./SECURITY.md).

Editorial corrections can be raised as ordinary issues. A frozen version is never
edited, not even editorially: a correction goes into a draft or the next version.

## License

Apache License 2.0. See [LICENSE](./LICENSE).
