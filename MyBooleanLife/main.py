from . import db
from urllib.parse import unquote
from typing import Union
# TODO: Initialization process
# TODO: Need a webserver of sorts. It'll need to communicate with vuejs. Should look into how this will integrate with docker.

from fastapi import FastAPI, Path

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
async def read_task(name: str) -> dict[str,list[str]]:
    """Returns all completion dates for task defined in url"""
    name = unquote(name)
    completions = db.get_task_completions(cursor, name)
    return {"message": completions}

@app.get("/complete/{name}")
async def complete_task(name: str) -> dict[str,Union[str,int]]:
    """Logs given task as complete, returning the completion id"""
    name = unquote(name)
    if name not in db.read_task_names(cursor):
        return {"message": "Task name not found."}
    completion_id = db.log_completion(cursor, name)
    return {"message": completion_id}

@app.get("/addtask/{name}")
async def add_task(name:str) -> dict[str,int]:
    """Add task to db, return task id"""
    name = unquote(name)
    task_id = db.add_task(cursor, name)
    return {"message": task_id}