import pytest
from src.agent import run_agent

def test_basic_query():
    result = run_agent("2 + 2")
    assert "4" in result["final_answer"]