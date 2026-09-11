"""
main.py
=======================================
One Click Recap App
=======================================
Video 1 ခုတည်းထည့်လိုက်ရင်:
  1) AssemblyAI နဲ့ စာသားထုတ်
  2) Gemini နဲ့ မြန်မာဘာသာပြန်
  3) edge-tts နဲ့ အသံဖိုင်ထုတ်
  4) Video + Voice ပေါင်းစပ်
  5) Text blur + Logo ထည့်
-> Recap Video အပြီးသတ်ထွက်လာမယ်
"""
import os
from transcribe import extract_text
from translate import translate_to_myanmar
from tts import generate_audio
from video_merge import merge_video_audio
from overlay import apply_blur_and_logo


def one_click_recap(
    video_path: str,
    output_dir: str = "output",
    logo_path: str = None,
    blur_regions: list = None,
    keep_original_audio: bool = False,
    tts_voice: str = None,
):
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(video_path))[0]

    audio_path = os.path.join(output_dir, f"{base_name}_voice.mp3")
    merged_path = os.path.join(output_dir, f"{base_name}_merged.mp4")
    final_path = os.path.join(output_dir, f"{base_name}_recap_final.mp4")

    print("[1/5] Video ထဲက စာသားထုတ်နေသည်...")
    transcript = extract_text(video_path)
    print(f"  -> {len(transcript['text'])} စာလုံးရရှိပါသည်")

    print("[2/5] မြန်မာဘာသာပြန်နေသည်...")
    myanmar_text = translate_to_myanmar(transcript["text"])

    print("[3/5] Voice-over ထုတ်နေသည်...")
    generate_audio(myanmar_text, audio_path, voice=tts_voice)

    print("[4/5] Video နှင့် အသံပေါင်းစပ်နေသည်...")
    merge_video_audio(
        video_path, audio_path, merged_path,
        keep_original_audio=keep_original_audio,
    )

    print("[5/5] Text blur + Logo ထည့်နေသည်...")
    if blur_regions or logo_path:
        apply_blur_and_logo(
            merged_path,
            blur_regions or [],
            logo_path,
            final_path,
        )
    else:
        os.replace(merged_path, final_path)

    print(f"\n✅ ပြီးပါပြီ! Output: {final_path}")
    return final_path


if __name__ == "__main__":
    # ================= ဥပမာသုံးနည်း =================
    result = one_click_recap(
        video_path="input.mp4",          # မူရင်း video
        output_dir="output",
        logo_path="logo.png",            # logo ပုံ (optional, None ဆိုရင် logo မထည့်)
        blur_regions=[                     # blur ဖုံးလိုသော area (optional)
            {"x": 50, "y": 900, "w": 400, "h": 80, "start": 0, "end": 9999},
        ],
        keep_original_audio=False,        # မူရင်း video အသံ ထားချင်ရင် True
        tts_voice="my-MM-NilarNeural",
    )
