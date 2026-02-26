"""Interface for Email Services"""
from abc import ABC, abstractmethod


class EmailService(ABC):
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> None:
        """Send a plain text email."""
        pass