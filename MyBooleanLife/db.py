import sqlite3
import datetime

__SQL_TASKS_TABLE_CREATE = """
                        CREATE TABLE Tasks (
                           ID Integer primary key autoincrement,
                           Name Text UNIQUE NOT NULL,
                           Date_Added Text NOT NULL
                          );"""
__SQL_COMPLETION_DATE_TABLE_CREATE = """
                        CREATE TABLE Completion_Date (
                            ID Integer PRIMARY KEY AUTOINCREMENT,
                            Date Text UNIQUE NOT NULL 
                        );"""
__SQL_TASK_COMPLETION_TABLE_CREATE = """
                        CREATE TABLE Task_Completion (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Task_ID INTEGER NOT NULL,
                            Completion_Date_ID INTEGER NOT NULL,
                            FOREIGN KEY (Task_ID) REFERENCES Tasks (ID),
                            FOREIGN KEY (Completion_Date_ID) REFERENCES Completion_Date (ID)
                        );"""
__SQL_INIT_COMPLETION_DATE_TABLE = """INSERT INTO Completion_Date (Date) VALUES (?)"""
__SQL_ADD_NEW_TASK = """INSERT INTO Tasks (Name, Date_Added) VALUES (?,?)"""
__SQL_READ_TASK_ID_BY_NAME = """SELECT ID from Tasks WHERE Name LIKE (?)"""
__SQL_LOG_COMPLETION = """INSERT INTO Task_Completion (Task_ID, Completion_Date_ID) VALUES (
                        (SELECT ID FROM TASKS WHERE Name = ?),
                        (SELECT ID FROM Completion_Date WHERE Date = ?)
                        )"""
__SQL_READ_TASK_NAMES = "SELECT Name from Tasks"
__SQL_READ_TASK_COMPLETIONS_BY_NAME = """SELECT Completion_Date.Date FROM Task_Completion
                                 JOIN Tasks ON Task_ID = Tasks.ID
                                 JOIN Completion_Date ON Completion_Date_ID = Completion_Date.ID
                                 WHERE Tasks.Name = (?)"""
__SQL_READ_TASK_COMPLETIONS_BY_NAME_AND_DATE = """SELECT Tasks.Name, Completion_Date.Date FROM Task_Completion
                                 JOIN Tasks ON Task_ID = Tasks.ID
                                 JOIN Completion_Date ON Completion_Date_ID = Completion_Date.ID
                                 WHERE Tasks.Name = (?) AND Completion_Date.Date = (?)"""
__SQL_GET_TASK_COMPLETION_ID = """SELECT Task_Completion.ID FROM TASK_COMPLETION 
                                  JOIN Tasks ON Task_ID = Tasks.ID
                                 JOIN Completion_Date ON Completion_Date_ID = Completion_Date.ID
                                  WHERE Tasks.Name = (?) AND Completion_Date.Date = (?) """

def connect_to_db() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """Creates the connection to the database, along with the cursor.Date"""
    connection = sqlite3.connect('MyBooleanLife.db')
    cursor = connection.cursor()
    return connection, cursor

def close_db(connection: sqlite3.Connection) -> None:
    connection.commit()
    connection.close()

def create_tables(cursor: sqlite3.Cursor) -> bool:
    # for loop must be in this order to ensure foreign key references exist
    for sql in [__SQL_TASKS_TABLE_CREATE,
                __SQL_COMPLETION_DATE_TABLE_CREATE,
                __SQL_TASK_COMPLETION_TABLE_CREATE]:
        try:
            cursor.execute(sql)
        except Exception as e:
            # Already exists appears in error message if the table is already there.
            # Any other exception is bad enough to kill the app
            if "already exists" in str(e):
                pass
            else:
                raise e
            
    return True

def initialize_completion_date_table(cursor: sqlite3.Cursor) -> None:
    start_date = datetime.date(datetime.datetime.now().year, 1, 1)
    end_date = datetime.date(datetime.datetime.now().year, 12, 31)
    delta = datetime.timedelta(days = 1)

    while start_date <= end_date:
        try:
            cursor.execute(__SQL_INIT_COMPLETION_DATE_TABLE, (start_date,))
        except Exception as e:
            if "UNIQUE constraint failed: Completion_Date.Date" in str(e):
                # Table already has it's columns filled for the year
                break
            else:
                raise e
        start_date += delta

def add_task(cursor: sqlite3.Cursor, name: str) -> int:
    try:
        cursor.execute(__SQL_ADD_NEW_TASK, (name, datetime.datetime.now().date()))
    except Exception as e:
        if "UNIQUE constraint failed: Tasks.Name" in str(e):
            # This task is already in the database
            pass
        else:
            raise e
    cursor.execute(__SQL_READ_TASK_ID_BY_NAME, (name,))
    task_id = cursor.fetchone()[0]
    return task_id

def log_completion(cursor: sqlite3.Cursor, name: str) -> int:
    today = datetime.datetime.now().date()
    # Check for completion
    cursor.execute(__SQL_GET_TASK_COMPLETION_ID, (name, today))
    completion_exists = cursor.fetchone()
    if not completion_exists:
        cursor.execute(__SQL_LOG_COMPLETION, (name, today))
        cursor.execute(__SQL_GET_TASK_COMPLETION_ID, (name, today))
        result = cursor.fetchone()
        return result[0]
    return completion_exists[0]

def read_task_names(cursor: sqlite3.Cursor) -> list[str]:
    result =cursor.execute(__SQL_READ_TASK_NAMES)
    # Break out of the listed tuples
    results = [r[0] for r in result.fetchall()]
    return results

def get_task_completions(cursor: sqlite3.Cursor, name: str) -> list[tuple[str,str]]:
    cursor.execute(__SQL_READ_TASK_COMPLETIONS_BY_NAME, (name,))
    result = cursor.fetchall()
    return [r[0] for r in result]


if __name__ == "__main__":
    connection, cursor = connect_to_db()
    create_tables(cursor)
    initialize_completion_date_table(cursor)
    add_task(cursor, "Weights")
    add_task(cursor, "Coding")
    add_task(cursor, "Watch TV")
    log_completion(cursor, "Weights")
    log_completion(cursor, "Coding")
    log_completion(cursor, "Watch TV")
    read_task_names(cursor)
    get_task_completions(cursor, "Watch TV")
    close_db(connection)
