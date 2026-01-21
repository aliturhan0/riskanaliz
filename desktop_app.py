import os
import sys
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import re

# ======================================================
# PROJECT FOLDERS
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_DIR = os.path.join(BASE_DIR, "data", "csv")
TXT_DIR = os.path.join(BASE_DIR, "data", "notebooklm_txt")

os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(TXT_DIR, exist_ok=True)

APP_TITLE = "TikTok Risk Analyzer Pro"
SCRIPT_NAME = "tiktok_scraper_raw.py"
NOTEBOOKLM_URL = "https://notebooklm.google.com/"


class Theme:
    """Temiz ve modern renk paleti"""
    # Arka Plan
    BG_DARK = "#0f1419"
    BG_CARD = "#1a1f26"
    BG_INPUT = "#242b33"
    
    # Border
    BORDER = "#2f3640"
    BORDER_FOCUS = "#5865f2"
    
    # Accent
    PRIMARY = "#5865f2"
    SUCCESS = "#57f287"
    DANGER = "#ed4245"
    WARNING = "#fee75c"
    INFO = "#5bc0eb"
    CYAN = "#00d9ff"
    
    # Text
    TEXT = "#ffffff"
    TEXT_SECONDARY = "#8b949e"
    TEXT_MUTED = "#6e7681"
    
    # Font
    FONT = "Segoe UI"
    FONT_MONO = "Consolas"


class SimpleButton(tk.Frame):
    """Sade ve temiz buton"""
    def __init__(self, parent, text="", command=None, style="primary", width=120, **kwargs):
        super().__init__(parent, bg=Theme.BG_DARK, **kwargs)
        
        self.command = command
        self.enabled = True
        
        # Stil renklerini ayarla
        colors = {
            "primary": (Theme.PRIMARY, "#ffffff"),
            "success": (Theme.SUCCESS, "#000000"),
            "danger": (Theme.DANGER, "#ffffff"),
            "ghost": (Theme.BG_CARD, Theme.TEXT),
            "cyan": (Theme.CYAN, "#000000"),
        }
        self.bg_color, self.fg_color = colors.get(style, (Theme.PRIMARY, "#ffffff"))
        self.style_name = style
        
        self.btn = tk.Label(
            self, text=text, bg=self.bg_color, fg=self.fg_color,
            font=(Theme.FONT, 10, "bold"), padx=20, pady=10,
            cursor="hand2", width=width // 10
        )
        self.btn.pack(fill="both", expand=True)
        
        # Border for ghost style
        if style == "ghost":
            self.config(highlightbackground=Theme.BORDER, highlightthickness=1)
        
        self.btn.bind("<Enter>", self._on_enter)
        self.btn.bind("<Leave>", self._on_leave)
        self.btn.bind("<Button-1>", self._on_click)
    
    def _on_enter(self, e):
        if self.enabled:
            self.btn.config(bg=self._lighten(self.bg_color))
    
    def _on_leave(self, e):
        if self.enabled:
            self.btn.config(bg=self.bg_color)
    
    def _on_click(self, e):
        if self.enabled and self.command:
            self.command()
    
    def _lighten(self, color):
        r = min(255, int(color[1:3], 16) + 20)
        g = min(255, int(color[3:5], 16) + 20)
        b = min(255, int(color[5:7], 16) + 20)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def configure(self, **kwargs):
        if "state" in kwargs:
            self.enabled = kwargs["state"] != "disabled"
            if self.enabled:
                self.btn.config(bg=self.bg_color, fg=self.fg_color, cursor="hand2")
            else:
                self.btn.config(bg=Theme.BG_INPUT, fg=Theme.TEXT_MUTED, cursor="")
        if "text" in kwargs:
            self.btn.config(text=kwargs["text"])
    
    def config(self, **kwargs):
        self.configure(**kwargs)


