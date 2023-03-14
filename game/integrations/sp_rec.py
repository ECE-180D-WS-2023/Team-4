
#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

import speech_recognition as sr
def speech_rec():
   # Record Audio
   r = sr.Recognizer()
   result = 0
   with sr.Microphone() as source:
      print("Say something!")
      audio = r.listen(source, 10, 3)
   # Speech recognition using Google Speech Recognition
   try:
      # for testing purposes, we're just using the default API key
      # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
      # instead of `r.recognize_google(audio)`
      result = format(r.recognize_google(audio))
   except sr.UnknownValueError:
      result = 0
   except sr.RequestError:
      result = 0
   if result == 'switch' or result =='search' or result =='which' or result =='sweet':
      return 'switch'
   else:
      return 0

print(speech_rec())