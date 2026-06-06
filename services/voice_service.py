# services/voice_service.py
import json
import time

import pyaudio
from vosk import Model, KaldiRecognizer


class VoiceService:
    def __init__(self, model_path):
        self.model = Model(model_path)
        self.mic_index = self.find_mic()

        print("Using mic index:", self.mic_index)

        if self.mic_index is None:
            print("WARNING: No microphone detected!")

    # =========================
    # AUTO MIC DETECTION
    # =========================
    def find_mic(self):
        p = pyaudio.PyAudio()

        try:
            best_index = None

            for i in range(p.get_device_count()):
                info = p.get_device_info_by_index(i)

                if int(info.get("maxInputChannels", 0)) <= 0:
                    continue

                name = info["name"].lower()

                print(f"{i}: {name}")

                # prioritize webcam / usb mic
                if "webcam" in name or "usb" in name or "microphone" in name:
                    return i

                if best_index is None:
                    best_index = i

            return best_index
        finally:
            p.terminate()

    # =========================
    # VOICE DETECTION
    # =========================
    def detect_command(self, keyword="open", timeout=10):
        rec = KaldiRecognizer(self.model, 16000)

        p = pyaudio.PyAudio()
        stream = None

        try:
            if self.mic_index is None:
                self.mic_index = self.find_mic()

            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                input_device_index=self.mic_index,
                frames_per_buffer=4000
            )

            stream.start_stream()

            print("Listening... say:", keyword)

            deadline = time.monotonic() + timeout

            while time.monotonic() < deadline:
                data = stream.read(4000, exception_on_overflow=False)

                if rec.AcceptWaveform(data):
                    text = json.loads(rec.Result()).get("text", "")
                    print("Heard:", text)

                    if keyword in text.lower():
                        print("Voice command detected!")
                        return True

            print("Voice command timeout")
            return False
        except OSError as exc:
            print("Failed to open microphone, rescanning:", exc)
            self.mic_index = self.find_mic()
            return False
        finally:
            if stream is not None:
                if stream.is_active():
                    stream.stop_stream()
                stream.close()
            p.terminate()
