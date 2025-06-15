from flask_mail import Message
from web_app.extensions import mail  # Import mail from extensions

def send_email(subject, recipients, body):
    """
    Sends an email using Flask-Mail.
    """
    msg = Message(subject, recipients=recipients, body=body)
    mail.send(msg)
