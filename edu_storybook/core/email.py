"""
email.py
    Initialization and interface for email functions.
"""

from .config import config
from . import sensitive as sensitive

import smtplib

import logging

def send_email(user_name: str, user_email: str, admin_name: str, admin_email: str, subject: str, body: str) -> bool:
    """
    Creates and sends an email to a user
    :param user_name: The name of the user
    :param to_email: The email of the user
    :param admin_name: Admin of user's study
    :param admin_email: Admin's email
    :param subject: Subject of the email
    :param body: Body of the email; where actual text is placed
    :return: Boolean on whether or not the email was sent.
    """
    if config['production'] == False:
        return True

    # Write Email
    to_line = "To: " + user_name + " <" + user_email + ">\n"
    from_line = "From: EDU Storybooks <edustorybooks@gmail.com>\n"
    reply_to_line = "Reply-To: " + admin_name + " <" + admin_email + ">\n"
    subject_line = "Subject: " + subject + "\n\n"
    body_lines = body
    email_text = to_line + from_line + reply_to_line + subject_line + body_lines

    # Email Command
    try:
        server = smtplib.SMTP(sensitive.smtp, sensitive.port)
        server.starttls(context=sensitive.context)
        server.login('edustorybooks@gmail.com', sensitive.email_password)
        server.sendmail("edustorybooks@gmail.com", user_email, email_text)
    except Exception as e:
        logging.error('Exception in Email Process')
        logging.error(e)
        return False
    finally:
        del to_line
        del from_line
        del reply_to_line
        del subject_line
        del body_lines
        del email_text
