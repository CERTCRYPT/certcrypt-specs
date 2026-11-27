# Verifying a rules corpus proof

Each registered rules domain has a corpus proof: the `independence.proof/1` proof
that certifies the documents that rules domain is made of. It answers one
question:

> Is the specification text I am reading the text that governs the certificate I
> am holding?

The corpus proofs are published in the `verification/rules/` directory of the
specifications repository, one directory per rules version. See
[Status](#status) for which proofs have been emitted.

Nothing here proves a certificate. A certificate is evaluated under
`independence.proof/1` and the rules domain it declares. What a corpus proof lets
you establish is that the rules you are about to read are the authentic ones —
without trusting GitHub, the specifications repository, its owner, or CERTCRYPT
continuing to exist.

## Why this exists

`rules-domain/1` Section 13.2 requires a published rules domain to be immutable
and to remain resolvable for the lifetime of any proof that depends on it. On its
own that is a promise about the publisher's conduct: a reader who obtains a
tampered copy has no way to tell. Section 13.3 makes it checkable by certifying
the corpus itself, and Section 13.3.4 requires the resulting proof to be published
beside the documents it certifies.

The consequence worth stating plainly: **the location you obtained these
documents from establishes nothing.** Not the specifications repository, not the
documentation site, not a mirror or an archive. Only the corpus proof does. That
is deliberate — see Section 13.3.3, "Distribution is not authority".

## What is certified

One `subject.collection/1` subject per rules domain. Its leaves are the documents
that rules domain **is made of** — in the active corpus, its registry entry —
each canonicalized under `subject.text/1`.

Not everything the rules domain is *read under*. The generic specifications
(`rules-domain/1`, `system-manifest/1`, the security model) are shared by every
rules domain and versioned separately, so they are outside the certified set. That
boundary is what keeps this usable: publishing more of the corpus never disturbs
an existing proof, and a conforming verifier — which ships the commitment — does
not need reissuing every time the corpus grows.

| | |
| --- | --- |
| Collection profile | `subject.collection/1` |
| Leaf profile | `subject.text/1` |
| Declared cardinality | the exact number of documents that constitute the rules domain |

Two boundaries follow from the profiles, and both are intended:

- **`subject.text/1` normalizes line endings and enforces exactly one final CRLF,
  preserving every other byte.** A document re-exported across platforms, which
  changes only its line endings, still verifies. A document with any other byte
  changed does not, whether or not the change affects its normative meaning:
  Section 13.2 forbids every in-place modification of a published rules document.
- **The declared cardinality binds the count.** Removing a document fails, not
  only altering one.

### What is not certified

- **Index pages** (`index.md` at any level). They are navigation, they carry no
  normative text, and they are where the proof reference itself is published — so
  certifying them would require the certified text to contain a value derived
  from itself.
- **The generic specifications the rules domain is interpreted under.** They are
  shared and separately versioned, so publishing `system-manifest/2` does not
  disturb any rules domain's proof. A frozen version never changes (see
  `frozen-versions.json` at the root of the specifications repository).
- **The `verification/` directory.** It is where the proofs are published.

## How to verify

Four steps. None of them requires CERTCRYPT, and after the first none of them
needs a network.

1. **Obtain the corpus and its proofs.** A `git clone` of the specifications
   repository carries the documents, this procedure and `verification/rules/`. For
   each rules version whose [Status](#status) entry says its corpus proof has been
   emitted, the same clone also carries that proof and no further retrieval is
   needed. A version still marked as pending cannot pass step 3.

2. **Recompute the collection.** Take the base certificate from the package. Its
   `anchor` member carries `nonce_hex`, and its one subject is a
   `subject.collection/1` whose leaves list, in order, one `subject.text/1` digest
   per document. For each certified document, in the order of the certified set —
   in the active corpus a single document, the registry entry of the rules domain
   (`normative/foundation/system-domain/1/registry/certcrypt/rules/<version>.md`):

   - canonicalize under `subject.text/1`: replace every `CRLF`, lone `CR` and
     `LF` with `CRLF`, then ensure exactly one trailing `CRLF`
   - compute its leaf under `collection.merkle-sha3-256/1`, salted with the ASCII
     bytes of the certificate's `nonce_hex` (`subject.collection/1` §8)
   - compare it with the leaf at the same position
   - fold the leaves into the collection root

   The salt is per certificate, so the root exists only once the certificate does. The
   path a document was read from is not part of its leaf: content and order are.

3. **Compare.** The folded root must equal the collection root the certificate
   signs, and the number of documents its declared cardinality. Then compare the
   proof's `subtree_root` with the corpus commitment your verifier carries for this
   `rules_version`: that pins this proof as the one that certifies the rules domain.
   If anything differs, **stop**: under `rules-domain/1` Section 13.3.2 evaluation
   fails closed. A mismatch is not a warning to work around.

4. **Verify the proof itself.** Read the package under `verification-package/1`
   and validate the proof it carries under `independence.proof/1`, as you would
   any other: its settlement reference, its inclusion and its finality, each as
   the settlement material carries it. Like the others, this step needs no
   CERTCRYPT service.

The JavaScript verifier toolkit performs steps 2 to 4 (`verifyRulesCorpus`). It is
not required: the procedure above is complete, and reimplementing it from these
specifications is the point.

## Availability, not authority

Additional channels may carry the same package — a publication profile such as
`arweave.publication/1` (an optional publication profile, not part of this corpus)
where permanence beyond a source repository is wanted.
None of that is required for validity and none of it confers authority. A verifier
evaluating a certificate does not need the corpus proofs at all: the artifact carries
its `rules_version` and its settlement reference, so the corpus can be recomputed
and the finality checked directly.

The corpus proofs serve the party who starts from a ruleset and asks whether it is
authentic — an auditor, an implementer, a reader years from now. For that party a
proof
must be obtainable without asking anyone. That is all it is for.

## Status

`rules/2026-01`: the text is final and its corpus proof has been emitted. It is
published in [`verification/rules/rules-2026-01/`](./rules-2026-01/):

- `verification-package.json`: the proof, as a `verification-package/1`;
- `system-foundation.json`: the `system-foundation/1` it is verified against;
- `corpus.json`: the certified set (one document), its collection root and the
  proof's `subtree_root`.

Its corpus commitment is
`subtree_root = 17e3a74a4fd05b039da9f740a138c36d353f561d49726c00351843bb518364ff`,
settled on the XRP Ledger at ledger 108590302 (2026-11-26,
`settlement.aggregated.xrpl/1`). A verifier that does not carry this commitment
for `rules/2026-01` still rejects every artifact under it — the fail-closed basis
of `rules-domain/1` Section 13.3.1.
