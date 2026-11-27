#!/usr/bin/env python3
"""Cross-reference resolver for the CERTCRYPT public specs corpus.

Usage:  python3 scripts/check-references.py [<specs-dir>] [--tsv out.tsv] [--quiet]

What it does
  1. Indexes every tracked .md (git ls-files) : identifier + numbered heading tree.
     Reports heading-numbering defects (child prefix != parent, gaps, duplicates,
     level inconsistent with depth).
  2. Extracts every section reference (§N, §§, Section(s) N, ranges, lists,
     Annex/Appendix) and binds it to a spec (explicit identifier before/after,
     a markdown link immediately before, inheritance inside a reference chain,
     else the current document / its sibling specification.md).
  3. Resolves: BROKEN when the target number does not exist; WRONG when a
     semantic rule (SEMANTIC_RULES) says the cited
     section is not the one that carries the cited content.
  4. Checks every relative markdown link (and in-repo #anchors) resolves.
  5. Checks that every specification identifier a specification.md cites in its
     body also appears in its References section: a document that depends on a
     specification it does not list cannot be implemented from its own text plus
     its declared dependencies.
  6. Checks that every normative specification has an index and an overview,
     and that their shared metadata, including status, matches the normative
     document. The family index must list the same lifecycle status.

Exit status: 1 if any BROKEN / WRONG reference (excluding entries listed in
KNOWN_AMBIGUOUS), broken link, or cited-but-unlisted dependency remains, else 0.
Heading-numbering defects are reported but do not fail the check.
"""
import os, re, subprocess, sys, unicodedata
from collections import defaultdict

# ---------------------------------------------------------------- config ----
EXTERNAL = re.compile(r'(RFC\s?\d+|FIPS\s?\d+|SP\s?800-\d+|NIST|ISO[ /]?\d*|ECMA-?\d+|XLS-\d+|UAX\s?#?\d+|BIP-?\d+|IEEE)\s*$')

# Semantic rules: (spec id, regex on context, set of acceptable section prefixes).
# A reference into <spec> whose sentence matches <regex> must land in one of the
# acceptable sections (prefix match), otherwise it is WRONG.
SEMANTIC_RULES = [
    # cost_commitment / declared_effective_units live in submission-set/1 §13
    ('submission-set/1', re.compile(r'cost_commitment|declared_effective_units|declared effective units|cost commitment|unbound channel', re.I), ('13',)),
    # "the settlement plane carries evidence digests, not the base certificate" is submission-set/1 §8.1
    ('submission-set/1', re.compile(r'settlement plane carries evidence digests', re.I), ('8.1',)),
    # original material / complete verification in verifier-toolkit/1 is §8.5 (delivery) or §15 (boundary), never §16 (Non-goals)
    ('verifier-toolkit/1', re.compile(r'original material|complete verification', re.I), ('8', '11', '15', '17')),
    # "the package carries no original material" is verification-package/1 §10 (or §18), not §4
    ('verification-package/1', re.compile(r'carries none of its own|MUST NOT include original material', re.I), ('10', '18')),
    # rejecting more than one proof for the same subtree_root is independence.proof/1 §12.9
    ('independence.proof/1', re.compile(r'reject more than one proof', re.I), ('12.9',)),
]

# References reviewed by hand and judged ambiguous; keyed by (relpath, line, raw).
KNOWN_AMBIGUOUS = set()

# --------------------------------------------------------------- helpers ----
HEAD_RE = re.compile(r'^(#{1,6})\s+(?:Section\s+)?(\d+[A-Z]?(?:\.\d+)*)\.?\s+(.*?)\s*#*\s*$')
NUM = r'\d+[A-Z]?(?:\.\d+)*'
ID_LINE = re.compile(r'^\*\*Identifier:\*\*\s*`?([^`\n]+?)`?\s*(?:\(.*\))?\s*$', re.M)


def git_md(root):
    out = subprocess.run(['git', '-C', root, 'ls-files', '*.md'], capture_output=True, text=True, check=True).stdout
    return sorted(p for p in out.split('\n') if p)


