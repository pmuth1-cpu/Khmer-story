import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.prompt_generator import CHARACTER_BASE_PROMPT

sun_scenes = [
    # Act 1: The Cosmic Switch (Minute 0 to Hour 1)
    {
        'act': 'Act 1: The Cosmic Switch (Minute 0 to Hour 1)',
        'km': 'តើអ្នកធ្លាប់ឆ្ងល់ទេថា នឹងមានអ្វីកើតឡើង ប្រសិនបើព្រះអាទិត្យស្រាប់តែរលត់បាត់ក្នុងមួយប៉ព្រិចភ្នែក?',
        'en': 'Have you ever wondered what would really happen if the sun suddenly vanished from existence?',
        'action': 'holding a miniature cartoon telescope looking up at starry sky with curious wide eyes',
        'env': 'cozy observatory rooftop with starlight and glowing constellations',
        'emotion': 'deeply curious'
    },
    {
        'act': 'Act 1: The Cosmic Switch (Minute 0 to Hour 1)',
        'km': 'ក្នុងរយៈពេល ៨ នាទីកន្លះដំបូង គ្មាននរណាម្នាក់នៅលើផែនដីដឹងខ្លួននោះឡើយ! យើងនៅតែលេងសប្បាយធម្មតា!',
        'en': 'For the first eight and a half minutes, nobody on Earth would even notice! Life carries on completely normally!',
        'action': 'smiling relaxed holding a stopwatch showing 08:20 ticking rhythmically',
        'env': 'warm sunny suburban park with gentle cartoon breeze and green trees',
        'emotion': 'relaxed and intrigued'
    },
    {
        'act': 'Act 1: The Cosmic Switch (Minute 0 to Hour 1)',
        'km': 'ពីព្រោះពន្លឺព្រះអាទិត្យ និងកម្លាំងទំនាញ ត្រូវចំណាយពេលធ្វើដំណើរឆ្លងកាត់លំហអាកាសដ៏ឆ្ងាយ ទើបមកដល់យើង។',
        'en': 'Because light and gravity travel across the vast distance of space at the finite speed of light.',
        'action': 'tracing a bright yellow laser beam speeding across a miniature solar system model',
        'env': 'futuristic planetarium classroom with glowing planetary orbits in space',
        'emotion': 'analytical and smart'
    },
    {
        'act': 'Act 1: The Cosmic Switch (Minute 0 to Hour 1)',
        'km': 'ប៉ុន្តែនៅនាទីទី ៨ និង ២០ វិនាទី... ផាច់! ផ្ទៃមេឃពណ៌ខៀវស្រឡះ ស្រាប់តែប្រែជាងងឹតស្លុបភ្លាមៗ!',
        'en': 'But at precisely minute eight and twenty seconds... CLICK! The bright blue sky instantly plunges into total darkness!',
        'action': 'dropping jaw in total shock as daylight abruptly vanishes like an unlit stage',
        'env': 'city center where midday instantly plunges into midnight with sparkling stars appearing',
        'emotion': 'jaw-dropped shock'
    },
    {
        'act': 'Act 1: The Cosmic Switch (Minute 0 to Hour 1)',
        'km': 'ព្រះចន្ទក៏រលត់បាត់ភ្លាមដែរ ព្រោះព្រះចន្ទគ្មានពន្លឺខ្លួនឯងទេ គឺត្រូវពឹងលើពន្លឺព្រះអាទិត្យចាំងជះមកកាន់វា!',
        'en': 'The moon vanishes simultaneously, because it has no light of its own and only reflects the sun!',
        'action': 'pointing flashlight into the dark night sky where the moon silhouette disappeared',
        'env': 'pitch-black night sky with stars shining with eerie, crystalline sharpness',
        'emotion': 'bewildered observer'
    },
    {
        'act': 'Act 1: The Cosmic Switch (Minute 0 to Hour 1)',
        'km': 'ហើយសំខាន់ជាងនេះទៅទៀត ផែនដីបាត់បង់ខ្សែទាញ និងចាប់ផ្តើមហោះត្រង់ទៅមុខក្នុងលំហ ដូចយានអវកាសយក្ស!',
        'en': 'Even more mind-blowing: freed from the sun pull, Earth hurtles straight into deep space like a colossal spaceship!',
        'action': 'clinging to a cartoon steering wheel as glowing trajectory line breaks from elliptical orbit',
        'env': 'cosmic vista of Earth sailing smoothly away from the dark solar core into the void',
        'emotion': 'wide-eyed awe'
    },

    # Act 2: The Deep Freeze (Day 1 - 3)
    {
        'act': 'Act 2: The Deep Freeze (Day 1 - 3)',
        'km': 'ក្នុងរយៈពេល ២៤ ម៉ោងដំបូង សីតុណ្ហភាពទូទាំងពិភពលោកធ្លាក់ចុះក្រោមសូន្យ! ទឹកកកចាប់ផ្តើមកកគ្រប់ទីកន្លែង!',
        'en': 'Within twenty-four hours, temperatures worldwide plunge below the freezing point. Frost spreads everywhere.',
        'action': 'zipping up a bright red winter parka and putting on fuzzy cartoon earmuffs',
        'env': 'city streets where frost crystals rapidly web across car windshields and puddles',
        'emotion': 'shivering cold'
    },
    {
        'act': 'Act 2: The Deep Freeze (Day 1 - 3)',
        'km': 'រុក្ខជាតិ និងដើមឈើទាំងអស់ឈប់លូតលាស់ ហើយចូលគេងដើម្បីសន្សំថាមពល រង់ចាំពន្លឺថ្ងៃត្រឡប់មកវិញ។',
        'en': 'Plants stop making food and enter a dormant winter sleep, saving their energy until the sun returns.',
        'action': 'kneeling beside a cartoon garden flower that droops peacefully as its cellular activity pauses',
        'env': 'frost-covered botanical garden illuminated by amber emergency solar lamps',
        'emotion': 'tender botanist'
    },
    {
        'act': 'Act 2: The Deep Freeze (Day 1 - 3)',
        'km': 'ប៉ុន្តែយើងមិនចាំបាច់បារម្ភរឿងខ្វះខ្យល់ដកដង្ហើមទេ ព្រោះបរិយាកាសផែនដីមានអុកស៊ីសែនគ្រប់គ្រាន់សម្រាប់រាប់ពាន់ឆ្នាំ!',
        'en': 'Yet suffocating is not an immediate danger: Earth atmosphere holds enough oxygen to last us for thousands of years!',
        'action': 'checking an oxygen barometer with a reassuring cartoon smile and thumbs up',
        'env': 'scientific research bunker with air quality meters glowing steady green',
        'emotion': 'reassured and confident'
    },
    {
        'act': 'Act 2: The Deep Freeze (Day 1 - 3)',
        'km': 'សត្រូវពិតប្រាកដគឺភាពត្រជាក់! ទឹកបឹង ស្ទឹង និងទុយោទឹកតាមផ្ទះ ចាប់ផ្តើមកកជាដុំទឹកកករឹងដូចថ្ម។',
        'en': 'The true enemy is the relentless cold. Lakes, rivers, and city plumbing pipes freeze rock solid.',
        'action': 'tapping on a thick solid ice sheet that has formed over a municipal park pond',
        'env': 'frozen city park where lampposts cast golden pools over crystalline ice',
        'emotion': 'cautious investigator'
    },
    {
        'act': 'Act 2: The Deep Freeze (Day 1 - 3)',
        'km': 'រោងចក្រអគ្គិសនី និងម៉ាស៊ីនកម្តៅក្នុងផែនដី ត្រូវដំណើរការពេញកម្លាំង ដើម្បីបញ្ជូនចំហាយក្តៅទៅកម្តៅទីក្រុង។',
        'en': 'Power plants and geothermal heat stations operate at full throttle, pumping steam and warmth to communities.',
        'action': 'operating heavy glowing valve wheels to route geothermal steam into district heating pipes',
        'env': 'steamy industrial geothermal station glowing with warm orange heat pipes',
        'emotion': 'hardworking engineer'
    },
    {
        'act': 'Act 2: The Deep Freeze (Day 1 - 3)',
        'km': 'នៅថ្ងៃទី ៣ សីតុណ្ហភាពធ្លាក់ចុះដល់ ដក ២០ អង្សាសេ ហើយមនុស្សចាប់ផ្តើមរើជម្រកចូលទៅក្នុងបន្ទប់ក្រោមដី។',
        'en': 'By Day 3, temperatures sink toward minus twenty Celsius. People move down into warm, insulated underground shelters.',
        'action': 'carrying warm woolen blankets and cozy lanterns into an insulated underground shelter entrance',
        'env': 'insulated underground shelter door with warm golden light spilling out into frozen twilight',
        'emotion': 'resilient and determined'
    },

    # Act 3: Deep Sea Secrets & Subterranean Life (Day 4 - 6)
    {
        'act': 'Act 3: Deep Sea Secrets & Subterranean Life (Day 4 - 6)',
        'km': 'ផ្ទៃទឹកមហាសមុទ្រកកជាផ្ទាំងទឹកកកក្រាស់ ប៉ុន្តែវាបានក្លាយជាភួយដ៏កក់ក្តៅការពារទឹកនៅខាងក្រោមមិនឱ្យកក!',
        'en': 'Ocean surfaces freeze into thick pack ice, which surprisingly acts as an insulating blanket for the liquid water below!',
        'action': 'kneeling on a glowing iceberg examining cross-section diagram of ocean layers',
        'env': 'vast frozen ocean under star-studded cosmic sky, thick ice protecting liquid ocean below',
        'emotion': 'amazed scientist'
    },
    {
        'act': 'Act 3: Deep Sea Secrets & Subterranean Life (Day 4 - 6)',
        'km': 'នៅបាតសមុទ្រជ្រៅ សត្វចម្លែកៗមានពន្លឺភ្លឹបភ្លែតៗក្បែររន្ធភ្នំភ្លើងក្រោមទឹក មិនទាំងដឹងថាព្រះអាទិត្យបាត់ខ្លួនផង!',
        'en': 'Miles down in the ocean abyss, glowing deep-sea creatures around volcanic vents don not even notice the sun is gone!',
        'action': 'pointing excitedly through submarine viewport at glowing bioluminescent jellyfish and hydrothermal chimneys',
        'env': 'deep ocean trench with bubbling black smoker chimneys and glowing creatures',
        'emotion': 'wonderstruck explorer'
    },
    {
        'act': 'Act 3: Deep Sea Secrets & Subterranean Life (Day 4 - 6)',
        'km': 'មនុស្សជាតិបានប្រមូលផ្តុំគ្នានៅតំបន់ក្បែរកម្តៅភ្នំភ្លើងដូចជានៅអ៊ីស្លង់ ដើម្បីទាញយកថាមពលកម្ដៅធម្មជាតិមកប្រើ។',
        'en': 'Humans gather around volcanic and geothermal hotspots like Iceland, harnessing limitless natural heat.',
        'action': 'sipping hot tea beside a natural bubbling cartoon thermal spring with cozy friends',
        'env': 'indoor geothermally heated botanical dome with lush green ferns and steam baths',
        'emotion': 'cozy and grateful'
    },
    {
        'act': 'Act 3: Deep Sea Secrets & Subterranean Life (Day 4 - 6)',
        'km': 'អំពូលភ្លើង LED ជួយឱ្យយើងអាចដាំដំណាំ និងបេះផ្លែស្ត្រប៊ែរីស្រស់ៗនៅក្នុងបន្ទប់ក្រោមដីបានយ៉ាងបរិបូណ៌។',
        'en': 'Special LED grow lights allow us to harvest fresh strawberries and crisp vegetables inside high-tech underground farms.',
        'action': 'harvesting vibrant cartoon strawberries from glowing ultraviolet hydroponic racks',
        'env': 'high-tech subterranean vertical farm with rows of crisp greens and ripe red berries',
        'emotion': 'delighted gardener'
    },
    {
        'act': 'Act 3: Deep Sea Secrets & Subterranean Life (Day 4 - 6)',
        'km': 'សាមគ្គីភាព និងការចែករំលែកអាហារ បានជួយឱ្យទីក្រុងក្រោមដីដំណើរការយ៉ាងកក់ក្តៅ និងមានក្តីសង្ឃឹម។',
        'en': 'Community solidarity and sharing warm meals turn underground shelters into bustling, joyful neighborhood hubs.',
        'action': 'sharing a warm meal with diverse smiling pill friends in a communal dining hall',
        'env': 'warmly lit underground city plaza with library books, soft music, and glowing fairy lights',
        'emotion': 'inspired community leader'
    },

    # Act 4: The 7th Day Miracle (Day 7)
    {
        'act': 'Act 4: The 7th Day Miracle (Day 7)',
        'km': 'ឈានចូលដល់ថ្ងៃទី ៧ ខាងក្រៅធ្លាក់ដល់ ដក ៧០ អង្សាសេ ស្ងប់ស្ងាត់ជ្រងំដូចនៅលើភពព្រះចន្ទ។',
        'en': 'On Day 7, outside temperatures touch minus seventy degrees; the surface is silent as a lunar plain.',
        'action': 'stepping onto surface in heavy thermal astronaut spacesuit, footsteps crunching in frost',
        'env': 'surreal snow-covered metropolis frozen in crystalline glass beauty under diamond stars',
        'emotion': 'awed astronaut'
    },
    {
        'act': 'Act 4: The 7th Day Miracle (Day 7)',
        'km': 'ស្រាប់តែភ្លាមៗនោះ... ឧបករណ៍វិទ្យាសាស្ត្របានចាប់សញ្ញាទំនាញ និងកម្ដៅដ៏មហិមាមួយដែលកំពុងលេចឡើងជាថ្មី!',
        'en': 'Suddenly, deep-space gravitational detectors blare with intense incoming thermal signatures!',
        'action': 'gasping with wide sparkling eyes as detector screen spikes with radiant golden waveforms',
        'env': 'underground observatory control console lit with golden warnings and alarms',
        'emotion': 'heart-stopping anticipation'
    },
    {
        'act': 'Act 4: The 7th Day Miracle (Day 7)',
        'km': 'ពន្លឺព្រះអាទិត្យពណ៌មាសដំបូងបានចាំងកាត់លំហអាកាស មកប៉ះផ្ទៃផែនដីជាលើកដំបូងក្នុងរយៈពេល ៧ ថ្ងៃ!',
        'en': 'A blinding wave of glorious golden sunlight tears through the vacuum, striking Earth frozen crust!',
        'action': 'shielding eyes with hand as radiant golden beam of sunlight bathes face and suit',
        'env': 'frozen icy cliff edge glowing in blinding dawn light, ice diamonds sparkling like stars',
        'emotion': 'overwhelmed with joy'
    },
    {
        'act': 'Act 4: The 7th Day Miracle (Day 7)',
        'km': 'ផ្ទាំងទឹកកករលាយជាដំណក់ទឹកថ្លាឈ្វេង ហើយផ្កានិងរុក្ខជាតិចាប់ផ្តើមភ្ញាក់ដឹងខ្លួនឡើងវិញយ៉ាងអស្ចារ្យ!',
        'en': 'Sheets of frost melt into sparkling mist, and dormant flowers wake up to drink in the nourishing rays!',
        'action': 'watching frost melt away from a green cartoon leaf as it unfurls happily in the sun',
        'env': 'fast-thawing meadow with steam rising and colorful wildflowers blooming in time-lapse',
        'emotion': 'ecstatic celebration'
    },

    # Act 5: The Eternal Star & Outro
    {
        'act': 'Act 5: The Eternal Star & Outro',
        'km': 'ការពិសោធន៍គំនិត ៧ ថ្ងៃនេះ បានរំលឹកយើងឱ្យដឹងគុណចំពោះព្រះអាទិត្យ ដែលផ្តល់កម្តៅ និងជីវិតដល់យើងរាល់ថ្ងៃ។',
        'en': 'This seven-day What-If odyssey reminds us how precious our sun is—the faithful engine of all life on Earth.',
        'action': 'hugging a cute mini cartoon sun with warm sunglasses, smiling gratefully at camera',
        'env': 'lush green rolling meadow under bright blue sky with magnificent smiling sun',
        'emotion': 'deeply grateful and joyful'
    },
    {
        'act': 'Act 5: The Eternal Star & Outro',
        'km': 'ចុះអ្នកវិញ? តើអ្នកគិតថាខ្លួនឯងអាចទ្រាំរស់នៅក្រោមដី ៧ ថ្ងៃដោយគ្មានពន្លឺថ្ងៃបានទេ? ខមមិនប្រាប់ផងណា!',
        'en': 'How would you have spent your seven days without sunlight? Tell us your survival ideas in the comments below!',
        'action': 'waving enthusiastically, pointing playfully at cartoon comment box below',
        'env': 'Kurzgesagt-style colorful outro screen with floating likes, comments, and bell icons',
        'emotion': 'friendly and engaging'
    },
    {
        'act': 'Act 5: The Eternal Star & Outro',
        'km': 'សូមកុំភ្លេចចុច Like និង Subscribe ដើម្បីបន្តរុករកអាថ៌កំបាំង What-If ដ៏អស្ចារ្យជាមួយពួកយើងនៅវីដេអូបន្ទាប់!',
        'en': 'Be sure to like and subscribe to continue exploring the fascinating mysteries of the universe with us!',
        'action': 'jumping with thumbs up as giant animated red Subscribe button clicks with sparkling golden stars',
        'env': 'colorful celebration outro with confetti and sparkling fireworks',
        'emotion': 'triumphant and smiling'
    }
]

