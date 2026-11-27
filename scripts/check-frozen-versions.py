#!/usr/bin/env python3
"""Verify that every frozen specification version still has its frozen bytes.

The manifest groups immutable paths into version sets. Each set commits to the
sorted path names and exact file bytes with SHA3-256. Family and registry
indexes that must list future successor versions stay outside the commitment;
concrete frozen registry entries are included explicitly.

Usage:
  python3 scripts/check-frozen-versions.py
  python3 scripts/check-frozen-versions.py --compute
"""

import hashlib
import json
import os
import subprocess
import sys


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MANIFEST = os.path.join(ROOT, 'frozen-versions.json')


def tracked_files():
    result = subprocess.run(
        ['git', '-C', ROOT, 'ls-files', '-z'],
        check=True,
        capture_output=True,
    ).stdout
    return sorted(path.decode('utf-8') for path in result.split(b'\0') if path)


def paths_for(version_set, tracked):
    selected = set(version_set.get('files', []))
    for root in version_set.get('roots', []):
        prefix = root['path'].rstrip('/') + '/'
        excluded = tuple(prefix + item.lstrip('/') for item in root.get('exclude', []))
        for path in tracked:
            if path.startswith(prefix) and not path.startswith(excluded):
                selected.add(path)
    return sorted(selected)


def digest(paths):
    value = hashlib.sha3_256()
    for path in paths:
        full = os.path.join(ROOT, path)
        if not os.path.isfile(full):
            raise FileNotFoundError(path)
        value.update(path.encode('utf-8'))
        value.update(b'\0')
        with open(full, 'rb') as source:
            value.update(source.read())
        value.update(b'\0')
    return value.hexdigest()


def main():
    compute = '--compute' in sys.argv[1:]
    unknown = [arg for arg in sys.argv[1:] if arg != '--compute']
    if unknown:
        print(f"unknown argument: {unknown[0]}", file=sys.stderr)
        return 2
    with open(MANIFEST, encoding='utf-8') as source:
        manifest = json.load(source)
    if manifest.get('format') != 'certcrypt-frozen-versions/1':
        print('frozen-versions.json: unsupported format', file=sys.stderr)
        return 1
    tracked = tracked_files()
    failed = False
    for version_set in manifest.get('sets', []):
        paths = paths_for(version_set, tracked)
        actual = digest(paths)
        expected = version_set.get('content_sha3_256')
        print(f"{version_set['id']}: {len(paths)} files · {actual}")
        if not compute and actual != expected:
            failed = True
            print(f"  expected: {expected}", file=sys.stderr)
            print('  frozen content changed; create a successor version instead of editing it in place', file=sys.stderr)
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
