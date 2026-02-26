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
        from_address: str = "noreply@yourapp.com"
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