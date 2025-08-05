class MailService(object):

    @staticmethod
    def send_register_token_mail(account, token):
        from flask import render_template
        from api.extensions.mail import mail

        account_id = account["id"]
        email = account["email"]

        html = render_template(
            "templates/mail/register.html",
            token=token,
            account_id=account_id,
            email=email,
        )
        mail.send(to=email, subject="Account Registration", html=html)