def slug(title):
    s = title.strip().lower()
    s = re.sub(r'[`*_~]', '', s)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = ''.join(ch for ch in s if ch.isalnum() or ch in ' -' or unicodedata.category(ch).startswith('L'))
    return s.replace(' ', '-')


def metadata_value(text, name):
    match = re.search(rf'^\*\*{re.escape(name)}:\*\*\s*(.+?)\s*$', text, re.M)
    return match.group(1).strip() if match else None


def companion_page_issues(root):
    issues = []
    normative = os.path.join(root, 'normative')
    for base, _, files in os.walk(normative):
        if 'specification.md' not in files:
            continue
        spec_path = os.path.join(base, 'specification.md')
        spec = open(spec_path, encoding='utf-8').read()
        expected = {
            'Identifier': metadata_value(spec, 'Identifier'),
            'Label': metadata_value(spec, 'Label'),
            'Specification type': metadata_value(spec, 'Type'),
            'Layer': metadata_value(spec, 'Layer'),
            'Status': metadata_value(spec, 'Status'),
        }
        pages = (
            ('index.md', 'Informative version index'),
            ('overview.md', 'Informative overview'),
        )
        for filename, page_kind in pages:
            page_path = os.path.join(base, filename)
            rel = os.path.relpath(page_path, root)
            if not os.path.isfile(page_path):
                issues.append((rel, 'page is missing'))
                continue
            page = open(page_path, encoding='utf-8').read()
            for name, value in expected.items():
                actual = metadata_value(page, name)
                if actual != value:
                    issues.append((rel, f'{name} is {actual!r}; expected {value!r}'))
            actual_page_kind = metadata_value(page, 'Page')
            if actual_page_kind != page_kind:
                issues.append((rel, f'Page is {actual_page_kind!r}; expected {page_kind!r}'))
            if metadata_value(page, 'Type') is not None:
                issues.append((rel, 'ambiguous Type field must be replaced by Page and Specification type'))
        identifier = expected['Identifier'].strip('`') if expected['Identifier'] else None
        status = expected['Status']
        family_index = os.path.join(os.path.dirname(base), 'index.md')
        family_rel = os.path.relpath(family_index, root)
        if status is None:
            issues.append((os.path.relpath(spec_path, root), 'Status is missing'))
        elif not os.path.isfile(family_index):
            issues.append((family_rel, 'family index is missing'))
        else:
            family = open(family_index, encoding='utf-8').read()
            row = re.search(
                rf'^\|\s*`{re.escape(identifier)}`\s*\|\s*([^|]+?)\s*\|',
                family,
                re.M,
            )
            expected_lifecycle = status.split()[0]
            if row is None:
                issues.append((family_rel, f'no lifecycle row for {identifier}'))
            elif row.group(1).strip().split()[0] != expected_lifecycle:
                issues.append((family_rel, f'status is {row.group(1).strip()!r}; expected {expected_lifecycle!r}'))
    return issues


class Doc:
    def __init__(self, root, rel):
        self.rel = rel
        self.path = os.path.join(root, rel)
        self.text = open(self.path, encoding='utf-8').read()
        self.lines = self.text.split('\n')
        m = ID_LINE.search(self.text)
        self.ident = m.group(1).strip() if m else None
        self.heads = []          # (line, level, num, title)
        self.anchors = set()
        in_code = False
        for i, ln in enumerate(self.lines, 1):
            if ln.lstrip().startswith('```'):
                in_code = not in_code
                continue
            if in_code:
                continue
            if re.match(r'^#{1,6}\s', ln):
                t = re.sub(r'^#{1,6}\s+', '', ln).strip()
                self.anchors.add(slug(t))
            h = HEAD_RE.match(ln)
            if h:
                self.heads.append((i, len(h.group(1)), h.group(2), h.group(3)))
        self.nums = {}
        for (i, lv, n, t) in self.heads:
            self.nums.setdefault(n, (i, t))
        # line -> offset table
        self.offs = [0]
        for ln in self.lines:
            self.offs.append(self.offs[-1] + len(ln) + 1)

    def line_of(self, off):
        lo, hi = 0, len(self.offs) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.offs[mid] <= off:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1


