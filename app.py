from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = Path(os.getenv("TLGG_DATA_PATH", BASE_DIR / "data" / "tlgg.json"))

app = Flask(__name__)


def load_data(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"slides": []}
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def normalize_data(data: dict[str, Any]) -> dict[str, Any]:
    for entry in data.get("slides", []):
        entry["title"] = entry.get("title", "").lower()
        entry["context"] = entry.get("context", "").lower()
        for section in entry.get("sections", []):
            section["title"] = section.get("title", "").lower()
            section["details"] = [detail.lower() for detail in section.get("details", [])]
    return data


def search_data(query: str, data: dict[str, Any]) -> list[dict[str, Any]]:
    query = query.strip().lower()
    if not query:
        return []

    results: list[dict[str, Any]] = []
    for entry in data.get("slides", []):
        if query in entry.get("title", "") or query in entry.get("context", ""):
            results.append(entry)
            continue

        for section in entry.get("sections", []):
            in_section_title = query in section.get("title", "")
            in_section_details = any(query in detail for detail in section.get("details", []))
            if in_section_title or in_section_details:
                results.append(entry)
                break

    return results


def get_dataset() -> dict[str, Any]:
    return normalize_data(load_data(DATA_PATH))


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    query = ""
    results: list[dict[str, Any]] = []
    error = None

    data = get_dataset()
    if not data.get("slides"):
        error = (
            f"No data found at {DATA_PATH}. Put your JSON dataset there or set TLGG_DATA_PATH."
        )

    if request.method == "POST":
        query = request.form.get("query", "")
        if query and not error:
            results = search_data(query, data)

    return render_template("index.html", query=query, results=results, error=error)


@app.route("/api/search", methods=["GET"])
def api_search() -> tuple[Any, int] | Any:
    query = request.args.get("q", "")
    data = get_dataset()
    if not data.get("slides"):
        return jsonify({"error": f"No data found at {DATA_PATH}"}), 400
    return jsonify({"query": query, "count": len(search_data(query, data)), "results": search_data(query, data)})


if __name__ == "__main__":
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8501"))
    app.run(host=host, port=port, debug=False)
