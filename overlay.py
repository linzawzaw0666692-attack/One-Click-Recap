"""
overlay.py
Function 5: မူရင်း Video ထဲက စာသား/Logo ကို Blur ဖုံးခြင်း
             + Logo/Watermark အသစ် ထည့်ခြင်း
"""
import cv2
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip


def _blur_region(get_frame, t, x, y, w, h, ksize=51):
    frame = get_frame(t).copy()
    roi = frame[y:y + h, x:x + w]
    if roi.size > 0:
        blurred = cv2.GaussianBlur(roi, (ksize, ksize), 0)
        frame[y:y + h, x:x + w] = blurred
    return frame


def _apply_blur_regions(video, blur_regions):
    """video ပေါ်ရှိ region များကို blur တင်ပြီး clip list ပြန်ပေးမယ်"""
    clips = [video]
    for region in blur_regions:
        x, y, w, h = region["x"], region["y"], region["w"], region["h"]
        start = region.get("start", 0)
        end = region.get("end", video.duration)

        blurred_clip = (
            video.subclip(start, end)
            .fl(lambda gf, t, x=x, y=y, w=w, h=h: _blur_region(gf, t, x, y, w, h))
            .set_start(start)
        )
        clips.append(blurred_clip)
    return clips


def add_logo(video, logo_path: str, position="bottom_right", opacity=0.8, size_ratio=0.12):
    """
    video (VideoFileClip သို့ path string) ပေါ်တွင် Logo ပုံ watermark ထည့်မယ်
    position : "bottom_right" | "bottom_left" | "top_right" | "top_left"
    """
    if isinstance(video, str):
        video = VideoFileClip(video)

    logo_w = int(video.w * size_ratio)
    logo = (
        ImageClip(logo_path)
        .set_duration(video.duration)
        .resize(width=logo_w)
        .set_opacity(opacity)
    )

    margin = 20
    positions = {
        "bottom_right": (video.w - logo.w - margin, video.h - logo.h - margin),
        "bottom_left": (margin, video.h - logo.h - margin),
        "top_right": (video.w - logo.w - margin, margin),
        "top_left": (margin, margin),
    }
    logo = logo.set_position(positions.get(position, positions["bottom_right"]))
    return CompositeVideoClip([video, logo])


def apply_blur_and_logo(
    video_path: str,
    blur_regions: list,
    logo_path: str,
    output_path: str,
    logo_position: str = "bottom_right",
) -> str:
    """
    Text blur + Logo နှစ်ခုလုံးကို တစ်ပြိုင်နက်ထည့်ပြီး final video ထုတ်မယ်
    blur_regions : [{"x":.., "y":.., "w":.., "h":.., "start":sec, "end":sec}, ...]
    logo_path    : logo image (png, background transparent ဖြစ်ရင် ပိုကောင်း)
    """
    video = VideoFileClip(video_path)

    clips = _apply_blur_regions(video, blur_regions) if blur_regions else [video]
    composed = CompositeVideoClip(clips) if len(clips) > 1 else video

    final = add_logo(composed, logo_path, position=logo_position) if logo_path else composed

    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        logger=None,
    )
    return output_path
