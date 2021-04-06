import os
from typing import List
from requests import Response, post

FAILED_LOAD_API_KEY = "Failed to load MailGun API key"
FAILED_LOAD_DOMAIN = "Failed to load MailGun domain"
ERROR_SENDING_EMAIL = 'Error in sending confirmation email, user registration failed'

# allows us to give our exceptions a custom name
# when we raise this exception, we'll get this message printed along with exception name
class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
    FROM_TITLE = "Music REST API"
    FROM_EMAIL = "postmaster@sandbox0aff3d4de056444392260ecbe134de56.mailgun.org"

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str):
        if cls.MAILGUN_API_KEY is None:
            raise MailGunException(FAILED_LOAD_API_KEY)
        if cls.MAILGUN_DOMAIN is None:
            raise MailGunException(FAILED_LOAD_DOMAIN)

        response = post (
            f'https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages',
            auth=('api', cls.MAILGUN_API_KEY),
            data={
                'from': f'{cls.FROM_TITLE} <{cls.FROM_EMAIL}>',
                'to': email,
                'subject': subject,
                'text': text,
                'html': html
            }
        )

        if response.status_code != 200:
            raise MailGunException(ERROR_SENDING_EMAIL)

        return response