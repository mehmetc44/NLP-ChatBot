from gtts import gTTS
import os,random
from playaudio import playaudio



def speak(text):
    text.lower()
    tts = gTTS(text=text, lang='tr', slow=False)
    file = "../../data/audio/audio" + str(random.randint(1, 1233442232)) + ".mp3"
    tts.save(file)
    playaudio(file)
    os.remove(file)

speak("Selamlar ben chatbot")