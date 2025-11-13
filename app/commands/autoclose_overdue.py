import logging
from sqlalchemy.orm import Session
from app.repositories.task_repository import TaskRepository

# Set up a simple logger for this command
log = logging.getLogger(__name__)

def autoclose_overdue_tasks(db_session: Session):
    """
    Finds and closes all tasks that are past their deadline
    and are not already 'done'.
    """
    log.info("Running autoclose_overdue_tasks job...")
    task_repo = TaskRepository(db_session)
    
    try:
        overdue_tasks = task_repo.find_overdue_tasks()
        
        if not overdue_tasks:
            log.info("No overdue tasks found.")
            return

        log.info(f"Found {len(overdue_tasks)} overdue tasks to close.")
        
        for task in overdue_tasks:
            log.info(f"Closing task {task.id} ('{task.title}')")
            task_repo.update_status(task.id, "done")
            
        log.info("Autoclose job complete.")

    except Exception as e:
        log.error(f"Error during autoclose_overdue_tasks: {e}")
        db_session.rollback()
    finally:
        db_session.close()