# 🕵️‍♂️ TikTok Risk Analyzer & Archiver

**TikTok Risk Analyzer** is a comprehensive tool that scans TikTok videos by hashtag or username, downloads them, performs text/audio/visual analysis, and calculates risk scores using **Artificial Intelligence (BERT)**.

## 🚀 Features

- **🛡️ Risk Analysis:** Analyzes video descriptions, audio (transcript), visuals, and overlay text (OCR) to provide a 0-100 risk score.
- **🎨 Premium Modern UI:** Dark mode, neon-effect buttons, and detailed step-by-step progress bar.
- **🧠 NotebookLM Integration:** One-click conversion of analyzed data to NotebookLM format with professional analysis prompts.
- **📥 Automatic Download:** Watermark-free video download support.
- **📝 Multi-Data Extraction:**
  - **Whisper AI:** Converts video audio to text (transcript).
  - **OCR:** Reads embedded text on videos.
  - **Face Detection:** Detects whether faces are present in videos.
  - **Visual Analysis:** Measures brightness and blur levels.

## 🛠️ Requirements

- **Python 3.11.9** (Recommended Version)
- **FFmpeg** (Required for audio processing)
- **Git**

## 📚 Installation & Usage Guide

> [!IMPORTANT]
> **🚨 CRITICAL - FIRST STEP:**
> For the application to work, you MUST download **2 required folders** and place them in the project root directory:
> 
> 1. 📂 **[DOWNLOAD BERT MODEL FOLDER](https://drive.google.com/drive/folders/1kuWtry5VCDYuCsKnf2tgX5fSfeoT9TUj)** (`my_suicide_bert_model` folder)
> 2. 📂 **[DOWNLOAD PYCACHE FOLDER](https://drive.google.com/drive/folders/1O_jxgsG20H2PmKCbjTmgH8Cjzh7VUdtB)** (`__pycache__` folder)
> 
> *After downloading, drag and drop these folders into the project directory.*
>
> ℹ️ **For the curious:** If you want to see how this model was trained, visit the [Google Colab Notebook](https://colab.research.google.com/drive/1fmDmyv6W7ezXBNjFa6U5CdSQKV5nhgwu?usp=share_link).

Choose the guide for your operating system:

### 👉 [WINDOWS Installation Guide](docs/WINDOWS_TUTORIAL_EN.md)
### 👉 [MAC OS Installation Guide](docs/MAC_TUTORIAL_EN.md)

---

**🇹🇷 Türkçe Dokümantasyon:** [README.md](README.md) | [Windows Rehberi](docs/WINDOWS_TUTORIAL.md) | [Mac Rehberi](docs/MAC_TUTORIAL.md)

---

## ⚡ Quick Overview

1. **Select Mode:** Hashtag (`#risk`) or User (`@username`)
2. **Limit:** Set how many videos to scan (e.g., 5)
3. **Start:** Click the "Start Analysis" button.
4. **Watch:** The application connects to TikTok.
    > ⚠️ **Note:** If a Captcha/Puzzle appears on the first launch, solve it manually in the browser. The program will detect this and continue.
5. **Results:** A detailed CSV file and analysis report are created in the `data/csv` folder.
6. **AI Interpretation:** Select the CSV file and click the **"🚀 NotebookLM"** button. Have the AI interpret your analysis report using the auto-generated prompt.

---
**Disclaimer:** This tool is for educational and research purposes only. Please comply with TikTok's terms of service.
