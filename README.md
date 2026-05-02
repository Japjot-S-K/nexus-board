# Nexus Board

A full-stack kanban task management application built with Python, FastAPI, Flask, and MongoDB Atlas. Designed as a resume project to demonstrate real-world backend architecture, REST API design, cloud database connectivity, and frontend rendering across two separate deployed services.

---

## Screenshots

> **Main Board**

<img width="1215" height="573" alt="image" src="https://github.com/user-attachments/assets/a01ad681-7c88-4b73-ba6c-94c6c53e085c" />

> **Create Task Modal**

<img width="373" height="410" alt="image" src="https://github.com/user-attachments/assets/05aeadcd-a111-49f3-9b8e-4790658827e5" />

> **AI Summarizer**

<img width="389" height="223" alt="image" src="https://github.com/user-attachments/assets/d39201ce-d663-4a47-8e36-a17ce64900e3" />
<img width="1919" height="955" alt="Screenshot 2026-05-02 134442" src="https://github.com/user-attachments/assets/540d6689-6a4d-494e-b9b7-6969ef35bb69" />

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI (Python) |
| Frontend Server | Flask (Python) |
| Database | MongoDB Atlas |
| Async DB Driver | Motor |
| Data Validation | Pydantic |
| Deployment | Render (two separate web services) |
| Version Control | GitHub |

---

## Architecture

Nexus Board is intentionally built as **two separate services** to demonstrate separation of concerns and a microservice-style architecture:

```
User Browser
     │
     ▼
Flask (port 5000) ── renders HTML ──► User sees the board
     │
     │ HTTP requests
     ▼
FastAPI (port 8000) ── CRUD logic ──► MongoDB Atlas
```

- **Flask** never touches the database directly. It only renders templates and calls FastAPI over HTTP.
- **FastAPI** never serves HTML. It exposes a clean REST API that returns JSON.
- **MongoDB Atlas** is the cloud-hosted database. FastAPI communicates with it asynchronously via Motor.

This mirrors how real production systems are structured — decoupled services that communicate over well-defined interfaces.

---

## Features

- **Kanban Board** — Three-column layout: Todo, In Progress, Done
- **Create Tasks** — Title, description, priority level, and due date
- **Edit Tasks** — Update any field on an existing task via a pre-filled modal
- **Move Tasks** — Progress tasks across columns with forward and back controls
- **Delete Tasks** — Remove tasks from any column
- **Priority Badges** — High / Medium / Low with colour-coded left borders on cards
- **Due Dates** — Displayed on each card when set
- **Stats Bar** — Live counts of total, todo, in-progress, done, and high-priority tasks with a completion progress bar
- **Search & Filter** — Filter tasks by keyword and priority simultaneously
- **AI Summarizer** — Click "Find out with AI" to get a natural language summary of your current workload built from live task data
- **Dark / Light Mode** — Theme toggle that persists across page refreshes via localStorage

---

## API Endpoints

All endpoints are served by FastAPI under the `/api` prefix.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks` | Fetch all tasks (supports `search`, `priority`, `status` query params) |
| GET | `/api/tasks/{id}` | Fetch a single task by ID |
| POST | `/api/tasks` | Create a new task |
| PATCH | `/api/tasks/{id}` | Update task fields (title, description, priority, status, due date) |
| DELETE | `/api/tasks/{id}` | Delete a task |

Interactive API docs available at `/docs` (Swagger UI) when running FastAPI locally.

---

## Project Structure

```
nexus-board/
├── fastapi_app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app entry point, CORS config
│   ├── database.py      # MongoDB Atlas connection via Motor
│   ├── models.py        # Pydantic schemas (TaskCreate, TaskUpdate, enums)
│   └── routes.py        # All CRUD route handlers
├── flask_app/
│   ├── __init__.py
│   ├── app.py           # Flask app, routes, AI summarizer logic
│   ├── templates/
│   │   └── index.html   # Kanban board UI, modals, JS
│   └── static/
│       └── style.css    # Full dark/light theme styling
├── .env                 # Local secrets (not committed)
├── .gitignore
├── Procfile.fastapi     # Render start command for FastAPI
├── Procfile.flask       # Render start command for Flask
├── render.yaml          # Render deployment config
└── requirements.txt
```

---

## Running Locally

**Prerequisites:** Python 3.10+, a MongoDB Atlas cluster, and an active virtual environment.

**1. Clone the repo and activate the virtual environment:**
```bash
git clone https://github.com/Japjot-S-K/nexus-board
cd nexus-board
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
```

**2. Set up your `.env` file:**
```env
MONGO_URI=your_mongodb_atlas_connection_string
MONGO_DB_NAME=nexusboard
FASTAPI_URL=http://localhost:8000/api
```

**3. Run FastAPI (Terminal 1):**
```bash
uvicorn fastapi_app.main:app --reload --port 8000
```

**4. Run Flask (Terminal 2):**
```bash
python flask_app/app.py
```

**5. Open your browser:**
```
http://localhost:5000
```

---

## Deployment

Both services are deployed independently on **Render** using the free tier.

| Service | URL |
|---|---|
| Flask UI | https://nexus-board-ui.onrender.com |
| FastAPI API | https://nexus-board-api.onrender.com |
| API Docs | https://nexus-board-api.onrender.com/docs |

MongoDB Atlas (M0 free tier) is used as the cloud database. The FastAPI service connects to Atlas on startup and keeps the connection alive for the lifetime of the process.

> Note: Free tier services on Render spin down after inactivity. The first request after a period of inactivity may take 30–50 seconds to respond while the service wakes up.

---

## Environment Variables

| Variable | Used By | Description |
|---|---|---|
| `MONGO_URI` | FastAPI | MongoDB Atlas connection string |
| `MONGO_DB_NAME` | FastAPI | Name of the MongoDB database |
| `FASTAPI_URL` | Flask | Base URL of the FastAPI service |

---

## Author

**Japjot Singh**  
[GitHub](https://github.com/Japjot-S-K)
