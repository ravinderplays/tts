from gtts import gTTS
import os

text = "ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?"
tts = gTTS(text=text, lang="pa", tld="co.in")
tts.save("output.mp3")
os.system("mpg321 output.mp3")
print("✅ Done!")
