"""
Unified TTS and Voice Engine.
Supports:
1. Edge-TTS with Expressive Pitch & Rate
2. ElevenLabs Multilingual v2 Emotional Storyteller
3. Custom Voice Actor Audio Injection
"""

import os
import asyncio
from typing import Dict, List, Optional
import edge_tts

from src.elevenlabs_engine import generate_elevenlabs_speech, VOICE_PRESETS


class UnifiedVoiceEngine:
    def __init__(
        self,
        voice_type: str = "meta_mms",
        edge_voice: str = "km-KH-PisethNeural",
        elevenlabs_key: Optional[str] = None,
        elevenlabs_voice_id: str = "pNInz6obpgDQGcFmaJgB",
        speech_rate: str = "-4%"
    ):
        """
        voice_type: 'meta_mms' (100% free offline Meta VITS), 'edge_tts', or 'elevenlabs'
        """
        self.voice_type = voice_type
        self.edge_voice = edge_voice
        self.elevenlabs_key = elevenlabs_key
        self.elevenlabs_voice_id = elevenlabs_voice_id
        self.speech_rate = speech_rate

    async def generate_scene_audio(self, text: str, output_path: str) -> float:
        """
        Generates audio for one scene and returns its exact duration in seconds.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        if self.voice_type == "meta_mms":
            from src.meta_mms_engine import generate_meta_mms_speech
            return generate_meta_mms_speech(text, output_path)

        if self.voice_type == "elevenlabs" and self.elevenlabs_key:
            success = generate_elevenlabs_speech(
                text=text,
                output_audio_path=output_path,
                api_key=self.elevenlabs_key,
                voice_id=self.elevenlabs_voice_id
            )
            if success:
                return self.probe_audio_duration(output_path)

        # Fallback to Expressive Edge-TTS
        comm = edge_tts.Communicate(text=text, voice=self.edge_voice, rate=self.speech_rate)
        duration = 0.0
        with open(output_path, "wb") as f:
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "SentenceBoundary":
                    end_time = (chunk["offset"] + chunk["duration"]) / 10_000_000.0
                    if end_time > duration:
                        duration = end_time

        if duration <= 0.0:
            duration = self.probe_audio_duration(output_path)

        return duration

    def probe_audio_duration(self, audio_path: str) -> float:
        try:
            import imageio_ffmpeg
            import subprocess
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            cmd = [
                ffmpeg_exe, "-i", audio_path
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            # Parse Duration: 00:00:07.84
            for line in res.stderr.splitlines():
                if "Duration:" in line:
                    parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
                    return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        except Exception:
            pass
        return 7.5

    async def process_scenes_batch(self, scenes: List[Dict], output_dir: str) -> List[Dict]:
        """
        Processes audio for all scenes in parallel/sequence.
        Respects custom uploaded audio if already present at output_dir/scene_XX.mp3.
        """
        os.makedirs(output_dir, exist_ok=True)
        results = []
        for sc in scenes:
            num = sc["scene_num"]
            audio_path = os.path.join(output_dir, f"scene_{num:02d}.mp3")

            # Check if custom voice actor audio was already uploaded
            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1024:
                duration = self.probe_audio_duration(audio_path)
            else:
                duration = await self.generate_scene_audio(sc["khmer_speech"], audio_path)

            display_dur = max(5.0, min(12.0, duration + 0.6))
            sc_copy = dict(sc)
            sc_copy["audio_path"] = audio_path
            sc_copy["speech_duration"] = duration
            sc_copy["display_duration"] = display_dur
            results.append(sc_copy)

        return results


def generate_srt_subtitles(scenes: List[Dict], output_srt_path: str, use_english: bool = False):
    def format_ts(s: float) -> str:
        h = int(s // 3600)
        m = int((s % 3600) // 60)
        sec = int(s % 60)
        ms = int((s - int(s)) * 1000)
        return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

    lines = []
    t = 0.0
    for idx, sc in enumerate(scenes, start=1):
        dur = sc.get("display_duration", 7.5)
        start_str = format_ts(t)
        end_str = format_ts(t + dur)
        
        sub_text = sc.get("english_speech") if use_english else (sc.get("khmer_speech") or sc.get("english_speech", ""))
        if not sub_text:
            sub_text = sc.get("speech_text", "")

        lines.append(f"{idx}")
        lines.append(f"{start_str} --> {end_str}")
        lines.append(sub_text)
        lines.append("")
        t += dur

    os.makedirs(os.path.dirname(os.path.abspath(output_srt_path)), exist_ok=True)
    with open(output_srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
