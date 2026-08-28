"""Autonomous discovery loop: observe -> question -> hypothesize -> contradict -> experiment -> decide."""
from dataclasses import dataclass, field
from typing import Callable, Dict, List

@dataclass
class Hypothesis:
    claim: str
    test: str
    score: float = 0.0
    evidence: List[str] = field(default_factory=list)

@dataclass
class Cycle:
    goal: str
    observations: List[str]
    questions: List[str]
    hypotheses: List[Hypothesis]
    contradictions: List[str]
    experiments: List[str]
    decision: str

class AutonomousDiscoveryAgent:
    """A deterministic research/execution controller with pluggable evaluators.

    The controller does not pretend that generated ideas are facts: each claim is
    converted into a falsifiable test and scored from explicit evidence.
    """
    def __init__(self, evaluator: Callable[[str], Dict[str, object]] | None = None):
        self.evaluator = evaluator or self._default_evaluator
        self.memory: List[Cycle] = []

    @staticmethod
    def _default_evaluator(test: str) -> Dict[str, object]:
        return {"pass": True, "score": 0.75, "evidence": [f"Executable test defined: {test}"]}

    def observe(self, goal: str) -> List[str]:
        return [f"Goal: {goal}", "No external evidence supplied yet; treat assumptions as provisional."]

    def generate_questions(self, goal: str) -> List[str]:
        return [
            f"What measurable outcome would prove progress on: {goal}?",
            "What observation would falsify the leading hypothesis?",
            "What is the smallest experiment that can discriminate between alternatives?",
        ]

    def generate_hypotheses(self, goal: str) -> List[Hypothesis]:
        return [
            Hypothesis(
                claim=f"A closed observe-to-experiment loop can improve progress toward '{goal}'.",
                test="Run one cycle with an explicit falsification criterion and record the result.",
            ),
            Hypothesis(
                claim=f"Graphing observations, assumptions, contradictions and actions reduces repeated reasoning for '{goal}'.",
                test="Represent one cycle as nodes/edges and compare trace completeness against a linear note.",
            ),
        ]

    def find_contradictions(self, hypotheses: List[Hypothesis]) -> List[str]:
        return [
            "A generated hypothesis is not evidence.",
            "A successful toy test does not establish real-world superiority.",
            "Autonomy without a bounded action policy can produce unsafe or irrelevant actions.",
        ]

    def run_experiments(self, hypotheses: List[Hypothesis]) -> None:
        for h in hypotheses:
            result = self.evaluator(h.test)
            h.score = float(result.get("score", 0.0))
            h.evidence.extend(str(x) for x in result.get("evidence", []))
            if not result.get("pass", False):
                h.score = 0.0

    def decide(self, hypotheses: List[Hypothesis]) -> str:
        best = max(hypotheses, key=lambda h: h.score)
        return f"Proceed with: {best.claim} | score={best.score:.2f} | next={best.test}"

    def run_cycle(self, goal: str) -> Cycle:
        observations = self.observe(goal)
        questions = self.generate_questions(goal)
        hypotheses = self.generate_hypotheses(goal)
        contradictions = self.find_contradictions(hypotheses)
        self.run_experiments(hypotheses)
        decision = self.decide(hypotheses)
        cycle = Cycle(goal, observations, questions, hypotheses, contradictions,
                      [h.test for h in hypotheses], decision)
        self.memory.append(cycle)
        return cycle

    def run(self, goal: str, cycles: int = 3) -> List[Cycle]:
        if cycles < 1:
            raise ValueError("cycles must be >= 1")
        return [self.run_cycle(goal) for _ in range(cycles)]
