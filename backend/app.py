from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# M-Pesa API Credentials
CONSUMER_KEY = "bt4dhsArAssYi7Tle3W6BDihJALHpwHFYC6tG5DTs10KBjAe"
CONSUMER_SECRET = "V0fIazyGEuruSulWYNg6iMdPh6pFUoEfvakTCTjxkklpAx8kfdppGVRAgyDGxH9g"
BASE_URL = "https://sandbox.safaricom.co.ke"  # Use production URL for live

def get_access_token():
    """Get OAuth token from M-Pesa."""
    url = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    return response.json().get("access_token")

@app.route('/send-money', methods=['POST'])
def send_money():
    """Handle sending money via M-Pesa."""
    data = request.json
    access_token = get_access_token()
    url = f"{BASE_URL}/mpesa/c2b/v1/simulate"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "ShortCode": "600982",  # Replace with your shortcode
        "CommandID": "CustomerPayBillOnline",
        "Amount": data.get("1"),
        "Msisdn": data.get("0701928129"),  # Customer phone number in 254 format
        "BillRefNumber": data.get("TEST")  # Optional: e.g., invoice number
    }
    response = requests.post(url, json=payload, headers=headers)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
