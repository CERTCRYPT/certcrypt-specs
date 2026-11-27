#!/usr/bin/env python3
"""Require the CERTCRYPT name as plain text in the normative Markdown.

The name is written ``CERTCRYPT``, with no Markdown emphasis inside it: a reader
of the raw text sees the name, and a site that renders these documents applies
its own brand styling. ``**CERT**CRYPT`` is refused.

Usage:
  python3 scripts/check-brandword.py
  python3 scripts/check-brandword.py --fix
"""

from __future__ import annotations

import os
import sys


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
NORMATIVE = os.path.join(ROOT, 'normative')
MARKED = '**CERT**CRYPT'
PLAIN = 'CERTCRYPT'


def markdown_files():
    for base, dirs, files in os.walk(NORMATIVE):
        dirs.sort()
        for filename in sorted(files):
            if filename.endswith('.md'):
                yield os.path.join(base, filename)


def main():
    apply_fix = '--fix' in sys.argv[1:]
    unknown = [arg for arg in sys.argv[1:] if arg != '--fix']
    if unknown:
        print(f'unknown argument: {unknown[0]}', file=sys.stderr)
        return 2
    failures = []
    for path in markdown_files():
        with open(path, encoding='utf-8') as source:
            text = source.read()
        lines = [n for n, line in enumerate(text.split('\n'), 1) if MARKED in line]
        if not lines:
            continue
        failures.append((path, lines))
        if apply_fix:
            with open(path, 'w', encoding='utf-8', newline='') as target:
                target.write(text.replace(MARKED, PLAIN))
    if apply_fix:
        print(f'brandword: updated {len(failures)} normative Markdown files')
        return 0
    for path, lines in failures:
        rel = os.path.relpath(path, ROOT)
        for line in lines:
            print(f'{rel}:{line}: write CERTCRYPT as plain text, not {MARKED}')
    if failures:
        print(f'brandword: {sum(len(lines) for _, lines in failures)} marked uses in {len(failures)} files', file=sys.stderr)
        return 1
    print('brandword: the name is plain text in every normative document')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
