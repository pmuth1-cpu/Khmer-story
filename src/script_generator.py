"""
Script Generator for Educational 'What If' and 'Why/How' YouTube cartoon videos.
Provides standard structured scene breakdowns with Khmer speech and Nano Banana prompts.
"""

from typing import List, Dict
from src.prompt_generator import create_scene_prompt, CHARACTER_BASE_PROMPT


SAMPLE_TOPICS = {
    "sun_disappears": {
        "title_en": "What If the Sun Disappeared for 7 Days?",
        "title_km": "ចុះបើព្រះអាទិត្យបាត់ខ្លួនរយៈពេល ៧ ថ្ងៃ?",
        "scenes": [
            {
                "scene_num": 1,
                "duration_hint": 6,
                "khmer_speech": "តើអ្នកធ្លាប់ស្រមៃទេថា ប្រសិនបើព្រះអាទិត្យស្រាប់តែរលត់បាត់ តើផែនដីយើងនឹងទៅជាយ៉ាងណា?",
                "action": "holding a tiny cartoon telescope, looking up at pitch black starry space with shocked face",
                "environment": "dark starry universe, giant eclipse silhouette where the sun used to be",
                "emotion": "shocked, bewildered with eyes wide open"
            },
            {
                "scene_num": 2,
                "duration_hint": 7,
                "khmer_speech": "ក្នុងរយៈពេល ៨ នាទីកន្លះដំបូង យើងនឹងមិនទាន់ដឹងខ្លួនទេ ពីព្រោះពន្លឺព្រះអាទិត្យត្រូវចំណាយពេលធ្វើដំណើរមកផែនដី។",
                "action": "tapping on a glowing wristwatch, showing an hourglass with floating clock gears",
                "environment": "cozy city at twilight, transition from golden light to sudden darkness",
                "emotion": "analytical and focused"
            },
            {
                "scene_num": 3,
                "duration_hint": 8,
                "khmer_speech": "ប៉ុន្តែបន្ទាប់ពីនោះ ភាពងងឹតទាំងស្រុងនឹងគ្របដណ្តប់ ហើយសីតុណ្ហភាពចាប់ផ្តើមធ្លាក់ចុះយ៉ាងលឿនក្រោមសូន្យ។",
                "action": "wrapped in multiple cozy cartoon blankets and thick beanie, holding a warm mug of cocoa",
                "environment": "frozen icy city street, cartoon breath condensing in the air, glowing streetlights",
                "emotion": "freezing and shivering comically"
            },
            {
                "scene_num": 4,
                "duration_hint": 8,
                "khmer_speech": "រុក្ខជាតិទាំងអស់នឹងឈប់ដំណើរការរស្មីសំយោគ ហើយមនុស្សត្រូវរស់នៅពឹងផ្អែកលើថាមពលកម្ដៅក្នុងផែនដី។",
                "action": "standing in a futuristic underground greenhouse with glowing purple UV grow-lights",
                "environment": "high-tech cartoon underground shelter with hydroponic vegetables and geothermal pipes",
                "emotion": "smart, inventive and hopeful"
            },
            {
                "scene_num": 5,
                "duration_hint": 7,
                "khmer_speech": "នេះបង្ហាញឱ្យឃើញថា ព្រះអាទិត្យគឺជាប្រភពជីវិតដ៏អស្ចារ្យ និងមានតម្លៃបំផុតសម្រាប់ពួកយើង!",
                "action": "hugging a cute mini smiling golden sun icon, smiling warmly at the camera",
                "environment": "warm golden morning sunrise spreading across rolling green hills and blue sky",
                "emotion": "grateful, super happy and joyful"
            }
        ]
    },
    "humans_ice_age": {
        "title_en": "How Did Humans Survive the Ice Age?",
        "title_km": "តើមនុស្សបុរាណរស់រានមានជីវិតពីយុគសម័យទឹកកកដោយរបៀបណា?",
        "scenes": [
            {
                "scene_num": 1,
                "duration_hint": 6,
                "khmer_speech": "កាលពីជាង ២ ម៉ឺនឆ្នាំមុន ផែនដីទាំងមូលត្រូវបានគ្របដណ្ដប់ដោយផ្ទាំងទឹកកកដ៏សែនត្រជាក់។",
                "action": "shivering in cold, rubbing hands together, wearing a cute cartoon furry earmuff",
                "environment": "vast endless arctic tundra, huge glaciers, snow falling gently",
                "emotion": "cold and trembling comically"
            },
            {
                "scene_num": 2,
                "duration_hint": 7,
                "khmer_speech": "ដើម្បីរស់ មនុស្សសម័យនោះបានច្នៃស្បែកសត្វធ្វើជាសម្លៀកបំពាក់កក់ក្តៅ និងរស់នៅក្នុងរូងភ្នំ។",
                "action": "wrapped in a thick warm fluffy fur coat, sitting happily near a cozy campfire",
                "environment": "inside a stone cave decorated with primitive cave paintings, warm orange fire glow",
                "emotion": "warm, cozy and relieved"
            },
            {
                "scene_num": 3,
                "duration_hint": 8,
                "khmer_speech": "ពួកគេចេះរួមសហការគ្នាដើម្បីបរបាញ់សត្វយក្សដូចជាដំរីម៉ាមុត ដើម្បីយកសាច់ និងឆ្អឹងធ្វើផ្ទះ។",
                "action": "tiptoeing cleverly behind a rock holding a cute wooden spear, looking at mammoth silhouette",
                "environment": "snowy mountain pass, majestic woolly mammoth in the distance",
                "emotion": "clever and determined hunter"
            },
            {
                "scene_num": 4,
                "duration_hint": 7,
                "khmer_speech": "ភាពវៃឆ្លាត និងការរួបរួមគ្នានេះហើយ ដែលជួយឱ្យមនុស្សជាតិឆ្លងផុតយុគសម័យទឹកកកដ៏កាចសាហាវ!",
                "action": "raising hands in victory, standing together with other little pill friends on a snow cliff",
                "environment": "golden sunrise over majestic icy mountains, sparkling snow, hope and triumph",
                "emotion": "proud, victorious and triumphant"
            }
        ]
    },
    "ocean_empty": {
        "title_en": "What If All Ocean Water Disappeared?",
        "title_km": "ចុះបើទឹកមហាសមុទ្រទាំងអស់ស្រាប់តែបាត់បង់?",
        "scenes": [
            {
                "scene_num": 1,
                "duration_hint": 6,
                "khmer_speech": "មហាសមុទ្រគ្របដណ្តប់ជាង ៧០ ភាគរយនៃផ្ទៃផែនដី ប៉ុន្តែចុះបើវាបាត់បង់ក្នុងមួយប៉ព្រិចភ្នែក?",
                "action": "standing on the beach edge with a cartoon lifebuoy, looking down into an empty giant abyss",
                "environment": "massive dry oceanic canyon where the sea used to be, dry corals and cliffs",
                "emotion": "jaw-dropped shock and surprise"
            },
            {
                "scene_num": 2,
                "duration_hint": 7,
                "khmer_speech": "យើងនឹងបានឃើញជ្រលងភ្នំ និងសំណង់បាតសមុទ្របុរាណដែលកប់ទុកជាយូរមកហើយ។",
                "action": "sliding down a steep rocky oceanic trench, pointing at an ancient cartoon sunken ship and lost city ruins",
                "environment": "vast alien-like underwater mountain ranges exposed under clear sky",
                "emotion": "amazed and exploring with flashlight"
            },
            {
                "scene_num": 3,
                "duration_hint": 8,
                "khmer_speech": "ប៉ុន្តែគ្មានទឹកមហាសមុទ្រ វដ្តទឹកនៃពពក និងភ្លៀងនឹងត្រូវដួលរលំ ធ្វើឱ្យផែនដីប្រែក្លាយទៅជាវាលខ្សាច់ដ៏ក្តៅគគុក។",
                "action": "sweating heavily under a scorching blazing cartoon sun, holding an empty water bottle",
                "environment": "arid cracked desert earth extending to horizon, heat waves rising",
                "emotion": "exhausted and desperately thirsty"
            },
            {
                "scene_num": 4,
                "duration_hint": 7,
                "khmer_speech": "មហាសមុទ្រគឺជាបេះដូងនៃជីវិតផែនដី ដូច្នេះចូរយើងទាំងអស់គ្នារួមគ្នាស្រឡាញ់ និងការពារវា!",
                "action": "swimming happily inside a giant glowing water bubble with cartoon colorful fish and dolphins",
                "environment": "vibrant turquoise ocean coral reef full of life, sun rays piercing through water",
                "emotion": "joyful, inspired and peaceful"
            }
        ]
    }
}


def build_custom_topic_script(topic_title_km: str, topic_title_en: str, scene_points: List[Dict]) -> Dict:
    """
    Constructs a structured video script from custom user points.
    """
    scenes = []
    for idx, pt in enumerate(scene_points, start=1):
        scenes.append({
            "scene_num": idx,
            "duration_hint": pt.get("duration", 7),
            "khmer_speech": pt["khmer_speech"],
            "action": pt.get("action", "explaining the concept with curious gestures"),
            "environment": pt.get("environment", "vibrant colorful educational background"),
            "emotion": pt.get("emotion", "curious and engaging")
        })
    return {
        "title_en": topic_title_en,
        "title_km": topic_title_km,
        "scenes": scenes
    }
