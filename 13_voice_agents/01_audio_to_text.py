import speech_recognition as sr


def main():
    r = sr.Recognizer() # speech to text

    with sr.Microphone() as source: # Mic access
        r.adjust_for_ambient_noise(source)
        r.pause_threshold =2    

        print("Speak Something...")
        audio = r.listen(source)
        print("Processing Audio... (STT)")
        stt = r.recognize_google(audio)
        print("You said: ", stt)


main()