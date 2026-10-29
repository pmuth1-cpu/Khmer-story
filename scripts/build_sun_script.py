import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.prompt_generator import CHARACTER_BASE_PROMPT

sun_scenes = [
    # Act 1: The Inciting Hook & First 8.5 Minutes
    {
        'act': 'Act 1: The Cosmic Switch (Minute 0 to Hour 1)',
        'km': 'តើអ្នកធ្លាប់ឆ្ងល់ទេថា នឹងមានអ្វីកើតឡើង ប្រសិនបើព្រះអាទិត្យស្រាប់តែរលត់បាត់ក្នុងមួយប៉ព្រិចភ្នែក?',
        'en': 'Have you ever wondered what would happen if the sun suddenly vanished from existence in the blink of an eye?',
        'action': 'holding a miniature cartoon telescope looking up at starry sky with curious wide eyes',
        'env': 'cozy observatory rooftop with starlight and glowing constellations',
        'emotion': 'deeply curious'
    },
    {
        'act': 'Act 1: The Cosmic Switch (Minute 0 to Hour 1)',
        'km': 'ក្នុងរយៈពេល ៨ នាទីកន្លះដំបូង គ្មាននរណាម្នាក់នៅលើផែនដីដឹងខ្លួននោះឡើយ!',
        'en': 'For the first eight and a half minutes, nobody on Earth would even notice anything was wrong!',
        'action': 'smiling relaxed holding a stopwatch showing 08:20 ticking rhythmically',
        'env': 'warm sunny suburban park with gentle cartoon breeze and green trees',
        'emotion': 'relaxed and intrigued'
    },
    {
        'act': 'Act 1: The Cosmic Switch (Minute 0 to Hour 1)',
        'km': 'ពីព្រោះពន្លឺព្រះអាទិត្យ និងទំនាញត្រូវចំណាយពេលធ្វើដំណើរក្នុងល្បឿន ៣ សែនគីឡូម៉ែត្រក្នុងមួយវិនាទី។',
        'en': 'Because light and gravity travel across the 150-million-kilometer cosmic gulf at the finite speed of light.',
        'action': 'tracing a bright yellow laser beam speeding across a miniature solar system model',
        'env': 'futuristic planetarium classroom with glowing planetary orbits in space',
        'emotion': 'analytical and smart'
    },
    {
        'act': 'Act 1: The Cosmic Switch (Minute 0 to Hour 1)',
        'km': 'ប៉ុន្តែនៅនាទីទី ៨ និង ២០ វិនាទី ផ្ទៃមេឃពណ៌ខៀវស្រងាត់នឹងប្រែទៅជាភាពងងឹតទាំងស្រុងភ្លាមៗ!',
        'en': 'But at precisely eight minutes and twenty seconds, the azure blue sky instantly snuffs out into total blackness!',
        'action': 'dropping jaw in total shock as daylight abruptly vanishes like an unlit stage',
        'env': 'city center where midday instantly plunges into midnight with sparkling stars appearing',
        'emotion': 'jaw-dropped shock'
    },
    {
        'act': 'Act 1: The Cosmic Switch (Minute 0 to Hour 1)',
        'km': 'ព្រះចន្ទនៅលើផ្ទៃមេឃក៏រលត់បាត់ភ្លាមៗដែរ ព្រោះគ្មានពន្លឺព្រះអាទិត្យចាំងជះមកកាន់វាទៀតឡើយ។',
        'en': 'The moon vanishes from the heavens simultaneously, as it possesses no light of its own to reflect.',
        'action': 'pointing flashlight into the dark night sky where the moon silhouette disappeared',
        'env': 'pitch-black night sky with stars shining with eerie, crystalline sharpness',
        'emotion': 'bewildered observer'
    },
    {
        'act': 'Act 1: The Cosmic Switch (Minute 0 to Hour 1)',
        'km': 'ហើយសំខាន់ជាងនេះទៅទៀត ផែនដីបានបាត់បង់ទំនាញទាញ និងចាប់ផ្តើមហោះត្រង់ទៅក្នុងលំហអាកាសដ៏ធំល្វឹងល្វើយ!',
        'en': 'Even more staggering: freed from the sun gravitational anchor, Earth hurtles into deep space along a straight line!',
        'action': 'clinging to a cartoon steering wheel as glowing trajectory line breaks from elliptical orbit',
        'env': 'cosmic vista of Earth sailing smoothly away from the dark solar core into the void',
        'emotion': 'wide-eyed awe'
    },

    # Act 2: Day 1 to 3 - The Rapid Freezing (Scenes 7-18)
    {
        'act': 'Act 2: The Deep Freeze (Day 1 - 3)',
        'km': 'ក្នុងរយៈពេល ២៤ ម៉ោងដំបូង សីតុណ្ហភាពទូទាំងពិភពលោកចាប់ផ្តើមធ្លាក់ចុះជាមធ្យមក្រោម ០ អង្សាសេ។',
        'en': 'Within twenty-four hours, global surface temperatures drop sharply below the freezing point.',
        'action': 'zipping up a bright red winter parka and putting on fuzzy cartoon earmuffs',
        'env': 'city streets where frost crystals rapidly web across car windshields and puddles',
        'emotion': 'shivering cold'
    },
    {
        'act': 'Act 2: The Deep Freeze (Day 1 - 3)',
        'km': 'រស្មីសំយោគរបស់រុក្ខជាតិទាំងអស់នៅលើពិភពលោកត្រូវឈប់ដំណើរការទាំងស្រុង។',
        'en': 'Photosynthesis everywhere on the planet halts completely, freezing the baseline of terrestrial food webs.',
        'action': 'kneeling beside a cartoon garden flower that droops peacefully as its cellular activity pauses',
        'env': 'frost-covered botanical garden illuminated by amber emergency solar lamps',
        'emotion': 'tender botanist'
    },
    {
        'act': 'Act 2: The Deep Freeze (Day 1 - 3)',
        'km': 'ប៉ុន្តែយើងមិនចាំបាច់បារម្ភរឿងខ្វះអុកស៊ីសែនភ្លាមៗទេ ព្រោះបរិយាកាសផែនដីមានអុកស៊ីសែនគ្រប់គ្រាន់សម្រាប់រាប់ពាន់ឆ្នាំ!',
        'en': 'Yet suffocating is not an immediate danger: Earth atmosphere holds enough oxygen to sustain humanity for millennia!',
        'action': 'checking an oxygen barometer with a reassuring cartoon smile and thumbs up',
        'env': 'scientific research bunker with air quality meters glowing steady green',
        'emotion': 'reassured and confident'
    },
    {
        'act': 'Act 2: The Deep Freeze (Day 1 - 3)',
        'km': 'បញ្ហាពិតប្រាកដគឺភាពត្រជាក់ដ៏សែនកាចសាហាវ ដែលចាប់ផ្តើមបង្កកបឹង ស្ទឹង និងប្រព័ន្ធទឹកទូទាំងពិភពលោក។',
        'en': 'The true mortal adversary is the relentless cold, rapidly freezing lakes, rivers, and plumbing pipes solid.',
        'action': 'tapping on a thick solid ice sheet that has formed over a municipal park pond',
        'env': 'frozen city park where lampposts cast golden pools over crystalline ice',
        'emotion': 'cautious investigator'
    },
    {
        'act': 'Act 2: The Deep Freeze (Day 1 - 3)',
        'km': 'រោងចក្រថាមពលអគ្គិសនីដើរដោយធ្យូងថ្ម នុយក្លេអ៊ែរ និងកម្តៅក្នុងផែនដី ត្រូវដំណើរការអស់សមត្ថភាពដើម្បីរក្សាកម្ដៅ។',
        'en': 'Nuclear and geothermal plants operate at full throttle, funneling steam and heating to urban communities.',
        'action': 'operating heavy glowing valve wheels to route geothermal steam into district heating pipes',
        'env': 'steamy industrial geothermal station glowing with warm orange heat pipes',
        'emotion': 'hardworking engineer'
    },
    {
        'act': 'Act 2: The Deep Freeze (Day 1 - 3)',
        'km': 'នៅថ្ងៃទី ៣ សីតុណ្ហភាពបានធ្លាក់ចុះដល់ ដក ២០ អង្សាសេ ហើយមនុស្សចាប់ផ្តើមរើជម្រកចូលទៅក្រោមដី។',
        'en': 'By Day 3, surface temperatures plunge toward minus twenty Celsius, prompting migrations into subterranean shelters.',
        'action': 'carrying warm woolen blankets and cozy lanterns into an insulated underground shelter entrance',
        'env': 'insulated underground shelter door with warm golden light spilling out into frozen twilight',
        'emotion': 'resilient and determined'
    },

    # Act 3: Day 4 to 6 - Subterranean & Ocean Survival (Scenes 13-24)
    {
        'act': 'Act 3: The Ocean Abyss & Deep Geothermal Life (Day 4 - 6)',
        'km': 'ផ្ទៃទឹកមហាសមុទ្រចាប់ផ្តើមកកជាផ្ទាំងទឹកកកកម្រាស់រាប់ម៉ែត្រ ប៉ុន្តែវាបានក្លាយជាភួយការពារទឹកនៅខាងក្រោម!',
        'en': 'Ocean surfaces freeze into thick sheets of pack ice, which paradoxically acts as an insulating blanket!',
        'action': 'kneeling on a glowing iceberg examining cross-section diagram of ocean layers',
        'env': 'vast frozen ocean under star-studded cosmic sky, thick ice protecting liquid ocean below',
        'emotion': 'amazed scientist'
    },
    {
        'act': 'Act 3: The Ocean Abyss & Deep Geothermal Life (Day 4 - 6)',
        'km': 'នៅបាតសមុទ្រជ្រៅ សត្វចម្លែកៗដែលរស់នៅក្បែររន្ធកម្ដៅភ្នំភ្លើងក្រោមទឹក មិនទាំងដឹងថាព្រះអាទិត្យបាត់ខ្លួនផង!',
        'en': 'Miles below in the oceanic abyss, bizarre creatures around volcanic hydrothermal vents don not even know the sun is gone!',
        'action': 'pointing excitedly through submarine viewport at glowing bioluminescent jellyfish and hydrothermal chimneys',
        'env': 'deep ocean trench with bubbling black smoker chimneys and glowing creatures',
        'emotion': 'wonderstruck explorer'
    },
    {
        'act': 'Act 3: The Ocean Abyss & Deep Geothermal Life (Day 4 - 6)',
        'km': 'មនុស្សជាតិបានប្រមូលផ្តុំគ្នានៅតាមតំបន់ក្បែរកម្តៅភ្នំភ្លើងក្រោមដីដូចជានៅអ៊ីស្លង់ ដើម្បីទាញយកថាមពលកម្ដៅឥតដែនកំណត់។',
        'en': 'Humans gather around volcanic and geothermal hotspots like Iceland, harnessing limitless planetary heat.',
        'action': 'sipping hot tea beside a natural bubbling cartoon thermal spring with cozy friends',
        'env': 'indoor geothermally heated botanical dome with lush green ferns and steam baths',
        'emotion': 'cozy and grateful'
    },
    {
        'act': 'Act 3: The Ocean Abyss & Deep Geothermal Life (Day 4 - 6)',
        'km': 'បច្ចេកវិទ្យាអំពូលភ្លើង LED ជួយឱ្យយើងអាចដាំដំណាំ និងបន្លែស្រស់ៗនៅក្នុងបន្ទប់ក្រោមដីបានយ៉ាងបរិបូណ៌។',
        'en': 'Artificial LED farming flourishes underground, producing crisp vegetables bathed in specialized wavelengths.',
        'action': 'harvesting vibrant cartoon strawberries from glowing ultraviolet hydroponic racks',
        'env': 'high-tech subterranean vertical farm with rows of crisp greens and ripe red berries',
        'emotion': 'delighted gardener'
    },
    {
        'act': 'Act 3: The Ocean Abyss & Deep Geothermal Life (Day 4 - 6)',
        'km': 'សាមគ្គីភាព និងការបែងចែកថាមពលដោយយុត្តិធម៌ បានជួយឱ្យទីក្រុងក្រោមដីដំណើរការយ៉ាងរលូន។',
        'en': 'Equitable energy sharing and community solidarity turn subterranean bunkers into warm, bustling miniature cities.',
        'action': 'sharing a warm meal with diverse smiling pill friends in a communal dining hall',
        'env': 'warmly lit underground city plaza with library books, soft music, and glowing fairy lights',
        'emotion': 'inspired community leader'
    },

    # Act 4: Day 7 - The Climax & Cosmic Return (Scenes 18-28)
    {
        'act': 'Act 4: The 7th Day Miracle (Day 7)',
        'km': 'ឈានចូលដល់ថ្ងៃទី ៧ សីតុណ្ហភាពខាងក្រៅបានធ្លាក់ចុះដល់ ដក ៧០ អង្សាសេ បរិយាកាសស្ងប់ស្ងាត់ដូចនៅលើភពព្រះចន្ទ។',
        'en': 'On Day 7, outside temperatures touch minus seventy degrees; the surface is silent as a lunar plain.',
        'action': 'stepping onto surface in heavy thermal astronaut spacesuit, footsteps crunching in frost',
        'env': 'surreal snow-covered metropolis frozen in crystalline glass beauty under diamond stars',
        'emotion': 'awed astronaut'
    },
    {
        'act': 'Act 4: The 7th Day Miracle (Day 7)',
        'km': 'ស្រាប់តែភ្លាមៗនោះ ឧបករណ៍សញ្ញាវិទ្យាសាស្ត្របានចាប់សញ្ញាទំនាញ និងកម្ដៅដ៏មហិមាមួយដែលកំពុងលេចឡើងជាថ្មី!',
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
        'km': 'ផ្ទាំងទឹកកកចាប់ផ្តើមរលាយជាដំណក់ទឹកថ្លាឈ្វេង ហើយផ្កានិងរុក្ខជាតិចាប់ផ្តើមភ្ញាក់ដឹងខ្លួនឡើងវិញយ៉ាងអស្ចារ្យ!',
        'en': 'Sheets of frost vaporize into sparkling mist, and dormant seeds awaken to drink in the nourishing rays!',
        'action': 'watching frost melt away from a green cartoon leaf as it unfurls happily in the sun',
        'env': 'fast-thawing meadow with steam rising and colorful wildflowers blooming in time-lapse',
        'emotion': 'ecstatic celebration'
    },

    # Act 5: Grand Conclusion & Outro
    {
        'act': 'Act 5: The Eternal Star & Outro',
        'km': 'ព្រឹត្តិការណ៍ ៧ ថ្ងៃនេះបានរំលឹកយើងឱ្យដឹងគុណចំពោះព្រះអាទិត្យ ដែលផ្តល់ពន្លឺ និងជីវិតដល់យើងរាល់ថ្ងៃដោយមិនគិតថ្លៃ!',
        'en': 'This seven-day odyssey reminds us how precious our sun is—the free, faithful engine of all life on Earth!',
        'action': 'hugging a cute mini cartoon sun with warm sunglasses, smiling gratefully at camera',
        'env': 'lush green rolling meadow under bright blue sky with magnificent smiling sun',
        'emotion': 'deeply grateful and joyful'
    },
    {
        'act': 'Act 5: The Eternal Star & Outro',
        'km': 'តើអ្នកយល់យ៉ាងណាដែរ ប្រសិនបើអ្នកត្រូវរស់នៅក្រោមដី ៧ ថ្ងៃ? សូមបញ្ចេញមតិយោបល់របស់អ្នកនៅខាងក្រោម!',
        'en': 'How would you have spent your seven days in the dark? Tell us your survival strategy in the comments below!',
        'action': 'waving enthusiastically, pointing playfully at cartoon comment box below',
        'env': 'Kurzgesagt-style colorful outro screen with floating likes, comments, and bell icons',
        'emotion': 'friendly and engaging'
    },
    {
        'act': 'Act 5: The Eternal Star & Outro',
        'km': 'សូមកុំភ្លេចចុច Like និង Subscribe ដើម្បីបន្តរុករកអាថ៌កំបាំងចក្រវាលដ៏អស្ចារ្យជាមួយពួកយើងនៅវីដេអូបន្ទាប់!',
        'en': 'Be sure to like and subscribe to continue exploring the mysteries of the cosmos with us in every episode!',
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
