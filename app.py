from flask import Flask, request, send_file, render_template_string
from gtts import gTTS
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Punjabi TTS</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
    textarea { width: 100%; height: 120px; font-size: 16px; padding: 10px; }
    button { padding: 12px 30px; font-size: 16px; background: #4CAF50; color: white; border: none; cursor: pointer; border-radius: 6px; margin-top: 10px; }
    audio { width: 100%; margin-top: 20px; }
    a { display: block; margin-top: 10px; font-size: 15px; }
  </style>
</head>
<body>
  <h2>🔊 Punjabi Text to Speech...</h2>
  <form method="POST" action="/tts">
    <textarea name="text" placeholder="ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?">{{ text }}</textarea>
    <br>
    <button type="submit">Generate & Download MP3</button>
  </form>
  {% if audio %}
    <audio controls src="/audio"></audio>
    <a href="/audio" download="punjabi_speech.mp3">⬇️ Download MP3</a>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML, text="", audio=False)

@app.route("/tts", methods=["POST"])
def tts():
    from flask import request
    text = request.form.get("text", "ਸਤ ਸ੍ਰੀ ਅਕਾਲ")
    tts = gTTS(text=text, lang="pa", tld="co.in")
    tts.save("output.mp3")
    return render_template_string(HTML, text=text, audio=True)

@app.route("/audio")
def audio():
    return send_file("output.mp3", mimetype="audio/mpeg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)