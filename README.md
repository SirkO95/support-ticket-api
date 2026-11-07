# Support Ticket API

A RESTful API for managing customer support tickets, built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

This project provides basic ticket management functionality, including creating tickets, updating their status and priority, filtering tickets, and adding comments.

## Features

- Create new support tickets
- Retrieve all tickets
- Filter tickets by status and priority
- Retrieve a ticket by ID
- Update ticket information
- Add comments to existing tickets
- Automatic database table creation
- Interactive API documentation with Swagger UI

## Tech Stack

- **Python**
- **FastAPI** – REST API framework
- **SQLAlchemy** – ORM for database operations
- **SQLite** – database
- **Pydantic** – request validation
- **Uvicorn** – ASGI server

## Project Structure

```text
support-ticket-api/
│
├── app/
│   ├── routers/
│   │   └── tickets.py
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── .gitignore
├── README.md
└── tickets.db (generated locally)
```

## Installation

1. Clone the repository:

```bash
git clone git@github.com:SirkO95/support-ticket-api.git
cd support-ticket-api
```

2. Create a virtual environment:

```bash
python3 -m venv .venv
```

3. Activate the virtual environment:

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows:**

```bash
.venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install fastapi sqlalchemy "uvicorn[standard]"
```

## Run the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI provides interactive API documentation.

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| POST | `/tickets/` | Create a ticket |
| GET | `/tickets/` | Get all tickets |
| GET | `/tickets/?status=open` | Filter tickets by status |
| GET | `/tickets/?priority=high` | Filter tickets by priority |
| GET | `/tickets/{ticket_id}` | Get a ticket by ID |
| PATCH | `/tickets/{ticket_id}` | Update a ticket |
| POST | `/tickets/{ticket_id}/comments` | Add a comment |

## Ticket Fields

Each ticket contains:

- `id` – unique ticket identifier
- `title` – ticket title
- `description` – detailed description
- `status` – ticket status (default: `open`)
- `priority` – ticket priority (default: `medium`)
- `created_at` – creation timestamp
- `updated_at` – last update timestamp
- `comments` – associated comments

## Database

The application uses SQLite and SQLAlchemy ORM.

The database file (`tickets.db`) is created locally when the application starts.

## Future Improvements

- Add authentication and authorization
- Implement ticket deletion
- Add pagination
- Improve input validation for ticket status and priority
- Add automated tests

## Author

**SirkO95**

GitHub: https://github.com/SirkO95
