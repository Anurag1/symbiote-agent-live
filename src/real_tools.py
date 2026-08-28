"""Real, bounded tools used by the discovery agent."""
from __future__ import annotations
import ast
import operator
import urllib.parse
import urllib.request
import json

_ALLOWED = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg}

def _safe_eval(node):
    if isinstance(node, ast.Expression): return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)): return node.value
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED: return _ALLOWED[type(node.op)](_safe_eval(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED: return _ALLOWED[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    raise ValueError("unsupported expression")

def calculator(expression: str):
    return _safe_eval(ast.parse(expression, mode="eval"))

def wikipedia_search(term: str, sentences: int = 2):
    query = urllib.parse.quote(term)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.load(response)
    return {"title": data.get("title"), "summary": data.get("extract", ""), "source": data.get("content_urls", {}).get("desktop", {}).get("page", url)}

def arxiv_search(term: str, limit: int = 5):
    query = urllib.parse.quote(term)
    url = f"https://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={limit}"
    with urllib.request.urlopen(url, timeout=15) as response:
        raw = response.read().decode("utf-8")
    return {"query": term, "raw": raw, "source": url}
