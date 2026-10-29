"""
Khmer Caption Card Renderer.
Renders clean, transparent YouTube-style subtitles:
- NO background box/pill
- Bold white or yellow text
- Strong black outline/stroke and shadow for readability over any scene
- Preserves accurate Khmer script shaping
"""

import os
import subprocess
from typing import List, Dict


def get_edge_binary() -> str:
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return ""


def is_english_text(text: str) -> bool:
    latin_count = sum(1 for c in text if 'a' <= c.lower() <= 'z')
    return latin_count > 5


def render_caption_png(
    text: str,
    output_png_path: str,
    width: int = 1920,
    height: int = 1080,
    text_color: str = "#ffffff",
    font_size: int = 52
) -> str:
    """
    Renders a clean floating subtitle card with ZERO background box.
    Supports both English (Inter / Modern Bold) and Khmer (Kantumruy Pro).
    Only text with a heavy black outline and shadow for crisp contrast over any video scene.
    """
    browser_exe = get_edge_binary()
    os.makedirs(os.path.dirname(os.path.abspath(output_png_path)), exist_ok=True)

    is_en = is_english_text(text)
    font_family = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" if is_en else "'Kantumruy Pro', 'Khmer UI', 'Leelawadee UI', sans-serif"
    font_weight = "800" if is_en else "700"
    adjusted_size = font_size if is_en else (font_size + 2)

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;800&family=Kantumruy+Pro:wght@700&display=swap');
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    width: {width}px;
    height: {height}px;
    background: transparent;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: flex-end;
    padding-bottom: 60px;
  }}
  .caption-text {{
    font-family: {font_family};
    font-size: {adjusted_size}px;
    font-weight: {font_weight};
    color: {text_color};
    text-align: center;
    line-height: 1.45;
    max-width: 1550px;
    /* Heavy black stroke & shadow, NO background box */
    text-shadow: 
      -3.5px -3.5px 0 #000,  
       3.5px -3.5px 0 #000,
      -3.5px  3.5px 0 #000,
       3.5px  3.5px 0 #000,
      -3.5px  0px   0 #000,
       3.5px  0px   0 #000,
       0px   -3.5px 0 #000,
       0px    3.5px 0 #000,
       0px    5px 16px rgba(0, 0, 0, 0.95);
  }}
</style>
</head>
<body>
  <div class="caption-text">{text}</div>
</body>
</html>
"""
    temp_html = output_png_path.replace(".png", ".html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    html_abs = os.path.abspath(temp_html).replace("\\", "/")
    out_abs = os.path.abspath(output_png_path)

    if browser_exe:
        cmd = [
            browser_exe,
            "--headless=new",
            "--disable-gpu",
            f"--screenshot={out_abs}",
            f"--window-size={width},{height}",
            "--default-background-color=00000000",
            f"file:///{html_abs}"
        ]
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        except Exception:
            pass

    if os.path.exists(temp_html):
        try:
            os.remove(temp_html)
        except Exception:
            pass

    return out_abs


render_khmer_caption_png = render_caption_png
