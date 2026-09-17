# Contributing

Useful contributions:

1. A dimension we are missing, phrased as a question a buyer would ask before migrating.
2. A migration failure mode with the fix (and the check that would have caught it earlier).
3. A correction to a cell in `data/alternatives.json`, citing the provider documentation and the date you checked it.

Before opening a pull request:

```bash
python tools/migrate_checklist.py --dimensions
python tools/migrate_checklist.py --from openrouter --to per-unit-relay
python tools/check_links.py
```

Rules: describe archetypes rather than marketing claims, disclose your affiliation, never state an unverified number,
and keep every APIMart link attributed through its `go.apimart.ai` short link.
