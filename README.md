# 🕵️‍♂️ TikTok Risk Analyzer & Archiver

**TikTok Risk Analizörü**, TikTok videolarını hashtag veya kullanıcı bazlı tarayan, indiren, metin/ses/görsel analizi yapan ve **Yapay Zeka (BERT)** ile risk skoru hesaplayan kapsamlı bir araçtır.

## 🚀 Özellikler

- **🛡️ Risk Analizi:** Videoların açıklama, ses (transkript), görsel ve üzerindeki yazıları (OCR) analiz ederek 0-100 arası risk skoru verir.
- **🎨 Premium Modern UI:** Karanlık mod, neon efektli butonlar ve aşamalı, detaylı progress bar.
- **🧠 NotebookLM Entegrasyonu:** Analiz edilen verileri tek tıkla NotebookLM formatına çevirir ve profesyonel analiz promptu oluşturur.
- **📥 Otomatik İndirme:** Filigransız video indirme desteği.
- **📝 Çoklu Veri Çıkarımı:**
  - **Whisper AI:** Videodan sesi yazıya (transcript) döker.
  - **OCR:** Video üzerindeki gömülü yazıları okur.
  - **Yüz Analizi:** Videoda yüz olup olmadığını tespit eder.
  - **Görsel Analiz:** Parlaklık ve bulanıklık tespiti yapar.

## 🛠️ Gereksinimler

- **Python 3.11.9** (Önerilen Sürüm)
- **FFmpeg** (Ses işleme için zorunlu)
- **Git**

## 📚 Kurulum ve Kullanım Rehberi

> [!IMPORTANT]
> **🚨 ÇOK ÖNEMLİ - İLK ADIM:**
> Uygulamanın çalışması için **2 zorunlu klasörü** indirip proje ana dizinine atmanız gerekmektedir:
> 
> 1. 📂 **[BERT MODEL KLASÖRÜNÜ İNDİR](https://drive.google.com/drive/folders/1kuWtry5VCDYuCsKnf2tgX5fSfeoT9TUj)** (`my_suicide_bert_model` klasörü)
> 2. 📂 **[PYCACHE KLASÖRÜNÜ İNDİR](https://drive.google.com/drive/folders/1fpdCmBWxDt6mOuLYco7O0am_jAyHP8Ux?usp=share_link)** (`__pycache__` klasörü)
> 
> *Bu klasörleri indirdikten sonra proje klasörünün içine sürükleyip bırakın.*
>
> ℹ️ **Meraklısı İçin:** Bu modelin nasıl eğitildiğini incelemek isterseniz [Google Colab Notebook](https://colab.research.google.com/drive/1fmDmyv6W7ezXBNjFa6U5CdSQKV5nhgwu?usp=share_link) sayfasını ziyaret edebilirsiniz.

İşletim sisteminize uygun rehberi seçin:

### 👉 [WINDOWS Kurulum Rehberi](docs/WINDOWS_TUTORIAL.md)
### 👉 [MAC OS Kurulum Rehberi](docs/MAC_TUTORIAL.md)

## ⚡ Hızlı Bakış

1. **Mod Seçin:** Hashtag (`#risk`) veya Kullanıcı (`@username`)
2. **Limit:** Kaç video taranacağını belirleyin (örn: 5)
3. **Başlat:** "Analizi Başlat" butonuna basın.
4. **İzle:** Uygulama TikTok'a bağlanır, videoları indirir ve analiz eder.
5. **Sonuç:** `data/csv` klasöründe detaylı CSV dosyası ve analiz raporu oluşur.

---
**Sorumluluk Reddi:** Bu araç sadece eğitim ve araştırma amaçlıdır. TikTok'un kullanım koşullarına uyunuz.
