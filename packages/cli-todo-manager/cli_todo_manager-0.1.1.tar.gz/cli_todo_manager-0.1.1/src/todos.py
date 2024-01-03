from dataclasses import dataclass
import datetime
import os
import sqlite3
import sys

from tabulate import tabulate

class ToDos:
    def __init__(self):
        self.database_connection = sqlite3.connect(".todos.db") if os.path.exists(".todos.db") else sys.exit("ToDo-list wasn't initialized use <todo init> to initialize the ToDo-list")
        self.cursor = self.database_connection.cursor()
        self.initialized = True if os.path.exists(".todos.db") else False
        self.weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        self.status_pending = "\033[93mPending ...\033[0m"
        self.status_in_progress = "\033[92mIn Progress\033[0m"
        self.status_finsished = "\033[96mFinished\033[0m"
        self.day = datetime.datetime.now().strftime('%d')
        self.month = datetime.datetime.now().strftime('%B')
        self.year = datetime.datetime.now().strftime('%Y')
        self.time = f"{self.day} {self.month} {self.year}"


    def update(self):
        if not self.initialized:
            sys.exit("ToDo-list wasn't initialized use <todo init> to initialize the ToDo-list")
        if len(sys.argv) != 3:
            sys.exit("Wrong amount of command line arguments")
        try:
            self.cursor.execute(
                "UPDATE todos set status = ? WHERE id = ? or todo = ?", (self.status_in_progress, sys.argv[2], sys.argv[2])
            )
            self.cursor.execute(
                "INSERT INTO logs (todo, time, action, status) VALUES ((SELECT todo FROM todos WHERE id = ? or todo = ?), ?, ?, (SELECT status FROM todos WHERE id = ? or todo = ?))", (sys.argv[2], sys.argv[2], self.time, "Updating Status", sys.argv[2], sys.argv[2])
            )
        except sqlite3.IntegrityError:
            sys.exit("Something went wrong")
        else:
            self.database_connection.commit()






    def logs(self):
        table = []
        if not self.initialized:
            sys.exit("ToDo-list wasn't initialized use <todo init> to initialize the ToDo-list")
        try:
            todos_ = self.cursor.execute("SELECT * FROM logs")
            check_list = todos_.fetchall()
            if not check_list:
                sys.exit("No results found")
            for todo in check_list:
                table.append(list(todo))
        except IndexError:
            sys.exit("Something went wrong")
        else:
            print(tabulate(table, headers=["ID", "ToDo", "Time", "Action", "Status"], tablefmt="grid"))






    def add(self, todo):
        if not self.initialized:
            sys.exit("ToDo-list wasn't initialized use <todo init> to initialize the ToDo-list")
        if len(sys.argv) != 4:
            sys.exit("Wrong amount of command line arguments")
        data = (todo.todo, todo.weekday.lower(), todo.importance, self.status_pending, todo.description)
        try:
            self.cursor.execute(
                "INSERT INTO todos (todo, weekday, importance, status, description) VALUES (?, ?, ?, ?, ?)", data
            )
            self.cursor.execute(
                "INSERT INTO logs (todo, time, action, status) VALUES ((SELECT todo FROM todos WHERE id = ? or todo = ?), ?, ?, (SELECT status FROM todos WHERE id = ? or todo = ?))", (sys.argv[2], sys.argv[2], self.time, "Adding ToDo", sys.argv[2], sys.argv[2])
            )
        except sqlite3.IntegrityError:
            sys.exit(f"Todo with the name {sys.argv[2]} already exists. Choose a different name")
        else:
            self.database_connection.commit()
        
        




    def show(self):
        table = []
        if not self.initialized:
            sys.exit("ToDo-list wasn't initialized use <todo init> to initialize the ToDo-list")
        try:
            requested = sys.argv[2].strip().lower()
        except IndexError:
            todos_ = self.cursor.execute("SELECT * FROM todos")
            check_list = todos_.fetchall()
            if not check_list:
                sys.exit("No results found")
            for todo in check_list:
                table.append(list(todo))
        else:
            data = (requested, requested, requested, requested, requested)
            todos_ = self.cursor.execute("SELECT * FROM todos WHERE weekday = ? or id = ? or todo = ? or importance = ? or status = ?", data)
            check_list = todos_.fetchall()
            if not check_list:
                sys.exit("No results found")
            for todo in check_list:
                table.append(list(todo))
        print(tabulate(table, headers=["ID", "ToDo", "Weekday", "Importance", "Description", "Status"], tablefmt="grid"))
            
        




    def show_history(self):
        table = []
        if not self.initialized:
            sys.exit("ToDo-list wasn't initialized use <todo init> to initialize the ToDo-list")
        try:
            requested = sys.argv[2].strip().lower()
        except IndexError:
            todos_ = self.cursor.execute("SELECT * FROM history")
            check_list = todos_.fetchall()
            if not check_list:
                sys.exit("No results found")
            for todo in check_list:
                table.append(list(todo))
        else:
            todos_ = self.cursor.execute("SELECT * FROM history WHERE finished_time = ? or id = ? or todo = ? or importance = ?", (requested, requested, requested, requested))
            check_list = todos_.fetchall()
            if not check_list:
                sys.exit("No results found")
            for todo in check_list:
                table.append(list(todo))
        print(tabulate(table, headers=["ID", "ToDo", "Finished", "Importance", "Description", "Comment", "Status"], tablefmt="grid"))
        
        



        
    @classmethod
    def create_database(cls):
        if not os.path.exists(".todos.db"):
            try:
                conn = sqlite3.connect(".todos.db")
                cur = conn.cursor()
                cur.execute("""
                    CREATE TABLE todos (
                        id INTEGER NOT NULL,
                        todo TEXT NOT NULL,
                        weekday TEXT NOT NULL,
                        importance TEXT,
                        description TEXT,
                        status TEXT,
                        PRIMARY KEY (id)
                        UNIQUE (todo)
                    )
                """)
                cur.execute("""
                    CREATE TABLE history (
                        id INTEGER NOT NULL,
                        todo TEXT NOT NULL,
                        finished_time TEXT NOT NULL,
                        importance TEXT,
                        description TEXT,
                        comment TEXT,
                        status TEXT,
                        PRIMARY KEY (id)
                    )
                """)
                cur.execute("""
                    CREATE TABLE logs (
                        id INTEGER NOT NULL,
                        todo TEXT NOT NULL,
                        time TEXT NOT NULL,
                        action TEXT,
                        status TEXT,
                        PRIMARY KEY (id)
                    )
                """)
                conn.commit()
            except:
                sys.exit("Something went wrong")
            else:
                sys.exit("Successfully initialized")
        else:
            sys.exit("This directory was already initialized")
       





    def remove(self):
        if not self.initialized:
            sys.exit("ToDo-list wasn't initialized use <todo init> to initialize the ToDo-list")
        if len(sys.argv) != 3:
            sys.exit("Wrong amount of arguments provided")
        todos_for_history = self.cursor.execute("SELECT * FROM todos WHERE id = ? or todo = ?", (sys.argv[2], sys.argv[2])).fetchone()
        if not todos_for_history:
            sys.exit("No Todo found with such id or name")
        else:
            id, todo, _, importance, description, __ = todos_for_history
            comment = input("Comment: ").strip()
            data = (todo, self.time, importance, self.status_finsished, description, comment)
            try:
                self.cursor.execute(
                    "INSERT INTO history (todo, finished_time, importance, status, description, comment) VALUES (?, ?, ?, ?, ?, ?)", data
                )
                self.cursor.execute(
                    "INSERT INTO logs (todo, time, action, status) VALUES ((SELECT todo FROM todos WHERE id = ? or todo = ?), ?, ?, (SELECT status FROM history WHERE id = ? or todo = ?))", (sys.argv[2], sys.argv[2], self.time, "Removing ToDo", sys.argv[2], sys.argv[2])
                )
                self.cursor.execute(
                    "DELETE FROM todos WHERE id = ? OR todo = ?", (sys.argv[2], sys.argv[2])
                )
            except:
                sys.exit("Couldn't remove todo. Try again...")
            else:
                self.database_connection.commit()



    


@dataclass
class ToDo:
    todo: str
    weekday: str
    description: str
    importance: str





if __name__ == "__main__":
    ToDos.create_database()
    todos = ToDos()
    
   
    todo = ToDo(sys.argv[1], sys.argv[2].lower(), input("Description: ").strip(), input("Importance: ").strip())
    todos.add(todo)
    todos.show()

    

    

