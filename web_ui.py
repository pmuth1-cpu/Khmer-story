"""
Khmer Cartoon Studio 4.0 - Multi-Topic Curiosity Suite.
Dedicated Natural Khmer Voice Engine (Google Khmer Neural & Meta MMS-TTS),
Accurate scene-by-scene audio generation from Khmer speech scripts,
Intelligent Multi-Pattern Batch Image Upload (Strict 1..N Scene Mapping),
Multi-Threaded Fast Video Rendering (Parallel Encoding & Clip Cache),
Clean Transparent Floating Captions (No Background Box),
and Real-time Render Progress Tracker.
"""

import os
import re
import json
import asyncio
import threading
from typing import Dict, Optional, List
from flask import Flask, request, jsonify, send_from_directory, render_template_string, Response

from src.pipeline_manager import (
    get_or_create_project_script,
    resolve_scene_image,
    execute_longform_pipeline
)
from src.longform_script_generator import (
    EXPANDED_CURIO_TOPICS,
    export_google_flow_prompts
)
from src.custom_topic_ai import sanitize_slug, create_ai_longform_script
from src.meta_mms_engine import generate_meta_mms_speech, generate_meta_mms_english_speech
from src.google_tts_engine import generate_google_khmer_speech
from src.edge_tts_engine import generate_edge_tts_speech

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CUSTOM_SCRIPTS_DIR = os.path.join(BASE_DIR, "custom_scripts")
os.makedirs(CUSTOM_SCRIPTS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Global in-memory render progress tracker
RENDER_STATUS = {}

# Full Kiri TTS Khmer Voice Actor Roster
KIRI_VOICE_ACTORS = [
    {"id": "Chanda", "name": "Chanda", "gender": "male", "tag": "ប្រុស - រស់រវើក (Energetic)"},
    {"id": "Dara", "name": "Dara", "gender": "male", "tag": "ប្រុស - និទានរឿង (Storyteller)"},
    {"id": "Borey", "name": "Borey", "gender": "male", "tag": "ប្រុស - ភាពយន្តឯកសារ (Documentary)"},
    {"id": "Rithy", "name": "Rithy", "gender": "male", "tag": "ប្រុស - សំឡេងជ្រៅ និងរឹងមាំ (Deep)"},
    {"id": "Setha", "name": "Setha", "gender": "male", "tag": "ប្រុស - ធម្មជាតិ (Natural)"},
    {"id": "Oudom", "name": "Oudom", "gender": "male", "tag": "ប្រុស - ព័ត៌មាន និងអប់រំ (Educational)"},
    {"id": "Arun", "name": "Arun", "gender": "male", "tag": "ប្រុស - ស្រទន់ (Calm)"},
    {"id": "Bora", "name": "Bora", "gender": "male", "tag": "ប្រុស - កំប្លុកកំប្លែង (Casual)"},
    {"id": "Seth", "name": "Seth", "gender": "male", "tag": "ប្រុស - យុវវ័យ (Youthful)"},
    {"id": "Maly", "name": "Maly", "gender": "female", "tag": "ស្រី - ធម្មជាតិ និងផ្អែមល្ហែម (Natural)"},
    {"id": "Nita", "name": "Nita", "gender": "female", "tag": "ស្រី - និទានរឿង (Storyteller)"},
    {"id": "Neary", "name": "Neary", "gender": "female", "tag": "ស្រី - ស្រទន់ (Gentle)"},
    {"id": "Theary", "name": "Theary", "gender": "female", "tag": "ស្រី - អប់រំ និងច្បាស់ (Clear)"},
    {"id": "Bosba", "name": "Bosba", "gender": "female", "tag": "ស្រី - អក្សរសាស្ត្រ និងរឿងព្រេង (Poetic)"},
    {"id": "Phanin", "name": "Phanin", "gender": "female", "tag": "ស្រី - រស់រវើក (Lively)"},
    {"id": "Mey", "name": "Mey", "gender": "female", "tag": "ស្រី - យុវវ័យ (Bright)"},
    {"id": "Soklin", "name": "Soklin", "gender": "female", "tag": "ស្រី - ព័ត៌មាន (News)"},
    {"id": "Sota", "name": "Sota", "gender": "female", "tag": "ស្រី - ស្រទន់ (Calm)"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="km">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Khmer Cartoon Studio 4.0 (Natural Khmer Voice & Fast Render)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Kantumruy+Pro:wght@400;600;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', 'Kantumruy Pro', sans-serif; }
    .khmer-font { font-family: 'Kantumruy Pro', sans-serif; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen">

  <!-- Header -->
  <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur px-6 py-4 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-11 h-11 rounded-full bg-gradient-to-tr from-amber-400 via-yellow-300 to-amber-500 flex items-center justify-center shadow-lg shadow-amber-500/20">
          <span class="text-2xl">💊</span>
        </div>
        <div>
          <h1 class="font-bold text-lg leading-tight flex items-center gap-2">
            Khmer Cartoon Studio <span class="text-xs bg-amber-400/20 text-amber-300 px-2.5 py-0.5 rounded-full border border-amber-400/40">Natural Voice & Curiosity</span>
          </h1>
          <p class="text-xs text-slate-400 khmer-font">ផលិតវីដេអូវែង ៨-១៥ នាទី បែប Human Pill Cartoon • សំឡេងធម្មជាតិ 100% Free • Multi-Core Turbo Render</p>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          Natural Khmer Voice Ready
        </span>
      </div>
    </div>
  </header>

  <!-- Main Grid -->
  <main class="max-w-7xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-8">
    
    <!-- Left Column: Controls (4 cols) -->
    <div class="lg:col-span-4 space-y-6">
      
      <!-- Instant Topic Creator Box -->
      <div class="bg-slate-900/95 border border-amber-500/30 rounded-2xl p-5 shadow-xl space-y-3">
        <div class="flex items-center justify-between">
          <h2 class="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
            <span>⚡</span> <span>បង្កើតប្រធានបទភ្លាមៗ (Instant Generator)</span>
          </h2>
          <span class="text-[10px] bg-amber-400/10 text-amber-300 px-2 py-0.5 rounded border border-amber-400/30">Auto Script</span>
        </div>

        <div>
          <input type="text" id="customTopicInput" placeholder="វាយសំណួរអ្វីក៏បាន (ឧ. ចុះបើគ្មានអ៊ីនធឺណិត ១ ខែ?)" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2.5 text-xs text-slate-100 focus:outline-none focus:border-amber-400 transition khmer-font">
        </div>

        <div class="flex items-center gap-2">
          <select id="customDurationSelect" class="w-1/2 bg-slate-950 border border-slate-700 rounded-xl px-2.5 py-2 text-xs text-slate-200 focus:outline-none focus:border-amber-400">
            <option value="8">⏱️ ៨ នាទី (~60 ប្លង់)</option>
            <option value="10" selected>⏱️ ១០ នាទី (~80 ប្លង់)</option>
            <option value="12">⏱️ ១២ នាទី (~95 ប្លង់)</option>
            <option value="15">⏱️ ១៥ នាទី (~120 ប្លង់)</option>
          </select>
          <button onclick="generateCustomTopic()" id="btnGenCustom" class="w-1/2 py-2 bg-gradient-to-r from-amber-500 to-yellow-400 hover:from-amber-400 hover:to-yellow-300 text-slate-950 font-bold rounded-xl text-xs shadow transition">
            🚀 បង្កើត Script ភ្លាមៗ
          </button>
        </div>
      </div>

      <!-- Preset Topics Library -->
      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-3">
        <div class="flex items-center justify-between">
          <h2 class="text-xs font-bold text-slate-300 uppercase tracking-wider">📚 បណ្ណាល័យប្រធានបទ (Topic Library)</h2>
          <span id="topicCountBadge" class="text-[10px] text-slate-500 font-mono">10 Topics</span>
        </div>
        
        <select id="themeSelect" onchange="loadActiveTopic()" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2.5 text-xs text-slate-100 focus:outline-none focus:border-amber-400 transition khmer-font">
          <!-- Dynamically populated topics -->
        </select>

        <p id="topicDescription" class="text-[11px] text-slate-400 italic bg-slate-950/60 p-2 rounded-lg border border-slate-800/80">...</p>

        <!-- Google Flow Export & Batch Buttons -->
        <div class="pt-3 border-t border-slate-800/80 grid grid-cols-2 gap-2">
          <a id="btnDownloadPrompts" href="#" target="_blank" class="px-3 py-2 text-center text-xs rounded-xl border border-slate-700 bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium transition flex items-center justify-center gap-1.5">
            <span>📥 Export Prompts</span>
          </a>
          <label class="cursor-pointer px-3 py-2 text-center text-xs rounded-xl border border-emerald-500/50 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 font-medium transition flex items-center justify-center gap-1.5">
            <span>📁 Batch Images (01...)</span>
            <input type="file" multiple accept="image/*" class="hidden" onchange="batchUploadImages(this.files)">
          </label>
        </div>
      </div>

      <!-- Voice Studio Section -->
      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-3">
        <div class="flex items-center justify-between">
          <h2 class="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
            <span>🎙️</span> <span>សំឡេងអាន (Khmer Voice Engine)</span>
          </h2>
          <span class="text-[10px] bg-emerald-500/10 text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/30">Local Offline VITS Model</span>
        </div>

        <select id="voiceEngineSelect" onchange="toggleVoiceEngine()" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2.5 text-xs text-slate-100 focus:outline-none focus:border-amber-400 khmer-font">
          <option value="edge_tts_chris" selected>🎙️ Christopher (Kurzgesagt Science Documentary • Deep & Emotional)</option>
          <option value="edge_tts_guy">🔥 Guy (Passionate Storyteller • Dynamic & Expressive)</option>
          <option value="meta_mms_eng">🇺🇸 Meta MMS English VITS (Offline VITS Model)</option>
          <option value="meta_mms">🤖 Meta MMS-TTS Khmer (Local Offline VITS Model)</option>
          <option value="google_tts">🌟 Google Khmer Neural (Natural Khmer Voice • 100% Free)</option>
          <option value="kiri_tts">🇰🇭 Kiri TTS (kiritts.com 19 Voice Actors)</option>
          <option value="custom_upload">🎤 Upload Custom Audio MP3 (CapCut / Voice Actor)</option>
        </select>

        <!-- Edge-TTS Christopher info & live player (Default Active) -->
        <div id="edgeChrisBox" class="p-3 bg-slate-950/80 rounded-xl border border-amber-400/40 text-[11px] text-slate-300 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-amber-300 font-semibold">Christopher (Kurzgesagt Style):</span>
            <span class="text-[10px] text-amber-400 font-mono">Deep & Emotional • 100% Free</span>
          </div>
          <p class="text-[11px] text-slate-400 leading-relaxed">សំឡេងនិទានបែបភាពយន្តឯកសារវិទ្យាសាស្ត្រ (Kurzgesagt / PBS Nova Style) មានមនោសញ្ចេតនាខ្ពស់ ចង្វាក់ឡើងចុះទាក់ទាញ និងមិនរឹង។</p>
          <div class="pt-1">
            <span class="text-[10px] text-amber-400 font-medium block mb-1">🎧 ស្តាប់សំឡេង Christopher (Emotional Documentary):</span>
            <audio controls class="w-full h-8 rounded-lg">
              <source src="/api/test_edge_chris_audio" type="audio/mp3">
            </audio>
          </div>
        </div>

        <!-- Edge-TTS Guy info & live player -->
        <div id="edgeGuyBox" class="hidden p-3 bg-slate-950/80 rounded-xl border border-rose-500/30 text-[11px] text-slate-300 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-rose-400 font-semibold">Guy (Passionate Storyteller):</span>
            <span class="text-[10px] text-rose-300 font-mono">Dynamic & Expressive</span>
          </div>
          <p class="text-[11px] text-slate-400 leading-relaxed">សំឡេងអានបែបភាពយន្ត រស់រវើក មានថាមពល និងអារម្មណ៍រំភើបខ្លាំង។</p>
          <div class="pt-1">
            <span class="text-[10px] text-rose-400 font-medium block mb-1">🎧 ស្តាប់សំឡេង Guy (Passionate Storyteller):</span>
            <audio controls class="w-full h-8 rounded-lg">
              <source src="/api/test_edge_guy_audio" type="audio/mp3">
            </audio>
          </div>
        </div>

        <!-- Meta MMS English VITS info & live player -->
        <div id="metaMmsEngBox" class="hidden p-3 bg-slate-950/80 rounded-xl border border-sky-500/30 text-[11px] text-slate-300 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-sky-400 font-semibold">Meta MMS English VITS:</span>
            <span class="text-[10px] text-sky-300 font-mono">Offline VITS</span>
          </div>
          <p class="text-[11px] text-slate-400 leading-relaxed">ម៉ូឌែល VITS ភាសាអង់គ្លេស ដំណើរការក្នុងកុំព្យូទ័រ Offline 100% គ្មានដែនកំណត់។</p>
          <div class="pt-1">
            <span class="text-[10px] text-sky-400 font-medium block mb-1">🎧 ស្តាប់សំឡេង Meta MMS English:</span>
            <audio controls class="w-full h-8 rounded-lg">
              <source src="/api/test_mms_eng_audio" type="audio/mp3">
            </audio>
          </div>
        </div>

        <!-- Meta MMS-TTS info & live player -->
        <div id="metaMmsBox" class="hidden p-3 bg-slate-950/80 rounded-xl border border-emerald-500/30 text-[11px] text-slate-300 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-emerald-400 font-semibold">Meta MMS Khmer VITS Model:</span>
            <span class="text-[10px] text-emerald-300 font-mono">Offline VITS</span>
          </div>
          <p class="text-[11px] text-slate-400 leading-relaxed">ម៉ូឌែល VITS ដំណើរការក្នុងកុំព្យូទ័រ Offline ដូចកំណែសាកល្បង (Test Version) ឥតគិតថ្លៃ ១០០%។</p>
          <div class="pt-1">
            <span class="text-[10px] text-amber-400 font-medium block mb-1">🎧 ស្តាប់សំឡេង VITS Khmer (Test Version):</span>
            <audio controls class="w-full h-8 rounded-lg">
              <source src="/api/test_mms_audio" type="audio/mp3">
            </audio>
          </div>
        </div>

        <!-- Google Khmer Neural info & live player -->
        <div id="googleTtsBox" class="hidden p-3 bg-slate-950/80 rounded-xl border border-slate-800 text-[11px] text-slate-300 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-amber-300 font-semibold">Google Khmer Neural Voice:</span>
            <span class="text-[10px] text-emerald-400 font-mono">Natural & Fluent • 100% Free</span>
          </div>
          <p class="text-[11px] text-slate-400 leading-relaxed">សំឡេងអានបែបធម្មជាតិ រលូន ច្បាស់ព្យញ្ជនៈ និងជើងអក្សរ ឥតគិតថ្លៃ ១០០% គ្មានកំណត់។</p>
          <div class="pt-1">
            <span class="text-[10px] text-amber-400 font-medium block mb-1">🎧 ស្តាប់សំឡេងធម្មជាតិ Google Khmer:</span>
            <audio controls class="w-full h-8 rounded-lg">
              <source src="/api/test_google_audio" type="audio/mp3">
            </audio>
          </div>
        </div>

        <!-- Kiri TTS Roster Box -->
        <div id="kiriBox" class="hidden space-y-2">
          <div class="p-3 bg-slate-950/80 rounded-xl border border-amber-500/30 text-[11px] text-slate-300 space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-amber-300 font-semibold">Kiri TTS Voice Actors:</span>
              <span class="text-[10px] text-amber-400 font-mono">kiritts.com</span>
            </div>
            <p class="text-[11px] text-slate-400 leading-relaxed">
              អ្នកអាច Copy Script ខាងក្រោម យកទៅបិទភ្ជាប់ក្នុងគេហទំព័រ <a href="https://kiritts.com" target="_blank" class="text-amber-400 underline">kiritts.com</a> ដើម្បីជ្រើសរើសសំឡេងតួសម្តែងអាជីព (Dara, Chanda, Maly) រួចទាញយក MP3 មក Upload ចូលទីនេះ៖
            </p>
            <button onclick="copyKiriScript()" class="w-full py-2 bg-amber-400 hover:bg-amber-300 text-slate-950 font-bold rounded-lg text-center text-xs transition">
              📋 ចម្លង Script ទាំងអស់សម្រាប់ kiritts.com
            </button>
          </div>
        </div>

        <!-- Custom Upload Box -->
        <div id="customUploadBox" class="hidden space-y-2">
          <label class="cursor-pointer block text-center py-2.5 px-3 border border-dashed border-emerald-500/60 bg-emerald-500/10 hover:bg-emerald-500/20 rounded-xl text-xs text-emerald-300 font-semibold transition">
            <span>📥 Upload Audio MP3 (CapCut / Voice Actor / Cloned Voice)</span>
            <input type="file" accept="audio/*" class="hidden" onchange="uploadVoiceTrack(this.files[0])">
          </label>
        </div>

        <!-- Render Action Buttons -->
        <div class="space-y-2 pt-2">
          <button onclick="startRenderPipeline(null)" id="btnStartRender" class="w-full py-3.5 px-4 bg-gradient-to-r from-amber-500 to-yellow-400 hover:from-amber-400 hover:to-yellow-300 text-slate-950 font-bold rounded-xl shadow-lg shadow-amber-500/20 active:scale-[0.98] transition flex items-center justify-center gap-2">
            <span>🚀 បង្កើតវីដេអូពេញលេញ (Fast Multi-Core Render)</span>
          </button>
          <button onclick="startRenderPipeline(5)" id="btnQuickRender" class="w-full py-2.5 px-4 bg-slate-800 hover:bg-slate-700 text-amber-300 font-semibold rounded-xl text-xs border border-amber-400/30 transition flex items-center justify-center gap-2">
            <span>⚡ Render សាកល្បង ៥ ប្លង់ (Quick 5-Scene Preview)</span>
          </button>
        </div>

        <!-- Render Progress Status Card -->
        <div id="renderProgressBox" class="hidden p-3.5 bg-slate-950 border border-amber-500/40 rounded-xl space-y-2">
          <div class="flex items-center justify-between text-xs">
            <span id="renderStepLabel" class="text-amber-300 font-medium">កំពុងដំណើរការ...</span>
            <span id="renderPercentLabel" class="font-mono text-slate-400">0%</span>
          </div>
          <div class="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden">
            <div id="renderProgressBar" class="bg-amber-400 h-2.5 rounded-full transition-all duration-300" style="width: 0%"></div>
          </div>
        </div>

      </div>

    </div>

    <!-- Right Column: Video Preview & Scenes Manager (8 cols) -->
    <div class="lg:col-span-8 space-y-6">

      <!-- Video Player Card -->
      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl">
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-sm font-semibold text-slate-100 flex items-center gap-2">
            <span>📺</span> <span>ការមើលវីដេអូជាមុន (Video Player Preview)</span>
          </h2>
          <span id="videoStatusBadge" class="text-xs px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300">Clean Subtitles • Human Pill</span>
        </div>

        <div class="relative aspect-video bg-black rounded-xl overflow-hidden border border-slate-800 flex items-center justify-center">
          <video id="player" controls class="w-full h-full object-contain">
            <source id="videoSource" src="" type="video/mp4">
            Your browser does not support the video tag.
          </video>
        </div>

        <div class="mt-4 flex flex-wrap items-center justify-between gap-3 text-xs">
          <div class="text-slate-400 flex items-center gap-3">
            <span>📥 ទាញយក:</span>
            <a id="downloadVideoBtn" href="#" download="khmer_cartoon_video.mp4" class="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 rounded-lg text-slate-200 transition font-medium">🎬 វីដេអូ MP4 (1080p)</a>
            <a id="downloadSrtBtn" href="#" download="captions.srt" class="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 rounded-lg text-slate-200 transition font-medium">📝 អក្សររត់ SRT</a>
          </div>
          <span class="text-slate-500 font-mono">1080p • Natural Voice • Multi-Core Turbo</span>
        </div>
      </div>

      <!-- YouTube Thumbnail Studio Card -->
      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl">
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center gap-2">
            <span class="text-lg">🖼️</span>
            <div>
              <h2 class="text-sm font-semibold text-slate-100 flex items-center gap-2">
                <span>រូបតំណាង YouTube (YouTube Thumbnail)</span>
                <span class="text-[11px] px-2 py-0.5 rounded-full bg-amber-400/20 text-amber-300 border border-amber-400/30">1280x720 HD • 16:9</span>
              </h2>
              <p class="text-xs text-slate-400">High-CTR Kurzgesagt 2D Vector & AI Art Thumbnail រចនាឡើងសម្រាប់ទាក់ទាញការចុចមើល</p>
            </div>
          </div>
          <span class="text-xs px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono font-bold">High CTR Ready</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
          <!-- Thumbnail Image Preview -->
          <div class="md:col-span-7 relative aspect-video bg-black rounded-xl overflow-hidden border border-slate-800 flex items-center justify-center group shadow-lg">
            <img id="thumbnailImg" src="" alt="YouTube Thumbnail" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-slate-950/60 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-3">
              <a id="downloadThumbnailBtn" href="#" download="youtube_thumbnail.png" class="px-4 py-2 bg-amber-400 hover:bg-amber-300 text-slate-950 font-bold rounded-lg shadow-xl text-xs transition flex items-center gap-2">
                <span>📥</span> ទាញយករូប Thumbnail (HD)
              </a>
            </div>
          </div>

          <!-- Thumbnail Actions & AI Prompts -->
          <div class="md:col-span-5 flex flex-col justify-between bg-slate-950/80 rounded-xl p-4 border border-slate-800 space-y-3">
            <div>
              <div class="text-xs font-semibold text-slate-200 mb-1 flex items-center gap-1.5">
                <span>✨</span> <span>AI Thumbnail Prompts (Nano Banana & Midjourney)</span>
              </div>
              <p class="text-[11px] text-slate-400 leading-relaxed mb-2.5">
                ចម្លង Prompt នេះទៅដាក់ក្នុង Nano Banana, Google Flow ឬ Midjourney ដើម្បីទទួលបានរូប Thumbnail ថ្មីៗបន្ថែមទៀត!
              </p>
              <textarea id="thumbnailPromptBox" readonly class="w-full h-24 bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-[11px] text-slate-300 font-mono resize-none focus:outline-none"></textarea>
            </div>
            <div class="flex items-center gap-2 pt-1">
              <button onclick="copyThumbnailPrompt()" class="flex-1 px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-medium transition flex items-center justify-center gap-1.5">
                <span>📋</span> ចម្លង Prompt
              </button>
              <a id="downloadThumbnailBtn2" href="#" download="youtube_thumbnail.png" class="px-3.5 py-2 bg-amber-400 hover:bg-amber-300 text-slate-950 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5">
                <span>📥</span> Download
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Scenes Breakdown & Batch Management -->
      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-sm font-semibold text-slate-100 flex items-center gap-2">
              <span>🎞️</span> <span>តារាងប្លង់វីដេអូ (Scenes Breakdown)</span>
            </h2>
            <p id="scenesCountHeader" class="text-xs text-slate-400 mt-0.5">កំពុងផ្ទុកប្លង់...</p>
          </div>
          <button onclick="copyAllPrompts()" class="text-xs text-amber-400 hover:text-amber-300 font-medium transition">
            📋 ចម្លង Prompts ទាំងអស់ (Copy All)
          </button>
        </div>

        <div id="scenesContainer" class="space-y-4 max-h-[750px] overflow-y-auto pr-2">
          <!-- Dynamically populated scenes -->
        </div>

      </div>

    </div>

  </main>

  <!-- Notification Toast -->
  <div id="toast" class="fixed bottom-6 right-6 bg-amber-400 text-slate-950 font-semibold px-4 py-3 rounded-xl shadow-2xl transition transform translate-y-20 opacity-0 pointer-events-none text-xs flex items-center gap-2 z-50">
    <span>✅</span> <span id="toastMsg">សារជូនដំណឹង</span>
  </div>

  <script>
    const PRESET_TOPICS = {{ topics|tojson }};
    const KIRI_VOICES = {{ voices|tojson }};
    let activeTopicId = 'oxygen_double';
    let currentScript = null;
    let renderPollInterval = null;

    function showToast(msg) {
      const toast = document.getElementById('toast');
      document.getElementById('toastMsg').innerText = msg;
      toast.classList.remove('translate-y-20', 'opacity-0');
      setTimeout(() => {
        toast.classList.add('translate-y-20', 'opacity-0');
      }, 3500);
    }

    function initInterface() {
      // Populate topics dropdown
      const sel = document.getElementById('themeSelect');
      sel.innerHTML = '';
      PRESET_TOPICS.forEach(t => {
        const opt = document.createElement('option');
        opt.value = t.id;
        opt.innerText = t.icon + ' ' + t.title_km;
        sel.appendChild(opt);
      });
      sel.value = 'oxygen_double';

      toggleVoiceEngine();
      loadActiveTopic();
    }

    function toggleVoiceEngine() {
      const mode = document.getElementById('voiceEngineSelect').value;
      document.getElementById('edgeChrisBox').style.display = (mode === 'edge_tts_chris') ? 'block' : 'none';
      document.getElementById('edgeGuyBox').style.display = (mode === 'edge_tts_guy') ? 'block' : 'none';
      document.getElementById('metaMmsEngBox').style.display = (mode === 'meta_mms_eng') ? 'block' : 'none';
      document.getElementById('metaMmsBox').style.display = (mode === 'meta_mms') ? 'block' : 'none';
      document.getElementById('googleTtsBox').style.display = (mode === 'google_tts') ? 'block' : 'none';
      document.getElementById('kiriBox').style.display = (mode === 'kiri_tts') ? 'block' : 'none';
      document.getElementById('customUploadBox').style.display = (mode === 'custom_upload') ? 'block' : 'none';
      showToast('បានជ្រើសរើស Voice Engine: ' + mode);
      
      // Refresh audio players with active engine
      if (currentScript && currentScript.scenes) {
        renderScenes(currentScript.scenes);
      }
    }

    async function loadActiveTopic() {
      activeTopicId = document.getElementById('themeSelect').value;
      
      const found = PRESET_TOPICS.find(t => t.id === activeTopicId);
      if (found) {
        document.getElementById('topicDescription').innerText = found.description || '';
      }

      const res = await fetch('/api/project/' + activeTopicId);
      currentScript = await res.json();

      document.getElementById('scenesCountHeader').innerText = 'ចំនួនប្លង់សរុប: ' + currentScript.scenes.length + ' ប្លង់ • រយៈពេលប៉ាន់ស្មាន: ' + (currentScript.estimated_duration_minutes || 8) + ' នាទី';
      document.getElementById('btnDownloadPrompts').href = '/api/project/' + activeTopicId + '/prompts_file';

      updateVideoPlayer();
      updateThumbnail();
      renderScenes(currentScript.scenes);
    }

    function updateVideoPlayer() {
      const player = document.getElementById('player');
      const vSrc = '/api/project/' + activeTopicId + '/video?t=' + Date.now();
      player.src = vSrc;
      document.getElementById('downloadVideoBtn').href = vSrc;
      document.getElementById('downloadSrtBtn').href = '/api/project/' + activeTopicId + '/subtitles';
    }

    async function updateThumbnail() {
      const now = Date.now();
      const thumbUrl = '/api/project/' + activeTopicId + '/thumbnail?t=' + now;
      const img = document.getElementById('thumbnailImg');
      if (img) img.src = thumbUrl;
      const btn1 = document.getElementById('downloadThumbnailBtn');
      if (btn1) btn1.href = '/api/project/' + activeTopicId + '/thumbnail';
      const btn2 = document.getElementById('downloadThumbnailBtn2');
      if (btn2) btn2.href = '/api/project/' + activeTopicId + '/thumbnail';

      try {
        const res = await fetch('/api/project/' + activeTopicId + '/thumbnail_prompts');
        const d = await res.json();
        const box = document.getElementById('thumbnailPromptBox');
        if (box && d.prompts) box.value = d.prompts;
      } catch (e) {
        console.error('Failed to fetch thumbnail prompt:', e);
      }
    }

    function copyThumbnailPrompt() {
      const box = document.getElementById('thumbnailPromptBox');
      if (!box || !box.value) return;
      navigator.clipboard.writeText(box.value).then(() => {
        showToast('ចម្លង AI Thumbnail Prompt បានជោគជ័យ!');
      });
    }

    function renderScenes(scenes) {
      const container = document.getElementById('scenesContainer');
      container.innerHTML = '';
      const now = Date.now();
      const engine = document.getElementById('voiceEngineSelect').value;

      scenes.forEach((sc) => {
        const card = document.createElement('div');
        card.className = 'p-4 rounded-xl bg-slate-950/80 border border-slate-800/80 space-y-3';
        const imgUrl = `/api/project/${activeTopicId}/image/${sc.scene_num}?t=${now}`;
        const audioUrl = `/api/project/${activeTopicId}/scene_audio/${sc.scene_num}?engine=${engine}&t=${now}`;

        card.innerHTML = `
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-amber-400 px-2 py-0.5 rounded bg-amber-400/10 border border-amber-400/20">
                ប្លង់ ${sc.scene_num} (${sc.duration_hint || 7.5}s)
              </span>
              <span class="text-[11px] text-slate-500 font-mono">${sc.act || ''}</span>
            </div>
            <div class="flex items-center gap-2">
              <label class="cursor-pointer text-[11px] text-emerald-400 hover:text-emerald-300 transition font-medium px-2 py-1 bg-emerald-500/10 rounded-lg border border-emerald-500/20">
                📁 Upload Image
                <input type="file" accept="image/*" class="hidden" onchange="uploadSingleImage(${sc.scene_num}, this.files[0])">
              </label>
              <button onclick="copyPrompt('${encodeURIComponent(sc.full_prompt)}')" class="text-[11px] text-slate-400 hover:text-amber-300 transition px-2 py-1 bg-slate-900 rounded-lg border border-slate-800">
                📋 Copy Prompt
              </button>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
            <div class="md:col-span-4 aspect-video bg-black rounded-lg overflow-hidden border border-slate-800 flex items-center justify-center relative">
              <img id="scene_img_${sc.scene_num}" src="${imgUrl}" class="w-full h-full object-cover">
            </div>
            <div class="md:col-span-8 space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-[11px] text-slate-400 font-medium">អត្ថបទសំឡេង (Narration Script):</span>
                <div class="flex items-center gap-1.5">
                  <span class="text-[10px] text-amber-300">🎙️ ស្តាប់សំឡេង:</span>
                  <audio controls class="h-6 w-36 rounded" src="${audioUrl}"></audio>
                </div>
              </div>
              <div class="space-y-1.5">
                <div class="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800/80">
                  <span class="text-[10px] text-amber-400 font-semibold block mb-0.5">🇰🇭 អត្ថបទខ្មែរ:</span>
                  <p class="khmer-font text-xs text-slate-200 leading-relaxed">${sc.khmer_speech || ''}</p>
                </div>
                ${sc.english_speech ? `
                <div class="p-2.5 rounded-lg bg-sky-950/20 border border-sky-800/40">
                  <span class="text-[10px] text-sky-400 font-semibold block mb-0.5">🇺🇸 English Narration:</span>
                  <p class="text-xs text-sky-200 leading-relaxed font-sans">${sc.english_speech}</p>
                </div>` : ''}
              </div>
              <div class="text-[10px] text-slate-500 font-mono truncate">Prompt: ${sc.full_prompt}</div>
            </div>
          </div>
        `;
        container.appendChild(card);
      });
    }

    async function generateCustomTopic() {
      const topicText = document.getElementById('customTopicInput').value.trim();
      const dur = parseInt(document.getElementById('customDurationSelect').value);
      if (!topicText) {
        alert('សូមវាយបញ្ចូលប្រធានបទ ឬសំណួររបស់អ្នក!');
        return;
      }

      const btn = document.getElementById('btnGenCustom');
      btn.disabled = true;
      btn.innerText = 'កំពុងបង្កើត...';

      try {
        const res = await fetch('/api/create_topic', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title_km: topicText, title_en: topicText, target_minutes: dur })
        });
        const data = await res.json();
        if (data.status === 'ok') {
          showToast('បានបង្កើត Script ថ្មីជោគជ័យ!');
          
          const sel = document.getElementById('themeSelect');
          const opt = document.createElement('option');
          opt.value = data.topic_id;
          opt.innerText = '✨ ' + data.title_km + ' (' + dur + ' min)';
          sel.insertBefore(opt, sel.firstChild);
          sel.value = data.topic_id;
          document.getElementById('customTopicInput').value = '';
          loadActiveTopic();
        }
      } catch (err) {
        alert('Error: ' + err);
      } finally {
        btn.disabled = false;
        btn.innerText = '🚀 បង្កើត Script ភ្លាមៗ';
      }
    }

    function copyKiriScript() {
      if (!currentScript) return;
      const fullText = currentScript.scenes.map(s => s.khmer_speech).join('\\n\\n');
      navigator.clipboard.writeText(fullText);
      showToast('បានចម្លងអត្ថបទពេញសម្រាប់ kiritts.com រួចរាល់!');
    }

    function copyPrompt(encoded) {
      navigator.clipboard.writeText(decodeURIComponent(encoded));
      showToast('បានចម្លង Prompt សម្រាប់ Google Flow!');
    }

    function copyAllPrompts() {
      if (!currentScript) return;
      const allText = currentScript.scenes.map(s => `Scene ${s.scene_num} (${s.act || ''}):\\n` + s.full_prompt).join('\\n\\n');
      navigator.clipboard.writeText(allText);
      showToast('បានចម្លង Prompts ទាំងអស់!');
    }

    async function uploadVoiceTrack(file) {
      if (!file) return;
      const formData = new FormData();
      formData.append('audio', file);
      formData.append('topic_id', activeTopicId);

      showToast('កំពុង Upload សំឡេង MP3...');
      try {
        const res = await fetch('/api/upload_voice_track', { method: 'POST', body: formData });
        const data = await res.json();
        if (data.status === 'ok') {
          showToast('បានបញ្ចូលសំឡេងជោគជ័យ!');
        }
      } catch (err) {
        alert('Upload audio error: ' + err);
      }
    }

    async function batchUploadImages(files) {
      if (!files || files.length === 0) return;
      const formData = new FormData();
      for (let i = 0; i < files.length; i++) {
        formData.append('images', files[i]);
      }
      formData.append('topic_id', activeTopicId);

      showToast(`កំពុង Upload រូបភាព ${files.length} សន្លឹកទៅកាន់ Scene Breakdown...`);
      try {
        const res = await fetch('/api/batch_upload_images', { method: 'POST', body: formData });
        const data = await res.json();
        if (data.status === 'ok') {
          showToast(`បានបញ្ចូល ${data.saved_count} រូបភាពជោគជ័យទៅក្នុងតារាងប្លង់!`);
          // Force complete refresh of thumbnails
          if (currentScript && currentScript.scenes) {
            renderScenes(currentScript.scenes);
          } else {
            loadActiveTopic();
          }
        }
      } catch (err) {
        alert('Batch upload error: ' + err);
      }
    }

    async function uploadSingleImage(sceneNum, file) {
      if (!file) return;
      const formData = new FormData();
      formData.append('image', file);
      formData.append('topic_id', activeTopicId);
      formData.append('scene', sceneNum);

      try {
        const res = await fetch('/api/upload_scene_image', { method: 'POST', body: formData });
        const data = await res.json();
        if (data.status === 'ok') {
          showToast(`បានបញ្ចូលរូបភាពប្លង់ ${sceneNum}!`);
          const img = document.getElementById(`scene_img_${sceneNum}`);
          if (img) {
            img.src = `/api/project/${activeTopicId}/image/${sceneNum}?t=${Date.now()}`;
          }
        }
      } catch (err) {
        alert('Error: ' + err);
      }
    }

    async function startRenderPipeline(maxScenes = null) {
      const btn = document.getElementById('btnStartRender');
      const qBtn = document.getElementById('btnQuickRender');
      const progressBox = document.getElementById('renderProgressBox');
      const stepLabel = document.getElementById('renderStepLabel');
      const percentLabel = document.getElementById('renderPercentLabel');
      const progressBar = document.getElementById('renderProgressBar');

      btn.disabled = true;
      qBtn.disabled = true;
      progressBox.classList.remove('hidden');
      stepLabel.innerText = 'កំពុងចាប់ផ្តើម Fast Render (Multi-Core)...';
      percentLabel.innerText = '0%';
      progressBar.style.width = '2%';
      progressBar.classList.remove('bg-emerald-500', 'bg-rose-500');
      progressBar.classList.add('bg-amber-400');

      const engine = document.getElementById('voiceEngineSelect').value;

      try {
        const res = await fetch('/api/render_project', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ topic_id: activeTopicId, max_scenes: maxScenes, voice_engine: engine })
        });
        const data = await res.json();
        if (data.status === 'started') {
          // Poll render progress
          if (renderPollInterval) clearInterval(renderPollInterval);
          renderPollInterval = setInterval(async () => {
            try {
              const sRes = await fetch(`/api/render_status/${activeTopicId}`);
              const sData = await sRes.json();
              
              if (sData.status === 'rendering') {
                const pct = sData.percent || 0;
                percentLabel.innerText = pct + '%';
                progressBar.style.width = pct + '%';
                stepLabel.innerText = sData.step || 'កំពុងដំណើរការ...';
              } else if (sData.status === 'complete') {
                clearInterval(renderPollInterval);
                percentLabel.innerText = '100%';
                progressBar.style.width = '100%';
                progressBar.classList.remove('bg-amber-400');
                progressBar.classList.add('bg-emerald-500');
                stepLabel.innerText = '✅ វីដេអូបាន Render រួចរាល់ ១០០%!';
                showToast('វីដេអូត្រូវបានផលិតជោគជ័យ!');
                updateVideoPlayer();
                btn.disabled = false;
                qBtn.disabled = false;
              } else if (sData.status === 'error') {
                clearInterval(renderPollInterval);
                stepLabel.innerText = '❌ កំហុស Render: ' + sData.error;
                progressBar.classList.add('bg-rose-500');
                btn.disabled = false;
                qBtn.disabled = false;
                alert('Render error: ' + sData.error);
              }
            } catch (pErr) {
              console.error('Poll error', pErr);
            }
          }, 1000);
        } else {
          alert('Render error: ' + (data.error || 'Failed to start'));
          btn.disabled = false;
          qBtn.disabled = false;
        }
      } catch (err) {
        alert('Render network error: ' + err);
        btn.disabled = false;
        qBtn.disabled = false;
      }
    }

    window.onload = initInterface;
  </script>
