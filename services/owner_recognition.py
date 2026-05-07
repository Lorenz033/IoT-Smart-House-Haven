# services/vision_service.py
import cv2
import face_recognition
import pickle

class VisionService:
    def __init__(self, model_path):
        with open(model_path, "rb") as f:
            data = pickle.load(f)
        self.known_encoding = data["encodings"][0]

    def detect_owner(self, threshold=0.48, required_matches=5):
        cap = cv2.VideoCapture(0)
        matches = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = face_recognition.face_locations(rgb)
            encs = face_recognition.face_encodings(rgb, faces)

            for enc in encs:
                dist = face_recognition.face_distance([self.known_encoding], enc)[0]

                if dist < threshold:
                    matches += 1
                else:
                    matches = max(0, matches - 1)

            if matches >= required_matches:
                break

        cap.release()
        cv2.destroyAllWindows()
        return True