"""
Video Builder Engine using FFmpeg (High-Performance Parallel Edition).
Combines frame-by-frame images, smooth Ken Burns zoom/motion,
Khmer audio narration, and pixel-perfect Chromium-rendered Khmer subtitles.
Optimized for multi-core parallelism and smart clip caching.
"""

import os
import subprocess
from typing import List, Dict
import imageio_ffmpeg


def get_ffmpeg_path() -> str:
    return imageio_ffmpeg.get_ffmpeg_exe()


def is_clip_up_to_date(output_clip_path: str, inputs: List[str]) -> bool:
    """Checks if a previously rendered clip is already up-to-date with its inputs."""
    if not os.path.exists(output_clip_path) or os.path.getsize(output_clip_path) < 20000:
        return False
    clip_mtime = os.path.getmtime(output_clip_path)
    for inp in inputs:
        if inp and os.path.exists(inp) and os.path.getmtime(inp) > clip_mtime:
            return False
    return True


def build_scene_clip_with_caption(
    image_path: str,
    audio_path: str,
    caption_overlay_path: str,
    duration: float,
    output_clip_path: str,
    zoom_in: bool = True,
    force_rebuild: bool = False
) -> str:
    """
    Renders an individual scene clip with:
    1. Base image with smooth Ken Burns zoom motion (24fps cinema speed)
    2. Transparent Khmer caption overlay
    3. Synchronized Khmer narration audio
    """
    # Check cache: if clip exists and inputs haven't changed, skip re-render
    if not force_rebuild and is_clip_up_to_date(output_clip_path, [image_path, audio_path, caption_overlay_path]):
        return output_clip_path

    ffmpeg = get_ffmpeg_path()
    os.makedirs(os.path.dirname(os.path.abspath(output_clip_path)), exist_ok=True)

    fps = 24
    total_frames = int(duration * fps)

    # Ken Burns slow zoom (optimized 24fps)
    if zoom_in:
        zoom_filter = (
            f"zoompan=z='min(zoom+0.0008,1.12)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={fps}"
        )
    else:
        zoom_filter = (
            f"zoompan=z='if(lte(zoom,1.0),1.12,max(1.001,zoom-0.0008))':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={fps}"
        )

    # High-performance bilinear scale + crop before zoompan
    bg_filter = f"scale=1920:1080:force_original_aspect_ratio=increase:flags=bilinear,crop=1920:1080,{zoom_filter}"

    # Complex filter:
    # [0:v] is base image -> [bg]
    # [2:v] is caption overlay PNG -> overlaid on top of [bg] -> [v]
    # [1:a] is audio -> apad to match duration -> [a]
    filter_complex = (
        f"[0:v]{bg_filter}[bg];"
        f"[bg][2:v]overlay=0:0:format=auto[v];"
        f"[1:a]apad=whole_dur={duration:.3f}[a]"
    )

    cmd = [
        ffmpeg, "-y",
        "-threads", "2",
        "-loop", "1", "-t", f"{duration:.3f}", "-i", image_path,
        "-i", audio_path,
        "-loop", "1", "-t", f"{duration:.3f}", "-i", caption_overlay_path,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{duration:.3f}",
        output_clip_path
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg failed building scene {output_clip_path}:\n{res.stderr}")

    return output_clip_path


def assemble_final_video(
    scene_clips: List[str],
    final_output_path: str
):
    """
    Concatenates all scene clips together into the final ready-to-upload YouTube MP4.
    """
    ffmpeg = get_ffmpeg_path()
    os.makedirs(os.path.dirname(os.path.abspath(final_output_path)), exist_ok=True)

    concat_txt_path = os.path.join(os.path.dirname(final_output_path), "concat_list.txt")
    with open(concat_txt_path, "w", encoding="utf-8") as f:
        for clip in scene_clips:
            norm_path = os.path.abspath(clip).replace("\\", "/")
            f.write(f"file '{norm_path}'\n")

    cmd_concat = [
        ffmpeg, "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt_path,
        "-c", "copy",
        final_output_path
    ]
    res_concat = subprocess.run(cmd_concat, capture_output=True, text=True)
    if res_concat.returncode != 0:
        raise RuntimeError(f"FFmpeg concat failed:\n{res_concat.stderr}")

    if os.path.exists(concat_txt_path):
        os.remove(concat_txt_path)

    return final_output_path
