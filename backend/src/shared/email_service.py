import logging

import aiosmtplib
from email.message import EmailMessage

from core.setting import Settings
from sqlmodel import SQLModel


class Email(SQLModel, table=False):
    From : str 
    To : str
    Subject : str
    Body : str
     
async def send_email(Email):
    logging.info(f"Sending email to {Email.To} with subject '{Email.Subject}'")
    msg = EmailMessage()
    msg["From"] = Email.From
    msg["To"] = Email.To
    msg["Subject"] = Email.Subject

    msg.set_content(Email.Body)

    await aiosmtplib.send(
        msg,
        hostname="localhost",
        port=Settings.SMTP_PORT,
        start_tls=False
    )
    


async def send_email_to_missing_checkin(to_email):
    email = Email(From=Settings.NO_REPLY_EMAIL, To=to_email, Subject="Check-in Missing", Body="You did not complete today's check-in.")
    send_email(email)
