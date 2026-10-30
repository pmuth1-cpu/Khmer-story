"""
Custom Topic Generator for Long-Form (8 to 15 minute) Curiosity Videos.
Generates structured narrative arcs with Khmer narration, English narration,
and Google Flow / Nano Banana prompts. Every scene is 100% unique, simple to understand,
and written in authentic 'What If', 'Why/How', and science curiosity documentary style.
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
    If Gemini API key is available, uses Gemini Flash in authentic Kurzgesagt / What-If documentary style.
    Otherwise, uses our procedural curiosity storytelling generator with zero repetition.
    """
    total_scenes_needed = int((target_minutes * 60) / 7.5)
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if key:
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=key)
            system_instruction = (
                "You are an expert YouTube science documentary writer specializing in Kurzgesagt, Riddles, "
                "and 'What If' curiosity questions ('What if...' / 'Why or How...' / 'History of...'). "
                "You write captivating, educational, thought-provoking scripts in Khmer and English with visual scene descriptions for cartoon pill characters.\n\n"
                "CRITICAL STYLE GUIDELINES:\n"
                "1. AUTHENTIC WHAT-IF / SCIENCE DOCUMENTARY: Maintain the core documentary identity: explore scientific thought experiments, "
                "hypothetical chain reactions, historical context, and real planetary/biological facts. Do NOT turn it into a literal video game arcade with cheat codes or player buttons.\n"
                "2. SIMPLE, EASY-TO-UNDERSTAND WORDS: Never use heavy, dry academic jargon (avoid complex medical terms or dense equations). "
                "Explain scientific concepts in everyday, clear, vivid language that anyone—from a 10-year-old to an adult—can easily follow.\n"
                "3. COMPELLING NARRATIVE JOURNEY: Follow a relatable storytelling path. Show our little character discovering what happens "
                "step-by-step, facing challenges, adapting with ingenuity, and learning the bigger lesson about nature's delicate balance.\n"
                "4. ENGAGING & SUSPENSEFUL: Pose thought-provoking questions, highlight surprising twists, and include fun interactive questions for the audience.\n"
                "5. STRICT CHRONOLOGICAL PROGRESSION: 5 clear acts progressing from the first shock to the final conclusion with zero repetition."
            )
            prompt = f"""
Write a complete, educational, easy-to-understand YouTube 'What If' documentary script for:
Title EN: {title_en}
Title KM: {title_km}
Total Scenes: {total_scenes_needed} scenes (each scene lasting 7-8 seconds of speech).
Divide the script across 5 narrative acts with STRICT CHRONOLOGICAL PROGRESSION:
- Act 1: The Inciting Hook & First Shock (Minute 0 to Hour 1)
- Act 2: Immediate 24-Hour Chain Reaction (The Crisis Begins)
- Act 3: Deep Scientific, Historical & Ecological Breakdown
- Act 4: Human & Animal Ingenuity, Adaptation & Survival
- Act 5: Grand Scientific Conclusion, The Bigger Lesson & Outro

Respond ONLY in valid JSON matching this schema:
{{
  "title_en": "{title_en}",
  "title_km": "{title_km}",
  "estimated_duration_minutes": {target_minutes},
  "scenes": [
    {{
      "scene_num": 1,
      "act": "Act 1: The Inciting Hook & First Shock",
      "duration_hint": 7.5,
      "khmer_speech": "អត្ថបទងាយយល់ បែបនិទានរឿងទាក់ទាញ...",
      "english_speech": "Clear, engaging, easy-to-understand English narration...",
      "action": "what the cute cartoon pill character is doing",
      "environment": "setting description",
      "emotion": "deeply curious / shocked / cheerful"
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

    # Rich progressive scientific storytelling generator with simple words & What-If narrative
    return generate_procedural_longform_script(title_km, title_en, total_scenes_needed, target_minutes)


# Deep bank of 100% unique progressive stages per act with simple words & What-If storytelling
# Each entry: (km_template, en_template, action, environment, emotion)
ACT_PROGRESSION_BANK = [
    # Act 1: The Inciting Hook & First Shock (0.16)
    (
        "Act 1: The Inciting Hook & First Shock",
        0.16,
        [
            (
                "តើអ្នកធ្លាប់ឆ្ងល់ទេថា នឹងមានអ្វីកើតឡើង ប្រសិនបើ {topic}?",
                "Have you ever wondered what would really happen if {topic_en}?",
                "looking up with big round cartoon eyes holding a small telescope",
                "starry cosmic background with floating question marks and glowing stardust",
                "deeply curious"
            ),
            (
                "វាស្តាប់ទៅដូចជារឿងមិនគួរឱ្យជឿ ប៉ុន្តែតាមពិតទៅ វិទ្យាសាស្ត្រមានចម្លើយដ៏គួរឱ្យភ្ញាក់ផ្អើលបំផុត!",
                "It sounds like pure science fiction, but modern physics and biology hold a truly mind-blowing answer!",
                "tapping chin thoughtfully while flipping pages of a giant colorful encyclopedia",
                "cozy observatory with blackboard equations and glowing stellar globes",
                "smart and engaged"
            ),
            (
                "នៅវិនាទីដំបូងដែលព្រឹត្តិការណ៍នេះចាប់ផ្តើម ផលប៉ះពាល់ដំបូងបង្អស់នឹងលេចឡើងយ៉ាងឆាប់រហ័ស។",
                "The very second this event unfolds, the first shockwaves begin propagating across the globe.",
                "pointing dramatically at a ticking red digital countdown clock",
                "dramatic scientific control room with pulsing warning lights and radar screens",
                "alert and focused"
            ),
            (
                "ច្បាប់ធម្មជាតិដែលយើងធ្លាប់ស្គាល់រាល់ថ្ងៃ ស្រាប់តែប្រែប្រួលទម្រង់ទាំងស្រុងក្នុងមួយប៉ព្រិចភ្នែក!",
                "The familiar natural rhythms we take for granted every single morning would instantly change beyond recognition.",
                "holding hands to head as background swirls into cartoon kaleidoscopic vortex",
                "abstract colorful space-time vortex with shifting reality grids",
                "wide-eyed in shock"
            ),
            (
                "មនុស្សរាប់ពាន់លាននាក់នឹងចាប់ផ្តើមកត់សម្គាល់ឃើញសញ្ញាមិនប្រក្រតីដំបូងនៅលើផ្ទៃមេឃ និងបរិយាកាសជុំវិញ។",
                "Billions of people would look out their windows, suddenly noticing strange new changes across the horizon.",
                "standing on a high balcony with binoculars, pointing at the oddly tinted sky",
                "city skyline under an extraordinary atmospheric color shift with vibrant purple hues",
                "bewildered observer"
            ),
            (
                "ឧបករណ៍វាស់ស្ទង់វិទ្យាសាស្ត្រនៅជុំវិញពិភពលោក ចាប់ផ្តើមលោតសញ្ញាអាសន្នព្រមៗគ្នា។",
                "Scientific monitoring stations worldwide trigger synchronized alerts as unusual readings spike.",
                "running between buzzing scientific consoles trying to stabilize wildly fluctuating meters",
                "high-tech seismic and atmospheric observation bunker lit by amber caution lights",
                "frantic and determined"
            ),
            (
                "តើជីវិតនៅលើផែនដីអាចទប់ទល់នឹងរលកនៃការប្រែប្រួលដ៏ធំសម្បើមនេះបានដោយរបៀបណា?",
                "Could life on Earth survive such an abrupt and dramatic planetary transformation?",
                "holding a small fragile glowing model of Earth gently between palms",
                "dark cinematic cosmos with delicate blue Earth surrounded by radiant energy rings",
                "introspective and questioning"
            ),
            (
                "ដំណើរផ្សងព្រេងវិទ្យាសាស្ត្ររបស់យើងទើបតែចាប់ផ្តើម ហើយជំហានបន្ទាប់នឹងនាំយើងទៅកាន់ម៉ោងដំបូងនៃវិបត្តិ!",
                "Our scientific journey is just getting underway, leading us directly into the first crucial hours of the phenomenon!",
                "turning sharply towards camera with determined expression, gesture inviting the viewer forward",
                "dynamic split-screen displaying ticking clock and unfolding planetary transformation",
                "electrified and eager"
            )
        ]
    ),

    # Act 2: Immediate 24-Hour Chain Reaction (0.24)
    (
        "Act 2: Immediate 24-Hour Chain Reaction",
        0.24,
        [
            (
                "ក្នុងរយៈពេលប៉ុន្មានម៉ោងដំបូង ប្រព័ន្ធអគ្គិសនី និងប្រព័ន្ធផ្គត់ផ្គង់ទឹកចាប់ផ្តើមរងផលប៉ះពាល់យ៉ាងធ្ងន់ធ្ងរ។",
                "Within the opening hours, electrical power grids and municipal water supplies begin feeling intense strain.",
                "running with a mini tool belt trying to monitor sparking fuse boxes and server racks",
                "busy cartoon cityscape with glowing neon wires and emergency flashing hazard lights",
                "hardworking and vigilant"
            ),
            (
                "ការប្រែប្រួលនៃកម្លាំងធម្មជាតិ ធ្វើឱ្យអាកាសធាតុ និងកម្តៅជុំវិញខ្លួនយើងចាប់ផ្តើមប្រែប្រួលយ៉ាងឆាប់រហ័ស។",
                "Shifts in natural forces cause surrounding temperatures and weather patterns to swing dramatically.",
                "holding an anemometer wind speed gauge against harsh cartoon wind gusts and swirling pressure lines",
                "windy cliff overlooking swirling colorful cloud vortices",
                "bracing against the storm"
            ),
            (
                "ភ្លើងក្នុងទីក្រុងចាប់ផ្តើមដាច់ជាបន្តបន្ទាប់ ហើយមនុស្សត្រូវប្រើប្រាស់ចង្កៀងគោម និងពិលដើម្បីបំភ្លឺ។",
                "City lights begin flickering off section by section, prompting families to light battery lanterns and candles.",
                "holding a warm glowing battery lantern as city background lights flicker and shut off",
                "metropolitan skyline going dark section by section, warm apartment windows glowing with candlelight",
                "cautious and observant"
            ),
            (
                "សត្វស្លាប និងសត្វព្រៃចាប់ផ្តើមបង្ហាញអាកប្បកិរិយាចម្លែក ដោយសារប្រព័ន្ធទិសដៅធម្មជាតិរបស់ពួកវាត្រូវរំខាន។",
                "Birds and wildlife display unusual behaviors as their natural navigational compasses are thrown off.",
                "kneeling gently beside cartoon birds fluttering curiously in unexpected flight patterns",
                "lush urban park where animals gather in unusual harmonious formations",
                "gentle and empathetic"
            ),
            (
                "មនុស្សម្នាប្រញាប់ប្រញាល់ទៅកាន់ផ្សារទំនិញ ដើម្បីស្តុកទុកស្បៀងអាហារចាំបាច់ និងទឹកស្អាត។",
                "People hurry to neighborhood markets, stocking up on essential food, water bottles, and flashlights.",
                "pushing a cartoon shopping cart filled with wholesome apples, bread, and water jugs",
                "colorful community supermarket with bustling shoppers and organized supply shelves",
                "resourceful planner"
            ),
            (
                "ក្រុមអ្នកវិទ្យាសាស្ត្រ និងវិស្វករអន្តរជាតិចាប់ផ្តើមបើកកិច្ចប្រជុំបន្ទាន់ ដើម្បីស្វែងរកដំណោះស្រាយ។",
                "International scientists hold emergency discussions to model the physics and find safe solutions.",
                "gesturing at holographic screens showing planetary projections alongside animated global scientists",
                "high-tech collaborative conference room with glowing holographic world map",
                "collaborative visionary"
            ),
            (
                "នៅចុងបញ្ចប់នៃថ្ងៃដំបូង មនុស្សគ្រប់រូបដឹងច្បាស់ថា ពិភពលោកយើងនឹងមិនដូចមុនទៀតឡើយ!",
                "By the end of the first twenty-four hours, one fact becomes undeniable: our world has changed forever!",
                "standing on rooftop at twilight, gazing thoughtfully into the rapidly transforming horizon",
                "panoramic city sunset with surreal glowing atmospheric auroras across the sky",
                "deeply reflective"
            )
        ]
    ),

    # Act 3: Deep Scientific, Historical & Ecological Breakdown (0.28)
    (
        "Act 3: Deep Scientific, Historical & Ecological Breakdown",
        0.28,
        [
            (
                "ចូរយើងក្រឡេកមើលទៅក្នុងកម្រិតវិទ្យាសាស្ត្រ និងប្រវត្តិសាស្ត្រ ដើម្បីយល់ច្បាស់ពីយន្តការនៅពីក្រោយរឿងនេះ។",
                "Let's look into the science and history to uncover exactly how and why this phenomenon happens.",
                "wearing tiny white lab coat and round glasses, peering into a giant high-powered electron microscope",
                "futuristic science laboratory with glowing DNA double helices and floating atom models",
                "expert scientist"
            ),
            (
                "ថាមពល និងកម្លាំងធម្មជាតិ ដើរតួនាទីយ៉ាងសំខាន់ក្នុងការកំណត់ជោគវាសនារបស់ភពផែនដីយើង។",
                "The fundamental laws of energy and physics dictate the unfolding fate of our environment.",
                "drawing glowing vector diagrams and thermal flowcharts on an interactive holographic glass board",
                "dim observatory room illuminated by vibrant blue and orange thermal infographics",
                "explaining passionately"
            ),
            (
                "ខ្សែសង្វាក់អាហារ និងសត្វតូចធំទាំងអស់ ត្រូវបង្ខំចិត្តសម្របខ្លួនយ៉ាងរហ័សដើម្បីរស់រានមានជីវិត។",
                "Food webs and animal species are forced to make rapid, clever adjustments to survive.",
                "observing cartoon fish, birds, and forest animals interacting inside an enclosed experimental biosphere",
                "vibrant nature sanctuary with cascading crystal waterfalls and rare luminous flora",
                "protective naturalist"
            ),
            (
                "រុក្ខជាតិបៃតងចាប់ផ្តើមកែសម្រួលការស្រូបពន្លឺ ដើម្បីបន្តដុះលូតលាស់ក្រោមលក្ខខណ្ឌថ្មី។",
                "Green plants adjust how they absorb sunlight and air to stay alive under these unique conditions.",
                "holding a magnifying glass over a glowing green cartoon leaf, showing pulsing cellular chloroplasts",
                "high-tech botanical greenhouse with ultraviolet LED grow lights and hydroponic mist",
                "fascinated researcher"
            ),
            (
                "មហាសមុទ្រដ៏ធំល្វឹងល្វើយដែលគ្របដណ្តប់ ៧០ ភាគរយនៃផែនដី ស្រូបយកកម្តៅ និងការប្រែប្រួលគីមីយ៉ាងច្រើន។",
                "The vast oceans, covering over seventy percent of Earth, absorb massive amounts of heat and chemical changes.",
                "navigating a yellow mini-submarine through deep turquoise waters past curious cartoon sea turtles",
                "sunlit coral reef trench with shimmering turquoise water and schools of exotic colorful fish",
                "intrepid oceanographer"
            ),
            (
                "ប្រសិនបើស្ថានភាពនេះនៅតែបន្ត ផលប៉ះពាល់នឹងរាលដាលដល់គ្រប់ជ្រុងទាំងអស់នៃភពផែនដី។",
                "If these conditions persist, the effects will ripple across every single ecosystem on the globe.",
                "pointing firmly at a 3D Earth projection surrounded by glowing interconnected concentric rings",
                "planetary simulation command center with rotating high-resolution digital globe",
                "serious and analytical"
            ),
            (
                "ប៉ុន្តែធម្មជាតិមានភាពធន់ដ៏អស្ចារ្យ ដែលតែងតែស្វែងរកផ្លូវបង្កើតលំនឹងថ្មីជានិច្ច!",
                "Yet nature possesses incredible resilience, constantly finding pathways toward a new balance!",
                "smiling with awe as a tiny green seedling sprouts through a crack in solid rock",
                "sun-dappled rocky cliff where vibrant wildflowers defiantly blossom against all odds",
                "inspired and hopeful"
            )
        ]
    ),

    # Act 4: Human & Animal Ingenuity, Adaptation & Survival (0.20)
    (
        "Act 4: Human & Animal Ingenuity, Adaptation & Survival",
        0.20,
        [
            (
                "ប៉ុន្តែមនុស្សជាតិមានអាវុធដ៏អស្ចារ្យបំផុតមួយ នោះគឺភាពវៃឆ្លាត និងសមត្ថភាពក្នុងការច្នៃប្រឌិតបច្ចេកវិទ្យា!",
                "Yet humanity possesses an unmatched superpower: intellect, creativity, and technological ingenuity!",
                "standing proudly beside a high-tech modular generator glowing with friendly emerald light",
                "modern eco-shelter powered by solar arrays and kinetic turbines",
                "proud inventor"
            ),
            (
                "វិស្វករបានបង្កើតដំណោះស្រាយទំនើបៗ ដើម្បីការពារជម្រក និងធនធានចាំបាច់សម្រាប់មនុស្សគ្រប់គ្នា។",
                "Engineers deploy smart habitats and life-support systems to protect communities and vital resources.",
                "collaborating enthusiastically with robot assistants and pill companions reviewing digital architectural blueprints",
                "bustling high-tech workshop filled with friendly drone couriers and robotic assembly arms",
                "visionary builder"
            ),
            (
                "ការចែករំលែកធនធាន និងការរួបរួមសាមគ្គីភាព បានជួយសង្គ្រោះជីវិតមនុស្សរាប់លាននាក់។",
                "Kindness and community solidarity become our greatest strength, as neighbors share food and clean water.",
                "sharing a warm loaf of bread and fresh flask of clean water with a smiling neighbor",
                "cozy community gathering hall illuminated by warm fairy lights and shared hearth",
                "deeply compassionate"
            ),
            (
                "សត្វព្រៃក្នុងធម្មជាតិក៏ចេះបង្កើតយុទ្ធសាស្ត្ររស់រាន ដោយធ្វើដំណើរទៅកាន់តំបន់សុវត្ថិភាព។",
                "Wildlife adapts cleverly too, forming peaceful migration paths toward safe ecological refuges.",
                "looking through binoculars at majestic cartoon animal caravans traversing a scenic mountain trail",
                "breathtaking alpine mountain pass with snowcaps, lush pine forests, and moving herds",
                "heartened observer"
            ),
            (
                "យើងបង្កើតផ្ទះកញ្ចក់កសិកម្មទំនើប ដើម្បីផលិតបន្លែ និងអាហារស្រស់ៗដោយមិនបាច់ពឹងលើអាកាសធាតុខាងក្រៅ។",
                "Advanced greenhouses grow fresh vegetables and crops safely, ensuring a steady food supply.",
                "holding a fresh crisp cartoon carrot freshly harvested from a vertical aeroponic tower",
                "futuristic clean-room vertical farm glowing with gentle pink and purple spectra",
                "thriving innovator"
            ),
            (
                "ភាពក្លាហាន និងការមិនចុះចាញ់នេះហើយ ដែលជួយឱ្យមនុស្សជាតិឆ្លងកាត់គ្រប់វិបត្តិក្នុងប្រវត្តិសាស្ត្រ!",
                "This unyielding spirit proves once more that human ingenuity can overcome the toughest challenges!",
                "standing tall atop a hill, raising a friendly cartoon banner of unity as the wind catches it",
                "golden hour landscape with sunrise cresting over newly rebuilt eco-villages",
                "triumphant and resolute"
            )
        ]
    ),

    # Act 5: Grand Scientific Conclusion, The Bigger Lesson & Outro (0.12)
    (
        "Act 5: Grand Scientific Conclusion, The Bigger Lesson & Outro",
        0.12,
        [
            (
                "នៅទីបំផុត ការពិសោធន៍គំនិតនេះបានបង្រៀនយើងឱ្យយល់កាន់តែច្បាស់អំពីភាពអស្ចារ្យ និងតុល្យភាពនៃធម្មជាតិ។",
                "Ultimately, this What-If thought experiment teaches us profound appreciation for the balance of our planet.",
                "sitting comfortably on the crest of a grassy hill looking up into the peaceful, sparkling starry night",
                "breathtaking panoramic night sky with twinkling constellations and glowing nebula ribbons",
                "peaceful and enlightened"
            ),
            (
                "ផែនដីគឺជាជម្រកដ៏មានតម្លៃតែមួយគត់របស់យើង ហើយវិទ្យាសាស្ត្រគឺជាពន្លឺដែលជួយឱ្យយើងស្រឡាញ់ និងថែរក្សាវា។",
                "Earth is our solitary, precious home, and science is the illuminating guide that helps us protect it.",
                "holding a small sprouting green seedling in cupped hands as colorful butterflies flutter gently overhead",
                "lush blooming meadow bathed in warm morning sunshine under a crisp azure sky",
                "pure joyful hope"
            ),
            (
                "តើអ្នកគិតយ៉ាងណាដែរចំពោះសេណារីយ៉ូមួយនេះ? តើអ្នកមានទ្រឹស្តី ឬគំនិតអ្វីបន្ថែមទេ? សូមបញ្ចេញមតិយោបល់នៅខាងក្រោម!",
                "What surprised you most about this scenario? Share your thoughts and theories in the comments below!",
                "waving cheerfully with both hands, gesturing playfully toward an animated speech bubble",
                "colorful modern Kurzgesagt-style studio set with animated comment bubbles and floating badges",
                "friendly and engaging"
            ),
            (
                "សូមកុំភ្លេចចុច Like និង Subscribe ដើម្បីបន្តរុករកអាថ៌កំបាំង What-If ដ៏អស្ចារ្យជាមួយពួកយើងនៅវីដេអូបន្ទាប់!",
                "Don't forget to hit Like and Subscribe to continue exploring fascinating What-If mysteries with us in every episode!",
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
    Guarantees 100% UNIQUE scenes with ZERO duplicates, simple words, and What-If documentary storytelling.
    """
    scenes = []
    current_num = 1

    clean_topic_en = re.sub(r'^(what\s+if\s+|why\s+|how\s+)', '', title_en, flags=re.IGNORECASE).strip().rstrip('?')
    if clean_topic_en:
        clean_topic_en = clean_topic_en[0].lower() + clean_topic_en[1:]
    clean_topic_km = re.sub(r'^(ចុះបើ\s*|ហេតុអ្វី\s*)', '', title_km).strip().rstrip('?')

    # Dynamic topic-specific Intro Hook (Avoids identical telescope across all topics)
    t_lower = (title_en + " " + title_km).lower()
    if any(k in t_lower for k in ["rain", "storm", "flood", "water", "ocean", "sea", "ភ្លៀង", "ទឹក"]):
        intro_action = "holding a small colorful umbrella, gazing with wide curious eyes as atmospheric storm clouds form overhead"
        intro_env = "vibrant stylized town square as the first dramatic rain droplets and stormy mist begin to fall"
    elif any(k in t_lower for k in ["sun", "star", "space", "cosmic", "moon", "ព្រះអាទិត្យ", "ផ្កាយ"]):
        intro_action = "standing on an open rooftop observatory, gazing upward with wonder as solar flares and planetary orbits shift"
        intro_env = "panoramic twilight sky with glowing celestial bodies, star charts, and atmospheric auroras"
    elif any(k in t_lower for k in ["oxygen", "air", "breath", "gas", "atmosphere", "អុកស៊ីសែន", "ខ្យល់"]):
        intro_action = "holding an interactive holographic bubble meter, taking a deep curious breath as glowing oxygen molecules dance in the air"
        intro_env = "modern open-air botanical laboratory with glowing atmospheric particle infographics"
    elif any(k in t_lower for k in ["ice", "cold", "snow", "freeze", "glacier", "ត្រជាក់", "ទឹកកក"]):
        intro_action = "wearing a cozy wool scarf and mittens, looking in awe as frost crystals rapidly expand across nearby surfaces"
        intro_env = "chilly cartoon landscape transitioning into glistening ice crystals under a crisp pale blue sky"
    elif any(k in t_lower for k in ["fire", "volcano", "lava", "heat", "hot", "ភ្លើង", "ភ្នំភ្លើង"]):
        intro_action = "adjusting protective safety goggles, looking down at glowing thermal fissures radiating bright orange energy"
        intro_env = "dramatic volcanic observatory with glowing heat-map monitors and rising thermal plumes"
    elif any(k in t_lower for k in ["sleep", "dream", "brain", "body", "human", "គេង", "ខួរក្បាល"]):
        intro_action = "sitting comfortably on a cozy modern chair, tapping forehead curiously while looking at a glowing animated brain hologram"
        intro_env = "warm cozy bedroom studio with soft ambient lighting and glowing biometric sleep rhythm charts"
    else:
        intro_action = f"holding an interactive glowing holographic globe projecting {clean_topic_en}, eyes wide with scientific curiosity"
        intro_env = "high-tech modern curiosity studio with floating infographic charts and glowing inquiry particles"

    step_prefixes_en = [
        "In the opening phase,", "Following that,", "As conditions develop,", "Looking closer at the science,",
        "Across different regions,", "At the biological level,", "Simultaneously,",
        "From an engineering view,", "Taking a deeper look,", "Moving forward,"
    ]
    step_prefixes_km = [
        "នៅដំណាក់កាលដំបូង ", "បន្ទាប់មកទៀត ", "ស្របពេលដែលស្ថានការណ៍វិវត្តទៅមុខ ", "ក្រឡេកមើលទិដ្ឋភាពវិទ្យាសាស្ត្រ ",
        "នៅតាមតំបន់ផ្សេងៗគ្នា ", "ក្នុងកម្រិតជីវសាស្ត្រ ", "ទន្ទឹមនឹងនេះដែរ ",
        "បើគិតពីទិដ្ឋភាពវិស្វកម្ម ", "ពិនិត្យឱ្យកាន់តែច្បាស់ ", "ឈានទៅមុខមួយកម្រិតទៀត "
    ]

    for act_title, ratio, templates in ACT_PROGRESSION_BANK:
        count_for_act = max(len(templates), int(scene_count * ratio))
        for i in range(count_for_act):
            tmpl_idx = i % len(templates)
            cycle_round = i // len(templates)
            tmpl = templates[tmpl_idx]

            base_speech_km = tmpl[0].replace("{topic}", clean_topic_km)
            base_speech_en = tmpl[1].replace("{topic_en}", clean_topic_en)

            if current_num == 1:
                speech_en = base_speech_en
                speech_km = base_speech_km
                action = intro_action
                env = intro_env
            elif cycle_round > 0:
                p_en = step_prefixes_en[i % len(step_prefixes_en)]
                p_km = step_prefixes_km[i % len(step_prefixes_km)]
                speech_en = f"{p_en} {base_speech_en[0].lower() + base_speech_en[1:]}"
                speech_km = f"{p_km}{base_speech_km}"
                action = f"{tmpl[2]} (stage {cycle_round + 1} analysis)"
                env = tmpl[3]
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
