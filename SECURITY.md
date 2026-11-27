# Security Policy

## A security issue here is a defect in the rules

This repository carries the normative specification corpus — the public rules a
verifier applies. It contains no running service and no deployed code. What can be
defective here is a **rule**: a specification that permits an invalid artifact to
verify, or that fails to require a check a sound verifier needs.

Defects in an implementation of these rules belong to that implementation's
repository, not here.

## Supported Versions

Specification families are versioned independently, and every artifact carries the
`rules_version` in force when it was issued. A published version is not revised in
place once frozen: a verifier resolving that version must find the same text.

| Version | Supported |
| --- | --- |
| Latest published version of a family | Yes |
| Earlier published versions | Remain resolvable, corrected only by a new version |

A correction to a frozen version, whatever its effect on normative meaning, is
issued as a new version. It does not re-evaluate, supersede, or invalidate
artifacts already bound to an earlier one.

## Reporting a Vulnerability

Please do not open public issues for security vulnerabilities.

Report security concerns by email to security@certcrypt.com.

Include:

- the specification and version affected (for example `independence.proof/1`)
- the section, and the requirement you believe is wrong or missing
- the artifact set or verifier behavior that demonstrates the issue
- potential impact — in particular, whether it lets an invalid artifact verify

Please avoid including customer data, production credentials, private keys, or
confidential third-party material in reports.

We will acknowledge valid reports as soon as practical and coordinate remediation
before public disclosure.

## Of particular interest

Reports that identify any of the following are especially valuable:

- a path by which an artifact could be accepted as `Independent` while omitting a
  required structural condition
- a canonicalization, serialization, or commitment rule that is ambiguous enough
  for two conforming implementations to disagree on the same input
- a failure condition that is stated as SHOULD where soundness requires MUST
- a specification that cannot be implemented from its own text plus the documents
  it declares a dependency on

## Coordinated Disclosure

Please give us a reasonable opportunity to investigate and remediate before public
disclosure.

Do not publish exploit details, proof-of-concept artifacts, or operational
indicators before we have completed triage and remediation planning.

## Out of Scope

The following are not handled through this repository's security process:

- defects in a specific implementation, SDK, or verifier toolkit — report those to
  the repository concerned
- general product questions
- editorial corrections (ordinary issues; a frozen version is never edited)
- requests for roadmap information or publication timing
- reports about private CERTCRYPT systems not represented in this corpus
- claims about semantic truth, legal validity, or factual correctness of
  certificate content — the corpus does not assert any of these, by design

For non-security questions, use the public contact channel:

opensource@certcrypt.com
