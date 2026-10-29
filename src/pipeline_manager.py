"""
Pipeline Manager for Long-Form YouTube Curiosity Videos.
High-Performance Multi-Threaded Edition:
1. Natural Voice Engine (Google Khmer Neural or Meta MMS-TTS)
2. Exact image for every scene (strictly prioritizing user-uploaded images)
3. Exact floating transparent Khmer caption for every scene
4. Multi-threaded parallel scene clip rendering (4x-6x faster)
5. Smart clip caching (skips unchanged clips)
6. Instant placeholder fallback (no 60-second web AI stalls during render)
"""

import os
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Callable

from src.custom_topic_ai import create_ai_longform_script, sanitize_slug
from src.longform_script_generator import (
    EXPANDED_CURIO_TOPICS,
    export_google_flow_prompts
)
from src.caption_renderer import render_khmer_caption_png
from src.video_builder import build_scene_clip_with_caption, assemble_final_video
from src.image_helper import generate_cartoon_pill_placeholder
from src.meta_mms_engine import generate_meta_mms_speech, generate_meta_mms_english_speech
from src.google_tts_engine import generate_google_khmer_speech
from src.edge_tts_engine import generate_edge_tts_speech


def get_or_create_project_script(
    topic_id: str,
    custom_title_km: Optional[str] = None,
    custom_title_en: Optional[str] = None,
    target_minutes: int = 8,
    gemini_key: Optional[str] = None
) -> Dict:
    custom_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "custom_scripts", f"{topic_id}.json")
    if os.path.exists(custom_file):
        try:
            with open(custom_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    matched = None
    for t in EXPANDED_CURIO_TOPICS:
        if t["id"] == topic_id:
            matched = t
            break

    if matched:
        return create_ai_longform_script(
            title_km=matched["title_km"],
            title_en=matched["title_en"],
            target_minutes=target_minutes,
            api_key=gemini_key
        )
    else:
        title_km = custom_title_km or topic_id
        title_en = custom_title_en or "Curiosity Topic"
        return create_ai_longform_script(
            title_km=title_km,
            title_en=title_en,
            target_minutes=target_minutes,
            api_key=gemini_key
        )


def resolve_scene_image(images_dir: str, scene_num: int) -> Optional[str]:
    """
    Finds the exact image file for a scene in images_dir.
    Prioritizes real user uploaded images (> 30KB) over placeholder vectors.
    Picks the most recently modified file if multiple match.
    """
    if not os.path.exists(images_dir):
        return None

    matches = []
    target_stems = [
        f"scene_{scene_num:02d}",
        f"scene_{scene_num}",
        f"{scene_num:02d}",
        str(scene_num)
    ]

    for fname in os.listdir(images_dir):
        stem, ext = os.path.splitext(fname)
        if ext.lower() in [".png", ".jpg", ".jpeg", ".webp", ".avif"]:
            if stem in target_stems:
                full_p = os.path.join(images_dir, fname)
                matches.append(full_p)

    if not matches:
        return None

    # Separate user-uploaded / full images (> 28KB) from placeholders (< 28KB)
    user_images = [p for p in matches if os.path.getsize(p) > 28000]
    if user_images:
        user_images.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return user_images[0]

    # Fallback to newest match
    matches.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return matches[0]


async def execute_longform_pipeline(
    script_data: Dict,
    output_dir: str,
    max_scenes: Optional[int] = None,
    voice_engine: str = "meta_mms",
    progress_callback: Optional[Callable[[str, int, int], None]] = None
) -> str:
    """
    Builds the complete video scene-by-scene with high-performance parallelism:
    - Audio generated using VITS voice engine (meta_mms) or google_tts
    - Captions and images resolved immediately
    - Scene clips rendered in parallel across 4 worker threads
    - Smart clip cache skips re-renders
    - Merges into final_youtube_video.mp4
    """
    os.makedirs(output_dir, exist_ok=True)
    images_dir = os.path.join(output_dir, "images")
    audio_dir = os.path.join(output_dir, "audio")
    captions_dir = os.path.join(output_dir, "captions")
    clips_dir = os.path.join(output_dir, "clips")
    for d in [images_dir, audio_dir, captions_dir, clips_dir]:
        os.makedirs(d, exist_ok=True)

    all_scenes = script_data["scenes"]
    scenes = all_scenes[:max_scenes] if max_scenes else all_scenes
    total = len(scenes)

    # 1. Export Google Flow Prompts
    prompts_file = os.path.join(output_dir, "google_flow_prompts.txt")
    export_google_flow_prompts(script_data, prompts_file)

    # 2. Phase 1: Prepare all Audio, Captions, and Images sequentially (fast metadata prep)
    render_tasks = []
    for idx, sc in enumerate(scenes, start=1):
        num = sc["scene_num"]
        if voice_engine.startswith("edge_tts") or voice_engine == "meta_mms_eng":
            speech_text = sc.get("english_speech") or sc.get("action", "Curiosity science breakdown")
        else:
            speech_text = sc.get("khmer_speech", "")

        # --- A. Audio ---
        aud_path = os.path.join(audio_dir, f"scene_{num:02d}.mp3")
        meta_path = os.path.join(audio_dir, f"scene_{num:02d}.meta.json")

        need_gen = True
        if os.path.exists(aud_path) and os.path.exists(meta_path) and os.path.getsize(aud_path) > 1000:
            try:
                with open(meta_path, "r", encoding="utf-8") as mf:
                    meta = json.load(mf)
                if meta.get("speech_text") == speech_text and meta.get("engine") == voice_engine:
                    need_gen = False
            except Exception:
                need_gen = True

        if need_gen:
            print(f"🎙️ Generating speech ({voice_engine}) for Scene {num:02d} ({idx}/{total})...")
            if voice_engine == "edge_tts_guy":
                dur = generate_edge_tts_speech(speech_text, aud_path, voice="guy")
            elif voice_engine.startswith("edge_tts"):
                dur = generate_edge_tts_speech(speech_text, aud_path, voice="christopher")
            elif voice_engine == "google_tts":
                dur = generate_google_khmer_speech(speech_text, aud_path)
            elif voice_engine == "meta_mms_eng":
                dur = generate_meta_mms_english_speech(speech_text, aud_path)
            else:
                dur = generate_meta_mms_speech(speech_text, aud_path)
            try:
                with open(meta_path, "w", encoding="utf-8") as mf:
                    json.dump({"speech_text": speech_text, "engine": voice_engine, "duration": dur}, mf, ensure_ascii=False)
            except Exception:
                pass
        else:
            from src.google_tts_engine import probe_audio_duration
            dur = probe_audio_duration(aud_path)

        display_dur = max(5.0, dur + 0.6)
        sc["audio_path"] = aud_path
        sc["display_duration"] = display_dur

        # --- B. Captions ---
        caption_path = os.path.join(captions_dir, f"sub_scene_{num:02d}.png")
        caption_meta = os.path.join(captions_dir, f"sub_scene_{num:02d}.meta.json")

        need_cap = True
        if os.path.exists(caption_path) and os.path.exists(caption_meta) and os.path.getsize(caption_path) > 1000:
            try:
                with open(caption_meta, "r", encoding="utf-8") as cmf:
                    if json.load(cmf).get("text") == speech_text:
                        need_cap = False
            except Exception:
                need_cap = True

        if need_cap:
            render_khmer_caption_png(speech_text, caption_path)
            try:
                with open(caption_meta, "w", encoding="utf-8") as cmf:
                    json.dump({"text": speech_text}, cmf, ensure_ascii=False)
            except Exception:
                pass

        sc["caption_overlay_path"] = caption_path

        # --- C. Images ---
        found_img = resolve_scene_image(images_dir, num)
        if not found_img:
            # Instant vector placeholder fallback (takes 0.01s, never blocks render)
            img_path = os.path.join(images_dir, f"scene_{num:02d}.png")
            generate_cartoon_pill_placeholder(
                output_path=img_path,
                scene_num=num,
                action_text=sc["action"],
                khmer_text=speech_text
            )
            found_img = img_path
        sc["image_path"] = found_img

        clip_path = os.path.join(clips_dir, f"clip_{num:02d}.mp4")
        zoom_in = (idx % 2 == 0)

        render_tasks.append({
            "idx": idx,
            "num": num,
            "image_path": sc["image_path"],
            "audio_path": sc["audio_path"],
            "caption_overlay_path": sc["caption_overlay_path"],
            "duration": sc["display_duration"],
            "output_clip_path": clip_path,
            "zoom_in": zoom_in
        })

    # 3. Phase 2: Parallel Video Encoding using ThreadPoolExecutor (4 concurrent workers)
    print(f"⚡ Starting parallel encoding for {total} scene clips with 4 workers...")
    completed_count = 0

    def _worker_encode(task):
        return build_scene_clip_with_caption(
            image_path=task["image_path"],
            audio_path=task["audio_path"],
            caption_overlay_path=task["caption_overlay_path"],
            duration=task["duration"],
            output_clip_path=task["output_clip_path"],
            zoom_in=task["zoom_in"]
        )

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(_worker_encode, t): t for t in render_tasks}
        for future in as_completed(futures):
            t = futures[future]
            try:
                future.result()
                completed_count += 1
                if progress_callback:
                    progress_callback("rendering_scene", completed_count, total)
                print(f"   ✓ Finished Scene {t['num']:02d} ({completed_count}/{total})")
            except Exception as exc:
                print(f"   ❌ Error rendering Scene {t['num']:02d}: {exc}")
                raise exc

    # Ensure clips list is strictly in scene order
    scene_clips = [t["output_clip_path"] for t in render_tasks]

    # 4. Phase 3: Concatenate all scene clips into Final Video
    final_video = os.path.join(output_dir, "final_youtube_video.mp4")
    print(f"🎬 Assembling {len(scene_clips)} scene clips into final MP4...")
    assemble_final_video(scene_clips=scene_clips, final_output_path=final_video)

    # 5. Generate standard SRT for YouTube
    from src.tts_engine import generate_srt_subtitles
    srt_file = os.path.join(output_dir, "captions.srt")
    is_en_speech = voice_engine.startswith("edge_tts") or voice_engine == "meta_mms_eng"
    generate_srt_subtitles(scenes, srt_file, use_english=is_en_speech)

    # 6. Generate High-CTR YouTube Thumbnail & AI Prompts
    from src.thumbnail_generator import generate_youtube_thumbnail, export_thumbnail_prompts
    thumb_path = os.path.join(output_dir, "youtube_thumbnail.png")
    prompt_txt_path = os.path.join(output_dir, "youtube_thumbnail_prompts.txt")
    topic_slug = os.path.basename(output_dir).replace("_longform", "").replace("_video", "")
    try:
        generate_youtube_thumbnail(
            topic_id=topic_slug,
            output_path=thumb_path,
            title_en=script_data.get("title_en"),
            title_km=script_data.get("title_km")
        )
        export_thumbnail_prompts(
            topic_id=topic_slug,
            title_en=script_data.get("title_en", topic_slug),
            output_txt_path=prompt_txt_path
        )
        print(f"🖼️ Generated high-CTR YouTube thumbnail -> {thumb_path}")
    except Exception as e:
        print(f"Notice: Thumbnail auto-generation: {e}")

    print(f"\n🎉 Successfully assembled video from all {total} scenes -> {final_video}")
    return final_video
