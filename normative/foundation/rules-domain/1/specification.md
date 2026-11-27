# CERTCRYPT Rules Domain Specification (rules-domain/1)

**Identifier:** `rules-domain/1`  

**Label:** CERTCRYPT Rules Domain Specification (rules-domain/1)  

**Type:** Foundation Specification

**Status:** Frozen

**Layer:** Layer 0 — Foundation

**Depends on:** See References *(active normative dependencies are listed below)*  

**Naming convention:** `rules-domain/1` is the formal identifier.  
CERTCRYPT Rules Domain Specification (rules-domain/1) is the human-readable label and may be used in titles, filenames, UI labels, and documentation headings.  

**Audience:** Protocol designers, specification authors, implementers, auditors  

**Purpose:** Define the normative semantics, constraints, and interpretation boundary of rules-domain/1 within the active CERTCRYPT public architecture.  

**Intended use:** rules-domain/1 is intended to be the authoritative public specification used by conforming implementers, verifiers, auditors, and ecosystem tooling when handling this artifact or behavior.  

**Scope:** Defines the active normative behavior of rules-domain/1; adjacent protocols, profiles, operational tooling, and product behavior remain out of scope except where explicitly referenced.  

**Non-goals:** rules-domain/1 does not prove truth, semantic validity, legal validity, or live service authority by itself, and MUST NOT be interpreted as a substitute for cryptographic authenticity, Proof of Independence, or managed-service behavior outside its own normative scope.

> This document is **normative**.  
> All requirements defined using the keywords MUST, MUST NOT, SHOULD, or MAY are authoritative and are to be interpreted as described in [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Background & rationale
This specification defines the CERTCRYPT rules-domain model.

The rules domain establishes the exact public ruleset under which CERTCRYPT artifacts are interpreted, evaluated, accepted, or rejected.

It defines:

- what a CERTCRYPT Rules Domain is
- how the applicable rules domain MUST be identified
- when a rules domain is exact enough for normative evaluation
- how equivalence, compatibility, and successor-rule claims MUST be constrained
- what cross-artifact consistency requirements apply

It does not define:

- system identity or system-root attribution
- proof validity by itself
- settlement execution details
- capacity issuance, authorization, locking, or consumption workflows
- product behavior or managed-service UX

Those concerns belong to separate specifications.

---

## 2. Scope

This specification applies to all systems, implementations, SDKs, verifiers, APIs, and artifacts that:

- declare, imply, or require a `rules_version`
- interpret CERTCRYPT artifacts under public rules
- evaluate leaf, capacity, settlement, or proof semantics
- derive or validate `Independent`

Any implementation that evaluates CERTCRYPT artifacts normatively MUST conform to this specification for rules-domain selection and consistency, and any implementation that emits artifacts declaring a `rules_version` MUST conform to it for rules-domain implementation. Section 14 states both, separately: the obligations differ because the two roles fail in opposite directions.

---

## 3. Terminology

The keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are to be interpreted as described in RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14).

---

## 4. Design principles

`rules-domain/1` is designed around the following principles:

- **Exact rule selection:** Normative evaluation MUST occur under one and only one exact public rules domain.
- **Deterministic verification:** Given the same artifacts and the same `rules_version`, conforming implementations MUST converge on the same interpretation boundary and outcome.
- **Fail-closed ambiguity rejection:** If exact rule selection cannot be established, evaluation MUST fail rather than degrade to compatibility, parser preference, or managed-service default.
- **Infrastructure neutrality:** The rules domain defines interpretation semantics, not product modes, runtime presets, or operator convenience branches.
- **Institutional independence:** Public rules MUST remain sufficient for verification without requiring continued control by any issuer, operator, or hosted CERTCRYPT layer.
- **Interpretation boundaries:** The rules domain constrains how artifacts are interpreted. It does not create truth, authority, or independence by itself.

---

## 5. Relationship to other foundations

Within the CERTCRYPT foundation:

- `system-domain` determines which system is being evaluated
- `rules-domain` determines which exact public rules govern that evaluation
- `security-model` determines which foundational properties must hold under those rules

Accordingly:

