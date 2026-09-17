# Security

- No credentials live in this repository; provider settings come from environment variables (`.env.example` is a template).
- The scanner in `openai_migration_check.py` reads local files only and never uploads source code.
- Never commit an API key. A key pasted into an issue, a log or a screenshot should be rotated immediately.
- Retried requests must reuse an `Idempotency-Key`, otherwise a timeout can bill the same generation twice.
- Report a leaked key or a security problem privately to the maintainer rather than in a public issue.
