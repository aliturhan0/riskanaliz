import os
import sys
import uuid
import subprocess
import certifi

# SSL sertifika yolu (Mac'te model indirme sorunlarını azaltır)
os.environ["SSL_CERT_FILE"] = certifi.where()

try:
    import whisper
except ImportError:
    # Bu dosya import edildiğinde hata vermesin, çağıran yer (tiktok_scraper) yakalasın
    whisper = None

# Global model değişkeni (modül içinde tutmak için)
_global_model = None

def get_model():
    """Modeli sadece bir kez yükle ve döndür"""
    global _global_model
    if _global_model is None:
        # SSL sertifika hatası için fix
        try:
            _global_model = whisper.load_model("small")
        except:
            # SSL hatası olursa
            import ssl
            ssl._create_default_https_context = ssl._create_unverified_context
            _global_model = whisper.load_model("small")
    return _global_model

def transcribe_audio(video_path, model=None):
    """
    Video dosyasından sesi çıkarıp metne döker.
    model argümanı verilirse onu kullanır, verilmezse global modeli yükler.
    """
    wav_path = f"_audio_{uuid.uuid4().hex}.wav"
    try:
        # 1. FFmpeg ile sesi çıkar (WAV)
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-ac", "1",
            "-ar", "16000",
            "-vn",
            wav_path
        ]
        # Hata bastırmak için stderr=DEVNULL
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # 2. Modeli hazırla
        if model is None:
            model = get_model()

        # 3. Transkript al
        result = model.transcribe(wav_path, fp16=False)
        return (result.get("text") or "").strip()

    except Exception as e:
        print(f"Transcript hatası: {e}")
        return ""
    finally:
        # Geçici ses dosyasını sil
        if os.path.exists(wav_path):
            try:
                os.remove(wav_path)
            except:
                pass

def main():
    if len(sys.argv) < 3:
        print("Kullanım: python transcribe_whisper.py <video_path> <out_txt>")
        sys.exit(1)

    video_path = sys.argv[1]
    out_path = sys.argv[2]
    
    if not os.path.exists(video_path):
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("")
        return

    text = transcribe_audio(video_path)
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    main()
