import cv2
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, base_model='yolov8s.pt', custom_model='models/hammer.pt'):
        # 1. Genel model (Bıçak, Makas, Kişi için)
        self.base_model = YOLO(base_model)
        
        # 2. Senin eğittiğin özel model (Çekiç için)
        self.custom_model = YOLO(custom_model)
        
        # COCO Dataset ID'leri: 0: person, 43: knife, 76: scissors
        self.base_targets = [0, 43, 76]
        
        # Özel modelde çekiç muhtemelen 0. indextedir
        self.custom_targets = [0] 

    def detect(self, frame):
        all_detections = []

        # --- GENEL MODEL TAHMİNİ ---
        base_results = self.base_model.predict(source=frame, conf=0.4, verbose=False)
        for r in base_results:
            for box in r.boxes:
                class_id = int(box.cls[0])
                if class_id in self.base_targets:
                    all_detections.append({
                        "box": box.xyxy[0].tolist(),
                        "confidence": float(box.conf[0]),
                        "label": self.base_model.names[class_id]
                    })

        # --- ÖZEL ÇEKİÇ MODELİ TAHMİNİ ---
        custom_results = self.custom_model.predict(source=frame, conf=0.5, verbose=False)
        for r in custom_results:
            for box in r.boxes:
                # Custom modelde sadece çekiç olduğu için class_id kontrolüne gerek olmayabilir
                # Ama yine de isimlendirmeyi 'hammer' olarak sabitleyelim
                all_detections.append({
                    "box": box.xyxy[0].tolist(),
                    "confidence": float(box.conf[0]),
                    "label": "hammer" # Özel modelden geleni çekiç olarak etiketle
                })

        return all_detections