"""
config.py
API key များနှင့် setting များ ထားရှိရာ file
.env file တစ်ခု ဖန်တီးပြီး အောက်ပါအတိုင်း ထည့်ပါ:

ASSEMBLYAI_API_KEY=your_assemblyai_key
GEMINI_API_KEY=your_gemini_key
TTS_VOICE=my-MM-NilarNeural
"""
import os
from dotenv import load_dotenv

load_dotenv()

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# edge-tts မြန်မာအသံများ:
# my-MM-NilarNeural  (အမျိုးသမီးအသံ)
# my-MM-ThihaNeural   (အမျိုးသားအသံ)
TTS_VOICE = os.getenv("TTS_VOICE", "my-MM-NilarNeural")
