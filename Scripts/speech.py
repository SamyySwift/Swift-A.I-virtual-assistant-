import speech_recognition as sr
import pyaudio
import webbrowser
import time
from datetime import datetime
import os
import pyttsx3
from googleapi import google
import vlc
from random import randint
from intents import chat
import datetime
import wikipedia
import requests


# Instantiate Modules
engine = pyttsx3.init()
r = sr.Recognizer()


def record_voice(ask = None):
    with sr.Microphone() as mic:
        if ask:
            swift_speak(ask)
        r.adjust_for_ambient_noise(mic)
        audio = r.listen(mic)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
            print(f'You: {voice_data}')
        except sr.UnknownValueError:
            swift_speak('Sorry, i did not quite get that. try saying something again')
        except sr.RequestError:
            swift_speak('Sorry, my speech service is down. Check your internet connection and try again')
        return voice_data

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        swift_speak("Hello,Good Morning")
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        swift_speak("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        swift_speak("Hello,Good Evening")
        print("Hello,Good Evening")



def swift_speak(audio_string):
    print(f'Swift: {audio_string}')
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 150)
    engine.setProperty('voice', voices[1].id)
    engine.say(audio_string)
    engine.runAndWait()

# Google search
def google_search(searchterm):
    num_pages = 1
    search_results = google.search(searchterm, num_pages)
    return search_results[0].description

# Music class
class songoperation():
    def playsong(self):
        ls = os.listdir('C:/Users/samue/Downloads/music')
        a = vlc.MediaList([vlc.Media('C:/Users/samue/Downloads/music/' + ls[randint(0, len(ls)-1)])])
        self.p = vlc.MediaListPlayer()
        self.p.set_media_list(a)
        self.p.play()
    def stopsong(self):
        if self.p.is_playing():
            self.p.stop()

    def nextsong(self):
        if self.p.is_playing():
            self.p.next()

    def previoussong(self):
        if self.p.is_playing():
            self.p.previous()

# instantiate class object
s = songoperation()

# Serach wikipedia
def wikipedia_search(statement):
    statement = statement.replace("Wikipedia", "")
    results = wikipedia.summary(statement, sentences=3)
    return results

# Tell time
def tell_time():
    hour = datetime.datetime.now().hour
    strTime = datetime.datetime.now().strftime("%H:%M")
    if 0 <= hour < 12:
        swift_speak('Good morning')
        swift_speak(f'The time is {strTime} AM')

    elif 12 >= hour < 18:
        swift_speak('Good afternoon')
        swift_speak(f'The time is {strTime} PM')

    else:
        swift_speak('Good evening')
        swift_speak(f'The time is {strTime} PM')



# Execute the function
while True:
    voice_data = record_voice()
    # time.sleep(1)
    swift_respond = chat(voice_data)
    #serach google
    if 'search' in voice_data:
        swift_speak(swift_respond)
        search_term = record_voice().split('for')
        answer = google_search(search_term[-1])
        swift_speak(answer)
    # Ask for time
    elif 'time' in voice_data:
        tell_time()
    # Play music
    elif 'play music' in voice_data:
        s.playsong()
        time.sleep(10)
    # stop music
    elif 'stop music' in voice_data:
        s.stopsong()
    # next music
    elif 'next music' in voice_data:
        s.nextsong()
    # ask questions
    elif 'ask' in voice_data:
        swift_speak('Sure, I guess i can try my best')
        term = record_voice()
        swift_speak(wikipedia_search(term))

    elif "weather" in voice_data:
        api_key = "0670ba0367d3fd6a13312d495fa514e9"
        swift_speak("What's the city name ")
        city_name = record_voice()
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID={api_key}&units=metric")
        x = response.json()
        try:
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                swift_speak(f'The current weather condition in {city_name} is {current_temperature} degrees. {weather_description}')
            else:
                swift_speak("City Not Found")
        except KeyError:
            swift_speak("I didn't get the city name")

    else:
        swift_speak(swift_respond)