"""
app.py
=======================================
One Click Recap - Web App (Flask)
=======================================
Video upload လုပ်ရင် one_click_recap() ကို run ပြီး
Recap video ကို download ချနိုင်အောင် ပြန်ပေးမည့် web app
"""
import os
import uuid
import traceback

from flask import (
    Flask, request, render_template, send_from_directory,
    redirect, url_for, flash
)
from werkzeug.utils import secure_filename

from main import one_click_recap

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"
ALLOWED_EXTENSIONS = {"mp4", "mov", "mkv", "webm"}
MAX_CONTENT_LENGTH = 300 * 1024 * 1024  # 300MB upload limit

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("video")

    if not file or file.filename == "":
        flash("Video file ရွေးပါ")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("mp4 / mov / mkv / webm file မျိုးသာ upload လုပ်ပါ")
        return redirect(url_for("index"))

    # unique name to avoid clashes between users
    job_id = uuid.uuid4().hex[:8]
    safe_name = secure_filename(file.filename)
    saved_name = f"{job_id}_{safe_name}"
    saved_path = os.path.join(UPLOAD_DIR, saved_name)
    file.save(saved_path)

    tts_voice = request.form.get("tts_voice") or "my-MM-NilarNeural"
    keep_original_audio = request.form.get("keep_original_audio") == "on"

    try:
        final_path = one_click_recap(
            video_path=saved_path,
            output_dir=OUTPUT_DIR,
            logo_path=None,
            blur_regions=None,
            keep_original_audio=keep_original_audio,
            tts_voice=tts_voice,
        )
    except Exception as exc:
        traceback.print_exc()
        flash(f"အမှားတစ်ခု ဖြစ်သွားပါတယ်: {exc}")
        return redirect(url_for("index"))
    finally:
        # clean up the uploaded source file, keep only the recap output
        if os.path.exists(saved_path):
            os.remove(saved_path)

    output_filename = os.path.basename(final_path)
    return render_template("result.html", output_filename=output_filename)


@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


@app.route("/healthz")
def healthz():
    # Render health check endpoint
    return {"status": "ok"}, 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
