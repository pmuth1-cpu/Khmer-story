"""
Image Helper for Human Cartoon with Pill Body Design.
Generates 2D flat vector human cartoon characters with pill-shaped body silhouettes
wearing modern clothes, with expressive human facial features and hair (NOT a medicine pill).
"""

import os
from typing import List, Dict
from PIL import Image, ImageDraw, ImageFont


def export_prompts_file(scenes: List[Dict], output_file: str, topic_title: str = ""):
    """
    Exports clean prompts formatted for Google Flow or Nano Banana.
    """
    from src.prompt_generator import create_scene_prompt

    lines = []
    lines.append(f"# Google Flow & Nano Banana Prompts: {topic_title}")
    lines.append("# Character Design: Human cartoon character with a cute pill/capsule-shaped body silhouette")
    lines.append("# (Human face, stylized hair, wearing casual human clothing - NOT a medicine capsule)\n")
    lines.append("=" * 75 + "\n")

    for sc in scenes:
        prompt = create_scene_prompt(
            scene_action=sc["action"],
            environment=sc["environment"],
            character_emotion=sc.get("emotion", "curious")
        )
        lines.append(f"### Scene {sc['scene_num']} ({sc.get('duration_hint', 7.5)}s)")
        lines.append(f"Khmer Speech: {sc['khmer_speech']}")
        lines.append("Prompt:")
        lines.append(prompt)
        lines.append("\n" + "-" * 75 + "\n")

    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def generate_cartoon_pill_placeholder(
    output_path: str,
    scene_num: int,
    action_text: str,
    khmer_text: str,
    width: int = 1920,
    height: int = 1080
):
    """
    Generates a high-resolution 2D flat vector human cartoon character
    with a pill-shaped body silhouette, wearing human clothing (hoodie, pants, shoes),
    with human hair and expressive face.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # 1. Background palette (Curiosity / Nature / Weather)
    palette_bg = [
        ((35, 115, 215), (75, 180, 245)),   # Scene 1: Day sky
        ((25, 45, 95), (65, 85, 140)),      # Scene 2: Rain / Storm
        ((15, 25, 55), (45, 60, 95)),       # Scene 3: Deep city flood
        ((65, 45, 30), (135, 85, 45)),      # Scene 4: Earth / Mud
        ((35, 160, 120), (95, 225, 175)),   # Scene 5: Fresh green
    ]
    bg_start, bg_end = palette_bg[(scene_num - 1) % len(palette_bg)]

    im = Image.new("RGBA", (width, height), bg_start)
    draw = ImageDraw.Draw(im)

    # Linear gradient background
    for y in range(height):
        r = int(bg_start[0] + (bg_end[0] - bg_start[0]) * (y / height))
        g = int(bg_start[1] + (bg_end[1] - bg_start[1]) * (y / height))
        b = int(bg_start[2] + (bg_end[2] - bg_start[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # Rolling Hill ground
    ground_color = (235, 245, 255) if "ice" in action_text.lower() else (45, 160, 95)
    draw.ellipse([(-200, height - 340), (width + 200, height + 420)], fill=ground_color)

    # Character Dimensions: Pill-shaped human cartoon body
    cx = width // 2
    cy = height // 2 + 10
    pw = 250   # pill body width
    ph = 430   # pill body height
    r = pw // 2

    # Drop Shadow
    draw.ellipse([(cx - 150, cy + ph // 2 + 45), (cx + 150, cy + ph // 2 + 95)], fill=(0, 0, 0, 50))

    # Legs & Shoes
    leg_w = 42
    leg_len = 65
    shoe_h = 32
    # Left Leg & Shoe (Sneaker)
    draw.rectangle([cx - 75, cy + ph // 2 - 20, cx - 75 + leg_w, cy + ph // 2 + leg_len], fill=(30, 41, 59), outline=(15, 23, 42), width=5)
    draw.rounded_rectangle([cx - 95, cy + ph // 2 + leg_len, cx - 25, cy + ph // 2 + leg_len + shoe_h], radius=15, fill=(245, 245, 250), outline=(15, 23, 42), width=5)
    # Right Leg & Shoe
    draw.rectangle([cx + 75 - leg_w, cy + ph // 2 - 20, cx + 75, cy + ph // 2 + leg_len], fill=(30, 41, 59), outline=(15, 23, 42), width=5)
    draw.rounded_rectangle([cx + 25, cy + ph // 2 + leg_len, cx + 95, cy + ph // 2 + leg_len + shoe_h], radius=15, fill=(245, 245, 250), outline=(15, 23, 42), width=5)

    # Pill Body Shape: Base warm human skin tone
    skin_color = (255, 219, 186)  # Warm peach skin tone
    pill_box = [cx - pw // 2, cy - ph // 2, cx + pw // 2, cy + ph // 2]
    draw.rounded_rectangle(pill_box, radius=r, fill=skin_color, outline=(30, 30, 35), width=7)

    # Clothing: Modern Colorful Hoodie on the lower 60% of the pill body
    hoodie_color = (245, 158, 11)   # Vibrant amber/orange hoodie
    hoodie_top_y = cy - 25
    
    # Draw hoodie body over the pill shape
    draw.pieslice([cx - pw // 2, cy + ph // 2 - 2 * r, cx + pw // 2, cy + ph // 2], 0, 180, fill=hoodie_color)
    draw.rectangle([cx - pw // 2, hoodie_top_y, cx + pw // 2, cy + ph // 2 - r], fill=hoodie_color)
    draw.rounded_rectangle(pill_box, radius=r, outline=(30, 30, 35), width=7)

    # Hoodie collar / V-neck
    draw.polygon([(cx - 35, hoodie_top_y), (cx + 35, hoodie_top_y), (cx, hoodie_top_y + 35)], fill=(217, 119, 6), outline=(30, 30, 35), width=4)
    # Hoodie kangaroo pocket
    pocket_box = [cx - 65, cy + 95, cx + 65, cy + 160]
    draw.rounded_rectangle(pocket_box, radius=16, fill=(217, 119, 6), outline=(30, 30, 35), width=4)

    # Cartoon Human Hair (Top of head)
    hair_color = (60, 35, 20)  # Dark brown cartoon hair
    # Hair cap with bangs tufts
    draw.pieslice([cx - pw // 2 - 8, cy - ph // 2 - 12, cx + pw // 2 + 8, cy - ph // 2 + 150], 180, 360, fill=hair_color)
    # Hair side tufts
    draw.polygon([(cx - 95, cy - ph // 2 + 65), (cx - 75, cy - ph // 2 + 95), (cx - 60, cy - ph // 2 + 65)], fill=hair_color)
    draw.polygon([(cx + 95, cy - ph // 2 + 65), (cx + 75, cy - ph // 2 + 95), (cx + 60, cy - ph // 2 + 65)], fill=hair_color)
    # Cute hair swirl on top
    draw.arc([(cx - 15, cy - ph // 2 - 35), (cx + 35, cy - ph // 2 + 5)], 170, 350, fill=hair_color, width=12)

    # Expressive Cartoon Human Face
    eye_y = cy - 85
    eye_spacing = 45
    eye_radius = 28

    # Eyebrows
    draw.arc([(cx - eye_spacing - 25, eye_y - 40), (cx - eye_spacing + 25, eye_y - 20)], 190, 350, fill=(45, 25, 15), width=6)
    draw.arc([(cx + eye_spacing - 25, eye_y - 40), (cx + eye_spacing + 25, eye_y - 20)], 190, 350, fill=(45, 25, 15), width=6)

    # Big Cartoon Eyes
    draw.ellipse([(cx - eye_spacing - eye_radius, eye_y - eye_radius), (cx - eye_spacing + eye_radius, eye_y + eye_radius)], fill=(255, 255, 255), outline=(30, 30, 35), width=5)
    draw.ellipse([(cx + eye_spacing - eye_radius, eye_y - eye_radius), (cx + eye_spacing + eye_radius, eye_y + eye_radius)], fill=(255, 255, 255), outline=(30, 30, 35), width=5)

    # Pupils
    pupil_r = 15
    draw.ellipse([(cx - eye_spacing - pupil_r + 3, eye_y - pupil_r), (cx - eye_spacing + pupil_r + 3, eye_y + pupil_r)], fill=(30, 30, 40))
    draw.ellipse([(cx + eye_spacing - pupil_r + 3, eye_y - pupil_r), (cx + eye_spacing + pupil_r + 3, eye_y + pupil_r)], fill=(30, 30, 40))
    # Eye sparkle reflections
    draw.ellipse([(cx - eye_spacing, eye_y - 7), (cx - eye_spacing + 7, eye_y)], fill=(255, 255, 255))
    draw.ellipse([(cx + eye_spacing, eye_y - 7), (cx + eye_spacing + 7, eye_y)], fill=(255, 255, 255))

    # Cute blush cheeks
    draw.ellipse([(cx - 78, eye_y + 12), (cx - 52, eye_y + 30)], fill=(255, 140, 160, 150))
    draw.ellipse([(cx + 52, eye_y + 12), (cx + 78, eye_y + 30)], fill=(255, 140, 160, 150))

    # Smiling cartoon mouth
    draw.arc([(cx - 26, eye_y + 15), (cx + 26, eye_y + 55)], 0, 180, fill=(40, 25, 20), width=6)

    # Cartoon Arms & Sleeves
    # Left Arm
    draw.line([(cx - pw // 2 + 10, hoodie_top_y + 35), (cx - pw // 2 - 45, hoodie_top_y + 90)], fill=hoodie_color, width=28)
    draw.ellipse([(cx - pw // 2 - 58, hoodie_top_y + 80), (cx - pw // 2 - 32, hoodie_top_y + 106)], fill=skin_color, outline=(30, 30, 35), width=4)
    # Right Arm waving
    draw.line([(cx + pw // 2 - 10, hoodie_top_y + 35), (cx + pw // 2 + 45, hoodie_top_y - 15)], fill=hoodie_color, width=28)
    draw.ellipse([(cx + pw // 2 + 35, hoodie_top_y - 30), (cx + pw // 2 + 65, hoodie_top_y)], fill=skin_color, outline=(30, 30, 35), width=4)

    # Header Badge: Scene tag
    badge_box = [cx - 260, 60, cx + 260, 130]
    draw.rounded_rectangle(badge_box, radius=25, fill=(15, 23, 42, 210), outline=(245, 158, 11), width=3)

    font_path = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "KantumruyPro.ttf")
    try:
        badge_font = ImageFont.truetype(font_path, 32)
    except Exception:
        badge_font = ImageFont.load_default()

    scene_title = f"SCENE {scene_num:02d} • HUMAN PILL CARTOON"
    draw.text((cx, 95), scene_title, font=badge_font, fill=(255, 215, 0), anchor="mm")

    im.convert("RGB").save(output_path, "PNG")