- a valid system domain without an exact rules domain is insufficient for normative evaluation
- a declared rules domain outside the attributed system domain is invalid
- a verifier MUST reject any context where system-domain attribution and rules-domain selection are inconsistent

---

## 6. Definitions

### 6.1 Rules domain

The **rules domain** is the exact versioned public ruleset that governs interpretation of artifacts within one system domain. A rules domain always belongs to exactly one system domain: it is registered under that domain, never independently of it (Section 16).

### 6.2 `rules_version`

`rules_version` is the canonical identifier by which a rules domain is declared or deterministically implied.

### 6.3 Exact rule selection

**Exact rule selection** means that one and only one rules domain applies to the evaluation context without heuristic choice, fallback behavior, parser discretion, or managed-service substitution.

### 6.4 Equivalent rules domains

**Equivalent rules domains** are distinct identifiers that public rules explicitly declare to be normatively interchangeable for one exact evaluation path.

No implementation MAY infer equivalence without such a public declaration.

### 6.5 Compatible or successor rules domains

**Compatible** or **successor** rules domains are rulesets that may resemble, extend, or replace earlier rulesets, but are not interchangeable unless public rules explicitly define them as equivalent for the specific evaluation path.

Compatibility alone is not sufficient for substitution.

### 6.6 Settlement profile

A **settlement profile** is the exact public-rule-defined contract selected by one `settlement_profile_id`.

Where a rules domain permits settlement-backed `Independent`, each permitted settlement profile MUST define:

- the exact settlement mode
- the exact settlement-material contract
- the exact finality profile
- the exact leaf-assignment interpretation
- the exact authorization-to-consumption bridge

---

## 7. Rules-domain identity

Every CERTCRYPT artifact whose normative meaning depends on public rules MUST include or deterministically imply one exact `rules_version`.

That `rules_version` MUST:

- identify one exact rules domain
- be stable enough for reproducible evaluation
- belong to the attributed system domain
- be sufficient to select the applicable public rules without heuristic inference

If `rules_version` is absent, multiple, ambiguous, or parser-dependent, normative evaluation MUST fail unless the applicable specification explicitly permits deterministic derivation and that derivation succeeds uniquely.

---

## 8. Selection requirements

Rules-domain selection MUST be:

- deterministic
- exact
- reproducible
- independent of UI preference
- independent of managed-service preference
- independent of parser tolerance or recovery behavior

An implementation MUST reject evaluation if:

- more than one rules domain could validly apply
- rule selection depends on fallback behavior
- rule selection depends on undocumented compatibility logic
- rule selection depends on parser discretion
- rule selection depends on transport context, wrapper metadata, or live service hints

---

## 9. Equivalence, compatibility, and successor rules

Equivalent rules domains MAY be treated as interchangeable only when public rules explicitly define:

- the exact identifiers involved
- the exact scope of equivalence
- the exact evaluation paths for which equivalence holds

Compatible, successor, upgraded, legacy, parser-preferred, or service-preferred rules domains MUST NOT be substituted merely because they:

- appear similar
- share field layouts
- produce superficially compatible outputs
- are newer
- are operationally more convenient

If an implementation cannot establish explicit public equivalence for the exact evaluation path, it MUST reject the substituted interpretation.

---

## 10. Cross-artifact consistency

All related artifacts in one evaluation context MUST remain consistent under one exact rules domain, unless public rules explicitly define a narrower exception.

This includes, where applicable:

- `submission-set`
- `capacity_commitment`
- `independence_proof`
- `verification_package`
- settlement-derived artifacts
- inclusion and bookkeeping artifacts

Where settlement-backed `Independent` is permitted, this consistency requirement also includes the exact `settlement_profile_id` and its proof-material contract.

An implementation MUST reject any context in which related artifacts:

- require different non-equivalent rules domains
- allow multiple plausible rule interpretations
- mix legacy and successor rules without explicit equivalence
- rely on wrapper or service metadata to reconcile rule differences

---

## 11. Verifier behavior

A conforming verifier MUST:

- determine the exact rules domain before normative evaluation
- reject unsupported or ambiguous rules domains
- reject fallback, downgrade, or heuristic substitution
- report incompleteness or rejection explicitly when exact rule selection fails

A verifier MUST NOT:

