"""
Edge-TTS Neural Voice Engine.
100% Free, High-Quality Emotional Storytelling Voices (Kurzgesagt / Documentary style).
"""

import os
import asyncio
import subprocess
import edge_tts
import imageio_ffmpeg

DEFAULT_VOICE = "en-US-ChristopherNeural"

VOICE_PRESETS = {
    "christopher": "en-US-ChristopherNeural",  # Deep documentary / Kurzgesagt narrator
    "guy": "en-US-GuyNeural",                  # Expressive & passionate storytelling
    "eric": "en-US-EricNeural",                # Youthful, energetic curiosity educator
    "ryan": "en-GB-RyanNeural",                # British BBC science documentary style
    "aria": "en-US-AriaNeural",                # Expressive conversational female
    "ava": "en-US-AvaNeural"                   # Crisp modern AI female
}


async def _synthesize_async(text: str, output_path: str, voice: str = DEFAULT_VOICE, rate: str = "+0%") -> float:
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    target_voice = VOICE_PRESETS.get(voice, voice)
    communicate = edge_tts.Communicate(text, target_voice, rate=rate)
    await communicate.save(output_path)
    return probe_audio_duration(output_path)


def generate_edge_tts_speech(text: str, output_path: str, voice: str = DEFAULT_VOICE, rate: str = "+0%") -> float:
    """Synchronous wrapper for generating speech via Edge-TTS."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    if loop.is_running():
        # Running inside another event loop
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return pool.submit(lambda: asyncio.run(_synthesize_async(text, output_path, voice, rate))).result()
    else:
        return loop.run_until_complete(_synthesize_async(text, output_path, voice, rate))


def probe_audio_duration(audio_path: str) -> float:
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
