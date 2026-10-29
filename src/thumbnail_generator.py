"""
YouTube Thumbnail Generator for Curiosity Cartoon Suite.
Produces high-CTR (Click-Through-Rate) 16:9 (1280x720) YouTube Thumbnails
in vibrant Kurzgesagt 2D vector style with expressive Human Pill characters,
dramatic atmospheric phenomena, high-contrast badges, and AI prompt exports.
"""

import os
import math
from typing import Dict, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont


TOPIC_THEMES = {
    "oxygen_double": {
        "badge_en": "OXYGEN x2?!",
        "badge_km": "អុកស៊ីសែន x២?!",
        "bg_top": (10, 35, 30),
        "bg_bottom": (15, 85, 70),
        "accent": (0, 240, 180),
        "secondary": (255, 90, 50),
        "headline": "EARTH OVERDOSED!",
        "subject": "GIANT INSECTS & HYPER FIRE"
    },
    "rain_for_month": {
        "badge_en": "30 DAYS NON-STOP?!",
        "badge_km": "ភ្លៀង ៣០ ថ្ងៃ?!",
        "bg_top": (8, 18, 38),
        "bg_bottom": (20, 55, 110),
        "accent": (56, 189, 248),
        "secondary": (250, 204, 21),
        "headline": "TOTAL FLOOD!",
        "subject": "THE SINKING METROPOLIS"
    },
    "sun_disappears": {
        "badge_en": "SUN VANISHED?!",
        "badge_km": "ព្រះអាទិត្យបាត់?!",
        "bg_top": (6, 6, 18),
        "bg_bottom": (35, 15, 60),
        "accent": (245, 158, 11),
        "secondary": (59, 130, 246),
        "headline": "DEEP FREEZE -70°C",
        "subject": "SURVIVING IN TOTAL DARK"
    },
    "ocean_empty": {
        "badge_en": "OCEANS VANISHED?!",
        "badge_km": "សមុទ្ររីងស្ងួត?!",
        "bg_top": (40, 25, 15),
        "bg_bottom": (120, 60, 25),
        "accent": (251, 146, 60),
        "secondary": (14, 165, 233),
        "headline": "DESERT PLANET",
        "subject": "THE LOST TRENCHES"
    },
    "no_sleep": {
        "badge_en": "10 DAYS NO SLEEP?!",
        "badge_km": "មិនគេង ១០ ថ្ងៃ?!",
        "bg_top": (25, 10, 35),
        "bg_bottom": (75, 20, 95),
        "accent": (236, 72, 153),
        "secondary": (234, 179, 8),
        "headline": "BRAIN OVERLOAD!",
        "subject": "THE HALLUCINATION SHIFT"
    },
    "no_gravity": {
        "badge_en": "NO GRAVITY FOR 5s?!",
        "badge_km": "គ្មានទំនាញ ៥ វិនាទី?!",
        "bg_top": (10, 15, 45),
        "bg_bottom": (40, 80, 160),
        "accent": (168, 85, 247),
        "secondary": (239, 68, 68),
        "headline": "EVERYTHING FLIES!",
        "subject": "THE FIVE-SECOND CHAOS"
    }
}


