import requests
import os
import uuid

def download_audio(url: str) -> str:
    """
    Downloads an audio file from the given URL and saves it locally.
    
    Args:
        url (str): The URL of the audio file (from Twilio RecordingUrl)
        
    Returns:
        str: The local file path of the downloaded audio
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error if download fails

        # Create unique filename to handle concurrent calls
        filename = f"{uuid.uuid4()}.wav"
        os.makedirs("static/audio", exist_ok=True)
        file_path = os.path.join("static/audio", filename)

        with open(file_path, "wb") as f:
            f.write(response.content)

        return file_path

    except requests.RequestException as e:
        print(f"Audio download error: {e}")
        return None
