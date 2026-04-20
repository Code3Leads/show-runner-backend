import time
import requests
from datetime import datetime

seen = set()

# 🔔 Pushover Alert
def send_alert(message):
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": "a84ffdv5iexeaf4op5seuzosman3nu",
        "user": "u6eoij1woait8s6rkb2ccb3gdkuyiq",
        "message": message
    })
    print("Sent:", message)

# 📞 simulate missed calls 
def get_missed_calls():
    return [
        {
            "name": "John Doe",
            "number": "+1234567890",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "name": "Jane Smith",
            "number": "+0987654321",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]

while True:
    calls = get_missed_calls()

    for call in calls:
        key = call["number"] + call["time"]

        if key not in seen:
            seen.add(key)
            message = f"📞 MISSED CALL\n{call['name']} | {call['number']} | {call['time']}"
            send_alert(message)

    time.sleep(30)  # check every 30 seconds
