# 🕵️‍♂️ TikTok Risk Intelligence System

**🇬🇧 English Documentation:** [README_EN.md](README_EN.md) | [Windows Guide](docs/WINDOWS_TUTORIAL_EN.md) | [Mac Guide](docs/MAC_TUTORIAL_EN.md)

---

**TikTok Risk Analizörü**, TikTok videolarını hashtag veya kullanıcı bazlı tarayan, derinlemesine analiz eden profesyonel bir veri istihbarat aracıdır.

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
> 2. 📂 **[PYCACHE KLASÖRÜNÜ İNDİR](https://drive.google.com/drive/folders/1O_jxgsG20H2PmKCbjTmgH8Cjzh7VUdtB)** (`__pycache__` klasörü)
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
4. **İzle:** Uygulama TikTok'a bağlanır.
    > ⚠️ **Not:** İlk açılışta Captcha/Puzzle çıkarsa tarayıcıdan manuel olarak çözün. Program bunu algılayıp devam edecektir.
5. **Sonuç:** `data/csv` klasöründe detaylı CSV dosyası ve analiz raporu oluşur.
6. **Yapay Zeka Yorumu:** Oluşan CSV dosyasını seçip **"🚀 NotebookLM"** butonuna basın. Otomatik oluşturulan prompt ile analiz raporunuzu yapay zekaya yorumlatın.

---

## 📖 Referanslar ve Kaynaklar

Bu proje aşağıdaki akademik çalışma ve veri setlerinden esinlenilerek geliştirilmiştir:

| Kaynak | Açıklama | Link |
|--------|----------|------|
| 📄 **IEEE Makalesi** | Projemizin temel aldığı akademik araştırma makalesi | [IEEE Xplore](https://ieeexplore.ieee.org/document/9591887) |
| 📊 **Kaggle Veri Seti** | Makalede kullanılan "Suicide Watch" veri seti | [Kaggle Dataset](https://www.kaggle.com/datasets/nikhileswarkomati/suicide-watch) |
| 📂 **Veri Seti Dosyaları** | Eğitim için kullanılan tüm veri seti dosyaları | [Google Drive](https://drive.google.com/drive/folders/1JugPur8Axd7OG874V9MitWIIiatp_OSW?usp=sharing) |

---

**Sorumluluk Reddi:** Bu araç sadece eğitim ve araştırma amaçlıdır. TikTok'un kullanım koşullarına uyunuz.
