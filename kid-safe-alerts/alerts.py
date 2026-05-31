import requests

PUSHOVER_USER_KEY = "u6eoij1woait8s6rkb2ccb3gdkuyiq"
PUSHOVER_APP_TOKEN = "ad239ofs3bijan9u3mo9wn3nks3b8v"


def send_alert(message):

    try:

        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": PUSHOVER_APP_TOKEN,
                "user": PUSHOVER_USER_KEY,
                "message": message,
                "title": "Kid Safe Alert"
            }
        )

        print("PUSHOVER RESPONSE:")
        print(response.text)

    except Exception as e:

        print("PUSHOVER ERROR:")
        print(e)