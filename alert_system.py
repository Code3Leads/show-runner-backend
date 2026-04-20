import time
import requests 

seen = set()

import requests

def send_alert(message):
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": "a84ffdv5iexeaf4op5seuzosman3nu",
         "user": "u6eoij1woait8s6rkb2ccb3gdkuyiq",
          "message": message
    })
    print("Sent:", message)

def get_calls():
    # simulated calls (we'll replace this later)
    return [
        {"type": "EMS Call", "Location": "123 Main St", "Time": "2024-06-01 12:00:00"},
        {"type": "Structure Fire", "Location": "456 Elm St", "Time": "2024-06-01 12:05:00"},
        {"type": "Alarm Activation", "Location": "789 Oak St", "Time": "2024-06-01 12:10:00"},
    ]

while True:
    calls = get_calls()
    for call in calls:
        if call["type"] == "Structure Fire":
            key = call["type"] + call["Location"] + call["Time"]

            if key not in seen:
                seen.add(key)
                message = f"ALERT: {call['type']} at {call['Location']} on {call['Time']}"
                send_alert(message)
    time.sleep(30)  # check every minute