- treat "compatible enough" as valid
- silently upgrade or downgrade rules
- use managed-service defaults as normative rule selectors
- accept a proof, package, or artifact set under a less strict or merely more familiar rules domain

---

## 12. Managed services and tooling

Managed services, SDK defaults, wrappers, or convenience tooling MAY help discover the declared `rules_version`.

They MUST NOT:

- define the normative rules domain by preference
- override declared or derivable public rules
- reconcile ambiguity privately
- convert unsupported rules into accepted evaluation through hidden fallback

Normative rule selection MUST remain reproducible without discretionary authority.

---

## 13. Relationship to higher-layer specifications

Higher-layer specifications MAY define:

- which artifacts require explicit `rules_version`
- when `rules_version` may be deterministically derived
- whether explicit equivalence exists for a particular evaluation path
- additional fail-closed requirements for specific proof, settlement, or capacity contexts

Where a rules domain permits settlement-backed `Independent`, those higher-layer specifications MAY refine the selected settlement profile, but they MUST NOT leave its proof-material contract, finality profile, or authorization-to-consumption bridge discretionary.

They MUST NOT:

- weaken the exactness requirement defined here
- authorize heuristic substitution
- permit parser-dependent rule selection
- convert compatibility into equivalence without explicit public definition

### 13.1 Settlement profile completeness

If a rules domain permits any settlement-backed path to `Independent`, it MUST define one or more exact `settlement_profile_id` values.

For each permitted `settlement_profile_id`, the public rules MUST define:

1. one exact settlement mode
2. one exact method for resolving `settlement_ref`
3. one exact finality profile sufficient for canonical acceptance
4. one exact settlement-material contract conforming to `settlement-material/1` or an explicitly declared equivalent successor
5. one exact capacity-consumption interpretation
6. one exact authorization-to-consumption bridge
7. one exact leaf-assignment interpretation

If any of those elements is absent, partial, ambiguous, or discretionary, that settlement profile MUST be treated as non-conformant and MUST fail closed.

### 13.2 Published rules immutability

A published `rules_version` MUST remain immutable once publicly released.

A published `rules_version` MUST remain publicly resolvable for the lifetime of any valid proof, package, or artifact whose normative meaning depends on that version.

Published rules documents MUST NOT be modified in place in any way, including editorial, typographic or clarifying changes that would leave their normative meaning unchanged.

If a later ruleset is needed:

- a new `rules_version` MUST be published
- any equivalence or successor relationship MUST be declared explicitly under public rules
- earlier published `rules_version` identifiers MUST continue to resolve as their original immutable ruleset

### 13.3 Published rules authenticity

Section 13.2 binds the publisher. This section binds the verifier, and makes the
obligation checkable: without it, immutability and perpetual resolvability are
assertions about publisher conduct that no relying party can evaluate.

A verifier that resolves a published ruleset MUST be able to establish, without a
live CERTCRYPT service and without trusting the location it was obtained from,
that the document set in hand is the exact ruleset governing the artifact under
evaluation.

The binding runs from the proof to the documents, never from the documents to the
proof. A published ruleset MUST NOT carry a reference to the proof that certifies
it: the certified text would then have to contain a value derived from itself, so
recording the reference would change the very bytes the proof committed to, and
the authentic document would fail its own verification.

Accordingly, a **corpus proof** of a rules domain is an `independence.proof/1`
proof that:

- carries the `rules_version` of the rules domain it certifies
- certifies one `subject.collection/1` subject whose leaves are the published
  documents that constitute that rules domain, each as one `subject.text/1` leaf,
  with the declared cardinality binding their exact number
- is resolvable independently of any CERTCRYPT-operated service

The proof is self-locating: `independence.proof/1` Section 10.3 already requires it
to carry the exact `rules_version` under which it was fixed, and its Section 12.9
already requires a verifier to reject more than one proof presented for the same
`subtree_root` under the same `system_id` and `rules_version`. A verifier
therefore resolves the corpus proof **by** the `rules_version` it is already
evaluating, and needs no pointer inside the ruleset to find it.

The corpus proof is emitted under the same `rules_version` it certifies. This is
not circular: emission treats each document as an opaque subject and does not
interpret it as rules, and verification of the corpus proof requires the
*parameters* of that rules domain, which a conforming verifier already holds — not
the *documents*, which are what is being authenticated.

