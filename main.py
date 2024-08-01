import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi ="97718672de2f4c3989d28d742e510d1e"

def  speak(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    client = OpenAI(api_key="sk-proj-RwUn3hpfiReZgTvz6L6MT3BlbkFJD8OIM2xMTrQYMNY2b2IH",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content
 
def processcommand(c):
    if "opengoogle " in c.lower():
     webbrowser.open("https://google.com")
    elif "open facebook "in c.lower():
     webbrowser.open("https://facebook.com")
    elif "open youtube "in c.lower():
     webbrowser.open("https://youtube.com")
    elif "open linkedin "in c.lower():
     webbrowser.open("https://linkedin.com")
    elif c.lower( ).startswith("play"):
       song = c.lower().split("")[1]
       link =musiclibrary.music[song]
       webbrowser.open(link)
    elif "news" in c.lower():
       r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
       if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 


if __name__=="__main__":
    speak("initializing jarvis...")
    while True:
        r=sr.Recognizer()
        print("recognizing")
       
        
        
        try:
            with sr.Microphone() as source:
              print("listening ...")
              audio=r.listen(source,timeout=2,phrase_time_limit=1)
              command = r.recognize_google(audio)
              if(command.lower() =="jarvis"):
                  speak("ya")
                
                  with sr.Microphone() as source:
                     print("jarvis active")
                     audio=r.listen(source)
                     command=r.recognize_google(audio)
                    
                     processcommand(command)
    
        except Exception as e:
            print(" error :{0}".format(e))

            # start from processcommand