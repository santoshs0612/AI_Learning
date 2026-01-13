from dotenv import load_dotenv
import os 
from openai import OpenAI
import speech_recognition as sr

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")





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

        # / adding a gemini model
        client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        SYSTEM_PROMPT = """
            You are an expert voice agent. You are given the transcript of what user has said using voice.
            You need to output as if you are an voice agent and whtever you speak will be converted back to audio using AI playes back to user.
        """

        response = client.chat.completions.create(
                    model="gemini-2.5-flash",
                    messages=[

                        {   "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        {
                            "role": "user",
                            "content": stt
                        }
                    ]
                )

        print("AI Response: ", response.choices[0].message.content)

main()