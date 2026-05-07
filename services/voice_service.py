# services/voice_service.py
import pyaudio
import json
from vosk import Model, KaldiRecognizer

class VoiceService:
    def __init__(self, model_path, mic_index):
        self.model = Model(model_path)
        self.mic_index = mic_index

    def detect_command(self, keyword="automatic"):
        rec = KaldiRecognizer(self.model, 16000)

        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            input_device_index=self.mic_index,
            frames_per_buffer=4000
        )

        stream.start_stream()

        while True:
            data = stream.read(4000, exception_on_overflow=False)

            if rec.AcceptWaveform(data):
                text = json.loads(rec.Result()).get("text", "")

                if keyword in text.lower():
                    return True