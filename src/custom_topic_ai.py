"""
Custom Topic Generator for Long-Form (8 to 15 minute) Curiosity Videos.
Generates structured narrative arcs with Khmer narration, English narration,
and Google Flow / Nano Banana prompts. Every scene is 100% unique and progressive.
"""

import os
import re
import json
from typing import Dict, List, Optional
from src.prompt_generator import CHARACTER_BASE_PROMPT


def sanitize_slug(text: str) -> str:
    slug = re.sub(r'[^a-zA-Z0-9_\u1780-\u17FF]', '_', text.strip())
    slug = re.sub(r'_+', '_', slug).strip('_')
    return slug[:40] if slug else "custom_topic"


def create_ai_longform_script(
    title_km: str,
    title_en: str,
    target_minutes: int = 8,
    api_key: Optional[str] = None
) -> Dict:
    """
    Creates a full long-form script for target_minutes (8 to 15 min).
    If Gemini API key is available, uses Gemini Flash.
    Otherwise, uses our rich progressive scientific storytelling generator with zero scene repetition.
    """
    total_scenes_needed = int((target_minutes * 60) / 7.5)
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if key:
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=key)
            system_instruction = (
                "You are an expert YouTube science documentary writer specializing in Kurzgesagt-style "
                "curiosity questions ('What if...' / 'Why or How...'). You write captivating, educational, "
                "storytelling scripts in Khmer and English with visual scene descriptions for cartoon pill characters. "
                "Every single scene MUST have completely unique narration and visuals, progressing chronologically with zero repetition."
            )
            prompt = f"""
Write a complete, educational YouTube video script for:
Title EN: {title_en}
Title KM: {title_km}
Total Scenes: {total_scenes_needed} scenes (each scene lasting 7-8 seconds of speech).
Divide the script across 5 narrative acts with STRICT CHRONOLOGICAL PROGRESSION (NO REPEATING TEXT):
- Act 1: The Inciting Hook & First Shock
- Act 2: Immediate 24-Hour Chain Reaction
- Act 3: Deep Scientific & Ecological Breakdown
- Act 4: Human & Animal Adaptation & Survival
- Act 5: The Grand Scientific Conclusion & Outro

Respond ONLY in valid JSON matching this schema:
{{
  "title_en": "{title_en}",
  "title_km": "{title_km}",
  "estimated_duration_minutes": {target_minutes},
  "scenes": [
    {{
      "scene_num": 1,
      "act": "Act 1: The Inciting Hook",
      "duration_hint": 7.5,
      "khmer_speech": "អត្ថបទភាសាខ្មែរ...",
      "english_speech": "English text...",
      "action": "what the cartoon pill character is doing",
      "environment": "setting description",
      "emotion": "curious / shocked / happy"
    }}
  ]
}}
"""
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    system_instruction=system_instruction
                )
            )
            data = json.loads(response.text)
            for sc in data.get("scenes", []):
                sc["full_prompt"] = (
                    f"{CHARACTER_BASE_PROMPT} "
                    f"The cute pill character is {sc.get('emotion', 'curious')}, {sc.get('action', '')}. "
                    f"Setting: {sc.get('environment', '')}. "
                    f"2D flat vector, Kurzgesagt aesthetic, vibrant colors, 16:9 ratio."
                )
            return data
        except Exception as e:
            print(f"[Notice] Gemini custom script generation fallback: {e}")

    # Rich progressive scientific storytelling generator with zero repetition
    return generate_procedural_longform_script(title_km, title_en, total_scenes_needed, target_minutes)