class ProgressTracker(tk.Frame):
    """
    Aşamalı ilerleme gösteren çubuk.
    Aşamalar:
    - Bağlanma: %0-10
    - Doğrulama: %10-20  
    - Video işleme: %20-80
    - Risk analizi: %80-95
    - Tamamlama: %95-100
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=Theme.BG_DARK, **kwargs)
        
        # Üst: Durum yazısı
        self.status_frame = tk.Frame(self, bg=Theme.BG_DARK)
        self.status_frame.pack(fill="x", pady=(0, 8))
        
        self.status_label = tk.Label(
            self.status_frame, text="Hazır", bg=Theme.BG_DARK, 
            fg=Theme.TEXT_SECONDARY, font=(Theme.FONT, 10)
        )
        self.status_label.pack(side="left")
        
        self.progress_label = tk.Label(
            self.status_frame, text="", bg=Theme.BG_DARK,
            fg=Theme.TEXT, font=(Theme.FONT, 10, "bold")
        )
        self.progress_label.pack(side="right")
        
        # Alt: Progress bar
        self.bar_bg = tk.Frame(self, bg=Theme.BG_INPUT, height=10)
        self.bar_bg.pack(fill="x")
        self.bar_bg.pack_propagate(False)
        
        self.bar_fill = tk.Frame(self.bar_bg, bg=Theme.PRIMARY, height=10)
        self.bar_fill.place(x=0, y=0, relheight=1, width=0)
        
        # İlerleme takibi
        self.percent = 0
        self.video_current = 0
        self.video_total = 0
        self._is_pulsing = False
    
    def set_status(self, text, color=None):
        self.status_label.config(text=text, fg=color or Theme.TEXT_SECONDARY)
    
    def set_percent(self, percent, status_text="", color=None):
        """Yüzdeyi direkt ayarla"""
        self.percent = max(0, min(100, percent))
        self._update_bar()
        self.progress_label.config(text=f"%{self.percent:.0f}")
        if status_text:
            self.set_status(status_text, color or Theme.INFO)
    
    def _update_bar(self):
        """Çubuğu güncelle - relwidth ile yüzdeyi direkt yansıt"""
        if self._is_pulsing:
            return
        # relwidth kullanarak yüzdeyi direkt uygula (0.0 - 1.0 arası)
        rel_width = self.percent / 100.0
        self.bar_fill.place(x=0, y=0, relheight=1, relwidth=rel_width)
    
    def set_video_progress(self, current, total):
        """Video işleme ilerlemesini ayarla (20%-80% aralığı)"""
        self.video_current = current
        self.video_total = total
        self.sub_step = 0  # Alt adım sıfırla
        
        if total > 0:
            # 20% - 80% aralığında
            video_percent = (current / total) * 60  # 60% video işleme için
            self.percent = 20 + video_percent
            self._update_bar()
            self.progress_label.config(text=f"%{self.percent:.0f} ({current}/{total})")
            self.set_status(f"📹 Video {current}/{total} işleniyor", Theme.INFO)
            self.bar_fill.config(bg=Theme.PRIMARY)
    
    def set_sub_step(self, step_name, step_num):
        """Video içindeki alt adımı güncelle (her adım için ekstra %2)"""
        if self.video_total > 0:
            # Mevcut video yüzdesi + alt adım
            base = 20 + ((self.video_current - 1) / self.video_total) * 60
            step_addition = (step_num / 7) * (60 / self.video_total)  # 7 alt adım var
            self.percent = base + step_addition
            self._update_bar()
            self.progress_label.config(text=f"%{self.percent:.0f}")
            self.set_status(f"  {step_name}", Theme.INFO)
    
    def phase_connecting(self):
        """Bağlanma aşaması: 0-10%"""
        self.bar_fill.config(bg=Theme.WARNING)
        self.set_percent(5, "🌐 TikTok'a bağlanılıyor...", Theme.WARNING)
    
    def phase_verification(self):
        """Doğrulama aşaması: 10-20%"""
        self.bar_fill.config(bg=Theme.WARNING)
        self.set_percent(15, "🔐 Doğrulama bekleniyor...", Theme.WARNING)
    
    def phase_verified(self):
        """Doğrulama geçildi: 20%"""
        self.bar_fill.config(bg=Theme.SUCCESS)
        self.set_percent(20, "✅ Doğrulama geçildi, videolar taranıyor", Theme.SUCCESS)
    
    def phase_analysis(self):
        """Risk analizi aşaması: 80-95%"""
        self.bar_fill.config(bg=Theme.INFO)
        self.set_percent(85, "🧠 Risk analizi yapılıyor...", Theme.INFO)
    
    def phase_saving(self):
        """Kaydetme aşaması: 95%"""
        self.bar_fill.config(bg=Theme.INFO)
        self.set_percent(95, "💾 Veriler kaydediliyor...", Theme.INFO)
    
    def complete(self, success=True):
        """Tamamlandı: 100%"""
        self._is_pulsing = False
        if success:
            self.bar_fill.config(bg=Theme.SUCCESS)
            self.set_percent(100, "✅ Tamamlandı!", Theme.SUCCESS)
        else:
            self.bar_fill.config(bg=Theme.DANGER)
            self.set_status("❌ Hata oluştu", Theme.DANGER)
    
    def reset(self):
        """Sıfırla"""
        self._is_pulsing = False
        self.percent = 0
        self.video_current = 0
        self.video_total = 0
        self.set_status("Hazır", Theme.TEXT_SECONDARY)
        self.progress_label.config(text="")
        self.bar_fill.config(bg=Theme.PRIMARY)
        self.bar_fill.place(x=0, y=0, relheight=1, width=0)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1200x850")
        self.minsize(1100, 800)
        self.configure(bg=Theme.BG_DARK)
        
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.script_path = os.path.join(self.script_dir, SCRIPT_NAME)
        
        if not os.path.exists(self.script_path):
            messagebox.showerror("Hata", f"{SCRIPT_NAME} bulunamadı.")
            self.destroy()
            return
        
        # Variables
        self.mode_var = tk.StringVar(value="hashtag")
        self.query_var = tk.StringVar(value="")
        self.limit_var = tk.IntVar(value=5)
        self.analyze_var = tk.BooleanVar(value=True)
        self.headless_var = tk.BooleanVar(value=False)
        self.csv_name_var = tk.StringVar(value="tiktok_analyzed.csv")
        
        self.proc = None
        self.running = False
        
        self._apply_theme()
        self._build_ui()
        self._sync_mode_ui()
        self.refresh_csv_list()
    
    def _apply_theme(self):
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except:
            pass
        
        self.style.configure(".", background=Theme.BG_DARK, foreground=Theme.TEXT)
        self.style.configure("TFrame", background=Theme.BG_DARK)
        self.style.configure("TLabel", background=Theme.BG_DARK, foreground=Theme.TEXT)
        
        self.style.configure(
            "TCheckbutton",
            background=Theme.BG_CARD,
            foreground=Theme.TEXT,
            font=(Theme.FONT, 10)
        )
        self.style.map("TCheckbutton", background=[("active", Theme.BG_INPUT)])
        
        self.style.configure(
            "TCombobox",
            fieldbackground=Theme.BG_INPUT,
            background=Theme.BG_CARD,
            foreground=Theme.TEXT,
            padding=8
        )
    
    def _build_ui(self):
        # ==================== HEADER ====================
        header = tk.Frame(self, bg=Theme.BG_DARK)
        header.pack(fill="x", padx=32, pady=(24, 20))
        
        tk.Label(
            header, text="TikTok Risk Analyzer",
            bg=Theme.BG_DARK, fg=Theme.TEXT,
            font=(Theme.FONT, 24, "bold")
        ).pack(side="left")
        
        tk.Label(
            header, text="AI-Powered Analysis",
            bg=Theme.BG_DARK, fg=Theme.TEXT_MUTED,
            font=(Theme.FONT, 12)
        ).pack(side="left", padx=(12, 0), pady=(8, 0))
        
        # ==================== PROGRESS TRACKER ====================
        self.progress = ProgressTracker(self)
        self.progress.pack(fill="x", padx=32, pady=(0, 20))
        
        # ==================== MAIN CONTENT ====================
        main = tk.Frame(self, bg=Theme.BG_DARK)
        main.pack(fill="both", expand=True, padx=32)
        
        # ==================== SETTINGS CARD ====================
        settings_card = tk.Frame(main, bg=Theme.BG_CARD, padx=24, pady=20)
        settings_card.pack(fill="x", pady=(0, 16))
        
        tk.Label(
            settings_card, text="⚙️ Arama Ayarları",
            bg=Theme.BG_CARD, fg=Theme.TEXT,
            font=(Theme.FONT, 12, "bold")
        ).pack(anchor="w", pady=(0, 16))
        
        # Settings row
        settings_row = tk.Frame(settings_card, bg=Theme.BG_CARD)
        settings_row.pack(fill="x")
        
        # Mode
        mode_frame = tk.Frame(settings_row, bg=Theme.BG_CARD)
        mode_frame.pack(side="left", padx=(0, 24))
        
        tk.Label(mode_frame, text="Mod", bg=Theme.BG_CARD, fg=Theme.TEXT_SECONDARY,
                font=(Theme.FONT, 9)).pack(anchor="w")
        
        self.mode_combo = ttk.Combobox(
            mode_frame, textvariable=self.mode_var,
            values=["hashtag", "user"], state="readonly", width=14
        )
        self.mode_combo.pack(pady=(4, 0))
        self.mode_combo.bind("<<ComboboxSelected>>", lambda e: self._sync_mode_ui())
        
        # Query
        query_frame = tk.Frame(settings_row, bg=Theme.BG_CARD)
        query_frame.pack(side="left", fill="x", expand=True, padx=(0, 24))
        
        self.query_label = tk.Label(query_frame, text="Hashtag", bg=Theme.BG_CARD,
                                    fg=Theme.TEXT_SECONDARY, font=(Theme.FONT, 9))
        self.query_label.pack(anchor="w")
        
        self.query_entry = tk.Entry(
            query_frame, textvariable=self.query_var,
            bg=Theme.BG_INPUT, fg=Theme.TEXT, font=(Theme.FONT, 11),
            insertbackground=Theme.TEXT, relief="flat", highlightthickness=1,
            highlightbackground=Theme.BORDER, highlightcolor=Theme.BORDER_FOCUS
        )
        self.query_entry.pack(fill="x", pady=(4, 0), ipady=8)
        
        # Limit
        limit_frame = tk.Frame(settings_row, bg=Theme.BG_CARD)
        limit_frame.pack(side="left", padx=(0, 24))
        
        tk.Label(limit_frame, text="Limit", bg=Theme.BG_CARD, fg=Theme.TEXT_SECONDARY,
                font=(Theme.FONT, 9)).pack(anchor="w")
        
        self.limit_spin = tk.Spinbox(
            limit_frame, from_=1, to=500, textvariable=self.limit_var, width=8,
            bg=Theme.BG_INPUT, fg=Theme.TEXT, font=(Theme.FONT, 11),
            buttonbackground=Theme.BG_CARD, relief="flat", highlightthickness=1,
            highlightbackground=Theme.BORDER, highlightcolor=Theme.BORDER_FOCUS
        )
        self.limit_spin.pack(pady=(4, 0), ipady=6)
        
        # Output
        csv_frame = tk.Frame(settings_row, bg=Theme.BG_CARD)
        csv_frame.pack(side="left")
        
        tk.Label(csv_frame, text="Çıktı Dosyası", bg=Theme.BG_CARD, fg=Theme.TEXT_SECONDARY,
                font=(Theme.FONT, 9)).pack(anchor="w")
        
        self.csv_entry = tk.Entry(
            csv_frame, textvariable=self.csv_name_var, width=24,
            bg=Theme.BG_INPUT, fg=Theme.TEXT, font=(Theme.FONT, 11),
            insertbackground=Theme.TEXT, relief="flat", highlightthickness=1,
            highlightbackground=Theme.BORDER, highlightcolor=Theme.BORDER_FOCUS
        )
        self.csv_entry.pack(fill="x", pady=(4, 0), ipady=8)
        
        # Options row
        opts_row = tk.Frame(settings_card, bg=Theme.BG_CARD)
        opts_row.pack(fill="x", pady=(16, 0))
        
        ttk.Checkbutton(opts_row, text="🧠 Risk Analizi (BERT)", 
                       variable=self.analyze_var).pack(side="left")
        ttk.Checkbutton(opts_row, text="👁️ Gizli Mod", 
                       variable=self.headless_var).pack(side="left", padx=(24, 0))
        
        # ==================== BUTTONS ====================
        btn_row = tk.Frame(main, bg=Theme.BG_DARK)
        btn_row.pack(fill="x", pady=(0, 16))
        
        left_btns = tk.Frame(btn_row, bg=Theme.BG_DARK)
        left_btns.pack(side="left")
        
        self.run_btn = SimpleButton(left_btns, text="▶ Başlat", command=self.on_run, 
                                    style="success", width=120)
        self.run_btn.pack(side="left", padx=(0, 12))
        
        self.stop_btn = SimpleButton(left_btns, text="■ Durdur", command=self.on_stop,
                                     style="danger", width=120)
        self.stop_btn.configure(state="disabled")
        self.stop_btn.pack(side="left", padx=(0, 12))
        
        self.clear_btn = SimpleButton(left_btns, text="🗑 Temizle", command=self.clear_log,
                                      style="ghost", width=110)
        self.clear_btn.pack(side="left")
        
        right_btns = tk.Frame(btn_row, bg=Theme.BG_DARK)
        right_btns.pack(side="right")
        
        self.notebook_btn = SimpleButton(right_btns, text="🚀 NotebookLM",
                                         command=self.open_notebooklm_with_prompt,
                                         style="cyan", width=140)
        self.notebook_btn.pack()
        
        # ==================== CONTENT ====================
        content = tk.Frame(main, bg=Theme.BG_DARK)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)
        
        # CSV Card
        csv_card = tk.Frame(content, bg=Theme.BG_CARD)
        csv_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        
        csv_header = tk.Frame(csv_card, bg=Theme.BG_CARD)
        csv_header.pack(fill="x", padx=16, pady=(16, 12))
        
        tk.Label(csv_header, text="📁 CSV Dosyaları", bg=Theme.BG_CARD, fg=Theme.TEXT,
                font=(Theme.FONT, 11, "bold")).pack(side="left")
        
        csv_list_frame = tk.Frame(csv_card, bg=Theme.BG_CARD)
        csv_list_frame.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        
        self.csv_listbox = tk.Listbox(
            csv_list_frame, bg=Theme.BG_INPUT, fg=Theme.TEXT,
            font=(Theme.FONT, 10), selectbackground=Theme.PRIMARY,
            selectforeground="#ffffff", highlightthickness=0, bd=0,
            activestyle="none"
        )
        self.csv_listbox.pack(side="left", fill="both", expand=True)
        
        csv_scroll = tk.Scrollbar(csv_list_frame, orient="vertical", command=self.csv_listbox.yview)
        csv_scroll.pack(side="right", fill="y")
        self.csv_listbox.configure(yscrollcommand=csv_scroll.set)
        self.csv_listbox.bind("<Double-Button-1>", self.on_csv_double_click)
        
        csv_btns = tk.Frame(csv_card, bg=Theme.BG_CARD)
        csv_btns.pack(fill="x", padx=16, pady=(0, 16))
        
        SimpleButton(csv_btns, text="Aç", command=self.on_csv_double_click, 
                    style="ghost", width=60).pack(side="left", padx=(0, 8))
        SimpleButton(csv_btns, text="Göster", command=self.open_in_finder,
                    style="ghost", width=70).pack(side="left", padx=(0, 8))
        SimpleButton(csv_btns, text="Yenile", command=self.refresh_csv_list,
                    style="ghost", width=70).pack(side="left")
        
        # Log Card
        log_card = tk.Frame(content, bg=Theme.BG_CARD)
        log_card.grid(row=0, column=1, sticky="nsew")
        
        log_header = tk.Frame(log_card, bg=Theme.BG_CARD)
        log_header.pack(fill="x", padx=16, pady=(16, 12))
        
        tk.Label(log_header, text="📋 Canlı Log", bg=Theme.BG_CARD, fg=Theme.TEXT,
                font=(Theme.FONT, 11, "bold")).pack(side="left")
        
        log_frame = tk.Frame(log_card, bg=Theme.BG_CARD)
        log_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        
        self.log_text = tk.Text(
            log_frame, wrap="word", bg=Theme.BG_INPUT, fg=Theme.TEXT_SECONDARY,
            font=(Theme.FONT_MONO, 10), insertbackground=Theme.TEXT,
            highlightthickness=0, bd=0, padx=12, pady=12
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        
        log_scroll = tk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        log_scroll.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=log_scroll.set)
        
        # Log tags
        self.log_text.tag_configure("success", foreground=Theme.SUCCESS)
        self.log_text.tag_configure("error", foreground=Theme.DANGER)
        self.log_text.tag_configure("warning", foreground=Theme.WARNING)
        self.log_text.tag_configure("info", foreground=Theme.INFO)
    
    def _sync_mode_ui(self):
        mode = self.mode_var.get()
        self.query_label.config(text="Hashtag" if mode == "hashtag" else "Kullanıcı Adı")
    
    def log(self, msg: str, tag=None):
        try:
            msg = msg.encode("utf-8", errors="replace").decode("utf-8", errors="replace")
        except:
            pass
        
        # İlerleme durumunu parse et [1/5] gibi
        progress_match = re.search(r'\[(\d+)/(\d+)\]', msg)
        if progress_match:
            current = int(progress_match.group(1))
            total = int(progress_match.group(2))
            self.progress.set_video_progress(current, total)
        
        # Video alt adımlarını yakala ve progress güncelle
        if "video sayfası yükleniyor" in msg.lower():
            self.progress.set_sub_step("📥 Video sayfası yükleniyor", 1)
        elif "caption alınıyor" in msg.lower():
            self.progress.set_sub_step("📝 Caption alınıyor", 2)
        elif "video indiriliyor" in msg.lower():
            self.progress.set_sub_step("⬇️ Video indiriliyor", 3)
        elif "ses transkripti" in msg.lower():
            self.progress.set_sub_step("🎤 Ses transkripti çıkarılıyor", 4)
        elif "ocr metin" in msg.lower():
            self.progress.set_sub_step("🔤 OCR metin taranıyor", 5)
        elif "yüz analizi" in msg.lower():
            self.progress.set_sub_step("👤 Yüz analizi yapılıyor", 6)
        elif "görsel analiz" in msg.lower():
            self.progress.set_sub_step("🎨 Görsel analiz yapılıyor", 7)
        
        # Aşama mesajlarını yakala
        msg_lower = msg.lower()
        if "doğrulama kontrol" in msg_lower:
            self.progress.phase_verification()
        elif "doğrulama geçildi" in msg_lower:
            self.progress.phase_verified()
        elif "risk analizi" in msg_lower and "başlıyor" in msg_lower:
            self.progress.phase_analysis()
        elif "ham veri toplama tamamlandı" in msg_lower:
            self.progress.phase_saving()
        elif "analyzed csv" in msg_lower or "csv oluşturuldu" in msg_lower:
            self.progress.set_percent(98, "💾 CSV kaydedildi", Theme.SUCCESS)
        
        # Tag belirleme
        if tag is None:
            if "✅" in msg:
                tag = "success"
            elif "❌" in msg:
                tag = "error"
            elif "⚠️" in msg:
                tag = "warning"
            elif "ℹ️" in msg or "🔎" in msg:
                tag = "info"
        
        self.log_text.insert("end", msg + "\n", tag if tag else ())
        self.log_text.see("end")
    
    def clear_log(self):
        self.log_text.delete("1.0", "end")
        self.progress.reset()
    
    def refresh_csv_list(self):
        self.csv_listbox.delete(0, "end")
        try:
            for f in sorted(os.listdir(CSV_DIR)):
                if f.lower().endswith(".csv"):
                    self.csv_listbox.insert("end", f"  {f}")
        except Exception as e:
            self.log(f"❌ CSV listeleme hatası: {e}")
    
    def get_selected_csv_path(self):
        sel = self.csv_listbox.curselection()
        if not sel:
            return None
        filename = self.csv_listbox.get(sel[0]).strip()
        return os.path.join(CSV_DIR, filename)
    
    def on_csv_double_click(self, event=None):
        path = self.get_selected_csv_path()
        if not path or not os.path.exists(path):
            messagebox.showerror("Hata", "CSV bulunamadı.")
            return
        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.run(["open", path], check=False)
            else:
                subprocess.run(["xdg-open", path], check=False)
        except Exception as e:
            messagebox.showerror("Hata", f"Açılamadı: {e}")
    
    def open_in_finder(self):
        path = self.get_selected_csv_path()
        if not path or not os.path.exists(path):
            messagebox.showerror("Hata", "CSV bulunamadı.")
            return
        try:
            if sys.platform.startswith("win"):
                subprocess.run(["explorer", "/select,", os.path.normpath(path)], check=False)
            elif sys.platform == "darwin":
                subprocess.run(["open", "-R", path], check=False)
            else:
                subprocess.run(["xdg-open", os.path.dirname(path)], check=False)
        except Exception as e:
            messagebox.showerror("Hata", f"Açılamadı: {e}")
    
    # ======================================================
    # NotebookLM - Profesyonel Entegrasyon
    # ======================================================
    def build_notebooklm_prompt(self, csv_path):
        """Profesyonel ve detaylı analiz promptu oluştur"""
        prompt = """Lütfen aşağıdaki direktiflere göre ekteki TikTok veri setini analiz et.

