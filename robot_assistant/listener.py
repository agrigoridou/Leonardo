import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():
    try:
        with sr.Microphone() as source:
            print("Ακούω...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)

        text = recognizer.recognize_google(audio, language="el-GR")
        print("Είπες:", text)
        return text.lower()

    except:
        return ""
