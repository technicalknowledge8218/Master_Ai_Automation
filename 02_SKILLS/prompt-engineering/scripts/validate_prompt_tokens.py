#!/usr/bin/env python3
"""
Prompt Token & Budget Validator
Estimates token counts using character/word heuristics (approx. 4 chars per token) and checks against budget limits.
"""

import argparse
import sys
import json

def estimate_tokens(text):
    # Rule of thumb for English text: ~4 characters per token or ~0.75 words per token
    char_count = len(text)
    word_count = len(text.split())
    est_by_chars = char_count / 4.0
    est_by_words = word_count / 0.75
    # Blend estimate
    est_tokens = int(round((est_by_chars + est_by_words) / 2.0))
    return {
        "characters": char_count,
        "words": word_count,
        "estimated_tokens": max(1, est_tokens)
    }

def main():
    parser = argparse.ArgumentParser(description="Estimate prompt tokens and validate budget")
    parser.add_argument("--prompt", required=True, help="Prompt text to validate")
    parser.add_argument("--max-tokens", type=int, default=4000, help="Maximum allowed token budget")
    args = parser.parse_args()

    metrics = estimate_tokens(args.prompt)
    metrics["max_tokens_budget"] = args.max_tokens
    metrics["within_budget"] = metrics["estimated_tokens"] <= args.max_tokens

    print(json.dumps(metrics, indent=2))
    if not metrics["within_budget"]:
        print(f"ERROR: Prompt exceeds token budget ({metrics['estimated_tokens']} > {args.max_tokens})", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
