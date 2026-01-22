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
    brew install python@3.11 git ffmpeg tesseract
    ```

## 2. Projeyi İndirme (Klonlama)

Terminalde projeyi indirmek istediğiniz klasöre gidin ve:

```bash
git clone https://github.com/aliturhan0/riskanaliz.git
cd riskanaliz
```

## 🚨 ÖNEMLİ ADIM: Model Dosyaları

Bu proje Yapay Zeka modeli kullanmaktadır. GitHub'a sığmadığı için aşağıdaki **İKİ KLASÖRÜ** manuel indirmeniz ZORUNLUDUR:

1.  **[BERT MODEL KLASÖRÜ (my_suicide_bert_model)](https://drive.google.com/drive/folders/1kuWtry5VCDYuCsKnf2tgX5fSfeoT9TUj)**
2.  **[PYCACHE KLASÖRÜ (__pycache__)](https://drive.google.com/drive/folders/1O_jxgsG20H2PmKCbjTmgH8Cjzh7VUdtB)**

**Yapılacaklar:**
1.  Linklerden dosyaları indirin.
2.  `riskanaliz` klasörünün içine sürükleyip bırakın.

👉 *Modelin eğitim kodlarını incelemek isterseniz: [Google Colab Linki](https://colab.research.google.com/drive/1fmDmyv6W7ezXBNjFa6U5CdSQKV5nhgwu?usp=share_link)*

## 3. Kurulum

1.  **Sanal Ortam Oluşturma:**
    ```bash
    python3.11 -m venv venv
    ```

2.  **Sanal Ortamı Aktif Etme:**
    ```bash
    source venv/bin/activate
    ```
    *(Komutun başında `(venv)` yazısını görmelisiniz)*

3.  **Kütüphaneleri Yükleme:**
    ```bash
    pip install requests pandas opencv-python easyocr playwright torch transformers openai-whisper ffmpeg-python certifi deep-translator imageio-ffmpeg sentencepiece
    python -m playwright install chromium
    ```

    *Not: Mac M1/M2/M3 işlemcili cihazlarda `torch` yüklemesi bazen uzun sürebilir veya özel ayar gerektirebilir.*

## 4. SSL Sertifikası (Önemli!)

Mac'te Python bazen SSL sertifika hatası verir. Bunu çözmek için terminalde şunu çalıştırın:

```bash
/Applications/Python\ 3.11/Install\ Certificates.command
```
*(Eğer dosya yoksa, finder'dan Uygulamalar -> Python 3.11 klasörüne gidip "Install Certificates" dosyasına çift tıklayın)*

## 5. Uygulamayı Çalıştırma

Venv aktifken:

```bash
python desktop_app.py
```

> **⚠️ ÖNEMLİ:** Program tarayıcıyı açtığında TikTok **Captcha (Puzzle)** sorabilir. Bunu tarayıcı penceresinden **manuel olarak çözmeniz** gerekir. Program siz doğrulamayı geçene kadar bekleyecektir.

## ⚠️ Mac Özel Uyarılar

- **Tkinter Hatası:** Eğer arayüz açılmazsa veya siyah ekran verirse, `python-tk` kütüphanesini brew ile yüklemeniz gerekebilir: `brew install python-tk`
- **İzinler:** Terminal, ilk çalıştırmada "Erişilebilirlik" veya "Ekran Kaydı" izni isteyebilir (Playwright tarayıcı kontrolü için). İzin verin.
