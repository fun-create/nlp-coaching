# -*- coding: utf-8 -*-
"""PWA用アイコン（icon-192.png / icon-512.png）を生成。アプリの表紙と同じコンパスマーク。"""
from PIL import Image, ImageDraw

def make(size, out):
    s = 4; S = size * s
    im = Image.new("RGBA", (S, S), (0x2f, 0x8f, 0x7f, 255))
    d = ImageDraw.Draw(im)
    cx = cy = S / 2
    r = S * 0.30; w = int(S * 0.035)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255, 255), width=w)
    dm = S * 0.20; dw = S * 0.07
    d.polygon([(cx, cy - dm), (cx + dw, cy), (cx, cy + dm), (cx - dw, cy)], fill=(255, 255, 255, 255))
    im = im.resize((size, size), Image.LANCZOS)
    im.save(out, optimize=True)
    print("wrote", out)

if __name__ == "__main__":
    make(192, "icon-192.png")
    make(512, "icon-512.png")
