"""
video_merge.py
Function 4: မူရင်း Video နှင့် Voice-over အသံဖိုင်အသစ်ကို ပေါင်းစပ်ပြီး
             Recap Video ထုတ်ခြင်း
"""
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, afx


def merge_video_audio(
    video_path: str,
    new_audio_path: str,
    output_path: str,
    keep_original_audio: bool = False,
    original_audio_volume: float = 0.15,
) -> str:
    """
    video_path            : မူရင်း video
    new_audio_path        : generate လုပ်ထားသော မြန်မာ voice-over mp3
    keep_original_audio   : မူရင်း video ၏ အသံကို အနည်းငယ်ရောထည့်ချင်လျှင် True
    original_audio_volume : မူရင်းအသံကို ဘယ်လောက် အသံနှစ်ချင်လဲ (0.0 - 1.0)
    """
    video = VideoFileClip(video_path)
    new_audio = AudioFileClip(new_audio_path)

    # voice-over က video ထက်ရှည်နေရင် video length အထိသာ ဖြတ်မယ်
    if new_audio.duration > video.duration:
        new_audio = new_audio.subclip(0, video.duration)

    if keep_original_audio and video.audio is not None:
        original_audio = video.audio.fx(afx.volumex, original_audio_volume)
        final_audio = CompositeAudioClip([original_audio, new_audio])
    else:
        final_audio = new_audio

    final_video = video.set_audio(final_audio)
    final_video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        logger=None,
    )

    video.close()
    new_audio.close()
    return output_path
