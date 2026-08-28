import json
from dataclasses import asdict
from src.autonomous_agent import AutonomousDiscoveryAgent


def main():
    goal = "turn my AI research ideas into a validated, useful prototype"
    agent = AutonomousDiscoveryAgent()
    cycles = agent.run(goal, cycles=3)
    print(json.dumps(asdict(cycles[-1]), indent=2))
    print("\nAUTONOMY CHECK: observe -> question -> hypothesis -> contradiction -> experiment -> decision -> memory")
    print(f"cycles={len(agent.memory)}")


if __name__ == "__main__":
    main()