`subject.text/1` is required rather than `subject.binary/1` so that the binding
tracks the text rather than its transport encoding: that profile normalizes
line endings and enforces exactly one final CRLF while preserving all other bytes
exactly. A document re-exported across platforms, which changes only its line
endings, therefore still verifies; a document with any other byte changed does
not, whether or not the change affects its normative meaning. Section 13.2
forbids every such change.

A verifier that obtains a ruleset establishes its authenticity through one chain,
each link of which MUST hold:

1. The corpus proof verifies under `independence.proof/1` for the `rules_version`
   it certifies.
2. Its anchored `subtree_root` equals the corpus commitment the verifier carries for
   that `rules_version` (Section 13.3.1). This identifies the one proof that
   certifies the rules domain: another emission over the same documents has another
   `subtree_root`.
3. Its base certificate commits to exactly one `subject.collection/1` subject whose
   leaves are all `subject.text/1`, and whose declared cardinality equals the
   number of documents.
4. Each document, canonicalized under `subject.text/1` and committed under the
   collection scheme with the certificate's own collection salt
   (`subject.collection/1`), reproduces its leaf in order, and the leaves fold to
   the collection root the certificate signs.

Link 4 binds the text to the certificate; links 1 and 2 bind that certificate to
the proof the verifier trusts. The collection root and the `subtree_root` are
different values: the first commits to the documents, the second to the leaf the
proof anchors, and the verifier carries the second.

##### Scope of the certified set

The certified set is the documents a rules domain **is made of**, not everything
it is interpreted under. In the active corpus that is its registry entry: Section
16 makes that entry the single canonical source of truth for a concrete
instance's parameters and forbids inferring them from anywhere else, so it is the
document whose authenticity a verifier's compiled parameters depend on.

The generic specifications a registry entry is read under — this document,
`system-manifest/1`, the security model — are deliberately outside it. They are
shared by every rules domain and versioned in their own right; folding them in
would tie one rules domain's commitment to the editorial life of documents it
does not define.

This scoping is what makes the mechanism usable rather than an obstacle:

- **Publishing more of the corpus does not disturb an existing commitment.**
  Publishing a further family or specification version leaves every existing
  rules domain's certified set untouched. Since a conforming verifier ships that commitment (Section 13.3.1), the alternative
  would require reissuing every verifier each time the corpus grew — for
  documents whose text did not change.
- **A rules domain's commitment changes only when that rules domain changes.**
  Under Section 13.2 a published rules domain is immutable once frozen, so the
  commitment of a frozen rules domain is fixed for its lifetime. A rules domain
  that has not yet been frozen may still be corrected in place, and the
  commitment recorded at freeze is the one that certifies the frozen text.
- **Documents that constitute no rules domain are outside every certified set.**
  Index pages, overviews that declare themselves informative, and publication
  notes carry no parameter a verifier relies on.

Which documents constitute a rules domain is a decision recorded per rules
domain, not a pattern inferred from paths. A rules domain whose parameters are
split across more than one document certifies all of them; one whose parameters
live in a single registry entry certifies exactly that entry.

#### 13.3.1 Bootstrap

A corpus proof cannot be resolved by a verifier that holds no starting point for
the system domain, and the bootstrap rules domain of a system domain has no earlier
ruleset that could supply one. The starting point is therefore the same one that
already anchors system identity: the bootstrap ceremony that fixes
`bootstrap_system_root_fingerprint` also fixes the system root under which the
corpus proof of that bootstrap rules domain is emitted, and the proof is emitted
after the ruleset text is final.

No value derived from the corpus proof is recorded in the ruleset. A verifier
resolves the proof by `(system_id, rules_version)` under the system root it already
attributed, which is exactly the resolution `independence.proof/1` already defines.

##### Distribution of the corpus commitment

The anchored `subtree_root` of the corpus proof of each supported rules domain —
its corpus commitment — MUST be published inside the conforming verifier itself, alongside the system-root fingerprint and
the settlement parameters it already carries.

