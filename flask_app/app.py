from flask import Flask, render_template, request, redirect, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000/api")


@app.route("/")
def index():
    search = request.args.get("search", "")
    priority = request.args.get("priority", "")

    params = {}
    if search:
        params["search"] = search
    if priority:
        params["priority"] = priority

    response = requests.get(f"{FASTAPI_URL}/tasks", params=params)
    tasks = response.json() if response.status_code == 200 else []

    todo = [t for t in tasks if t["status"] == "todo"]
    in_progress = [t for t in tasks if t["status"] == "in_progress"]
    done = [t for t in tasks if t["status"] == "done"]

    stats = {
        "total": len(tasks),
        "todo": len(todo),
        "in_progress": len(in_progress),
        "done": len(done),
        "high": len([t for t in tasks if t["priority"] == "high"]),
    }

    return render_template("index.html",
        todo=todo, in_progress=in_progress, done=done,
        stats=stats, search=search, priority=priority
    )


@app.route("/tasks/create", methods=["POST"])
def create_task():
    due_date = request.form.get("due_date")
    data = {
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "priority": request.form.get("priority"),
        "due_date": due_date if due_date else None,
    }
    requests.post(f"{FASTAPI_URL}/tasks", json=data)
    return redirect(url_for("index"))


@app.route("/tasks/<task_id>/status", methods=["POST"])
def update_status(task_id):
    new_status = request.form.get("status")
    requests.patch(f"{FASTAPI_URL}/tasks/{task_id}", json={"status": new_status})
    return redirect(url_for("index"))


@app.route("/tasks/<task_id>/edit", methods=["POST"])
def edit_task(task_id):
    due_date = request.form.get("due_date")
    data = {
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "priority": request.form.get("priority"),
        "due_date": due_date if due_date else None,
    }
    data = {k: v for k, v in data.items() if v is not None}
    requests.patch(f"{FASTAPI_URL}/tasks/{task_id}", json=data)
    return redirect(url_for("index"))


@app.route("/tasks/<task_id>/delete", methods=["POST"])
def delete_task(task_id):
    requests.delete(f"{FASTAPI_URL}/tasks/{task_id}")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)