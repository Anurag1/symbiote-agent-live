from src.autonomous_agent import AutonomousDiscoveryAgent


def test_cycle_contains_discovery_stages():
    agent = AutonomousDiscoveryAgent()
    cycle = agent.run_cycle("build a useful AI research tool")
    assert cycle.observations
    assert cycle.questions
    assert cycle.hypotheses
    assert cycle.contradictions
    assert cycle.experiments
    assert cycle.decision.startswith("Proceed with:")


def test_failed_experiment_is_rejected():
    agent = AutonomousDiscoveryAgent(lambda _: {"pass": False, "score": 0.99, "evidence": []})
    cycle = agent.run_cycle("test")
    assert all(h.score == 0.0 for h in cycle.hypotheses)


def test_multi_cycle_memory():
    agent = AutonomousDiscoveryAgent()
    cycles = agent.run("test", cycles=3)
    assert len(cycles) == 3
    assert len(agent.memory) == 3