This is the same requirement, for the same reason. A verifier must not be
configurable into trusting the wrong rules text: were the commitment read from
the environment, from a configuration file, or from the ruleset being evaluated,
anyone could substitute their own and obtain a valid verdict over a corpus they
authored. Shipping it in the verifier is what makes the check independent of
whoever runs it — the property that already governs `system_root_fingerprint`.

It also closes the loop between the verifier and the corpus. A conforming verifier
holds the parameters of a rules domain compiled in, and does not read the
published documents at evaluation time; the commitment is what lets any third
party confirm that those compiled parameters are the ones the published corpus
states. Without it, a verifier built against an altered registry entry is
indistinguishable from one built against the authentic text.

A conforming verifier MUST therefore:

- carry one certified `subtree_root` per rules domain it declares support for
- fail closed on any rules domain it declares support for but holds no commitment
  for, exactly as it fails closed on an unrecorded system-root fingerprint
- reject a corpus proof whose certified `subtree_root` differs from the value it
  carries, without regard to where the proof or the corpus was obtained

A verifier that declares support for a rules domain while holding no commitment
for it, or that treats a missing commitment as an absence of constraint, is
non-conformant. Absence MUST NOT be read as permission.

Because a certified set is what a rules domain is made of and not what it is read
under (Section 13.3, "Scope of the certified set"), shipping the commitment does
not couple verifier releases to corpus releases. Publishing a further
family or specification version leaves every existing
commitment unchanged; a verifier needs reissuing only when a rules domain it
supports changes, which for a frozen rules domain does not happen. A verifier
adds a commitment when it adds support for a new rules domain — the same occasion
on which it would already need the new domain's parameters.

Until a corpus proof exists for a rules domain and its commitment is distributed
in the conforming verifier, no artifact under that rules domain can be validated,
on the same fail-closed basis as an unrecorded bootstrap fingerprint.

#### 13.3.2 Failure conditions

Normative evaluation MUST fail closed if:

- no corpus proof resolves for the applicable `rules_version`
- more than one corpus proof resolves for it
- the resolved proof does not carry the `rules_version` under evaluation
- the recomputed collection root differs from the collection root the corpus
  proof's base certificate signs, or any document fails to reproduce its leaf
- the number of resolved documents differs from the certified declared cardinality
- the resolved proof's own attribution fails under Sections 7 through 10
- the certified `subtree_root` differs from the commitment the verifier carries
  for that rules domain, or the verifier carries none

Absence of a corpus proof MUST NOT be treated as absence of constraint. A verifier
MUST NOT accept a ruleset on the basis of the location it was retrieved from, the
presence of a matching `rules_version` label, or a transport-level assurance such
as a signed certificate for the serving host.

A published ruleset that carries any self-referential proof identifier cannot
be authentic: the identifier is derived from the bytes the proof committed to, so
writing it into the document changes those bytes. Such a document fails link 4 of
Section 13.3 — it does not reproduce its leaf — and needs no separate check.

#### 13.3.3 Distribution is not authority

A published ruleset MAY be distributed through any number of channels, including
source repositories, documentation sites, mirrors, and archives. Such channels
serve availability only.

No distribution channel, publication transaction, repository identity, or hosting
arrangement MAY be treated as establishing the authenticity of a ruleset. Only the
corpus proof does that.

Where public transparency of the corpus proof itself is desired, it MAY be
published under a publication profile such as `arweave.publication/1` (an optional publication profile, not part of the published corpus). That
publication reinforces availability and public history; it does not confer
authority, and a verifier MUST NOT substitute the existence of such a publication
for the recomputation required by Section 13.3.

#### 13.3.4 Publication of the corpus proof

A corpus proof is of no use to a third party that cannot obtain it. Section 13.3
requires the proof to be resolvable independently of any CERTCRYPT-operated
service; this section states how that resolution is served in practice.

The corpus proof of a rules domain MUST be published alongside the documents it
certifies, as a `verification-package/1` for the `independent` target. Publishing
it beside the corpus is what makes the check self-contained: a third party
obtains the documents and the proof in one retrieval, and the material original
to the verification — the specification documents themselves — is already present,
which is why the package carries none of its own (`verification-package/1`
Section 10).

The published package MUST:

- use the archive structure of `verification-package/1` Section 22.2, or its
  inline JSON equivalent under Section 22.1
