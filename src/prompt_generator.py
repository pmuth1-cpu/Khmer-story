"""
Prompt Generator for Human Cartoon with Pill Body Design.
Character: A charming human cartoon character with a smooth pill-shaped capsule body,
human facial features, cartoon hair, and modern human clothing (NOT a medicine pill).
"""

CHARACTER_BASE_PROMPT = (
    "A cute stylized human cartoon character designed with a minimalist pill-shaped capsule silhouette, "
    "smooth rounded pill body proportions, expressive friendly human face, big round animated eyes with pupils, "
    "stylized cartoon hair, wearing casual human clothes (colorful hoodie or t-shirt, trousers and small sneakers), "
    "Kurzgesagt and modern infographic animation aesthetic, flat 2D vector character illustration, clean bold outlines, "
    "vibrant color palette, charming educational storytelling character, crisp 4k digital vector art, 16:9 aspect ratio."
)

STYLE_SUFFIX = (
    "vector art style, highly detailed colorful environment, smooth soft lighting, "
    "child-friendly science educational animation still, trending on ArtStation, 16:9 ratio."
)

def create_scene_prompt(scene_action: str, environment: str, character_emotion: str = "curious") -> str:
    """
    Creates a standardized prompt for the human cartoon pill character in a specific scene.
    """
    return (
        f"{CHARACTER_BASE_PROMPT} "
        f"The human cartoon pill character is {character_emotion}, {scene_action}. "
        f"Background Setting: {environment}. "
        f"{STYLE_SUFFIX}"
    )


THEME_TEMPLATES = {
    "rain_for_month": {
        "title_en": "What If It Rained For a Whole Month?",
        "title_km": "ចុះបើភ្លៀងធ្លាក់ជាប់គ្នាពេញមួយខែ?",
        "scenes": [
            {
                "scene_num": 1,
                "duration_hint": 7,
                "khmer_speech": "តើអ្នកធ្លាប់គិតទេថា នឹងមានអ្វីកើតឡើង ប្រសិនបើភ្លៀងធ្លាក់មិនឈប់ រយៈពេលមួយខែពេញ?",
                "action": "standing on green grass in a cozy hoodie looking up at the sky with curious eyes",
                "environment": "blue sky starting to be covered by giant fluffy cartoon dark rain clouds",
                "emotion": "curious and questioning"
            },
            {
                "scene_num": 2,
                "duration_hint": 7,
                "khmer_speech": "នៅសប្តាហ៍ដំបូង ទឹកភ្លៀងនឹងធ្វើឱ្យដីស្រូបយកមិនទាន់ ហើយទីក្រុងចាប់ផ្តើមជន់លិចផ្លូវថ្នល់។",
                "action": "wearing a bright yellow raincoat and little rainboots over clothes, holding a red umbrella splashed by raindrops",
                "environment": "city streets covered in puddles, splashing water, dramatic funny cartoon rain",
                "emotion": "nervous and holding umbrella tightly"
            },
            {
                "scene_num": 3,
                "duration_hint": 8,
                "khmer_speech": "នៅសប្តាហ៍ទីពីរ ប្រព័ន្ធលូទាំងអស់នឹងស្ទះ ហើយចរន្តអគ្គិសនី និងប្រព័ន្ធអ៊ីនធឺណិតអាចនឹងត្រូវបានកាត់ផ្តាច់។",
                "action": "sitting safely on a rubber inflatable float on water, holding a battery lantern looking at dark buildings",
                "environment": "flooded modern city, power poles with cartoon sparks, floating cars in water",
                "emotion": "shocked and wide-eyed with mouth open"
            },
            {
                "scene_num": 4,
                "duration_hint": 8,
                "khmer_speech": "ចូលដល់សប្តាហ៍ទីបី ដំណាំកសិកម្មចាប់ផ្តើមរលួយ ហើយមនុស្សជួបការលំបាកក្នុងការស្វែងរកស្បៀងអាហារ។",
                "action": "wearing muddy overalls, inspecting a drowned cartoon plant in a field, holding a clipboard",
                "environment": "endless muddy farmland submerged under water, heavy stormy rain clouds",
                "emotion": "sad and deeply worried"
            },
            {
                "scene_num": 5,
                "duration_hint": 8,
                "khmer_speech": "នៅចុងខែ ធម្មជាតិនឹងផ្លាស់ប្តូររូបរាងទាំងស្រុង ប៉ុន្តែក៏ជាមេរៀនមួយអំពីសារៈសំខាន់នៃតុល្យភាពធម្មជាតិ!",
                "action": "standing under a vibrant rainbow in fresh clean clothes, smiling and waving cheerfully at the viewer",
                "environment": "sunlight breaking through bright clouds, vibrant green landscape recovering with fresh flowers",
                "emotion": "happy, joyful and welcoming"
            }
        ]
    },
    "humans_ice_age": {
        "title_en": "How Did Humans Survive the Ice Age?",
        "title_km": "តើមនុស្សបុរាណរស់រានមានជីវិតពីយុគសម័យទឹកកកដោយរបៀបណា?",
        "scenes": [
            {
                "scene_num": 1,
                "duration_hint": 7,
                "khmer_speech": "កាលពីជាង ២ ម៉ឺនឆ្នាំមុន ផែនដីទាំងមូលត្រូវបានគ្របដណ្ដប់ដោយផ្ទាំងទឹកកកដ៏សែនត្រជាក់។",
                "action": "wrapped in a cozy winter knit scarf and beanie, shivering comically in the cold arctic wind",
                "environment": "vast endless arctic tundra, huge glaciers, snow falling gently",
                "emotion": "cold and trembling comically"
            },
            {
                "scene_num": 2,
                "duration_hint": 8,
                "khmer_speech": "ដើម្បីរស់ មនុស្សសម័យនោះបានច្នៃស្បែកសត្វធ្វើជាសម្លៀកបំពាក់កក់ក្តៅ និងរស់នៅក្នុងរូងភ្នំ។",
                "action": "wearing a stitched prehistoric fur parka and boots, sitting comfortably by a crackling warm campfire",
                "environment": "inside a stone cave decorated with primitive cave paintings, warm orange fire glow",
                "emotion": "warm, cozy and relieved"
            },
            {
                "scene_num": 3,
                "duration_hint": 8,
                "khmer_speech": "ពួកគេចេះរួមសហការគ្នាដើម្បីបរបាញ់សត្វយក្សដូចជាដំរីម៉ាមុត ដើម្បីយកសាច់ និងឆ្អឹងធ្វើផ្ទះ។",
                "action": "wearing hunting tunic, crouching cleverly behind a snowy rock holding a wooden spear, watching mammoth",
                "environment": "snowy mountain pass, majestic woolly mammoth in the distance",
                "emotion": "clever and determined hunter"
            },
            {
                "scene_num": 4,
                "duration_hint": 8,
                "khmer_speech": "ភាពវៃឆ្លាត និងការរួបរួមគ្នានេះហើយ ដែលជួយឱ្យមនុស្សជាតិឆ្លងផុតយុគសម័យទឹកកកដ៏កាចសាហាវ!",
                "action": "standing proudly with friends on a snowy mountain summit, raising hands high in triumph",
                "environment": "golden sunrise over majestic icy mountains, sparkling snow, hope and triumph",
                "emotion": "proud, victorious and triumphant"
            }
        ]
    }
}
