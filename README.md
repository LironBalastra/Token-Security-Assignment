# Token Security Project - Liron Balastra

## Description

A FastAPI-based application that exploring github repository.

## Prerequisites

- Python 3.10 or higher

## Installation

1. Clone the repository:

```bash
git clone [your-repository-url]
cd Liron_Token_Security
```

## Project Structure

```
Token Security Github Assignment/
├── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   └── ... (frontend files)
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    └── ... (backend files)
```

## Dependencies

The project uses the following main packages:

- `fastapi[all]`
- `aiohttp`
- `asyncio`

## Usage

To run the application - using Docker:
docker compose up --build

The API will be available at `http://localhost:8000`
The Front-React will be available at 'http://localhost:5173/'
