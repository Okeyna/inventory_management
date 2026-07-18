import argparse
import requests


class InventoryCLI:
    def __init__(self, base_url: str = "http://127.0.0.1:5000") -> None:
        self.base_url = base_url.rstrip("/")

    def run(self, argv: list[str] | None = None) -> None:
        parser = argparse.ArgumentParser(description="Inventory management CLI")
        subparsers = parser.add_subparsers(dest="command", required=True)

        subparsers.add_parser("list", help="List all inventory items")

        lookup_parser = subparsers.add_parser("lookup", help="Fetch product details")
        lookup_parser.add_argument("--query", required=True, help="Search term for the product")

        args = parser.parse_args(argv)

        if args.command == "list":
            response = requests.get(f"{self.base_url}/items")
            if response.status_code != 200:
                print("Unable to fetch items.")
                return

            items = response.json()
            if not items:
                print("No items available.")
                return

            for item in items:
                print(f"{item['id']}: {item['name']} - qty {item['quantity']} - price {item['price']}")
            return

        if args.command == "lookup":
            response = requests.get(f"{self.base_url}/products", params={"query": args.query})
            if response.status_code != 200:
                print("Unable to fetch product details.")
                return

            data = response.json()
            product = data.get("product") or {}
            print(product.get("product_name") or "No product found")


if __name__ == "__main__":
    InventoryCLI().run()
