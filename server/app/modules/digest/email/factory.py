# app/modules/email/factory.py

from ....core.settings import settings
from .email_service import SMTPEmailService


def build_email_service() -> SMTPEmailService:
    return SMTPEmailService(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_USER,
        password=settings.EMAIL_PASSWORD,
        from_address=settings.EMAIL_FROM,
        use_tls=settings.EMAIL_USE_TLS,
    )
