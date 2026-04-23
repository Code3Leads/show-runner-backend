from flask import Flask, request 
import requests
import time
from datetime import datetime
from twilio.rest import Client
import os 

app = Flask(__name__)

API_TOKEN = os.environ.get("API_TOKEN")
USER_KEY = os.environ.get("USER_KEY")
account_sid = os.environ.get("TWILIO_SID")
auth_token = os.environ.get("TWILIO_AUTH")
TWILIO_NUMBER = "+14439125624"

client = Client(account_sid, auth_token)

# =========================
# 🔔 PUSHOVER ALERTS
# =========================
def send_alert(message, title="Show Runner"):
    try:
        print(f"[ALERT] {title} - {message}")

        requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": API_TOKEN,
                "user": USER_KEY,
                "title": title,
                "message": message
            },
            timeout=5
        )
    except Exception as e:
        print(f"[ERROR] Pushover failed: {e}")

# =========================
# 📲 TWILIO SMS
# =========================
def send_sms(to, message):
    try:
        print(f"[SMS] Sending to {to}: {message}")

        msg = client.messages.create(
            body=message,
            from_=TWILIO_NUMBER,
            to=to
        )

        print(f"[SMS SUCCESS] SID: {msg.sid}")
        return True

    except Exception as e:
        print(f"[SMS ERROR] {e}")
        return False

# =========================
# 🧪 DEMO FLOW
# =========================
def run_demo():
    name = "John Smith"
    number = "+14105551234"
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    send_alert(f"{name} | {number} | {time_now}", "📞 Missed Call")

    send_alert(
        f"Hey {name}, sorry we missed your call. What can we help you with?",
        "🤖 Auto Text Sent"
    )

    send_alert("I need an estimate for roof repair", "📲 Customer Response")

    send_alert(
        f"Name: {name}\nNumber: {number}\nService: Roof Repair\n\n✅ Ready for follow-up",
        "💰 New Lead Captured"
    )

# =========================
# 🚀 MAIN ENDPOINT
# =========================
@app.route("/simulate-call", methods=["POST"])
def simulate_call():
    try:
        # Support JSON + form data
        data = request.get_json(silent=True) or request.form

        name = data.get("name", "John Smith")
        number = data.get("number", "+14105551234")
        service = data.get("service", "General Inquiry")

        # Normalize phone number
        if not number.startswith("+"):
            number = "+1" + number.replace("-", "").replace(" ", "")

        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[REQUEST] Name={name}, Number={number}, Service={service}, Time={time_now}")

        # 📞 Missed call alert
        send_alert(f"{name} | {number} | {time_now}", "📞 Missed Call")

        # 📲 Send SMS
        sms_sent = send_sms(
            number,
            f"Hey {name}, sorry we missed your call. What can we help you with?"
        )

        # 📲 Simulated response
        send_alert(service, "📲 Customer Response")

        # 💰 Lead captured
        send_alert(
            f"Name: {name}\nNumber: {number}\nService: {service}\n\n✅ Ready for follow-up",
            "💰 New Lead Captured"
        )

        return {
            "status": "success",
            "sms_sent": sms_sent,
            "sent_to": number
        }, 200

    except Exception as e:
        print(f"[CRITICAL ERROR] {e}")

        return {
            "status": "error",
            "message": str(e)
        }, 500

# =========================
# 🧪 DEMO ROUTE
# =========================
@app.route("/run-demo")
def trigger_demo():
    run_demo()
    return "Demo Ran", 200

# =========================
# 🏠 HEALTH CHECK
# =========================
@app.route("/")
def home():
    return "Show Runner Backend LIVE", 200