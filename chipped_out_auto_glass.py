# Standard Library Imports
import json
import logging
import os
import smtplib

# Third-Party Imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(16).hex()

# Load environment variables from .env file
load_dotenv()

# Retrieve reCAPTCHA keys from environment variables
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")
RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY")


@app.route("/")
def home():
    """Home route that renders the index.html and passes the reCAPTCHA site key."""
    return render_template("index.html", site_key=RECAPTCHA_SITE_KEY)


@app.route("/form", methods=["POST"])
def form_submit():
    """
    Handles the form submission.
    Verifies the reCAPTCHA response, collects the form fields, and sends an email.
    """
    # Collect and verify reCAPTCHA data
    recaptcha_response = request.form.get("g-recaptcha-response")
    payload = {"secret": RECAPTCHA_SECRET_KEY, "response": recaptcha_response}
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", data=payload
    )
    result = response.json()

    if not result["success"] or result["score"] < 0.5:
        flash("reCAPTCHA verification failed. Please try again.", "error")
        return redirect(url_for("home"))

    # Get form fields
    name = request.form.get("name")
    user_email = request.form.get("email")
    state = request.form.get("state")
    license_plate = request.form.get("license-plate")
    message = request.form.get("message")
    phone_number = request.form.get("phone-number")
    allow_advertising = (
        request.form.get("allow-advertising") == "on"
    )  # Checkbox returns "on" if checked

    # Search for license plate
    vehicle_info = license_plate_search(license_plate, state)

    # Retrieve email settings from environment variables
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    receiver_email = os.environ.get("RECEIVER_EMAIL")

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = f"New message from {name}"
    msg["Reply-To"] = user_email  # User's email set in Reply-To field

    email_body = (
        f"{name},\n\n"
        f"Message: {message}\n\n"
        f"State: {state}\n"
        f"Phone Number: {phone_number}\n"
        f"Email: {user_email}\n"
        f"Allow Advertising: {'Yes' if allow_advertising else 'No'}\n"
        f"Vehicle Info:\n{vehicle_info}"
    )

    msg.attach(MIMEText(email_body, "plain"))

    # Establish a secure session with Gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Secure the connection
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

    flash("Email sent successfully.")
    return redirect(url_for("home"))


def make_api_request(license_plate, state):
    """
    Makes an API request to convert a license plate to VIN data.
    Returns a dictionary of the API response.
    """
    plate_to_vin_url = "https://platetovin.com/api/convert"

    payload = {"plate": license_plate, "state": state}

    headers = {
        "Authorization": "imcOfy5D2xZVSGp",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        response = requests.post(plate_to_vin_url, headers=headers, json=payload)
        response.raise_for_status()
        return json.loads(response.text)
    except requests.HTTPError as e:
        logging.error(f"HTTP Error: {e}")
        return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None


def format_response_to_pretty_string(vin_data):
    """
    Formats the VIN data dictionary into a readable string.
    Returns the formatted string.
    """
    return (
        f"Vin: {vin_data.get('vin')}\n"
        f"Year: {vin_data.get('year')}\n"
        f"Make: {vin_data.get('make')}\n"
        f"Model: {vin_data.get('model')}\n"
        f"Trim: {vin_data.get('trim')}\n"
        f"Name: {vin_data.get('name')}\n"
        f"Engine: {vin_data.get('engine')}\n"
        f"Style: {vin_data.get('style')}\n"
        f"Transmission: {vin_data.get('transmission')}\n"
        f"Drive Type: {vin_data.get('driveType')}\n"
        f"Fuel: {vin_data.get('fuel')}\n"
        f"Color: {vin_data.get('color', {}).get('name')} "
        f"({vin_data.get('color', {}).get('abbreviation')})"
    )


def license_plate_search(license_plate, state):
    """
    Conducts a license plate search by making an API request and formatting the response.
    Returns the formatted VIN data string or an error message.
    """
    response_dict = make_api_request(license_plate, state)

    if response_dict and response_dict.get("success"):
        vin_data = response_dict.get("vin", {})
        return format_response_to_pretty_string(vin_data)
    else:
        return "License plate search was unsuccessful."


if __name__ == "__main__":
    app.run(debug=True)
