# services/voice_service.py
import pyaudio
import json
from vosk import Model, KaldiRecognizer

class VoiceService:
    def __init__(self, model_path):
        self.model = Model(model_path)
        self.mic_index = self.find_mic()

        print("🎤 Using mic index:", self.mic_index)

        if self.mic_index is None:
            print("⚠️ WARNING: No microphone detected!")

    # =========================
    # AUTO MIC DETECTION
    # =========================
    def find_mic(self):
        p = pyaudio.PyAudio()

        best_index = None

        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            name = info["name"].lower()

            print(f"{i}: {name}")

            # prioritize webcam / usb mic
            if "webcam" in name or "usb" in name or "microphone" in name:
                best_index = i
                break

        p.terminate()
        return best_index

    # =========================
    # VOICE DETECTION
    # =========================
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

        print("🎤 Listening... say:", keyword)

        while True:
            data = stream.read(4000, exception_on_overflow=False)

            if rec.AcceptWaveform(data):
                text = json.loads(rec.Result()).get("text", "")
                print("Heard:", text)

                if keyword in text.lower():
                    print("✅ Voice command detected!")
                    return True