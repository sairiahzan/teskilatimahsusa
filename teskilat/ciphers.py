# Şifreleme Yöntemleri ve Algoritmaları

# -*- coding: utf-8 -*-
# algoritmalar tek yerde dursun; UI’dan bağımsız

import base64

# alfabe filtresi
def only_alpha(s):
    return ''.join(ch for ch in s if ch.isalpha())

# ——— Sezar ———
def caesar_shift_char(ch, s):
    if 'A' <= ch <= 'Z': return chr((ord(ch) - 65 + s) % 26 + 65)
    if 'a' <= ch <= 'z': return chr((ord(ch) - 97 + s) % 26 + 97)
    return ch

def caesar_encrypt(t, s): return ''.join(caesar_shift_char(c, s) for c in t)
def caesar_decrypt(t, s): return caesar_encrypt(t, -s)

# ——— Mors ———
MORSE = {'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..','0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.'}
REV_MORSE = {v: k for k, v in MORSE.items()}

def morse_encrypt(t):
    return ' / '.join(' '.join(MORSE.get(c.upper(), c) for c in w) for w in t.split(' '))

def morse_decrypt(c):
    return ' '.join(''.join(REV_MORSE.get(tok, tok) for tok in w.split()) for w in c.split(' / '))

# ——— Vigenère ———
def vigenere_encrypt(text, key):
    key = only_alpha(key).upper()
    if not key: return text
    res = []; i = 0
    for ch in text:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            shift = ord(key[i % len(key)]) - 65
            res.append(chr((ord(ch) - ord(base) + shift) % 26 + ord(base))); i += 1
        else:
            res.append(ch)
    return ''.join(res)

def vigenere_decrypt(text, key):
    key = only_alpha(key).upper()
    if not key: return text
    res = []; i = 0
    for ch in text:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            shift = ord(key[i % len(key)]) - 65
            res.append(chr((ord(ch) - ord(base) - shift) % 26 + ord(base))); i += 1
        else:
            res.append(ch)
    return ''.join(res)

# ——— Atbash ———
def atbash_transform(t):
    out = []
    for ch in t:
        if 'A' <= ch <= 'Z': out.append(chr(155 - ord(ch)))
        elif 'a' <= ch <= 'z': out.append(chr(219 - ord(ch)))
        else: out.append(ch)
    return ''.join(out)

# ——— Rail Fence ———
def rail_fence_encrypt(t, rails):
    if rails < 2: return t
    fence = [[] for _ in range(rails)]; r = 0; d = 1
    for ch in t:
        fence[r].append(ch); r += d
        if r == 0 or r == rails - 1: d *= -1
    return ''.join(''.join(row) for row in fence)

def rail_fence_decrypt(ct, rails):
    if rails < 2: return ct
    pat = []; r = 0; d = 1
    for _ in ct:
        pat.append(r); r += d
        if r == 0 or r == rails - 1: d *= -1
    counts = [pat.count(i) for i in range(rails)]
    slices = []; i = 0
    for c in counts: slices.append(list(ct[i:i+c])); i += c
    idx = [0] * rails; out = []
    for r in pat: out.append(slices[r][idx[r]]); idx[r] += 1
    return ''.join(out)

# ——— Base64 ———
def b64_encode(t):
    return base64.b64encode(t.encode('utf-8')).decode('ascii')

def b64_decode(t):
    try:
        return base64.b64decode(t.encode('ascii')).decode('utf-8', errors='replace')
    except Exception:
        try:
            return base64.b64decode(t).decode('utf-8', errors='replace')
        except Exception as e:
            return f"[Hata] {e}"

# ——— Playfair ———
def only_alpha_upper(s): 
    return ''.join(ch for ch in s.upper() if 'A' <= ch <= 'Z')

def pf_prepare_key(key):
    k = []; seen = set(); key = only_alpha_upper(key).replace('J','I')
    for ch in key + 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if ch not in seen and ch != 'J' and 'A' <= ch <= 'Z':
            seen.add(ch); k.append(ch)
    return [k[i*5:(i+1)*5] for i in range(5)]

def pf_find(g, ch):
    for r in range(5):
        for c in range(5):
            if g[r][c] == ch: return r, c

