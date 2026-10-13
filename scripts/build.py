#!/usr/bin/env python3
"""Merge src/base.yaml and src/fragments/*.yaml into the root openapi.yaml.

Usage: python scripts/build.py [--check]
  --check  exit non-zero if openapi.yaml is not up to date (used in CI).
"""
import glob
import os
import sys

import yaml


def _literal(dumper, value):
    style = "|" if "\n" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


yaml.SafeDumper.add_representer(str, _literal)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "openapi.yaml")


def build():
    with open(os.path.join(ROOT, "src", "base.yaml"), encoding="utf-8") as fh:
        spec = yaml.safe_load(fh)
    spec.setdefault("paths", {})
    schemas = spec["components"].setdefault("schemas", {})
    for name in sorted(glob.glob(os.path.join(ROOT, "src", "fragments", "*.yaml"))):
        with open(name, encoding="utf-8") as fh:
            fragment = yaml.safe_load(fh) or {}
        for path, item in (fragment.get("paths") or {}).items():
            spec["paths"].setdefault(path, {}).update(item)
        for schema, definition in ((fragment.get("components") or {}).get("schemas") or {}).items():
            if schema in schemas and schemas[schema] != definition:
                print(f"warning: schema {schema} redefined in {os.path.basename(name)}", file=sys.stderr)
            schemas[schema] = definition
    return yaml.dump(spec, Dumper=yaml.SafeDumper, sort_keys=False, allow_unicode=True, width=100), spec


def main():
    text, spec = build()
    if "--check" in sys.argv:
        current = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if current != text:
            sys.exit("openapi.yaml is out of date; run: python scripts/build.py")
        return
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"wrote {OUT}: {len(spec['paths'])} paths, {len(spec['components']['schemas'])} schemas")


if __name__ == "__main__":
    main()