</body>
</html>
"""


def render_placeholder_svg(scene_num: int, topic_id: str) -> str:
    """Renders a clean styled SVG card when no image has been uploaded for a scene yet."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <linearGradient id="pillGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fbbf24"/>
      <stop offset="100%" stop-color="#f59e0b"/>
    </linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#bg)"/>
  
  <!-- Dashed border -->
  <rect x="40" y="40" width="1200" height="640" rx="24" fill="none" stroke="#334155" stroke-width="4" stroke-dasharray="16 12"/>
  
  <!-- Cute Pill Avatar Silhouette -->
  <g transform="translate(640, 290)">
    <!-- Pill Character Body -->
    <rect x="-65" y="-130" width="130" height="230" rx="65" fill="url(#pillGrad)" opacity="0.9"/>
    <!-- Cute Eyes -->
    <circle cx="-24" cy="-55" r="9" fill="#0f172a"/>
    <circle cx="24" cy="-55" r="9" fill="#0f172a"/>
    <circle cx="-21" cy="-58" r="3.5" fill="#ffffff"/>
    <circle cx="27" cy="-58" r="3.5" fill="#ffffff"/>
    <!-- Curious Smile -->
    <path d="M -14 -22 Q 0 -12 14 -22" stroke="#0f172a" stroke-width="4.5" fill="none" stroke-linecap="round"/>
    <!-- Hoodie Pocket / Detail -->
    <path d="M -35 25 Q 0 45 35 25" stroke="#b45309" stroke-width="3" fill="none" opacity="0.6"/>
  </g>

  <!-- Labels -->
  <text x="640" y="470" font-family="'Kantumruy Pro', 'Inter', sans-serif" font-size="34" font-weight="bold" fill="#f8fafc" text-anchor="middle">
    ប្លង់ទី {scene_num:02d} • Scene {scene_num:02d}
  </text>
  <text x="640" y="520" font-family="'Kantumruy Pro', 'Inter', sans-serif" font-size="22" fill="#94a3b8" text-anchor="middle">
    មិនទាន់មានរូបភាព (ចុច Upload Image ឬប្រើ Batch Images)
  </text>
  <text x="640" y="565" font-family="'Inter', sans-serif" font-size="16" fill="#64748b" text-anchor="middle">
    1920 × 1080 • Human Pill Silhouette Style
  </text>
