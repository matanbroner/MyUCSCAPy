import smtplib, ssl
from email.mime.text        import MIMEText
from email.mime.multipart   import MIMEMultipart
from ..assets.utils         import remove_tags
from ..assets.providers     import providers
from .messages              import *

class Messenger:
    def __init__(self, config):
        self.config = config

    def __del__(self):
        self.server.quit()

    def login(self, user, password):
        self.user = user
        try:
            self._generate_server()
            self.server.login(user, password)
        except Exception as e:
            raise self._error("SMTP Server Login Failed")  
    
    def send_text_message(self, html):
        message = MIMEMultipart("alternative")
        message["Subject"] = "MyUCSC Api Update"
        message["From"] = self.user
        message["To"] = self._email()

        plain_text_message = MIMEText(remove_tags(html), "plain")
        html_message = MIMEText(html, "html")

        message.attach(plain_text_message)
        message.attach(html_message)

        try:
            self.server.sendmail(self.user, self._email(), message.as_string())
        except Exception as e:
            raise self._error("Error Sending Text Message")

    def test(self):
        self.send_text_message(test_message())

    def inform_course_open(self, course, course_url, occupied_spots, total_spots):
        self.send_text_message(course_open_message(course["name"], course_url, occupied_spots, total_spots))

    def _email(self):
        return "{}@{}".format(self.config["phone"], providers[self.config["provider"]])

    def _generate_server(self):
        smtp_server = "smtp.gmail.com"
        port = 587
        context = ssl.create_default_context()
        self.server = smtplib.SMTP(smtp_server,port)
        self.server.starttls(context=context)

    def _error(self, message):
        return Exception("Messenger: {}".format(message))