from flask import Flask, request
from datetime import datetime
from twilio.rest import Client
from flask_cors import CORS
from dotenv import load_dotenv

from config.clients import CLIENTS

import os

load_dotenv()

# =========================
# FLASK SETUP
# =========================

app = Flask(__name__)

CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True
)

# =========================
# ENVIRONMENT VARIABLES
# =========================

API_KEY = os.getenv("API_KEY")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")

# Default Code 3 Leads number
# Used for generic/demo routes only.
TWILIO_NUMBER = "+14432229649"

twilio = Client(TWILIO_SID, TWILIO_AUTH)

# =========================
# SEND SMS
# =========================

def send_sms(from_number, to_number, message):

    try:

        print(f"[SMS] {from_number} ➜ {to_number}")

        msg = twilio.messages.create(

            body=message,

            from_=from_number,

            to=to_number

        )

        print(f"[SMS SUCCESS] SID: {msg.sid}")

        return True

    except Exception as e:

        print(f"[SMS ERROR] {e}")

        return False

# =========================
# SIMULATE MISSED CALL
# =========================

@app.route("/simulate-call", methods=["POST"])
def simulate_call():

    try:

        # -------------------------
        # API Authentication
        # -------------------------

        if request.headers.get("x-api-key") != API_KEY:

            return {
                "error": "Unauthorized"
            }, 403

        # -------------------------
        # Request Data
        # -------------------------

        data = request.get_json(silent=True) or request.form

        name = data.get("name", "John Smith")
        number = data.get("number", "+14432229649")
        service = data.get("service", "General Inquiry")

        # -------------------------
        # Normalize Phone Number
        # -------------------------

        if not number.startswith("+"):

            number = "+1" + number.replace("-", "").replace(" ", "")

        print(
            f"[SIMULATION] {name} | {number} | {service}"
        )

        # -------------------------
        # Customer SMS
        # -------------------------

        sms_sent = send_sms(

    TWILIO_NUMBER,

    number,

    f"Hey {name}, sorry we missed your call. "
    f"What can we help you with?"

)

        return {

            "status": "success",

            "sms_sent": sms_sent,

            "sent_to": number

        }, 200

    except Exception as e:

        print(f"[SIMULATION ERROR] {e}")

        return {

            "status": "error",

            "message": str(e)

        }, 500

# =========================
# WEBSITE LEAD FORM
# =========================

@app.route("/lead", methods=["POST"])
def website_lead():

    try:

        data = request.get_json()

        name = data.get("name", "Unknown")
        business = data.get("business", "")
        phone = data.get("phone", "Unknown")
        email = data.get("email", "Unknown")
        service = data.get("service", "Unknown")
        message = data.get("message", "")

        # -------------------------
        # Find Client
        # -------------------------

        client = CLIENTS.get(business)

        if not client:

            return {
                "status": "error",
                "message": f"Unknown business: {business}"
            }, 400

        # -------------------------
        # Normalize Customer Phone
        # -------------------------

        if phone != "Unknown" and not phone.startswith("+"):

            phone = "+1" + (
                phone.replace("-", "")
                     .replace(" ", "")
                     .replace("(", "")
                     .replace(")", "")
            )

        # -------------------------
        # Log Lead
        # -------------------------

        lead_message = f"""
Business:
{client["business_name"]}

Customer:
{name}

Phone:
{phone}

Email:
{email}

Service:
{service}

Message:
{message}
"""

        print(lead_message)

        # -------------------------
        # Notify Business Owner
        # -------------------------

        send_sms(

            client["twilio_number"],

            client["owner_phone"],

            f"""
🚨 NEW WEBSITE LEAD

Business:
{client["business_name"]}

Customer:
{name}

Phone:
{phone}

Email:
{email}

Service:
{service}

Message:
{message}
"""

        )

        # -------------------------
        # Customer Confirmation
        # -------------------------

        if phone != "Unknown":

            send_sms(

                client["twilio_number"],

                phone,

                client["customer_confirmation"]

            )

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
# HEALTH CHECK
# =========================

@app.route("/")
def home():

    return "Show Runner Backend LIVE", 200


# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )