import os
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.exceptions.base import TodolistError
from app.models.project import Project

def print_menu():
    print("\n--- To-Do List Menu (RDB) ---")
    print("1. List all projects")
    print("2. Create a new project")
    print("3. Edit a project")
    print("4. List tasks in a project")
    print("5. Add a task to a project")
    print("6. Change a task's status")
    print("7. Edit a task's details")
    print("8. Delete a project")
    print("9. Delete a task")
    print("0. Exit")

def run_cli():
    """Main function to run the command-line interface."""
    MAX_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECTS", 10))
    MAX_TASKS = int(os.getenv("MAX_NUMBER_OF_TASKS", 20))

    # The CLI is responsible for creating and 'injecting' dependencies.
    db: Session = SessionLocal()
    
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    
    project_service = ProjectService(project_repo, max_projects=MAX_PROJECTS)
    task_service = TaskService(task_repo, max_tasks_per_project=MAX_TASKS)

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                projects = project_service.list_projects()
                if not projects:
                    print("No projects found.")
                for p in projects:
                    print(p)
            
            elif choice == "2":
                name = input("Enter project name: ")
                desc = input("Enter project description: ")
                project = project_service.create_project(name, desc)
                print(f"✅ Project '{project.name}' created successfully!")

            elif choice == "3":
                proj_id = int(input("Enter project ID to edit: "))
                current_project = project_service.get_project(proj_id)

                print("(Leave blank to keep current value)")
                name = input(f"Enter new name [{current_project.name}]: ") or current_project.name
                desc = input(f"Enter new description [{current_project.description}]: ") or current_project.description

                project = project_service.edit_project(proj_id, name, desc)
                print(f"✅ Project {project.id} updated successfully.")
            
            elif choice == "4":
                proj_id = int(input("Enter project ID to list tasks: "))
                tasks = task_service.list_tasks(proj_id)
                if not tasks:
                    print("No tasks found for this project.")
                for t in tasks:
                    print(t)

            elif choice == "5":
                proj_id = int(input("Enter project ID to add task to: "))
                title = input("Enter task title: ")
                desc = input("Enter task description: ")
                deadline = input("Enter deadline (YYYY-MM-DD, optional): ")
                task = task_service.create_task(proj_id, title, desc, deadline)
                print(f"✅ Task '{task.title}' added successfully!")

            elif choice == "6":
                task_id = int(input("Enter task ID to change status: "))
                status = input("Enter new status (todo/doing/done): ")
                task = task_service.change_task_status(task_id, status)
                print(f"✅ Task {task_id} status updated to '{task.status}'.")
            
            elif choice == "7":
                task_id = int(input("Enter task ID to edit: "))
                current_task = task_service.get_task(task_id)
                
                print(f"(Leave blank to keep current value)")
                title = input(f"Enter new title [{current_task.title}]: ") or current_task.title
                desc = input(f"Enter new description [{current_task.description}]: ") or current_task.description
                status = input(f"Enter new status (todo/doing/done) [{current_task.status}]: ") or current_task.status
                
                current_deadline_str = current_task.deadline.strftime('%Y-%m-%d') if current_task.deadline else ""
                deadline_str = input(f"Enter new deadline (YYYY-MM-DD) [{current_deadline_str}]: ")
                
                if deadline_str == "":
                    deadline_str = current_deadline_str
                
                task = task_service.edit_task(task_id, title, desc, status, deadline_str)
                print(f"✅ Task {task_id} updated successfully.")
                
            elif choice == "8":
                proj_id = int(input("Enter project ID to delete: "))
                project_service.delete_project(proj_id)
                print(f"✅ Project {proj_id} and its tasks have been deleted.")
                
            elif choice == "9":
                task_id = int(input("Enter task ID to delete: "))
                task_service.delete_task(task_id)
                print(f"✅ Task {task_id} has been deleted.")

            elif choice == "0":
                print("Goodbye!")
                db.close() # Close the database session on exit
                break
            
            else:
                print("Invalid choice, please try again.")

        except TodolistError as e:
            print(f"Error: {e}")
        except ValueError:
            print("Error: Invalid input. Please enter a number where required.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")