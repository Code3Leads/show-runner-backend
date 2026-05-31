from flask import Flask, request 
import requests
import time
from datetime import datetime
from twilio.rest import Client
import os 
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

PUSHOVER_APP_TOKEN = os.getenv("PUSHOVER_APP_TOKEN")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
API_KEY = os.getenv("API_KEY")
account_sid = os.environ.get("TWILIO_SID")
auth_token = os.environ.get("TWILIO_AUTH")
TWILIO_NUMBER = "+14432229649"

client = Client(account_sid, auth_token)

# =========================
# 🔔 PUSHOVER ALERTS
# =========================
def send_alert(message, title="Show Runner"):
    try:
        print(f"[ALERT] {title} - {message}")

        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": PUSHOVER_APP_TOKEN,
                "user": PUSHOVER_USER_KEY,
                "title": title,
                "message": message
            },
            timeout=5
        )

        print("PUSHOVER STATUS:", response.status_code)
        print("PUSHOVER RESPONSE:", response.text)

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
        print(f"[DEBUG] Incoming API KEY: {request.headers.get('x-api-key')}")
        print(f"[DEBUG] Expected API KEY: {API_KEY}")

        if request.headers.get("x-api-key") != API_KEY:
            return {"error": "Unauthorized"}, 403
        
        # Support JSON + form data
        data = request.get_json(silent=True) or request.form

        name = data.get("name", "John Smith")
        number = data.get("number", "+14432229649")
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
# 📋 WEBSITE LEAD FORM
# =========================
@app.route("/lead", methods=["POST"])
def website_lead():

    try:

        data = request.get_json()

        name = data.get("name", "Unknown")
        business = data.get("business", "Unknown")
        phone = data.get("phone", "Unknown")
        service = data.get("service", "Unknown")
        message = data.get("message", "")

        lead_message = f"""
🚨 NEW WEBSITE LEAD

Name: {name}
Business: {business}
Phone: {phone}

Interested In:
{service}

Message:
{message}
"""

        send_alert(lead_message, "💰 New Website Lead")

        print(lead_message)

        return {
            "status": "success"
        }, 200

    except Exception as e:

        print(f"[LEAD ERROR] {e}")

        return {
            "status": "error",
            "message": str(e)
        }, 500

# =========================
# 🏠 HEALTH CHECK
# =========================
@app.route("/")
def home():
    return "Show Runner Backend LIVE", 200

# =========================
# ▶ START SERVER
# =========================
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )