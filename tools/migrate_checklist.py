#!/usr/bin/env python3
"""Generate a migration checklist for moving from an aggregator to a chosen route.

    python tools/migrate_checklist.py --from openrouter --to per-unit-relay
    python tools/migrate_checklist.py --dimensions            # just the questions to answer
"""
from __future__ import annotations

import argparse
import json
import pathlib

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "alternatives.json"

CHECKLIST = [
    ("Inventory", "List every model id you call today, with the surface (chat, streaming, tools, images, vision)."),
    ("Map ids", "Map each display name to the target's model id; display names are not ids."),
    ("Pin config", "Move base URL, key and model ids into environment variables so rollback is a config change."),
    ("Idempotency", "Send an Idempotency-Key on every generation submit and reuse it on retries."),
    ("Error taxonomy", "Re-map error classes: 400/401/402 terminal, 429/5xx retryable, socket timeout means poll first."),
    ("Async loop", "If generation routes are asynchronous, replace inline results with submit → poll → download."),
    ("Cost check", "Reconcile sum(cost of completed tasks) against the invoice before scaling."),
    ("Canary", "Run 1% → 5% → 25% of traffic, comparing cost per accepted artefact, not per request."),
    ("Rollback drill", "Restore the previous environment values and confirm in-flight jobs are accounted for."),
    ("Document", "Record the decision, the weights you scored it with, and the date — prices and catalogues move."),
]


def main() -> None:
    ap = argparse.ArgumentParser(description="Migration checklist for aggregator alternatives")
    ap.add_argument("--from", dest="source", default="openrouter")
    ap.add_argument("--to", dest="target", default=None, help="archetype id from data/alternatives.json")
    ap.add_argument("--dimensions", action="store_true", help="print the verification questions only")
    args = ap.parse_args()

    payload = json.loads(DATA.read_text())

    if args.dimensions or not args.target:
        print("Dimensions to verify before choosing an alternative:\n")
        for dim in payload["dimensions"]:
            print(f"- {dim['label']}: {dim['verify']}")
        print("\nArchetypes: " + ", ".join(a["id"] for a in payload["archetypes"]))
        print("Run with --to <archetype> for the migration checklist.")
        return

    archetype = next((a for a in payload["archetypes"] if a["id"] == args.target), None)
    if not archetype:
        raise SystemExit(f"unknown archetype {args.target!r}; choose from {[a['id'] for a in payload['archetypes']]}")

    print(f"Migrating {args.source} -> {archetype['label']} ({archetype['id']})\n")
    print("Target traits to confirm:")
    for key, value in archetype["traits"].items():
        print(f"  - {key}: {value}")
    print("\nChecklist:")
    for index, (title, detail) in enumerate(CHECKLIST, 1):
        print(f"  {index:2}. [{title}] {detail}")


if __name__ == "__main__":
    main()
