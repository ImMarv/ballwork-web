import smtplib
from email.message import EmailMessage
from typing import Optional

from i_email_service import EmailService


class SMTPEmailService(EmailService):
    """In charge of SMTP Conncetions and

    Args:
        EmailService (_type_): _description_
    """

    def __init__(
        self,
        host: str,
        port: int,
        username: Optional[str],
        password: Optional[str],
        use_tls: bool = True,
        from_address: str = "noreply@yourapp.com",
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.from_address = from_address

    def send_email(self, to: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message["From"] = self.from_address
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP(self.host, self.port) as server:
            if self.use_tls:
                server.starttls()

            if self.username and self.password:
                server.login(self.username, self.password)

            server.send_message(message)
            server.quit()


# region - Errors Handlers
class EmailError(Exception):
    """Base exception for email service errors"""

    pass


class SMTPConnectionError(EmailError):
    """Raised when unable to connect to SMTP server"""

    pass


class SMTPAuthenticationError(EmailError):
    """Raised when SMTP authentication fails"""

    pass


class InvalidEmailError(EmailError):
    """Raised when email address format is invalid"""

    pass


class EmailSendError(EmailError):
    """Raised when email fails to send"""

    def __init__(self, message: str, error_code: Optional[int] = None):
        super().__init__(message)
        self._error_code = error_code

    def error_code(self) -> Optional[int]:
        """Return the SMTP error code if available."""
        return self._error_code

    def error_message(self) -> str:
        """Return the error message."""
        return str(self)


# endregion
