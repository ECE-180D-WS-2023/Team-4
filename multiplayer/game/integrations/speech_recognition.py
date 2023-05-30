import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self):
        self.running = False
        self.mic = sr.Microphone()
        self.recognizer = sr.Recognizer()
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
        self.recognizer.dynamic_energy_threshold = False
        self.mute()
        self._prediction = None

    @property
    def prediction(self):
        if self._prediction:
            p = self._prediction
            self._prediction = None
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
