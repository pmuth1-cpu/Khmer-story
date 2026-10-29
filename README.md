# 🎬 YouTube Automation: Cartoon Pill Style (Nano Banana + Khmer Voice & Captions)

ប្រព័ន្ធស្វ័យប្រវត្តិកម្មបង្កើតវីដេអូ YouTube បែប **"What If" (ចុះបើ...)** និង **"Why / How" (ហេតុអ្វី និងរបៀបណា...)** ដោយប្រើតួអង្គ **Cartoon Pill (រាងកន្សោមថ្នាំ cute vector Kurzgesagt style)** ជាមួយរូបភាពពី **Nano Banana** រួមទាំងសំឡេងនិយាយ និងអក្សររត់ភាសាខ្មែរ (.srt / burned captions)។

---

## 🌟 លក្ខណៈពិសេសសំខាន់ៗ (Key Features)

1. **ស្ទីលរូបភាព Nano Banana Cartoon Pill Consistency**:
   - រក្សាទម្រង់តួអង្គកន្សោមថ្នាំពណ៌លឿង/ស (Cute anthropomorphic pill capsule) ឱ្យដូចគ្នានៅគ្រប់ប្លង់ (Scene 1 ដល់ Scene 10)។
   - ស្ទីល 2D flat vector, ពណ៌ដិតស្រស់ស្អាត (Kurzgesagt / educational cartoon style)។
   - រូបភាពនីមួយៗបង្ហាញពី **5 ទៅ 10 វិនាទី** ក្នុងមួយប្លង់ ជាមួយចលនា **Ken Burns (Slow Pan/Zoom)** ដើម្បីឱ្យវីដេអូមានភាពរស់រវើកដូចគំនូរជីវចល។

2. **សំឡេងនិយាយភាសាខ្មែរធម្មជាតិ (Neural Khmer TTS)**:
   - ប្រើប្រាស់ Neural Voices គុណភាពខ្ពស់ពី Microsoft:
     - 👨 `km-KH-PisethNeural` (សំឡេងប្រុស រួសរាយ រស់រវើក)
     - 👩 `km-KH-SreymomNeural` (សំឡេងស្រី ច្បាស់ និងស្រទន់)
   - គណនាពេលវេលានិយាយ និងកំណត់រយៈពេលប្លង់រូបភាពដោយស្វ័យប្រវត្តិ។

3. **អក្សររត់ភាសាខ្មែរត្រឹមត្រូវ (Khmer Subtitles & Captions)**:
   - ប្រើប្រាស់ពុម្ពអក្សរ **Kantumruy Pro / Khmer UI** ធានាការផ្គុំជើងអក្សរ និងស្រៈត្រឹមត្រូវ ១០០% ដោយគ្មានសញ្ញាការ៉ូឡើយ។
   - បង្កើតឯកសារ `.srt` សម្រាប់ Upload ទៅ YouTube Subtitles ដោយផ្ទាល់។
   - Burned-in Subtitles នៅលើវីដេអូស្រាប់ (1080p Full HD)។