[ROLÜN]
Sen uzman bir Sosyal Medya Risk Analisti ve Davranış Bilimcisisin. Sadece sayısal verileri değil, içeriğin alt metnini, potansiyel toplumsal etkilerini ve psikolojik yansımalarını da yorumlamalısın.

[VERİ SETİ HAKKINDA]
Bu dosya TikTok videolarının ham verilerini ve Yapay Zeka (BERT) tarafından hesaplanan risk skorlarını içerir.
- caption_risk / transcript_risk / overlay_risk: 0 (Güvenli) ile 1 (Çok Riskli) arasındadır.
- face_detected: Videoda yüz olup olmadığı.
- visual_brightness: Videonun karanlık/aydınlık durumu.

[ANALİZ VE YORUMLAMA GÖREVLERİ]

1. DETAYLI RİSK YORUMLAMASI
Her videoyu sadece "Riskli/Riskli Değil" diye ayırma. "NEDEN Riskli?" sorusuna odaklan.
- Videonun transkripti ve açıklamasını birleştirerek, içerikteki gizli tehlikeleri, intihara meyil, depresyon, şiddet veya yasa dışı özendirme gibi nüansları tespit et.
- Risk skorlarının neden yüksek olduğunu metin içerikleriyle ilişkilendirerek açıkla.

