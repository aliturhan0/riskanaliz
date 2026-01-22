# 🪟 Windows Installation & Usage Guide

This guide explains how to install and run the TikTok Risk Analyzer application on your Windows computer from scratch.

## 1. Prerequisites (Required Programs)

Make sure the following programs are installed. If not, download and install them from the links (don't forget to check "Add to PATH"!):

1.  **Python 3.11.9 (Recommended):** [Download](https://www.geeks3d.com/dl/show/10222)
    *   *During installation, MAKE SURE to check the "Add Python to PATH" checkbox.*
2.  **Git:** [Download](https://git-scm.com/download/win)
3.  **FFmpeg:**
    *   **Easy Method (with Winget):** Open Terminal (PowerShell) and type:
        ```powershell
        winget install Gyan.FFmpeg
        ```
    *   Close and reopen the terminal after installation.

## 2. Download the Project (Clone)

1.  Create an empty folder on your Desktop or anywhere you prefer.
2.  Right-click inside the folder and select **"Open in Terminal"** (or Git Bash).
3.  Paste the following command:

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
3.  Your folder structure should look like this:
    ```
    riskanaliz/
    ├── my_suicide_bert_model/
    ├── __pycache__/
    ├── desktop_app.py
    └── ...
    ```

👉 *To see how the model was trained: [Google Colab Link](https://colab.research.google.com/drive/1fmDmyv6W7ezXBNjFa6U5CdSQKV5nhgwu?usp=share_link)*

## 3. Installation (Automatic)

Run the following commands in order in your terminal:

1.  **Create Virtual Environment:**
    ```powershell
    python -m venv venv
    ```

2.  **Activate Virtual Environment:**
    ```powershell
    .\venv\Scripts\activate
    ```
    *(You should see `(venv)` at the beginning of the command line)*

3.  **Install Libraries:**
    ```powershell
    pip install -r requirements.txt
    ```
    *(If requirements.txt doesn't exist, use the manual command below)*

    **Manual Installation Command:**
    ```powershell
    pip install requests pandas opencv-python easyocr playwright torch transformers openai-whisper ffmpeg-python certifi deep-translator imageio-ffmpeg sentencepiece
    python -m playwright install chromium
    ```

## 4. Run the Application

Everything is ready! To start the application:

```powershell
python desktop_app.py
```

> **⚠️ IMPORTANT:** When the program opens the browser, TikTok may show a **Captcha (Puzzle)**. You need to **solve it manually** in the browser window. The program will wait until you pass the verification.

## ❓ Frequently Asked Questions

**Q:** I'm getting `ModuleNotFoundError: No module named ...` error.
**A:** Make sure the virtual environment is active (should show `(venv)`). Run the `pip install ...` command again.

**Q:** "FFmpeg not found" error.
**A:** Try restarting your computer after installing FFmpeg, or check if it's properly added to PATH.

**Q:** The interface opens but stays on "Connecting".
**A:** Check your internet connection. TikTok may temporarily block your IP if too many requests are made. Try turning off VPN.
