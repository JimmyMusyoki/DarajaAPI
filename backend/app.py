from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# M-Pesa API Credentials
CONSUMER_KEY = "bt4dhsArAssYi7Tle3W6BDihJALHpwHFYC6tG5DTs10KBjAe"
CONSUMER_SECRET = "V0fIazyGEuruSulWYNg6iMdPh6pFUoEfvakTCTjxkklpAx8kfdppGVRAgyDGxH9g"
BASE_URL = "https://sandbox.safaricom.co.ke"  # Use production URL for live

def get_access_token():
    """Get OAuth token from M-Pesa."""
    url = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    try:
        response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to get access token", "details": str(e)}), 500

@app.route('/send-money', methods=['POST'])
def send_money():
    """Handle sending money via M-Pesa."""
    data = request.json

    # Validate input data
    amount = data.get("amount")
    msisdn = data.get("msisdn")
    bill_ref_number = data.get("bill_ref_number", "TestAPI")

    if not amount or not msisdn:
        return jsonify({"error": "Missing required fields: 'amount' or 'msisdn'"}), 400

    # Get access token
    access_token = get_access_token()
    if isinstance(access_token, tuple):  # If `get_access_token` returned an error response
        return access_token

    # Define endpoint and headers
    url = f"{BASE_URL}/mpesa/c2b/v1/simulate"
    headers = {"Authorization": f"Bearer {access_token}"}

    # Prepare payload
    payload = {
        "ShortCode": "600982",  # Replace with your shortcode
        "CommandID": "CustomerPayBillOnline",
        "Amount": amount,
        "Msisdn": msisdn,  # Customer phone number in 254 format
        "BillRefNumber": bill_ref_number  # Optional: e.g., invoice number
    }

    try:
        # Make the API call
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to process payment", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
