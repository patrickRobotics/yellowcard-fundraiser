from flask import Flask, request, render_template, redirect, url_for, flash
import requests
import json
import uuid

from yellowcard_apis import apis
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a strong secret key for session management

YELLOWCARD_API_BASE_URL = "https://sandbox.api.yellowcard.io"
YELLOWCARD_API_KEY = "your_api_key"  # Replace with your YellowCard API key


@app.route('/')
def index():
    with open('funds.json', 'r') as f:
        funds = json.load(f)
    return render_template('index.html', funds=funds)


@app.route('/create_fund', methods=['GET', 'POST'])
def create_fund():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        goal_amount = float(request.form['goal_amount'])
        recipient_address = request.form['recipient_address']

        # Create fund logic
        fund = {
            'title': title,
            'description': description,
            'goal_amount': goal_amount,
            'recipient_address': recipient_address,
            'raised_amount': 0.0,
            'donations': []
        }

        # Save fund to a simple in-memory storage (for demonstration purposes)
        with open('funds.json', 'r') as f:
            funds = json.load(f)
        funds.append(fund)
        with open('funds.json', 'w') as f:
            json.dump(funds, f)

        flash('Fundraising campaign created successfully!')
        return redirect(url_for('index'))

    return render_template('create_fund.html')


@app.route('/donate/<int:fund_id>', methods=['GET', 'POST'])
def donate(fund_id):
    channels = apis.get_yellow_card_channels("GET", "/business/channels", country="KE")
    rates = apis.get_yellowcard_rates("GET", "/business/rates", "KE")
    if request.method == 'POST':
        print(request.form)

        name = request.form['name']
        #network_id is hardcoded to a specific value that was fetched for kenyan-based momos
        payload = {
            "recipient": {
                "name": "Sample Name",
                "country": "US",
                "phone": "+12222222222",
                "address": "Sample Address",
                "dob": "mm/dd/yyyy",
                "email": "email@domain.com",
                "idNumber": "0123456789",
                "idType": "license"
            },
            "source": {
                "accountNumber": "1111111111",
                "accountType": "momo",
                "networkId": "7ea6df5c-6bba-46b2-a7e6-f511959e7edb",
            },
            "forceAccept": False,
            "customerType": "retail",
            "channelId": request.form['channel_id'],
            "sequenceId": str(uuid.uuid4()),
            "amount": float(request.form['amount'])
        }
        res = apis.post_collection_request("POST", "/business/collections", payload)

        with open('funds.json', 'r') as f:
            funds = json.load(f)
        fund = funds[fund_id]
        fund['raised_amount'] += float(request.form['amount'])
        fund['donations'].append({'name': name, 'amount': float(request.form['amount'])})

        with open('funds.json', 'w') as f:
            json.dump(funds, f)

        flash('Donation successful!')
        return redirect(url_for('index'))

    return render_template(
        'donate.html',
        fund_id=fund_id,
        channels=channels,
        rates=rates
    )


@app.route('/funds')
def funds():
    with open('funds.json', 'r') as f:
        funds = json.load(f)
    return render_template('funds.html', funds=funds)


@app.route('/send_funds/<int:fund_id>', methods=['POST'])
def send_funds(fund_id):
    with open('funds.json', 'r') as f:
        funds = json.load(f)
    fund = funds[fund_id]

    if fund['raised_amount'] >= fund['goal_amount']:
        recipient_address = fund['recipient_address']
        amount = fund['raised_amount']

        # Call YellowCard API to send funds
        response = requests.post(f"{YELLOWCARD_API_BASE_URL}/path_to_send_endpoint", json={
            "recipient_address": recipient_address,
            "amount": amount,
            "api_key": YELLOWCARD_API_KEY
        })

        if response.status_code == 200:
            fund['raised_amount'] = 0
            with open('funds.json', 'w') as f:
                json.dump(funds, f)
            flash('Funds sent successfully!')
        else:
            flash('Error sending funds!')

    return redirect(url_for('index'))


if __name__ == '__main__':
    with open('funds.json', 'w') as f:
        json.dump([], f)  # Initialize an empty list of funds
    app.run(debug=True)
