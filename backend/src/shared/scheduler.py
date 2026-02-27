import logging
from apscheduler.schedulers.background import BackgroundScheduler
from features.checkins.services import create_daily_checkins_service, mark_missing_and_notify
from core.database.session import engine
from core.setting import Settings
from shared.email_service import send_email_to_missing_checkin
from sqlmodel import Session, select
from features.checkins.models import CheckIn
from features.users.models import User
from features.relationships.models import Relationship
from datetime import date

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def scheduled_create_daily_checkins():
    """Create daily check-ins for all seniors"""
    try:
        with Session(engine) as session:
            create_daily_checkins_service(session)
            logger.info("Daily check-ins created successfully")
    except Exception as e:
        logger.error(f"Error creating daily check-ins: {e}")


def scheduled_send_missing_checkin_reminders():
    """Send email reminders for seniors with missing today's check-in"""
    try:
        with Session(engine) as session:
            mark_missing_and_notify(session)
    except Exception as e:
        logger.error(f"Error in scheduled_send_missing_checkin_reminders: {e}")


def start_scheduler():
    """Start the background scheduler with multiple jobs"""
    # Create daily check-ins at midnight
    scheduler.add_job(
        scheduled_create_daily_checkins,
        trigger="cron",
        hour=0,
        minute=0,
        id="create_daily_checkins",
    )
    
    # Send reminder emails at 10 PM for missing check-ins
    scheduler.add_job(
        scheduled_send_missing_checkin_reminders,
        trigger="cron",
        hour=22,
        minute=0,
        # second="*/30",  # For testing, run every 30 seconds
        id="send_missing_checkin_reminders",
    )
    
    scheduler.start()
    logger.info("Scheduler started with check-in and email reminder jobs")