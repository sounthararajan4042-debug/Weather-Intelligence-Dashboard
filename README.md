# Weather Intelligence Dashboard

A Python-based desktop application that provides weather information for different cities using the Open-Meteo API.

## Features

- Search weather by city name
- Display current temperature
- Show humidity and wind speed
- Display feels-like temperature
- Save favorite cities
- Maintain search history
- Modern dark-themed desktop interface

## Technologies Used

- Python
- CustomTkinter
- FastAPI
- SQLite
- Requests
- Open-Meteo API
- Uvicorn
- Pydantic

## Project Architecture

The application uses a frontend and backend architecture.

1. CustomTkinter provides the desktop user interface.
2. FastAPI handles backend requests.
3. Requests communicates with the backend and external weather API.
4. Open-Meteo provides weather and geographical information.
5. SQLite stores search history and favorite cities.

## Project Structure

```text
Weather-Intelligence-Dashboard/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   └── weather_service.py
│
├── dashboard/
│   ├── __init__.py
│   └── gui.py
│
├── run_api.py
├── run_app.py
└── README.md
```

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd Weather-Intelligence-Dashboard
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install fastapi uvicorn requests customtkinter pydantic
```

## Run the Application

First, start the FastAPI backend:

```bash
python run_api.py
```

Open another terminal and run the desktop application:

```bash
python run_app.py
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API status |
| GET | `/health` | Health check |
| GET | `/weather` | Get weather |
| GET | `/history` | View search history |
| GET | `/favorites` | View favorites |
| POST | `/favorites` | Add favorite |
| DELETE | `/favorites/{city}` | Remove favorite |

## Learning Outcomes

- Python application development
- REST API integration
- FastAPI backend development
- SQLite database operations
- GUI development
- Frontend and backend communication
- Exception handling and threading

## Author

Developed as a Python project to gain practical experience in desktop application development and API integration.
