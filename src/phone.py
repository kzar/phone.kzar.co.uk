import smtplib
from functools import wraps
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from flask import Flask, request
import twilio.twiml
from twilio.util import RequestValidator
from twilio.rest import TwilioRestClient

application = Flask(__name__)
application.config.from_pyfile("../config/phone.cfg")

client = TwilioRestClient(application.config["TWILIO_ACCOUNT_SID"],
                          application.config["TWILIO_AUTH_TOKEN"])
validator = RequestValidator(application.config["TWILIO_AUTH_TOKEN"])

def validated_twilio_request(f):
  @wraps(f)
  def validated(*args, **kwargs):
    if not validator.validate(request.url, request.form,
                              request.headers.get('X-Twilio-Signature', '')):
      return "401 - Incorrect X-Twilio-Signiture", 401
    return f(*args, **kwargs)
  return validated

def send_email(subject, body):
  email = application.config["GOOGLE_EMAIL"]

  msg = MIMEMultipart()
  msg["From"] = email
  msg["To"] = email
  msg["Subject"] = subject
  msg.attach(MIMEText(body, "plain"))

  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(email, application.config["GOOGLE_PASSWORD"])
  try:
    return server.sendmail(email, email, msg.as_string())
  finally:
    server.quit()

def execute_sms_command(twilio_number, sender, body):
  response = twilio.twiml.Response()

  # PWD CMD ARGS
  _, command, args = body.split(" ", 2)

  if command.upper() == "SEND":
    # "PWD SEND TO [FROM]: MSG"
    dest, message = args.split(":", 1)
    from_ = twilio_number
    if " " in dest:
      dest, from_ = dest.split(" ", 1)

    response.message(
      client.messages.create(
        to=dest, from_=from_, body=message.lstrip()
      ).sid
    )
  else:
    response.message("Unknown command '%s'" % command)

  return str(response)

@application.route("/sms", methods=["POST"])
@validated_twilio_request
def sms():
  if request.form["Body"].startswith(application.config["SMS_PASSWORD"]):
    return execute_sms_command(request.form["To"],
                               request.form["From"], request.form["Body"])

  send_email("SMS from " + request.form["From"], request.form["Body"])
  response = twilio.twiml.Response()
  return str(response)

@application.route("/voice", methods=["POST"])
@validated_twilio_request
def voice():
  response = twilio.twiml.Response()
  response.record(timeout="10", action="/recording", playBeep=False)
  return str(response)

@application.route("/recording", methods=["POST"])
@validated_twilio_request
def recording():
  send_email("Voicemail from " + request.form["From"],
             request.form["RecordingUrl"])

  response = twilio.twiml.Response()
  return str(response)

if __name__ == "__main__":
  application.run(debug=True)
