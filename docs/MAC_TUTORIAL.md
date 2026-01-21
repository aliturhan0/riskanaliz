# 🍎 Mac OS Kurulum ve Kullanım Rehberi

Bu rehber, TikTok Risk Analyzer uygulamasını Mac bilgisayarınızda nasıl kurup çalıştıracağınızı anlatır.

## 1. Ön Hazırlıklar (Homebrew ile)

Mac'te kurulum yapmanın en kolay yolu **Homebrew** kullanmaktır. Terminali açın:

1.  **Homebrew Yüklü mü?**
    Değilse terminale şunu yapıştırın:
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2.  **Gerekli Araçları Yükleyin:**
    ```bash
    brew install python@3.10 git ffmpeg tesseract
    ```

## 2. Projeyi İndirme (Klonlama)

Terminalde projeyi indirmek istediğiniz klasöre gidin ve:

```bash
git clone https://github.com/aliturhan0/riskanaliz.git
cd riskanaliz
```

## 3. Kurulum

1.  **Sanal Ortam Oluşturma:**
    ```bash
    python3.10 -m venv venv
    ```

2.  **Sanal Ortamı Aktif Etme:**
    ```bash
    source venv/bin/activate
    ```
    *(Komutun başında `(venv)` yazısını görmelisiniz)*

3.  **Kütüphaneleri Yükleme:**
    ```bash
    pip install requests pandas opencv-python easyocr playwright torch transformers openai-whisper ffmpeg-python certifi
    python -m playwright install chromium
    ```

    *Not: Mac M1/M2/M3 işlemcili cihazlarda `torch` yüklemesi bazen uzun sürebilir veya özel ayar gerektirebilir.*

## 4. SSL Sertifikası (Önemli!)

Mac'te Python bazen SSL sertifika hatası verir. Bunu çözmek için terminalde şunu çalıştırın:

```bash
/Applications/Python\ 3.10/Install\ Certificates.command
```
*(Eğer dosya yoksa, finder'dan Uygulamalar -> Python 3.10 klasörüne gidip "Install Certificates" dosyasına çift tıklayın)*

## 5. Uygulamayı Çalıştırma

Venv aktifken:

```bash
python desktop_app.py
```

## ⚠️ Mac Özel Uyarılar

- **Tkinter Hatası:** Eğer arayüz açılmazsa veya siyah ekran verirse, `python-tk` kütüphanesini brew ile yüklemeniz gerekebilir: `brew install python-tk`
- **İzinler:** Terminal, ilk çalıştırmada "Erişilebilirlik" veya "Ekran Kaydı" izni isteyebilir (Playwright tarayıcı kontrolü için). İzin verin.
