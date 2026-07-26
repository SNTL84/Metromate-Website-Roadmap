# Gold Rate Brief (pplx-gold-tracker)

Adapted from [perplexityai/api-cookbook](https://github.com/perplexityai/api-cookbook)'s `equity-research-brief` example, repurposed for Tragad Soni's gold/silver rate tracking in Surat, Gujarat.

This integration lives in its own folder and does not modify any other files in this repo.

## What it does

Uses Perplexity's Agent API (`web_search` + `fetch_url` tools) to generate a structured Markdown brief covering:

1. Current gold (22K/24K) and silver rate in INR, with as-of timestamp
2. Daily change vs. yesterday
3. Key market drivers (USD/INR, international spot, local demand)
4. Short-term outlook (clearly labeled as analysis, not financial advice)
5. Sources used

## Setup

```bash
pip install -r requirements.txt
```

Set your API key as an environment variable (get one from https://www.perplexity.ai/settings/api):

```bash
export PERPLEXITY_API_KEY="your-api-key-here"
```

Or create a `.env` / `.pplx_api_key` file locally. Never commit your API key to this repo.

## Usage

```bash
python gold_rate_brief.py "22K gold Surat"
python gold_rate_brief.py "silver rate Gujarat" --config gold_rate
python gold_rate_brief.py "MCX gold futures" --config research
python gold_rate_brief.py "22K gold Surat" --json
```

## Configs

- `gold_rate` (default) - fast, cheap, single web lookup via `perplexity/sonar`
- `research` - deeper multi-step research via `anthropic/claude-opus-4-7`

## Attribution

Original upstream source: `docs/examples/equity-research-brief/equity_research_brief.py` in perplexityai/api-cookbook (MIT License). This adapted version keeps the same auth, response-parsing, and cost-reporting logic, with the `finance_search` equity workflow replaced by a `web_search`-based precious metals workflow.
