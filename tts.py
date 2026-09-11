"""
tts.py
Function 3: edge-tts API သုံးပြီး မြန်မာအသံဖိုင်ထုတ်ခြင်း
"""
import asyncio
import edge_tts
from config import TTS_VOICE


async def _generate(text: str, output_path: str, voice: str, rate: str, volume: str):
    communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume)
    await communicate.save(output_path)


def generate_audio(
    text: str,
    output_path: str,
    voice: str = None,
    rate: str = "+0%",
    volume: str = "+0%",
) -> str:
    """
    မြန်မာစာသားကို အသံဖိုင် (mp3) အဖြစ်ပြောင်းပေးမယ်

    voice : "my-MM-NilarNeural" (အမျိုးသမီး) / "my-MM-ThihaNeural" (အမျိုးသား)
    rate  : ဥပမာ "+10%" = ပိုမြန်, "-10%" = ပိုနှေး
    """
    voice = voice or TTS_VOICE
    asyncio.run(_generate(text, output_path, voice, rate, volume))
    return output_path


async def list_myanmar_voices():
    """ရရှိနိုင်သော မြန်မာအသံစာရင်းကို ကြည့်ရန်"""
    voices = await edge_tts.list_voices()
    return [v for v in voices if v["Locale"] == "my-MM"]
