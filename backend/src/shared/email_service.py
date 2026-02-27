import logging
import smtplib
from email.message import EmailMessage

from core.setting import Settings
from sqlmodel import SQLModel


class Email(SQLModel, table=False):
    From: str
    To: str
    Subject: str
    Body: str


def send_email(email_obj: Email):
    """Send a generic email message using smtplib (synchronous)."""
    logging.info(f"Sending email to {email_obj.To} with subject '{email_obj.Subject}'")
    msg = EmailMessage()
    msg["From"] = email_obj.From
    msg["To"] = email_obj.To
    msg["Subject"] = email_obj.Subject

    msg.set_content(email_obj.Body)

    try:
        with smtplib.SMTP(Settings.SMTP_HOST, Settings.SMTP_PORT) as server:
            server.send_message(msg)
        logging.info(f"Email sent successfully to {email_obj.To}")
    except Exception as e:
        logging.error(f"Failed to send email to {email_obj.To}: {e}")
        raise


def send_email_to_missing_checkin(to_email: str):
    """Convenience wrapper for a missing check-in notification."""
    email = Email(
        From=Settings.NO_REPLY_EMAIL,
        To=to_email,
        Subject="Check-in Missing",
        Body="You did not complete today's check-in.",
    )
    send_email(email)
