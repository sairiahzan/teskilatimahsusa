# Toplu İşlem Ekranı

# -*- coding: utf-8 -*-
import os, shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ..io_helpers import read_text_from_path, write_text_same_type
from .. import ciphers as C
from ..codebook import codebook_encode, codebook_decode

# yöntem listesi – UI tarafı bundan besleniyor
METHODS = [
    "Sezar","Mors","Vigenère","Atbash","Rail Fence",
    "Playfair","Sütunar","Base64","Affine","XOR","Miftah Defteri"
]

# ekranı kur
def build_bulk(root):
    b = tk.Frame(root.content, bg=root.bg)
    root.screens['bulk'] = b

    root._btn(b, "← Ana Menü", lambda: root.show('home')).pack(anchor='e', padx=8, pady=8)
    tk.Label(b, text="Toplu İşlem", bg=root.bg, fg=root.ink,
             font=('Helvetica', 18, 'bold')).pack(anchor='w', padx=8, pady=(0, 6))

    # dosya listesi
    files_card = tk.Frame(b, bg=root.panel, highlightbackground=root.box, highlightthickness=2)
    files_card.pack(fill='both', expand=True, padx=8, pady=(0, 8))

    ctr = tk.Frame(files_card, bg=root.panel); ctr.pack(fill='x', padx=10, pady=(10,6))
    tk.Label(ctr, text="Dosyalar", bg=root.panel, fg=root.ink,
             font=('Helvetica', 12, 'bold')).pack(side='left')
    btns = tk.Frame(ctr, bg=root.panel); btns.pack(side='right')
    ttk.Button(btns, text="Ekle", style="Mahsusa.TButton", command=lambda: _bulk_add_files(root)).pack(side='left', padx=4)
    ttk.Button(btns, text="Kaldır", style="Mahsusa.TButton", command=lambda: _bulk_remove_selected(root)).pack(side='left', padx=4)
    ttk.Button(btns, text="Temizle", style="Mahsusa.TButton", command=lambda: _bulk_clear_files(root)).pack(side='left', padx=4)

    list_wrap = tk.Frame(files_card, bg=root.panel); list_wrap.pack(fill='both', expand=True, padx=10, pady=(0,10))
    root.bulk_list = tk.Listbox(list_wrap, selectmode='extended', bg=root.text_bg, fg=root.text_fg, relief='flat')
    root.bulk_list.pack(side='left', fill='both', expand=True)
    sb = ttk.Scrollbar(list_wrap, orient='vertical', command=root.bulk_list.yview)
    sb.pack(side='right', fill='y')
    root.bulk_list.config(yscrollcommand=sb.set)

    # alt satır – çıkış klasörü, yöntem ve parametreler
    bottom = tk.Frame(b, bg=root.bg); bottom.pack(fill='x', padx=8, pady=8)

    out_row = tk.Frame(bottom, bg=root.bg); out_row.pack(fill='x')
    tk.Label(out_row, text="Çıkış Klasörü:", bg=root.bg, fg=root.ink).pack(side='left', padx=(0,8))
    root.bulk_outdir = tk.StringVar(value="")
    ttk.Entry(out_row, textvariable=root.bulk_outdir, width=80).pack(side='left', fill='x', expand=True)
    ttk.Button(out_row, text="Seç", style="Mahsusa.TButton", command=lambda: _bulk_choose_outdir(root)).pack(side='left', padx=6)

    method_row = tk.Frame(bottom, bg=root.bg); method_row.pack(fill='x', pady=(8,0))
    tk.Label(method_row, text="Yöntem:", bg=root.bg, fg=root.ink).pack(side='left', padx=(0,8))
    root.bulk_method = tk.StringVar(value="Sezar")
    ttk.Combobox(method_row, textvariable=root.bulk_method, values=METHODS,
                 width=24, state="readonly", style="Mahsusa.TCombobox").pack(side='left')
    mode = tk.Frame(method_row, bg=root.bg); mode.pack(side='left', padx=12)
    root.bulk_is_encrypt = tk.BooleanVar(value=True)
    ttk.Radiobutton(mode, text="Şifrele", variable=root.bulk_is_encrypt, value=True, style="Mahsusa.TRadiobutton").pack(side='left')
    ttk.Radiobutton(mode, text="Çöz",    variable=root.bulk_is_encrypt, value=False, style="Mahsusa.TRadiobutton").pack(side='left')

    root.bulk_params = tk.Frame(bottom, bg=root.bg); root.bulk_params.pack(fill='x', pady=(6,0))
    _bulk_bind_params(root)

    ttk.Button(bottom, text="Başlat", style="Mahsusa.TButton",
               command=lambda: _bulk_start(root)).pack(anchor='e', pady=(8,0))