def heading_defects(doc):
    out = []
    seen = {}
    last_child = {}   # parent -> last child int
    top_last = None
    for (i, lv, n, t) in doc.heads:
        parts = n.split('.')
        if n in seen:
            out.append((doc.rel, i, f'duplicate heading number {n} (first at line {seen[n]})'))
        seen.setdefault(n, i)
        depth = len(parts)
        # expected markdown level: top-level number uses the level of the first numbered heading
        if depth == 1:
            m = re.match(r'(\d+)([A-Z]?)$', parts[0])
            v = int(m.group(1))
            if not m.group(2):
                if top_last is not None and v != top_last + 1 and v != top_last:
                    out.append((doc.rel, i, f'top-level numbering jumps {top_last} -> {v}'))
                top_last = v
        else:
            parent = '.'.join(parts[:-1])
            if parent not in seen:
                out.append((doc.rel, i, f'heading {n} has no parent heading {parent}'))
            try:
                v = int(parts[-1])
                prev = last_child.get(parent, 0)
                if v != prev + 1:
                    out.append((doc.rel, i, f'subsection numbering under {parent} jumps {prev} -> {v}'))
                last_child[parent] = v
            except ValueError:
                pass
    # level consistency per depth
    lv_by_depth = defaultdict(lambda: defaultdict(list))
    for (i, lv, n, t) in doc.heads:
        lv_by_depth[len(n.split('.'))][lv].append(i)
    for d, m in lv_by_depth.items():
        if len(m) > 1:
            major = max(m, key=lambda k: len(m[k]))
            for lv, ls in m.items():
                if lv != major:
                    for i in ls:
                        out.append((doc.rel, i, f'depth-{d} heading uses markdown level {lv} (others use {major})'))
    return out


# ------------------------------------------------------------- reference ----
REF_RE = re.compile(
    r'(?P<kw>§§|§|\b[Ss]ections?\b|\bAnnex\b|\bAppendix\b)\s*'
    r'(?P<first>' + NUM + r'|[A-Z]\b)'
    r'(?P<rest>(?:\s*(?:,\s*(?:and|or)\s+|,|\band\b|\bor\b|\s/\s|/|–|—|-|\bthrough\b|\bto\b)\s*§?\s*' + NUM + r'(?![\w/]))*)'
)
SPLIT_RE = re.compile(r'(' + NUM + r')')
RANGE_SEP = re.compile(r'–|—|-|\bthrough\b|\bto\b')


def build_id_pattern(ids):
    alts = sorted(ids, key=len, reverse=True)
    return re.compile(r'(?<![\w./-])(' + '|'.join(re.escape(a) for a in alts) + r')(?![\w/-])')


