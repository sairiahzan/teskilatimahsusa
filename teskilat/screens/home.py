# Ana Menü Kartları
# -*- coding: utf-8 -*-
import tkinter as tk

# ana menü – kart ızgarası
def build_home(root):
    home = tk.Frame(root.content, bg=root.bg)
    root.screens['home'] = home

    grid = tk.Frame(home, bg=root.bg)
    grid.pack(expand=True, fill='both', padx=8)

    COLS = 4   # satırı doldursun
    CARD = 240 # kare kart
    PAD = 10
    for c in range(COLS):
        grid.columnconfigure(c, weight=1)

    tiles = [
        ("Sezar",         "Her harfi sabit bir kaydırma kadar öteler; noktalama ve boşluklar korunur.",      lambda: root.show('sezar')),
        ("Mors",          "Harfleri nokta/çizgi dizilerine çevirir; sözcükleri ' / ' ile ayırır.",           lambda: root.show('mors')),
        ("Vigenère",      "Anahtar kelimeye göre çok alfabeli kaydırma; tekrar paternlerini kırar.",         lambda: root.show('vigenere')),
        ("Atbash",        "Alfabeyi tersine eşler; aynı işlemle çözülür (simetrik).",                         lambda: root.show('atbash')),
        ("Rail Fence",    "Zikzak yaz, satır satır topla; düzen bozulur, çözmede desen geri kurulur.",       lambda: root.show('rail')),
        ("Playfair",      "5×5 tabloluyla ikililer (diagrams); J/I birleştirme, tekrar bölme kuralları.",    lambda: root.show('playfair')),
        ("Sütunar",       "Anahtar sırasına göre kolonları yeniden dizer; boşluk/noktalama korunabilir.",    lambda: root.show('columnar')),
        ("Base64",        "İkilik veriyi ASCII güvenli metne çevirir; ağ/dosya taşıma için pratik.",         lambda: root.show('base64')),
        ("Affine",        "a·x+b (mod 26) dönüşümü; a ile 26 aralarında asal olmak zorunda.",                lambda: root.show('affine')),
        ("XOR",           "Baytları anahtarla XOR’lar; çıktı Base64 ile okunur hale gelir.",                  lambda: root.show('xor')),
        ("Miftah Defteri","Kelime→kod sözlüğüyle kodla/çöz; JSON defteri düzenlenebilir (yalnız çöz aktif).",lambda: root.show('miftah')),
        ("Toplu İşlem",   "Çoklu dosyayı seçilen yöntemle dönüştürür; çıktıyı klasöre `_proc` ekleyerek yazar.", lambda: root.show('bulk')),
    ]

    for i, (title, desc, cmd) in enumerate(tiles):
        r, c = divmod(i, COLS)
        card = root.soft_card(grid, CARD, CARD)
        card.grid(row=r, column=c, padx=PAD, pady=PAD, sticky='nsew')

        tk.Label(card, text=title, bg=root.panel, fg=root.ink,
                 font=('Helvetica', 13, 'bold')).pack(anchor='w', padx=12, pady=(12, 4))
        tk.Label(card, text=desc, bg=root.panel, fg=root.ink,
                 font=('Helvetica', 10), wraplength=CARD-36,
                 justify='left').pack(anchor='w', padx=12, pady=(0, 8))
        tk.Frame(card, bg=root.panel).pack(expand=True, fill='both')
        root._btn(card, "Aç", cmd).pack(anchor='e', padx=12, pady=(0, 10))
