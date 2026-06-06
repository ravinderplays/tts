from flask import Flask, request, send_file, render_template_string
from gtts import gTTS
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Text to Speech App</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #f4f6f8; color: #1a1a1a; }
    .header { background: #1D9E75; padding: 1.5rem 2rem; color: white; display: flex; align-items: center; gap: 14px; }
    .header i { font-size: 28px; }
    .header h1 { font-size: 22px; font-weight: 600; }
    .header p { font-size: 14px; opacity: 0.85; margin-top: 2px; }
    .container { max-width: 680px; margin: 2rem auto; padding: 0 1rem 3rem; }
    .card { background: white; border-radius: 12px; border: 1px solid #e2e8f0; padding: 1.5rem; margin-bottom: 1rem; }
    label { font-size: 13px; color: #555; display: block; margin-bottom: 6px; }
    textarea { width: 100%; font-size: 15px; padding: 12px; border-radius: 8px; border: 1px solid #ddd; resize: vertical; min-height: 130px; background: #fafafa; color: #1a1a1a; line-height: 1.7; }
    textarea:focus { outline: none; border-color: #1D9E75; }
    .char-count { font-size: 12px; color: #999; text-align: right; margin-top: 4px; }
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 14px; }
    select { width: 100%; font-size: 14px; padding: 9px 12px; border-radius: 8px; border: 1px solid #ddd; background: #fafafa; color: #1a1a1a; }
    select:focus { outline: none; border-color: #1D9E75; }
    .lang-tabs { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }
    .lang-tab { padding: 7px 16px; border-radius: 20px; font-size: 13px; cursor: pointer; border: 1px solid #ddd; background: white; color: #555; font-weight: 500; }
    .lang-tab.active { background: #1D9E75; color: white; border-color: #1D9E75; }
    .lang-tab:hover:not(.active) { background: #f0fdf4; border-color: #5DCAA5; color: #0F6E56; }
    .samples { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
    .sample-btn { font-size: 12px; padding: 5px 14px; cursor: pointer; border-radius: 20px; background: #E1F5EE; color: #0F6E56; border: 1px solid #5DCAA5; }
    .sample-btn:hover { background: #9FE1CB; }
    .generate-btn { width: 100%; padding: 14px; font-size: 15px; font-weight: 600; cursor: pointer; border-radius: 10px; background: #1D9E75; color: white; border: none; margin-bottom: 1rem; }
    .generate-btn:hover { background: #0F6E56; }
    .generate-btn:disabled { opacity: 0.6; cursor: not-allowed; }
    .audio-card { background: #E1F5EE; border: 1px solid #5DCAA5; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; }
    .audio-card .audio-title { font-size: 13px; color: #0F6E56; font-weight: 600; margin-bottom: 10px; }
    audio { width: 100%; margin-bottom: 12px; }
    .dl-btn { display: flex; align-items: center; justify-content: center; gap: 8px; padding: 11px; font-size: 14px; font-weight: 600; border: 1px solid #5DCAA5; border-radius: 8px; text-decoration: none; color: #0F6E56; background: white; }
    .dl-btn:hover { background: #E1F5EE; }
    .error { background: #fff5f5; border: 1px solid #fca5a5; border-radius: 8px; padding: 12px 14px; font-size: 14px; color: #dc2626; margin-bottom: 1rem; }
    .lang-badge { display: inline-block; font-size: 11px; padding: 3px 10px; border-radius: 12px; background: #E1F5EE; color: #0F6E56; border: 1px solid #5DCAA5; margin-left: 8px; vertical-align: middle; }
    .footer { text-align: center; font-size: 12px; color: #999; padding-top: 1rem; border-top: 1px solid #eee; margin-top: 1rem; }
    .ehide { display: none}
  </style>
</head>
<body>

<div class="header">
  <i class="fa-solid fa-volume-high"></i>
  <div>
    <h1>Text to Speech</h1>
    <p>Supports Punjabi, English, Hindi &amp; more</p>
  </div>
</div>

<div class="container">
  <div class="card">
    <label style="margin-bottom:10px;"><i class="fa-solid fa-language" style="margin-right:5px;"></i>Select language</label>
    <div class="lang-tabs" id="langTabs">
      <button class="lang-tab" onclick="setLang('pa', this)" data-lang="pa">ਪੰਜਾਬੀ Punjabi</button>
      <button class="lang-tab" onclick="setLang('en', this)" data-lang="en">English</button>
      <button class="lang-tab ehide" onclick="setLang('hi', this)" data-lang="hi">हिन्दी Hindi</button>
      <button class="lang-tab ehide" onclick="setLang('ur', this)" data-lang="ur">اردو Urdu</button>
      <button class="lang-tab ehide" onclick="setLang('gu', this)" data-lang="gu">ગુજરાતી</button>
      <button class="lang-tab ehide" onclick="setLang('ta', this)" data-lang="ta">தமிழ் Tamil</button>
    </div>

    <label>
      <i class="fa-solid fa-pen-to-square" style="margin-right:5px;"></i>Enter text
      <span class="lang-badge" id="langBadge">Punjabi (pa)</span>
    </label>
    <textarea id="inputText" oninput="updateCount()">{{ text }}</textarea>
    <div class="char-count"><span id="charCount">{{ text|length }}</span> characters</div>

    <div class="grid-2">
      <div>
        <label>Speed</label>
        <select id="speedSelect">
          <option value="false" {% if speed == 'false' %}selected{% endif %}>Normal speed</option>
          <option value="true"  {% if speed == 'true'  %}selected{% endif %}>Slow speed</option>
        </select>
      </div>
      <div>
        <label>Accent</label>
        <select id="accentSelect">
          <option value="co.in" {% if tld == 'co.in' %}selected{% endif %}>Indian accent</option>
          <option value="com"   {% if tld == 'com'   %}selected{% endif %}>Global accent</option>
          <option value="co.uk" {% if tld == 'co.uk' %}selected{% endif %}>British accent</option>
          <option value="com.au"{% if tld == 'com.au'%}selected{% endif %}>Australian accent</option>
        </select>
      </div>
    </div>

    <div style="margin-top:14px;">
      <label>Quick samples</label>
      <div class="samples" id="samplesBox"></div>
    </div>
  </div>

  <button class="generate-btn" onclick="submitForm()">
    <i class="fa-solid fa-play" style="margin-right:8px;"></i>Generate speech
  </button>

  {% if audio %}
  <div class="audio-card">
    <p class="audio-title"><i class="fa-solid fa-circle-check" style="margin-right:5px;"></i>Audio ready — preview below</p>
    <audio controls src="/audio" autoplay></audio>
    <a href="/audio" download="speech.mp3" class="dl-btn">
      <i class="fa-solid fa-download"></i> Download MP3
    </a>
  </div>
  {% endif %}

  {% if error %}
  <div class="error">
    <i class="fa-solid fa-circle-exclamation" style="margin-right:6px;"></i>{{ error }}
  </div>
  {% endif %}

  <div class="footer">
    Powered by gTTS &amp; Flask &nbsp;&middot;&nbsp; Multi-language TTS App
  </div>
</div>

<script>
const langData = {
  pa: { name: 'Punjabi (pa)',   placeholder: 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?',          accent: 'co.in', samples: ['ਸਤ ਸ੍ਰੀ ਅਕਾਲ', 'ਪੰਜਾਬ ਦੀ ਧਰਤੀ ਬਹੁਤ ਸੁੰਦਰ ਹੈ', 'ਤੁਹਾਡਾ ਨਾਮ ਕੀ ਹੈ?', 'ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖਾਲਸਾ'] },
  en: { name: 'English (en)',   placeholder: 'Hello! How are you today?',                accent: 'co.in', samples: ['Hello, how are you?', 'Good morning everyone', 'Welcome to our app', 'Have a nice day!'] },
  hi: { name: 'Hindi (hi)',     placeholder: 'नमस्ते, आप कैसे हैं?',                    accent: 'co.in', samples: ['नमस्ते', 'आप कैसे हैं?', 'भारत महान है', 'धन्यवाद'] },
  ur: { name: 'Urdu (ur)',      placeholder: 'آپ کیسے ہیں؟',                             accent: 'com',   samples: ['السلام علیکم', 'آپ کیسے ہیں؟', 'شکریہ', 'خوش آمدید'] },
  gu: { name: 'Gujarati (gu)',  placeholder: 'નમસ્તે, તમે કેમ છો?',                     accent: 'co.in', samples: ['નમસ્તે', 'તમે કેમ છો?', 'ગુજરાત', 'આભાર'] },
  ta: { name: 'Tamil (ta)',     placeholder: 'வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?', accent: 'co.in', samples: ['வணக்கம்', 'நன்றி', 'தமிழ்நாடு', 'எப்படி இருக்கிறீர்கள்?'] }
};

let currentLang = '{{ lang }}' || 'pa';

function setLang(lang, el) {
  currentLang = lang;
  document.querySelectorAll('.lang-tab').forEach(t => t.classList.remove('active'));
  if (el) el.classList.add('active');
  const data = langData[lang];
  document.getElementById('langBadge').textContent = data.name;
  document.getElementById('inputText').placeholder = data.placeholder;
  document.getElementById('accentSelect').value = data.accent;
  renderSamples(lang);
}

function renderSamples(lang) {
  const box = document.getElementById('samplesBox');
  box.innerHTML = langData[lang].samples
    .map(s => `<button class="sample-btn" onclick="setSample('${s}')">${s}</button>`)
    .join('');
}

function updateCount() {
  document.getElementById('charCount').textContent = document.getElementById('inputText').value.length;
}

function setSample(text) {
  document.getElementById('inputText').value = text;
  updateCount();
}

function submitForm() {
  const text = document.getElementById('inputText').value.trim();
  if (!text) { alert('Please enter some text first.'); return; }
  const speed = document.getElementById('speedSelect').value;
  const tld   = document.getElementById('accentSelect').value;
  const form  = document.createElement('form');
  form.method = 'POST';
  form.action = '/tts';
  [['text', text], ['lang', currentLang], ['speed', speed], ['tld', tld]].forEach(([k, v]) => {
    const i = document.createElement('input');
    i.type = 'hidden'; i.name = k; i.value = v;
    form.appendChild(i);
  });
  document.body.appendChild(form);
  form.submit();
}

// ✅ On page load — restore last selected language
(function init() {
  const savedLang = currentLang || 'pa';
  const tabEl = document.querySelector(`.lang-tab[data-lang="${savedLang}"]`);
  setLang(savedLang, tabEl);
  updateCount();
})();
</script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML, text="", audio=False, error=None, lang="pa", speed="false", tld="co.in")

@app.route("/tts", methods=["POST"])
def tts():
    text  = request.form.get("text", "").strip()
    lang  = request.form.get("lang", "pa")
    slow  = request.form.get("speed", "false") == "true"
    speed = request.form.get("speed", "false")
    tld   = request.form.get("tld", "co.in")
    if not text:
        return render_template_string(HTML, text="", audio=False, error="Please enter some text.", lang=lang, speed=speed, tld=tld)
    try:
        tts_obj = gTTS(text=text, lang=lang, slow=slow, tld=tld)
        tts_obj.save("output.mp3")
        return render_template_string(HTML, text=text, audio=True, error=None, lang=lang, speed=speed, tld=tld)
    except Exception as e:
        return render_template_string(HTML, text=text, audio=False, error=str(e), lang=lang, speed=speed, tld=tld)

@app.route("/audio")
def audio():
    return send_file("output.mp3", mimetype="audio/mpeg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)