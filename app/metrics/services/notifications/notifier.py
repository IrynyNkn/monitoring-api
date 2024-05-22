import logging
import smtplib
from email.message import EmailMessage

from email_validator import validate_email, EmailNotValidError

from app.settings import SMTPSettings


class EmailNotifier:
    def __init__(self, smtp_settings: SMTPSettings) -> None:
        self._settings = smtp_settings
        self._logger = logging.getLogger(self.__class__.__name__)

    def send_email(self, subject: str, body: str, to: str) -> None:
        try:
            validate_email(to)

            msg = EmailMessage()
            msg.set_content(body)
            msg["Subject"] = subject
            msg["From"] = self._settings.username
            msg["To"] = to

            with smtplib.SMTP(self._settings.host, self._settings.port) as server:
                server.starttls()  # we need that for encryption
                server.login(self._settings.username, self._settings.password)

                server.send_message(msg)

            self._logger.info(f"Email was sent to {to}")
        except EmailNotValidError:
            self._logger.error(f"Invalid email address: {to}")
        except Exception as e:
            self._logger.error(f"Error sending email: {e}", exc_info=True)
