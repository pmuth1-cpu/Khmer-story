"""
1-Click Fully Autonomous YouTube Video Generator.
Usage:
    python auto_create_video.py
or:
    python auto_create_video.py --topic "ចុះបើភ្លៀងធ្លាក់មួយខែពេញ?" --minutes 8
"""

import os
import sys
import asyncio
import argparse
from typing import Optional

# Load .env if present
env_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

from src.custom_topic_ai import create_ai_longform_script, sanitize_slug
from src.longform_script_generator import export_google_flow_prompts
from src.tts_engine import UnifiedVoiceEngine, generate_srt_subtitles
from src.caption_renderer import render_khmer_caption_png
from src.nanobanana_generator import generate_nanobanana_image, build_nanobanana_prompt
from src.image_helper import generate_cartoon_pill_placeholder
from src.video_builder import build_scene_clip_with_caption, assemble_final_video


async def run_autonomous_pipeline(
    topic_km: str,
    topic_en: str = "",
    duration_minutes: int = 8,
    voice: str = "km-KH-PisethNeural",
    gemini_key: Optional[str] = None
):
    print("\n" + "=" * 70)
    print("🤖 1-CLICK AUTONOMOUS YOUTUBE VIDEO GENERATOR")
    print("=" * 70)
    print(f"📌 Topic (Khmer):    {topic_km}")
    if topic_en:
        print(f"📌 Topic (English):  {topic_en}")
    print(f"⏱️ Target Duration:  {duration_minutes} minutes")
    print(f"🎙️ Khmer Voice:      {voice}")

    api_key = gemini_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if api_key:
        print("🔑 Gemini API Key:   DETECTED (Auto AI Images enabled)")
    else:
        print("ℹ️ Gemini API Key:   None (Using stylized vector preview images)")
        print("   -> Tip: Add GEMINI_API_KEY to generate real Imagen 3 / Nano Banana images automatically.")
    print("=" * 70 + "\n")

    topic_slug = sanitize_slug(topic_en if topic_en else topic_km)
    output_dir = os.path.join("output", f"{topic_slug}_video")
    images_dir = os.path.join(output_dir, "images")
    audio_dir = os.path.join(output_dir, "audio")
    captions_dir = os.path.join(output_dir, "captions")
    clips_dir = os.path.join(output_dir, "clips")

    for d in [images_dir, audio_dir, captions_dir, clips_dir]:
        os.makedirs(d, exist_ok=True)

    # -------------------------------------------------------------
    # Step 1: Autonomous Script & Prompt Generation
    # -------------------------------------------------------------
    print("⏳ [Step 1/5] Generating full scene-by-scene script & prompts...")
    script_data = create_ai_longform_script(
        title_km=topic_km,
        title_en=topic_en if topic_en else topic_km,
        target_minutes=duration_minutes,
        api_key=api_key
    )
    scenes = script_data["scenes"]
    total = len(scenes)
    print(f"   ✓ Generated {total} scenes across structured narrative acts!")

    # Export prompts file
    prompts_file = os.path.join(output_dir, "prompts.txt")
    export_google_flow_prompts(script_data, prompts_file)

    # -------------------------------------------------------------
    # Step 2: Autonomous Khmer TTS Narration Generation
    # -------------------------------------------------------------
    print(f"\n⏳ [Step 2/5] Synthesizing Khmer speech for all {total} scenes...")
    voice_engine = UnifiedVoiceEngine(voice_type="edge_tts", edge_voice=voice)
    timed_scenes = await voice_engine.process_scenes_batch(scenes, audio_dir)
    print("   ✓ All speech audio generated and synchronized!")

    # Export SRT
    srt_file = os.path.join(output_dir, "captions.srt")
    generate_srt_subtitles(timed_scenes, srt_file)

    # -------------------------------------------------------------
    # Step 3: Autonomous Accurate Khmer Caption Cards
    # -------------------------------------------------------------
    print(f"\n⏳ [Step 3/5] Rendering accurate Khmer captions (Chromium HarfBuzz)...")
    for idx, sc in enumerate(timed_scenes, start=1):
        num = sc["scene_num"]
        card_path = os.path.join(captions_dir, f"sub_scene_{num:02d}.png")
        if not os.path.exists(card_path):
            render_khmer_caption_png(sc["khmer_speech"], card_path)
        sc["caption_overlay_path"] = card_path
        if idx % 10 == 0 or idx == total:
            print(f"   - Captions: {idx}/{total} scenes rendered")

    # -------------------------------------------------------------
    # Step 4: Autonomous Image Generation (Human Pill Cartoon Style)
    # -------------------------------------------------------------
    print(f"\n⏳ [Step 4/5] Preparing Human Pill Cartoon images...")
    for idx, sc in enumerate(timed_scenes, start=1):
        num = sc["scene_num"]
        img_path = os.path.join(images_dir, f"scene_{num:02d}.png")
        
        if not os.path.exists(img_path):
            generated_ai = False
            if api_key:
                prompt = build_nanobanana_prompt(
                    action=sc["action"],
                    environment=sc["environment"],
                    emotion=sc.get("emotion", "curious")
                )
                generated_ai = generate_nanobanana_image(prompt, img_path, api_key=api_key)
            
            if not generated_ai:
                generate_cartoon_pill_placeholder(
                    output_path=img_path,
                    scene_num=num,
                    action_text=sc["action"],
                    khmer_text=sc["khmer_speech"]
                )

        sc["image_path"] = img_path
        if idx % 10 == 0 or idx == total:
            print(f"   - Images: {idx}/{total} prepared")

    # -------------------------------------------------------------
    # Step 5: Autonomous Video Assembly (Motion + Captions + Audio)
    # -------------------------------------------------------------
    print(f"\n⏳ [Step 5/5] Assembling final YouTube MP4 video with Ken Burns motion...")
    scene_clips = []
    for idx, sc in enumerate(timed_scenes, start=1):
        clip_path = os.path.join(clips_dir, f"clip_{sc['scene_num']:02d}.mp4")
        zoom_in = (idx % 2 == 0)
        build_scene_clip_with_caption(
            image_path=sc["image_path"],
            audio_path=sc["audio_path"],
            caption_overlay_path=sc["caption_overlay_path"],
            duration=sc["display_duration"],
            output_clip_path=clip_path,
            zoom_in=zoom_in
        )
        scene_clips.append(clip_path)
        if idx % 10 == 0 or idx == total:
            print(f"   - Video clips: {idx}/{total} encoded")

    final_video_path = os.path.join(output_dir, "final_youtube_video.mp4")
    assemble_final_video(scene_clips=scene_clips, final_output_path=final_video_path)

    total_secs = sum(sc["display_duration"] for sc in timed_scenes)
    total_mins = total_secs / 60.0

    print("\n" + "=" * 70)
    print("🎉 FULL VIDEO AUTOMATION COMPLETED!")
    print("=" * 70)
    print(f"🎥 Finished Video:     {os.path.abspath(final_video_path)}")
    print(f"⏱️ Actual Duration:   {total_mins:.1f} minutes ({total_secs:.1f} seconds)")
    print(f"📝 YouTube Captions:   {os.path.abspath(srt_file)}")
    print(f"🎨 Prompts File:       {os.path.abspath(prompts_file)}")
    print("=" * 70 + "\n")

    return final_video_path


