import requests

api_domain = ""
api_username = ""
api_passowrd = ""


class Emails(object):

    def __init__(self) -> None:
        pass

    def send(self, data):
        # {"from": from_, "to": to, "subject": subject, "html": html}
        headers = {"Content-Type": "multipart/form-data"}
        api_url = "https://api.mailgun.net/v3/" + api_domain + "/messages"
        response = requests.post(
            api_url, data, headers=headers, auth=(api_username, api_passowrd)
        )

        return response.json()
