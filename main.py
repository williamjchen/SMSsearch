from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from search import search_gpt

app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    body = request.values.get('Body', None)

    resp = MessagingResponse()

    # Determine the right reply for this message
    resp.message(search_gpt(body))

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
