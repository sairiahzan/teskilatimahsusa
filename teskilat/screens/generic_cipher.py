# ortak şifre ekranı

# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

# ortak şablon – tüm şifre ekranları aynı iskeleti kullansın
def cipher_screen(root, container, name, title, desc, enc, dec, build_params=None):
    frm = tk.Frame(container, bg=root.bg)
    root.screens[name] = frm

    head = tk.Frame(frm, bg=root.bg)
    head.pack(fill='x', padx=8, pady=(0, 8))
    root._btn(head, "← Ana Menü", lambda: root.show('home')).pack(side='right', padx=8, pady=8)
    tk.Label(head, text=title, bg=root.bg, fg=root.ink,
             font=('Helvetica', 18, 'bold')).pack(anchor='w', padx=8, pady=(8, 0))

    body = tk.Frame(frm, bg=root.bg)
    body.pack(expand=True, fill='both', padx=8, pady=8)

    top = tk.Frame(body, bg=root.bg)
    top.pack(fill='x', padx=6, pady=6)
    tk.Label(top, text=desc, bg=root.bg, fg=root.ink,
             font=('Helvetica', 10), wraplength=1100,
             justify='left').pack(anchor='w', side='left')

    if build_params:
        params = tk.Frame(top, bg=root.bg)
        params.pack(side='right')
        build_params(params)

    io = tk.Frame(body, bg=root.bg)
    io.pack(expand=True, fill='both', padx=6, pady=6)

    left = tk.Frame(io, bg=root.bg);  left.pack(side='left',  expand=True, fill='both', padx=6)
    right = tk.Frame(io, bg=root.bg); right.pack(side='right', expand=True, fill='both', padx=6)

    tk.Label(left, text="Girdi", bg=root.bg, fg=root.ink,
             font=('Helvetica', 12, 'bold')).pack(anchor='w')
    inp = tk.Text(left, height=15, wrap='word',
                  bg=root.text_bg, fg=root.text_fg,
                  insertbackground=root.text_fg)
    inp.pack(expand=True, fill='both')

    tk.Label(right, text="Çıktı", bg=root.bg, fg=root.ink,
             font=('Helvetica', 12, 'bold')).pack(anchor='w')
    out = tk.Text(right, height=15, wrap='word',
                  bg=root.text_bg, fg=root.text_fg,
                  insertbackground=root.text_fg)
    out.pack(expand=True, fill='both')

    btns = tk.Frame(body, bg=root.bg)
    btns.pack(anchor='e', padx=6, pady=6)

    # tek tuşla dönüştür – minimal gecikme
    root._btn(btns, "Şifrele",
              lambda: (out.delete('1.0', 'end'),
                       out.insert('1.0', enc(inp.get('1.0', 'end-1c'))))
              ).pack(side='right', padx=6)

    root._btn(btns, "Çöz",
              lambda: (out.delete('1.0', 'end'),
                       out.insert('1.0', dec(inp.get('1.0', 'end-1c'))))
              ).pack(side='right', padx=6)

    return frm