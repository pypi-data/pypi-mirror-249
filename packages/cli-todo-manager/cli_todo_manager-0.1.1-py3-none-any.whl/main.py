import os
import sys


from todos import ToDos, ToDo


def add_todo():
    todos = ToDos()
    try:
        if sys.argv[3] not in todos.weekdays:
            sys.exit("Not a valid day")
        todo = ToDo(sys.argv[2], sys.argv[3], input("Description: ").strip(), input("Importance: ").strip())
    except IndexError:
        sys.exit("Missing commeand line arguments => todo add <todo-name> <weekday>")
    else:
        todos.add(todo)

def init():
    ToDos.create_database()

def remove_todo():
    todos = ToDos()
    todos.remove()

def show():
    todos = ToDos()
    todos.show()

def show_history():
    todos = ToDos()
    todos.show_history()

def update_status():
    todos = ToDos()
    todos.update()

def show_logs():
    todos = ToDos()
    todos.logs()

def todo():
    if sys.argv[1] == "add":
        try:
            add_todo()
        except KeyboardInterrupt:
            sys.exit("\nOperation canceled")
    elif sys.argv[1] == "init":
        init()
    elif sys.argv[1] == "remove":
        try:
            remove_todo()
        except KeyboardInterrupt:
            sys.exit("\nOperation canceled")
    elif sys.argv[1] == "show":
        show()
    elif sys.argv[1] == "history":
        show_history()
    elif sys.argv[1] == "update":
        update_status()
    elif sys.argv[1] == "logs":
        show_logs()
    else:
        sys.exit("Invalid command")
