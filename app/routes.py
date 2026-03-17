from flask import Blueprint, request
from twilio.twiml.voice_response import VoiceResponse

from app.services.stt import transcribe
from app.services.tts import synthesize
from app.services.llm import generate_reply
from app.utils.audio import download_audio

main = Blueprint("main", __name__)

@main.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    resp.say("Hello. Speak after the beep.")
    resp.record(max_length=5, action="/process")
    return str(resp)

@main.route("/process", methods=["POST"])
def process():
    recording_url = request.form.get("RecordingUrl") + ".wav"

    file_path = download_audio(recording_url)

    user_text = transcribe(file_path)
    print("User:", user_text)

    reply = generate_reply(user_text)

    audio_url = synthesize(reply)

    resp = VoiceResponse()
    resp.play(audio_url)

    return str(resp)
