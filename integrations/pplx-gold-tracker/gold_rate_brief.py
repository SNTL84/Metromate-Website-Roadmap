#!/usr/bin/env python3
"""
Gold Rate Brief - Generate a structured precious metals market brief for
Surat/Gujarat gold and silver rates using Perplexity's Agent API with
web_search and fetch_url tools.

Adapted from perplexityai/api-cookbook's equity-research-brief example.
Original upstream file: docs/examples/equity-research-brief/equity_research_brief.py
This version swaps the finance_search-based equity workflow for a
web_search-based precious metals workflow suited to Tragad Soni's
goldsmith trade community.

Docs:
- Agent API: https://docs.perplexity.ai/docs/agent-api/quickstart
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from perplexity import Perplexity

# ---------------------------------------------------------------------------
# Configurations. 'gold_rate' is the primary config for this use case.
# ---------------------------------------------------------------------------
CONFIGS: Dict[str, Dict[str, Any]] = {
    "gold_rate": {
        # Live web-sourced precious metals rate lookup.
        "model": "perplexity/sonar",
        "max_tokens": 1024,
        "max_steps": 3,
        "tools": [{"type": "web_search"}, {"type": "fetch_url"}],
    },
    "research": {
        # Deeper multi-step precious metals market research.
        "model": "anthropic/claude-opus-4-7",
        "max_tokens": 4096,
        "max_steps": 10,
        "tools": [{"type": "web_search"}, {"type": "fetch_url"}],
    },
}

SYSTEM_PROMPT = """You are a precious metals market analyst tracking gold and
silver rates for the Indian trade and goldsmith community in Surat, Gujarat.
Be specific and quantitative. When you cite numbers, attribute them to the
relevant date/time. Never invent data: only use figures returned by
web_search or fetch_url. If a number is unavailable, say so explicitly.
Format the final output in clean Markdown."""

BRIEF_TEMPLATE = """Provide today's gold and silver rate brief for {ticker}.

Sections (in this order, all required):
1. **Current rate** - price per 10 grams in INR (22K and 24K gold, and
   silver per kg if available), with the as-of date/time.
2. **Daily change** - percentage and absolute change vs. yesterday's rate.
3. **Key drivers** - 2-3 current factors affecting the price (USD/INR rate,
   international spot price, local demand, festival/wedding season effects).
4. **Outlook** - 1-2 sentence short-term view, clearly labeled as analytical
   opinion, not financial advice.

End with a "Sources" section listing the URLs used."""


def build_client(api_key: Optional[str] = None) -> Perplexity:
    """Return an authenticated Perplexity client.

    Looks up the key in this order: explicit argument, ``PERPLEXITY_API_KEY``,
    ``PPLX_API_KEY``, then a ``.pplx_api_key`` / ``pplx_api_key`` file in the
    working directory.
    """
    if not api_key:
        api_key = os.environ.get("PERPLEXITY_API_KEY") or os.environ.get(
            "PPLX_API_KEY"
        )
    if not api_key:
        for candidate in (".pplx_api_key", "pplx_api_key"):
            path = Path(candidate)
            if path.exists():
                api_key = path.read_text().strip()
                break
    if not api_key:
        raise RuntimeError(
            "API key not found. Set PERPLEXITY_API_KEY, pass --api-key, or "
            "create a .pplx_api_key file."
        )
    return Perplexity(api_key=api_key)


def generate_brief(
    client: Perplexity,
    ticker: str,
    config_name: str = "gold_rate",
) -> Any:
    """Call the Agent API and return the raw response object."""
    cfg = CONFIGS[config_name]
    request: Dict[str, Any] = {
        "model": cfg["model"],
        "instructions": SYSTEM_PROMPT,
        "input": BRIEF_TEMPLATE.format(ticker=ticker),
        "tools": cfg["tools"],
        "max_output_tokens": cfg["max_tokens"],
    }
    if "max_steps" in cfg:
        request["max_steps"] = cfg["max_steps"]
    if "reasoning_effort" in cfg:
        request["reasoning"] = {"effort": cfg["reasoning_effort"]}
    return client.responses.create(**request)


# ---------------------------------------------------------------------------
# Pretty-printing helpers (unchanged logic from upstream equity brief example)
# ---------------------------------------------------------------------------

def _safe_output_text(response: Any) -> str:
    """Concatenate every assistant text block in the response output."""
    chunks: List[str] = []
    for item in getattr(response, "output", []) or []:
        item_type = getattr(item, "type", None) or (
            item.get("type") if isinstance(item, dict) else None
        )
        if item_type != "message":
            continue
        content = (
            getattr(item, "content", None)
            if not isinstance(item, dict)
            else item.get("content")
        )
        for block in content or []:
            block_type = getattr(block, "type", None) or (
                block.get("type") if isinstance(block, dict) else None
            )
            if block_type != "output_text":
                continue
            text = (
                getattr(block, "text", None)
                if not isinstance(block, dict)
                else block.get("text")
            )
            if text:
                chunks.append(text)
    return "\n\n".join(chunks)


def display(response: Any, format_json: bool = False) -> None:
    """Render the response to stdout."""
    if format_json:
        if hasattr(response, "model_dump"):
            print(json.dumps(response.model_dump(), indent=2, default=str))
        else:
            print(json.dumps(response, indent=2, default=str))
        return

    text = _safe_output_text(response)
    if text:
        print(text)

    cost = getattr(getattr(response, "usage", None), "cost", None)
    if cost is not None:
        if not isinstance(cost, dict):
            cost = cost.model_dump() if hasattr(cost, "model_dump") else {}
        total = cost.get("total_cost")
        currency = cost.get("currency", "USD")
        if total is not None:
            print(f"\nCost: {total:.4f} {currency}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a gold/silver rate brief for Surat/Gujarat using the "
            "Perplexity Agent API."
        )
    )
    parser.add_argument(
        "ticker",
        help="Query, e.g. '22K gold Surat', 'MCX gold futures', 'silver rate Gujarat'.",
    )
    parser.add_argument(
        "--config",
        choices=sorted(CONFIGS.keys()),
        default="gold_rate",
        help="Tool/model configuration: 'gold_rate' (default, fast web lookup) or 'research' (deeper multi-step).",
    )
    parser.add_argument(
        "--api-key",
        help="Perplexity API key (defaults to PERPLEXITY_API_KEY env var).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the raw Agent API response as JSON.",
    )
    args = parser.parse_args()

    try:
        client = build_client(args.api_key)
    except RuntimeError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    print(f"Generating {args.config} brief for '{args.ticker}'...", file=sys.stderr)

    try:
        response = generate_brief(client, args.ticker, args.config)
    except Exception as err:  # noqa: BLE001
        print(f"Agent API error: {err}", file=sys.stderr)
        return 2

    display(response, format_json=args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