# dosya seçimleri
def _bulk_add_files(root):
    paths = filedialog.askopenfilenames(
        title="Dosya Ekle",
        filetypes=[
            ("Desteklenen", "*.txt *.pdf *.doc *.docx *.md *.rtf"),
            ("Metin", "*.txt *.md *.rtf"),
            ("PDF", "*.pdf"),
            ("Word", "*.doc *.docx"),
            ("Tümü", "*.*"),
        ]
    )
    for p in paths or []:
        root.bulk_list.insert('end', p)

def _bulk_remove_selected(root):
    sel = list(root.bulk_list.curselection()); sel.reverse()
    for i in sel: root.bulk_list.delete(i)

def _bulk_clear_files(root):
    root.bulk_list.delete(0, 'end')

def _bulk_choose_outdir(root):
    d = filedialog.askdirectory(title="Çıkış Klasörü Seç")
    if d: root.bulk_outdir.set(d)

# param bağla
def _bulk_bind_params(root):
    try:
        root.bulk_method.trace_add('write', lambda *_: _bulk_refresh_params(root))
    except Exception:
        root.bulk_method.trace('w', lambda *_: _bulk_refresh_params(root))
    _bulk_refresh_params(root)

# param arayüzü
def _bulk_refresh_params(root):
    for w in root.bulk_params.winfo_children(): w.destroy()
    if not hasattr(root,'bulk_sz'): root.bulk_sz = tk.IntVar(value=3)
    if not hasattr(root,'bulk_vk'): root.bulk_vk = tk.StringVar(value="")
    if not hasattr(root,'bulk_rf'): root.bulk_rf = tk.IntVar(value=3)
    if not hasattr(root,'bulk_pf'): root.bulk_pf = tk.StringVar(value="")
    if not hasattr(root,'bulk_cl'): root.bulk_cl = tk.StringVar(value="")
    if not hasattr(root,'bulk_af_a'): root.bulk_af_a = tk.IntVar(value=5)
    if not hasattr(root,'bulk_af_b'): root.bulk_af_b = tk.IntVar(value=8)
    if not hasattr(root,'bulk_xr'): root.bulk_xr = tk.StringVar(value="")

    def add(lbl, widget, pad=(0,10)):
        tk.Label(root.bulk_params, text=lbl, bg=root.bg, fg=root.ink).pack(side='left', padx=(0,6))
        widget.pack(side='left', padx=pad)
        return widget

    m = root.bulk_method.get()
    if m == "Sezar":
        add('Kaydırma:', ttk.Spinbox(root.bulk_params, from_=-25, to=25, width=6, textvariable=root.bulk_sz))
    elif m == "Vigenère":
        add('Anahtar:', ttk.Entry(root.bulk_params, textvariable=root.bulk_vk, width=24, style="Mahsusa.TEntry"))
    elif m == "Rail Fence":
        add('Ray:', ttk.Spinbox(root.bulk_params, from_=2, to=10, width=6, textvariable=root.bulk_rf))
    elif m == "Playfair":
        add('Anahtar:', ttk.Entry(root.bulk_params, textvariable=root.bulk_pf, width=24, style="Mahsusa.TEntry"))
    elif m == "Sütunar":
        add('Anahtar:', ttk.Entry(root.bulk_params, textvariable=root.bulk_cl, width=24, style="Mahsusa.TEntry"))
    elif m == "Affine":
        add('a:', ttk.Spinbox(root.bulk_params, from_=1, to=25, width=5, textvariable=root.bulk_af_a), pad=(0,6))
        add('b:', ttk.Spinbox(root.bulk_params, from_=0, to=25, width=5, textvariable=root.bulk_af_b))
    elif m == "XOR":
        add('Anahtar:', ttk.Entry(root.bulk_params, textvariable=root.bulk_xr, width=24, style="Mahsusa.TEntry"))

    info = {
        'Mors': 'Kelime ayırıcı: " / "',
        'Base64': 'Çıktı ASCII; çözüm UTF-8',
        'Miftah Defteri': 'Önce kod defterini yükleyin/düzenleyin',
    }.get(m)
    if info:
        tk.Label(root.bulk_params, text=info, bg=root.bg, fg=root.ink).pack(side='left', padx=6)

