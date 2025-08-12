class MailService(object):

    @staticmethod
    def send_register_token_mail(user, token):
        from flask import render_template
        from api.extensions.mail import mail

        user_id = user["id"]
        email = user["email"]

        html = render_template(
            "templates/mail/register.html",
            token=token,
            user_id=user_id,
            email=email,
        )
        mail.send(to=email, subject="User Registration", html=html)