2. BÜTÜNCÜL SKORLAMA
Veri setindeki her bir video için 100 üzerinden bir "Tehlike Puanı" belirle.
- 0-30: Güvenli
- 31-60: Dikkat Edilmeli
- 61-85: Yüksek Risk
- 86-100: Kritik/Acil Durum

3. YÖNETİCİ ÖZETİ VE TRENDLER
- Bu veri setinde genel olarak hangi zararlı temalar öne çıkıyor?
- Kullanılan dil, müzik veya görsel efektlerde (karanlık ortam vb.) ortak bir depresif/zararlı örüntü var mı?
- Bu içeriklerin hedef kitle (özellikle gençler) üzerindeki olası psikolojik etkileri neler olabilir?

[İSTENEN ÇIKTI FORMATI]

Lütfen analizi şu başlıklar altında, okunabilir ve profesyonel bir dille sun:

---
📊 GENEL DURUM RAPORU
[Genel risk seviyesi ve tespit edilen ana tehditlerin özeti]

🔴 KRİTİK VİDEOLAR ANALİZİ (En Yüksek Riskli 5-10 Video)
1. Video URL: ...
   ⚠️ Risk Puanı: .../100
   🧐 Tespit: [Buraya yapay zeka yorumunu, videonun neden tehlikeli olduğunu detaylıca yaz]

