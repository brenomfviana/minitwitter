import logging

from minitwitter import celery_app

logger = logging.getLogger(__name__)


class EmailService:
    @celery_app.task(name="notification.email")
    def send(
        self,
        email: str,
        subject: str,
        content: str,
    ):
        logger.info(
            f"Email {subject} sent to {email}\nEmail content:\n  {content}"
        )
