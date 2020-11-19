![](https://github.com/SamyySwift/Swift-A.I-virtual-assistant-/blob/main/image/assitant.png)
# Swift-A.I-virtual-assistant
Swift is an AI assistant I built using Machine Learning, SpeechRecognition, GoogleTexttoSpeech and python programming language. Swift basicallytries to mimic High level Assistants like Siri, Google assistant, Alexa, e.t.c.but not as sophiticated as them.
I trained Swift with custom intents such as greetings, about, name, a few to mention. When swift is woken up by its wake word, it listens to the users voice input command using the speech recognition API and then converts it to text,  the text is then passed to the machine learning model, and  the model makes a predcition in form of text which is then converted back to audio using Google text to speech API: this audio is then passed to the user as the responds.Swift is smart enough to give responds to questions it is not familiar with. 
Swift can do perform the following tasks curently:

* #### play Music
* #### Search google for anything
* #### Search wikipedia for anything
* #### Tell time and date
* #### Give weather condition of any city
* #### Anwser basic questions asked by the user
* #### Greet the user based on the current time of the day

# Dependencies
The following libraries was used to build swift
* speech_recognition API (used for speech recognition)
* pyaudio (responsible for audio output)
* webbrowser (for controlling the browser)
* pyttsx3 (used for text to speech)
* googleapi (used for searching google)
* vlc (used for controlling media playlist)
* wikipedia (used for searching wikipedia)
* Tensorflow (used for training model)

# Discusion
This is just a basic version of swift. It can be made more sophisticated by adding more features, and by using a more advanced deep leaning neural network wich can make the bot be a self learning AI. Am still working on the this.
Anyways, feel free to contribute to the project.
