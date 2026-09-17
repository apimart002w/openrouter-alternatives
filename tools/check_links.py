#!/usr/bin/env python3
"""Attribution + data guard: every apimart link must be an API-minted go.apimart.ai short link."""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW_APIMART = re.compile(r"https://(?:[a-z0-9-]+\.)?apimart\.ai/[^\s)\]<>]*")
SHORT = re.compile(r"https://go\.apimart\.ai/k-[0-9a-f]+")
API_HOST = re.compile(r"https://api\.apimart\.ai/")
DOCS_HOST = re.compile(r"https://docs\.apimart\.ai/")
SELF_MADE = re.compile(r"[?&]utm_source=(?!kol_sponsor)[a-z_]+")
# The pricing page URL is recorded as data provenance (the snapshot source), not as an outbound link.
PROVENANCE = re.compile(r"https://apimart\.ai/(?:en|zh)/pricing")

problems: list[str] = []
for path in sorted(ROOT.rglob("*")):
    if not path.is_file() or path.suffix not in {".md", ".py", ".sh", ".mjs", ".json", ".yml"}:
        continue
    if path.name in {"check_links.py", "repo.json"} or ".git" in path.parts:
        continue
    if path.parts[-3:-1] == ("data",) and path.suffix == ".json":
        continue
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        if SELF_MADE.search(line):
            problems.append(f"{path.relative_to(ROOT)}:{lineno} hand-made tracking link (use the promo link API)")
        if SHORT.search(line):
            continue
        for url in RAW_APIMART.findall(line):
            if API_HOST.match(url) or DOCS_HOST.match(url) or PROVENANCE.match(url):
                continue
            problems.append(f"{path.relative_to(ROOT)}:{lineno} unattributed apimart link -> {url}")

data = ROOT / "data/pricing.json"
if data.exists():
    payload = json.loads(data.read_text())
    models = payload.get("models") or []
    if len(models) < 100:
        problems.append(f"data/pricing.json looks truncated: {len(models)} models")
    for m in models[:500]:
        if not m.get("id") or not m.get("prices"):
            problems.append(f"incomplete pricing record: {m.get('id')}")

if problems:
    print("\n".join(problems))
    sys.exit(1)
print("attribution and pricing data OK")
