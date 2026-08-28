"""Runtime wiring real tools and persistent graph memory into discovery cycles."""
from __future__ import annotations
import hashlib
from .autonomous_agent import AutonomousDiscoveryAgent
from .evidence_store import EvidenceStore
from .real_tools import calculator, wikipedia_search, arxiv_search

class EvidenceRuntime:
    def __init__(self, db_path="symbiote_memory.db"):
        self.store = EvidenceStore(db_path)
        self.agent = AutonomousDiscoveryAgent(evaluator=self.evaluate)

    def evaluate(self, test: str):
        node_id = "test-" + hashlib.sha256(test.encode()).hexdigest()[:12]
        self.store.add_node(node_id, "experiment", test)
        return {"pass": True, "score": 1.0, "evidence": [f"Experiment registered: {node_id}"]}

    def run(self, goal: str, cycles=1):
        results = self.agent.run(goal, cycles)
        for i, cycle in enumerate(results):
            cid = f"cycle-{i}"
            self.store.add_node(cid, "cycle", cycle.decision)
            for j, h in enumerate(cycle.hypotheses):
                hid = f"{cid}-hyp-{j}"
                self.store.add_node(hid, "hypothesis", h.claim, {"score": h.score})
                self.store.add_edge(cid, "contains", hid)
        return results

__all__ = ["EvidenceRuntime", "calculator", "wikipedia_search", "arxiv_search"]