def main():
    os.makedirs('custom_scripts', exist_ok=True)
    scenes = []
    for idx, s in enumerate(sun_scenes, start=1):
        fp = (
            f"{CHARACTER_BASE_PROMPT} "
            f"The cute pill character is {s['emotion']}, {s['action']}. "
            f"Setting: {s['env']}. "
            f"2D flat vector, Kurzgesagt aesthetic, vibrant colors, 16:9 ratio."
        )
        scenes.append({
            'scene_num': idx,
            'act': s['act'],
            'duration_hint': 7.5,
            'khmer_speech': s['km'],
            'english_speech': s['en'],
            'action': s['action'],
            'environment': s['env'],
            'emotion': s['emotion'],
            'full_prompt': fp
        })

    script_obj = {
        'title_en': 'What If the Sun Disappeared for 7 Days?',
        'title_km': 'ចុះបើព្រះអាទិត្យបាត់ខ្លួនរយៈពេល ៧ ថ្ងៃ?',
        'total_scenes': len(scenes),
        'estimated_duration_minutes': 8,
        'scenes': scenes
    }

    # Save to both sun_disappears.json and What_If_The_Sun_Disappeared_for_7_Days.json
    paths = [
        os.path.join('custom_scripts', 'sun_disappears.json'),
        os.path.join('custom_scripts', 'What_If_The_Sun_Disappeared_for_7_Days.json')
    ]
    for p in paths:
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(script_obj, f, ensure_ascii=False, indent=2)
        print(f"Saved {p} with {len(scenes)} unique scenes.")

if __name__ == '__main__':
    main()
