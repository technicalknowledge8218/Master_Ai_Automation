"""Master AI - Empirical LLM Benchmark Engine.

Evaluates models across reasoning, coding, long context, structured output,
instruction adherence, bilingual English/Hindi understanding, latency, and cost.
Persists results with evidence-based scorecards.
"""

from __future__ import annotations

import datetime
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .adapters.base_adapter import BaseLLMAdapter
from .model_registry import ModelRegistry
from .provider_registry import ProviderRegistry


@dataclass
class BenchmarkTask:
    """A standardized evaluation task with verification rule."""

    task_id: str
    category: str
    prompt: str
    system_prompt: str = "You are an intelligent assistant evaluated for precision."
    expected_indicator: str = ""
    min_tokens_out: int = 10


# Standardized benchmark tasks across all required dimensions
BENCHMARK_SUITE: List[BenchmarkTask] = [
    BenchmarkTask(
        task_id="BM-01-REASONING",
        category="general_reasoning",
        prompt="A farmer has 17 sheep. All but 9 die. How many sheep does the farmer have left? Explain your step-by-step logic concisely.",
        expected_indicator="9",
    ),
    BenchmarkTask(
        task_id="BM-02-RESEARCH",
        category="research_synthesis",
        prompt="Summarize the key differences between monolithic architectures and microservices in two concise paragraphs.",
        expected_indicator="microservices",
    ),
    BenchmarkTask(
        task_id="BM-03-CODING",
        category="coding_generation",
        prompt="Write a Python function named `find_primes(n: int) -> list[int]` implementing the Sieve of Eratosthenes with complete type hints.",
        expected_indicator="def find_primes",
    ),
    BenchmarkTask(
        task_id="BM-04-STRUCTURED-JSON",
        category="structured_output",
        prompt="Return a JSON object with keys 'project', 'version', and 'status'. Set project to 'Master AI', version to '2.0.0', and status to 'active'. Only return valid JSON.",
        expected_indicator="Master AI",
    ),
    BenchmarkTask(
        task_id="BM-05-INSTRUCTION-FOLLOWING",
        category="instruction_following",
        prompt="Reply with exactly three bullet points, each starting with the word 'VERIFIED'. Do not include an intro or conclusion.",
        expected_indicator="VERIFIED",
    ),
    BenchmarkTask(
        task_id="BM-06-BILINGUAL-HINDI",
        category="bilingual_hindi_english",
        prompt="नमस्ते! कृप्या मुझे समझाएं कि मशीन लर्निंग (Machine Learning) क्या है और इसका क्या महत्व है? उत्तर हिंदी में दें।",
        expected_indicator="मशीन",
    ),
    BenchmarkTask(
        task_id="BM-07-LONG-CONTEXT",
        category="long_context_retrieval",
        prompt="The secret code word hidden inside the document is PHOENIX-992. " + ("Context filler sentence repeating system configuration. " * 50) + "What was the secret code word?",
        expected_indicator="PHOENIX-992",
    ),
]


@dataclass
class TaskResult:
    """Result of an individual benchmark evaluation."""

    task_id: str
    category: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    passed_validation: bool
    estimated_cost_usd: float
    output_snippet: str
    error: Optional[str] = None


@dataclass
class BenchmarkReport:
    """Aggregated benchmark report for a model."""

    benchmark_id: str
    timestamp: str
    model_id: str
    provider: str
    total_tasks: int
    tasks_passed: int
    pass_rate_percent: float
    average_latency_ms: float
    total_cost_usd: float
    overall_rating: str  # EXCELLENT, PROFICIENT, MARGINAL, INADEQUATE
    results: List[TaskResult] = field(default_factory=list)


