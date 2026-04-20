from flask import Flask
import requests
import time
from datetime import datetime

app = Flask(__name__)

API_TOKEN = "a84ffdv5iexeaf4op5seuzosman3nu"
USER_KEY = "u6eoij1woait8s6rkb2ccb3gdkuyiq"

def send_alert(message, title="Show Runner"):
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": API_TOKEN,
        "user": USER_KEY,
        "title": title,
        "message": message
    })

def run_demo():
    name = "John Smith"
    number = "410-555-1234"
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    send_alert(f"{name} | {number} | {time_now}", "📞 Missed Call")
    time.sleep(2)

    send_alert(f" Hey {name}, sorry we missed your call. What can we help you with?", "🤖 Auto Text Sent")
    time.sleep(3)

    send_alert("I need an estimate for roof repair", "📲 Customer Response")
    time.sleep(2)

    send_alert(f"Name: {name}\nNumber: {number}\nService: Roof Repair\n\n✅ Ready for follow-up", "💰 New Lead Captured")

@app.route("/run-demo")
def triggert():
    run_demo()
    return "Demo Ran"
