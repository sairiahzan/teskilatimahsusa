# Renk Paleti ve TKK stilleri

# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

# koyu palet – göz yormasın
def set_palette(root, mode='dark'):
    if mode == 'light':
        bg = "#f7f8fb"; panel = "#ffffff"; ink = "#0f172a"; box = "#e5e7eb"; accent = "#8b6a3d"
        text_bg = "#ffffff"; text_fg = "#0f172a"; btn = "#2a3548"
    else:
        bg = "#0b0f14"; panel = "#18202c"; ink = "#e8eaef"; box = "#243147"; accent = "#c9a469"
        text_bg = "#0f141c"; text_fg = "#e8eaef"; btn = "#2a3548"

    # referans olsun diye renkleri köke işliyorum
    root.bg, root.panel, root.ink, root.box, root.accent = bg, panel, ink, box, accent
    root.text_bg, root.text_fg, root.btn = text_bg, text_fg, btn
    root.configure(bg=bg)

# ttk stiller – sade ve tutarlı
def style_init(root):
    s = ttk.Style()
    try:
        s.theme_use('clam')  # stabil
    except:
        pass

    # buton – düz, koyu
    s.configure("Mahsusa.TButton",
                background="#2a3548",
                foreground=root.ink,
                padding=(14, 8),
                borderwidth=1)
    s.map("Mahsusa.TButton",
          background=[("active", "#33425a"), ("pressed", "#3a4c66")],
          relief=[("pressed", "sunken"), ("!pressed", "flat")])

    # seçim bileşenleri – arka planı temayla uyumlu
    s.configure("Mahsusa.TCheckbutton", background=root.bg, foreground=root.ink)
    s.map("Mahsusa.TCheckbutton", background=[("active", root.bg)])

    s.configure("Mahsusa.TCombobox",
                fieldbackground=root.panel,
                background=root.panel,
                foreground=root.ink)
    s.map("Mahsusa.TCombobox", fieldbackground=[("readonly", root.panel)])

    s.configure("Mahsusa.TRadiobutton", background=root.bg, foreground=root.ink)
    s.configure("Mahsusa.TEntry", fieldbackground=root.panel, foreground=root.ink)