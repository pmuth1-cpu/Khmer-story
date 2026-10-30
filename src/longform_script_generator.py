"""
Expanded Long-Form Curiosity Topic Library (8 to 15 minutes).
Includes rich scientific curiosity scripts and instant topic generator.
"""

from typing import List, Dict, Optional
import os

from src.prompt_generator import CHARACTER_BASE_PROMPT


EXPANDED_CURIO_TOPICS = [
    {
        "id": "rain_for_month",
        "title_km": "ចុះបើភ្លៀងធ្លាក់ជាប់គ្នាពេញមួយខែ?",
        "title_en": "What If It Rained Non-Stop for 30 Days?",
        "icon": "🌧️",
        "description": "ទឹកជំនន់ ការដួលរលំហេដ្ឋារចនាសម្ព័ន្ធ និងការផ្លាស់ប្តូរប្រព័ន្ធអេកូឡូស៊ីផែនដី"
    },
    {
        "id": "humans_ice_age",
        "title_km": "តើមនុស្សបុរាណរស់រានពីយុគទឹកកកយ៉ាងណា?",
        "title_en": "How Humans Survived the Ice Age",
        "icon": "❄️",
        "description": "ការប្រើប្រាស់ភ្លើង សម្លៀកបំពាក់រោមសត្វ និងការបរបាញ់ដំរីម៉ាមុត"
    },
    {
        "id": "sun_disappears",
        "title_km": "ចុះបើព្រះអាទិត្យបាត់ខ្លួនរយៈពេល ៧ ថ្ងៃ?",
        "title_en": "What If the Sun Disappeared for 7 Days?",
        "icon": "☀️",
        "description": "ភាពងងឹតទាំងស្រុង សីតុណ្ហភាពធ្លាក់ចុះក្រោមសូន្យ និងការរស់រានក្នុងទីជម្រកក្រោមដី"
    },
    {
        "id": "ocean_empty",
        "title_km": "ចុះបើទឹកមហាសមុទ្រទាំងអស់រីងស្ងួត?",
        "title_en": "What If All Ocean Water Disappeared?",
        "icon": "🌊",
        "description": "ការលេចចេញនូវជ្រលងបាតសមុទ្របុរាណ ការដួលរលំវដ្តទឹក និងផែនដីប្រែជាវាលខ្សាច់"
    },
    {
        "id": "no_sleep",
        "title_km": "ចុះបើមនុស្សគ្រប់រូបគេងមិនលក់ ១០ ថ្ងៃ?",
        "title_en": "What If Humans Couldn't Sleep for 10 Days?",
        "icon": "🧠",
        "description": "ការប្រែប្រួលនៃខួរក្បាល ការស្រមើស្រមៃឃើញរូបភាពចម្លែក និងការគាំងបេះដូង"
    },
    {
        "id": "no_gravity",
        "title_km": "ចុះបើគ្មានទំនាញផែនដីរយៈពេល ៥ វិនាទី?",
        "title_en": "What If Gravity Vanished for 5 Seconds?",
        "icon": "🌌",
        "description": "មនុស្ស រថយន្ត និងមហាសមុទ្រហោះឡើងទៅក្នុងអាកាស និងការធ្លាក់មកវិញយ៉ាងកាចសាហាវ"
    },
    {
        "id": "all_ice_melts",
        "title_km": "ចុះបើផ្ទាំងទឹកកកប៉ូលទាំងអស់រលាយអស់?",
        "title_en": "What If All Earth's Ice Melted?",
        "icon": "🧊",
        "description": "នីវ៉ូទឹកសមុទ្រឡើងខ្ពស់ ៦៦ ម៉ែត្រ លិចទីក្រុងឆ្នេរសមុទ្រពិភពលោកទាំងអស់"
    },
    {
        "id": "oxygen_double",
        "title_km": "ចុះបើកម្រិតអុកស៊ីសែនកើនឡើងទ្វេដង?",
        "title_en": "What If Oxygen Doubled on Earth?",
        "icon": "🌿",
        "description": "សត្វល្អិតរីកមាឌយក្ស ភ្លើងឆេះព្រៃមិនអាចពន្លត់បាន និងមនុស្សមានថាមពលអស្ចារ្យ"
    },
    {
        "id": "supervolcano",
        "title_km": "ចុះបើភ្នំភ្លើងយក្ស Yellowstone ផ្ទុះឡើង?",
        "title_en": "What If a Supervolcano Erupted?",
        "icon": "🌋",
        "description": "ផេះភ្នំភ្លើងបាំងពន្លឺព្រះអាទិត្យ បង្កើតរដូវរងាភ្នំភ្លើងសកលរាប់ឆ្នាំ"
    },
    {
        "id": "moon_closer",
        "title_km": "ចុះបើព្រះចន្ទខិតមកជិតផែនដីពាក់កណ្តាល?",
        "title_en": "What If the Moon Were Twice as Close?",
        "icon": "🌙",
        "description": "រលកយក្សស៊ូណាមិកម្ពស់រាប់រយម៉ែត្រ និងការរញ្ជួយដីទូទាំងពិភពលោក"
    }
]


def export_google_flow_prompts(script_data: Dict, output_file: str):
    lines = []
    lines.append(f"# Google Flow & Nano Banana Prompts: {script_data.get('title_en', '')}")
    lines.append(f"# Khmer Title: {script_data.get('title_km', '')}")
    lines.append(f"# Total Scenes: {len(script_data.get('scenes', []))} | Est Duration: {script_data.get('estimated_duration_minutes', 8)} minutes")
    lines.append("# Character Design: Human cartoon character with a pill-shaped body silhouette (Kurzgesagt aesthetic)\n")
    lines.append("=" * 80 + "\n")

    for sc in script_data.get("scenes", []):
        lines.append(f"### [Scene {sc['scene_num']:02d}] {sc.get('act', '')} (Duration: {sc.get('duration_hint', 7.5)}s)")
        lines.append(f"Speech (Khmer): {sc.get('khmer_speech', '')}")
        if sc.get('english_speech'):
            lines.append(f"Speech (English): {sc.get('english_speech', '')}")
        lines.append("Google Flow Prompt:")
        lines.append(sc.get("full_prompt", ""))
        lines.append("\n" + "-" * 80 + "\n")

    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
