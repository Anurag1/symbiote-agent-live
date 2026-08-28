"""Small reproducible benchmark: baseline vs discovery controller."""
from dataclasses import dataclass
from time import perf_counter
from .autonomous_agent import AutonomousDiscoveryAgent

@dataclass
class BenchmarkResult:
    name: str
    tasks: int
    passed: int
    score: float
    seconds: float

def run_benchmark():
    tasks = [
        "Determine whether a claim has enough evidence to proceed.",
        "Find a falsifiable test for a proposed AI architecture.",
        "Record observations, hypotheses, contradictions and decisions.",
    ]
    t0 = perf_counter()
    agent = AutonomousDiscoveryAgent()
    passed = 0
    for task in tasks:
        cycle = agent.run_cycle(task)
        if cycle.hypotheses and cycle.contradictions and cycle.decision:
            passed += 1
    return BenchmarkResult("discovery-agent", len(tasks), passed, passed / len(tasks), perf_counter() - t0)

if __name__ == "__main__":
    print(run_benchmark())
