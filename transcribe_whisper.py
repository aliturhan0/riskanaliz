import os
import sys
import uuid
import subprocess
import certifi

# SSL sertifika yolu (Mac'te model indirme sorunlarını azaltır)
os.environ["SSL_CERT_FILE"] = certifi.where()

import whisper

# FFmpeg yolunu bul (Windows'ta PATH'de olmayabilir)
try:
    import imageio_ffmpeg
    FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
    # FFmpeg dizinini PATH'e ekle (Whisper'ın dahili çağrısı için gerekli)
    ffmpeg_dir = os.path.dirname(FFMPEG_BIN)
    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
except ImportError:
    FFMPEG_BIN = "ffmpeg"

def main():
    if len(sys.argv) < 3:
        # Kullanım: python transcribe_whisper.py <video_path> <out_txt>
        sys.exit(1)

    video_path = sys.argv[1]
    out_path = sys.argv[2]

    if not os.path.exists(video_path):
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("")
        sys.exit(0)

    # WAV dosyasını video ile aynı dizine koy
    video_dir = os.path.dirname(video_path)
    wav_path = os.path.join(video_dir, f"_audio_{uuid.uuid4().hex}.wav")

    try:
        print(f"[DEBUG] Video path: {video_path}")
        print(f"[DEBUG] Video exists: {os.path.exists(video_path)}")
        print(f"[DEBUG] FFMPEG_BIN: {FFMPEG_BIN}")
        print(f"[DEBUG] FFMPEG exists: {os.path.exists(FFMPEG_BIN)}")
        
        # MP4 -> WAV (PCM, mono, 16kHz)
        cmd = [
            FFMPEG_BIN, "-y",
            "-i", video_path,
            "-ac", "1",
            "-ar", "16000",
            "-vn",
            wav_path
        ]
        print(f"[DEBUG] Running FFmpeg via imageio_ffmpeg subprocess...")
        sys.stdout.flush()
        
        # imageio_ffmpeg'in subprocess wrapper'ını kullan
        try:
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            
            # FFmpeg komutu DOSYA ÇIKTISI ile (pipe değil)
            cmd = [
                ffmpeg_exe, "-y",
                "-i", video_path,
                "-ac", "1",
                "-ar", "16000",
                "-vn",
                wav_path
            ]
            
            print(f"[DEBUG] Command: {' '.join(cmd)}")
            sys.stdout.flush()
            
            # imageio_ffmpeg kendi subprocess yönetimini yapıyor
            # Biz de aynı şekilde Popen kullanalım ama shell=False
            import subprocess as sp
            process = sp.Popen(
                cmd,
                stdin=sp.PIPE,
                stdout=sp.PIPE,
                stderr=sp.PIPE
            )
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"[FFMPEG ERROR] Exit: {process.returncode}")
                print(f"[STDERR] {stderr.decode('utf-8', errors='ignore')[:500]}")
                sys.stdout.flush()
                raise Exception("FFmpeg failed")
            
            print(f"[DEBUG] FFmpeg success! WAV created: {wav_path}")
            print(f"[DEBUG] WAV exists: {os.path.exists(wav_path)}")
            sys.stdout.flush()
            
        except Exception as ffmpeg_error:
            print(f"[FFMPEG ERROR] {type(ffmpeg_error).__name__}: {ffmpeg_error}")
            sys.stdout.flush()
            raise

        # WAV dosyasını numpy array olarak oku (Whisper'ın FFmpeg çağrısını bypass et)
        import numpy as np
        import wave
        
        print(f"[DEBUG] Loading WAV file as numpy array...")
        sys.stdout.flush()
        
        with wave.open(wav_path, 'rb') as wav_file:
            sample_rate = wav_file.getframerate()
            n_frames = wav_file.getnframes()
            audio_data = wav_file.readframes(n_frames)
        
        # bytes -> numpy float32 array (Whisper formatı)
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        print(f"[DEBUG] Audio array shape: {audio_np.shape}, sample_rate: {sample_rate}")
        sys.stdout.flush()

        # Whisper model (local)
        print(f"[DEBUG] Loading Whisper model...")
        sys.stdout.flush()
        model = whisper.load_model("small")

        # HAM transcript (numpy array ile - FFmpeg bypass)
        print(f"[DEBUG] Transcribing with numpy array...")
        sys.stdout.flush()
        result = model.transcribe(
            audio_np,
            fp16=False
        )

        text = (result.get("text") or "").strip()
        print(f"[DEBUG] Transcript alındı: {len(text)} karakter")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)

    except Exception as e:
        # Hata olursa EKRANA YAZ ve boş dosya oluştur
        print(f"[HATA] transcribe_whisper.py: {e}")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("")
    finally:
        if os.path.exists(wav_path):
            try:
                os.remove(wav_path)
            except:
                pass

if __name__ == "__main__":
    main()
