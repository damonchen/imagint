import click
import json
from flask import current_app
from flask.cli import with_appcontext

from .data.models.user import User
from .extensions.database import db
from .libs.helper import validate_email
from .services.user_service import UserService
from .services.task_service import TaskWorkerService


@click.command("reset-password", help="Reset the user password.")
@click.option("--email", prompt=True, help="The email address of the user to reset.")
@click.option("--new-password", prompt=True, help="The new password.")
@click.option("--password-confirm", prompt=True, help="The new password confirm.")
def reset_password(email, new_password, password_confirm):
    new_password = str(new_password).strip()
    password_confirm = str(password_confirm).strip()
    if new_password != password_confirm:
        click.echo(
            click.style("Two passwords do not match, please retry it.", fg="red")
        )
        return

    try:
        UserService.send_reset_password_email(email, new_password)
    except ValueError:
        click.echo(
            click.style(
                f"Password should be larger than 8 characters and contain at least one uppper case letter, one digital",
                fg="red",
            )
        )
        return

    db.session.commit()
    click.echo(click.style("Congratulations! Password has been changed", fg="green"))


@click.command("reset-email", help="Reset the user email.")
@click.option("--email", prompt=True, help="The email address of the user to reset.")
@click.option("--new-email", prompt=True, help="The new email.")
@click.option("--email-confirm", prompt=True, help="The new email confirm.")
def reset_email(email, new_email, email_confirm):
    new_email = new_email.strip()
    email_confirm = email_confirm.strip()

    if new_email == email_confirm:
        click.echo(click.style("Two emails do not match, please retry it", fg="red"))
        return

    user = db.session.query(User).filter_by(email=email).first()
    if user is None:
        click.echo(click.style(f"The user '{user}' is not exist.", fg="red"))
        return

    try:
        validate_email(new_email)
    except ValueError:
        click.echo(click.style(f"The new email '{new_email}' is not valid", fg="red"))
        return

    user.email = new_email
    db.session.commit()

    click.echo(click.style("Congratulations! Email has been changed", fg="green"))


@click.command("reset-encrypt-key-pair", help="Reset encrypt key pair")
def reset_encrypt_key_pair():
    pass


@click.command("init-database", help="Init the database")
def init_database():
    pass


@click.command("init-data")
@with_appcontext
def init_db():
    from .extensions.database import db
    from .data.models.model import AppSetup
    from .services.user_service import UserService

    version = current_app.config.get("CURRENT_VERSION")
    setup = AppSetup(version=version)
    db.session.add(setup)

    user = UserService.register(
        email="netubu@gmail.com", username="damon", password="Damon#2"
    )
    user = UserService.active_user(user)
    print("user", user)

    TaskWorkerService.create_task_worker("1234567890")

    db.session.commit()


@click.command("reset-db")
@with_appcontext
def reset_db():
    from .extensions.database import db

    db.drop_all()
    db.create_all()


def register_command(app):
    app.cli.add_command(reset_password)
    app.cli.add_command(reset_email)
    app.cli.add_command(init_db)
    app.cli.add_command(reset_db)
