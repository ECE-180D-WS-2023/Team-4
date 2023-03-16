import time

import speech_recognition as sr

def speech_rec():
    def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            word = ["switch", "sweet", "which"]
            for i in word:
                if i in recognizer.recognize_google(audio):
                    print(1)
                    return 1
            return 0
        except sr.UnknownValueError:
            return 0
        except sr.RequestError as e:
            return 0
# this is called from the background threa
    
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
    
    # start listening in the background (note that we don't have to do this inside a `with` statement)
    return r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# calling this function requests that the background listener stop listening
stop_listening = speech_rec()
for i in range(1,10):
    time.sleep(1)
    print(i)
stop_listening(wait_for_stop=False)