class BenchmarkEngine:
    """Orchestrates model evaluation across capability categories."""

    def __init__(
        self,
        provider_registry: ProviderRegistry | None = None,
        model_registry: ModelRegistry | None = None,
        results_dir: Path | None = None,
    ) -> None:
        self.provider_registry = provider_registry or ProviderRegistry()
        self.model_registry = model_registry or ModelRegistry()
        if results_dir is None:
            workspace_root = Path(__file__).resolve().parents[2]
            results_dir = workspace_root / "04_LLM_AND_AI" / "benchmarks" / "results"
        self.results_dir = results_dir
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def run_benchmark_for_model(self, model_id: str) -> BenchmarkReport:
        """Run standardized benchmark suite on target model."""
        profile = self.model_registry.get_model(model_id)
        if not profile:
            raise ValueError(f"Model '{model_id}' is not in registry.")

        adapter = self.provider_registry.get_adapter(profile.provider)
        if not adapter:
            raise ValueError(f"Provider adapter '{profile.provider}' is not registered.")

        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        bm_id = f"BM-{model_id.replace(':', '_')}-{timestamp_str}"

        task_results: List[TaskResult] = []
        total_latencies = 0.0
        total_cost = 0.0

        for task in BENCHMARK_SUITE:
            messages = [
                {"role": "system", "content": task.system_prompt},
                {"role": "user", "content": task.prompt},
            ]
            t0 = time.time()
            try:
                res = adapter.generate(messages=messages, model=model_id, max_tokens=1024)
                latency = round((time.time() - t0) * 1000, 2)
                content = res.get("choices", [{}])[0].get("message", {}).get("content", "")
                usage = res.get("usage", {})
                p_tokens = usage.get("prompt_tokens", len(task.prompt.split()))
                c_tokens = usage.get("completion_tokens", len(content.split()))
                cost = profile.estimate_cost_usd(p_tokens, c_tokens)

                # Validation assertion
                passed = False
                if task.expected_indicator:
                    passed = task.expected_indicator.lower() in content.lower()
                else:
                    passed = len(content.strip()) >= task.min_tokens_out

                task_results.append(
                    TaskResult(
                        task_id=task.task_id,
                        category=task.category,
                        prompt_tokens=p_tokens,
                        completion_tokens=c_tokens,
                        latency_ms=latency,
                        passed_validation=passed,
                        estimated_cost_usd=cost,
                        output_snippet=content[:160].replace("\n", " "),
                    )
                )
                total_latencies += latency
                total_cost += cost
            except Exception as e:
                latency = round((time.time() - t0) * 1000, 2)
                task_results.append(
                    TaskResult(
                        task_id=task.task_id,
                        category=task.category,
                        prompt_tokens=0,
                        completion_tokens=0,
                        latency_ms=latency,
                        passed_validation=False,
                        estimated_cost_usd=0.0,
                        output_snippet="",
                        error=str(e),
                    )
                )

        passed_count = sum(1 for r in task_results if r.passed_validation)
        total_tasks = len(task_results)
        pass_rate = round((passed_count / total_tasks) * 100, 1) if total_tasks > 0 else 0.0
        avg_latency = round(total_latencies / max(1, total_tasks), 2)

        if pass_rate >= 85.0:
            rating = "EXCELLENT"
        elif pass_rate >= 70.0:
            rating = "PROFICIENT"
        elif pass_rate >= 50.0:
            rating = "MARGINAL"
        else:
            rating = "INADEQUATE"

        report = BenchmarkReport(
            benchmark_id=bm_id,
            timestamp=datetime.datetime.now().isoformat(),
            model_id=model_id,
            provider=profile.provider,
            total_tasks=total_tasks,
            tasks_passed=passed_count,
            pass_rate_percent=pass_rate,
            average_latency_ms=avg_latency,
            total_cost_usd=round(total_cost, 6),
            overall_rating=rating,
            results=task_results,
        )

        self._save_report(report)
        return report

    def _save_report(self, report: BenchmarkReport) -> None:
        """Persist report to JSON file in results directory."""
        filename = f"{report.benchmark_id}.json"
        target_path = self.results_dir / filename
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(asdict(report), f, indent=2)

    def list_saved_reports(self) -> List[Dict[str, Any]]:
        """List summary of all persisted benchmark reports."""
        summaries = []
        for file in sorted(self.results_dir.glob("*.json"), reverse=True):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                summaries.append({
                    "benchmark_id": data.get("benchmark_id"),
                    "timestamp": data.get("timestamp"),
                    "model_id": data.get("model_id"),
                    "provider": data.get("provider"),
                    "pass_rate_percent": data.get("pass_rate_percent"),
                    "average_latency_ms": data.get("average_latency_ms"),
                    "overall_rating": data.get("overall_rating"),
                    "file_path": str(file),
                })
            except Exception:
                pass
        return summaries
