from apscheduler.schedulers.background import BackgroundScheduler
from features.checkins.services import create_daily_checkins_service
from core.database.session import engine
from sqlmodel import Session

scheduler = BackgroundScheduler()


def scheduled_create_daily_checkins():
    with Session(engine) as session:
        create_daily_checkins_service(session)


def start_scheduler():
    scheduler.add_job(
        scheduled_create_daily_checkins,
        trigger="cron",
        second=3,
    )
    scheduler.start()