- carry the corpus proof as `independence_proof`
- state which documents are certified, at which specification versions, and the
  `subject.collection/1` cardinality that binds them
- state the recomputation procedure in full: the `subject.text/1`
  canonicalization of each document, the collection commitment under the
  certificate's collection salt, the comparison against the collection root the
  certificate signs, and the comparison of the proof's `subtree_root` against the
  corpus commitment a conforming verifier carries

The package MUST NOT be part of any certified set. It contains the proof, so
certifying it would require the certified text to contain a value derived from
itself — the self-reference Section 13.3 forbids. It therefore lives outside the
normative corpus it accompanies.

Publication of the package is a matter of availability, not authority. A verifier
evaluating an artifact does not need it: the artifact carries the `rules_version`
and the settlement reference, so the corpus can be recomputed and the finality
checked directly. The package serves the party that starts from a ruleset and asks
whether it is authentic — an auditor, an implementer, a reader in a distant
future — and for that party it must be obtainable without asking anyone.

Additional publication channels MAY carry the same package. A publication profile
such as `arweave.publication/1` (an optional publication profile, not part of the published corpus) MAY be used where permanence beyond a source
repository is wanted. None of that is required for validity, and none of it
confers authority: Section 13.3.3 applies to the package exactly as it applies to
the corpus.

---

## 14. Conformance

Conformance is stated separately for the two roles, because they fail in opposite
directions. A verifier that does not implement a rules domain rejects artifacts
under it, which is safe: the answer is "cannot evaluate". An issuer that emits
under a rules domain it does not implement produces artifacts that verify
perfectly and attest to behavior it never performed — every signature valid,
every digest matching, the settlement real. No verifier can detect it, because
there is nothing malformed to detect. Emission therefore carries the stricter
obligation.

### 14.1 Evaluating implementations

An implementation that evaluates CERTCRYPT artifacts conforms to `rules-domain/1`
if and only if it:

- selects one and only one exact rules domain for normative evaluation
- rejects ambiguous, heuristic, fallback, or parser-dependent rule selection
- preserves cross-artifact rules-domain consistency
- refuses compatible or successor substitution unless explicit public equivalence applies
- authenticates the resolved ruleset against the corpus proof for that `rules_version` under Section 13.3, rather than trusting the channel it was obtained from
- carries the certified corpus commitment of every rules domain it declares support for, and fails closed where it holds none
- reports rule-selection failure explicitly rather than silently degrading evaluation

### 14.2 Emitting implementations

An implementation that emits artifacts declaring a `rules_version` — an SDK, an
issuer library, a service that assembles certificates or proofs — conforms to
`rules-domain/1` if and only if it:

- declares the exact set of rules domains it implements
- refuses to emit under any `rules_version` outside that set, rather than
  accepting it as an opaque parameter
- refuses to emit an artifact whose subject profiles, commitment constructions,
  signature algorithms or settlement profile are not the ones the declared rules
  domain fixes, even where the implementation supports them under another
- fails closed on that refusal, and reports it as a rules-domain conformance
  failure rather than a validation or input error

An emitting implementation is not a generic parameterisable engine that a caller
points at a rules domain. It implements one exact normative body: the
canonicalization of each admitted subject profile, the commitment constructions
with their exact preimages, the signature algorithms, the settlement contract.
Those are properties of the rules domain, fixed in its registry entry, and an
implementation either realizes them or does not.

Accepting `rules_version` as a free parameter therefore misstates what the
implementation is. The value is not configuration: it is the assertion, carried
in every artifact emitted and covered by its signatures, that the artifact was
produced under that exact normative body. An implementation that cannot honor the
assertion MUST NOT make it.

This is the counterpart of the commitment requirement in Section 13.3.1. A
conforming verifier declares which rules domains it can evaluate and carries the
corpus commitment of each; a conforming emitter declares which rules domains it
can produce under. Between them the two declarations close the loop: no artifact
is emitted under rules its producer does not implement, and none is accepted
under rules text its consumer cannot authenticate.

---

## 15. Final statement

CERTCRYPT depends not only on exact system attribution, but also on exact rules-domain attribution.

If a verifier cannot determine which exact public rules govern an evaluation, it cannot validly determine whether a CERTCRYPT artifact is acceptable, rejectable, or capable of proving `Independent`.

