import os
from dotenv import load_dotenv
from todolist.core.services import TodolistService
from todolist.storage.in_memory import InMemoryStorage
from todolist.exceptions import TodolistError

def print_menu():
    print("\n--- To-Do List Menu ---")
    print("1. List all projects")
    print("2. Create a new project")
    print("3. List tasks in a project")
    print("4. Add a task to a project")
    print("5. Edit a task")
    print("6. Delete a project")
    print("0. Exit")

def run_cli():
    """Main function to run the command-line interface."""
    load_dotenv()
    MAX_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECTS", 10))
    MAX_TASKS = int(os.getenv("MAX_NUMBER_OF_TASKS", 20))
    storage = InMemoryStorage()
    service = TodolistService(storage, max_projects=MAX_PROJECTS, max_tasks=MAX_TASKS)
    
    # Pre-populate with some data for easier testing
    p1 = service.create_project("Personal", "Tasks for home and personal life.")
    service.create_task(p1.id, "Buy groceries", "Milk, Bread, Cheese", "2025-10-15")

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                projects = service.list_projects()
                if not projects:
                    print("No projects found.")
                for p in projects:
                    print(p)
            
            elif choice == "2":
                name = input("Enter project name: ")
                desc = input("Enter project description: ")
                project = service.create_project(name, desc)
                print(f"✅ Project '{project.name}' created successfully!")

            elif choice == "3":
                proj_id = int(input("Enter project ID to list tasks: "))
                tasks = service.list_tasks(proj_id)
                if not tasks:
                    print("No tasks found for this project.")
                for t in tasks:
                    print(t)

            elif choice == "4":
                proj_id = int(input("Enter project ID to add task to: "))
                title = input("Enter task title: ")
                desc = input("Enter task description: ")
                deadline = input("Enter deadline (YYYY-MM-DD, optional): ")
                task = service.create_task(proj_id, title, desc, deadline)
                print(f"✅ Task '{task.title}' added successfully!")

            elif choice == "5":
                task_id = int(input("Enter task ID to edit: "))
                # Get current values to show as defaults
                current_task = service.get_task(task_id)
                
                print(f"(Leave blank to keep current value)")
                title = input(f"Enter new title [{current_task.title}]: ") or current_task.title
                desc = input(f"Enter new description [{current_task.description}]: ") or current_task.description
                status = input(f"Enter new status (todo/doing/done) [{current_task.status}]: ") or current_task.status
                
                current_deadline_str = current_task.deadline.strftime('%Y-%m-%d') if current_task.deadline else ""
                deadline_str = input(f"Enter new deadline (YYYY-MM-DD) [{current_deadline_str}]: ")
                
                # Handle case where user wants to keep existing deadline
                if deadline_str == "":
                    deadline_str = current_deadline_str
                
                task = service.edit_task(task_id, title, desc, status, deadline_str)
                print(f"✅ Task {task_id} updated successfully.")
                
            elif choice == "6":
                proj_id = int(input("Enter project ID to delete: "))
                storage.delete_project(proj_id) # Calling storage directly for simplicity here
                print(f"✅ Project {proj_id} and its tasks have been deleted.")

            elif choice == "0":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice, please try again.")

        except TodolistError as e:
            print(f"Error: {e}")
        except ValueError:
            print("Error: Invalid input. Please enter a number where required.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")