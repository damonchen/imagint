class Mail(object):
    def __init__(self):
        self._client = None
        self._default_send_from = None

    def is_inited(self):
        return self._client is not None

    def init_app(self, app):
        if "MAIL_TYPE" in app.config:
            mail_type = app.config["MAIL_TYPE"]

            if app.config.get("MAIL_DEFAULT_SEND_FROM"):
                self._default_send_from = app.config.get("MAIL_DEFAULT_SEND_FROM")

            if mail_type == "mailgun":
                import libs.mailgun as mailgun

                api_username = app.config.get("MAILGUN_API_USERNAME")
                if not api_username:
                    raise ValueError("MAILGUN_API_USERNAME is not set")

                api_password = app.config.get("MAILGUN_API_PASSWOROD")
                if not api_password:
                    raise ValueError("MAILGUN_API_PASSWOROD is not set")

                api_domain = app.config.get("MAIL_API_DOMAIN")
                if api_domain:
                    mailgun.api_domain = api_domain

                mailgun.api_username = api_username
                mailgun.api_passowrd = api_password
                self._client = mailgun.Emails()

            if mail_type == "resend":
                import resend

                api_key = app.config.get("RESEND_API_KEY")
                if not api_key:
                    raise ValueError("RESEND_API_KEY is not set")

                api_url = app.config.get("RESEND_API_URL")
                if api_url:
                    resend.api_url = api_url

                resend.api_key = api_key
                self._client = resend.Emails()
            elif mail_type == "smtp":
                import libs.smtp as smtp

                if not app.config.get("SMTP_SERVER") or not app.config.get("SMTP_PORT"):
                    raise ValueError(
                        "SMTP_SERVER and SMTP_PORT are required for smtp mail type"
                    )
                smtp.server = (app.config.get("SMTP_SERVER"),)
                smtp.port = (app.config.get("SMTP_PORT"),)
                smtp.username = (app.config.get("SMTP_USERNAME"),)
                smtp.password = (app.config.get("SMTP_PASSWORD"),)
                smtp._from = (app.config.get("MAIL_DEFAULT_SEND_FROM"),)
                smtp.use_tls = (app.config.get("SMTP_USE_TLS"),)

                self._client = smtp.SMTPClient()
            else:
                raise ValueError(
                    "Unsupported mail type {}".format(app.config.get("MAIL_TYPE"))
                )

    def send(self, to, subject, html, from_=None):
        if not self._client:
            raise ValueError("Mail client is not initialized")

        if not from_ and self._default_send_from:
            from_ = self._default_send_from

        if not from_:
            raise ValueError("mail from is not set")

        if not to:
            raise ValueError("mail to is not set")

        if not subject:
            raise ValueError("mail subject is not set")

        if not html:
            raise ValueError("mail html is not set")

        self._client.send({"from": from_, "to": to, "subject": subject, "html": html})


mail = Mail()


def init_app(app):
    mail.init_app(app)
