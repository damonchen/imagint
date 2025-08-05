from flask import url_for, current_app as app


def get_file_url(file_id):
    app_web_url = app.config.get("APP_WEB_URL")
    # The route is registered as /files/<file_id> on the web blueprint
    # Since it's registered with add_url_rule, we need to construct the URL manually
    return f"{app_web_url}/v1/files/{file_id}"
