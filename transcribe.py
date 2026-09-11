"""
transcribe.py
Function 1: AssemblyAI API သုံးပြီး Video/Audio ထဲက စာသားထုတ်ခြင်း
"""
import assemblyai as aai
from config import ASSEMBLYAI_API_KEY

aai.settings.api_key = ASSEMBLYAI_API_KEY


def extract_text(video_path: str) -> dict:
    """
    video/audio file ကို AssemblyAI ကို ပို့ပြီး စာသားထုတ်ပေးမယ်

    Returns:
        {
            "text": "full transcript text",
            "sentences": [{"text": str, "start": ms, "end": ms}, ...]
        }
    """
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(video_path)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription ပျက်သွားပါတယ်: {transcript.error}")

    sentences = []
    for s in transcript.get_sentences() or []:
        sentences.append({
            "text": s.text,
            "start": s.start,  # milliseconds
            "end": s.end,
        })

    return {
        "text": transcript.text,
        "sentences": sentences,
    }
