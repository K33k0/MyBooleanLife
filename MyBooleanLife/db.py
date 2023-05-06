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
__SQL_READ_TASK_BY_NAME = """SELECT ID from Tasks WHERE Name = (?)"""
__SQL_LOG_COMPLETION = """INSERT INTO Task_Completion (Task_ID, Completion_Date_ID) VALUES (
                        (SELECT ID FROM TASKS WHERE Name = ?),
                        (SELECT ID FROM Completion_Date WHERE Date = ?)
                        )"""


def connect_to_db() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """Creates the connection to the database, along with the cursor."""
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
    cursor.execute(__SQL_READ_TASK_BY_NAME, (name,))
    task_id = cursor.fetchone()[0]
    return task_id

def log_completion(cursor: sqlite3.Cursor, name: str) -> None:
    cursor.execute(__SQL_LOG_COMPLETION, (name, datetime.datetime.now().date()))

if __name__ == "__main__":
    connection, cursor = connect_to_db()
    create_tables(cursor)
    initialize_completion_date_table(cursor)
    add_task(cursor, "Weights")
    log_completion(cursor, "Weights")
    close_db(connection)