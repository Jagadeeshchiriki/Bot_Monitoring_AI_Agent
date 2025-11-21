import os
import hmac
import hashlib
import time
from urllib.parse import urlencode, urljoin
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# CONFIG - set these in environment for production
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER", "your-email@gmail.com")
SMTP_PASS = os.getenv("SMTP_PASS", "your-app-password")
LINK_BASE = os.getenv("APPROVAL_BACKEND_BASE", "https://your-backend.com/approve")
HMAC_SECRET = os.getenv("HMAC_SECRET", "replace-with-secure-secret")
LINK_EXPIRY_SECONDS = int(os.getenv("LINK_EXPIRY_SECONDS", 60 * 60 * 24))  # 24h default

def _make_signature(event_id: str, status: str, expires_at: int, secret: str) -> str:
    """
    Create an HMAC-SHA256 signature over event_id|status|expires_at
    """
    msg = f"{event_id}|{status}|{expires_at}".encode("utf-8")
    return hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()

def generate_approval_link(base_url: str, event_id: str, status: str, secret: str,
                           expiry_seconds: int = LINK_EXPIRY_SECONDS) -> str:
    """
    Generate a signed approval/rejection link that points to the user's backend.
    Query params: eventId, status, expires, sig
    Example result:
      https://your-backend.com/approve?eventId=EVT-1&status=approved&expires=1700000000&sig=...
    """
    expires_at = int(time.time()) + expiry_seconds
    sig = _make_signature(event_id, status, expires_at, secret)
    query = urlencode({"eventId": event_id, "status": status, "expires": expires_at, "sig": sig})
    return f"{base_url}?{query}"

def send_approval_mail(to_email: str, developer_name: str, event_id: str, event_details: str,
                       link_base: str = LINK_BASE, smtp_user: str = SMTP_USER, smtp_pass: str = SMTP_PASS,
                       smtp_host: str = SMTP_HOST, smtp_port: int = SMTP_PORT, hmac_secret: str = HMAC_SECRET):
    """
    Send an HTML approval email with signed Approve/Reject links.
    """
    approve_link = generate_approval_link(link_base, event_id, "approved", hmac_secret)
    reject_link = generate_approval_link(link_base, event_id, "rejected", hmac_secret)

    subject = f"Approval Required — Event {event_id}"

    html_content = f"""
    <html>
    <body style="font-family:Arial, sans-serif; padding:20px;">
        <h3>Hi {developer_name},</h3>
        <p>The following event requires your decision:</p>

        <h4>Event ID: {event_id}</h4>
        <pre style="background:#f4f4f4; padding:12px; border-radius:6px; white-space:pre-wrap;">
{event_details}
        </pre>

        <p style="margin-top:16px;">Please choose:</p>

        <a href="{approve_link}" style="display:inline-block;padding:10px 18px;margin-right:10px;
           text-decoration:none;border-radius:6px;background:#28a745;color:#ffffff;">Approve</a>

        <a href="{reject_link}" style="display:inline-block;padding:10px 18px;
           text-decoration:none;border-radius:6px;background:#dc3545;color:#ffffff;">Reject</a>

        <p style="margin-top:24px;font-size:12px;color:#666;">
            Links expire in {LINK_EXPIRY_SECONDS // 3600} hour(s). If you didn't expect this email, ignore it.
        </p>

        <p>Regards,<br/>Automation System</p>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, to_email, msg.as_string())
        print(f"Approval email sent to {to_email} (event {event_id})")
    except Exception as e:
        print("Failed to send approval email:", e)
        raise

# -----------------------
# Example usage
# -----------------------
if __name__ == "__main__":
    send_approval_mail(
        to_email="developer@example.com",
        developer_name="Suresh",
        event_id="EVT-98765",
        event_details="Process: FileUpload\nError: NullReferenceException\nState: Failed"
    )
