import numpy as np

class ThreatAnalyzer:
    def __init__(self, proximity_threshold=80):
        # Mesafe eşiği: 80 pikselden yakınsa tehdit kabul edilir
        self.proximity_threshold = proximity_threshold

    def calculate_threat(self, hands, objects):
        """
        Main.py tarafından çağrılan ana analiz fonksiyonu.
        """
        threat_detected = False
        threat_info = []

        for hand in hands:
            landmarks = hand["landmarks"]
            # İşaret parmağı ucu (MediaPipe Landmark ID: 8)
            finger_tip = landmarks[8] 

            for obj in objects:
                # Sadece tehlikeli nesneleri kontrol et
                if obj["label"] in ["knife", "scissors", "hammer"]:
                    o_box = obj["box"]
                    
                    # 1. Objenin merkez noktasını hesapla
                    obj_center = (
                        int((o_box[0] + o_box[2]) / 2),
                        int((o_box[1] + o_box[3]) / 2)
                    )

                    # 2. İşaret parmağı ile obje merkezi arasındaki mesafeyi ölç (Öklid)
                    distance = np.sqrt((finger_tip[0] - obj_center[0])**2 + 
                                       (finger_tip[1] - obj_center[1])**2)

                    # 3. Eğer mesafe eşik değerinden küçükse TEHDİT
                    if distance < self.proximity_threshold:
                        threat_detected = True
                        threat_info.append({
                            "object": obj["label"],
                            "confidence": obj.get("confidence", 0),
                            "box": o_box,
                            "distance": int(distance)
                        })

        return threat_detected, threat_info