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

# FFmpeg yolunu belirle (imageio-ffmpeg varsa onu kullan, yoksa sistemdekini)
try:
    import imageio_ffmpeg
    FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
    
    # KRTİK DÜZELTME: Whisper kütüphanesi de arka planda 'ffmpeg' komutunu çağırır.
    # Bu yüzden imageio-ffmpeg'in bulduğu ffmpeg klasörünü PATH'e eklemeliyiz.
    ffmpeg_dir = os.path.dirname(FFMPEG_BIN)
    os.environ["PATH"] += os.pathsep + ffmpeg_dir
    
except ImportError:
    FFMPEG_BIN = "ffmpeg"

# Global model değişkeni (modül içinde tutmak için)
_global_model = None

def get_model():
    """Modeli sadece bir kez yükle ve döndür"""
    global _global_model
    
    # Whisper kütüphanesi yüklü mü kontrol et
    if whisper is None:
        raise ImportError("openai-whisper kütüphanesi bulunamadı! Lütfen 'pip install openai-whisper' komutunu çalıştırın.")

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

# numpy import et (Whisper'a array vermek için)
import numpy as np

def load_audio_custom(file_path, sr=16000):
    """
    Sesi doğrudan numpy array olarak okur.
    Whisper'ın kendi load_audio fonksiyonu yerine bunu kullanacağız çünkü
    Whisper arka planda sistem ffmpeg'ini arıyor ve bulamıyor.
    """
    try:
        print(f"🎤 [CUSTOM LOAD] Ses okunuyor: {file_path}")
        print(f"🎤 [CUSTOM LOAD] Kullanılan FFMPEG: {FFMPEG_BIN}")
        
        cmd = [
            FFMPEG_BIN,
            "-nostdin",
            "-threads", "0",
            "-i", file_path,
            "-f", "s16le",
            "-ac", "1",
            "-acodec", "pcm_s16le",
            "-ar", str(sr),
            "-"
        ]
        
        # Sesi stdout'a yaz
        # bufsize hatasını önlemek için büyük buffer
        process = subprocess.run(
            cmd,
            capture_output=True,
            check=True
        )
        
        audio = np.frombuffer(process.stdout, np.int16).flatten().astype(np.float32) / 32768.0
        print(f"✅ [CUSTOM LOAD] Ses başarıyla numpy array'e çevrildi: {len(audio)} samples")
        return audio
        
    except Exception as e:
        print(f"❌ [CUSTOM LOAD HATA]: {e}")
        if hasattr(e, 'stderr'):
             print(f"⬇️ STDERR:\n{e.stderr.decode('utf-8', errors='ignore')}")
        raise e

def transcribe_audio(video_path, model=None):
    """
    Video dosyasından sesi çıkarıp metne döker.
    model argümanı verilirse onu kullanır, verilmezse global modeli yükler.
    """
    wav_path = f"_audio_{uuid.uuid4().hex}.wav"
    try:
        if not os.path.exists(video_path):
            print(f"❌ [HATA] Video dosyası bulunamadı: {video_path}")
            return ""

        # 1. FFmpeg ile sesi çıkar (WAV)
        print(f"🎬 [FFMPEG] Kullanılan Exe: {FFMPEG_BIN}")
        
        cmd = [
            FFMPEG_BIN, "-y",
            "-i", video_path,
            "-ac", "1",
            "-ar", "16000",
            "-vn",
            wav_path
        ]
        
        # FFmpeg çalıştır
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"✅ [FFMPEG] Ses ayrıştırıldı: {wav_path}")

        # 2. Modeli hazırla
        if model is None:
            model = get_model()

        # 3. Transkript al (CUSTOM LOAD KULLANARAK)
        # Whisper'a dosya yolu yerine doğrudan ses verisini (array) veriyoruz
        print("⏳ [WHISPER] Transkript başlıyor (Custom Loader)...")
        audio_data = load_audio_custom(wav_path)
        result = model.transcribe(audio_data, fp16=False)
        
        text = (result.get("text") or "").strip()
        print(f"📝 [SONUÇ] Transkript uzunluğu: {len(text)} karakter")
        return text

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
