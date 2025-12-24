import datetime
import os
import cv2

def log_threat(object_name, confidence):
    """
    Tehdit algılandığında logs/threat_logs.txt dosyasına kayıt atar.
    """
    # 1. logs klasörü yoksa oluştur
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 2. Zaman damgasını al
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 3. Log mesajını hazırla
    log_message = f"[{timestamp}] TEHDIT: {object_name} tespit edildi! (Guven: {confidence:.2f})\n"
    
    # 4. Dosyaya ekle (append modu 'a')
    with open("logs/threat_logs.txt", "a", encoding="utf-8") as file:
        file.write(log_message)
    
    print(f">>> LOG KAYDEDILDI: {log_message.strip()}")

def save_evidence(frame, object_name):
    """
    Tehdit anında fotoğraf kaydeder (Advanced özellik için).
    """
    if not os.path.exists('evidences'):
        os.makedirs('evidences')
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"evidences/threat_{object_name}_{timestamp}.jpg"
    
    import cv2
    cv2.imwrite(filename, frame)
    return filename

def start_video_recording(frame_width, frame_height):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"evidences/threat_clip_{timestamp}.avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (frame_width, frame_height))
    return out, filename