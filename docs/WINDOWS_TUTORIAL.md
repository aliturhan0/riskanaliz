# 🪟 Windows Kurulum ve Kullanım Rehberi

Bu rehber, TikTok Risk Analyzer uygulamasını Windows bilgisayarınızda sıfırdan nasıl kurup çalıştıracağınızı anlatır.

## 1. Ön Hazırlıklar (Gerekli Programlar)

Aşağıdaki programların yüklü olduğundan emin olun. Değilse linklerden indirip kurun ("Add to PATH" seçeneğini işaretlemeyi unutmayın!):

1.  **Python 3.11.9 (Tavsiye Edilen):** [İndir](https://www.geeks3d.com/dl/show/10222)
    *   *Kurulum sırasında "Add Python to PATH" kutucuğunu MUTLAKA işaretleyin.*
2.  **Git:** [İndir](https://git-scm.com/download/win)
3.  **FFmpeg:**
    *   **Kolay Yöntem (Winget ile):** Terminali (PowerShell) açın ve şunu yazın:
        ```powershell
        winget install Gyan.FFmpeg
        ```
    *   Kurulumdan sonra terminali kapatıp yeniden açın.

## 2. Projeyi İndirme (Klonlama)

1.  Masaüstünde veya istediğiniz bir yerde boş bir klasör açın.
2.  Klasörün içinde sağ tıklayıp **"Open in Terminal"** (veya Git Bash) deyin.
3.  Şu komutu yapıştırın:

```bash
git clone https://github.com/aliturhan0/riskanaliz.git
cd riskanaliz
```

## 🚨 ÖNEMLİ ADIM: Model Dosyaları

Bu proje Yapay Zeka modeli kullanmaktadır. GitHub'a sığmadığı için aşağıdaki **İKİ KLASÖRÜ** manuel indirmeniz ZORUNLUDUR:

1.  **[BERT MODEL KLASÖRÜ (my_suicide_bert_model)](https://drive.google.com/drive/folders/1kuWtry5VCDYuCsKnf2tgX5fSfeoT9TUj)**
2.  **[PYCACHE KLASÖRÜ (__pycache__)](https://drive.google.com/drive/folders/1fpdCmBWxDt6mOuLYco7O0am_jAyHP8Ux?usp=share_link)**

**Yapılacaklar:**
1.  Linklerden dosyaları indirin.
2.  `riskanaliz` klasörünün içine sürükleyip bırakın.
3.  Klasör yapısı şöyle görünmeli:
    ```
    riskanaliz/
    ├── my_suicide_bert_model/
    ├── __pycache__/
    ├── desktop_app.py
    └── ...
    ```

👉 *Modelin eğitim kodlarını incelemek isterseniz: [Google Colab Linki](https://colab.research.google.com/drive/1fmDmyv6W7ezXBNjFa6U5CdSQKV5nhgwu?usp=share_link)*

## 3. Kurulum (Otomatik)

Terminalde şu komutları sırasıyla çalıştırın:

1.  **Sanal Ortam Oluşturma:**
    ```powershell
    python -m venv venv
    ```

2.  **Sanal Ortamı Aktif Etme:**
    ```powershell
    .\venv\Scripts\activate
    ```
    *(Komutun başında `(venv)` yazısını görmelisiniz)*

3.  **Kütüphaneleri Yükleme:**
    ```powershell
    pip install -r requirements.txt
    ```
    *(Eğer requirements.txt yoksa aşağıdaki manuel komutu kullanın)*

    **Manuel Yükleme Komutu:**
    ```powershell
    pip install requests pandas opencv-python easyocr playwright torch transformers openai-whisper ffmpeg-python certifi
    python -m playwright install chromium
    ```

## 4. Uygulamayı Çalıştırma

Her şey hazır! Uygulamayı başlatmak için:

```powershell
python desktop_app.py
```

## ❓ Sık Karşılaşılan Sorunlar

**Soru:** `ModuleNotFoundError: No module named ...` hatası alıyorum.
**Çözüm:** Sanal ortamın aktif olduğundan emin olun (`(venv)` yazmalı). Tekrar `pip install ...` komutunu çalıştırın.

**Soru:** "FFmpeg bulunamadı" hatası.
**Çözüm:** FFmpeg'i kurduktan sonra bilgisayarı yeniden başlatmayı deneyin veya PATH'e eklenip eklenmediğini kontrol edin.

**Soru:** Arayüz açılıyor ama "Bağlanıyor"da kalıyor.
**Çözüm:** İnternet bağlantınızı kontrol edin. TikTok bazen çok fazla istek yapıldığında IP'nizi geçici engelleyebilir. VPN kapatıp deneyin.
