import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.prompt_generator import CHARACTER_BASE_PROMPT

scenes_data = [
    # Act 1: The Inciting Hook & First 48 Hours (Scenes 1-10)
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'តើអ្នកធ្លាប់ឆ្ងល់ទេថា នឹងមានអ្វីកើតឡើង ប្រសិនបើភ្លៀងធ្លាក់មិនឈប់ទាល់តែសោះ រយៈពេល ៣០ ថ្ងៃជាប់ៗគ្នា?',
        'en': 'Have you ever wondered what would happen if torrential rain fell continuously without stopping for thirty whole days?',
        'action': 'holding a tiny yellow umbrella, staring up at dark grey stormy clouds with curious round eyes',
        'env': 'cozy cartoon street as first heavy raindrops begin to splash into glowing puddles',
        'emotion': 'deeply curious'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'នៅថ្ងៃដំបូង មនុស្សភាគច្រើនប្រហែលជាគិតថាវាគ្រាន់តែជាអាកាសធាតុត្រជាក់ស្រួល និងរ៉ូមែនទិកធម្មតាប៉ុណ្ណោះ។',
        'en': 'On Day 1, most people would simply enjoy the cozy weather, sipping coffee and listening to the soothing rhythm of raindrops.',
        'action': 'sitting inside a warm coffee shop window holding a steaming mug, watching cartoon rain droplets glide down glass',
        'env': 'warm pastel cafe interior with soft golden lights contrasting with rainy blue window',
        'emotion': 'relaxed and peaceful'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'ប៉ុន្តែនៅពេលដែលថ្ងៃទី ២ ចូលមកដល់ ភ្លៀងនៅតែធ្លាក់យ៉ាងគំហុកដោយគ្មានសញ្ញានៃការថមថយសូម្បីតែមួយវិនាទី។',
        'en': 'But as Day 2 rolls in, the rain continues to pour violently without a single second of pause.',
        'action': 'peering through blinds with growing suspicion, checking digital weather forecast on tablet showing 100% rain icon',
        'env': 'living room with rain hammering loudly against windowpanes, gloomy grey sky',
        'emotion': 'slightly concerned and puzzled'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'ប្រព័ន្ធលូក្នុងទីក្រុងចាប់ផ្តើមរងសម្ពាធទឹកលើសចំណុះ ហើយផ្លូវថ្នល់មួយចំនួនចាប់ផ្តើមក្លាយជាស្ទឹងតូចៗ។',
        'en': 'City storm drains quickly reach maximum capacity, and suburban streets begin transforming into shallow flowing rivers.',
        'action': 'wearing bright red rubber rain boots, stepping cautiously into water rising over sidewalk curb',
        'env': 'city intersection where water gushes up out of storm grates like bubbling fountains',
        'emotion': 'cautious and observant'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'ដីធម្មជាតិស្រូបយកទឹកដល់កម្រិតឆ្អែត ធ្វើឱ្យសួនច្បារ និងវាលស្មៅប្រែទៅជាភក់ជ្រាំដ៏រអិល។',
        'en': 'Topsoil across parks and farmland reaches total saturation point, incapable of absorbing even one more drop of water.',
        'action': 'standing in a suburban park where cartoon earth squelches muddy bubbles beneath feet',
        'env': 'city park with saturated marshy grass, puddles merging into a vast shallow pond',
        'emotion': 'surprised and uneasy'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'ពពកខ្មៅក្រាស់ឃ្មឹកបានបាំងពន្លឺព្រះអាទិត្យទាំងស្រុង ធ្វើឱ្យទីក្រុងទាំងមូលស្ថិតក្នុងភាពងងឹតស្លัวពេញមួយថ្ងៃ។',
        'en': 'Colossal nimbostratus clouds blot out sunlight entirely, plunging cities into an eerie, perpetual twilight.',
        'action': 'holding a glowing flashlight upwards toward ominous purple-grey ceiling of endless clouds',
        'env': 'dim city square at midday, streetlamps flickering on automatically beneath dark cloud canopy',
        'emotion': 'intimidated and solemn'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'តើទឹកភ្លៀងរាប់ពាន់លានតោននេះមកពីណា? វាគឺជាវដ្តទឹកបរិយាកាសដែលកំពុងដំណើរការក្នុងល្បឿនមិនធ្លាប់មានពីមុនមក។',
        'en': 'Where does all this water come from? An unprecedented atmospheric river is dumping billions of tons of moisture.',
        'action': 'pointing at a holographic 3D Earth showing swirling white atmospheric moisture ribbons across oceans',
        'env': 'high-tech meteorological observatory with weather radars glowing cyan and green',
        'emotion': 'analytical and fascinated'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'សីតុណ្ហភាពចាប់ផ្តើមធ្លាក់ចុះជាលំដាប់ ហើយសំណើមក្នុងខ្យល់ឡើងដល់ ១០០ ភាគរយឥតឈប់ឈរ។',
        'en': 'Ambient temperatures plunge as relative humidity locks at a suffocating one hundred percent.',
        'action': 'checking an analog wall barometer and thermometer with needle pinned at maximum humidity',
        'env': 'foggy interior hallway where moisture condenses on metal door handles and cool mirrors',
        'emotion': 'shivering slightly'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'សត្វស្លាប និងសត្វល្អិតត្រូវស្វែងរកជម្រកជាបន្ទាន់ ព្រោះគ្រាប់ភ្លៀងធ្លាក់ខ្លាំងដូចជាគ្រាប់កាំភ្លើងតូចៗ។',
        'en': 'Birds and insects desperately seek shelter, unable to fly as heavy raindrops hit their fragile bodies like bullets.',
        'action': 'gently guiding tiny soaked cartoon sparrows into a dry hollow wooden tree shelter',
        'env': 'leafy forest branch trembling under torrential bombardment of fat raindrops',
        'emotion': 'protective and compassionate'
    },
    {
        'act': 'Act 1: The Unbroken Downpour (Day 1 - 2)',
        'km': 'ចរាចរណ៍តាមដងផ្លូវធំៗចាប់ផ្តើមជាប់គាំង ដោយសាររថយន្តតូចៗមិនអាចបើកបរឆ្លងកាត់ទឹកជ្រៅបាន។',
        'en': 'Major highways and ring roads grind to a dead halt as cars stall in deep rising floodwaters.',
        'action': 'standing on a highway pedestrian bridge, looking down at rows of headlights reflected in water',
        'env': 'rain-slicked expressway submerged under three feet of water, emergency hazard lights blinking',
        'emotion': 'worried and watchful'
    },

    # Act 2: Days 3 to 7 - Urban Breakdown & Saturated Soil (Scenes 11-22)
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'ឈានចូលដល់ថ្ងៃទី ៤ កម្រិតទឹកនៅក្នុងទន្លេធំៗបានហក់ឡើងជិតដល់មាត់ទំនប់ការពារទឹកជំនន់។',
        'en': 'By Day 4, river levels worldwide surge dangerously close to the crest of protective floodwalls.',
        'action': 'standing on a concrete flood levee with measuring stick showing water rising past yellow safety line',
        'env': 'turbulent muddy river foaming against massive concrete floodwalls under pounding rain',
        'emotion': 'tense and anxious'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'ដីក្រោមគ្រឹះអគារ និងផ្លូវដែកចាប់ផ្តើមជ្រាយ បង្កឱ្យមានការស្រុតដីនៅតាមតំបន់ទំនាប។',
        'en': 'Waterlogged subsoil beneath roads and foundations softens, triggering localized ground subsidence.',
        'action': 'kneeling down examining cracked asphalt where water bubbles up from underground soil',
        'env': 'suburban street with curved cracks appearing in pavement as road foundation sags',
        'emotion': 'investigative and alarmed'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'រថភ្លើងក្រោមដី និងផ្លូវរូងក្រោមដីទាំងអស់ត្រូវផ្អាកដំណើរការទាំងស្រុង ដោយសារទឹកជ្រាបចូលដូចទឹកជ្រោះ។',
        'en': 'Underground subways and tunnels are completely shut down as floodwaters cascade down subway stairs like waterfalls.',
        'action': 'standing behind safety barricade looking down subway entrance overflowing with gushing water',
        'env': 'metro station entrance with emergency yellow tape, water roaring down tiled escalators',
        'emotion': 'shocked'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'ផ្ទះរាប់ពាន់ខ្នងនៅតំបន់ទំនាបត្រូវទឹកជន់លិចដល់ជាន់ទីមួយ ហើយប្រជាជនត្រូវរើអីវ៉ាន់ឡើងទៅជាន់លើ។',
        'en': 'Thousands of suburban ground floors are submerged, forcing families to evacuate belongings to rooftops.',
        'action': 'carrying boxes of dry supplies and cute pillows up a spiral staircase inside home',
        'env': 'living room with floating furniture and water halfway up sofa cushions',
        'emotion': 'frantic but resilient'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'ការដាច់ចរន្តអគ្គិសនីចាប់ផ្តើមរាលដាល ពីព្រោះស្ថានីយបំប្លែងភ្លើងក្រោមដីត្រូវបានទឹកជន់លិច។',
        'en': 'Rolling power outages strike as electrical substations short-circuit beneath standing water.',
        'action': 'holding a warm glowing lantern as room lights suddenly pop and flicker out completely',
        'env': 'dark apartment illuminated only by handheld lantern and flashes of outdoor lightning',
        'emotion': 'startled'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'កង្វះពន្លឺព្រះអាទិត្យចាប់ផ្តើមជះឥទ្ធិពលលើរុក្ខជាតិ រស្មីសំយោគត្រូវថមថយ ហើយស្លឹកឈើចាប់ផ្តើមលឿង។',
        'en': 'The complete absence of direct sunlight suppresses photosynthesis, turning leaves pale and sickly yellow.',
        'action': 'inspecting a droopy cartoon potted plant whose leaves are losing green pigmentation',
        'env': 'indoor windowsill garden drenched in gloomy dim mist, pale yellowing leaves',
        'emotion': 'worried botanist'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'ផ្សិត និងពពួកបាក់តេរីសំណើមចាប់ផ្តើមដុះលូតលាស់យ៉ាងលឿនតាមជញ្ជាំង និងជ្រុងផ្ទះនីមួយៗ។',
        'en': 'Mold spores and damp-loving fungi flourish exponentially across damp wallpaper and corners.',
        'action': 'shining UV magnifying glass at cartoon green spores sprouting along wall baseboard',
        'env': 'damp room corner with velvety green moss and tiny cartoon mushrooms sprouting',
        'emotion': 'disgusted and cautious'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'នៅតាមជនបទ ស្រែចម្ការ និងដំណាំកសិកម្មរាប់សែនហិកតាត្រូវលិចលង់ក្រោមផ្ទៃទឹកពណ៌ក្រហមច្រាល។',
        'en': 'In rural countrysides, endless wheat and rice fields vanish beneath a sea of muddy brown water.',
        'action': 'riding a rescue dinghy through flooded farm fields, looking at submerged tractor roofs',
        'env': 'vast submerged agricultural valley where only treetops and telephone poles emerge from water',
        'emotion': 'heartbroken observer'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'សត្វព្រៃជាច្រើនត្រូវបង្ខំចិត្តរត់គេចឡើងទៅលើដើមឈើធំៗ និងកំពូលភ្នំដើម្បីរកទីទួលសុវត្ថិភាព។',
        'en': 'Forest wildlife—deer, foxes, and hedgehogs—cluster together on shrinking hilltop knolls and branches.',
        'action': 'looking through binoculars at a group of cartoon forest critters huddled safely on a high rock knoll',
        'env': 'flooded forest canopy with animals sharing dry branches peacefully',
        'emotion': 'deeply moved and observant'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'ទឹកស្អាតសម្រាប់បរិភោគចាប់ផ្តើមក្លាយជាបញ្ហាចម្បង ព្រោះរោងចក្រចម្រោះទឹកស្អាតត្រូវរងការបំពុលដោយទឹកកខ្វក់។',
        'en': 'Potable drinking water becomes severely scarce as municipal treatment plants are overwhelmed by contaminated runoff.',
        'action': 'holding a glass water bottle under a dripping faucet that coughs out brown murky water',
        'env': 'kitchen with stockpiled water jugs and boiling pots on emergency camping stove',
        'emotion': 'troubled'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'ក្រុមជួយសង្គ្រោះត្រូវប្រើប្រាស់ទូកកៅស៊ូ និងឧទ្ធម្ភាគចក្រដើម្បីចែកស្បៀងអាហារដល់អ្នកជាប់គាំង។',
        'en': 'First responders deploy rubber rafts and rescue choppers to deliver vital rations to stranded residents.',
        'action': 'waving from a rooftop with bright orange signal flag towards a friendly cartoon rescue helicopter',
        'env': 'rainy rooftop island surrounded by miles of floodwaters, helicopter lowering cargo sling',
        'emotion': 'relieved and grateful'
    },
    {
        'act': 'Act 2: The Sinking World (Day 3 - 7)',
        'km': 'ហើយនៅចុងសប្តាហ៍ទីមួយ មនុស្សគ្រប់រូបចាប់ផ្តើមភ័យខ្លាចថា ពិភពលោកប្រហែលជាលែងស្គាល់ពាក្យថាថ្ងៃរះទៀតហើយ!',
        'en': 'By the close of week one, the unsettling fear sinks in: will the sun ever shine again?',
        'action': 'sitting on rooftop ledge wearing yellow raincoat, gazing out into the relentless curtain of grey rain',
        'env': 'sweeping panoramic view of flooded metropolis shimmering with ripples in stormy twilight',
        'emotion': 'deeply contemplative'
    },

    # Act 3: Days 8 to 15 - Deep Ecological & Geological Crisis (Scenes 23-35)
    {
        'act': 'Act 3: The Earth Under Siege (Day 8 - 15)',
        'km': 'ឈានចូលដល់សប្តាហ៍ទី ២ សម្ពាធទឹកដ៏មហិមាបានធ្វើឱ្យទំនប់វារីអគ្គិសនីមួយចំនួនត្រូវបើកទ្វារទឹកទាំងអស់ជាបន្ទាន់។',
        'en': 'Entering week two, immense hydrostatic pressure forces hydroelectric dams to unleash emergency spillways.',
        'action': 'standing on a dam observation tower watching colossal roaring white foam geysers exploding from sluice gates',
        'env': 'gigantic concrete hydroelectric dam with roaring discharge gates blasting into downstream canyon',
        'emotion': 'awe-struck and frightened'
    },
    {
        'act': 'Act 3: The Earth Under Siege (Day 8 - 15)',
        'km': 'នៅតាមតំបន់ភ្នំ ដីភ្នំទាំងមូលដែលជ្រាបទឹកខ្លាំងចាប់ផ្តើមបាក់ស្រុត បង្កជាគ្រោះបាក់ដីយ៉ាងសាហាវ។',
        'en': 'In mountainous regions, saturated soil liquefies, unleashing devastating mudslides down mountain valleys.',
        'action': 'pointing safety whistle to guide cartoon vehicles away from crumbling hillside road',
        'env': 'steep mountain road where muddy torrents and dislodged boulders crash into safety barriers',
        'emotion': 'urgent and brave'
    },
    {
        'act': 'Act 3: The Earth Under Siege (Day 8 - 15)',
        'km': 'ទម្ងន់ទឹកភ្លៀងរាប់ពាន់លានតោនដែលធ្លាក់លើទ្វីប បានធ្វើឱ្យសំបកផែនដីរងសម្ពាធទម្ងន់បន្ថែមយ៉ាងខ្លាំង។',
        'en': 'Trillions of tons of newly added surface water exert tangible gravitational and tectonic weight on continental plates.',
        'action': 'studying seismograph machine with needle tracing delicate vibration ripples across paper drum',
        'env': 'geophysical underground vault with digital Earth crust stress maps glowing crimson',
        'emotion': 'scientific precision'
    },
    {
        'act': 'Act 3: The Earth Under Siege (Day 8 - 15)',
        'km': 'ជាតិអំបិលនៅក្នុងទឹកសមុទ្រនៅតាមមាត់ឆ្នេរចាប់ផ្តើមធ្លាក់ចុះ ដោយសារបរិមាណទឹកសាបដ៏ច្រើនលើសលុបហូរចូល។',
        'en': 'Ocean salinity around coastal estuaries plummets as monstrous volumes of freshwater dilute the shoreline.',
        'action': 'dipping a hydrometer testing tube into coastal water to measure salt salinity levels',
        'env': 'coastal bay where brown freshwater plume collides with emerald ocean tide',
        'emotion': 'curious researcher'
    },
    {
        'act': 'Act 3: The Earth Under Siege (Day 8 - 15)',
        'km': 'ការប្រែប្រួលជាតិប្រៃនេះ ធ្វើឱ្យផ្កាថ្ម និងពពួកមច្ឆាតាមឆ្នេរសមុទ្ររងការប៉ះពាល់យ៉ាងធ្ងន់ធ្ងរ។',
        'en': 'This sudden salinity shock causes severe osmotic stress to delicate coral reefs and coastal fish species.',
        'action': 'peering through underwater observation window at bewildered cartoon clownfish hovering near pale corals',
        'env': 'underwater reef station where freshwater turbidity clouds the vibrant reef ecosystem',
        'emotion': 'empathetic and concerned'
    },
    {
        'act': 'Act 3: The Earth Under Siege (Day 8 - 15)',
        'km': 'នៅក្នុងទីក្រុង មនុស្សចាប់ផ្តើមច្នៃប្រឌិតទូកក្បូនពីធុងជ័រ និងកង់ឡាន ដើម្បីធ្វើដំណើរទៅរកម្ហូបអាហារ។',
        'en': 'In submerged city alleys, citizens construct inventive makeshift rafts out of plastic drums and inner tubes.',
        'action': 'cheerfully paddling a bright blue raft made from strapped-together recycling drums with a wooden oar',
        'env': 'flooded Venice-like avenue where street signs stick out of four-foot-deep turquoise-tinted water',
        'emotion': 'resourceful and energetic'
    },
    {
        'act': 'Act 3: The Earth Under Siege (Day 8 - 15)',
        'km': 'បណ្តាញទំនាក់ទំនងទូរស័ព្ទ និងអ៊ីនធឺណិតចាប់ផ្តើមរអាក់រអួល ដោយសារខ្សែអុបទិកក្រោមដីរងការខូចខាត។',
        'en': 'Telecommunications wobble as flooded junction boxes and severed subterranean cables trigger digital blackouts.',
        'action': 'holding smartphone up high searching for elusive signal bar against rainy sky',
        'env': 'makeshift rooftop communication post with ham radio antenna and wire coils',
        'emotion': 'frustrated yet determined'
    },
    {
        'act': 'Act 3: The Earth Under Siege (Day 8 - 15)',
        'km': 'ទោះជាយ៉ាងណា សហគមន៍មនុស្សជាតិបានបង្ហាញពីសាមគ្គីភាព ដោយបើកផ្ទះបាយសាធារណៈចែករំលែកបាយក្តៅៗ។',
        'en': 'Yet human warmth shines through as neighbors establish communal kitchens on high ground, serving steaming soup.',
        'action': 'ladling steaming delicious soup from a giant cartoon cauldron into bowls for smiling neighbors',
        'env': 'school gymnasium community kitchen lit with cozy lanterns, joyful aroma and steam rising',
        'emotion': 'warm and generous'
    },
    {
        'act': 'Act 3: The Earth Under Siege (Day 8 - 15)',
        'km': 'វេជ្ជបណ្ឌិត និងក្រុមពេទ្យត្រូវធ្វើការទាំងយប់ទាំងថ្ងៃ ដើម្បីទប់ស្កាត់ជំងឺឆ្លងតាមទឹកកខ្វក់។',
        'en': 'Medical professionals work around the clock distributing water purification tablets to halt waterborne illness.',
        'action': 'wearing clean white lab coat, dropping fizzy effervescent chlorine tablets into clear water carboy',
        'env': 'clean white medical relief tent with medical crates, microscopic slides, and sterilizers',
        'emotion': 'focused and caring'
    },
    {
        'act': 'Act 3: The Earth Under Siege (Day 8 - 15)',
        'km': 'កុមារតូចៗនៅលើដំបូលផ្ទះ រៀនលេងល្បែងប្រជាប្រិយ និងបត់ទូកក្រដាសបណ្តែតលើទឹកភ្លៀង។',
        'en': 'Children on dry upper terraces find creative joy, folding colorful paper boats and racing them down roof gutters.',
        'action': 'gently placing a bright red origami paper boat into clear rainwater streaming down roof tile channel',
        'env': 'cozy covered porch with colorful folded origami boats floating gently in clean collected rainwater',
        'emotion': 'playful and cheerful'
    },
    {
        'act': 'Act 3: The Earth Under Siege (Day 8 - 15)',
        'km': 'រុក្ខជាតិទឹក និងសារាយសមុទ្រមួយចំនួនបែរជាទទួលបានផលប្រយោជន៍ និងលូតលាស់យ៉ាងលឿនអស្ចារ្យ។',
        'en': 'Surpassingly, aquatic weeds and floating lotus lilies thrive wildly, soaking in endless freshwater nutrients.',
        'action': 'admiring an enormous cartoon water lily pad that has bloomed into a radiant pink flower',
        'env': 'submerged botanical garden where giant lily pads float among drowned street lamps',
        'emotion': 'fascinated by nature'
    },
    {
        'act': 'Act 3: The Earth Under Siege (Day 8 - 15)',
        'km': 'នៅថ្ងៃទី ១៥ ពាក់កណ្តាលផ្លូវនៃដំណើរផ្សងព្រេង ផែនដីបានក្លាយជាពិភពទឹកដ៏អាថ៌កំបាំងមួយដែលគ្មាននរណាស្មានដល់!',
        'en': 'By Day 15, the halfway milestone, Earth has transformed into a wondrous, alien waterworld unlike anything in human history!',
        'action': 'standing atop city hall clock tower with waterproof binoculars, scanning the boundless water horizon',
        'env': 'grand clock tower viewpoint over boundless water mirror reflecting dramatic storm clouds',
        'emotion': 'epic awe and reverence'
    },

    # Act 4: Days 16 to 25 - The Peak Deluge & Human Resilience (Scenes 36-47)
    {
        'act': 'Act 4: High Water Resilience (Day 16 - 25)',
        'km': 'ចូលដល់សប្តាហ៍ទី ៣ វិស្វករទូទាំងពិភពលោកបានរួមសហការគ្នាបង្កើតប្រព័ន្ធរំដោះទឹកទំនើបឆ្លាតវៃ។',
        'en': 'By week three, international engineers unite to deploy massive floating siphon systems and industrial pumps.',
        'action': 'reviewing holographic digital blueprinted pipelines alongside friendly robot assistant',
        'env': 'floating engineering barge with humming mega-pumps discharging water into retention basins',
        'emotion': 'visionary problem solver'
    },
    {
        'act': 'Act 4: High Water Resilience (Day 16 - 25)',
        'km': 'រោងចក្រអណ្តែតទឹក និងកសិដ្ឋានបន្លែអណ្តែតទឹកត្រូវបានបង្កើតឡើង ដើម្បីផ្គត់ផ្គង់បន្លែស្រស់ៗដល់មនុស្សរាប់លាននាក់។',
        'en': 'Floating hydroponic gardens bloom atop barges, yielding crisp lettuce and herbs for urban communities.',
        'action': 'harvesting fresh bright green cartoon lettuce leaves from a floating modular raft system',
        'env': 'lush green floating greenhouse dome glowing with warm pink LED grow lights over water',
        'emotion': 'triumphant gardener'
    },
    {
        'act': 'Act 4: High Water Resilience (Day 16 - 25)',
        'km': 'ប្រព័ន្ធថាមពលវារីអគ្គិសនីខ្នាតតូចត្រូវបានដំឡើងតាមចរន្តទឹកហូរខ្លាំង ដើម្បីទាញយកអគ្គិសនីស្អាតមកប្រើប្រាស់វិញ។',
        'en': 'Mini hydro turbines deployed in flowing current channels capture boundless renewable electricity.',
        'action': 'connecting a glowing yellow electrical cable to a spinning waterwheel generator submerged in torrent',
        'env': 'wooden pier with spinning hydro turbine illuminating string fairy lights with clean energy',
        'emotion': 'proud innovator'
    },
    {
        'act': 'Act 4: High Water Resilience (Day 16 - 25)',
        'km': 'មនុស្សជាតិមិនចុះចាញ់ទេ! យើងបានសម្របខ្លួនទៅនឹងពិភពទឹក ដោយប្រែក្លាយបញ្ហាប្រឈមទៅជាឱកាសច្នៃប្រឌិត។',
        'en': 'Humanity does not yield! Instead of despair, communities adapt and turn floodwaters into highways of cooperation.',
        'action': 'steering a solar-powered catamaran boat smiling warmly and waving to neighboring raft pilots',
        'env': 'bustling aquatic street where families on canoes and small boats trade fruits and supplies cheerily',
        'emotion': 'confident and joyful'
    },
    {
        'act': 'Act 4: High Water Resilience (Day 16 - 25)',
        'km': 'សត្វព្រៃក៏បានបង្កើតផ្លូវរស់រានផ្ទាល់ខ្លួន សត្វបក្សីចាប់ផ្តើមរៀនស្ទូចត្រីដែលហែលតាមផ្លូវថ្នល់ទីក្រុង។',
        'en': 'Wildlife adapts in surprising ways—clever seabirds perch on road signs to catch river fish swimming down streets.',
        'action': 'giggling quietly as a friendly cartoon pelican scoops a silver fish right off a submerged zebra crossing',
        'env': 'submerged city crosswalk where clear rainwater hosts colorful darting fish and resting pelicans',
        'emotion': 'delighted and amused'
    },
    {
        'act': 'Act 4: High Water Resilience (Day 16 - 25)',
        'km': 'នៅតាមតំបន់វាលខ្សាច់ដែលធ្លាប់តែស្ងួតហួតហែង ភ្លៀងមួយខែនេះបានប្រែក្លាយវាលខ្សាច់ទៅជាវាលស្មៅបៃតងខ្ចីដ៏ស្រស់ស្អាត!',
        'en': 'Across historically arid deserts, this historic downpour awakens ancient dormant seeds, turning sand into blooming oases!',
        'action': 'kneeling in awe touching soft green clover and vibrant yellow wildflowers blanketing red desert dunes',
        'env': 'breathtaking Sahara-like desert transformed into blooming green meadow with sparkling freshwater lakes',
        'emotion': 'wonderstruck and joyful'
    },
    {
        'act': 'Act 4: High Water Resilience (Day 16 - 25)',
        'km': 'បឹងបុរាណដែលធ្លាប់រីងស្ងួតរាប់ពាន់ឆ្នាំមុន ត្រូវបានបំពេញដោយទឹកថ្លាឈ្វេងជាថ្មីម្តងទៀត។',
        'en': 'Ancient dry lake beds, desolate for thousands of years, fill with crystal turquoise waters, rekindling vanished ecosystems.',
        'action': 'skipping a smooth flat pebble across mirror-smooth surface of a newly reborn desert lake',
        'env': 'vast turquoise mirror lake framed by red sandstone canyons under misting gentle rain',
        'emotion': 'peaceful and serene'
    },
    {
        'act': 'Act 4: High Water Resilience (Day 16 - 25)',
        'km': 'នៅថ្ងៃទី ២៥ សម្ពាធបរិយាកាសចាប់ផ្តើមបង្ហាញសញ្ញានៃការប្រែប្រួល ខ្យល់ព្យុះចាប់ផ្តើមថយចុះកម្លាំងជាបណ្តើរៗ។',
        'en': 'By Day 25, barometric pressures begin stabilizing as the mammoth atmospheric river finally starts exhausting its moisture.',
        'action': 'pointing enthusiastically at a weather radar screen showing the dark purple rain band thinning to light blue',
        'env': 'weather command station with engineers celebrating as radar storm intensity dials drop',
        'emotion': 'hopeful and excited'
    },

    # Act 5: Days 26 to 30 - The Sun Returns & Lessons for Humanity (Scenes 48-58)
    {
        'act': 'Act 5: The Golden Dawn & Grand Outro (Day 26 - 30)',
        'km': 'ឈានចូលដល់ថ្ងៃទី ២៨ គ្រាប់ភ្លៀងធ្លាក់កាន់តែរង្វើលៗ ពីទឹកភ្លៀងខ្លាំងក្លាយជាដំណក់ទឹកតូចៗស្រទន់។',
        'en': 'By Day 28, the relentless deluge softens into a gentle, tranquil misting drizzle.',
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
        'en': 'Then, like a theater curtain opening, the dark clouds part—and a brilliant beam of golden sunshine pierces through!',
        'action': 'looking up with joyful wide eyes, face bathed in warm radiant golden sunlight',
        'env': 'dramatic heavenly light beam breaking through stormy grey clouds, illuminating glistening landscape',
        'emotion': 'pure ecstatic happiness'
    },
    {
        'act': 'Act 5: The Golden Dawn & Grand Outro (Day 26 - 30)',
        'km': 'ឥន្ធនូដ៏ធំស្កឹមស្កៃ ៧ ពណ៌ បានលាតសន្ធឹងពាសពេញជើងមេឃ នាំមកនូវសេចក្តីសង្ឃឹម និងជីវិតថ្មីដល់ផែនដី!',
        'en': 'A colossal, vibrant double rainbow arches across the entire horizon, symbolizing rebirth and triumph for humanity!',
        'action': 'jumping up into the air with outstretched arms against a giant spectacular cartoon double rainbow',
        'env': 'panoramic vista of glistening city and green hills under bright blue sky with vivid double rainbow',
        'emotion': 'triumphant and ecstatic'
    },
    {
        'act': 'Act 5: The Golden Dawn & Grand Outro (Day 26 - 30)',
        'km': 'កម្រិតទឹកចាប់ផ្តើមស្រកចុះយ៉ាងលឿនតាមប្រព័ន្ធរំដោះទឹក ហើយទីក្រុងចាប់ផ្តើមសម្អាត និងស្តារឡើងវិញ។',
        'en': 'Floodwaters recede rapidly through newly engineered drainage canals, and communities begin cheerful cleanups.',
        'action': 'holding a broom and smiling alongside friends hosing down clean city sidewalk in warm sunshine',
        'env': 'sunlit sparkling city street where citizens joyfully clean up, blooming flowers along sidewalk',
        'emotion': 'energetic and proud'
    },
    {
        'act': 'Act 5: The Golden Dawn & Grand Outro (Day 26 - 30)',
        'km': 'ព្រឹត្តិការណ៍នេះបានបង្រៀនយើងឱ្យឃើញពីអំណាចនៃធម្មជាតិ និងសារៈសំខាន់នៃតុល្យភាពបរិយាកាសផែនដី។',
        'en': 'This extraordinary ordeal proved the raw power of nature and the vital importance of protecting Earth climate stability.',
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
        'km': 'តើអ្នកគិតយ៉ាងណាដែរ ប្រសិនបើអ្នកត្រូវរស់នៅក្រោមភ្លៀងធ្លាក់ ៣០ ថ្ងៃជាប់គ្នា? សូមបញ្ចេញមតិយោបល់នៅខាងក្រោម!',
        'en': 'How would you survive if it rained continuously for 30 days in your hometown? Tell us your survival strategy below!',
        'action': 'waving enthusiastically with both hands, pointing down playfully at animated comment box bubble',
        'env': 'colorful Kurzgesagt style outro studio set with floating like, share, and notification bell icons',
        'emotion': 'friendly and engaging'
    },
    {
        'act': 'Act 5: The Golden Dawn & Grand Outro (Day 26 - 30)',
        'km': 'សូមកុំភ្លេចចុច Like និង Subscribe ដើម្បីបន្តរុករកអាថ៌កំបាំងវិទ្យាសាស្ត្រដ៏អស្ចារ្យជាមួយពួកយើងនៅវីដេអូបន្ទាប់!',
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
