import requests
import os
import uuid

def synthesize(text):
    """
    Convert text to speech using ElevenLabs
    Returns a public URL to the audio file
    """
    try:
        api_key = os.getenv("ELEVENLABS_API_KEY")
        voice_id = "EXAVITQu4vr4xnSDxMaL"

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }

        data = {
            "text": text,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.7
            }
        }

        response = requests.post(url, json=data, headers=headers)

        # unique filename per request (important for concurrent calls)
        filename = f"{uuid.uuid4()}.mp3"
        os.makedirs("static", exist_ok=True)

        file_path = f"static/{filename}"
        with open(file_path, "wb") as f:
            f.write(response.content)

        base_url = os.getenv("PUBLIC_BASE_URL")
        return f"{base_url}/static/{filename}"

    except Exception as e:
        print("TTS Error:", e)
        return None