def main():
    args = sys.argv[1:]
    if '-h' in args or '--help' in args:
        print(__doc__); sys.exit(0)
    positional = [a for i, a in enumerate(args)
                  if not a.startswith('--') and (i == 0 or args[i - 1] != '--tsv')]
    # Default: the repository this script lives in.
    root = os.path.abspath(positional[0] if positional
                           else os.path.join(os.path.dirname(__file__), '..'))
    tsv = None; quiet = '--quiet' in args
    if '--tsv' in args:
        tsv = args[args.index('--tsv') + 1]
    rels = git_md(root)
    docs = {r: Doc(root, r) for r in rels}

    # identifier -> primary document carrying the numbered sections
    idmap = {}
    for r, d in docs.items():
        if not d.ident:
            continue
        ident = d.ident.split(' - ')[0].strip()
        base = os.path.basename(r)
        prio = 0 if base == 'specification.md' else (1 if base not in ('index.md', 'overview.md') else 3)
        if base == 'envelope.md':
            prio = 5
        cur = idmap.get(ident)
        if cur is None or prio < cur[0]:
            idmap[ident] = (prio, r)
    idmap = {k: v[1] for k, v in idmap.items()}
    idpat = build_id_pattern(list(idmap))
    idalt = '|'.join(re.escape(a) for a in sorted(idmap, key=len, reverse=True))

    def spec_for_path(fromrel, target):
        p = os.path.normpath(os.path.join(os.path.dirname(fromrel), target.split('#')[0]))
        if p in docs:
            d = docs[p]
            if not d.heads:
                sib = os.path.join(os.path.dirname(p), 'specification.md')
                if sib in docs:
                    return sib
            return p
        return None

    def default_doc(rel):
        d = docs[rel]
        if d.heads:
            return rel
        sib = os.path.join(os.path.dirname(rel), 'specification.md')
        if sib in docs:
            return sib
        # family-level companion doc (profiles/<x>/<doc>.md): the single /1/ spec
        sib = os.path.join(os.path.dirname(rel), '1', 'specification.md')
        if sib in docs:
            return sib
        # nested identifier (e.g. rules-domain/1/registry) -> its parent spec
        ident = d.ident
        while ident and '/' in ident:
            ident = ident.rsplit('/', 1)[0]
            if ident in idmap:
                return idmap[ident]
        return None

    results = []   # dict rows
    for rel, d in docs.items():
        text = d.text
        # mask fenced code blocks
        masked = list(text)
        for m in re.finditer(r'```.*?```', text, re.S):
            for k in range(m.start(), m.end()):
                if masked[k] != '\n':
                    masked[k] = ' '
        masked = ''.join(masked)
        prev_end = -10**9; prev_spec = None; prev_qual = False; last_qual_spec = None
        for m in REF_RE.finditer(masked):
            line = d.line_of(m.start())
            if re.match(r'^#{1,6}\s', d.lines[line - 1]):
                continue  # heading text itself
            raw = m.group(0).rstrip(' ,;-–—')
            before = masked[max(0, m.start() - 160):m.start()]
            after = masked[m.end():m.end() + 120]
            kw = m.group('kw')
            spec = None; how = None
            if EXTERNAL.search(before[-25:].rstrip('` ')):
                results.append(dict(rel=rel, line=line, raw=raw, spec='EXTERNAL', nums=[], status='EXTERNAL', how='external', ctx=d.lines[line-1].strip()))
                prev_end = m.end(); prev_spec = 'EXTERNAL'; prev_qual = False
                continue
            # (a) explicit identifier immediately before (inside or outside backticks / link label)
            mb = None
            for x in idpat.finditer(before):
                mb = x
            if mb and re.fullmatch(r"[`\s'’s]*(?:\]\([^)]*\)[`\s]*)?", before[mb.end():]) :
                spec = idmap[mb.group(1)]; how = 'pre-id'
            elif mb and re.fullmatch(r"[`\s]*(?:wire-format\s+)?(?:envelope|annex)[`\s]*", before[mb.end():], re.I):
                env = os.path.join(os.path.dirname(idmap[mb.group(1)]), 'envelope.md')
                if env in docs:
                    spec = env; how = 'pre-id'
            # (b) markdown link immediately before
            if spec is None:
                ml = re.search(r'\]\(([^)\s]+)\)[`\s]*$', before)
                if ml and not ml.group(1).startswith('http'):
                    sp = spec_for_path(rel, ml.group(1))
                    if sp:
                        spec = sp; how = 'pre-link'
            # (b2) bare sibling filename before: "envelope.md §4"
            if spec is None:
                mf = re.search(r'(?<![\w/(])([\w.-]+\.md)[`\s]*$', before)
                if mf:
                    pth = os.path.normpath(os.path.join(os.path.dirname(rel), mf.group(1)))
                    if pth in docs:
                        spec = pth; how = 'pre-file'
            # (c) qualifier after: "of `X`", "in `X`", "of [X](...)"
            if spec is None:
                ma = re.match(r"\s*(?:of|in)\s+(?:the\s+)?[`\[]*(" + idalt + r")(?![\w/-])", after)
                if ma:
                    spec = idmap[ma.group(1)]; how = 'post-id'
                elif re.match(r'\s*of\s+(this|the present)\s+(document|specification)', after):
                    spec = default_doc(rel); how = 'post-this'
                elif re.match(r'\s*of\s+that\s+', after):
                    how = 'post-that'
                    sent = re.split(r'\.\s', before)[-1]
                    ids = list(idpat.finditer(sent))
                    if ids:
                        spec = idmap[ids[-1].group(1)]
            # (d) inheritance in a reference chain
            if spec is None and how != 'post-that' and prev_spec and prev_qual:
                gap = masked[prev_end:m.start()]
                if len(gap) <= 22 and re.fullmatch(r"[`\s,;()]*(?:(?:input\s+\d+\s*)?(?:and|or|,|/|–|—|-)?)[`\s,;()]*", gap):
                    spec = prev_spec; how = 'chain'
            # (d2) inside the same parenthetical as the previous qualified ref
            if spec is None and how != 'post-that' and prev_spec and prev_qual:
                gap = masked[prev_end:m.start()]
                head = masked[max(0, prev_end - 300):prev_end]
                open_paren = head.rfind('(') > head.rfind(')')
                if open_paren and len(gap) <= 60 and not re.search(r'[()]|\.\s|;', gap):
                    spec = prev_spec; how = 'paren-chain'
            # (e) list item that starts with a link to a spec: "- [X](...) — ... (§N)"
            if spec is None and how != 'post-that':
                ls = d.offs[line - 1]
                li = re.match(r'\s*[-*]\s+\[[^\]]*\]\(([^)\s]+)\)', text[ls:m.start()])
                if li and not li.group(1).startswith('http'):
                    sp = spec_for_path(rel, li.group(1))
                    if sp and sp != rel:
                        spec = sp; how = 'list-link'
            if spec is None:
                dd = default_doc(rel)
                if dd is None or not docs[dd].heads:
                    # no own numbering: inherit the last explicitly qualified spec of this document
                    spec = last_qual_spec or dd or rel; how = 'doc-inherit'
                else:
                    spec = dd; how = how or 'self'
                    # unqualified ref missing here but present in the spec named earlier in the same sentence
                    if prev_spec and prev_qual and prev_spec not in ('EXTERNAL',) and prev_spec != spec:
                        n0 = m.group('first')
                        gap = masked[prev_end:m.start()]
                        if n0 not in docs[spec].nums and n0 in docs[prev_spec].nums and '. ' not in gap and len(gap) < 200:
                            spec = prev_spec; how = 'sentence-inherit'
            # expand numbers
            first = m.group('first'); rest = m.group('rest') or ''
            nums = [first]
            ranges = []
            pos = 0
            tokens = re.split(r'(' + NUM + r')', rest)
            # tokens: sep, num, sep, num ...
            lastn = first
            for k in range(1, len(tokens), 2):
                sep = tokens[k - 1]; n = tokens[k]
                if RANGE_SEP.search(sep):
                    ranges.append((lastn, n))
                nums.append(n); lastn = n
            status = 'OK'; missing = []
            tdoc = docs.get(spec)
            if kw in ('Annex', 'Appendix') and re.fullmatch(r'[A-Z]', first):
                ok = tdoc and any(re.match(rf'^#+\s+(Annex|Appendix)\s+{first}\b', l) for l in tdoc.lines)
                status = 'OK' if ok else 'BROKEN'
                if not ok: missing = [first]
            else:
                for n in nums:
                    if not tdoc or n not in tdoc.nums:
                        missing.append(n)
                if missing:
                    status = 'BROKEN'
            titles = []
            for n in nums:
                if tdoc and n in tdoc.nums:
                    titles.append(f'{n} {tdoc.nums[n][1]}')
            ctx_start = d.offs[line - 1]
            ctx = text[max(ctx_start, m.start() - 200): m.end() + 120].replace('\n', ' ')
            sid = tdoc.ident.split(' - ')[0] if tdoc and tdoc.ident else spec
            if status == 'OK':
                for (rid, rx, okp) in SEMANTIC_RULES:
                    if sid == rid and rx.search(ctx):
                        for n in nums:
                            if not any(n == p or n.startswith(p + '.') for p in okp):
                                status = 'WRONG'; missing.append(f'{n}!sem')
            results.append(dict(rel=rel, line=line, raw=raw, spec=spec, sid=sid, nums=nums, status=status,
                                how=how, missing=missing, titles=titles, ctx=ctx))
            prev_end = m.end(); prev_spec = spec
            prev_qual = how in ('pre-id', 'pre-link', 'pre-file', 'post-id', 'post-that', 'chain', 'paren-chain', 'list-link', 'sentence-inherit')
            if how in ('pre-id', 'pre-link', 'pre-file', 'post-id'):
                last_qual_spec = spec

    # relative links
    link_issues = []
    for rel, d in docs.items():
        for m in re.finditer(r'\]\(([^)\s]+)\)', d.text):
            t = m.group(1)
            if re.match(r'^[a-z]+:', t) or t.startswith('mailto:'):
                continue
            pth, _, frag = t.partition('#')
            tgt = os.path.normpath(os.path.join(os.path.dirname(rel), pth)) if pth else rel
            full = os.path.join(root, tgt)
            ln = d.line_of(m.start())
            if not os.path.exists(full):
                link_issues.append((rel, ln, t, 'target missing'))
            elif frag and tgt in docs and frag not in docs[tgt].anchors:
                link_issues.append((rel, ln, t, 'anchor missing'))

    hdefects = []
    for d in docs.values():
        hdefects += heading_defects(d)

    # body citations must be listed in References
    ref_issues = []
    for rel, d in docs.items():
        if os.path.basename(rel) != 'specification.md' or not d.ident:
            continue
        own = d.ident.split(' - ')[0].strip()
        ref_at = None
        for (ln, level, num, title) in d.heads:
            if re.match(r'(?i)^references\b', title):
                ref_at = ln
        if ref_at is None:
            continue
        body = '\n'.join(d.lines[:ref_at - 1])
        body = re.sub(r'```.*?```', ' ', body, flags=re.S)
        refs = '\n'.join(d.lines[ref_at:])
        listed = set(m.group(1) for m in idpat.finditer(refs))
        cited = set(m.group(1) for m in idpat.finditer(body))
        for ident in sorted(cited - listed - {own}):
            # Versioned specification identifiers only: family indexes and
            # registry entries (rules/<version>) are not dependencies.
            if not re.search(r'/\d+$', ident) or ident.startswith('rules/'):
                continue
            if own.startswith(ident + '/') or ident.startswith(own + '/'):
                continue
            ref_issues.append((rel, ident))

    page_issues = companion_page_issues(root)

    if tsv:
        with open(tsv, 'w') as f:
            for r in results:
                f.write('\t'.join([f"{r['rel']}:{r['line']}", r['status'], r.get('how', ''), r.get('sid', r['spec']) or '',
                                   re.sub(r'\s+', ' ', r['raw']), ' | '.join(r.get('titles', [])), ','.join(r.get('missing', [])), r['ctx']]) + '\n')

    bad = [r for r in results if r['status'] in ('BROKEN', 'WRONG') and (r['rel'], r['line'], r['raw']) not in KNOWN_AMBIGUOUS]
    counts = defaultdict(int)
    for r in results:
        counts[r['status']] += 1
    print(f"documents indexed: {len(docs)}; identifiers: {len(idmap)}")
    print(f"references: {len(results)}  " + '  '.join(f'{k}={v}' for k, v in sorted(counts.items())))
    print(f"heading-numbering defects: {len(hdefects)}")
    if not quiet:
        for h in hdefects:
            print(f"  HEAD  {h[0]}:{h[1]}  {h[2]}")
    for r in bad:
        print(f"  {r['status']}  {r['rel']}:{r['line']}  [{r.get('sid')}] {r['raw']}  missing={r['missing']}  ({r['how']})")
        if not quiet:
            print(f"        ctx: {r['ctx'][:260]}")
    print(f"relative-link issues: {len(link_issues)}")
    for li in link_issues:
        print(f"  LINK  {li[0]}:{li[1]}  {li[2]}  ({li[3]})")
    print(f"cited but not in References: {len(ref_issues)}")
    for ri in ref_issues:
        print(f"  REFS  {ri[0]}  cites {ri[1]}")
    print(f"companion-page issues: {len(page_issues)}")
    for pi in page_issues:
        print(f"  PAGE  {pi[0]}  {pi[1]}")
    sys.exit(1 if (bad or link_issues or ref_issues or page_issues) else 0)


if __name__ == '__main__':
    main()
