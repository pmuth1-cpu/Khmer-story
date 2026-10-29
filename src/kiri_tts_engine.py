"""
Kiri TTS Engine for Native Khmer Speech Generation (kiritts.com).
Uses OpenAI-compatible endpoint: https://api.kiritts.com/v1/audio/speech
"""

import os
import requests
from typing import Optional, List, Dict


class KiriTTSEngine:
    def __init__(self, api_key: str, voice: str = "Maly", speed: float = 1.0):
        self.api_key = api_key
        self.voice = voice
        self.speed = speed
        self.endpoint = "https://api.kiritts.com/v1/audio/speech"

    def generate_speech(self, text: str, output_path: str) -> bool:
        """
        Calls Kiri TTS API to generate MP3 speech for a scene or full script.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "kiritts",
            "input": text,
            "voice": self.voice,
            "response_format": "mp3",
            "speed": self.speed
        }

        try:
            res = requests.post(self.endpoint, headers=headers, json=data, timeout=45)
            if res.status_code == 200:
                os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(res.content)
                return True
            else:
                error_msg = res.json().get("error", {}).get("message", res.text[:200])
                print(f"[Kiri TTS API Error {res.status_code}]: {error_msg}")
                return False
        except Exception as e:
            print(f"[Kiri TTS Request Exception]: {e}")
            return False