def main():
    parser = argparse.ArgumentParser(description="Autonomous YouTube Video Maker")
    parser.add_argument("--topic", help="Khmer topic title / question")
    parser.add_argument("--topic-en", default="", help="English topic title")
    parser.add_argument("--minutes", type=int, default=8, help="Video duration in minutes (e.g. 8, 10, 15)")
    parser.add_argument("--voice", default="km-KH-PisethNeural", help="Khmer voice (km-KH-PisethNeural or km-KH-SreymomNeural)")
    parser.add_argument("--key", default=None, help="Gemini API Key")
    args = parser.parse_args()

    topic_km = args.topic
    if not topic_km:
        print("=" * 60)
        print("🎬 YOUTUBE VIDEO 1-CLICK AUTOMATION")
        print("=" * 60)
        topic_km = input("បញ្ចូលប្រធានបទវីដេអូ (Topic in Khmer) [Enter for default]: ").strip()
        if not topic_km:
            topic_km = "ចុះបើភ្លៀងធ្លាក់ជាប់គ្នាពេញមួយខែ?"

    asyncio.run(run_autonomous_pipeline(
        topic_km=topic_km,
        topic_en=args.topic_en,
        duration_minutes=args.minutes,
        voice=args.voice,
        gemini_key=args.key
    ))


if __name__ == "__main__":
    main()
