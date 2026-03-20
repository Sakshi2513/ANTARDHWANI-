import speech_recognition as sr


class VoiceService:

    def listen(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            return text
        except:
            return "Could not understand audio"