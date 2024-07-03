import os
import tempfile
import json

from flask import Flask, request, render_template
import requests
from requests import utils

DEBUG=True

app = Flask(__name__)

# Payment Form
@app.route("/")
def payment_form():
    return render_template('index.html', text="")


# Payment success page
@app.route('/payment-success')
def success_page():
    return render_template('payment-success.html')


# Payment failure page
@app.route('/payment-failure')
def failure_page():
    return render_template('payment-failure.html')


# Apple Pay Validation
@app.route('/applepay_validation', methods=['GET'])
def applepay_payment_session():
    data = {
        "merchantIdentifier": "merchant.com.vgs.victor.sample.app",
        "initiativeContext": "opulent-doodle-qrrvp6qwgvwfqx9-5000.app.github.dev",
        "initiative": "web",
        "displayName": "Victor Apple Pay App"
    }
    cert_file = '/workspaces/vgs_stripe_sample/apple-pay-certs/certificate_sandbox.pem'
    key_file = '/workspaces/vgs_stripe_sample/apple-pay-certs/certificate_sandbox.key'
    url = 'https://apple-pay-gateway-cert.apple.com/paymentservices/paymentSession'
    response = requests.post(url, json=data, cert=(cert_file, key_file))

    print(f"Response Status Code: {response.status_code}")
    parsed_json = json.loads(response.text)
    formatted_json = json.dumps(parsed_json, indent=4)
    print(formatted_json)
    return response.json()


# Recieve data from VGS reverse proxy inbound route 
@app.route('/post', methods=['POST'])
def handle_request():
    if request.method == 'POST':
        formatted_json = json.dumps(request.get_json(), indent=4)
        print(formatted_json)
        return request.get_json()
    else:
        return 'Unsupported HTTP method'


if __name__ == '__main__':
    app.run(debug=DEBUG)



#-------------
#Setting up a directory for Apple Pay domain verification
#import http.server
#import socketserver
#PORT = 5000
#web_dir = os.path.join(os.path.dirname(__file__), 'apple-pay-verification')
#os.chdir(web_dir)
#Handler = http.server.SimpleHTTPRequestHandler
#with socketserver.TCPServer(("", PORT), Handler) as httpd:
#    print(f"Serving at port {PORT}")
#    httpd.serve_forever()
#-------------