</svg>"""


@app.route("/api/test_edge_chris_audio")
def get_test_edge_chris_audio():
    p = os.path.join(BASE_DIR, "test_edge_chris.mp3")
    if os.path.exists(p):
        return send_from_directory(BASE_DIR, "test_edge_chris.mp3")
    return "Not generated", 404


@app.route("/api/test_edge_guy_audio")
def get_test_edge_guy_audio():
    p = os.path.join(BASE_DIR, "test_edge_guy.mp3")
    if os.path.exists(p):
        return send_from_directory(BASE_DIR, "test_edge_guy.mp3")
    return "Not generated", 404


@app.route("/api/test_mms_eng_audio")
def get_test_mms_eng_audio():
    p = os.path.join(BASE_DIR, "test_mms_eng.mp3")
    if os.path.exists(p):
        return send_from_directory(BASE_DIR, "test_mms_eng.mp3")
    return "Not generated", 404


@app.route("/api/test_mms_audio")
def get_test_mms_audio():
    p = os.path.join(BASE_DIR, "test_meta_mms.mp3")
    if os.path.exists(p):
        return send_from_directory(BASE_DIR, "test_meta_mms.mp3")
    return "Not generated", 404


@app.route("/api/test_google_audio")
def get_test_google_audio():
    p = os.path.join(OUTPUT_DIR, "test_google_speech.mp3")
    if os.path.exists(p):
        return send_from_directory(OUTPUT_DIR, "test_google_speech.mp3")
    return "Not generated", 404


@app.route("/")
def index():
    return render_template_string(
        HTML_TEMPLATE,
        topics=EXPANDED_CURIO_TOPICS,
        voices=KIRI_VOICE_ACTORS
    )


@app.route("/api/project/<topic_id>")
def get_project_script(topic_id):
    custom_path = os.path.join(CUSTOM_SCRIPTS_DIR, f"{topic_id}.json")
    if os.path.exists(custom_path):
        with open(custom_path, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))

    script = get_or_create_project_script(topic_id)
    return jsonify(script)


@app.route("/api/project/<topic_id>/prompts_file")
def download_prompts_file(topic_id):
    out_dir = os.path.join(OUTPUT_DIR, f"{topic_id}_longform")
    prompts_file = os.path.join(out_dir, "google_flow_prompts.txt")
    script = get_or_create_project_script(topic_id)
    os.makedirs(out_dir, exist_ok=True)
    export_google_flow_prompts(script, prompts_file)
    return send_from_directory(out_dir, "google_flow_prompts.txt", as_attachment=True)


@app.route("/api/create_topic", methods=["POST"])
def create_topic_action():
    data = request.json or {}
    title_km = data.get("title_km", "ប្រធានបទថ្មី")
    title_en = data.get("title_en", "Curious Question")
    dur = int(data.get("target_minutes", 8))

    topic_slug = sanitize_slug(title_en if title_en else title_km)
    script_data = create_ai_longform_script(
        title_km=title_km,
        title_en=title_en,
        target_minutes=dur
    )

    custom_path = os.path.join(CUSTOM_SCRIPTS_DIR, f"{topic_slug}.json")
    with open(custom_path, "w", encoding="utf-8") as f:
        json.dump(script_data, f, ensure_ascii=False, indent=2)

    return jsonify({"status": "ok", "topic_id": topic_slug, "title_km": title_km})


@app.route("/api/upload_voice_track", methods=["POST"])
def upload_voice_track():
    topic_id = request.form.get("topic_id", "oxygen_double")
    audio = request.files.get("audio")
    if not audio:
        return jsonify({"status": "error", "error": "No audio"}), 400

    out_dir = os.path.join(OUTPUT_DIR, f"{topic_id}_longform")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "kiri_voiceover.mp3")
    audio.save(target)
    return jsonify({"status": "ok", "path": target})


@app.route("/api/batch_upload_images", methods=["POST"])
def batch_upload():
    """
    Intelligent batch upload:
    - Obtains total_scenes for the active project
    - Checks explicit scene patterns (scene_1, 01, img_1, etc.) within 1..total_scenes
    - Ignores large random seeds/IDs (> total_scenes)
    - Fills unassigned scenes in natural order
    - Deletes old conflicting files & clips for updated scenes so re-render reflects changes
    """
    topic_id = request.form.get("topic_id", "oxygen_double")
    images = request.files.getlist("images")
    dest_dir = os.path.join(OUTPUT_DIR, f"{topic_id}_longform", "images")
    clips_dir = os.path.join(OUTPUT_DIR, f"{topic_id}_longform", "clips")
    os.makedirs(dest_dir, exist_ok=True)
    os.makedirs(clips_dir, exist_ok=True)

    # 1. Get total scenes for this topic
    custom_path = os.path.join(CUSTOM_SCRIPTS_DIR, f"{topic_id}.json")
    if os.path.exists(custom_path):
        with open(custom_path, "r", encoding="utf-8") as f:
            script_data = json.load(f)
    else:
        script_data = get_or_create_project_script(topic_id)
    total_scenes = len(script_data.get("scenes", [])) or 100

    def parse_file_scene_num(filename):
        stem = os.path.splitext(filename)[0].lower()
        # Explicit pattern: scene_1, blang 1, prompt_1, img 1
        m = re.search(r'(?:scene|blang|prompt|slide|frame|p|img|image)[_\s-]*0*(\d{1,3})\b', stem)
        if m:
            val = int(m.group(1))
            if 1 <= val <= total_scenes:
                return val

        # Leading number: 01.png, 01_xxx.jpg, 1.jpg
        m = re.search(r'^0*(\d{1,3})(?:[_\s.-]|$)', stem)
        if m:
            val = int(m.group(1))
            if 1 <= val <= total_scenes:
                return val

        # Trailing number: xxx_01.jpg, xxx (1).jpg
        m = re.search(r'(?:[_\s.-]|\()0*(\d{1,3})\)?$', stem)
        if m:
            val = int(m.group(1))
            if 1 <= val <= total_scenes:
                return val

        # Any single number in range
        nums = [int(x) for x in re.findall(r'\b\d{1,3}\b', stem)]
        valid = [n for n in nums if 1 <= n <= total_scenes]
        if len(valid) == 1:
            return valid[0]

        return None

    # Separate files with explicit scene numbers vs files that need assignment
    assigned = {}
    unassigned = []

    for f in images:
        s_num = parse_file_scene_num(f.filename)
        if s_num and s_num not in assigned:
            assigned[s_num] = f
        else:
            unassigned.append(f)

    # Human/natural sort for unassigned files
    def natural_keys(text):
        return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]

    unassigned.sort(key=lambda f: natural_keys(f.filename))

    # Find open scene slots
    all_slots = list(range(1, total_scenes + 1))
    empty_slots = [s for s in all_slots if s not in assigned]

    # Fill empty slots with unassigned files
    for f in unassigned:
        if empty_slots:
            slot = empty_slots.pop(0)
            assigned[slot] = f
        else:
            next_slot = max(assigned.keys()) + 1 if assigned else 1
            assigned[next_slot] = f

    # Save files to disk and clear conflicting old files
    saved_scenes = []
    for scene_num, f in sorted(assigned.items()):
        ext = os.path.splitext(f.filename)[1].lower() or ".png"

        # Remove ANY existing image files for this scene
        stems = [f"scene_{scene_num:02d}", f"scene_{scene_num}", f"{scene_num:02d}", str(scene_num)]
        for exist_file in os.listdir(dest_dir):
            e_stem, e_ext = os.path.splitext(exist_file)
            if e_ext.lower() in [".png", ".jpg", ".jpeg", ".webp", ".avif"] and e_stem in stems:
                try:
                    os.remove(os.path.join(dest_dir, exist_file))
                except Exception:
                    pass

        # Invalidate old rendered clip for this scene
        old_clip = os.path.join(clips_dir, f"clip_{scene_num:02d}.mp4")
        if os.path.exists(old_clip):
            try:
                os.remove(old_clip)
            except Exception:
                pass

        target_path = os.path.join(dest_dir, f"scene_{scene_num:02d}{ext}")
        f.save(target_path)
        saved_scenes.append(scene_num)

    return jsonify({"status": "ok", "saved_count": len(saved_scenes), "scenes": saved_scenes})


@app.route("/api/upload_scene_image", methods=["POST"])
def upload_scene_image():
    """Uploads an image for a specific single scene."""
    topic_id = request.form.get("topic_id", "oxygen_double")
    scene_num = int(request.form.get("scene", 1))
    f = request.files.get("image")
    if not f:
        return jsonify({"status": "error", "error": "No file"}), 400

    dest_dir = os.path.join(OUTPUT_DIR, f"{topic_id}_longform", "images")
    clips_dir = os.path.join(OUTPUT_DIR, f"{topic_id}_longform", "clips")
    os.makedirs(dest_dir, exist_ok=True)
    ext = os.path.splitext(f.filename)[1].lower() or ".png"

    # Remove any existing files for this scene
    stems = [f"scene_{scene_num:02d}", f"scene_{scene_num}", f"{scene_num:02d}", str(scene_num)]
    for exist_file in os.listdir(dest_dir):
        e_stem, e_ext = os.path.splitext(exist_file)
        if e_ext.lower() in [".png", ".jpg", ".jpeg", ".webp", ".avif"] and e_stem in stems:
            try:
                os.remove(os.path.join(dest_dir, exist_file))
            except Exception:
                pass

    # Invalidate old rendered clip for this scene
    old_clip = os.path.join(clips_dir, f"clip_{scene_num:02d}.mp4")
    if os.path.exists(old_clip):
        try:
            os.remove(old_clip)
        except Exception:
            pass

    target = os.path.join(dest_dir, f"scene_{scene_num:02d}{ext}")
    f.save(target)
    return jsonify({"status": "ok", "scene_num": scene_num})


@app.route("/api/project/<topic_id>/image/<int:scene_num>")
def get_scene_image(topic_id, scene_num):
    """
    Returns the exact image for a scene:
    - User uploaded images take top priority
    - Never falls back to a different topic's rain image!
    - If no image is uploaded yet, returns a clean dynamic SVG placeholder
    """
    folder = os.path.join(OUTPUT_DIR, f"{topic_id}_longform", "images")
    img_path = resolve_scene_image(folder, scene_num)
    if img_path and os.path.exists(img_path):
        resp = send_from_directory(folder, os.path.basename(img_path))
        resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return resp

    # Return clean dynamic SVG placeholder
    svg_data = render_placeholder_svg(scene_num, topic_id)
    return Response(svg_data, mimetype="image/svg+xml")


@app.route("/api/project/<topic_id>/scene_audio/<int:scene_num>")
def get_scene_audio(topic_id, scene_num):
    """
    Returns audio for a single scene with selectable voice engine.
    Defaults to Christopher (Kurzgesagt deep documentary voice).
    """
    engine = request.args.get("engine", "edge_tts_chris")
    out_dir = os.path.join(OUTPUT_DIR, f"{topic_id}_longform")
    audio_dir = os.path.join(out_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    aud_path = os.path.join(audio_dir, f"scene_{scene_num:02d}.mp3")
    meta_path = os.path.join(audio_dir, f"scene_{scene_num:02d}.meta.json")

    need_gen = True
    if os.path.exists(aud_path) and os.path.exists(meta_path) and os.path.getsize(aud_path) > 1000:
        try:
            with open(meta_path, "r", encoding="utf-8") as mf:
                meta = json.load(mf)
            if meta.get("engine") == engine:
                need_gen = False
        except Exception:
            need_gen = True

    if need_gen:
        custom_path = os.path.join(CUSTOM_SCRIPTS_DIR, f"{topic_id}.json")
        if os.path.exists(custom_path):
            with open(custom_path, "r", encoding="utf-8") as f:
                script_data = json.load(f)
        else:
            script_data = get_or_create_project_script(topic_id)

        target_scene = None
        for s in script_data.get("scenes", []):
            if s.get("scene_num") == scene_num:
                target_scene = s
                break

        if target_scene:
            if engine == "edge_tts_guy":
                sp_text = target_scene.get("english_speech") or target_scene.get("action", "Curiosity science scene")
                generate_edge_tts_speech(sp_text, aud_path, voice="guy")
            elif engine.startswith("edge_tts"):
                sp_text = target_scene.get("english_speech") or target_scene.get("action", "Curiosity science scene")
                generate_edge_tts_speech(sp_text, aud_path, voice="christopher")
            elif engine == "meta_mms_eng":
                sp_text = target_scene.get("english_speech") or target_scene.get("action", "Curiosity science scene")
                generate_meta_mms_english_speech(sp_text, aud_path)
            elif engine == "google_tts":
                sp_text = target_scene.get("khmer_speech", "")
                generate_google_khmer_speech(sp_text, aud_path)
            else:
                sp_text = target_scene.get("khmer_speech", "")
                generate_meta_mms_speech(sp_text, aud_path)
            try:
                with open(meta_path, "w", encoding="utf-8") as mf:
                    json.dump({"speech_text": sp_text, "engine": engine}, mf, ensure_ascii=False)
            except Exception:
                pass

    if os.path.exists(aud_path):
        resp = send_from_directory(audio_dir, f"scene_{scene_num:02d}.mp3")
        resp.headers["Cache-Control"] = "no-cache"
        return resp
    return "Audio not found", 404


@app.route("/api/project/<topic_id>/video")
def get_project_video(topic_id):
    """Returns the rendered final video. Does NOT fall back to other topics."""
    p = os.path.join(OUTPUT_DIR, f"{topic_id}_longform", "final_youtube_video.mp4")
    if os.path.exists(p):
        return send_from_directory(os.path.dirname(p), os.path.basename(p))
    return jsonify({"status": "not_ready", "error": "Video has not been rendered yet."}), 404


@app.route("/api/project/<topic_id>/subtitles")
def get_project_subtitles(topic_id):
    p = os.path.join(OUTPUT_DIR, f"{topic_id}_longform", "captions.srt")
    if os.path.exists(p):
        return send_from_directory(os.path.dirname(p), os.path.basename(p), as_attachment=True)
    return "Subtitles not found", 404


@app.route("/api/project/<topic_id>/thumbnail")
def get_project_thumbnail(topic_id):
    """Returns the YouTube thumbnail picture (16:9, 1280x720). Generates one if missing."""
    out_dir = os.path.join(OUTPUT_DIR, f"{topic_id}_longform")
    os.makedirs(out_dir, exist_ok=True)
    
    # Prioritize AI generated artwork thumbnail if available
    ai_thumb = os.path.join(out_dir, "youtube_thumbnail_ai.png")
    if os.path.exists(ai_thumb):
        resp = send_from_directory(out_dir, "youtube_thumbnail_ai.png")
        resp.headers["Cache-Control"] = "no-cache"
        return resp

    vec_thumb = os.path.join(out_dir, "youtube_thumbnail.png")
    if not os.path.exists(vec_thumb):
        from src.thumbnail_generator import generate_youtube_thumbnail, export_thumbnail_prompts
        script_data = get_or_create_project_script(topic_id)
        generate_youtube_thumbnail(
            topic_id=topic_id,
            output_path=vec_thumb,
            title_en=script_data.get("title_en"),
            title_km=script_data.get("title_km")
        )
        export_thumbnail_prompts(
            topic_id=topic_id,
            title_en=script_data.get("title_en", topic_id),
            output_txt_path=os.path.join(out_dir, "youtube_thumbnail_prompts.txt")
        )

    if os.path.exists(vec_thumb):
        resp = send_from_directory(out_dir, "youtube_thumbnail.png")
        resp.headers["Cache-Control"] = "no-cache"
        return resp
    return "Thumbnail not found", 404


@app.route("/api/project/<topic_id>/thumbnail_prompts")
def get_project_thumbnail_prompts(topic_id):
    out_dir = os.path.join(OUTPUT_DIR, f"{topic_id}_longform")
    txt_path = os.path.join(out_dir, "youtube_thumbnail_prompts.txt")
    if not os.path.exists(txt_path):
        from src.thumbnail_generator import export_thumbnail_prompts
        script_data = get_or_create_project_script(topic_id)
        export_thumbnail_prompts(
            topic_id=topic_id,
            title_en=script_data.get("title_en", topic_id),
            output_txt_path=txt_path
        )
    if os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            return jsonify({"status": "ok", "prompts": f.read()})
    return jsonify({"status": "error", "error": "Prompts not found"}), 404


def _run_render_worker(topic_id: str, max_scenes: Optional[int] = None, voice_engine: str = "edge_tts_chris"):
    """Background worker that executes the complete longform video pipeline with parallelism."""
    try:
        custom_path = os.path.join(CUSTOM_SCRIPTS_DIR, f"{topic_id}.json")
        if os.path.exists(custom_path):
            with open(custom_path, "r", encoding="utf-8") as f:
                script_data = json.load(f)
        else:
            script_data = get_or_create_project_script(topic_id)

        out_dir = os.path.join(OUTPUT_DIR, f"{topic_id}_longform")
        total_to_render = max_scenes if max_scenes else len(script_data.get("scenes", []))

        def on_progress(step_type, current, total):
            pct = int((current / total) * 100) if total else 0
            RENDER_STATUS[topic_id] = {
                "status": "rendering",
                "current": current,
                "total": total,
                "percent": pct,
                "step": f"កំពុង Render ប្លង់ {current}/{total} (Turbo Multi-Core)...",
                "error": None
            }

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        final_video = loop.run_until_complete(
            execute_longform_pipeline(
                script_data=script_data,
                output_dir=out_dir,
                max_scenes=max_scenes,
                voice_engine=voice_engine,
                progress_callback=on_progress
            )
        )
        loop.close()

        RENDER_STATUS[topic_id] = {
            "status": "complete",
            "current": total_to_render,
            "total": total_to_render,
            "percent": 100,
            "step": "✅ វីដេអូបាន Render រួចរាល់ ១០០%!",
            "video_path": final_video,
            "error": None
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        RENDER_STATUS[topic_id] = {
            "status": "error",
            "error": str(e),
            "step": f"កំហុស: {e}"
        }


@app.route("/api/render_project", methods=["POST"])
def render_project_action():
    data = request.json or {}
    topic_id = data.get("topic_id", "oxygen_double")
    max_scenes = data.get("max_scenes")
    voice_engine = data.get("voice_engine", "edge_tts_chris")
    if max_scenes:
        max_scenes = int(max_scenes)

    # Initialize render status
    RENDER_STATUS[topic_id] = {
        "status": "rendering",
        "current": 0,
        "total": 0,
        "percent": 0,
        "step": "កំពុងចាប់ផ្តើម Multi-Core Pipeline...",
        "error": None
    }

    # Start background rendering thread
    t = threading.Thread(target=_run_render_worker, args=(topic_id, max_scenes, voice_engine), daemon=True)
    t.start()

    return jsonify({"status": "started", "topic_id": topic_id})


@app.route("/api/render_status/<topic_id>")
def get_render_status(topic_id):
    status = RENDER_STATUS.get(topic_id, {
        "status": "idle",
        "current": 0,
        "total": 0,
        "percent": 0,
        "step": "",
        "error": None
    })
    return jsonify(status)


if __name__ == "__main__":
    print("=" * 65)
    print("🚀 Khmer Cartoon Studio 4.0 (Natural Voice & Fast Render)")
    print("👉 Studio URL: http://localhost:5000")
    print("=" * 65)
    app.run(host="0.0.0.0", port=5000, debug=False)
