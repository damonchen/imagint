import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


server = ""
port = 0
_from = ""
username = ""
password = ""
use_tls = False


class SMTPClient:
    def __init__(
        self,
    ):
        pass

    def send(self, mail: dict):
        smtp = smtplib.SMTP(server, port)
        if use_tls:
            smtp.starttls()
        if username and password:
            smtp.login(username, password)
        msg = MIMEMultipart()
        msg["Subject"] = mail["subject"]
        msg["From"] = _from
        msg["To"] = mail["to"]
        msg.attach(MIMEText(mail["html"], "html"))
        smtp.sendmail(username, mail["to"], msg.as_string())
        smtp.quit()
