import os
import json
import asyncio
from flask import Flask, request, send_file, render_template
import edge_tts
from gtts import gTTS
from voices import VOICES

app = Flask(__name__)


def is_edge_voice(voice_id: str) -> bool:
    """Edge TTS voices contain 'Neural', gTTS voices use 'lang|tld|slow' format"""
    return "Neural" in voice_id


def generate_gtts(text: str, voice_id: str):
    """voice_id format: lang|tld|slow"""
    parts = voice_id.split("|")
    lang  = parts[0]
    tld   = parts[1] if len(parts) > 1 else "com"
    slow  = parts[2] == "true" if len(parts) > 2 else False
    tts   = gTTS(text=text, lang=lang, tld=tld, slow=slow)
    tts.save("output.mp3")


async def generate_edge(text: str, voice_id: str):
    """Use Microsoft Edge TTS Neural voice"""
    communicate = edge_tts.Communicate(text, voice_id)
    await communicate.save("output.mp3")


def generate_audio(text: str, voice_id: str):
    if is_edge_voice(voice_id):
        asyncio.run(generate_edge(text, voice_id))
    else:
        generate_gtts(text, voice_id)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html",
        text        = "",
        audio       = False,
        error       = None,
        lang        = "pa",
        voice       = "pa|co.in|false",
        voice_name  = "",
        lang_name   = "",
        voices_json = json.dumps(VOICES)
    )


@app.route("/tts", methods=["POST"])
def tts():
    text  = request.form.get("text",  "").strip()
    lang  = request.form.get("lang",  "pa")
    voice = request.form.get("voice", "pa|co.in|false")

    context = dict(
        text        = text,
        lang        = lang,
        voice       = voice,
        voices_json = json.dumps(VOICES)
    )

    if not text:
        return render_template("index.html", audio=False,
            error="Please enter some text.",
            voice_name="", lang_name="", **context)
    try:
        generate_audio(text, voice)
        voice_name = next(
            (v["name"] for v in VOICES.get(lang, []) if v["id"] == voice), voice
        )
        return render_template("index.html", audio=True, error=None,
            voice_name=voice_name, lang_name=lang.upper(), **context)
    except Exception as e:
        return render_template("index.html", audio=False,
            error=str(e), voice_name="", lang_name="", **context)


@app.route("/audio")
def audio():
    return send_file("output.mp3", mimetype="audio/mpeg")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)