4. **ផ្ទាំងបញ្ជា Web Dashboard + CLI**:
   - អាចដំណើរការតាមរយៈ Web Browser យ៉ាងងាយស្រួល (http://localhost:5000) ឬតាម command line។

---

## 🚀 របៀបប្រើប្រាស់ (Quick Start)

### ជម្រើសទី ១: ដំណើរការតាមរយៈ Web Dashboard (ងាយស្រួលបំផុត)

បើក terminal រួចវាយពាក្យបញ្ជា៖
```bash
python web_ui.py
```
បន្ទាប់មកបើក browser ទៅកាន់: **`http://localhost:5000`**

នៅក្នុង Web Dashboard អ្នកអាច៖
- ជ្រើសរើសប្រធានបទ (Topic): *ភ្លៀងធ្លាក់មួយខែ, យុគសម័យទឹកកក, ព្រះអាទិត្យបាត់ខ្លួន, មហាសមុទ្ររីងស្ងួត...*
- ចុច **Copy Prompt** សម្រាប់ប្លង់នីមួយៗយកទៅ Gen ក្នុង Nano Banana / Imagen / Midjourney។
- ជ្រើសរើសសំឡេង (Piseth ឬ Sreymom)។
- ចុច **🚀 បង្កើតវីដេអូពេញលេញ (Render Video)** ហើយទស្សនានិងទាញយក MP4 ភ្លាមៗ!

---

### ជម្រើសទី ២: ដំណើរការតាម Command Line (CLI)

បង្កើតវីដេអូប្រធានបទ "ភ្លៀងធ្លាក់មួយខែ" (Rain for a Month):
```bash
python main.py --theme rain_for_month --voice km-KH-PisethNeural
```

បង្កើតវីដេអូប្រធានបទ "យុគសម័យទឹកកក" (Humans in the Ice Age):
```bash
python main.py --theme ice_age_survival --voice km-KH-SreymomNeural
```

---

## 🎨 រចនាសម្ព័ន្ធ Prompt សម្រាប់ Nano Banana

ឯកសារ `nano_banana_prompts.txt` នឹងត្រូវបានបង្កើតឡើងដោយស្វ័យប្រវត្តិនៅក្នុង folder `output/` សម្រាប់គម្រោងនីមួយៗ។ ឧទាហរណ៍ Prompt សម្រាប់ប្លង់ Scene 1៖

```text
Cute anthropomorphic pill capsule cartoon character, smooth rounded pill body with vibrant colors, large expressive circular cartoon eyes with glossy pupils, tiny adorable stubby limbs, minimal clean design, Kurzgesagt and infographic cartoon aesthetic, flat vector 2D art style, clean outline, bold vibrant colors, crisp 4k digital illustration, cinematic educational animation still. The pill character is curious and questioning, standing on green grass looking up at the sky with curious big eyes. Setting: blue sky starting to be covered by giant fluffy cartoon dark rain clouds. vector art style, highly detailed, colorful vivid background, smooth soft lighting, child-friendly science educational cartoon, trending on ArtStation, 16:9 ratio.
```

### របៀបដាក់រូបភាពផ្ទាល់ខ្លួនពី Nano Banana ចូលទៅក្នុងវីដេអូ៖
1. Copy Prompts ពី `output/<project_name>/nano_banana_prompts.txt` ទៅ Gen ក្នុង Nano Banana។
2. Save រូបភាពដាក់ឈ្មោះ `scene_01.png`, `scene_02.png`, `scene_03.png`, ... ទៅក្នុង folder `output/<project_name>/images/`។
3. ដំណើរការ `python main.py` ម្តងទៀត ប្រព័ន្ធនឹងយកផ្ទាំងគំនូរជាក់ស្តែងរបស់អ្នកមកផ្គុំជាវីដេអូពេញលេញភ្លាមៗ!

---

## 📁 រចនាសម្ព័ន្ធ Folder (Project Structure)

```text
joyful-faraday/
├── src/
│   ├── prompt_generator.py    # ប្រព័ន្ធបង្កើត Nano Banana Cartoon Pill Prompts
│   ├── tts_engine.py          # បង្កើតសំឡេងខ្មែរ (Edge-TTS) និងកាលវិភាគ Subtitles
│   ├── image_helper.py        # ជំនួយការនាំចេញ Prompts និងគំនូរប្លង់បណ្តោះអាសន្ន
│   ├── video_builder.py       # FFmpeg Engine: Zoom/Pan, Merge Audio, Burn Subtitles
│   └── script_generator.py    # បណ្តុំប្រធានបទ What If / How-Why Scripts
├── assets/
│   └── fonts/
│       └── KantumruyPro.ttf   # Google Font សម្រាប់អក្សររត់ខ្មែរស្រស់ស្អាត
├── output/
│   └── rain_for_month_video/
│       ├── final_youtube_video.mp4  # វីដេអូចុងក្រោយ (1080p YouTube Ready)
│       ├── captions.srt             # អក្សររត់ SRT សម្រាប់ YouTube
│       ├── captions.ass             # Subtitle styling file
│       ├── nano_banana_prompts.txt  # បណ្តុំ Prompts សម្រាប់យកទៅ Gen
│       ├── audio/                   # សំឡេងអានខ្មែរតាមប្លង់នីមួយៗ
│       └── images/                  # រូបភាពប្លង់នីមួយៗ
├── main.py                    # CLI Pipeline Generator
├── web_ui.py                  # Web Dashboard Studio
└── README.md
```
