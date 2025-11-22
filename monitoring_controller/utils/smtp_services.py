from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()



SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT",587))
IMAP_SERVER = os.getenv("IMAP_SERVER")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")  
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


thread_id = "abc123-thread"


def send_email(subject: str, body: str, thread_id: str = None) -> bool:
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    if thread_id:
        msg['threadId'] = thread_id

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("Email sent successfully")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def send_request_email(subject: str, body: str):
    return send_email(subject, body, thread_id=thread_id)

def send_action_email(subject: str, body: str):
    return send_email(subject, body, thread_id=thread_id)
