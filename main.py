import cv2
import time
import pyttsx3
import threading
from modules.object_detector import ObjectDetector
from modules.hand_tracker import HandTracker
from modules.threat_analyzer import ThreatAnalyzer
from utils.logger import log_threat, save_evidence, start_video_recording

# Ses motoru
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak_alarm(text):
    try:
        local_engine = pyttsx3.init()
        local_engine.setProperty('rate', 150)
        local_engine.say(text)
        local_engine.runAndWait()
    except:
        pass

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    detector = ObjectDetector()
    tracker = HandTracker()
    analyzer = ThreatAnalyzer()

    threat_in_progress = False
    p_time = 0

    # Video Kayıt Değişkenleri
    video_out = None
    recording_start_time = 0
    record_duration = 7  # saniye

    print("Sistem Aktif... Çıkmak için 'q' tuşuna basın.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # 1. TESPİTLER
        hands = tracker.find_hands(frame)
        objects = detector.detect(frame)
        is_threat, threats = analyzer.calculate_threat(hands, objects)

        # 2. TEHDİT ALGILANDIĞINDA
        if is_threat and not threat_in_progress:
            obj_name = threats[0]["object"]
            conf = threats[0]["confidence"]

            log_threat(obj_name, conf)
            save_evidence(frame, obj_name)

            # VIDEO KAYDI BAŞLAT
            video_out, video_name = start_video_recording(w, h)
            recording_start_time = time.time()
            print(f"🎥 Video Kaydı Başladı: {video_name}")

            threading.Thread(
                target=speak_alarm,
                args=("Threat detected",),
                daemon=True
            ).start()

            threat_in_progress = True

        # 3. VIDEO KAYIT DEVAM EDİYORSA
        if video_out is not None:
            video_out.write(frame)

            if time.time() - recording_start_time > record_duration:
                video_out.release()
                video_out = None
                print("✅ Video Klip Kaydedildi.")

        if not is_threat:
            threat_in_progress = False

        # 4. ÇİZİMLER
        frame = tracker.draw_hands(frame)

        for obj in objects:
            x1, y1, x2, y2 = map(int, obj["box"])
            color = (0, 0, 255) if is_threat else (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                frame,
                obj["label"].upper(),
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )

        # 5. DASHBOARD
        panel_overlay = frame.copy()
        cv2.rectangle(panel_overlay, (w - 230, 0), (w, 160), (30, 30, 30), -1)
        frame = cv2.addWeighted(panel_overlay, 0.7, frame, 0.3, 0)

        status_color = (0, 0, 255) if is_threat else (0, 255, 0)
        status_text = "DANGER" if is_threat else "SECURE"

        cv2.putText(frame, "SECURITY DASHBOARD", (w - 215, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
        cv2.line(frame, (w - 215, 40), (w - 15, 40), (100, 100, 100), 1)

        cv2.putText(frame, f"STATUS: {status_text}", (w - 215, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        cv2.putText(frame, f"OBJECTS: {len(objects)}", (w - 215, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(frame, f"HANDS: {len(hands)}", (w - 215, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # FPS
        c_time = time.time()
        fps = 1 / (c_time - p_time) if p_time else 0
        p_time = c_time
        cv2.putText(frame, f"FPS: {int(fps)}", (w - 215, 145),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)

        # 6. ALT UYARI BAR
        if is_threat:
            cv2.rectangle(frame, (0, h - 50), (w, h), (0, 0, 255), -1)
            cv2.putText(
                frame,
                f"WARNING: {threats[0]['object'].upper()} DETECTED IN HAND!",
                (int(w / 2) - 260, h - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

        cv2.imshow("Advanced Threat Detection System v1.0", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if video_out:
        video_out.release()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