# dönüşüm çekirdeği
def _bulk_transform_text(root, text):
    enc = root.bulk_is_encrypt.get()
    m = root.bulk_method.get()
    try:
        if m == 'Sezar':
            s = int(root.bulk_sz.get()); 
            return C.caesar_encrypt(text, s) if enc else C.caesar_decrypt(text, s)
        if m == 'Mors':
            return C.morse_encrypt(text) if enc else C.morse_decrypt(text)
        if m == 'Vigenère':
            k = root.bulk_vk.get(); 
            return C.vigenere_encrypt(text, k) if enc else C.vigenere_decrypt(text, k)
        if m == 'Atbash':
            return C.atbash_transform(text)
        if m == 'Rail Fence':
            r = int(root.bulk_rf.get()); 
            return C.rail_fence_encrypt(text, r) if enc else C.rail_fence_decrypt(text, r)
        if m == 'Playfair':
            k = root.bulk_pf.get(); 
            return C.playfair_encrypt(text, k) if enc else C.playfair_decrypt(text, k)
        if m == 'Sütunar':
            k = root.bulk_cl.get(); 
            return C.columnar_encrypt(text, k) if enc else C.columnar_decrypt(text, k)
        if m == 'Base64':
            return C.b64_encode(text) if enc else C.b64_decode(text)
        if m == 'Affine':
            a = int(root.bulk_af_a.get()); b = int(root.bulk_af_b.get())
            return C.affine_encrypt(text, a, b) if enc else C.affine_decrypt(text, a, b)
        if m == 'XOR':
            k = root.bulk_xr.get(); 
            return C.xor_crypt(text, k) if enc else C.xor_decrypt(text, k)
        if m == 'Miftah Defteri':
            if not hasattr(root, 'codebook') or not root.codebook:
                raise RuntimeError('Kod defteri yüklü değil.')
            return codebook_encode(text, root.codebook) if enc else codebook_decode(text, root.codebook)
        return text
    except Exception as e:
        return f"[Hata] {e}"

# yürüt
def _bulk_start(root):
    n = root.bulk_list.size()
    if n == 0:
        messagebox.showwarning(root.APP_NAME, "Önce dosya ekleyin.")
        return
    outdir = root.bulk_outdir.get().strip()
    if not outdir:
        messagebox.showwarning(root.APP_NAME, "Çıkış klasörü seçilmedi.")
        return

    ok = fail = skipped = 0
    for i in range(n):
        src = root.bulk_list.get(i)
        try:
            if not os.path.isfile(src):
                raise FileNotFoundError(src)

            base = os.path.basename(src)
            name, ext = os.path.splitext(base)
            ext_l = ext.lower()
            dest = os.path.join(outdir, f"{name}_proc{ext}")

            text = read_text_from_path(src)

            # metin çıkaramıyorsak atlama stratejisi (korumalı/resim tabanlı PDF söz konusu)
            if text is None or (ext_l in ('.pdf', '.doc', '.docx') and (not isinstance(text, str) or not text.strip())):
                try:
                    shutil.copy2(src, dest)
                    skipped += 1
                    continue
                except Exception:
                    fail += 1
                    continue

            out_text = _bulk_transform_text(root, text)
            _final, _fallback = write_text_same_type(dest, out_text)
            ok += 1
        except Exception:
            fail += 1

    msg = f"Tamamlandı. Başarılı: {ok}, Atlanan: {skipped}, Hatalı: {fail}\n(Metin çıkarılamayan PDF/DOCX dosyaları kopyalandı.)"
    messagebox.showinfo(root.APP_NAME, msg)