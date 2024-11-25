from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
from datetime import datetime
import config
import json
import os
import helpers
from dotenv import load_dotenv
from flask_talisman import Talisman
from flask_mail import Mail, Message
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
log_format = '[%(asctime)s] %(levelname)s [line %(lineno)d in %(module)s]: %(message)s'
log_datefmt='%Y-%m-%d %H:%M:%S'
logging.basicConfig(
    format=log_format,
    datefmt=log_datefmt
)
log_level = os.getenv('LOG_LEVEL', 'WARNING').upper()
logging.getLogger().setLevel(getattr(logging, log_level, logging.INFO))

app = Flask(__name__)

# Load configuration from config.Config
app.config.from_object(config.Config)

mail = Mail(app)

# Configuring Talisman with HSTS enabled
# https://pypi.org/project/flask-talisman/
csp = {
    'default-src': ["'self'"],
    'script-src': ["'self'", "https://stackpath.bootstrapcdn.com", "https://www.youtube.com", 
                   "https://cdnjs.cloudflare.com", "https://cdn.jsdelivr.net", 
                   "https://www.googletagmanager.com", "https://googleads.g.doubleclick.net",
                   "https://www.googleadservices.com"],
    'style-src': ["'self'", "'unsafe-inline'", "https://stackpath.bootstrapcdn.com", 
                  "https://cdnjs.cloudflare.com", "https://netdna.bootstrapcdn.com", 
                  "https://fonts.googleapis.com", "https://cdn.jsdelivr.net"],
    'font-src': ["'self'", "https://stackpath.bootstrapcdn.com", "https://netdna.bootstrapcdn.com", 
                 "https://fonts.gstatic.com"],
    'img-src': ["'self'", "https://www.youtube.com", "data:", "https://www.google.com", 
                "https://www.google.ca", "https://googleads.g.doubleclick.net"],
    'connect-src': ["'self'", "https://cb-server-production.up.railway.app", "https://dunnoservicesinc.com"],
    'frame-src': ["'self'", "https://www.youtube.com", "https://td.doubleclick.net"], 
    'object-src': ["'none'"],
    'media-src': ["'self'"]
}
talisman = Talisman(
    app,
    frame_options=None,
    force_https=True,
    strict_transport_security_include_subdomains=True,
    strict_transport_security_max_age=31536000,
    content_security_policy=csp,
    content_security_policy_nonce_in=['script-src', 'style-src']
)

# Enable debug mode
app.debug = False

# Initializations
current_year = datetime.now().year

@app.route('/')
def index():
    current_route = request.path
    return render_template('index.html', current_route=current_route, 
                                            current_year=current_year)


@app.route('/how_to_use')
def how_to_use():
    current_route = request.path
    return render_template('htu_doc2board.html', current_route=current_route,
                            current_year=current_year)

@app.route('/doc2board/how_to_use')
def how_to_use_d2b():
    current_route = request.path
    return render_template('htu_doc2board.html', current_route=current_route,
                            current_year=current_year)

@app.route('/doc2board')
def doc2board():
    current_route = request.path
    return render_template('doc2board.html', current_route=current_route,
                            current_year=current_year)


@app.route('/doc2board/pricing')
def doc2board_pricing():
    current_route = request.path
    return render_template('pricing_d2b.html', current_route=current_route,
                           current_year=current_year)


@app.route('/privacy')
def privacy():
    current_route = request.path
    return render_template('privacy_policy.html', current_route=current_route, 
                                            current_year=current_year)

@app.route('/terms')
def terms():
    current_route = request.path
    return render_template('terms_of_service.html', current_route=current_route, 
                                            current_year=current_year)

@app.route('/monday-app-association.json')
def monday_association():
    print("json route checked")
    rtn_str = open("static/monday-app-association.json")
    print(rtn_str)
    return (rtn_str)


@app.route('/email_notify', methods=["POST", "GET", "OPTIONS"])
def email_notify():
    logging.info(request.headers)
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        logging.info(request.headers)
        response = jsonify({"message": "Preflight OK"})
        response.headers.add("Access-Control-Allow-Origin", "https://dunnoservicesinc.com/")
        response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response, 204

    if request.method == 'POST':
        incoming_data = json.loads(request.data)
        sender_name = incoming_data['sender_name']
        sender_email = incoming_data['sender_email']
        message = incoming_data['sender_message']
        html = f"""
                <h1>Message Received</h1>
                <p>Dear Cogni-Bridge Team,</p>
                <p>You have received a new message from the contact form:</p>
                <ul>
                    <li><strong>Name:</strong> {sender_name}</li>
                    <li><strong>Email:</strong> {sender_email}</li>
                    <li><strong>Message:</strong> {message}</li>
                </ul>
                <p>Thank you!</p>
            """
        logging.debug("Attempting to send email")
        helpers.send_message_received_notification(html)
        logging.debug("Sent email")
        response = jsonify({"message": "success"})
        response.headers.add("Access-Control-Allow-Origin", "https://dunnoservicesinc.com/")
        response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response, 200

    # Handle bad requests
    response = jsonify({"message": "Bad request"})
    response.headers.add("Access-Control-Allow-Origin", "https://dunnoservicesinc.com/")
    return response, 400


if __name__ == '__main__':
    app.run(debug=False)