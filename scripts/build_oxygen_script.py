import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.prompt_generator import CHARACTER_BASE_PROMPT

scenes = [
    # Act 1: The Supercharged Morning (0 to 12 Hours)
    {
        "scene_num": 1,
        "act": "Act 1: The Supercharged Morning (0 to 12 Hours)",
        "duration_hint": 7.5,
        "khmer_speech": "ចុះបើកម្រិតអុកស៊ីសែននៅលើផែនដី ស្រាប់តែកើនឡើងទ្វេដងក្នុងមួយយប់? តើជីវិតយើងនឹងទៅជាយ៉ាងណា?",
        "english_speech": "What if the oxygen on Earth suddenly doubled overnight? Let's step into this ultimate thought experiment!",
        "action": "looking up with big round eyes holding a small telescope",
        "environment": "starry cosmic sky with glowing chemical symbols",
        "emotion": "deeply curious"
    },
    {
        "scene_num": 2,
        "act": "Act 1: The Supercharged Morning (0 to 12 Hours)",
        "duration_hint": 7.5,
        "khmer_speech": "សព្វថ្ងៃ ខ្យល់ដែលយើងដកដង្ហើមមានអុកស៊ីសែនប្រហែល ២១ ភាគរយ ដែលជាបរិមាណដ៏ល្អឥតខ្ចោះសម្រាប់ជីវិតយើង។",
        "english_speech": "Right now, the air we breathe has about twenty-one percent oxygen. It is the perfect recipe that keeps us alive and healthy.",
        "action": "holding up a circular pie-chart hologram showing atmospheric gas percentages",
        "environment": "cozy observatory laboratory",
        "emotion": "smart and educational"
    },
    {
        "scene_num": 3,
        "act": "Act 1: The Supercharged Morning (0 to 12 Hours)",
        "duration_hint": 7.5,
        "khmer_speech": "ប៉ុន្តែចុះបើស្អែកឡើង ពេលអ្នកភ្ញាក់ពីគេង ស្រាប់តែតួលេខនេះហក់ឡើងដល់ ៤២ ភាគរយវិញនោះ?",
        "english_speech": "But what if you wake up tomorrow morning, look at the weather meter, and it jumped all the way to forty-two percent?",
        "action": "pointing with wide shocked eyes at a digital gauge spiking violently into the red",
        "environment": "high-tech weather station",
        "emotion": "shocked and startled"
    },
    {
        "scene_num": 4,
        "act": "Act 1: The Supercharged Morning (0 to 12 Hours)",
        "duration_hint": 7.5,
        "khmer_speech": "អ្នកបើកបង្អួច ដកដង្ហើមវែងមួយចូលទៅក្នុងសួត... វ៉ាវ! ខ្យល់អាកាសត្រជាក់ស្រួល និងមានអារម្មណ៍ស្រស់ថ្លាប្លែកភ្នែក!",
        "english_speech": "You stretch, open your window, and take a deep breath. Instantly, the air feels crisp, electric, and super refreshing!",
        "action": "taking a deep euphoric breath with hands on chest and shining eyes",
        "environment": "sunny bedroom window overlooking morning city",
        "emotion": "rejuvenated and amazed"
    },
    {
        "scene_num": 5,
        "act": "Act 1: The Supercharged Morning (0 to 12 Hours)",
        "duration_hint": 7.5,
        "khmer_speech": "អ្នកមានអារម្មណ៍ថាខ្លួនឯងមានកម្លាំងពេញទំហឹង! អ្នកអាចរត់យ៉ាងលឿនតាមផ្លូវ ដោយមិនដឹងហត់សូម្បីតែបន្តិច!",
        "english_speech": "Suddenly, you have boundless energy! You could sprint down the street faster than sports cars without even panting!",
        "action": "sprinting effortlessly past sports cars with a cartoon trail of sparks",
        "environment": "colorful city park track",
        "emotion": "thrilled and energetic"
    },
    {
        "scene_num": 6,
        "act": "Act 1: The Supercharged Morning (0 to 12 Hours)",
        "duration_hint": 7.5,
        "khmer_speech": "អ្នកមានអារម្មណ៍ដូចជាកំពូលវីរបុរស! លើករបស់ធ្ងន់ៗ ឬរើថ្មធំៗ ស្រាលដូចសំឡី!",
        "english_speech": "You feel like a real-life superhero! Lifting heavy backpacks and moving giant rocks feels as light as a feather!",
        "action": "lifting a giant cartoon boulder with one hand with a triumphant grin",
        "environment": "mountain hiking trail",
        "emotion": "confident superhero"
    },
    {
        "scene_num": 7,
        "act": "Act 1: The Supercharged Morning (0 to 12 Hours)",
        "duration_hint": 7.5,
        "khmer_speech": "ម៉ាស៊ីនឡាន និងយន្តហោះក៏ឆេះសន្ធោសន្ធៅខ្លាំង ហោះហើរ និងរត់ទៅមុខយ៉ាងលឿនដូចគ្រាប់រ៉ុក្កែត!",
        "english_speech": "Engines love extra oxygen too! Car engines burn fuel with ferocious power, zooming forward like mini rockets!",
        "action": "standing next to a retro cartoon rocket car zooming forward with clean cyan flames",
        "environment": "futuristic highway",
        "emotion": "excited and awe-struck"
    },
    {
        "scene_num": 8,
        "act": "Act 1: The Supercharged Morning (0 to 12 Hours)",
        "duration_hint": 7.5,
        "khmer_speech": "ខ្យល់កាន់តែណែន ធ្វើឱ្យយន្តហោះក្រដាសអាចហោះអណ្តែតលើអាកាសបានរាប់រយម៉ែត្រដោយមិនងាយធ្លាក់!",
        "english_speech": "Because the air is thicker, paper airplanes can glide smoothly for hundreds of meters without falling!",
        "action": "throwing a small white paper airplane that floats smoothly without descending",
        "environment": "bright open grassy meadow",
        "emotion": "playful and delighted"
    },
    {
        "scene_num": 9,
        "act": "Act 1: The Supercharged Morning (0 to 12 Hours)",
        "duration_hint": 7.5,
        "khmer_speech": "មនុស្សគ្រប់គ្នាស្រែកអបអរសាទរ ដោយគិតថានេះជាកាដូដ៏អស្ចារ្យបំផុតដែលធម្មជាតិបានផ្តល់ឱ្យ!",
        "english_speech": "People everywhere celebrate! It feels like humanity just received the greatest physical upgrade in history!",
        "action": "cheering in a crowded town square holding festive scientific banners",
        "environment": "bustling sunny town square",
        "emotion": "joyful and celebratory"
    },
    {
        "scene_num": 10,
        "act": "Act 1: The Supercharged Morning (0 to 12 Hours)",
        "duration_hint": 7.5,
        "khmer_speech": "ប៉ុន្តែធម្មជាតិមានច្បាប់មួយ... អ្វីដែលផ្តល់ជីវិត ក៏អាចប្រែក្លាយទៅជាការសាកល្បងដ៏គ្រោះថ្នាក់បំផុតបានដែរ!",
        "english_speech": "But nature has a golden rule... What gives life can also turn into our greatest survival challenge!",
        "action": "lowering celebratory banner as a dark dramatic shadow falls across the screen",
        "environment": "dimming sky with ominous crimson clouds",
        "emotion": "suspicious and wary"
    },

    # Act 2: The Fire Threat & The Body's Limit (12 to 24 Hours)
    {
        "scene_num": 11,
        "act": "Act 2: The Fire Threat & The Body's Limit",
        "duration_hint": 7.5,
        "khmer_speech": "គ្រោះថ្នាក់ដំបូងបង្អស់ដែលលេចឡើងក្នុងរយៈពេលតែប៉ុន្មានម៉ោង គឺភ្លើង! អុកស៊ីសែនគឺជាចំណីដ៏ធំបំផុតរបស់ភ្លើង!",
        "english_speech": "The very first real danger appears within hours: FIRE. Oxygen is the favorite food of fire!",
        "action": "stepping back cautiously as a tiny matchstick bursts into a roaring torch flame",
        "environment": "cozy kitchen counter",
        "emotion": "alarmed and nervous"
    },
    {
        "scene_num": 12,
        "act": "Act 2: The Fire Threat & The Body's Limit",
        "duration_hint": 7.5,
        "khmer_speech": "អុកស៊ីសែនមិនឆេះដោយខ្លួនឯងទេ ប៉ុន្តែវាជួយឱ្យអណ្តាតភ្លើងឆាបឆេះយ៉ាងសន្ធោសន្ធៅ និងលឿនបំផុត!",
        "english_speech": "Oxygen does not burn by itself, but it makes any tiny flame roar with explosive fury!",
        "action": "pointing at a 3D animated fire tetrahedron diagram glowing violently",
        "environment": "dark scientific laboratory",
        "emotion": "intense and analytical"
    },
    {
        "scene_num": 13,
        "act": "Act 2: The Fire Threat & The Body's Limit",
        "duration_hint": 7.5,
        "khmer_speech": "គ្រាន់តែចុចកុងតាក់ភ្លើង ឬដោតឌុយឆ្នាំង ផ្កាភ្លើងតូចមួយអាចបង្កជាដុំភ្លើងឆាបឆេះពេញផ្ទះបាយភ្លាមៗ!",
        "english_speech": "If you try to toast some bread or start your car, a tiny spark can instantly explode into a raging fireball!",
        "action": "shielding face from sudden bright orange flames bursting from an electrical outlet",
        "environment": "modern urban apartment",
        "emotion": "panicked and defensive"
    },
    {
        "scene_num": 14,
        "act": "Act 2: The Fire Threat & The Body's Limit",
        "duration_hint": 7.5,
        "khmer_speech": "សូម្បីតែព្រៃឈើបៃតងសើមៗ ក៏អាចឆេះបានយ៉ាងងាយ ដូចជាចាក់ប្រេងសាំងលើគំនរក្រដាសស្ងួត!",
        "english_speech": "Even wet, green rainforests that never normally burn can catch fire like dry paper soaked in gasoline!",
        "action": "standing on a ridge watching a distant lush jungle suddenly explode in wall of flames",
        "environment": "cliff edge overlooking burning valley",
        "emotion": "horrified and stunned"
    },
    {
        "scene_num": 15,
        "act": "Act 2: The Fire Threat & The Body's Limit",
        "duration_hint": 7.5,
        "khmer_speech": "ក្រុមពន្លត់អគ្គិភ័យបាញ់ទឹកជួយសង្គ្រោះ ប៉ុន្តែភ្លើងក្តៅខ្លាំងពេក រហូតដល់ទឹកហួតក្លាយជាផ្សែងមុនពេលប៉ះដី!",
        "english_speech": "Firefighters spray water on the flames, but the heat is so intense that water evaporates into steam before it even lands!",
        "action": "holding a fire hose in miniature firefighter helmet as water turns into cartoon steam clouds",
        "environment": "smoky woodland road",
        "emotion": "overwhelmed and sweating"
    },
    {
        "scene_num": 16,
        "act": "Act 2: The Fire Threat & The Body's Limit",
        "duration_hint": 7.5,
        "khmer_speech": "ផ្សែងអ័ព្ទហុយពេញទីក្រុង ហើយខ្សែភ្លើងផ្ទុះជាបន្តបន្ទាប់ បង្ខំឱ្យអាជ្ញាធរប្រកាសអាសន្នទូទាំងក្រុង!",
        "english_speech": "Smoke fills the city skyline, and electrical wires spark and pop! Cities are forced to issue emergency warnings.",
        "action": "running through smoky city street as neon signs spark and flicker out",
        "environment": "apocalyptic cartoon cityscape under orange haze",
        "emotion": "frightened and rushing"
    },
    {
        "scene_num": 17,
        "act": "Act 2: The Fire Threat & The Body's Limit",
        "duration_hint": 7.5,
        "khmer_speech": "ទន្ទឹមនឹងនេះដែរ នៅក្នុងខ្លួនយើង អារម្មណ៍ស្រស់ស្រាយដំបូង ចាប់ផ្តើមប្រែទៅជាការឈឺចាប់យ៉ាងធ្ងន់ធ្ងរ។",
        "english_speech": "Meanwhile, inside your body, that amazing supercharged feeling takes a dark and painful turn.",
        "action": "clutching throat and chest with trembling hands and furrowed brow",
        "environment": "dim clinical examination room",
        "emotion": "gasping and distressed"
    },
    {
        "scene_num": 18,
        "act": "Act 2: The Fire Threat & The Body's Limit",
        "duration_hint": 7.5,
        "khmer_speech": "នេះហៅថាការពុលអុកស៊ីសែន។ នៅពេលយើងដកដង្ហើមយកអុកស៊ីសែនច្រើនជ្រុលពេក សួតរបស់យើងចាប់ផ្តើមរលាក។",
        "english_speech": "It is called Oxygen Poisoning, or Hyperoxia. When you breathe way too much oxygen, your lungs start to hurt.",
        "action": "pointing at a medical monitor showing spiking oxidative stress curves and red warnings",
        "environment": "high-tech medical bay",
        "emotion": "gravely serious"
    },
    {
        "scene_num": 19,
        "act": "Act 2: The Fire Threat & The Body's Limit",
        "duration_hint": 7.5,
        "khmer_speech": "ភាគល្អិតអុកស៊ីសែនដែលច្រើនលើសលុប ចាប់ផ្តើមវាយប្រហារកោសិកា និងសរសៃ DNA របស់យើងពីខាងក្នុង។",
        "english_speech": "Angry little oxygen particles attack your healthy cells and damage your DNA like tiny invisible needles.",
        "action": "watching a floating hologram of a DNA double helix being stripped by glowing jagged red particles",
        "environment": "microscopic laboratory background",
        "emotion": "dismayed and horrified"
    },
    {
        "scene_num": 20,
        "act": "Act 2: The Fire Threat & The Body's Limit",
        "duration_hint": 7.5,
        "khmer_speech": "មនុស្សជាច្រើនចាប់ផ្តើមវិលមុខ ស្រវាំងភ្នែក និងក្អកញាប់ៗ ពិបាកដកដង្ហើមចូលសួត។",
        "english_speech": "People begin feeling dizzy, vision gets blurry, and painful coughing fits make it hard to catch a breath.",
        "action": "stumbling dizzily holding head with cartoon swirl stars circling eyes",
        "environment": "crowded hospital triage tent",
        "emotion": "dizzy and exhausted"
    },
    {
        "scene_num": 21,
        "act": "Act 2: The Fire Threat & The Body's Limit",
        "duration_hint": 7.5,
        "khmer_speech": "មន្ទីរពេទ្យនានាពេញណែនដោយអ្នកជំងឺ ដែលរងគ្រោះដោយសារតែការដកដង្ហើមធម្មតានៅក្នុងបន្ទប់។",
        "english_speech": "Hospitals overflow with patients who got sick simply by breathing normal everyday room air.",
        "action": "wearing a protective respirator mask checking on small pill patients in hospital beds",
        "environment": "emergency hospital ward",
        "emotion": "compassionate and weary"
    },
    {
        "scene_num": 22,
        "act": "Act 2: The Fire Threat & The Body's Limit",
        "duration_hint": 7.5,
        "khmer_speech": "សម្លឹងមើលទៅក្រៅបង្អួច យើងដឹងច្បាស់នូវរឿងដ៏គួរឱ្យខ្លាចមួយ៖ ខ្យល់ដកដង្ហើមដែលធ្លាប់ចិញ្ចឹមជីវិត បានក្លាយជាគ្រោះថ្នាក់!",
        "english_speech": "Looking out the window, we realize something scary: the very air that keeps us alive has become dangerous.",
        "action": "looking out at the hazily glowing world through a sealed glass quarantine window",
        "environment": "quarantine bio-dome window",
        "emotion": "somber and contemplative"
    },

    # Act 3: History & The Giant Insect Era
    {
        "scene_num": 23,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "ដើម្បីយល់ពីអ្វីដែលនឹងកើតឡើងបន្ទាប់ យើងត្រូវក្រឡេកមើលប្រវត្តិសាស្ត្រផែនដី កាលពី ៣០០ លានឆ្នាំមុន!",
        "english_speech": "To understand where this story goes next, we have to travel back in Earth's history: 300 million years ago!",
        "action": "opening a giant glowing holographic portal into the prehistoric past",
        "environment": "dark museum gallery with glowing fossil displays",
        "emotion": "scholarly and focused"
    },
    {
        "scene_num": 24,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "កាលពីសម័យបុរេប្រវត្តិ ផែនដីពិតជាធ្លាប់មានអុកស៊ីសែនខ្ពស់ដល់ ៣៥ ភាគរយ ដូចសេណារីយ៉ូរបស់យើងពេលនេះអញ្ចឹង!",
        "english_speech": "Back in the prehistoric Carboniferous era, Earth actually had around 35 percent oxygen, almost like our scenario!",
        "action": "walking through a lush prehistoric swamp under giant primitive fern canopies",
        "environment": "Carboniferous swamp forest with giant mosses",
        "emotion": "captivated and cautious"
    },
    {
        "scene_num": 25,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "ចំណុចវិទ្យាសាស្ត្រដ៏គួរឱ្យចាប់អារម្មណ៍មួយគឺ៖ សត្វល្អិតគ្មានសួតដូចយើងទេ ពួកវាដកដង្ហើមតាមរន្ធតូចៗលើស្បែក!",
        "english_speech": "Here is a fascinating science fact: insects do not have lungs! They breathe directly through tiny holes in their skin.",
        "action": "magnifying a cartoon beetle with a glowing magnifying glass showing blue air channels",
        "environment": "bright outdoor botanical station",
        "emotion": "curious investigator"
    },
    {
        "scene_num": 26,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "ដោយសារពួកវាដកដង្ហើមតាមស្បែក ពេលអុកស៊ីសែនច្រើន ដែនកំណត់ទំហំរាងកាយរបស់សត្វល្អិតត្រូវបានដោះលែង!",
        "english_speech": "Because they breathe through their skin, double oxygen completely unlocks their body growth limits!",
        "action": "gasping as a small ant shadow on the ground grows into a massive cartoon silhouette",
        "environment": "jungle clearing floor",
        "emotion": "wide-eyed with shock"
    },
    {
        "scene_num": 27,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "សត្វកន្លាត និងពីងពាងចាប់ផ្តើមរីកធំធាត់ដល់ទំហំប៉ុនចានបាយ ឬធំប៉ុនសត្វកូនឆ្មា!",
        "english_speech": "Spiders and beetles begin growing to the size of dinner plates, and even as big as pet cats!",
        "action": "tiptoeing nervously past a giant friendly-looking but enormous colorful cartoon beetle",
        "environment": "giant oversized garden foliage",
        "emotion": "nervous and sneaking"
    },
    {
        "scene_num": 28,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "កន្ទុំរុយយក្សបុរាណដែលមានស្លាបប្រវែងស្មើនឹងកូនក្មេងម្នាក់ នឹងហោះត្រដាងស្លាបពេញផ្ទៃមេឃម្តងទៀត!",
        "english_speech": "Ancient giant dragonflies with wings as wide as an eagle would rule the skies once again!",
        "action": "ducking down as a magnificent giant cartoon dragonfly swoops gracefully overhead",
        "environment": "riverside marshland under bright sky",
        "emotion": "ducking and ducking"
    },
    {
        "scene_num": 29,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "ចុះសត្វទន្សាយ និងសត្វស្លាបគួរឱ្យស្រឡាញ់វិញ? តើពួកវាអាចរស់រានក្នុងបរិយាកាសដ៏ចម្លែកនេះដោយរបៀបណា?",
        "english_speech": "What about cute warm-blooded animals like rabbits and birds? How do they survive this strange atmosphere?",
        "action": "observing cartoon rabbits, deer, and sparrows with scientific binoculars",
        "environment": "woodland clearing near stream",
        "emotion": "thoughtful observer"
    },
    {
        "scene_num": 30,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "សត្វតូចៗដែលមានបេះដូងលោតញាប់ ឆាប់អស់កម្លាំងខ្លាំង ព្រោះរាងកាយរបស់ពួកវាឆេះថាមពលលឿនពេក។",
        "english_speech": "Small animals with fast heartbeats get exhausted very quickly as their bodies burn through energy too fast.",
        "action": "gently checking a small cartoon field mouse with a glowing stethoscope",
        "environment": "nature sanctuary research bench",
        "emotion": "gentle and caring"
    },
    {
        "scene_num": 31,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "ចុះទៅក្នុងបាតសមុទ្រ ទឹកសមុទ្រស្រូបយកអុកស៊ីសែនរលាយយ៉ាងច្រើន បង្កើតជាពពុះតូចៗដូចទឹកក្រូចកូកា!",
        "english_speech": "Down in the oceans, seawater absorbs huge amounts of dissolved oxygen, bubbling like fizzy soda!",
        "action": "wearing a small diving suit observing glowing oxygen bubbles rising in clear blue water",
        "environment": "vibrant coral reef underwater",
        "emotion": "curious diver"
    },
    {
        "scene_num": 32,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "ពពួកសារាយសមុទ្ររីកដុះដាលយ៉ាងសន្ធឹកសន្ធាប់ បង្កើតជាពន្លឺពណ៌បៃតងរលោងពាសពេញផ្ទៃទឹក!",
        "english_speech": "Glowing green sea algae explodes across the water, turning entire bays into bright emerald green!",
        "action": "looking down from a boat at vibrant bioluminescent green swirls in the ocean",
        "environment": "calm ocean surface under sunset",
        "emotion": "fascinated and mesmerized"
    },
    {
        "scene_num": 33,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "នៅតាមស្រែចម្ការ ដំណាំស្រូវ និងពោតចាប់ផ្តើមស្រពោន និងឡើងពណ៌លឿង ព្រោះមិនស៊ាំនឹងកម្រិតខ្យល់នេះ។",
        "english_speech": "On farmland, crops like rice and wheat get stressed by the intense air, causing their leaves to wilt and turn yellow.",
        "action": "examining a wilted yellowing crop leaf with a portable plant-scanner device",
        "environment": "wilted wheat crop field",
        "emotion": "concerned agronomist"
    },
    {
        "scene_num": 34,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "ការផ្គត់ផ្គង់ស្បៀងអាហារចាប់ផ្តើមធ្លាក់ចុះ បង្ខំឱ្យមនុស្សទូទាំងពិភពលោកត្រូវស្វែងរកដំណោះស្រាយជាបន្ទាន់។",
        "english_speech": "Food supplies start running low, forcing humans around the world to find smart new ways to feed everyone.",
        "action": "looking sadly at empty grain silos and a ticking global food supply monitor",
        "environment": "farming cooperative storehouse",
        "emotion": "worried and resolute"
    },
    {
        "scene_num": 35,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "ប៉ុន្តែមានរឿងល្អមួយ... ស្រទាប់អូហ្សូននៅលើមេឃឡើងក្រាស់ ក្លាយជាខែលការពារកម្តៅថ្ងៃស្ទើរតែ ១០០ ភាគរយ!",
        "english_speech": "On the bright side, the high atmosphere creates a super thick ozone shield that blocks almost all harmful sunburn rays!",
        "action": "pointing up with a smile as an invisible glowing blue shield reflects harsh purple UV cosmic rays",
        "environment": "mountaintop atmospheric observatory",
        "emotion": "hopeful and pointing"
    },
    {
        "scene_num": 36,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "ប៉ុន្តែដែក និងលោហធាតុជួបបញ្ហាធំ នោះគឺច្រែះ! ដែកគោល និងស្ពានកកើតច្រែះលឿនជាងធម្មតារាប់សិបដង!",
        "english_speech": "However, metals face a huge problem: SUPER RUST! Bridges, cars, and steel bolts rust ten times faster than normal.",
        "action": "scratching head looking at bright orange rust flaking off a large metal bolt on a bridge",
        "environment": "industrial suspension bridge",
        "emotion": "puzzled and concerned"
    },
    {
        "scene_num": 37,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "ក្រុមវិស្វករត្រូវប្រញាប់បាញ់ថ្នាំការពារពណ៌ខៀវលើធ្នឹមដែក ដើម្បីកុំឱ្យស្ពាន និងសំណង់នានាពុកផុយ។",
        "english_speech": "Maintenance crews must constantly spray protective blue sealants on metal beams so bridges do not break down.",
        "action": "wearing hardhat applying glowing blue anti-rust sealant spray to a structural beam",
        "environment": "active construction scaffold",
        "emotion": "focused engineer"
    },
    {
        "scene_num": 38,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "សម្ពាធខ្យល់ដ៏ណែន បង្កើតជាព្យុះផ្គររន្ទះពណ៌ស្វាយដ៏កាចសាហាវ បាញ់ផ្គរលាន់ឮសូរគ្រហឹមពេញភ្នំ!",
        "english_speech": "Dense, compressed air triggers massive purple lightning storms that roar across mountain peaks!",
        "action": "watching huge purple lightning bolts strike distant mountains from inside a control bunker",
        "environment": "meteorological storm bunker",
        "emotion": "alert and vigilant"
    },
    {
        "scene_num": 39,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "រន្ទះបាញ់ម្តងៗបង្កជាភ្លើងឆេះព្រៃយ៉ាងងាយ ធ្វើឱ្យផ្ទៃមេឃពេលល្ងាចប្រែជាពណ៌ក្រហមឆ្អៅដូចភ្លើង។",
        "english_speech": "Every single lightning bolt can ignite huge wildfires, painting the evening horizon in glowing crimson flames.",
        "action": "gazing out at a dramatically glowing crimson twilight sky filled with lightning reflections",
        "environment": "panoramic mountain vantage point",
        "emotion": "somber and watchful"
    },
    {
        "scene_num": 40,
        "act": "Act 3: History & The Giant Insect Era",
        "duration_hint": 7.5,
        "khmer_speech": "តុល្យភាពធម្មជាតិកំពុងស្ថិតក្នុងភាពរង្គោះរង្គើ។ តើមនុស្សយើងអាចរស់រានក្នុងពិភព What-If ដ៏ចម្លែកនេះដោយរបៀបណា?",
        "english_speech": "The balance of nature is tipping toward danger. How can human civilization survive this wild What-If world?",
        "action": "holding a delicately balanced antique brass scale that slowly tips toward danger",
        "environment": "scholarly planetary archives room",
        "emotion": "profoundly serious"
    },

    # Act 4: Human Ingenuity & Adaptation
    {
        "scene_num": 41,
        "act": "Act 4: Human Ingenuity & Adaptation",
        "duration_hint": 7.5,
        "khmer_speech": "មនុស្សជាតិមិនចុះចាញ់ងាយៗឡើយ! អាវុធដ៏ខ្លាំងបំផុតរបស់យើង គឺភាពវៃឆ្លាត និងការច្នៃប្រឌិតបច្ចេកវិទ្យា។",
        "english_speech": "Human beings never give up! Our greatest superpower has always been our intelligence and adaptability.",
        "action": "standing tall in clean futuristic coveralls, raising a glowing wrench with determination",
        "environment": "bustling tech workshop",
        "emotion": "determined and inspiring"
    },
    {
        "scene_num": 42,
        "act": "Act 4: Human Ingenuity & Adaptation",
        "duration_hint": 7.5,
        "khmer_speech": "វិស្វករបានបង្កើតផ្ទះកញ្ចក់ពិសេស ដែលមានប្រព័ន្ធចម្រោះខ្យល់ រក្សាកម្រិតអុកស៊ីសែន ២១ ភាគរយ ដូចដើមបេះបិទ!",
        "english_speech": "Engineers build pressurized bubble homes with smart filters that keep indoor air safe at the normal twenty-one percent!",
        "action": "adjusting a high-tech environmental control panel inside a sleek modular home",
        "environment": "cozy futuristic apartment living room",
        "emotion": "smart and methodical"
    },
    {
        "scene_num": 43,
        "act": "Act 4: Human Ingenuity & Adaptation",
        "duration_hint": 7.5,
        "khmer_speech": "នៅក្នុងផ្ទះនេះ យើងអាចដកដង្ហើមបានស្រួល គេងលក់ស្កប់ស្កល់ និងមានសុវត្ថិភាពពីផ្សែង និងភ្លើងខាងក្រៅ។",
        "english_speech": "Inside these safe zones, families can relax, sleep soundly, and breathe clean, refreshing air with zero coughing.",
        "action": "sitting in a comfy armchair drinking warm tea while looking peacefully through transparent dome",
        "environment": "warmly lit interior habitat dome",
        "emotion": "peaceful and relieved"
    },
    {
        "scene_num": 44,
        "act": "Act 4: Human Ingenuity & Adaptation",
        "duration_hint": 7.5,
        "khmer_speech": "នៅពេលចេញទៅខាងក្រៅ មនុស្សគ្រប់គ្នាពាក់ម៉ាសការពារពណ៌ខៀវស្រាល ដើម្បីចម្រោះខ្យល់ឱ្យមានសុវត្ថិភាព។",
        "english_speech": "Whenever going outdoors, everyone wears lightweight respirator masks that mix safe air into every breath.",
        "action": "adjusting a cool glowing cyan respirator mask over face before stepping through airlock",
        "environment": "airlock chamber door",
        "emotion": "ready and adventurous"
    },
    {
        "scene_num": 45,
        "act": "Act 4: Human Ingenuity & Adaptation",
        "duration_hint": 7.5,
        "khmer_speech": "យើងញ៉ាំផ្លែបឺរី និងផ្លែក្រូចស្រស់ៗ ដែលមានសារធាតុប្រឆាំងអុកស៊ីតកម្ម ដើម្បីការពារកោសិការាងកាយពីខាងក្នុង។",
        "english_speech": "People eat healthy berries and fresh citrus fruits rich in antioxidants to shield their body cells from oxygen wear.",
        "action": "eating a delicious bowl of glowing fresh blueberries and bright oranges with a cheerful smile",
        "environment": "futuristic hydroponic dining area",
        "emotion": "healthy and happy"
    },
    {
        "scene_num": 46,
        "act": "Act 4: Human Ingenuity & Adaptation",
        "duration_hint": 7.5,
        "khmer_speech": "កូនរ៉ូបូតពន្លត់អគ្គិភ័យស្វ័យប្រវត្តិក៏ត្រូវបានដាក់ពង្រាយ ដើម្បីបាញ់ពពុះត្រជាក់ពន្លត់ភ្លើងព្រៃឱ្យទាន់ពេលវេលា។",
        "english_speech": "Cute robotic fire drones patrol the forests, spraying cooling nitrogen foam to put out fires before they spread.",
        "action": "guiding a cute remote-controlled firefighting robot that shoots cooling nitrogen foam",
        "environment": "forest perimeter command center",
        "emotion": "innovative leader"
    },
    {
        "scene_num": 47,
        "act": "Act 4: Human Ingenuity & Adaptation",
        "duration_hint": 7.5,
        "khmer_speech": "សំណង់ផ្ទះថ្មីៗត្រូវបានសាងសង់ឡើងដោយប្រើថ្មសេរ៉ាមិចមិនឆេះ និងដែកទីតាន ដែលមិនកកើតច្រែះ។",
        "english_speech": "Builders replace rusty steel and dry wood with fireproof ceramic tiles and shiny rust-proof titanium.",
        "action": "inspecting blueprints alongside friendly pill architect colleagues",
        "environment": "sunlit architectural design office",
        "emotion": "visionary builder"
    },
    {
        "scene_num": 48,
        "act": "Act 4: Human Ingenuity & Adaptation",
        "duration_hint": 7.5,
        "khmer_speech": "ផ្ទះកញ្ចក់កសិកម្មទំនើបជួយឱ្យដំណាំស្រូវ និងបន្លែលូតលាស់បានយ៉ាងល្អ ធានាការផ្គត់ផ្គង់ស្បៀងឡើងវិញ។",
        "english_speech": "Special climate-controlled greenhouses grow giant golden wheat and vegetables, securing plenty of fresh food.",
        "action": "walking through rows of thriving, glowing giant golden wheat inside an enclosed glass greenhouse",
        "environment": "massive geodesic agricultural biodome",
        "emotion": "joyful farmer"
    },
    {
        "scene_num": 49,
        "act": "Act 4: Human Ingenuity & Adaptation",
        "duration_hint": 7.5,
        "khmer_speech": "អ្នកវិទ្យាសាស្ត្រសិក្សាពីហ្វូស៊ីលបុរាណ ដើម្បីរៀនពីរបៀបដែលភាវរស់ពីសម័យមុនធ្លាប់រស់រានក្នុងខ្យល់បែបនេះ។",
        "english_speech": "Scientists examine ancient fossils from 300 million years ago to discover how prehistoric creatures lived and adapted.",
        "action": "examining an ancient fossilized fern in stone under a gentle glowing holographic lamp",
        "environment": "paleontology research archive",
        "emotion": "deeply focused"
    },
    {
        "scene_num": 50,
        "act": "Act 4: Human Ingenuity & Adaptation",
        "duration_hint": 7.5,
        "khmer_speech": "អ្នកជិតខាងជួយគ្នាទៅវិញទៅមក ចែករំលែកធុងខ្យល់ស្អាត និងទឹកបរិសុទ្ធ បង្កើតជាសហគមន៍ដ៏កក់ក្តៅ។",
        "english_speech": "Neighbors band together, sharing clean air tanks and clean water. Human kindness helps communities thrive.",
        "action": "handing a glowing clean air canister to a grateful smiling neighbor with a warm handshake",
        "environment": "friendly community courtyard",
        "emotion": "kind and collaborative"
    },
    {
        "scene_num": 51,
        "act": "Act 4: Human Ingenuity & Adaptation",
        "duration_hint": 7.5,
        "khmer_speech": "ទីក្រុងក្រោមដីដ៏ស្រស់ស្អាត ដែលមានសួនច្បារ និងទឹកធ្លាក់ បង្ហាញពីភាពអស្ចារ្យនៃការតស៊ូរបស់មនុស្សជាតិ។",
        "english_speech": "Incredible underground cities with parks, waterfalls, and warm lights show how resilient humanity can be.",
        "action": "overlooking a breathtaking glowing underground city with parks and cascading fountains",
        "environment": "panoramic underground city balcony",
        "emotion": "proud and amazed"
    },
    {
        "scene_num": 52,
        "act": "Act 4: Human Ingenuity & Adaptation",
        "duration_hint": 7.5,
        "khmer_speech": "យើងមិនគ្រាន់តែរស់រានមានជីវិតទេ ប៉ុន្តែយើងបានរៀនច្បាស់ពីរបៀបថែរក្សា និងការពារភពផែនដីរបស់យើង។",
        "english_speech": "We didn't just survive—we learned how to master and protect our environment like true guardians of the planet.",
        "action": "high-fiving fellow scientists with a beaming smile around a glowing planetary hologram",
        "environment": "scientific mission control center",
        "emotion": "triumphant partner"
    },

    # Act 5: Grand Scientific Conclusion & The Golden Balance
    {
        "scene_num": 53,
        "act": "Act 5: Grand Scientific Conclusion & The Golden Balance",
        "duration_hint": 7.5,
        "khmer_speech": "យូរៗទៅ ដំណើរការគីមីធម្មជាតិ និងដីថ្ម បានចាប់ផ្តើមស្រូបយកអុកស៊ីសែនលើសត្រឡប់ទៅក្នុងដីវិញបន្តិចម្តងៗ។",
        "english_speech": "Over many decades, natural chemical reactions slowly trap the extra oxygen back into minerals and rocks.",
        "action": "watching glowing mineral veins absorb atmospheric particles into crystalline strata",
        "environment": "crystal cavern geological formation",
        "emotion": "intrigued observer"
    },
    {
        "scene_num": 54,
        "act": "Act 5: Grand Scientific Conclusion & The Golden Balance",
        "duration_hint": 7.5,
        "khmer_speech": "ផ្ទៃមេឃពណ៌ខៀវស្រឡះ និងខ្យល់ត្រជាក់ស្រួលបានវិលត្រឡប់មកវិញ ដោយបន្សល់ទុកមេរៀនវិទ្យាសាស្ត្រដ៏មានតម្លៃ។",
        "english_speech": "Peaceful blue skies and calm breezes return, leaving us with a priceless science lesson about Earth.",
        "action": "sitting peacefully on a green hill as clear blue skies and calm gentle breezes return",
        "environment": "peaceful hill with blooming wildflowers",
        "emotion": "calm and enlightened"
    },
    {
        "scene_num": 55,
        "act": "Act 5: Grand Scientific Conclusion & The Golden Balance",
        "duration_hint": 7.5,
        "khmer_speech": "ការពិសោធន៍គំនិតបែប What-If មួយនេះ បានបង្ហាញយើងនូវការពិតដ៏អស្ចារ្យមួយអំពីពិភពលោកដែលជាផ្ទះរបស់យើង។",
        "english_speech": "This What-If thought experiment reveals a wonderful, hidden truth about the world we call home.",
        "action": "holding up a small delicate glowing glass Earth globe in cupped hands",
        "environment": "warm ambient studio background",
        "emotion": "gentle and reverent"
    },
    {
        "scene_num": 56,
        "act": "Act 5: Grand Scientific Conclusion & The Golden Balance",
        "duration_hint": 7.5,
        "khmer_speech": "កម្រិតអុកស៊ីសែន ២១ ភាគរយ មិនមែនជារឿងចៃដន្យទេ ប៉ុន្តែជាតុល្យភាពមាសដ៏ល្អឥតខ្ចោះនៃជីវិត។",
        "english_speech": "Twenty-one percent oxygen is not an accident—it is the magical Goldilocks zone for life on Earth.",
        "action": "pointing thoughtfully at glowing balanced golden equations floating in the air",
        "environment": "clean minimalist infographics backdrop",
        "emotion": "master educator"
    },
    {
        "scene_num": 57,
        "act": "Act 5: Grand Scientific Conclusion & The Golden Balance",
        "duration_hint": 7.5,
        "khmer_speech": "តិចជាងនេះបន្តិច សត្វទាំងអស់នឹងថប់ដង្ហើម។ ច្រើនជាងនេះបន្តិច ពិភពលោកនឹងឆេះ ហើយសត្វល្អិតក្លាយជាយក្ស!",
        "english_speech": "A little less, and animals suffocate. A little more, and the whole planet burns and bugs grow into monsters!",
        "action": "gesturing between two contrasting cartoon holograms: frosty blue suffocation and blazing orange fire",
        "environment": "educational visual studio",
        "emotion": "dramatic and expressive"
    },
    {
        "scene_num": 58,
        "act": "Act 5: Grand Scientific Conclusion & The Golden Balance",
        "duration_hint": 7.5,
        "khmer_speech": "រាល់ដង្ហើមដែលយើងដកចូលរាល់ថ្ងៃ គឺជាអព្ភូតហេតុនៃធម្មជាតិដ៏មានតម្លៃបំផុតដែលយើងត្រូវស្រឡាញ់ និងថែរក្សា។",
        "english_speech": "Every single breath you take right now is a silent miracle of physics and biology that we should truly treasure.",
        "action": "taking a gentle peaceful breath smiling warmly with hands over heart",
        "environment": "radiant sunrise over tranquil green valley",
        "emotion": "deeply grateful"
    },
    {
        "scene_num": 59,
        "act": "Act 5: Grand Scientific Conclusion & The Golden Balance",
        "duration_hint": 7.5,
        "khmer_speech": "វិទ្យាសាស្ត្រគឺជាពន្លឺដែលជួយឱ្យយើងយល់ដឹង ស្រឡាញ់ និងការពារភពផែនដីដ៏កក់ក្តៅតែមួយគត់របស់យើង។",
        "english_speech": "Science is the light that helps us understand, respect, and protect this tiny blue marble floating in space.",
        "action": "holding a small lantern whose warm friendly light pushes back the vast velvet cosmic darkness",
        "environment": "edge of Earth looking toward gentle starlight",
        "emotion": "inspiring guide"
    },
    {
        "scene_num": 60,
        "act": "Act 5: Grand Scientific Conclusion & The Golden Balance",
        "duration_hint": 7.5,
        "khmer_speech": "ចុះអ្នកវិញ? តើអ្នកចង់បានកម្លាំងរត់លឿន ប្តូរជាមួយការរស់នៅក្បែរសត្វល្អិតយក្សប៉ុនកូនឆ្មាដែរឬទេ?",
        "english_speech": "What about you? Would you trade super-running speed if it meant living with hawk-sized dragonflies?",
        "action": "leaning forward with friendly grin, cupping ear toward the viewer",
        "environment": "cozy animation studio set with interactive speech bubbles",
        "emotion": "engaging and humorous"
    },
    {
        "scene_num": 61,
        "act": "Act 5: Grand Scientific Conclusion & The Golden Balance",
        "duration_hint": 7.5,
        "khmer_speech": "សូមបញ្ចេញមតិយោបល់របស់អ្នកនៅខាងក្រោម! តើអ្នកចង់ឱ្យយើងធ្វើវីដេអូ What-If អំពីរឿងអ្វីទៀត?",
        "english_speech": "Tell us your thoughts in the comments below! What other 'What If' question should we explore next?",
        "action": "pointing enthusiastically down toward an animated glowing comment box icon",
        "environment": "vibrant studio floor with animated likes",
        "emotion": "welcoming and lively"
    },
    {
        "scene_num": 62,
        "act": "Act 5: Grand Scientific Conclusion & The Golden Balance",
        "duration_hint": 7.5,
        "khmer_speech": "សូមកុំភ្លេចចុច Like និង Subscribe ដើម្បីកុំឱ្យខកខានការផ្សងព្រេងវិទ្យាសាស្ត្របន្ទាប់ទៀត! ជួបគ្នាវគ្គក្រោយ!",
        "english_speech": "Don't forget to like and subscribe so you never miss our next curious adventure! See you next time!",
        "action": "jumping in the air with joyful thumbs up as colorful confetti and Subscribe bell pop with sparkle",
        "environment": "festive animated channel outro screen with confetti",
        "emotion": "triumphant and waving"
    }
]

for sc in scenes:
    sc["full_prompt"] = (
        f"{CHARACTER_BASE_PROMPT} "
        f"The cute pill character is {sc.get('emotion', 'curious')}, {sc.get('action', '')}. "
        f"Environment: {sc.get('environment', '')}. "
        f"Infographic 2D vector style, vibrant Kurzgesagt aesthetic, clean bold line art, 16:9 ratio."
    )

output_data = {
    "title_en": "What If Oxygen Doubled on Earth?",
    "title_km": "ចុះបើកម្រិតអុកស៊ីសែនកើនឡើងទ្វេដង?",
    "total_scenes": len(scenes),
    "estimated_duration_minutes": 8,
    "scenes": scenes
}

out_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'custom_scripts', 'oxygen_double.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(scenes)} scenes in {out_path}")
