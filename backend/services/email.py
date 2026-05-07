import os
from email.message import EmailMessage
import aiosmtplib


SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_SENDER = os.getenv("SMTP_SENDER", SMTP_USER)


def _ensure_configured() -> None:
    """Validate SMTP configuration is present."""
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASSWORD:
        raise RuntimeError("SMTP not configured")


async def send_email(to_email: str, subject: str, body: str) -> None:
    """Send an email using configured SMTP settings."""
    _ensure_configured()
    message = EmailMessage()
    message["From"] = SMTP_SENDER
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USER,
        password=SMTP_PASSWORD,
        start_tls=True,
    )
