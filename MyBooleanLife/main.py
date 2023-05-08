from . import db
from urllib.parse import unquote
# TODO: Initialization process
# TODO: Need a webserver of sorts. It'll need to communicate with vuejs. Should look into how this will integrate with docker.

from fastapi import FastAPI

app = FastAPI()
connection, cursor = db.connect_to_db()

@app.get("/")
async def root():
    return {"message": "MyBooleanLife"}

@app.get("/alltasks")
async def all_tasks():
    """Return all defined tasks"""
    tasks = db.read_task_names(cursor)
    return {"message": tasks}

@app.get("/task/{name}")
async def read_task(name):
    """Returns all completion dates for task defined in url"""
    completions = db.get_task_completions(cursor, name)
    return {"message": completions}

@app.get("/complete/{name}")
async def complete_task(name):
    """Logs given task as complete, returning the completion id"""
    name = unquote(name)
    print(name)
    completion_id = db.log_completion(cursor, name)
    return {"message": completion_id}