def get_font(size: int, is_bold: bool = True) -> ImageFont.ImageFont:
    candidate_fonts = [
        "C:/Windows/Fonts/impact.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/seguisb.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/KantumruyPro-Bold.ttf"
    ]
    for font_path in candidate_fonts:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def generate_youtube_thumbnail(
    topic_id: str,
    output_path: str,
    title_en: Optional[str] = None,
    title_km: Optional[str] = None,
    width: int = 1280,
    height: int = 720
) -> str:
    """
    Renders a stunning 16:9 YouTube Thumbnail optimized for maximum CTR.
    Features:
    - Glowing dramatic dual-gradient background with cosmic/phenomenon textures
    - Giant glowing planet / atmospheric phenomenon
    - Expressive human pill character with shocked reaction, drop shadow, and clean vector art
    - High-visibility Curiosity Badge (e.g. '30 DAYS NON-STOP?!', 'OXYGEN x2?!')
    - 3D layered drop-shadowed typography
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    theme = TOPIC_THEMES.get(topic_id, {
        "badge_en": "WHAT IF?!",
        "badge_km": "ចុះបើ?!",
        "bg_top": (15, 23, 42),
        "bg_bottom": (30, 58, 138),
        "accent": (245, 158, 11),
        "secondary": (56, 189, 248),
        "headline": "THE SHOCKING TRUTH",
        "subject": "SCIENTIFIC BREAKDOWN"
    })

    im = Image.new("RGBA", (width, height), theme["bg_top"])
    draw = ImageDraw.Draw(im)

    # 1. High-contrast vertical gradient background
    c_top = theme["bg_top"]
    c_bot = theme["bg_bottom"]
    for y in range(height):
        ratio = y / height
        r = int(c_top[0] + (c_bot[0] - c_top[0]) * ratio)
        g = int(c_top[1] + (c_bot[1] - c_top[1]) * ratio)
        b = int(c_top[2] + (c_bot[2] - c_top[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # 2. Glowing celestial body / phenomenon on the right
    planet_cx = int(width * 0.72)
    planet_cy = int(height * 0.45)
    planet_r = 230

    # Glow rings
    glow_color = theme["accent"]
    for gr in range(planet_r + 80, planet_r, -10):
        alpha = int(45 * (1 - (gr - planet_r) / 80))
        glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)
        glow_draw.ellipse(
            [(planet_cx - gr, planet_cy - gr), (planet_cx + gr, planet_cy + gr)],
            fill=(glow_color[0], glow_color[1], glow_color[2], alpha)
        )
        im = Image.alpha_composite(im, glow_layer)
        draw = ImageDraw.Draw(im)

    # Planet base
    draw.ellipse(
        [(planet_cx - planet_r, planet_cy - planet_r), (planet_cx + planet_r, planet_cy + planet_r)],
        fill=(25, 40, 75, 255),
        outline=theme["accent"],
        width=6
    )

    # Topic-specific visual flourishes inside/around planet
    if "rain" in topic_id:
        # Rain streaks & lightning
        for lx in range(planet_cx - 150, planet_cx + 150, 30):
            draw.line([(lx, planet_cy - 120), (lx - 40, planet_cy + 140)], fill=(120, 210, 255, 180), width=4)
        # Giant stylized lightning bolt
        bolt = [
            (planet_cx + 20, planet_cy - 180),
            (planet_cx - 30, planet_cy - 20),
            (planet_cx + 10, planet_cy - 10),
            (planet_cx - 50, planet_cy + 170)
        ]
        draw.line(bolt, fill=(255, 240, 100, 255), width=8)
    elif "oxygen" in topic_id:
        # Glowing green energy vortex & giant insect silhouette
        for ir in range(40, 190, 35):
            draw.ellipse(
                [(planet_cx - ir, planet_cy - ir), (planet_cx + ir, planet_cy + ir)],
                outline=(0, 255, 180, 160),
                width=3
            )
        # Glowing oxygen atom markers (O2)
        draw.ellipse([(planet_cx - 60, planet_cy - 40), (planet_cx + 10, planet_cy + 30)], fill=(0, 255, 200, 220))
        draw.ellipse([(planet_cx - 10, planet_cy - 30), (planet_cx + 60, planet_cy + 40)], fill=(0, 220, 180, 220))
    elif "sun" in topic_id:
        # Eclipsed dark core with bright coronal flares
        draw.ellipse(
            [(planet_cx - planet_r + 15, planet_cy - planet_r + 15), (planet_cx + planet_r - 15, planet_cy + planet_r - 15)],
            fill=(5, 5, 15, 255)
        )
        draw.arc(
            [(planet_cx - planet_r, planet_cy - planet_r), (planet_cx + planet_r, planet_cy + planet_r)],
            start=200, end=340, fill=(255, 200, 50, 255), width=10
        )

    # 3. Dramatic ground silhouette
    ground_color = (15, 23, 42, 255)
    draw.ellipse([(-100, height - 160), (width + 100, height + 300)], fill=ground_color)

    # 4. Human Pill Cartoon Character on the Left (Kurzgesagt aesthetic)
    char_cx = int(width * 0.28)
    char_cy = int(height * 0.62)
    pw = 190   # pill body width
    ph = 330   # pill body height
    r = pw // 2

    # Drop shadow under character
    draw.ellipse([(char_cx - 130, char_cy + ph // 2 + 10), (char_cx + 130, char_cy + ph // 2 + 45)], fill=(0, 0, 0, 110))

    # Sneaker shoes & legs
    draw.rectangle([char_cx - 55, char_cy + ph // 2 - 20, char_cx - 20, char_cy + ph // 2 + 45], fill=(30, 41, 59), outline=(15, 23, 42), width=4)
    draw.rounded_rectangle([char_cx - 75, char_cy + ph // 2 + 40, char_cx - 15, char_cy + ph // 2 + 68], radius=12, fill=(245, 245, 250), outline=(15, 23, 42), width=4)

    draw.rectangle([char_cx + 20, char_cy + ph // 2 - 20, char_cx + 55, char_cy + ph // 2 + 45], fill=(30, 41, 59), outline=(15, 23, 42), width=4)
    draw.rounded_rectangle([char_cx + 15, char_cy + ph // 2 + 40, char_cx + 75, char_cy + ph // 2 + 68], radius=12, fill=(245, 245, 250), outline=(15, 23, 42), width=4)

    # Pill Capsule Body (Skin tone top half, hoodie bottom half)
    pill_box = [char_cx - r, char_cy - ph // 2, char_cx + r, char_cy + ph // 2]
    # Outline & Skin
    draw.rounded_rectangle(pill_box, radius=r, fill=(255, 219, 186), outline=(15, 23, 42), width=6)

    # Casual Hoodie (Bottom half of pill)
    hoodie_top = char_cy - 10
    draw.chord([char_cx - r, char_cy + ph // 2 - 2 * r, char_cx + r, char_cy + ph // 2], start=0, end=180, fill=(239, 68, 68), outline=(15, 23, 42), width=5)
    draw.rectangle([char_cx - r + 3, hoodie_top, char_cx + r - 3, char_cy + ph // 2 - r + 1], fill=(239, 68, 68))
    # Hoodie zipper & cords
    draw.line([(char_cx, hoodie_top), (char_cx, char_cy + ph // 2 - 10)], fill=(220, 38, 38), width=3)
    draw.line([(char_cx - 15, hoodie_top + 10), (char_cx - 15, hoodie_top + 50)], fill=(255, 255, 255), width=3)
    draw.line([(char_cx + 15, hoodie_top + 10), (char_cx + 15, hoodie_top + 50)], fill=(255, 255, 255), width=3)

    # Stylized Hair (Kurzgesagt modern swoosh)
    hair_box = [char_cx - r - 6, char_cy - ph // 2 - 12, char_cx + r + 6, char_cy - ph // 2 + 75]
    draw.pieslice(hair_box, start=180, end=360, fill=(45, 30, 20), outline=(15, 23, 42), width=5)
    draw.chord([char_cx - r - 4, char_cy - ph // 2 + 10, char_cx + 15, char_cy - ph // 2 + 70], start=160, end=350, fill=(45, 30, 20))

    # Shocked / Curious Face: HUGE animated eyes
    eye_y = char_cy - 70
    eye_r = 30
    # Left Eye
    draw.ellipse([(char_cx - 45 - eye_r, eye_y - eye_r), (char_cx - 45 + eye_r, eye_y + eye_r)], fill=(255, 255, 255), outline=(15, 23, 42), width=5)
    draw.ellipse([(char_cx - 40, eye_y - 12), (char_cx - 22, eye_y + 12)], fill=(15, 23, 42))
    draw.ellipse([(char_cx - 36, eye_y - 8), (char_cx - 28, eye_y)], fill=(255, 255, 255)) # sparkle
    # Right Eye
    draw.ellipse([(char_cx + 45 - eye_r, eye_y - eye_r), (char_cx + 45 + eye_r, eye_y + eye_r)], fill=(255, 255, 255), outline=(15, 23, 42), width=5)
    draw.ellipse([(char_cx + 50, eye_y - 12), (char_cx + 68, eye_y + 12)], fill=(15, 23, 42))
    draw.ellipse([(char_cx + 54, eye_y - 8), (char_cx + 62, eye_y)], fill=(255, 255, 255)) # sparkle

    # Wide-open shocked mouth
    mouth_box = [char_cx - 18, char_cy - 22, char_cx + 22, char_cy + 22]
    draw.ellipse(mouth_box, fill=(185, 28, 28), outline=(15, 23, 42), width=4)
    # Cute little tongue
    draw.chord([char_cx - 12, char_cy + 2, char_cx + 16, char_cy + 20], start=0, end=180, fill=(251, 113, 133))

    # Sweat drop of shock
    draw.ellipse([(char_cx + r - 8, eye_y - 30), (char_cx + r + 14, eye_y - 4)], fill=(56, 189, 248), outline=(15, 23, 42), width=2)

    # Expressive raised cartoon hands (gesturing dramatically at planet)
    # Right hand pointing forward
    draw.rounded_rectangle([char_cx + r - 15, char_cy + 15, char_cx + r + 55, char_cy + 45], radius=15, fill=(255, 219, 186), outline=(15, 23, 42), width=4)
    # Left hand up near head
    draw.rounded_rectangle([char_cx - r - 45, char_cy - 40, char_cx - r + 15, char_cy - 10], radius=15, fill=(255, 219, 186), outline=(15, 23, 42), width=4)

    # 5. Top Curiosity Badge Banner (High-CTR Angled Pill Ribbon)
    badge_text = theme.get("badge_en", "WHAT IF?!")
    badge_font = get_font(52, is_bold=True)

    bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    bx = 60
    by = 50
    bw = tw + 60
    bh = th + 28

    # Badge 3D shadow
    draw.rounded_rectangle([bx + 8, by + 8, bx + bw + 8, by + bh + 8], radius=20, fill=(0, 0, 0, 160))
    # Badge background (vibrant accent color)
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=20, fill=theme["secondary"], outline=(255, 255, 255), width=5)
    # Badge text
    draw.text((bx + 30, by + 12), badge_text, fill=(15, 23, 42), font=badge_font)

    # 6. Secondary Headline Banner (e.g. "EARTH OVERDOSED!", "30 DAYS DELUGE")
    headline_text = theme.get("headline", "WHAT IF?")
    head_font = get_font(38, is_bold=True)
    h_bbox = draw.textbbox((0, 0), headline_text, font=head_font)
    h_tw = h_bbox[2] - h_bbox[0]
    h_th = h_bbox[3] - h_bbox[1]
    h_bx = 60
    h_by = by + bh + 18
    h_bw = h_tw + 45
    h_bh = h_th + 20

    draw.rounded_rectangle([h_bx + 6, h_by + 6, h_bx + h_bw + 6, h_by + h_bh + 6], radius=14, fill=(0, 0, 0, 140))
    draw.rounded_rectangle([h_bx, h_by, h_bx + h_bw, h_by + h_bh], radius=14, fill=(15, 23, 42, 230), outline=theme["accent"], width=3)
    draw.text((h_bx + 22, h_by + 8), headline_text, fill=theme["accent"], font=head_font)

    # 7. Subtle YouTube 4K / HD corner watermark badge
    draw.rounded_rectangle([width - 150, height - 70, width - 40, height - 30], radius=8, fill=(0, 0, 0, 160), outline=(255, 255, 255, 80), width=2)
    watermark_font = get_font(20, is_bold=True)
    draw.text((width - 130, height - 63), "16:9 • HD", fill=(255, 255, 255), font=watermark_font)

    # Save final high-res thumbnail
    im = im.convert("RGB")
    im.save(output_path, "PNG", quality=95)
    return output_path


def export_thumbnail_prompts(
    topic_id: str,
    title_en: str,
    output_txt_path: str
) -> str:
    """
    Generates a high-converting text prompt file formatted for:
    - Google Flow
    - Midjourney v6
    - Nano Banana / DALL-E 3
    """
    theme = TOPIC_THEMES.get(topic_id, {
        "badge_en": "WHAT IF?!",
        "headline": "THE SHOCKING TRUTH",
        "subject": "SCIENTIFIC BREAKDOWN"
    })

    content = f"""# YouTube Thumbnail AI Art Prompts (16:9 High-CTR)
