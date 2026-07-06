# Expense Tracker API

A REST API for managing expenses, built with FastAPI and PostgreSQL.

## Features

- Add, view, update, and delete expenses (full CRUD)
- Data persisted in a PostgreSQL database
- Input validation with Pydantic
- Configuration via environment variables

## Tech Stack

- **FastAPI** — web framework
- **PostgreSQL** — database
- **psycopg2** — Postgres driver
- **python-dotenv** — environment config

## Setup

1. Install dependencies:
   pip install fastapi uvicorn psycopg2-binary python-dotenv
2. Create a `.env` file (see `.env.example`):
   DB_NAME=expenses
   DB_USER=your_username
   DB_HOST=localhost

3. Run the server:
   python3 -m uvicorn main:app --reload

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/expenses` | Get all expenses |
| POST | `/expenses` | Add a new expense |
| PUT | `/expenses` | Update an expense by id |
| DELETE | `/expenses` | Delete an expense by id |

   
   
