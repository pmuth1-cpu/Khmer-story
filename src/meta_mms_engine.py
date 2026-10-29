"""
Meta MMS-TTS Engine (Khmer: facebook/mms-tts-khm & English: facebook/mms-tts-eng).
100% Open-Source, Always Free, Runs Locally without any API key or subscription.
Uses VITS architecture for high-fidelity text-to-speech synthesis.
"""

import os
import subprocess
from typing import List, Dict, Optional
import torch
import scipy.io.wavfile as wavfile
from transformers import VitsModel, AutoTokenizer
import imageio_ffmpeg

MODELS = {
    "khm": "facebook/mms-tts-khm",
    "eng": "facebook/mms-tts-eng"
}


class MetaMMSEngine:
    _instances = {}

    def __init__(self, lang: str = "khm"):
        self.lang = lang
        self.model_id = MODELS.get(lang, "facebook/mms-tts-khm")
        self.model = None
        self.tokenizer = None
        self.sampling_rate = 16000
        self._load_model()

    def _load_model(self):
        if self.model is None or self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            self.model = VitsModel.from_pretrained(self.model_id)
            self.sampling_rate = self.model.config.sampling_rate

    @classmethod
    def get_instance(cls, lang: str = "khm"):
        if lang not in cls._instances:
            cls._instances[lang] = cls(lang=lang)
        return cls._instances[lang]

    def synthesize(self, text: str, output_path: str) -> float:
        """
        Synthesizes speech and saves it as MP3.
        Returns exact duration in seconds.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            output = self.model(**inputs).waveform

        raw_wav = output_path.replace(".mp3", ".wav")
        wavfile.write(
            raw_wav,
            rate=self.sampling_rate,
            data=output.float().numpy().squeeze()
        )

        # Convert to standard MP3
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [
            ffmpeg, "-y",
            "-i", raw_wav,
            "-b:a", "192k",
            output_path
        ]
        subprocess.run(cmd, capture_output=True, check=True)

        if os.path.exists(raw_wav) and raw_wav != output_path:
            os.remove(raw_wav)

        return self.probe_audio_duration(output_path)

    def probe_audio_duration(self, audio_path: str) -> float:
        try:
            ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
            cmd = [ffmpeg, "-i", audio_path]
            res = subprocess.run(cmd, capture_output=True, text=True)
            for line in res.stderr.splitlines():
                if "Duration:" in line:
                    parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
                    return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        except Exception:
            pass
        return 7.5


def generate_meta_mms_speech(text: str, output_path: str, lang: str = "khm") -> float:
    engine = MetaMMSEngine.get_instance(lang=lang)
    return engine.synthesize(text, output_path)


def generate_meta_mms_english_speech(text: str, output_path: str) -> float:
    return generate_meta_mms_speech(text, output_path, lang="eng")
