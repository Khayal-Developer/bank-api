 # Bank API

A mini banking REST API built with Python, FastAPI, and PostgreSQL.

Built as a capstone project for the Andersen Python traineeship technical interview preparation.

## Features (planned)

- Customer registration and management
- Multiple account types (Savings, Checking)
- Deposit, withdraw, transfer operations
- Transaction history
- REST API with proper authentication
- PostgreSQL persistence
- Docker containerization

## Tech Stack

- **Language:** Python 3.12
- **Framework:** FastAPI
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Testing:** pytest
- **Containerization:** Docker

## Architecture

The project follows SOLID principles with clear separation:
- `models/` — Domain entities (Money, Customer, Account)
- `exceptions/` — Custom exception types
- `services/` — Business logic
- `api/` — REST endpoints
- `tests/` — pytest test suite

## Status

Project in active development — building day-by-day.

## Author

Khayal — Andersen Python Trainee Candidate
