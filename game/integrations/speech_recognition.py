import speech_recognition as sr

def speech_rec(ans):
    def callback(recognizer, audio):
        print(ans)
    # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            word = ["switch", "sweet", "which"]
            recognized_str = recognizer.recognize_google(audio)
            for i in word:
                if i in recognized_str:
                    ans[0] = "switch"
            #answer = "none"
        except sr.UnknownValueError:
            return 0
            #answer = "none"
        except sr.RequestError as e:
            #answer = "none"
            return 0
        print("After callback: ", ans)
# this is called from the background threa
    
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
    r.energy_threshold = 999999
    r.dynamic_energy_threshold = False

    # start listening in the background (note that we don't have to do this inside a `with` statement)
    return r, r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# calling this function requests that the background listener stop listening
# stop_listening = speech_rec()
# for i in range(1,10):
#     time.sleep(1)
#     print(i)
# stop_listening(wait_for_stop=False)

class SpeechRecognizer:
    def __init__(self):
        self.running = False
        self.mic = sr.Microphone()
        self.recognizer = sr.Recognizer()
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
        self.recognizer.dynamic_energy_threshold = False
        self.mute()
        self._prediction = ""

    @property
    def prediction(self):
        if self._prediction != "":
            p = self._prediction
            self._prediction = ""
            return p
        return self._prediction

    @prediction.setter
    def prediction(self, prediction):
        self._prediction = prediction

    def _predict(self, recognizer, audio):
        try:
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            word_cloud_for_switch = ["switch", "sweet", "which"]
            recognized_str = recognizer.recognize_google(audio)
            for word in word_cloud_for_switch:
                if word in recognized_str:
                    self.prediction = "switch"
        except sr.UnknownValueError:
            return 0
        except sr.RequestError as e:
            return 0

    def start(self):
        if not self.running:
            self.stop_listening = self.recognizer.listen_in_background(self.mic, self._predict)
            self.running = True

    def stop(self):
        if self.running:
            self.stop_listening()
            self.running = False

    def mute(self):
        self.recognizer.energy_threshold = 999999

    def unmute(self):
        self.recognizer.energy_threshold = 300
