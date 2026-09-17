#!/usr/bin/env python3
"""The three-line change: point an OpenAI-SDK client at a different gateway.

No network calls here — the module only builds the client so CI can run it without credentials.
"""
from __future__ import annotations

import os


def build_client(provider: str = "candidate"):
    from openai import OpenAI

    if provider == "openrouter":
        return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
    return OpenAI(base_url=os.environ.get("APIMART_BASE_URL", "https://api.apimart.ai/v1"),
                  api_key=os.environ["APIMART_API_KEY"])


def main() -> None:
    for provider in ("openrouter", "candidate"):
        try:
            client = build_client(provider)
        except KeyError as exc:
            print(f"{provider}: skipped (missing {exc.args[0]})")
            continue
        print(f"{provider}: client ready for {client.base_url}")
    print("Same request body, same messages: only base_url, key and model id change.")


if __name__ == "__main__":
    main()
