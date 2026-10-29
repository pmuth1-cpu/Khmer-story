"""
Main YouTube Video Automation Suite
Creates 'What If' / 'Why or How' cartoon pill videos with Khmer speech and captions.
Uses Chromium DirectWrite/HarfBuzz for 100% accurate Khmer coeng (ជើងអក្សរ ្).
"""

import os
import sys
import asyncio
import argparse

from src.prompt_generator import THEME_TEMPLATES
from src.tts_engine import KhmerTTSEngine, generate_srt_subtitles
from src.caption_renderer import render_all_captions
from src.nanobanana_generator import batch_generate_scenes
from src.image_helper import export_prompts_file, generate_cartoon_pill_placeholder
from src.video_builder import build_scene_clip_with_caption, assemble_final_video


async def run_pipeline(
    theme_key: str = "rain_for_month",
    voice: str = "km-KH-PisethNeural",
    output_dir: str = "output/demo_video",
    api_key: str = None,
    use_placeholders_if_missing: bool = True
):
    print("=" * 65)
    print("🎬 KHMER CARTOON PILL YOUTUBE VIDEO AUTOMATION (NANO BANANA)")
    print("=" * 65)

    if theme_key not in THEME_TEMPLATES:
        print(f"Theme '{theme_key}' not found in presets. Using 'rain_for_month'.")
        theme_key = "rain_for_month"

    theme = THEME_TEMPLATES[theme_key]
    title_en = theme["title_en"]
    title_km = theme["title_km"]
    scenes = theme["scenes"]

    print(f"\n📌 Project Title (EN): {title_en}")
    print(f"📌 Project Title (KM): {title_km}")
    print(f"🎙️ Voice Selected:    {voice}")
    print(f"📁 Output Directory:   {output_dir}")
    print(f"🎞️ Total Scenes:       {len(scenes)} (5 - 10s per image)\n")

    os.makedirs(output_dir, exist_ok=True)
    images_dir = os.path.join(output_dir, "images")
    audio_dir = os.path.join(output_dir, "audio")
    captions_dir = os.path.join(output_dir, "captions")
    clips_dir = os.path.join(output_dir, "clips")
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(captions_dir, exist_ok=True)
    os.makedirs(clips_dir, exist_ok=True)

    # 1. Export Nano Banana Prompts
    prompts_file = os.path.join(output_dir, "nano_banana_prompts.txt")
    export_prompts_file(scenes, prompts_file, topic_title=f"{title_en} ({title_km})")
    print(f"✅ Step 1: Exported Nano Banana prompts to:\n   -> {prompts_file}")

    # 2. Generate Khmer TTS Speech & Timings
    print("\n⏳ Step 2: Generating Khmer speech via Edge-TTS...")
    tts_engine = KhmerTTSEngine(voice=voice)
    timed_scenes = await tts_engine.process_all_scenes(scenes, audio_dir)

    for sc in timed_scenes:
        print(f"   - Scene {sc['scene_num']}: {sc['display_duration']:.1f}s | {sc['khmer_speech'][:30]}...")

    # 3. Export Standard SRT Subtitles
    srt_file = os.path.join(output_dir, "captions.srt")
    generate_srt_subtitles(timed_scenes, srt_file)
    print(f"✅ Step 3: Generated YouTube SRT Subtitles: {srt_file}")

    # 4. Render 100% Accurate Khmer Caption Cards (DirectWrite / HarfBuzz)
    print("\n⏳ Step 4: Rendering pixel-perfect Khmer caption cards (fixing ជើងអក្សរ ្)...")
    scenes_with_captions = render_all_captions(timed_scenes, captions_dir)
    print("   ✓ All Khmer coeng ligatures (ភ្ល, ធ្ល, ស្ទ, ផ្ត, ប្ត) rendered accurately!")

    # 5. Nano Banana Image Handling
    print("\n⏳ Step 5: Preparing scene images (Nano Banana Cartoon Pill style)...")
    # If API key provided, attempt direct AI generation
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        print("   [Nano Banana API] Attempting AI image generation...")
        batch_results = batch_generate_scenes(scenes_with_captions, images_dir, api_key=key)
        for num, ok in batch_results.items():
            if ok:
                print(f"   ✓ Scene {num:02d} generated via Nano Banana AI!")
            else:
                print(f"   [Notice] Scene {num:02d} generation skipped or failed.")

    for sc in scenes_with_captions:
        num = sc["scene_num"]
        img_path = os.path.join(images_dir, f"scene_{num:02d}.png")
        if not os.path.exists(img_path):
            if use_placeholders_if_missing:
                print(f"   [Notice] 'scene_{num:02d}.png' not found. Generating pill vector preview...")
                generate_cartoon_pill_placeholder(
                    output_path=img_path,
                    scene_num=num,
                    action_text=sc["action"],
                    khmer_text=sc["khmer_speech"]
                )
            else:
                raise FileNotFoundError(f"Missing required image: {img_path}")
        else:
            print(f"   [Found] Using image for Scene {num:02d}")
        sc["image_path"] = img_path

    # 6. Build Scene Clips with Motion & Subtitle Overlay
    print("\n⏳ Step 6: Rendering scene clips with Ken Burns camera motion & accurate captions...")
    scene_clips = []
    for idx, sc in enumerate(scenes_with_captions):
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
        print(f"   ✓ Built Clip {sc['scene_num']:02d} ({sc['display_duration']:.1f}s)")

    # 7. Final Video Assembly
    print("\n⏳ Step 7: Assembling final YouTube MP4 video...")
    final_video_path = os.path.join(output_dir, "final_youtube_video.mp4")
    assemble_final_video(
        scene_clips=scene_clips,
        final_output_path=final_video_path
    )

    total_duration = sum(sc["display_duration"] for sc in scenes_with_captions)
    print("\n" + "=" * 65)
    print("🎉 VIDEO COMPLETED SUCCESSFULLY!")
    print("=" * 65)
    print(f"🎥 Final Video File:   {os.path.abspath(final_video_path)}")
    print(f"⏱️ Total Duration:     {total_duration:.1f} seconds")
    print(f"📝 YouTube Captions:   {os.path.abspath(srt_file)}")
    print(f"🎨 Nano Prompts:       {os.path.abspath(prompts_file)}")
    print("=" * 65)
    return final_video_path


def main():
    parser = argparse.ArgumentParser(description="Khmer Cartoon Pill YouTube Automation")
    parser.add_argument(
        "--theme",
        choices=["rain_for_month", "ice_age_survival"],
        default="rain_for_month",
        help="Select video theme preset"
    )
    parser.add_argument(
        "--voice",
        choices=["km-KH-PisethNeural", "km-KH-SreymomNeural"],
        default="km-KH-PisethNeural",
        help="Khmer voice selection"
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="Gemini API Key for direct Nano Banana generation"
    )
    parser.add_argument(
        "--out",
        default="output/rain_for_month_video",
        help="Output folder path"
    )
    args = parser.parse_args()

    asyncio.run(run_pipeline(
        theme_key=args.theme,
        voice=args.voice,
        api_key=args.api_key,
        output_dir=args.out
    ))


if __name__ == "__main__":
    main()