Topic: {title_en}
Badge Idea: "{theme.get('badge_en', 'WHAT IF?!')}"

===============================================================================
1. NANO BANANA / GOOGLE FLOW PROMPT:
===============================================================================
A high-click-through-rate YouTube video thumbnail in vibrant Kurzgesagt and modern infographic 2D vector flat animation style, 16:9 aspect ratio.
Composition: On the left, an adorable human cartoon character with a cute pill capsule body silhouette, human face with wide-open shocked eyes, mouth agape in utter disbelief, wearing a modern casual colorful hoodie and sneakers, pointing dramatically toward the right.
On the right: A colossal dramatic phenomenon depicting {theme.get('subject', title_en)} with glowing high-contrast energy rings, vibrant glowing colors, and cinematic planetary perspective.
Aesthetic: Clean bold outlines, vibrant saturated colors, no photographic clutter, high visual hierarchy, clean negative space, dramatic lighting, 4K digital vector art.

===============================================================================
2. MIDJOURNEY V6 PROMPT:
===============================================================================
YouTube thumbnail vector art, Kurzgesagt aesthetic, high CTR curiosity concept of {title_en}, cute minimalist pill-shaped cartoon character with shocked expression and giant pupils, vibrant flat 2D vector, dramatic cosmic planetary glow, bold outlines, saturated color palette, clean composition --ar 16:9 --style raw --v 6.0

===============================================================================
3. RECOMMENDED YOUTUBE TITLE & THUMBNAIL TEXT:
===============================================================================
Hook Text Overlay: {theme.get('badge_en', 'WHAT IF?!')}
Sub-Hook Text: {theme.get('headline', 'THE SHOCKING TRUTH')}
"""
    os.makedirs(os.path.dirname(os.path.abspath(output_txt_path)), exist_ok=True)
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(content)
    return output_txt_path
