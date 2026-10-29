"""
100% Always Free AI Image Generator using FLUX / Pollinations.
Requires ZERO API keys, ZERO account setup, unlimited and always free.
Produces high quality 2D vector / Kurzgesagt / Human Pill Cartoon images.
"""

import os
import time
import urllib.parse
import urllib.request
from typing import List, Dict, Optional
from PIL import Image

FREE_FLUX_STYLE_PROMPT = (
    "Cute stylized human cartoon character with a pill-shaped capsule body design, "
    "smooth rounded silhouette, friendly expressive face, big round cartoon eyes, "
    "stylish hair, wearing casual modern clothes (hoodie, jeans, sneakers), "
    "Kurzgesagt 2D flat vector aesthetic, clean bold outlines, vibrant saturated colors, "
    "educational animation still, 16:9 aspect ratio."
)


def generate_free_flux_image(
    action: str,
    environment: str,
    output_path: str,
    emotion: str = "curious",
    width: int = 1280,
    height: int = 720
) -> bool:
    """
    Generates a real AI image via Pollinations FLUX engine with ZERO API key.
    Always free, unlimited.
    """
    full_prompt = (
        f"{FREE_FLUX_STYLE_PROMPT} "
        f"The human cartoon pill character is {emotion}, {action}. "
        f"Environment: {environment}. "
        f"Vivid colorful vector illustration, clean lines."
    )

    encoded_prompt = urllib.parse.quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true&seed={int(time.time() * 1000) % 999999}"

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )

    try:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with urllib.request.urlopen(req, timeout=40) as res:
            if res.status == 200:
                with open(output_path, "wb") as f:
                    f.write(res.read())
                return True
    except Exception as e:
        print(f"[Notice] Free Flux AI generation notice: {e}")
        return False

    return False


def batch_generate_flux_scenes(scenes: List[Dict], images_dir: str) -> int:
    """
    Automatically generates real Flux AI images for all scenes in a script.
    """
    os.makedirs(images_dir, exist_ok=True)
    generated = 0
    for sc in scenes:
        num = sc["scene_num"]
        out_path = os.path.join(images_dir, f"scene_{num:02d}.png")
        if not os.path.exists(out_path):
            ok = generate_free_flux_image(
                action=sc["action"],
                environment=sc["environment"],
                output_path=out_path,
                emotion=sc.get("emotion", "curious")
            )
            if ok:
                generated += 1
                time.sleep(0.5)  # slight pause between free requests
        else:
            generated += 1
    return generated
