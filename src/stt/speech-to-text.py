import speech_recognition as sr
def toText():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Dinliyorum...")
        r.adjust_for_ambient_noise(source, duration=1)
        sound = r.listen(source, phrase_time_limit=8)
    try:
        text = r.recognize_google(sound, language="tr")
        print(f"You: {text}")
    except sr.UnknownValueError:
        print("I don't understand!")
    except sr.RequestError as e:
        print(f"Error: {e}")


def main():
    toText()


if __name__ == "__main__":
    main()



