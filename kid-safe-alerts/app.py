from flask import Flask, request, jsonify
from alerts import send_alert

app = Flask(__name__)

@app.route("/")
def home():
    return "Kid Safe Alerts Backend Running"

@app.route("/event", methods=["POST"])
def event():

    data = request.json

    device = data.get("device", "Unknown Device")
    event_type = data.get("event_type", "Unknown Event")
    source = data.get("source", "Unknown Source")
    timestamp = data.get("timestamp", "Unknown Time")

    print("EVENT RECEIVED:")
    print(data)
    print("SHORTCUT HIT SUCCESSFULLY")

    message = f"""
{event_type}

Device: {device}
Source: {source}
Time: {timestamp}
"""
    print(message)
    send_alert(message)

    return jsonify({
        "status": "success",
        "received": data
    })

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000, debug=True)
