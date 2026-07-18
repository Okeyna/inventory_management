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

Create and activate the Pipenv environment:

```bash
pipenv install --dev
pipenv shell
```

If Pipenv fails on your machine because of Python version compatibility, use the project’s existing virtual environment directly:

```bash
./.venv/bin/python -m pytest -q
./.venv/bin/python -m flask --app inventory_app run
```

If you prefer to run a command without entering the shell:

```bash
pipenv run python -m pytest -q
pipenv run flask --app inventory_app run
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
pipenv run python cli.py list
pipenv run python cli.py lookup --query milk
```

## Run tests

```bash
pipenv run python -m pytest -q
```