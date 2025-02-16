from fastapi import FastAPI
from app.tasks import run_task

app = FastAPI()

@app.get("/")
def home():
    return {"message": "LLM-based Automation Agent is Running"}

@app.post("/run")
def run(task: dict):
    return run_task(task.get("task_name"), task.get("task_data"))
