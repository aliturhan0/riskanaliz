# 🍎 Mac OS Installation & Usage Guide

This guide explains how to install and run the TikTok Risk Analyzer application on your Mac computer.

## 1. Prerequisites (with Homebrew)

The easiest way to install on Mac is using **Homebrew**. Open Terminal:

1.  **Is Homebrew installed?**
    If not, paste this in the terminal:
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2.  **Install Required Tools:**
    ```bash
    brew install python@3.11 git ffmpeg tesseract
    ```

## 2. Download the Project (Clone)

Navigate to the folder where you want to download the project in Terminal and run:

```bash
git clone https://github.com/aliturhan0/riskanaliz.git
cd riskanaliz
```

## 🚨 IMPORTANT STEP: Model Files

This project uses an AI model. Since it's too large for GitHub, you MUST manually download the following **TWO FOLDERS**:

1.  **[BERT MODEL FOLDER (my_suicide_bert_model)](https://drive.google.com/drive/folders/1kuWtry5VCDYuCsKnf2tgX5fSfeoT9TUj)**
2.  **[PYCACHE FOLDER (__pycache__)](https://drive.google.com/drive/folders/1O_jxgsG20H2PmKCbjTmgH8Cjzh7VUdtB)**

**Steps:**
1.  Download the files from the links.
2.  Drag and drop them into the `riskanaliz` folder.

👉 *To see how the model was trained: [Google Colab Link](https://colab.research.google.com/drive/1fmDmyv6W7ezXBNjFa6U5CdSQKV5nhgwu?usp=share_link)*

## 3. Installation

1.  **Create Virtual Environment:**
    ```bash
    python3.11 -m venv venv
    ```

2.  **Activate Virtual Environment:**
    ```bash
    source venv/bin/activate
    ```
    *(You should see `(venv)` at the beginning of the command line)*

3.  **Install Libraries:**
    ```bash
    pip install requests pandas opencv-python easyocr playwright torch transformers openai-whisper ffmpeg-python certifi deep-translator imageio-ffmpeg sentencepiece
    python -m playwright install chromium
    ```

    *Note: On Mac M1/M2/M3 chips, `torch` installation may take longer or require special configuration.*

## 4. SSL Certificate (Important!)

Python on Mac sometimes gives SSL certificate errors. To fix this, run in terminal:

```bash
/Applications/Python\ 3.11/Install\ Certificates.command
```
*(If the file doesn't exist, go to Finder -> Applications -> Python 3.11 folder and double-click "Install Certificates")*

## 5. Run the Application

With venv active:

```bash
python desktop_app.py
```

> **⚠️ IMPORTANT:** When the program opens the browser, TikTok may show a **Captcha (Puzzle)**. You need to **solve it manually** in the browser window. The program will wait until you pass the verification.

## ⚠️ Mac-Specific Notes

- **Tkinter Error:** If the interface doesn't open or shows a black screen, you may need to install `python-tk` library with brew: `brew install python-tk`
- **Permissions:** Terminal may request "Accessibility" or "Screen Recording" permissions on first run (for Playwright browser control). Grant the permissions.