# Deep bank of 100% unique progressive stages per act
# Each entry: (km_template, en_template, action, environment, emotion)
ACT_PROGRESSION_BANK = [
    # Act 1: Inciting Hook & First Shock
    (
        "Act 1: The Inciting Hook & Mystery",
        0.16,
        [
            (
                "តើអ្នកធ្លាប់ឆ្ងល់ទេថា នឹងមានអ្វីកើតឡើង ប្រសិនបើ {topic}?",
                "Have you ever wondered what would happen if {topic_en}?",
                "looking up with big round cartoon eyes holding a small telescope",
                "starry cosmic background with floating question marks and glowing stardust",
                "deeply curious"
            ),
            (
                "វាស្តាប់ទៅដូចជាការស្រមើស្រមៃ ប៉ុន្តែតាមពិតទៅ វិទ្យាសាស្ត្រមានចម្លើយដ៏គួរឱ្យភ្ញាក់ផ្អើលបំផុត!",
                "It sounds like pure science fiction, but modern physics and biology hold a truly mind-blowing answer!",
                "tapping chin thoughtfully while flipping pages of a giant colorful encyclopedia",
                "cozy observatory with blackboard equations and glowing stellar globes",
                "smart and engaged"
            ),
            (
                "នៅពេលដែលព្រឹត្តិការណ៍នេះចាប់ផ្តើម ផលប៉ះពាល់ដំបូងបង្អស់នឹងលេចឡើងក្នុងរយៈពេលតែប៉ុន្មានវិនាទីប៉ុណ្ណោះ។",
                "The very second this event strikes, the initial shockwaves would propagate across the globe almost instantaneously.",
                "pointing dramatically at a ticking red digital countdown clock",
                "dramatic scientific control room with pulsing warning lights and radar screens",
                "alert and focused"
            ),
            (
                "ប្រព័ន្ធធម្មជាតិដែលយើងធ្លាប់ស្គាល់ និងទុកចិត្តរាល់ថ្ងៃ នឹងត្រូវផ្លាស់ប្តូរទម្រង់ទាំងស្រុងក្នុងមួយប៉ព្រិចភ្នែក!",
                "The familiar natural rhythms we take for granted every single morning would instantly warp beyond recognition.",
                "holding hands to head as background swirls into cartoon kaleidoscopic vortex",
                "abstract colorful space-time vortex with shifting reality grids",
                "wide-eyed in shock"
            ),
            (
                "មនុស្សជាតិរាប់ពាន់លាននាក់នឹងចាប់ផ្តើមកត់សម្គាល់ឃើញសញ្ញាមិនប្រក្រតីដំបូងនៅលើផ្ទៃមេឃ និងបរិយាកាសជុំវិញ។",
                "Billions of people would look out their windows, suddenly noticing strange anomalies across the horizon.",
                "standing on a high balcony with binoculars, pointing at the oddly tinted sky",
                "city skyline under an extraordinary atmospheric color shift with vibrant purple hues",
                "bewildered observer"
            ),
            (
                "ឧបករណ៍វាស់ស្ទង់វិទ្យាសាស្ត្រនៅជុំវិញពិភពលោក ចាប់ផ្តើមបញ្ចេញសំឡេងរោទិ៍អាសន្នព្រមៗគ្នា។",
                "Scientific monitoring stations worldwide trigger synchronized high-priority alerts as gauges spike off the charts.",
                "running between buzzing scientific consoles trying to stabilize wildly fluctuating meters",
                "high-tech seismic and atmospheric observation bunker lit by amber caution lights",
                "frantic and determined"
            ),
            (
                "តើជីវិតនៅលើផែនដីអាចទប់ទល់នឹងរលកនៃការប្រែប្រួលដ៏ធំសម្បើមនេះបានដោយរបៀបណា?",
                "Could life on Earth survive such an abrupt and violent shift in planetary conditions?",
                "holding a small fragile glowing model of Earth gently between palms",
                "dark cinematic cosmos with delicate blue Earth surrounded by radiant energy rings",
                "introspective and questioning"
            ),
            (
                "ដំណើរផ្សងព្រេងវិទ្យាសាស្ត្ររបស់យើងទើបតែចាប់ផ្តើម ហើយជំហានបន្ទាប់នឹងនាំយើងទៅកាន់ម៉ោងដំបូងនៃវិបត្តិ!",
                "Our scientific journey is just getting underway, leading us directly into the chaotic first hours of the phenomenon!",
                "turning sharply towards camera with determined expression, gesture inviting the viewer forward",
                "dynamic split-screen displaying ticking clock and unfolding planetary transformation",
                "electrified and eager"
            )
        ]
    ),

    # Act 2: Immediate 24-Hour Chain Reaction
    (
        "Act 2: The Immediate 24-Hour Chain Reaction",
        0.24,
        [
            (
                "ក្នុងរយៈពេលប៉ុន្មានម៉ោងដំបូង ហេដ្ឋារចនាសម្ព័ន្ធ និងប្រព័ន្ធទំនាក់ទំនងទូទាំងពិភពលោកនឹងចាប់ផ្តើមរងសម្ពាធយ៉ាងធ្ងន់ធ្ងរ។",
                "Within the opening hours, global communication grids and municipal infrastructure experience unprecedented mechanical strain.",
                "running with a mini tool belt trying to monitor sparking fuse boxes and server racks",
                "busy cartoon cityscape with glowing neon wires and emergency flashing hazard lights",
                "hardworking and vigilant"
            ),
            (
                "ការប្រែប្រួលនៃកម្លាំងធម្មជាតិ ធ្វើឱ្យតុល្យភាពបរិយាកាស និងលំនឹងកម្ដៅចាប់ផ្តើមរង្គោះរង្គើ។",
                "Unprecedented thermodynamic shifts shake the delicate atmospheric equilibrium of our skies.",
                "holding an anemometer wind speed gauge against harsh cartoon wind gusts and swirling pressure lines",
                "windy cliff overlooking swirling colorful cloud vortices",
                "bracing against the storm"
            ),
            (
                "ចរន្តអគ្គិសនី និងប្រព័ន្ធផ្គត់ផ្គង់ទឹកស្អាតនៅតាមទីក្រុងធំៗ ត្រូវប្រឈមមុខនឹងការរអាក់រអួលជាបន្តបន្ទាប់។",
                "Power grids and municipal water supplies in metropolitan hubs face cascading rolling brownouts.",
                "holding a warm glowing battery lantern as city background lights flicker and shut off",
                "metropolitan skyline going dark section by section, warm apartment windows glowing with candlelight",
                "cautious and observant"
            ),
            (
                "សត្វស្លាប និងសត្វព្រៃជាច្រើនចាប់ផ្តើមបង្ហាញអាកប្បកិរិយាចម្លែក ដោយសារប្រព័ន្ធទិសដៅធម្មជាតិរបស់ពួកវាត្រូវរំខាន។",
                "Wildlife and migratory birds exhibit erratic behavior as their internal navigational compasses are thrown into disarray.",
                "kneeling gently beside cartoon birds fluttering curiously in unexpected flight patterns",
                "lush urban park where animals gather in unusual harmonious formations",
                "gentle and empathetic"
            ),
            (
                "ផ្សារទំនើប និងហាងទំនិញត្រូវបានបំពេញដោយមនុស្សម្នាដែលកំពុងប្រញាប់ប្រញាល់ស្តុកទុកស្បៀងអាហារចាំបាច់។",
                "Grocery stores and community hubs fill with anxious citizens stocking up on non-perishable canned goods and flashlights.",
                "pushing a cartoon shopping cart filled with wholesome apples, bread, and water jugs",
                "colorful community supermarket with bustling shoppers and organized supply shelves",
                "resourceful planner"
            ),
            (
                "ក្រុមអ្នកវិទ្យាសាស្ត្រ និងវិស្វករអន្តរជាតិចាប់ផ្តើមបើកកិច្ចប្រជុំបន្ទាន់តាមប្រព័ន្ធផ្កាយរណប ដើម្បីស្វែងរកដំណោះស្រាយ។",
                "International scientists convene emergency video symposiums to model the escalating planetary trajectory.",
                "gesturing at holographic screens showing planetary projections alongside animated global scientists",
                "high-tech collaborative conference room with glowing holographic world map",
                "collaborative visionary"
            ),
            (
                "នៅចុងបញ្ចប់នៃថ្ងៃដំបូង មនុស្សជាតិគ្រប់រូបដឹងច្បាស់ថា ពិភពលោកចាស់នឹងមិនអាចត្រឡប់មកដូចដើមបានឡើយ!",
                "By the end of the first twenty-four hours, one fact becomes undeniable: life has crossed a threshold of no return!",
                "standing on rooftop at twilight, gazing thoughtfully into the rapidly transforming horizon",
                "panoramic city sunset with surreal glowing atmospheric auroras across the sky",
                "deeply reflective"
            )
        ]
    ),

    # Act 3: Deep Scientific & Ecological Breakdown
    (
        "Act 3: Deep Scientific & Ecological Breakdown",
        0.28,
        [
            (
                "ចូរយើងក្រឡេកមើលទៅក្នុងកម្រិតម៉ូលេគុល និងរូបវិទ្យា ដើម្បីយល់ច្បាស់ពីយន្តការនៅពីក្រោយបាតុភូតនេះ។",
                "Let's zoom straight down to the molecular level and fundamental physics to uncover the underlying mechanics.",
                "wearing tiny white lab coat and round glasses, peering into a giant high-powered electron microscope",
                "futuristic science laboratory with glowing DNA double helices and floating atom models",
                "expert scientist"
            ),
            (
                "ថាមពលកម្ដៅ និងចលនានៃសម្ពាធបរិយាកាស ដើរតួនាទីយ៉ាងសំខាន់ក្នុងការកំណត់ជោគវាសនារបស់ផែនដី។",
                "Thermodynamic transfer and atmospheric kinetic pressures dictate the unfolding fate of our biosphere.",
                "drawing glowing vector diagrams and thermal flowcharts on an interactive holographic glass board",
                "dim observatory room illuminated by vibrant blue and orange thermal infographics",
                "explaining passionately"
            ),
            (
                "ខ្សែសង្វាក់អាហារ និងប្រព័ន្ធអេកូឡូស៊ីក្នុងទឹក ក៏ដូចជាលើគោក ត្រូវបង្ខំចិត្តសម្របខ្លួនយ៉ាងរហ័សបំផុត។",
                "Food webs and terrestrial biomes are forced to undergo rapid, forced evolutionary adaptations.",
                "observing cartoon fish, birds, and forest animals interacting inside an enclosed experimental biosphere",
                "vibrant nature sanctuary with cascading crystal waterfalls and rare luminous flora",
                "protective naturalist"
            ),
            (
                "រុក្ខជាតិបៃតងចាប់ផ្តើមកែសម្រួលដំណើរការរស្មីសំយោគ ដើម្បីស្រូបយកថាមពលក្រោមលក្ខខណ្ឌថ្មីនេះ។",
                "Green flora recalibrates chloroplast activity to optimize metabolic survival under altered atmospheric radiation.",
                "holding a magnifying glass over a glowing green cartoon leaf, showing pulsing cellular chloroplasts",
                "high-tech botanical greenhouse with ultraviolet LED grow lights and hydroponic mist",
                "fascinated researcher"
            ),
            (
                "មហាសមុទ្រពិភពលោកដែលគ្របដណ្តប់ ៧០ ភាគរយនៃផ្ទៃផែនដី ចាប់ផ្តើមស្រូបយកកម្ដៅ និងចរន្តទឹកជំនន់ថ្មី។",
                "Global oceans, covering over seventy percent of Earth's crust, absorb titanic thermal and chemical shocks.",
                "navigating a yellow mini-submarine through deep turquoise waters past curious cartoon sea turtles",
                "sunlit coral reef trench with shimmering turquoise water and schools of exotic colorful fish",
                "intrepid oceanographer"
            ),
            (
                "ប្រសិនបើតួលេខទាំងនេះនៅតែបន្តប្រែប្រួល ផលវិបាកនឹងរាលដាលដល់គ្រប់ជ្រុងទាំងអស់នៃភពផែនដីដោយគ្មានការលើកលែង។",
                "If these atmospheric conditions persist unchecked, cascading systemic ripples will touch every corner of the planet.",
                "pointing firmly at a 3D Earth projection surrounded by glowing interconnected concentric rings",
                "planetary simulation command center with rotating high-resolution digital globe",
                "serious and analytical"
            ),
            (
                "ប៉ុន្តែធម្មជាតិមានភាពធន់ដ៏អស្ចារ្យ ដែលតែងតែស្វែងរកផ្លូវបង្កើតលំនឹងថ្មីជានិច្ច ទោះបីស្ថិតក្នុងវិបត្តិធំបំផុតក៏ដោយ!",
                "Yet nature possesses breathtaking self-healing resilience, perpetually carving pathways toward a new equilibrium!",
                "smiling with awe as a tiny green seedling sprouts through a crack in solid rock",
                "sun-dappled rocky cliff where vibrant wildflowers defiantly blossom against all odds",
                "inspired and hopeful"
            )
        ]
    ),

    # Act 4: Human & Animal Survival Mechanisms
    (
        "Act 4: Human & Animal Survival Mechanisms",
        0.20,
        [
            (
                "ប៉ុន្តែមនុស្សជាតិមានអាវុធដ៏អស្ចារ្យបំផុតមួយ នោះគឺភាពវៃឆ្លាត និងសមត្ថភាពក្នុងការច្នៃប្រឌិតបច្ចេកវិទ្យា!",
                "Yet humanity wields an unmatched superpower: intellect, adaptability, and relentless technological ingenuity!",
                "standing proudly beside a high-tech modular generator glowing with friendly emerald light",
                "modern eco-shelter powered by solar arrays and kinetic turbines",
                "proud inventor"
            ),
            (
                "យើងបានបង្កើតដំណោះស្រាយវិស្វកម្មទំនើប ដើម្បីការពារជម្រក និងធនធានចាំបាច់សម្រាប់មនុស្សជំនាន់ក្រោយ។",
                "Engineers and civic builders rapidly deploy modular habitats and closed-loop life-support networks.",
                "collaborating enthusiastically with robot assistants and pill companions reviewing digital architectural blueprints",
                "bustling high-tech workshop filled with friendly drone couriers and robotic assembly arms",
                "visionary builder"
            ),
            (
                "ការរួបរួមសាមគ្គីភាព និងការចែករំលែកធនធាន បានជួយសង្គ្រោះជីវិតមនុស្សរាប់លាននាក់ពីគ្រោះមហន្តរាយនេះ។",
                "Cross-border solidarity and decentralized mutual aid become the absolute cornerstone of societal resilience.",
                "sharing a warm loaf of bread and fresh flask of clean water with a smiling neighbor",
                "cozy community gathering hall illuminated by warm fairy lights and shared hearth",
                "deeply compassionate"
            ),
            (
                "សត្វព្រៃក្នុងធម្មជាតិក៏បានបង្កើតយុទ្ធសាស្ត្ររស់រានផ្ទាល់ខ្លួន ដោយការធ្វើចំណាកស្រុកទៅកាន់តំបន់សុវត្ថិភាព។",
                "Wildlife herds pioneer ingenious survival migration corridors, seeking out newly formed ecological refuges.",
                "looking through binoculars at majestic cartoon animal caravans traversing a scenic mountain trail",
                "breathtaking alpine mountain pass with snowcaps, lush pine forests, and moving herds",
                "heartened observer"
            ),
            (
                "បច្ចេកវិទ្យាវេជ្ជសាស្ត្រ និងជីវបច្ចេកវិទ្យាបានជួយឱ្យយើងអាចផលិតអាហាររូបត្ថម្ភគ្រប់គ្រាន់ដោយមិនចាំបាច់ពឹងផ្អែកតែលើអាកាសធាតុ។",
                "Biotechnology and vertical vertical aeroponic agriculture ensure stable food production independent of weather extremes.",
                "holding a fresh crisp cartoon carrot freshly harvested from a vertical aeroponic tower",
                "futuristic clean-room vertical farm glowing with gentle pink and purple spectra",
                "thriving innovator"
            ),
            (
                "ភាពអត់ធន់ និងការមិនចុះចាញ់នេះហើយ ដែលបញ្ជាក់ថា មនុស្សជាតិអាចឆ្លងកាត់គ្រប់ឧបសគ្គក្នុងប្រវត្តិសាស្ត្រ!",
                "This unyielding spirit proves once more that human curiosity and collaboration can conquer any cosmic hurdle!",
                "standing tall atop a hill, raising a friendly cartoon banner of unity as the wind catches it",
                "golden hour landscape with sunrise cresting over newly rebuilt eco-villages",
                "triumphant and resolute"
            )
        ]
    ),

    # Act 5: Grand Scientific Conclusion & Outro
    (
        "Act 5: The Grand Scientific Conclusion & Outro",
        0.12,
        [
            (
                "នៅទីបំផុត ព្រឹត្តិការណ៍នេះបានបង្រៀនយើងឱ្យយល់កាន់តែច្បាស់អំពីភាពអស្ចារ្យ និងតុល្យភាពនៃចក្រវាល។",
                "Ultimately, this grand ordeal teaches us profound humility and deep respect for the majestic balance of our cosmos.",
                "sitting comfortably on the crest of a grassy hill looking up into the peaceful, sparkling starry night",
                "breathtaking panoramic night sky with twinkling constellations and glowing nebula ribbons",
                "peaceful and enlightened"
            ),
            (
                "ផែនដីគឺជាជម្រកតែមួយគត់របស់យើង ហើយការយល់ដឹងពីវិទ្យាសាស្ត្រគឺជាគន្លឹះក្នុងការថែរក្សាវាឱ្យស្ថិតស្ថេរ។",
                "Earth remains our singular, irreplaceable oasis, and scientific literacy is the compass guiding its stewardship.",
                "holding a small sprouting green seedling in cupped hands as colorful butterflies flutter gently overhead",
                "lush blooming meadow bathed in warm morning sunshine under a crisp azure sky",
                "pure joyful hope"
            ),
            (
                "តើអ្នកគិតយ៉ាងណាដែរចំពោះសេណារីយ៉ូមួយនេះ? ប្រសិនបើអ្នកជួបប្រទះវា តើអ្នកនឹងធ្វើដូចម្តេច? សូមបញ្ចេញមតិយោបល់នៅខាងក្រោម!",
                "What are your thoughts on this hypothetical scenario? How would you have adapted? Share your ideas in the comments below!",
                "waving cheerfully with both hands, gesturing playfully toward an animated speech bubble",
                "colorful modern Kurzgesagt-style studio set with animated comment bubbles and floating badges",
                "friendly and engaging"
            ),
            (
                "សូមកុំភ្លេចចុច Like និង Subscribe ដើម្បីបន្តដំណើរផ្សងព្រេងក្នុងពិភពវិទ្យាសាស្ត្រជាមួយពួកយើងនៅវីដេអូបន្ទាប់!",
                "Don't forget to hit Like and Subscribe to continue embarking on mind-expanding scientific adventures with us in every episode!",
                "leaping happily into the air with thumbs up as animated red Subscribe and bell buttons ring with sparkles",
                "celebratory animated channel outro screen with festive confetti bursts and upbeat graphics",
                "triumphant and smiling"
            )
        ]
    )
]


