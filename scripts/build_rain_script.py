import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.prompt_generator import CHARACTER_BASE_PROMPT

scenes_data = [
    # Act 1: The Unbroken Downpour (Day 1 - 2)
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'តើអ្នកធ្លាប់ឆ្ងល់ទេថា នឹងមានអ្វីកើតឡើង ប្រសិនបើភ្លៀងធ្លាក់មិនឈប់ទាល់តែសោះ រយៈពេល ៣០ ថ្ងៃជាប់ៗគ្នា?',
        'en': 'Have you ever wondered what would happen if rain fell continuously without stopping for thirty whole days?',
        'action': 'holding a tiny yellow umbrella, staring up at dark grey stormy clouds with curious round eyes',
        'env': 'cozy cartoon street as first heavy raindrops begin to splash into glowing puddles',
        'emotion': 'deeply curious'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'នៅថ្ងៃដំបូង មនុស្សភាគច្រើនគិតថាវាគ្រាន់តែជាអាកាសធាតុត្រជាក់ស្រួល អង្គុយផឹកកាហ្វេ និងស្តាប់សូរទឹកភ្លៀង។',
        'en': 'On Day 1, most people simply enjoy the cozy weather, sipping hot coffee and listening to the soothing raindrops.',
        'action': 'sitting inside a warm coffee shop window holding a steaming mug, watching cartoon rain droplets glide down glass',
        'env': 'warm pastel cafe interior with soft golden lights contrasting with rainy blue window',
        'emotion': 'relaxed and peaceful'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'ប៉ុន្តែនៅថ្ងៃទី ២ ភ្លៀងនៅតែធ្លាក់យ៉ាងគំហុកដោយគ្មានការថមថយសូម្បីតែមួយវិនាទី! មេឃគ្មានសញ្ញាថានឹងរាំងឡើយ។',
        'en': 'But on Day 2, the rain keeps pouring violently without a single second of pause. There is zero sign of stopping.',
        'action': 'peering through blinds with growing suspicion, checking digital weather forecast on tablet showing 100% rain icon',
        'env': 'living room with rain hammering loudly against windowpanes, gloomy grey sky',
        'emotion': 'slightly concerned and puzzled'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'ប្រព័ន្ធលូក្នុងទីក្រុងចាប់ផ្តើមពេញហៀរ ហើយផ្លូវថ្នល់មួយចំនួនចាប់ផ្តើមក្លាយជាស្ទឹងហូរទឹកតូចៗ។',
        'en': 'City storm drains quickly overflow, and suburban streets begin transforming into shallow flowing rivers.',
        'action': 'wearing bright red rubber rain boots, stepping cautiously into water rising over sidewalk curb',
        'env': 'city intersection where water gushes up out of storm grates like bubbling fountains',
        'emotion': 'cautious and observant'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'ដីធម្មជាតិស្រូបយកទឹកដល់កម្រិតឆ្អែត ធ្វើឱ្យសួនច្បារ និងវាលស្មៅប្រែទៅជាភក់ជ្រាំដ៏រអិល។',
        'en': 'Park lawns absorb water to their absolute limit, turning into squishy, slippery mud zones.',
        'action': 'standing in a suburban park where cartoon earth squelches muddy bubbles beneath feet',
        'env': 'city park with saturated marshy grass, puddles merging into a vast shallow pond',
        'emotion': 'surprised and uneasy'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'ពពកខ្មៅក្រាស់ឃ្មឹកបានបាំងពន្លឺព្រះអាទិត្យទាំងស្រុង ធ្វើឱ្យពេលថ្ងៃត្រង់មើលទៅដូចពេលយប់អញ្ចឹង។',
        'en': 'Colossal storm clouds blot out the sun entirely, plunging the city into an eerie midday twilight.',
        'action': 'holding a glowing flashlight upwards toward ominous purple-grey ceiling of endless clouds',
        'env': 'dim city square at midday, streetlamps flickering on automatically beneath dark cloud canopy',
        'emotion': 'intimidated and solemn'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'តើទឹកភ្លៀងរាប់ពាន់លានតោននេះមកពីណា? វាដូចជាមានទន្លេទឹកបរិយាកាសនៅលើមេឃកំពុងចាក់ទឹកមកក្រោម!',
        'en': 'Where does all this water come from? A massive atmospheric river in the sky is dumping billions of tons of moisture.',
        'action': 'pointing at a holographic 3D Earth showing swirling white atmospheric moisture ribbons across oceans',
        'env': 'high-tech meteorological observatory with weather radars glowing cyan and green',
        'emotion': 'analytical and fascinated'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'សីតុណ្ហភាពធ្លាក់ចុះជាលំដាប់ ហើយសំណើមក្នុងខ្យល់ឡើងដល់ ១០០ ភាគរយឥតឈប់ឈរ។',
        'en': 'Temperatures drop steadily as relative humidity locks at a maximum one hundred percent.',
        'action': 'checking an analog wall barometer and thermometer with needle pinned at maximum humidity',
        'env': 'foggy interior hallway where moisture condenses on metal door handles and cool mirrors',
        'emotion': 'shivering slightly'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'សត្វស្លាបតូចៗត្រូវប្រញាប់ស្វែងរកជម្រក ព្រោះគ្រាប់ភ្លៀងធ្លាក់មកខ្លាំងដូចជាគ្រាប់កាំភ្លើងតូចៗ។',
        'en': 'Little birds desperately seek shelter, unable to fly as heavy raindrops pelt down like tiny pebbles.',
        'action': 'gently guiding tiny soaked cartoon sparrows into a dry hollow wooden tree shelter',
        'env': 'leafy forest branch trembling under torrential bombardment of fat raindrops',
        'emotion': 'protective and compassionate'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'ចរាចរណ៍តាមដងផ្លូវធំៗចាប់ផ្តើមជាប់គាំង ដោយសាររថយន្តតូចៗមិនអាចបើកបរឆ្លងកាត់ទឹកជ្រៅបានឡើយ។',
        'en': 'Major roadways grind to a complete halt as passenger cars stall in the rising floodwaters.',
        'action': 'standing on a highway pedestrian bridge, looking down at rows of headlights reflected in water',
        'env': 'rain-slicked expressway submerged under three feet of water, emergency hazard lights blinking',
        'emotion': 'worried and watchful'
    },

    # Act 2: The Sinking World (Day 3 - 7)
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'ឈានចូលដល់ថ្ងៃទី ៤ កម្រិតទឹកនៅក្នុងទន្លេធំៗបានហក់ឡើងជិតដល់មាត់ទំនប់ការពារទឹកជំនន់។',
        'en': 'By Day 4, river levels worldwide surge dangerously close to the very top edge of concrete floodwalls.',
        'action': 'standing on a concrete flood levee with measuring stick showing water rising past yellow safety line',
        'env': 'turbulent muddy river foaming against massive concrete floodwalls under pounding rain',
        'emotion': 'tense and anxious'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'ដីក្រោមគ្រឹះផ្លូវថ្នល់ចាប់ផ្តើមជ្រាយ បង្កឱ្យមានការស្រុតដី និងទឹកផុសចេញពីក្រោមដី។',
        'en': 'Waterlogged subsoil beneath roads softens, triggering cracks and bubbling mini-springs along sidewalks.',
        'action': 'kneeling down examining cracked asphalt where water bubbles up from underground soil',
        'env': 'suburban street with curved cracks appearing in pavement as road foundation sags',
        'emotion': 'investigative and alarmed'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'រថភ្លើងក្រោមដីត្រូវផ្អាកដំណើរការទាំងស្រុង ដោយសារទឹកហូរធ្លាក់តាមកាំជណ្តើរដូចទឹកធ្លាក់កម្សាន្ត។',
        'en': 'Underground subways shut down completely as floodwaters cascade down station stairs like waterfalls.',
        'action': 'standing behind safety barricade looking down subway entrance overflowing with gushing water',
        'env': 'metro station entrance with emergency yellow tape, water roaring down tiled escalators',
        'emotion': 'shocked'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'ផ្ទះរាប់ពាន់ខ្នងត្រូវទឹកលិចជាន់ក្រោម ហើយប្រជាជនត្រូវរើស្បៀង និងខ្នើយភួយឡើងទៅជាន់ខាងលើ។',
        'en': 'Thousands of suburban ground floors are submerged, forcing families to move supplies and bedding upstairs.',
        'action': 'carrying boxes of dry supplies and cute pillows up a spiral staircase inside home',
        'env': 'living room with floating furniture and water halfway up sofa cushions',
        'emotion': 'frantic but resilient'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'ការដាច់ចរន្តអគ្គិសនីចាប់ផ្តើមរាលដាល ពីព្រោះស្ថានីយបំប្លែងភ្លើងក្រោមដីត្រូវបានទឹកជន់លិច។',
        'en': 'Rolling power outages strike as electrical substations short-circuit under standing water.',
        'action': 'holding a warm glowing lantern as room lights suddenly pop and flicker out completely',
        'env': 'dark apartment illuminated only by handheld lantern and flashes of outdoor lightning',
        'emotion': 'startled'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'កង្វះពន្លឺព្រះអាទិត្យធ្វើឱ្យរុក្ខជាតិក្នុងផើងផ្កាស្រពោន ហើយស្លឹកឈើចាប់ផ្តើមប្រែជាពណ៌លឿងស្លេក។',
        'en': 'The complete absence of direct sunlight suppresses plant growth, turning potted leaves pale and yellow.',
        'action': 'inspecting a droopy cartoon potted plant whose leaves are losing green pigmentation',
        'env': 'indoor windowsill garden drenched in gloomy dim mist, pale yellowing leaves',
        'emotion': 'worried botanist'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'ផ្សិតតូចៗ និងពពួកបាក់តេរីសំណើមចាប់ផ្តើមដុះលូតលាស់យ៉ាងលឿនតាមជញ្ជាំង និងជ្រុងផ្ទះ។',
        'en': 'Tiny damp-loving mushrooms and velvety green moss sprout quickly across humid corners and baseboards.',
        'action': 'shining UV magnifying glass at cartoon green spores sprouting along wall baseboard',
        'env': 'damp room corner with velvety green moss and tiny cartoon mushrooms sprouting',
        'emotion': 'disgusted and cautious'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'នៅតាមជនបទ ស្រែចម្ការដំណាំកសិកម្មរាប់ម៉ឺនហិកតាត្រូវលិចលង់ក្រោមផ្ទៃទឹកពណ៌ត្នោត។',
        'en': 'Across the countryside, farmland vanishes under a vast sea of brown water, with only tractor roofs peeking out.',
        'action': 'riding a rescue dinghy through flooded farm fields, looking at submerged tractor roofs',
        'env': 'vast submerged agricultural valley where only treetops and telephone poles emerge from water',
        'emotion': 'heartbroken observer'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'សត្វព្រៃគួរឱ្យស្រឡាញ់ដូចជាកូនទន្សាយ និងកញ្ជ្រោង នាំគ្នារត់ឡើងទៅលើកំពូលទួលខ្ពស់ៗដើម្បីសុវត្ថិភាព។',
        'en': 'Cute forest critters—bunnies, foxes, and deer—gather peacefully together on shrinking high knolls to stay dry.',
        'action': 'looking through binoculars at a group of cartoon forest critters huddled safely on a high rock knoll',
        'env': 'flooded forest canopy with animals sharing dry branches peacefully',
        'emotion': 'deeply moved and observant'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'ទឹកស្អាតសម្រាប់បរិភោគចាប់ផ្តើមក្លាយជាបញ្ហាចម្បង ព្រោះរោងចក្រចម្រោះទឹកត្រូវរងការលិចលង់។',
        'en': 'Clean drinking water becomes scarce as municipal treatment stations get swamped by contaminated runoff.',
        'action': 'holding a glass water bottle under a dripping faucet that coughs out brown murky water',
        'env': 'kitchen with stockpiled water jugs and boiling pots on emergency camping stove',
        'emotion': 'troubled'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'ក្រុមជួយសង្គ្រោះប្រើប្រាស់ទូកកៅស៊ូ និងឧទ្ធម្ភាគចក្រដើម្បីទម្លាក់ស្បៀងអាហារដល់អ្នកជាប់គាំងលើដំបូល។',
        'en': 'First responders deploy rubber rafts and helicopters to drop fresh rations and water to stranded rooftop residents.',
        'action': 'waving from a rooftop with bright orange signal flag towards a friendly cartoon rescue helicopter',
        'env': 'rainy rooftop island surrounded by miles of floodwaters, helicopter lowering cargo sling',
        'emotion': 'relieved and grateful'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'នៅចុងសប្តាហ៍ទីមួយ មនុស្សគ្រប់រូបចាប់ផ្តើមឆ្ងល់ថា៖ តើព្រះអាទិត្យនឹងរះឡើងវិញនៅពេលណា?',
        'en': 'By the close of week one, the quiet question sinks in: will our warm sunny friend ever shine again?',
        'action': 'sitting on rooftop ledge wearing yellow raincoat, gazing out into the relentless curtain of grey rain',
        'env': 'sweeping panoramic view of flooded metropolis shimmering with ripples in stormy twilight',
        'emotion': 'deeply contemplative'
    },

    # Act 3: Ecological Shifts & The Floating World (Day 8 - 15)
    {
        'act': 'Act 3: Ecological Shifts & The Floating World (Day 8 - 15)',
        'km': 'ចូលដល់សប្តាហ៍ទី ២ សម្ពាធទឹកដ៏មហិមាបានបង្ខំឱ្យទំនប់វារីអគ្គិសនីត្រូវបើកទ្វារទឹកបាញ់កម្សាន្តដូចទឹកជ្រោះយក្ស។',
        'en': 'Entering week two, immense water pressure forces hydroelectric dams to unleash roaring emergency spillways.',
        'action': 'standing on a dam observation tower watching colossal roaring white foam geysers exploding from sluice gates',
        'env': 'gigantic concrete hydroelectric dam with roaring discharge gates blasting into downstream canyon',
        'emotion': 'awe-struck and frightened'
    },
    {
        'act': 'Act 3: Ecological Shifts & The Floating World (Day 8 - 15)',
        'km': 'នៅតាមតំបន់ភ្នំ ដីភ្នំទាំងមូលដែលជ្រាបទឹកខ្លាំងចាប់ផ្តើមបាក់ស្រុត បង្កជាគ្រោះបាក់ដីដែលត្រូវប្រុងប្រយ័ត្ន។',
        'en': 'In mountain regions, saturated hillside soil gives way, creating dangerous mudslides that block roadways.',
        'action': 'pointing safety whistle to guide cartoon vehicles away from crumbling hillside road',
        'env': 'steep mountain road where muddy torrents and dislodged boulders crash into safety barriers',
        'emotion': 'urgent and brave'
    },
    {
        'act': 'Act 3: Ecological Shifts & The Floating World (Day 8 - 15)',
        'km': 'ទម្ងន់ទឹកភ្លៀងរាប់ពាន់លានតោនដែលធ្លាក់លើដី បានធ្វើឱ្យឧបករណ៍វាស់រំញ័រដីកម្រើកឡើងយ៉ាងច្បាស់។',
        'en': 'Trillions of tons of newly added surface water exert tangible weight on the crust, recorded on delicate seismographs.',
        'action': 'studying seismograph machine with needle tracing delicate vibration ripples across paper drum',
        'env': 'geophysical underground vault with digital Earth crust stress maps glowing crimson',
        'emotion': 'scientific precision'
    },
    {
        'act': 'Act 3: Ecological Shifts & The Floating World (Day 8 - 15)',
        'km': 'ជាតិអំបិលនៅក្នុងទឹកសមុទ្រនៅតាមមាត់ឆ្នេរចាប់ផ្តើមធ្លាក់ចុះ ដោយសារទឹកភ្លៀងសាបដ៏ច្រើនហូរចូល។',
        'en': 'Ocean salinity along coastal bays drops sharply as monstrous volumes of freshwater dilute the shoreline.',
        'action': 'dipping a hydrometer testing tube into coastal water to measure salt salinity levels',
        'env': 'coastal bay where brown freshwater plume collides with emerald ocean tide',
        'emotion': 'curious researcher'
    },
    {
        'act': 'Act 3: Ecological Shifts & The Floating World (Day 8 - 15)',
        'km': 'ការប្រែប្រួលជាតិប្រៃនេះ ធ្វើឱ្យត្រីត្លុក និងផ្កាថ្មតាមឆ្នេរសមុទ្ររងការប៉ះពាល់យ៉ាងខ្លាំង។',
        'en': 'This sudden salinity change temporarily disorients coastal fish species and delicate coral reefs.',
        'action': 'peering through underwater observation window at bewildered cartoon clownfish hovering near pale corals',
        'env': 'underwater reef station where freshwater turbidity clouds the vibrant reef ecosystem',
        'emotion': 'empathetic and concerned'
    },
    {
        'act': 'Act 3: Ecological Shifts & The Floating World (Day 8 - 15)',
        'km': 'នៅក្នុងទីក្រុង មនុស្សចាប់ផ្តើមច្នៃក្បូនជ័រពណ៌ខៀវ ដើម្បីអុំទូកធ្វើដំណើរទៅរកម្ហូបអាហារដូចទីក្រុង Venice។',
        'en': 'In submerged city streets, citizens build clever makeshift rafts out of plastic drums, paddling like in Venice.',
        'action': 'cheerfully paddling a bright blue raft made from strapped-together recycling drums with a wooden oar',
        'env': 'flooded Venice-like avenue where street signs stick out of four-foot-deep turquoise-tinted water',
        'emotion': 'resourceful and energetic'
    },
    {
        'act': 'Act 3: Ecological Shifts & The Floating World (Day 8 - 15)',
        'km': 'បណ្តាញទំនាក់ទំនងទូរស័ព្ទ និងអ៊ីនធឺណិតរអាក់រអួល ដោយសារខ្សែក្រោមដីត្រូវទឹកជន់លិច។',
        'en': 'Telecommunications wobble as flooded cables cause digital blackouts, sending people to search for signals on roofs.',
        'action': 'holding smartphone up high searching for elusive signal bar against rainy sky',
        'env': 'makeshift rooftop communication post with ham radio antenna and wire coils',
        'emotion': 'frustrated yet determined'
    },
    {
        'act': 'Act 3: Ecological Shifts & The Floating World (Day 8 - 15)',
        'km': 'ទោះជាយ៉ាងណា សហគមន៍បានរួបរួមគ្នា បើកផ្ទះបាយសាធារណៈចែករំលែកស៊ុបក្តៅៗដល់អ្នកជិតខាង។',
        'en': 'Yet human warmth shines brightly as neighbors open communal kitchens, serving bowls of steaming soup to everyone.',
        'action': 'ladling steaming delicious soup from a giant cartoon cauldron into bowls for smiling neighbors',
        'env': 'school gymnasium community kitchen lit with cozy lanterns, joyful aroma and steam rising',
        'emotion': 'warm and generous'
    },
    {
        'act': 'Act 3: Ecological Shifts & The Floating World (Day 8 - 15)',
        'km': 'គ្រូពេទ្យ និងក្រុមសង្គ្រោះធ្វើការទាំងយប់ទាំងថ្ងៃ ចែករំលែកថ្នាំចម្រោះទឹកស្អាតដល់ប្រជាជន។',
        'en': 'Medical professionals work around the clock distributing water purification tablets to ensure safe, drinkable water.',
        'action': 'wearing clean white lab coat, dropping fizzy effervescent chlorine tablets into clear water carboy',
        'env': 'clean white medical relief tent with medical crates, microscopic slides, and sterilizers',
        'emotion': 'focused and caring'
    },
    {
        'act': 'Act 3: Ecological Shifts & The Floating World (Day 8 - 15)',
        'km': 'កុមារតូចៗនៅលើដំបូលផ្ទះ រៀនបត់ទូកក្រដាសពណ៌ក្រហម ប្រណាំងគ្នាតាមខ្សែទឹកភ្លៀងយ៉ាងសប្បាយ។',
        'en': 'Children on dry terraces find creative joy, folding bright origami paper boats and racing them down rainwater channels.',
        'action': 'gently placing a bright red origami paper boat into clear rainwater streaming down roof tile channel',
        'env': 'cozy covered porch with colorful folded origami boats floating gently in clean collected rainwater',
        'emotion': 'playful and cheerful'
    },
    {
        'act': 'Act 3: Ecological Shifts & The Floating World (Day 8 - 15)',
        'km': 'រុក្ខជាតិទឹក និងផ្កាឈូកទឹកបែរជារីកដុះដាលយ៉ាងស្រស់ស្អាត ដោយសារទទួលបានទឹកច្រើនលើសលុប។',
        'en': 'Floating water lilies and aquatic plants actually thrive wildly, expanding into enormous blooming pink blossoms.',
        'action': 'admiring an enormous cartoon water lily pad that has bloomed into a radiant pink flower',
        'env': 'submerged botanical garden where giant lily pads float among drowned street lamps',
        'emotion': 'fascinated by nature'
    },
    {
        'act': 'Act 3: Ecological Shifts & The Floating World (Day 8 - 15)',
        'km': 'នៅថ្ងៃទី ១៥ ពាក់កណ្តាលផ្លូវនៃដំណើរផ្សងព្រេង ផែនដីបានក្លាយជាពិភពទឹកដ៏អស្ចារ្យដែលមិនធ្លាប់មានពីមុនមក!',
        'en': 'By Day 15, the halfway milestone, Earth has transformed into a wondrous, mirror-like water world!',
        'action': 'standing atop city hall clock tower with waterproof binoculars, scanning the boundless water horizon',
        'env': 'grand clock tower viewpoint over boundless water mirror reflecting dramatic storm clouds',
        'emotion': 'epic awe and reverence'
    },

    # Act 4: Human Resilience & Nature's Miracles (Day 16 - 25)
    {
        'act': 'Act 4: Human Resilience & Nature\'s Miracles (Day 16 - 25)',
        'km': 'ចូលដល់សប្តាហ៍ទី ៣ វិស្វករបានរួមសហការគ្នាបង្កើតប្រព័ន្ធបូមទឹកយក្ស ដើម្បីរំដោះទឹកទៅកាន់អាងស្តុក។',
        'en': 'By week three, international engineers deploy massive floating pump systems to divert water into safety basins.',
        'action': 'reviewing holographic digital blueprinted pipelines alongside friendly robot assistant',
        'env': 'floating engineering barge with humming mega-pumps discharging water into retention basins',
        'emotion': 'visionary problem solver'
    },
    {
        'act': 'Act 4: Human Resilience & Nature\'s Miracles (Day 16 - 25)',
        'km': 'កសិដ្ឋានបន្លែអណ្តែតទឹកត្រូវបានបង្កើតឡើង ដើម្បីផ្គត់ផ្គង់សាឡាត់ និងបន្លែស្រស់ៗដល់មនុស្សរាប់លាននាក់។',
        'en': 'Floating hydroponic gardens bloom atop barges, yielding crisp lettuce and herbs for urban communities.',
        'action': 'harvesting fresh bright green cartoon lettuce leaves from a floating modular raft system',
        'env': 'lush green floating greenhouse dome glowing with warm pink LED grow lights over water',
        'emotion': 'triumphant gardener'
    },
    {
        'act': 'Act 4: Human Resilience & Nature\'s Miracles (Day 16 - 25)',
        'km': 'កង្ហារទឹកតូចៗត្រូវបានដំឡើងតាមចរន្តទឹកហូរ ដើម្បីទាញយកអគ្គិសនីស្អាតមកបំភ្លឺអំពូលភ្លើង។',
        'en': 'Mini hydro turbines deployed in rushing current channels capture clean renewable electricity to power homes.',
        'action': 'connecting a glowing yellow electrical cable to a spinning waterwheel generator submerged in torrent',
        'env': 'wooden pier with spinning hydro turbine illuminating string fairy lights with clean energy',
        'emotion': 'proud innovator'
    },
    {
        'act': 'Act 4: Human Resilience & Nature\'s Miracles (Day 16 - 25)',
        'km': 'មនុស្សជាតិមិនចុះចាញ់ទេ! យើងបានសម្របខ្លួនទៅនឹងពិភពទឹក ដោយជិះទូកដោះដូរផ្លែឈើ និងជួយគ្នាដោយស្នាមញញឹម។',
        'en': 'Humanity does not give up! Instead, communities adapt, turning canals into cheerful avenues of trade and connection.',
        'action': 'steering a solar-powered catamaran boat smiling warmly and waving to neighboring raft pilots',
        'env': 'bustling aquatic street where families on canoes and small boats trade fruits and supplies cheerily',
        'emotion': 'confident and joyful'
    },
    {
        'act': 'Act 4: Human Resilience & Nature\'s Miracles (Day 16 - 25)',
        'km': 'សត្វព្រៃក៏ចេះសម្របខ្លួនយ៉ាងឆ្លាត សត្វទុងឈរលើស្លាកសញ្ញាផ្លូវ ចាប់ត្រីដែលហែលកាត់ផ្លូវថ្មើរជើងយ៉ាងសប្បាយ។',
        'en': 'Wildlife adapts in surprising ways: clever seabirds perch on road signs to scoop up fish swimming down flooded crosswalks.',
        'action': 'giggling quietly as a friendly cartoon pelican scoops a silver fish right off a submerged zebra crossing',
        'env': 'submerged city crosswalk where clear rainwater hosts colorful darting fish and resting pelicans',
        'emotion': 'delighted and amused'
    },
    {
        'act': 'Act 4: Human Resilience & Nature\'s Miracles (Day 16 - 25)',
        'km': 'នៅឯវាលខ្សាច់ដែលធ្លាប់តែស្ងួត ភ្លៀងមួយខែនេះបានដាស់គ្រាប់ពូជបុរាណ ប្រែក្លាយវាលខ្សាច់ទៅជាវាលស្មៅ និងផ្ការីកស្គុះស្គាយ!',
        'en': 'Across historically dry deserts, this historic rain awakens dormant seeds, turning sand dunes into lush blooming meadows!',
        'action': 'kneeling in awe touching soft green clover and vibrant yellow wildflowers blanketing red desert dunes',
        'env': 'breathtaking Sahara-like desert transformed into blooming green meadow with sparkling freshwater lakes',
        'emotion': 'wonderstruck and joyful'
    },
    {
        'act': 'Act 4: Human Resilience & Nature\'s Miracles (Day 16 - 25)',
        'km': 'បឹងបុរាណដែលធ្លាប់រីងស្ងួតរាប់ពាន់ឆ្នាំ បានពេញដោយទឹកថ្លាឈ្វេងដូចកញ្ចក់ជាថ្មីម្តងទៀត។',
        'en': 'Ancient dry lake beds, desolate for thousands of years, fill with crystal turquoise waters, rekindling vanished ecosystems.',
        'action': 'skipping a smooth flat pebble across mirror-smooth surface of a newly reborn desert lake',
        'env': 'vast turquoise mirror lake framed by red sandstone canyons under misting gentle rain',
        'emotion': 'peaceful and serene'
    },
    {
        'act': 'Act 4: Human Resilience & Nature\'s Miracles (Day 16 - 25)',
        'km': 'នៅថ្ងៃទី ២៥ រ៉ាដាអាកាសធាតុបង្ហាញថា ពពកខ្មៅដ៏ធំមហិមា ចាប់ផ្តើមអស់ទឹកភ្លៀងជាបណ្តើរៗហើយ។',
        'en': 'By Day 25, atmospheric radars show the mammoth moisture ribbons finally beginning to thin and clear.',
        'action': 'pointing enthusiastically at a weather radar screen showing the dark purple rain band thinning to light blue',
        'env': 'weather command station with engineers celebrating as radar storm intensity dials drop',
        'emotion': 'hopeful and excited'
    },

    # Act 5: The Golden Dawn & Grand Outro (Day 26 - 30)
    {
        'act': 'Act 5: The Golden Dawn & Grand Outro (Day 26 - 30)',
        'km': 'ឈានចូលដល់ថ្ងៃទី ២៨ គ្រាប់ភ្លៀងធ្លាក់កាន់តែរង្វើលៗ ក្លាយជាដំណក់ទឹកតូចៗស្រទន់។',
        'en': 'By Day 28, the torrential downpour softens into a gentle, tranquil misting drizzle.',
        'action': 'stepping out without an umbrella, holding open palm outward to catch tiny soft raindrops',
        'env': 'quiet calm city rooftop where rain has slowed to gentle sparkling drizzle',
        'emotion': 'calm and expectant'
    },
    {
        'act': 'Act 5: The Golden Dawn & Grand Outro (Day 26 - 30)',
        'km': 'នៅព្រឹកព្រលឹមថ្ងៃទី ៣០ សំឡេងគ្រាប់ភ្លៀងបានស្ងាត់បាត់ទាំងស្រុងជាលើកដំបូងក្នុងរយៈពេលមួយខែ!',
        'en': 'On the morning of Day 30, the sound of falling rain vanishes completely for the very first time in a month.',
        'action': 'standing in absolute peaceful silence, listening with ear cupped towards the tranquil sky',
        'env': 'misty serene morning landscape, total quiet except for gentle dripping from eaves',
        'emotion': 'in breath-holding suspense'
    },
    {
        'act': 'Act 5: The Golden Dawn & Grand Outro (Day 26 - 30)',
        'km': 'ពពកខ្មៅក្រាស់បានចាប់ផ្តើមរសាត់បែកចេញពីគ្នា ហើយកាំរស្មីព្រះអាទិត្យពណ៌មាសដំបូងបានចាំងកាត់ផ្ទៃមេឃ!',
        'en': 'Then, like a theater curtain parting, the clouds break—and a brilliant beam of warm golden sunshine strikes through!',
        'action': 'looking up with joyful wide eyes, face bathed in warm radiant golden sunlight',
        'env': 'dramatic heavenly light beam breaking through stormy grey clouds, illuminating glistening landscape',
        'emotion': 'pure ecstatic happiness'
    },
    {
        'act': 'Act 5: The Golden Dawn & Grand Outro (Day 26 - 30)',
        'km': 'ឥន្ធនូដ៏ធំស្កឹមស្កៃ ៧ ពណ៌ បានលាតសន្ធឹងពាសពេញជើងមេឃ នាំមកនូវសេចក្តីសង្ឃឹម និងជីវិតថ្មីដល់ផែនដី!',
        'en': 'A colossal vibrant double rainbow arches across the entire horizon, symbolizing rebirth and triumph for life on Earth!',
        'action': 'jumping up into the air with outstretched arms against a giant spectacular cartoon double rainbow',
        'env': 'panoramic vista of glistening city and green hills under bright blue sky with vivid double rainbow',
        'emotion': 'triumphant and ecstatic'
    },
    {
        'act': 'Act 5: The Golden Dawn & Grand Outro (Day 26 - 30)',
        'km': 'កម្រិតទឹកចាប់ផ្តើមស្រកចុះយ៉ាងលឿន ហើយមនុស្សគ្រប់គ្នាកាន់អំបោសជួយបោសសម្អាតទីក្រុងឱ្យស្អាតដូចដើម។',
        'en': 'Floodwaters drain away rapidly, and communities cheerfully gather to clean up and restore sparkling sidewalks in the sun.',
        'action': 'holding a broom and smiling alongside friends hosing down clean city sidewalk in warm sunshine',
        'env': 'sunlit sparkling city street where citizens joyfully clean up, blooming flowers along sidewalk',
        'emotion': 'energetic and proud'
    },
    {
        'act': 'Act 5: The Golden Dawn & Grand Outro (Day 26 - 30)',
        'km': 'ព្រឹត្តិការណ៍នេះបានបង្រៀនយើងឱ្យឃើញពីអំណាចនៃធម្មជាតិ និងសារៈសំខាន់នៃតុល្យភាពអាកាសធាតុផែនដី។',
        'en': 'This thought experiment reminds us of the raw power of nature and the vital importance of Earth climate balance.',
        'action': 'sitting on grassy hilltop under shade of an apple tree, observing peaceful blue planet below',
        'env': 'lush rolling green meadow overlooking sparkling clean blue bay under radiant sunny sky',
        'emotion': 'wise and contemplative'
    },
    {
        'act': 'Act 5: The Golden Dawn & Grand Outro (Day 26 - 30)',
        'km': 'ហើយសំខាន់បំផុត វាបង្ហាញថា នៅពេលដែលមនុស្សជាតិរួបរួមគ្នា គ្មានព្យុះសង្ឃរាណាដែលអាចយកឈ្នះយើងបានឡើយ!',
        'en': 'Above all, it proved that when humanity stands together in courage and solidarity, no storm can ever break us!',
        'action': 'standing shoulder to shoulder with diverse cute cartoon pill friends smiling warmly at the camera',
        'env': 'vibrant sun-drenched town square full of smiles, blooming trees, and fluttering celebration banners',
        'emotion': 'deeply inspired and grateful'
    },
    {
        'act': 'Act 5: The Golden Dawn & Grand Outro (Day 26 - 30)',
        'km': 'តើអ្នកគិតយ៉ាងណាដែរ ប្រសិនបើអ្នកត្រូវជួបភ្លៀងធ្លាក់ ៣០ ថ្ងៃជាប់គ្នា? សូមបញ្ចេញមតិយោបល់នៅខាងក្រោម!',
        'en': 'How would you handle 30 continuous days of rain? Tell us your survival ideas in the comments below!',
        'action': 'waving enthusiastically with both hands, pointing down playfully at animated comment box bubble',
        'env': 'colorful Kurzgesagt style outro studio set with floating like, share, and notification bell icons',
        'emotion': 'friendly and engaging'
    },
    {
        'act': 'Act 5: The Golden Dawn & Grand Outro (Day 26 - 30)',
        'km': 'សូមកុំភ្លេចចុច Like និង Subscribe ដើម្បីបន្តរុករកអាថ៌កំបាំង What-If ដ៏អស្ចារ្យជាមួយពួកយើងនៅវីដេអូបន្ទាប់!',
        'en': 'Do not forget to like and subscribe to embark on more mind-bending scientific adventures with us in the next episode!',
        'action': 'giving enthusiastic thumbs up as giant animated red Subscribe button clicks with sparkling golden stars',
        'env': 'celebratory colorful animated channel outro card with exploding confetti and bright fireworks',
        'emotion': 'triumphant and smiling'
    }
]

def main():
    os.makedirs('custom_scripts', exist_ok=True)
    scenes = []
    for idx, s in enumerate(scenes_data, start=1):
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
        'title_en': 'What If It Rained Non-Stop for 30 Days?',
        'title_km': 'ចុះបើភ្លៀងធ្លាក់ជាប់គ្នាពេញមួយខែ?',
        'total_scenes': len(scenes),
        'estimated_duration_minutes': 8,
        'scenes': scenes
    }

    out_path = os.path.join('custom_scripts', 'rain_for_month.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(script_obj, f, ensure_ascii=False, indent=2)

    print(f"Created {out_path} with {len(scenes)} unique scenes successfully.")

if __name__ == '__main__':
    main()
