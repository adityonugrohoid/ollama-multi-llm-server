#!/usr/bin/env python3
"""Benchmark all available models on a standard prompt set."""

import argparse
import json
import sys
import time

import httpx

DEFAULT_API = "http://localhost:8080"

PROMPTS = [
    "Explain what a neural network is in two sentences.",
    "Write a Python function that checks if a string is a palindrome.",
    "Summarize the benefits of containerization in three bullet points.",
]

MODELS = [
    "gemma2:2b",
    "llama3.2:1b",
    "phi3:3.8b",
    "llama3.2:3b",
    "mistral:7b",
    "llama3.1:8b",
]


def run_benchmark(api_url: str, models: list[str], prompts: list[str]):
    results = []

    for model in models:
        model_results = {"model": model, "runs": [], "avg_latency_ms": 0}

        for prompt in prompts:
            print(f"  {model} | prompt {prompts.index(prompt) + 1}/{len(prompts)}...", end=" ", flush=True)

            try:
                start = time.time()
                resp = httpx.post(
                    f"{api_url}/inference/generate",
                    json={"prompt": prompt, "model": model, "max_tokens": 256},
                    timeout=120.0,
                )
                resp.raise_for_status()
                data = resp.json()
                wall_ms = int((time.time() - start) * 1000)

                run = {
                    "prompt": prompt[:60],
                    "latency_ms": data["latency_ms"],
                    "wall_ms": wall_ms,
                    "tokens": data["tokens_generated"],
                }
                tokens_per_sec = (
                    run["tokens"] / (run["latency_ms"] / 1000) if run["latency_ms"] > 0 else 0
                )
                run["tokens_per_sec"] = round(tokens_per_sec, 1)
                model_results["runs"].append(run)
                print(f"{data['latency_ms']}ms, {run['tokens_per_sec']} tok/s")

            except Exception as e:
                print(f"ERROR: {e}")
                model_results["runs"].append({"prompt": prompt[:60], "error": str(e)})

        successful = [r for r in model_results["runs"] if "latency_ms" in r]
        if successful:
            model_results["avg_latency_ms"] = round(
                sum(r["latency_ms"] for r in successful) / len(successful)
            )
            model_results["avg_tokens_per_sec"] = round(
                sum(r["tokens_per_sec"] for r in successful) / len(successful), 1
            )

        results.append(model_results)

    return results


def print_summary(results: list[dict]):
    print("\n" + "=" * 70)
    print(f"{'Model':<20} {'Avg Latency':>12} {'Avg tok/s':>12} {'Runs':>6}")
    print("-" * 70)
    for r in sorted(results, key=lambda x: x.get("avg_latency_ms", 999999)):
        successful = [run for run in r["runs"] if "latency_ms" in run]
        print(
            f"{r['model']:<20} {r.get('avg_latency_ms', 'N/A'):>10}ms "
            f"{r.get('avg_tokens_per_sec', 'N/A'):>11}/s "
            f"{len(successful):>5}/{len(r['runs'])}"
        )
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Benchmark Ollama models")
    parser.add_argument("--api", default=DEFAULT_API, help="API base URL")
    parser.add_argument("--models", nargs="*", default=MODELS, help="Models to benchmark")
    parser.add_argument("--output", help="Save JSON results to file")
    args = parser.parse_args()

    print(f"Benchmarking {len(args.models)} models against {len(PROMPTS)} prompts\n")
    results = run_benchmark(args.api, args.models, PROMPTS)
    print_summary(results)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
