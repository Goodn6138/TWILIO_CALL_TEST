import os
import pytest
from app import create_app
from unittest.mock import patch

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ---------------------------
# Test /voice endpoint
# ---------------------------
def test_voice_endpoint(client):
    response = client.post("/voice")
    assert response.status_code == 200
    # Should contain TwiML <Say> tag
    assert b"<Say>" in response.data
    assert b"Hello. Speak after the beep." in response.data

# ---------------------------
# Test /process endpoint
# ---------------------------
@patch("app.services.stt.transcribe")
@patch("app.services.llm.generate_reply")
@patch("app.services.tts.synthesize")
@patch("app.utils.audio.download_audio")
def test_process_endpoint(mock_download, mock_tts, mock_llm, mock_stt, client):
    # Mock return values
    mock_download.return_value = "input.wav"
    mock_stt.return_value = "Hello world"
    mock_llm.return_value = "You said hello"
    mock_tts.return_value = "https://example.com/response.mp3"

    # Simulate POST from Twilio
    response = client.post("/process", data={"RecordingUrl": "https://example.com/audio"})

    assert response.status_code == 200
    # Should contain <Play> tag for TTS
    assert b"<Play>" in response.data
    assert b"https://example.com/response.mp3" in response.data

    # Check that mocks were called
    mock_download.assert_called_once()
    mock_stt.assert_called_once()
    mock_llm.assert_called_once()
    mock_tts.assert_called_once()
