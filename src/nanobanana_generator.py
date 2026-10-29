"""
Nano Banana / Google Flow Image Generator.
Character Definition: A cute stylized human cartoon character with a pill-shaped capsule body design,
human facial features, styled hair, and casual clothes (NOT a medicine capsule).
"""

import os
from typing import Optional, List, Dict
from io import BytesIO
from PIL import Image

NANO_BANANA_HUMAN_PILL_CORE = (
    "Cute stylized human cartoon character designed with a minimalist pill-shaped capsule body silhouette, "
    "smooth rounded pill body proportions, expressive friendly human face, big round cartoon eyes, "
    "stylish cartoon hair, wearing modern casual clothes (colorful hoodie or t-shirt with pants and sneakers), "
    "Kurzgesagt and modern infographic 2D flat vector aesthetic, clean bold outlines, vibrant saturated colors, "
    "charming educational storytelling character, 4k digital vector art, 16:9 widescreen ratio."
)


def build_nanobanana_prompt(action: str, environment: str, emotion: str = "curious") -> str:
    """
    Constructs an optimized prompt for Google Flow / Nano Banana / Imagen.
    """
    return (
        f"{NANO_BANANA_HUMAN_PILL_CORE} "
        f"The human cartoon pill character is {emotion}, {action}. "
        f"Setting environment: {environment}. "
        f"Cinematic soft lighting, colorful educational scene, highly detailed vector animation still."
    )


def generate_nanobanana_image(
    prompt: str,
    output_path: str,
    api_key: Optional[str] = None,
    aspect_ratio: str = "16:9"
) -> bool:
    """
    Calls Google GenAI (Imagen 3 / Nano Banana) to generate the human cartoon pill character image.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        return False

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=key)

        try:
            result = client.models.generate_images(
                model='imagen-3.0-generate-002',
                prompt=prompt,
                config=dict(
                    number_of_images=1,
                    aspect_ratio=aspect_ratio,
                    person_generation="ALLOW_ADULT",
                )
            )
            if result.generated_images:
                img_bytes = result.generated_images[0].image.image_bytes
                img = Image.open(BytesIO(img_bytes))
                os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
                img.save(output_path, "PNG")
                return True
        except Exception:
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['IMAGE', 'TEXT']
                )
            )
            for part in response.candidates[0].content.parts:
                if getattr(part, 'inline_data', None):
                    img = Image.open(BytesIO(part.inline_data.data))
                    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
                    img.save(output_path, "PNG")
                    return True

    except Exception as e:
        print(f"[Warning] Image generation failed: {e}")
        return False

    return False


def batch_generate_scenes(
    scenes: List[Dict],
    images_dir: str,
    api_key: Optional[str] = None
) -> Dict[int, bool]:
    os.makedirs(images_dir, exist_ok=True)
    results = {}
    for sc in scenes:
        num = sc["scene_num"]
        out_path = os.path.join(images_dir, f"scene_{num:02d}.png")
        prompt = build_nanobanana_prompt(
            action=sc["action"],
            environment=sc["environment"],
            emotion=sc.get("emotion", "curious")
        )
        success = generate_nanobanana_image(prompt, out_path, api_key=api_key)
        results[num] = success
    return results
