# Miftah Ekranı (Yalnız Çözme Tuşu)

# -*- coding: utf-8 -*-
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ..codebook import codebook_decode, codebook_encode

# miftah defteri ekranı – yalnız çözüm var
def build_miftah(root):
    m = tk.Frame(root.content, bg=root.bg)
    root.screens['miftah'] = m

    root._btn(m, "← Ana Menü", lambda: root.show('home'), instant=True).pack(anchor='e', padx=8, pady=8)
    tk.Label(m, text="Miftah Defteri", bg=root.bg, fg=root.ink,
             font=('Helvetica', 18, 'bold')).pack(anchor='w', padx=8, pady=(0, 6))

    top = tk.Frame(m, bg=root.bg)
    top.pack(fill='x', padx=8, pady=6)

    # yan menü – dosya yükle / kaydet / düzenle
    tools = tk.Frame(top, bg=root.bg)
    tools.pack(side='right')
    root._btn(tools, "Yükle (JSON)", lambda: _cb_load(root)).pack(anchor='w', pady=3, padx=4)
    root._btn(tools, "Kaydet (JSON)", lambda: _cb_save(root)).pack(anchor='w', pady=3, padx=4)
    root._btn(tools, "Düzenle", lambda: _cb_edit(root)).pack(anchor='w', pady=3, padx=4)

    # giriş–çıkış metin kutuları
    io = tk.Frame(m, bg=root.bg)
    io.pack(expand=True, fill='both', padx=8, pady=6)
    left = tk.Frame(io, bg=root.bg)
    right = tk.Frame(io, bg=root.bg)
    left.pack(side='left', expand=True, fill='both', padx=6)
    right.pack(side='right', expand=True, fill='both', padx=6)

    tk.Label(left, text="Girdi", bg=root.bg, fg=root.ink,
             font=('Helvetica', 12, 'bold')).pack(anchor='w')
    root.miftah_in = tk.Text(left, height=15, wrap='word',
                             bg=root.text_bg, fg=root.text_fg,
                             insertbackground=root.text_fg)
    root.miftah_in.pack(expand=True, fill='both')

    tk.Label(right, text="Çıktı", bg=root.bg, fg=root.ink,
             font=('Helvetica', 12, 'bold')).pack(anchor='w')
    root.miftah_out = tk.Text(right, height=15, wrap='word',
                              bg=root.text_bg, fg=root.text_fg,
                              insertbackground=root.text_fg)
    root.miftah_out.pack(expand=True, fill='both')

    act = tk.Frame(m, bg=root.bg)
    act.pack(fill='x', padx=8, pady=6)

    # yalnız çözüm butonu
    root._btn(act, "Çöz", lambda: _miftah_dec(root)).pack(side='right', padx=6)


# json yükleme
def _cb_load(root):
    p = filedialog.askopenfilename(title="Kod Defteri (JSON) Aç",
                                   filetypes=[("JSON", "*.json"), ("Tümü", "*.*")])
    if not p:
        return
    try:
        with open(p, 'r', encoding='utf-8') as f:
            root.codebook = json.load(f)
        messagebox.showinfo(root.APP_NAME, "Kod defteri yüklendi.")
    except Exception as e:
        messagebox.showerror(root.APP_NAME, f"Hata: {e}")


# json kaydetme
def _cb_save(root):
    if not hasattr(root, 'codebook') or not root.codebook:
        messagebox.showwarning(root.APP_NAME, "Kaydedilecek kod defteri yok.")
        return
    p = filedialog.asksaveasfilename(title="Kod Defteri Kaydet",
                                     defaultextension=".json",
                                     filetypes=[("JSON", "*.json")])
    if p:
        try:
            with open(p, 'w', encoding='utf-8') as f:
                json.dump(root.codebook, f, ensure_ascii=False, indent=2)
            messagebox.showinfo(root.APP_NAME, "Kaydedildi.")
        except Exception as e:
            messagebox.showerror(root.APP_NAME, f"Hata: {e}")


# json düzenleme
def _cb_edit(root):
    top = tk.Toplevel(root, bg=root.bg)
    top.title("Kod Defteri Düzenle")
    txt = tk.Text(top, width=64, height=24, bg=root.text_bg,
                  fg=root.text_fg, insertbackground=root.text_fg)
    txt.pack(expand=True, fill='both', padx=8, pady=8)

    current = getattr(root, 'codebook', {
        "vatan": "31", "namus": "72", "teşkilat": "99",
        "31": "vatan", "72": "namus", "99": "teşkilat"
    })
    txt.insert('1.0', json.dumps(current, ensure_ascii=False, indent=2))

    def save_close():
        try:
            data = json.loads(txt.get('1.0', 'end-1c'))
            if not isinstance(data, dict):
                raise ValueError("Sözlük olmalı.")
            root.codebook = data
            top.destroy()
            messagebox.showinfo(root.APP_NAME, "Kod defteri güncellendi.")
        except Exception as e:
            messagebox.showerror(root.APP_NAME, f"Hata: {e}")

    ttk.Button(top, text="Kaydet", command=save_close, style="Mahsusa.TButton").pack(pady=6)


# çözüm
def _miftah_dec(root):
    if not hasattr(root, 'codebook') or not root.codebook:
        messagebox.showwarning(root.APP_NAME, "Önce bir kod defteri yükleyin.")
        return
    text = root.miftah_in.get('1.0', 'end-1c')
    try:
        res = codebook_decode(text, root.codebook)
    except Exception as e:
        messagebox.showerror(root.APP_NAME, f"Hata: {e}")
        return
    root.miftah_out.delete('1.0', 'end')
    root.miftah_out.insert('1.0', res)
