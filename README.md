# OpenRouter Alternatives — How to Choose an AI API Aggregator

Looking for **OpenRouter alternatives** usually means one of three things: the price moved, a model you need is missing,
or you want the same single-key convenience with a billing unit you can predict. This repository gives you the dimensions
to compare on, the migration checklist, and a script so the decision is reproducible instead of vibes.

**Attributed entry points:** [Browse the model catalog](https://go.apimart.ai/k-b82f4a) · [Current pricing](https://go.apimart.ai/k-bf4d4d) · [Get an API key](https://go.apimart.ai/k-8181e4)

```bash
python tools/migrate_checklist.py --dimensions             # the questions to answer first
python tools/migrate_checklist.py --from openrouter --to per-unit-relay
```

## The nine questions that decide it

| Dimension | What to verify |
| --- | --- |
| Model coverage | Which model ids do you actually call, and are all of them present? Display names are not ids. |
| Pricing unit | Per token, per image, per second or per call — and is it billed per request or per delivered artefact? |
| OpenAI compatibility | Same path and body for chat, streaming, tools, structured output, vision, images? What needs an adapter? |
| Bring your own keys | Can you attach provider keys, or does the platform own the provider relationship? |
| Free tier | Are free requests rate-limited or model-limited, and what happens when credits run out? |
| Rate limits & quotas | RPM, TPM, concurrency, and the exact error shape when you exceed them. |
| Async model | Does generation return a task id with a poll URL, and do result URLs expire? |
| Retention & regions | Log retention, training use, residency, and whether you need a data processing agreement. |
| Migration effort | base_url swap only, or model-id mapping plus parameter differences plus a new error taxonomy? |

Full archetype data (with the traits and scores this checklist is derived from) lives in
[`data/alternatives.json`](data/alternatives.json). Named products appear only as examples of an archetype.

## Archetypes, not a ranking

| Archetype | Typical fit | Visible cost of choosing it |
| --- | --- | --- |
| Unified aggregator (OpenRouter-style) | breadth across vendors, model shopping | per-token billing needs measurement; free tiers are rate-limited |
| Per-unit relay route | uniform batches of images, seconds or tokens | async poll loop; one extra hop; provider quirks can leak |
| Self-hosted gateway | data residency, full control | you operate upgrades, scaling and incidents |
| Direct vendor APIs | one model, deepest vendor features | one integration per vendor; no single key |

Score them with your own weights on the gateway side of this series
([`llm-gateway-comparison`](https://go.apimart.ai/k-dda2cc)) — the method is identical.

## Migration in an afternoon

`examples/swap_base_url.py` shows the whole change: the request body and messages stay, only `base_url`, the key and the
model id move.

```python
from openai import OpenAI

client = OpenAI(base_url="https://api.apimart.ai/v1", api_key=os.environ["APIMART_API_KEY"])
client.chat.completions.create(model="gpt-5.5", messages=[{"role": "user", "content": "hi"}])
```

Then run the checklist and keep these rules:

1. **Pin configuration.** Base URL, key and model ids in environment variables, so rollback is not a code change.
2. **Reuse idempotency keys.** A retried submit without one is a second charge.
3. **Replace inline results with submit → poll → download** if the target's generation routes are asynchronous.
4. **Reconcile before scaling.** Sum `cost` of completed tasks; compare against the invoice; then canary 1% → 5% → 25%.
5. **Re-check the catalogue.** Model ids and prices move; the catalogue in
   [`unified-ai-api-model-catalog`](https://go.apimart.ai/k-fa6008) is regenerated daily for exactly that reason.

## FAQ

**What is the cheapest OpenRouter alternative?**
Cheapest depends on your unit. Per-image and per-second routes make cost a multiplication, which beats token billing on
uniform batches; token billing with cache hits wins on small, repetitive requests. Compute cost per *accepted artefact*
for both before declaring a winner.

**Can I keep the same code when switching?**
Often yes for chat: the OpenAI request shape is widely implemented. Image, video and vision routes are where adapters
appear — different parameter names, different batch caps, and an asynchronous job model.

**How do I compare free tiers honestly?**
Treat free credits as a trial, not a price: measure what happens at the rate limit (queue, error, or silent downgrade)
and what the paid unit costs immediately after the free quota ends.

**What breaks first in a migration?**
Assumptions about synchronous completion and about model ids. Both surface as timeouts or validation errors rather than
wrong output, which is the good version of this failure.

## Related searches

- `openrouter alternatives`
- `openrouter alternative free models`
- `ai api aggregator`
- `unified ai api`
- `llm api comparison`
- `cheapest llm api`
- `openai compatible api`

## Attributed links (how this repository is measured)

| Purpose | Attributed link | Target |
| --- | --- | --- |
| Browse the model catalog | <https://go.apimart.ai/k-b82f4a> | `apimart.ai` |
| Current pricing page | <https://go.apimart.ai/k-bf4d4d> | `apimart.ai/pricing` |
| Get an API key | <https://go.apimart.ai/k-8181e4> | `apimart.ai/keys` |

Outbound APIMart links are minted through the promo link API; hand-made tracking parameters are rejected by
`tools/check_links.py` in CI.

## Disclosure

This repository documents how to compare and migrate between AI API aggregators; it is published to document that
method, not to claim official status for any vendor. Product names are used as examples only and belong to their owners.
Nothing here is a vendor scorecard: verify every cell against the provider's own documentation for your account.

## Repository map

```text
README.md                    the nine questions, archetypes, migration workflow
data/alternatives.json       dimensions, archetype traits and scores (schema: openrouter-alternatives-v1)
tools/migrate_checklist.py   checklist generator
examples/swap_base_url.py    the minimal code change
tools/check_links.py         attribution guard (CI)
```

## License

MIT — see [LICENSE](LICENSE).
