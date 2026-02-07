"""
Flask application - minimal routing layer.
All business logic is delegated to the engine.
"""
from flask import Flask, request, Response

from adapters.twilio_sms import twilio_sms_adapter
from adapters.base import OutgoingMessage
from engine.assistant import assistant_engine
from utils.logging import logger

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.route("/sms", methods=["POST"])
def sms_webhook():
    """
    Twilio SMS/WhatsApp webhook.
    This is now a thin adapter layer.
    """
    try:
        # Parse incoming message
        incoming = twilio_sms_adapter.parse_incoming(request.form.to_dict())
        
        logger.info("Incoming message", extra={
            "user_id": incoming.user_id,
            "extra_data": {
                "channel": incoming.channel,
                "content_length": len(incoming.content),
            }
        })
        
        # Process through engine
        response_text = assistant_engine.process_message(
            user_id=incoming.user_id,
            message=incoming.content,
        )
        
        # Format response
        outgoing = OutgoingMessage(content=response_text, user_id=incoming.user_id)
        twiml = twilio_sms_adapter.format_outgoing(outgoing)
        
        return Response(twiml, mimetype="application/xml")
        
    except Exception as e:
        logger.exception("Webhook error")
        
        # Return a graceful error message
        from twilio.twiml.messaging_response import MessagingResponse
        response = MessagingResponse()
        response.message("Sorry, I\'m having trouble right now. Please try again in a moment.")
        return Response(str(response), mimetype="application/xml")


@app.route("/voice", methods=["POST"])
def voice_webhook():
    """
    Placeholder for Twilio Voice webhook.
    Will be implemented with same engine, different adapter.
    """
    from twilio.twiml.voice_response import VoiceResponse
    response = VoiceResponse()
    response.say("Voice support is coming soon. Please text me instead.")
    response.hangup()
    return Response(str(response), mimetype="application/xml")


if __name__ == "__main__":
    app.run(port=5000, debug=False)
