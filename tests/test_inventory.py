import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from inventory_app import create_app
from cli import InventoryCLI


class InventoryAppTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_list_items_returns_empty_collection_initially(self):
        response = self.client.get("/items")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_create_update_and_delete_item(self):
        create_response = self.client.post(
            "/items",
            json={"name": "Keyboard", "quantity": 7, "price": 49.99},
        )
        self.assertEqual(create_response.status_code, 201)
        payload = create_response.get_json()
        self.assertEqual(payload["name"], "Keyboard")
        self.assertEqual(payload["quantity"], 7)
        self.assertEqual(payload["price"], 49.99)

        item_id = payload["id"]

        update_response = self.client.put(
            f"/items/{item_id}",
            json={"quantity": 10, "price": 59.99},
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.get_json()["quantity"], 10)
        self.assertEqual(update_response.get_json()["price"], 59.99)

        delete_response = self.client.delete(f"/items/{item_id}")
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response.get_json()["deleted"], item_id)

    def test_lookup_product_details_from_external_api(self):
        fake_response = type(
            "FakeResponse",
            (),
            {"status_code": 200, "json": lambda self: {"product": {"product_name": "Milk", "brands": "Acme"}}},
        )()

        with patch("inventory_app.requests.get", return_value=fake_response):
            response = self.client.get("/products?query=milk")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["product"]["product_name"], "Milk")


class InventoryCLITests(unittest.TestCase):
    def test_cli_can_list_items(self):
        cli = InventoryCLI(base_url="http://example.test")
        with patch("cli.requests.get", return_value=type("Response", (), {"status_code": 200, "json": lambda self: []})()):
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                cli.run(["list"])
            self.assertIn("No items available.", buffer.getvalue())

    def test_cli_can_lookup_product(self):
        cli = InventoryCLI(base_url="http://example.test")
        with patch("cli.requests.get", return_value=type("Response", (), {"status_code": 200, "json": lambda self: {"product": {"product_name": "Water"}}})()):
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                cli.run(["lookup", "--query", "water"])
            self.assertIn("Water", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