Therefore, exact rules-domain selection is a foundation property of CERTCRYPT and MUST fail closed whenever ambiguity remains.

---

## 16. Registered rules domains

This specification defines the generic `rules-domain/1` profile. It does not
define the concrete parameters of any specific rules-domain instance.

A rules domain belongs to exactly one system domain (Section 7), so instances are
registered under that domain rather than under this specification: a registry
here would have to name a system domain to be meaningful, and this document names
none. Each entry defines exactly one `rules_version` and provides the complete
normative parameter set required by Sections 8, 10 and 13 for that instance.

The registry entry is the single canonical source of truth for the parameters of
a concrete rules-domain instance. Implementers MUST NOT infer them from this
generic specification, from defaults, or from any source other than the entry
whose `rules_version` exactly matches the artifact under evaluation.

For the active CERTCRYPT public architecture, the registered rules domains are
listed under
[system-domain/1/registry/certcrypt/rules/](../../system-domain/1/registry/certcrypt/rules/index.md).

A rules domain of any other system domain is registered under that domain, by
whoever operates it, and is not part of this corpus.

### 16.1 Conformance rules domains

The identifiers `rules/conformance` and `rules/conformance-uncommitted` are
reserved for the public conformance vectors of this corpus. They are not
registered rules domains and never will be: they exist so that the vectors can
exercise the protocol mechanics — signatures, bindings, inclusion proofs, and the
fail-closed cases — without depending on any deployment.

They are used only with a synthetic system root generated for the vectors, whose
keys are published with them and therefore protect nothing. A verdict obtained
under them is a test result, never evidence about a real artifact. Accordingly:

- a conforming verifier configured with a registered system domain MUST NOT
  accept them: like any unlisted `rules_version`, they fail selection (Section 8)
- a verifier MAY accept them only under a configuration that carries the
  synthetic root of the vectors, and MUST then report its result as a
  non-production verification
- they carry no exception: every check of this corpus applies under them exactly
  as under a registered rules domain, including the mandatory proof signature
  and the corpus commitment of Section 13.3.1 — `rules/conformance-uncommitted`
  is the vector of a rules domain a verifier declares without holding its
  commitment, and fails for that reason

---

## 17. Versioning & extensibility

This `/1` specification defines the current active public contract for `rules-domain/1`.

Once frozen, this version MUST NOT be modified in place in any way, including editorial, typographic or clarifying changes that would leave its normative meaning unchanged. Any change MUST be published under a new version identifier.

---

## 18. References

- CERTCRYPT Specifications
    - [security-model/1 — CERTCRYPT Security Model](../../security-model/1/index.md)
    - [system-domain/1 — CERTCRYPT System Domain](../../system-domain/1/index.md)
    - [system-foundation/1 — CERTCRYPT System Foundation](../../system-foundation/1/index.md)
    - [system-manifest/1 — CERTCRYPT System Manifest](../../system-manifest/1/index.md)
    - CCCP/1 — CERTCRYPT Canonicalization Commitment Protocol
    - CCSP/1 — CERTCRYPT Certificate Serialization Protocol
    - CCVP/1 — CERTCRYPT Consistency Verification Protocol
    - [independence.proof/1 — CERTCRYPT Independence Proof Model](../../../models/independence.proof/1/index.md)
    - [settlement-material/1 — CERTCRYPT Settlement Material Specification](../../../ecosystem/settlement/settlement-material/1/index.md)
    - [subject.binary/1 — CERTCRYPT Binary Subject Canonicalization Profile](../../../profiles/subject.binary/1/index.md)
    - [subject.collection/1 — CERTCRYPT Collection Subject Canonicalization Profile](../../../profiles/subject.collection/1/index.md)
    - [subject.text/1 — CERTCRYPT Plain Text Subject Canonicalization Profile](../../../profiles/subject.text/1/index.md)
    - [verification-package/1 — CERTCRYPT Verification Package Specification](../../../ecosystem/verification/verification-package/1/index.md)
- **External**
    - [RFC 8174 — Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words (BCP 14)](https://www.rfc-editor.org/rfc/rfc8174)

---

**End of rules-domain/1**
