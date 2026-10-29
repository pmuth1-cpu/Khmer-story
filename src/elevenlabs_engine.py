"""
ElevenLabs Emotional Voice Engine for Khmer / Multilingual Speech.
Uses ElevenLabs Multilingual v2 for dramatic, emotional storytelling.
"""

import os
import requests
from typing import Optional

# Popular emotional storytelling voice IDs on ElevenLabs
VOICE_PRESETS = {
    "adam_deep_storyteller": {
        "id": "pNInz6obpgDQGcFmaJgB",
        "name": "Adam (Deep Documentary Storyteller)",
        "style": "Dramatic, serious, deep curiosity"
    },
    "rachel_warm_explainer": {
        "id": "21m00Tcm4TlvDq8ikWAM",
        "name": "Rachel (Warm, Expressive Explainer)",
        "style": "Energetic, engaging, clear educational"
    },
    "antoni_cinematic": {
        "id": "ErXwobaYiN019PkySvjV",
        "name": "Antoni (Cinematic Narration)",
        "style": "Epic, mysterious, suspenseful"
    },
    "charlotte_intense": {
        "id": "XB0fDUnXU5powFXDhCwa",
        "name": "Charlotte (Intense & Emotional)",
        "style": "Emotional, captivated"
    }
}


def generate_elevenlabs_speech(
    text: str,
    output_audio_path: str,
    api_key: Optional[str] = None,
    voice_id: str = "pNInz6obpgDQGcFmaJgB",
    stability: float = 0.45,
    similarity_boost: float = 0.85
) -> bool:
    """
    Calls ElevenLabs text-to-speech API using eleven_multilingual_v2.
    """
    key = api_key or os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        return False

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": key
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": 0.55,
            "use_speaker_boost": True
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(os.path.abspath(output_audio_path)), exist_ok=True)
            with open(output_audio_path, "wb") as f:
                f.write(response.content)
            return True
        else:
            print(f"[ElevenLabs Error] HTTP {response.status_code}: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"[ElevenLabs Error] Request failed: {e}")
        return False