📈 DAVRANIŞSAL VE İÇERİK TRENDLERİ
[Veri setindeki ortak zararlı şablonlar, anahtar kelimeler ve görsel tercihler üzerine derinlemesine yorum]

💡 ÖNERİLEN AKSİYONLAR
[İçeriklerin kaldırılması, hesapların incelenmesi veya psikolojik destek yönlendirmesi gibi somut öneriler]
---
"""
        if csv_path:
            import os
            prompt += f"\n(Analiz Edilecek Dosya: {os.path.basename(csv_path)})\n"
        
        return prompt
    
    def export_csv_for_notebooklm(self, csv_path):
        """CSV'yi NotebookLM için TXT formatına dönüştür"""
        if not csv_path or not os.path.exists(csv_path):
            return None
        
        base_name = os.path.splitext(os.path.basename(csv_path))[0]
        out_path = os.path.join(TXT_DIR, f"{base_name}_notebooklm.txt")
        
        raw = open(csv_path, "rb").read()
        text = None
        for enc in ("utf-8-sig", "utf-8", "cp1254", "latin-1"):
            try:
                text = raw.decode(enc)
                break
            except:
                pass
        
        if text:
            text = text.replace("\r\n", "\n")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)
            return out_path
        return None
    
    def open_notebooklm_with_prompt(self):
        """NotebookLM'i aç, prompt kopyala, kullanıcıya rehberlik et"""
        csv_path = self.get_selected_csv_path()
        
        if not csv_path or not os.path.exists(csv_path):
            messagebox.showwarning(
                "⚠️ CSV Seçilmedi",
                "Lütfen önce sol taraftaki listeden bir CSV dosyası seçin."
            )
            return
        
        # Prompt oluştur
        prompt = self.build_notebooklm_prompt(csv_path)
        
        # TXT dosyası oluştur
        txt_path = self.export_csv_for_notebooklm(csv_path)
        
        if not txt_path:
            messagebox.showerror("Hata", "TXT dosyası oluşturulamadı.")
            return
        
        # Prompt'u panoya kopyala
        try:
            self.clipboard_clear()
            self.clipboard_append(prompt)
            self.update()
        except Exception as e:
            messagebox.showerror("Hata", f"Panoya kopyalanamadı: {e}")
            return
        
        # TXT klasörünü aç (kolay erişim için)
        try:
            if sys.platform.startswith("win"):
                subprocess.run(["explorer", "/select,", os.path.normpath(txt_path)], check=False)
        except:
            pass
        
        # NotebookLM'i aç
        try:
            webbrowser.open_new_tab(NOTEBOOKLM_URL)
        except Exception as e:
            messagebox.showerror("Hata", f"NotebookLM açılamadı: {e}")
            return
        
        # Kullanıcıya adım adım talimat ver
        instructions = f"""✅ NotebookLM Hazırlandı!

📋 PROMPT PANODA (Ctrl+V ile yapıştır)

📁 VERİ DOSYASI:
{os.path.basename(txt_path)}
(Klasör açıldı, dosyayı sürükle-bırak yapabilirsin)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 ADIMLAR:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ NotebookLM'de "Create New" tıkla

2️⃣ Açılan klasörden TXT dosyasını
   sürükle-bırak ile yükle

3️⃣ Sohbet kutusuna Ctrl+V ile
   promptu yapıştır

4️⃣ Enter'a bas ve analizi bekle!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        
        messagebox.showinfo("🚀 NotebookLM Rehberi", instructions)
    
    # ======================================================
    # Run / Stop
    # ======================================================
    def build_cmd(self):
        mode = self.mode_var.get().strip()
        query = self.query_var.get().strip()
        
        if not query:
            raise ValueError("Query boş olamaz.")
        
        csv_name = self.csv_name_var.get().strip() or "tiktok_analyzed.csv"
        if not csv_name.lower().endswith(".csv"):
            csv_name += ".csv"
        
        return [
            sys.executable, self.script_path,
            "--mode", mode,
            "--query", query,
            "--limit", str(int(self.limit_var.get())),
            "--analyze", "1" if self.analyze_var.get() else "0",
            "--headless", "1" if self.headless_var.get() else "0",
            "--out_csv", os.path.join(CSV_DIR, csv_name),
        ]
    
    def on_run(self):
        if self.running:
            return
        
        try:
            cmd = self.build_cmd()
        except Exception as e:
            messagebox.showerror("Hata", str(e))
            return
        
        self.running = True
        self.run_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        # Progress başlat - bağlanma aşaması
        self.progress.phase_connecting()
        
        self.log("━" * 50)
        self.log(f"🚀 Başlatılıyor: {self.query_var.get()} ({self.limit_var.get()} video)")
        self.log("━" * 50)
        
        threading.Thread(target=self._run_process, args=(cmd,), daemon=True).start()
    
    def _run_process(self, cmd):
        try:
            env = os.environ.copy()
            if sys.platform.startswith("win"):
                env["PYTHONIOENCODING"] = "utf-8"
                env["PYTHONUTF8"] = "1"
            
            self.proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace",
                bufsize=1, cwd=self.script_dir, env=env
            )
            
            if self.proc.stdout:
                for line in self.proc.stdout:
                    clean = line.rstrip("\n\r")
                    self.after(0, lambda l=clean: self.log(l))
            
            code = self.proc.wait()
            if code == 0:
                self.after(0, lambda: self.progress.complete(True))
                self.after(0, lambda: self.log("✅ İşlem başarıyla tamamlandı!"))
            else:
                self.after(0, lambda: self.progress.complete(False))
                self.after(0, lambda: self.log(f"❌ Hata kodu: {code}"))
        
        except Exception as e:
            self.after(0, lambda: self.progress.complete(False))
            self.after(0, lambda: self.log(f"❌ Hata: {e}"))
        
        finally:
            self.proc = None
            self.running = False
            self.after(0, self._reset_ui)
    
    def _reset_ui(self):
        self.run_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.refresh_csv_list()
    
    def on_stop(self):
        if self.proc and self.running:
            try:
                self.proc.terminate()
                self.progress.set_status("🛑 Durduruldu", Theme.WARNING)
                self.log("🛑 İşlem durduruldu.")
            except Exception as e:
                self.log(f"❌ Durdurma hatası: {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
