"""Persistent SQLite evidence graph for autonomous discovery."""
from __future__ import annotations
import json
import sqlite3
from datetime import datetime, timezone

class EvidenceStore:
    def __init__(self, path: str = "symbiote_memory.db"):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS nodes (id TEXT PRIMARY KEY, kind TEXT, text TEXT, metadata TEXT, created_at TEXT)")
        self.db.execute("CREATE TABLE IF NOT EXISTS edges (source TEXT, relation TEXT, target TEXT, created_at TEXT, PRIMARY KEY(source, relation, target))")
        self.db.commit()

    def add_node(self, node_id: str, kind: str, text: str, metadata: dict | None = None):
        now = datetime.now(timezone.utc).isoformat()
        self.db.execute("INSERT OR REPLACE INTO nodes VALUES (?, ?, ?, ?, ?)", (node_id, kind, text, json.dumps(metadata or {}), now))
        self.db.commit()

    def add_edge(self, source: str, relation: str, target: str):
        now = datetime.now(timezone.utc).isoformat()
        self.db.execute("INSERT OR IGNORE INTO edges VALUES (?, ?, ?, ?)", (source, relation, target, now))
        self.db.commit()

    def related(self, node_id: str):
        rows = self.db.execute("SELECT source, relation, target FROM edges WHERE source=? OR target=?", (node_id, node_id)).fetchall()
        return [{"source": s, "relation": r, "target": t} for s, r, t in rows]

    def close(self):
        self.db.close()
