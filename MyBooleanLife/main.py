import sqlite3
from datetime import datetime

conn = sqlite3.connect('MyBooleanLife.db')
cursor = conn.cursor()


def init_db():
    global cursor
    sql = "CREATE TABLE tasks (name TEXT)"
    cursor.execute(sql)


    

def initialize_task(db, task_name):

    task = Query()
    results = db.search((task.name == task_name))
    if not results:
        task_table.insert({'name': task_name})
    
def mark_task_done(db, task_name):
    task = Query()
    results = db.search((task.name == task_name) & (task.date == str(datetime.now().date())))
    if not results:
        task_table.insert({'name': task_name, 'date': str(datetime.now().date())})

def read_task_completion(db, task_name):
    task = Query()
    results = db.search((task.name == task_name))
    return results

initialize_task(db, "GoToWork")
mark_task_done(db, "GoToWork")
read_task_completion(db, "GoToWork")