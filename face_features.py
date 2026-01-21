import cv2
import os

# ======================================================
# FACE FEATURES (OpenCV ile basit yüz tespiti)
# DeepFace TensorFlow gerektirdiği için, 
# basit OpenCV Haar Cascade kullanıyoruz
# ======================================================

# Haar cascade yükle
face_cascade = None

def _load_cascade():
    global face_cascade
    if face_cascade is None:
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
    return face_cascade

def extract_face_features(video_path: str):
    """
    Videodan 5 farklı frame alır.
    Eğer bu frame'lerin herhangi birinde yüz bulunursa:
        - face_detected = True
    Hiçbir frame'de yüz yoksa:
        - face_detected = False
    
    Not: DeepFace yerine OpenCV kullanıldığı için
    emotion analizi yapılmıyor.
    """

    if not video_path or not os.path.exists(video_path):
        return {
            "face_detected": False,
            "face_dominant_emotion": None,
            "face_emotion_score": 0.0,
        }

    cascade = _load_cascade()
    
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if frame_count <= 0:
        cap.release()
        return {
            "face_detected": False,
            "face_dominant_emotion": None,
            "face_emotion_score": 0.0,
        }

    # Videonun %10, %30, %50, %70, %90 noktaları
    frame_indices = [
        int(frame_count * 0.10),
        int(frame_count * 0.30),
        int(frame_count * 0.50),
        int(frame_count * 0.70),
        int(frame_count * 0.90),
    ]

    face_count = 0
    
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue

        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            if len(faces) > 0:
                face_count += 1
                
        except Exception:
            continue

    cap.release()

    # En az bir frame'de yüz bulundu mu?
    if face_count > 0:
        return {
            "face_detected": True,
            "face_dominant_emotion": "detected",  # Emotion analizi yok
            "face_emotion_score": round(face_count / len(frame_indices), 2),
        }

    return {
        "face_detected": False,
        "face_dominant_emotion": None,
        "face_emotion_score": 0.0,
    }