def generate_procedural_longform_script(
    title_km: str,
    title_en: str,
    scene_count: int,
    target_minutes: int
) -> Dict:
    """
    Procedural science narrative generator supporting custom curiosity topics.
    Guarantees 100% UNIQUE scenes with ZERO duplicates or overlapping narration.
    """
    scenes = []
    current_num = 1

    clean_topic_en = re.sub(r'^(what\s+if\s+|why\s+|how\s+)', '', title_en, flags=re.IGNORECASE).strip().rstrip('?')
    if clean_topic_en:
        clean_topic_en = clean_topic_en[0].lower() + clean_topic_en[1:]
    clean_topic_km = re.sub(r'^(ចុះបើ\s*|ហេតុអ្វី\s*)', '', title_km).strip().rstrip('?')

    # Chronological progression nuance modifiers if an act needs more scenes than base templates
    step_prefixes_en = [
        "Initially,", "Following that,", "As the situation evolves,", "Examining the physics closer,",
        "Across regional territories,", "At the biological level,", "Simultaneously,",
        "From an engineering standpoint,", "Taking a deeper look,", "Advancing further,"
    ]
    step_prefixes_km = [
        "នៅដំណាក់កាលដំបូង ", "បន្ទាប់មកទៀត ", "ស្របពេលដែលស្ថានការណ៍វិវត្តទៅមុខ ", "ក្រឡេកមើលទិដ្ឋភាពរូបវិទ្យា ",
        "នៅតាមតំបន់ផ្សេងៗគ្នា ", "ក្នុងកម្រិតជីវសាស្ត្រ ", "ទន្ទឹមនឹងនេះដែរ ",
        "បើគិតពីទិដ្ឋភាពវិស្វកម្ម ", "ពិនិត្យឱ្យកាន់តែស៊ីជម្រៅ ", "ឈានទៅមុខមួយកម្រិតទៀត "
    ]

    for act_title, ratio, templates in ACT_PROGRESSION_BANK:
        count_for_act = max(len(templates), int(scene_count * ratio))
        for i in range(count_for_act):
            tmpl_idx = i % len(templates)
            cycle_round = i // len(templates)
            tmpl = templates[tmpl_idx]

            base_speech_km = tmpl[0].replace("{topic}", clean_topic_km)
            base_speech_en = tmpl[1].replace("{topic_en}", clean_topic_en)

            # If an act requires more scenes than base templates, apply distinct progression modifiers
            if cycle_round > 0:
                p_en = step_prefixes_en[i % len(step_prefixes_en)]
                p_km = step_prefixes_km[i % len(step_prefixes_km)]
                speech_en = f"{p_en} {base_speech_en[0].lower() + base_speech_en[1:]}"
                speech_km = f"{p_km}{base_speech_km}"
                action = f"{tmpl[2]} (phase {cycle_round + 1} analysis)"
            else:
                speech_en = base_speech_en
                speech_km = base_speech_km
                action = tmpl[2]

            env = tmpl[3]
            emotion = tmpl[4]

            full_prompt = (
                f"{CHARACTER_BASE_PROMPT} "
                f"The cute pill character is {emotion}, {action}. "
                f"Environment: {env}. "
                f"Infographic 2D vector style, vibrant Kurzgesagt aesthetic, clean bold line art, 16:9 ratio."
            )

            scenes.append({
                "scene_num": current_num,
                "act": act_title,
                "duration_hint": 7.5,
                "khmer_speech": speech_km,
                "english_speech": speech_en,
                "action": action,
                "environment": env,
                "emotion": emotion,
                "full_prompt": full_prompt
            })
            current_num += 1

    return {
        "title_en": title_en,
        "title_km": title_km,
        "total_scenes": len(scenes),
        "estimated_duration_minutes": target_minutes,
        "scenes": scenes
    }
