import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, mode=False, max_hands=2, detection_con=0.5, track_con=0.5):
        # MediaPipe Hands ayarları
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=mode,
            max_num_hands=max_hands,
            min_detection_confidence=detection_con,
            min_tracking_confidence=track_con
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame):
        # MediaPipe RGB görüntü ile çalışır
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        all_hands = []
        h, w, c = frame.shape

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                hand_data = []
                for id, lm in enumerate(hand_lms.landmark):
                    # Oransal koordinatları (0-1) piksel koordinatlarına çeviriyoruz
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    hand_data.append((cx, cy))
                
                all_hands.append({
                    "landmarks": hand_data,
                    "bbox": self.get_hand_bbox(hand_data) # Elin etrafındaki hayali kutu
                })
        return all_hands

    def get_hand_bbox(self, landmarks):
        # El noktalarının en uç noktalarını bularak bir sınırlayıcı kutu oluşturur
        x_coords = [lm[0] for lm in landmarks]
        y_coords = [lm[1] for lm in landmarks]
        return [min(x_coords), min(y_coords), max(x_coords), max(y_coords)]

    def draw_hands(self, frame):
        # Elleri ve eklemleri ekrana çizer
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return frame