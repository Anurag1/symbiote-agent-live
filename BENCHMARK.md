# Evidence-Grounded Agent Benchmark

## Objective
Compare a standard LLM agent with Symbiote's discovery controller under the same task set and evidence budget.

## Metrics
- task success
- evidence coverage
- unsupported-claim rate
- contradiction detection
- falsification-test quality
- persistence across runs
- latency and token/tool cost

## Protocol
1. Give both systems identical goals.
2. Allow identical external evidence sources.
3. Record complete traces.
4. Score claims only against retrieved evidence.
5. Repeat each task multiple times.
6. Report mean and variance; never treat toy-test success as proof of general superiority.

The repository's deterministic benchmark is an architecture smoke test, not a claim of state-of-the-art performance.
