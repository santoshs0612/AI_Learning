from dotenv import load_dotenv
import os,io
from openai import OpenAI
import speech_recognition as sr
import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
from gtts import gTTS  # Use gTTS since Google OpenAI shim doesn't support TTS
import pygame
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")



############################
##  use this section easy when having a open ai api ############
# client_sppech = AsyncOpenAI()
# async def tts(speach: str) -> None:
#     async with client_sppech.audio.speech.with_streaming_response.create(
#         model="gpt-4o-mini-tts",
#         voice="coral",
#         input=speach,
#         instructions="Speak in a cheerful and positive tone.",
#         response_format="pcm",
#     ) as response:
#         await LocalAudioPlayer().play(response)


##########################

#using basic text to speech 
def tts(text):
    """
    Converts text to speech using gTTS and plays it.
    Google's OpenAI endpoint does NOT support client.audio.speech.
    """
    print("AI is speaking...")
    tts_obj = gTTS(text=text, lang='en')
    
    # Use a byte stream to play audio without saving a file
    fp = io.BytesIO()
    tts_obj.write_to_fp(fp)
    fp.seek(0)
    
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)



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
        # asyncio.run(tts(response.choices[0].message.content))
        tts(response.choices[0].message.content)

main()