def pf_prepare_text(s, pad='X'):
    s = only_alpha_upper(s).replace('J','I'); out = []; i = 0
    while i < len(s):
        a = s[i]; b = s[i+1] if i+1 < len(s) else pad
        if a == b: out.append(a + pad); i += 1
        else: out.append(a + b); i += 2
    if out and len(out[-1]) == 1: out[-1] += pad
    return out

def playfair_encrypt(pt, key):
    g = pf_prepare_key(key); res = []
    for a, b in pf_prepare_text(pt):
        ra, ca = pf_find(g, a); rb, cb = pf_find(g, b)
        if ra == rb: res.append(g[ra][(ca+1)%5] + g[rb][(cb+1)%5])
        elif ca == cb: res.append(g[(ra+1)%5][ca] + g[(rb+1)%5][cb])
        else: res.append(g[ra][cb] + g[rb][ca])
    return ''.join(res)

def playfair_decrypt(ct, key):
    g = pf_prepare_key(key); res = []
    for i in range(0, len(ct), 2):
        if i+1 >= len(ct): break
        a, b = ct[i:i+2]; ra, ca = pf_find(g, a); rb, cb = pf_find(g, b)
        if ra == rb: res.append(g[ra][(ca-1)%5] + g[rb][(cb-1)%5])
        elif ca == cb: res.append(g[(ra-1)%5][ca] + g[(rb-1)%5][cb])
        else: res.append(g[ra][cb] + g[rb][ca])
    return ''.join(res)

# ——— Sütunar ———
def col_order(key):
    pairs = sorted([(ch, i) for i, ch in enumerate(key)])
    order = [None] * len(key); rank = 0
    for ch, i in pairs: order[i] = rank; rank += 1
    return order

def columnar_encrypt(text, key):
    if not key: return text
    key = ''.join(ch for ch in key if not ch.isspace())
    cols = len(key); rows = (len(text) + cols - 1) // cols if cols else 0
    grid = [[''] * cols for _ in range(rows)]; i = 0
    for r in range(rows):
        for c in range(cols):
            if i < len(text): grid[r][c] = text[i]; i += 1
    order = col_order(key); out = []
    for rank in range(cols):
        c = order.index(rank)
        for r in range(rows): out.append(grid[r][c])
    return ''.join(out)

def columnar_decrypt(cipher, key):
    if not key: return cipher
    key = ''.join(ch for ch in key if not ch.isspace())
    cols = len(key); rows = (len(cipher) + cols - 1) // cols if cols else 0
    order = col_order(key); grid = [[''] * cols for _ in range(rows)]; i = 0
    for rank in range(cols):
        c = order.index(rank)
        for r in range(rows):
            if i < len(cipher): grid[r][c] = cipher[i]; i += 1
    out = []
    for r in range(rows):
        for c in range(cols): out.append(grid[r][c])
    return ''.join(out)

# ——— Affine ———
def egcd(a, b):
    if a == 0: return (b, 0, 1)
    g, y, x = egcd(b % a, a); return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1: raise ValueError("a ile 26 aralarında asal olmalı")
    return x % m

def affine_encrypt(text, a, b):
    out = []
    for ch in text:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            x = ord(ch) - ord(base); y = (a * x + b) % 26
            out.append(chr(y + ord(base)))
        else: out.append(ch)
    return ''.join(out)

def affine_decrypt(text, a, b):
    a_inv = modinv(a, 26); out = []
    for ch in text:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            y = ord(ch) - ord(base); x = (a_inv * (y - b)) % 26
            out.append(chr(x + ord(base)))
        else: out.append(ch)
    return ''.join(out)

# ——— XOR ———
def xor_crypt(text, key):
    if not key: return text
    kb = key.encode('utf-8'); tb = text.encode('utf-8')
    out = bytearray()
    for i, b in enumerate(tb): out.append(b ^ kb[i % len(kb)])
    return base64.b64encode(bytes(out)).decode('ascii')

def xor_decrypt(b64text, key):
    try:
        raw = base64.b64decode(b64text)
    except Exception as e:
        return f"[Hata] Geçersiz Base64/XOR: {e}"
    if not key: return raw.decode('utf-8', errors='replace')
    kb = key.encode('utf-8'); out = bytearray()
    for i, b in enumerate(raw): out.append(b ^ kb[i % len(kb)])
    return bytes(out).decode('utf-8', errors='replace')