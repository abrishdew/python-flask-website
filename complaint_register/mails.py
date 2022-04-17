from flask import request
from flask_mail import Message
import secrets 

import os
from dotenv import load_dotenv
load_dotenv()

from complaint_register import mail

class VerificationEmailError(Exception):
    pass

def generate_verification_token():
    token = secrets.token_urlsafe(32)
    return token

def send_verification_email(user):
    verification_url = f"{request.host_url}verify_email/{user.verification_token}"

    subject = "Email Verification"
    sender = os.environ.get('MAIL_DEFAULT_SENDER')
    recipient = user.email
    body = f"Hello {user.username},\n\nPlease click the link below to verify your email address:\n{verification_url}\n\nIf you did not request this verification, please ignore this email.\n\nBest regards,\nThe YourApp Team"

    msg = Message(subject=subject, sender=sender, recipients=[recipient])
    msg.body = body

    mail.send(msg)