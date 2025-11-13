import time
import schedule
import logging
from app.db.session import SessionLocal
from app.commands.autoclose_overdue import autoclose_overdue_tasks

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_job():
    """Helper function to create a new session for each job run."""
    db_session = SessionLocal()
    autoclose_overdue_tasks(db_session)

def run_scheduler():
    """Runs the main scheduler loop."""
    logging.info("Starting scheduler...")
    
    # Run the job every 15 minutes, as an example
    schedule.every(15).minutes.do(run_job)
    
    # You could also use other schedules:
    # schedule.every().day.at("02:00").do(run_job)
    
    logging.info("Scheduler started. Waiting for jobs...")
    
    while True:
        schedule.run_pending()
        time.sleep(1)