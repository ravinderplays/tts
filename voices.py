# voices.py — only confirmed working Edge TTS voices

VOICES = {
    "pa": [
        # No pa-IN in Edge TTS — using gTTS fallback handled in app.py
        {"id": "pa|co.in|false", "name": "Punjabi Normal", "gender": "neutral"},
        {"id": "pa|co.in|true",  "name": "Punjabi Slow",   "gender": "neutral"},
    ],
    "en": [
        {"id": "en-IN-PrabhatNeural",          "name": "Prabhat Indian (Male)",    "gender": "male"},
        {"id": "en-IN-NeerjaNeural",           "name": "Neerja Indian (Female)",   "gender": "female"},
        {"id": "en-IN-NeerjaExpressiveNeural", "name": "Neerja Expressive (Female)","gender": "female"},
        {"id": "en-US-GuyNeural",              "name": "Guy US (Male)",            "gender": "male"},
        {"id": "en-US-JennyNeural",            "name": "Jenny US (Female)",        "gender": "female"},  # ✅ added
        {"id": "en-US-AriaNeural",             "name": "Aria US (Female)",         "gender": "female"},
        {"id": "en-GB-RyanNeural",             "name": "Ryan UK (Male)",           "gender": "male"},
        {"id": "en-GB-SoniaNeural",            "name": "Sonia UK (Female)",        "gender": "female"},
    ],
    "hi": [
        {"id": "hi-IN-MadhurNeural",   "name": "Madhur (Male)",     "gender": "male"},
        {"id": "hi-IN-SwaraNeural",    "name": "Swara (Female)",    "gender": "female"},
    ],
    "ur": [
        {"id": "pa|com|false",   "name": "Urdu Normal",     "gender": "neutral"},
        {"id": "pa|com|true",    "name": "Urdu Slow",       "gender": "neutral"},
    ],
    "gu": [
        {"id": "gu|co.in|false", "name": "Gujarati Normal", "gender": "neutral"},
        {"id": "gu|co.in|true",  "name": "Gujarati Slow",   "gender": "neutral"},
    ],
    "ta": [
        {"id": "ta|co.in|false", "name": "Tamil Normal",    "gender": "neutral"},
        {"id": "ta|co.in|true",  "name": "Tamil Slow",      "gender": "neutral"},
    ],
}