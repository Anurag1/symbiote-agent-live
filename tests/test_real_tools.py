from src.real_tools import calculator
from src.evidence_store import EvidenceStore

def test_calculator():
    assert calculator("2 + 2 * 3") == 8

def test_graph_persistence(tmp_path):
    path = tmp_path / "memory.db"
    store = EvidenceStore(str(path))
    store.add_node("h1", "hypothesis", "test")
    store.add_node("e1", "evidence", "result")
    store.add_edge("h1", "supported_by", "e1")
    assert store.related("h1") == [{"source": "h1", "relation": "supported_by", "target": "e1"}]
    store.close()
