import argparse
import datetime
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class Task:
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime


task_status = ["new", "in process", "revision", "complete", "cancel"]


class TaskManager:
    def __init__(self):
        self._tasks = []
    
    def add_task(self, task):
        while True:
            if task.status in task_status:
                self._tasks.append(task)
                break
            else:
                task.status = input("Status is not correct ")
    
    def save_tasks_to_file(self, filename):
        task_dict = [task.__dict__ for task in self._tasks]
        with open(filename, 'w') as file:
            json.dump(task_dict, file)
    
    def load_tasks_from_file(self, filename):
        with open(filename, 'r') as file:
            task_dict = json.load(file)
        self._tasks = [Task(**task) for task in task_dict]
    
    def view_task_history(self, title):
        for task in self._tasks:
            if task.title == title:
                print(f"History of task '{task.title}':")
                status_history = task.status.split(',')
                date_history = task.updated_at.split(',')
                print(f"____Status right now: {status_history[0]}; Date of last modification: {date_history[0]}")
                for i in range(1, len(status_history)):
                    print(f" ____Status: {status_history[i]}; Date of last modification: {date_history[i]}")
                break
        else:
            print(f" Task '{title}' not founded")
    
    def update_task_status(self, title, filename):
        for task in self._tasks:
            if task.title == title:
                print("1. the curren one status -> the previous one status")
                print("2. the curren one status -> the next one status")
                print("3. the curren one status -> status <cancel>")
                print("4. status <cancel> -> status <new>")
                update_status = input("Enter a number of command :")
                date_now = datetime.today().strftime("%Y-%m-%d")
                status_date = str(date_now)
                first_status = task.status.split(',')[0]
                
                if update_status == "1" and  first_status != "new":
                    update_status = task_status[task_status.index(first_status)-1]
                elif update_status == "1" and first_status == "new":
                    print("The status cannot be moved to the previous one")
                    update_status = ''
                elif update_status == "2" and first_status != "complete":
                    update_status = task_status[task_status.index(first_status)+1]
                elif update_status == "2" and first_status == "complete":
                    print("status can not be update in next")
                    update_status = ''
                elif update_status == "3":
                    update_status = task_status[4]
                elif update_status == "4" and first_status == "cancel":
                    update_status = task_status[0]
                else:
                    print("the command does not exist")
                    update_status = task.status
                
                if update_status == '':
                    task.status = task.status
                    task.updated_at = task.updated_at
                else:
                    task.status = update_status + ',' + task.status
                    task.updated_at = status_date + ',' + task.updated_at
                
                self.save_tasks_to_file(filename)
                print(f" Status: '{task.title}' is update. New status: '{update_status}'")
                break
        else:
            print(f"Task '{title}' is not founded")

parser = argparse.ArgumentParser(description="name of file with tasks")
parser.add_argument("filename", type=str)
args = parser.parse_args()

# rewrite task_meneger
task_manager = TaskManager()
try:
    task_manager.load_tasks_from_file(args.filename)
except FileNotFoundError:
    print("file doesn't exist")

while True:
    print('1) check task')
    print('2) update the status')
    print('3) create task')
    print('4) exit')
    number_of_task = input("Select an action: ")
    print("................................")
    # Check history 
    if number_of_task == "1":
        name = input("Enter the name of the task: ")
        task_manager.view_task_history(name)
    # Update
    elif number_of_task == "2":
        name = input("Enter the name of the task: ")
        task_manager.update_task_status(name, args.filename)
    # Create new task
    elif number_of_task == "3":
        date_now = str(datetime.today())
        new_task = Task(input("Enter the name of new task: "),
                        input("Enter the description of the task: "),
                        input("Enter the status of the task: new; in process; revision; complete; cancel :"),
                        date_now,
                        date_now)
        task_manager.add_task(new_task)
        task_manager.save_tasks_to_file(args.filename)
    # Exit
    elif number_of_task == "4":
        break
    else:
        print("unknown task")