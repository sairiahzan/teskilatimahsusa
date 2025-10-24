from threading import Thread
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Dahili modüller
from .theme import set_palette, style_init
from . import ciphers as C
from .screens.home import build_home
from .screens.generic_cipher import cipher_screen
from .screens.miftah import build_miftah
from .screens.bulk import build_bulk


class App(tk.Tk):
    APP_NAME = "Teşkilat-ı Mahsusa"

    def __init__(self):
        super().__init__()

        # ------------------ PENCERE ------------------
        self.title(self.APP_NAME)
        self.geometry("1300x850")
        self.minsize(1100, 700)
        self.icon_path = "/Users/sairiahzan/Documents/Teşkilat-ı Mahsusa/Teşkilat-ı Mahsusa Logo.png"
        self.logo_img = None  # logo tek sefer yüklenip önbelleğe alınır

        # ------------------ TEMA ------------------
        set_palette(self, "dark")
        style_init(self)

        # ------------------ ÇERÇEVELER ------------------
        self.screens = {}
        self.current_screen = None
        self._build_header()   # ← ÜST BAR: Logo solda, başlık ortada
        self._build_footer()   # ← ALT BAR: “Arda Yiğit - Hazani” ortada
        self._build_content()  # ← İçerik alanı

        # ------------------ EKRANLAR ------------------
        build_home(self)               # ana menü kartları
        self._build_cipher_screens()   # tüm şifreleme ekranları
        build_miftah(self)             # miftah defteri ekranı (yalnız çöz)
        build_bulk(self)               # toplu işlem ekranı

        # Başlangıç ekranı
        self.show("home")

    # ============================================================
    #  ÜST BAR / HEADER  —  LOGO SOLDa, BAŞLIK ÜSTTE ORTADA
    # ============================================================
    def _build_header(self):
        header = tk.Frame(self, bg=self.panel, height=110)
        header.pack(fill="x", side="top")

        # grid: [logo] [başlık-orta] [boş]
        header.grid_columnconfigure(0, weight=0)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=0)

        # Logo (sol üst) – tek sefer yükle
        logo_path = self.icon_path  # …/teskilat/Teşkilat-ı Mahsusa Logo.png
        if os.path.exists(logo_path):
            try:
                from PIL import Image, ImageTk
                if not self.logo_img:
                    img = Image.open(logo_path).resize((95, 95))
                    self.logo_img = ImageTk.PhotoImage(img)
                tk.Label(header, image=self.logo_img, bg=self.panel)\
                  .grid(row=0, column=0, sticky="w", padx=10, pady=6)
            except Exception:
                tk.Label(header, text="[Logo]", bg=self.panel, fg=self.ink)\
                  .grid(row=0, column=0, sticky="w", padx=10, pady=6)
        else:
            tk.Label(header, text="[Logo bulunamadı]", bg=self.panel, fg=self.ink)\
              .grid(row=0, column=0, sticky="w", padx=10, pady=6)

        # Başlık (üstte ortalı, kolon-1)
        tk.Label(
            header,
            text=self.APP_NAME,
            font=("Helvetica", 28, "bold"),
            fg=self.accent,
            bg=self.panel
        ).grid(row=0, column=1, sticky="nw", padx=50, pady=30)

    # ============================================================
    #  ALT BAR / FOOTER  —  İMZA ALTA ORTALI
    # ============================================================
    def _build_footer(self):
        footer = tk.Frame(self, bg=self.panel, height=30)
        footer.pack(fill="x", side="bottom")
        tk.Label(
            footer,
            text="Arda Yiğit - Hazani",
            font=("Helvetica", 10),
            fg=self.ink,
            bg=self.panel
        ).pack(anchor="center", pady=4)

    # ============================================================
    #  İÇERİK ALANI (EKRANLARIN BARINDIĞI KISIM)
    # ============================================================
    def _build_content(self):
        self.content = tk.Frame(self, bg=self.bg)
        self.content.pack(expand=True, fill="both")

    # ============================================================
    #  GÖRSEL YARDIMCILAR (KART & BUTON)
    # ============================================================
    def soft_card(self, parent, w=260, h=260):
        f = tk.Frame(
            parent,
            bg=self.panel,
            width=w,
            height=h,
            highlightbackground=self.box,
            highlightthickness=2,
            bd=0
        )
        f.pack_propagate(False)
        return f

    def _btn(self, parent, text, cmd, instant=None):
        # Navigasyonlar anlık, ağır işler kuyruktan
        if instant is None:
            # metne göre sezgisel: geri/ana menü tuşlarını anında çalıştır
            instant = bool(text and ("Ana Menü" in text or text.strip().startswith("←")))
        if instant:
            return ttk.Button(parent, text=text, command=cmd, style="Mahsusa.TButton")

        def on_click():
            btn.config(state='disabled')
            # UI'ı kilitlemeden işi sıraya koy
            self.after_idle(lambda: (cmd(), btn.config(state='normal')))
        btn = ttk.Button(parent, text=text, command=on_click, style="Mahsusa.TButton")
        return btn

    # ============================================================
    #  SAYFA GEÇİŞİ
    # ============================================================
    def show(self, name):
        # hızlı ekran değişimi: sadece aktif ekranı gizle/göster
        if getattr(self, 'current_screen', None) == name:
            return
        if getattr(self, 'current_screen', None) in self.screens:
            self.screens[self.current_screen].pack_forget()
        if name in self.screens:
            self.screens[name].pack(expand=True, fill="both")
            self.current_screen = name
            self.update_idletasks()

    # ============================================================
    #  ŞİFRELEME EKRANLARINI TANIMLAMA
    # ============================================================
    def _build_cipher_screens(self):
        # Sezar
        cipher_screen(
            self, self.content, "sezar", "Sezar Şifrelemesi",
            "Her harfi sabit bir kaydırma kadar öteler; noktalama ve boşluklar korunur.",
            lambda t: C.caesar_encrypt(t, 3),
            lambda t: C.caesar_decrypt(t, 3)
        )

        # Mors
        cipher_screen(
            self, self.content, "mors", "Mors Alfabesi",
            "Harfleri nokta ve çizgi dizilerine çevirir; sözcükleri ' / ' ile ayırır.",
            lambda t: C.morse_encrypt(t),
            lambda t: C.morse_decrypt(t)
        )

        # Vigenère
        cipher_screen(
            self, self.content, "vigenere", "Vigenère Şifrelemesi",
            "Anahtar kelimeye göre çok alfabeli kaydırma yapar; tekrarı kırmak zordur.",
            lambda t: C.vigenere_encrypt(t, "ANAHTAR"),
            lambda t: C.vigenere_decrypt(t, "ANAHTAR")
        )

        # Atbash
        cipher_screen(
            self, self.content, "atbash", "Atbash Şifrelemesi",
            "Alfabeyi tersine çevirerek eşler; aynı işlemle çözülür.",
            lambda t: C.atbash_transform(t),
            lambda t: C.atbash_transform(t)
        )

        # Rail Fence
        cipher_screen(
            self, self.content, "rail", "Rail Fence Şifrelemesi",
            "Metni zikzak biçiminde yazar, satır satır okuyarak karıştırır.",
            lambda t: C.rail_fence_encrypt(t, 3),
            lambda t: C.rail_fence_decrypt(t, 3)
        )

        # Playfair
        cipher_screen(
            self, self.content, "playfair", "Playfair Şifrelemesi",
            "5×5 tablo ile ikili harf bloklarını dönüştürür; J/I birleştirilir.",
            lambda t: C.playfair_encrypt(t, "TEŞKİLAT"),
            lambda t: C.playfair_decrypt(t, "TEŞKİLAT")
        )

        # Sütunar
        cipher_screen(
            self, self.content, "columnar", "Sütunar Şifrelemesi",
            "Anahtar sırasına göre sütunları yeniden dizer; boşluk korunabilir.",
            lambda t: C.columnar_encrypt(t, "İTTİHAT"),
            lambda t: C.columnar_decrypt(t, "İTTİHAT")
        )

        # Base64
        cipher_screen(
            self, self.content, "base64", "Base64 Kodlama",
            "İkilik veriyi ASCII güvenli metne dönüştürür; ağ aktarımı için idealdir.",
            lambda t: C.b64_encode(t),
            lambda t: C.b64_decode(t)
        )

        # Affine
        cipher_screen(
            self, self.content, "affine", "Affine Şifrelemesi",
            "Her harfi a·x + b (mod 26) formülüyle dönüştürür; a ve 26 aralarında asal olmalıdır.",
            lambda t: C.affine_encrypt(t, 5, 8),
            lambda t: C.affine_decrypt(t, 5, 8)
        )

        # XOR
        cipher_screen(
            self, self.content, "xor", "XOR Şifrelemesi",
            "Her karakteri anahtar baytlarıyla XOR’lar; Base64 ile metinleşir.",
            lambda t: C.xor_crypt(t, "SIR"),
            lambda t: C.xor_decrypt(t, "SIR")
        )
