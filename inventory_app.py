from __future__ import annotations

from copy import deepcopy
from typing import Any

import requests
from flask import Flask, jsonify, request


app = Flask(__name__)
items: list[dict[str, Any]] = []


def create_app() -> Flask:
    return app


@app.get("/items")
def list_items() -> tuple[Any, int]:
    return jsonify(items), 200


@app.post("/items")
def create_item() -> tuple[Any, int]:
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    quantity = payload.get("quantity")
    price = payload.get("price")

    if not name or quantity is None or price is None:
        return jsonify({"error": "name, quantity, and price are required"}), 400

    item = {"id": len(items) + 1, "name": name, "quantity": quantity, "price": price}
    items.append(item)
    return jsonify(item), 201


@app.put("/items/<int:item_id>")
def update_item(item_id: int) -> tuple[Any, int]:
    payload = request.get_json(silent=True) or {}
    for item in items:
        if item["id"] == item_id:
            if "name" in payload:
                item["name"] = payload["name"]
            if "quantity" in payload:
                item["quantity"] = payload["quantity"]
            if "price" in payload:
                item["price"] = payload["price"]
            return jsonify(item), 200
    return jsonify({"error": "item not found"}), 404


@app.delete("/items/<int:item_id>")
def delete_item(item_id: int) -> tuple[Any, int]:
    for index, item in enumerate(items):
        if item["id"] == item_id:
            del items[index]
            return jsonify({"deleted": item_id}), 200
    return jsonify({"error": "item not found"}), 404


@app.get("/products")
def fetch_product_details() -> tuple[Any, int]:
    query = request.args.get("query", "")
    if not query:
        return jsonify({"error": "query parameter is required"}), 400

    response = requests.get("https://world.openfoodfacts.org/api/v2/search", params={"search_terms": query, "page_size": 1, "json": 1})
    if response.status_code != 200:
        return jsonify({"error": "external api request failed"}), 502

    return jsonify(response.json()), 200
