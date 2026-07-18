# Inventory Management System

A small Flask-based inventory management system with CRUD endpoints, an external product lookup integration, a CLI, and unit tests.

## Features

- Create, read, update, and delete inventory items through a REST API
- Look up product details from the OpenFoodFacts API by query term
- Interact with the API from a command-line interface
- Validate behavior with unit tests

## Project structure

- inventory_app.py: Flask app and REST API endpoints
- cli.py: command-line client for interacting with the API
- tests/test_inventory.py: unit tests for the API and CLI

## Setup

Install dependencies:

```bash
pip install flask requests pytest
```

## Run the API

Start the Flask app:

```bash
flask --app inventory_app run
```

## Example API calls

- List items: GET /items
- Create an item: POST /items with JSON body
- Update an item: PUT /items/<id>
- Delete an item: DELETE /items/<id>
- Product lookup: GET /products?query=milk

## Run the CLI

```bash
python cli.py list
python cli.py lookup --query milk
```

## Run tests

```bash
pytest -q
```