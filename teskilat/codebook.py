# miftah encode/decode

# -*- coding: utf-8 -*-
# sözcük→kod sözlüğü ile basit eşleme

def codebook_encode(text, mapping):
    def m(tok):
        if not tok: return tok
        return mapping.get(tok, mapping.get(tok.lower(), mapping.get(tok.capitalize(), tok)))
    return ' '.join(m(t) for t in text.split())

def codebook_decode(text, mapping):
    return ' '.join(mapping.get(t, t) for t in text.split())