#!/usr/bin/env python3
"""Traitement des images d'un deck (PIL + numpy).

Traiter une photo :
  python images.py traiter SRC OUT --taille 1920x1080 --preset chaud --sombre bas
    --taille   LxH exacte du layout (1920x1080, 960x1080, 1920x600, 720x1080...)
    --cadre    centre du recadrage en fractions, ex. 0.5,0.3 (défaut 0.5,0.5)
    --preset   chaud | studio | neutre | presse | trame | mode | doc | pixel
    --sombre   bas | haut | gauche | droite | aucun (dégradé sous le texte)
    --force    intensité du dégradé, 0 à 1 (défaut selon le preset)
    --encres   pour trame et pixel : deux couleurs hex, ex. FF48B0,0078BF
    --papier   couleur du papier pour presse, trame, pixel (hex)
    --grain    force du grain (défaut selon le preset)

Générer une texture :
  python images.py texture papier|sombre|journal|kraft OUT [--couleur EFE3C8] [--taille 1920x1080]

Le tirage aléatoire a une graine fixe : deux exécutions donnent la même image.
"""
import argparse
import sys

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

RNG = np.random.default_rng(7)

PRESETS = {
    # sat, contraste, chaud(r,b), fondu des noirs, grain, sombre par défaut, force
    "chaud":  dict(sat=.85, con=1.08, warm=(1.03, .95), fade=0,  grain=6, sombre="bas",   force=.75),
    "studio": dict(sat=.80, con=1.12, warm=(.98, 1.04), fade=0,  grain=5, sombre="bas",   force=.80),
    "neutre": dict(sat=.72, con=1.04, warm=(.99, 1.02), fade=6,  grain=2, sombre="aucun", force=0),
    "mode":   dict(sat=.92, con=.97,  warm=(1.01, .99), fade=14, grain=3, sombre="aucun", force=0),
    "doc":    dict(sat=.78, con=1.02, warm=(1.0, 1.0),  fade=8,  grain=2, sombre="aucun", force=0),
}


def hexrgb(h):
    h = h.strip().lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=float)


def taille(s):
    w, h = s.lower().split("x")
    return int(w), int(h)


def crop_to(im, w, h, cx=.5, cy=.5):
    """Recadre au ratio exact autour du centre (cx, cy), puis redimensionne."""
    r = w / h
    W, H = im.size
    if W / H > r:
        nw = int(H * r)
        x0 = int(min(max(cx * W - nw / 2, 0), W - nw))
        im = im.crop((x0, 0, x0 + nw, H))
    else:
        nh = int(W / r)
        y0 = int(min(max(cy * H - nh / 2, 0), H - nh))
        im = im.crop((0, y0, W, y0 + nh))
    return im.resize((w, h), Image.LANCZOS)


def degrade(a, cote, force):
    """Assombrit progressivement vers un côté, pour poser du texte dessus."""
    if cote == "aucun" or force <= 0:
        return a
    h, w = a.shape[:2]
    n = h if cote in ("bas", "haut") else w
    t = np.linspace(0, 1, n)
    if cote in ("haut", "gauche"):
        t = t[::-1]
    g = 1 - force * np.clip((t - .35) / .65, 0, 1) ** 1.5
    return a * (g[:, None, None] if cote in ("bas", "haut") else g[None, :, None])


def grain(a, force):
    if force <= 0:
        return a
    return a + RNG.normal(0, force, a.shape[:2])[..., None]


def etalonner(im, p):
    im = ImageEnhance.Color(im.convert("RGB")).enhance(p["sat"])
    im = ImageEnhance.Contrast(im).enhance(p["con"])
    a = np.asarray(im).astype(float)
    a[..., 0] *= p["warm"][0]
    a[..., 2] *= p["warm"][1]
    if p["fade"]:
        a = p["fade"] + a * (255 - p["fade"]) / 255
    return a


def presse(im, papier="EDE6D6", force=.0, cote="aucun", g=7):
    """Noir et blanc de journal : contraste franc, noirs jamais purs, encre posée sur le papier."""
    l = np.asarray(ImageEnhance.Contrast(im.convert("L")).enhance(1.25)).astype(float) / 255
    l = degrade(l[..., None], cote, force)[..., 0]
    pap = hexrgb(papier)
    encre = np.array([28, 26, 24], float)
    a = encre + (pap - encre) * l[..., None]
    return grain(a, g)


def trame(im, encres=("FF48B0", "0078BF"), papier="F2EBDD", pas=9, decalage=(6, 4)):
    """Bichromie tramée façon risographie : deux trames de points à angles différents,
    encres en surimpression (multiplication) et léger défaut de repérage."""
    w, h = im.size
    rgb = np.asarray(im.convert("RGB")).astype(float) / 255
    lum = rgb @ np.array([.3, .59, .11])
    lum = np.asarray(Image.fromarray((lum * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.2))).astype(float) / 255
    lum = np.clip((lum - .08) / .84, 0, 1)
    # encre 1 : les ombres et les tons moyens ; encre 2 : les tons chauds et les ombres profondes
    # on garde du papier dans les hautes lumières : c'est lui qui fait la lumière d'une affiche
    cov1 = np.clip((1 - lum - .12) / .88, 0, 1) ** 1.35
    chaud = np.clip(rgb[..., 0] - rgb[..., 2] + .25, 0, 1)
    cov2 = np.clip((1 - lum) * .5 + chaud * .3 - .25, 0, .75)

    yy, xx = np.mgrid[0:h, 0:w].astype(float)

    def points(cov, angle, dx=0, dy=0):
        a = np.deg2rad(angle)
        x, y = xx - dx, yy - dy
        u = x * np.cos(a) + y * np.sin(a)
        v = -x * np.sin(a) + y * np.cos(a)
        fu = (u % pas) - pas / 2
        fv = (v % pas) - pas / 2
        d = np.sqrt(fu ** 2 + fv ** 2)
        c = np.roll(np.roll(cov, dy, 0), dx, 1)
        r = pas * .72 * np.sqrt(c)
        return np.clip(r - d + .5, 0, 1)  # bord légèrement adouci

    m1 = points(cov1, 45)
    m2 = points(cov2, 15, *decalage)
    pap = hexrgb(papier) / 255
    e1, e2 = hexrgb(encres[0]) / 255, hexrgb(encres[1]) / 255
    out = pap * (1 - m1[..., None] * (1 - e1)) * (1 - m2[..., None] * (1 - e2))
    out = out * 255
    return grain(out, 4)


def pixel(im, encres=("111111",), papier="FFFFFF", taille_px=2):
    """Tramage 1 bit (Floyd-Steinberg) façon écran ancien. Une encre sur un papier."""
    w, h = im.size
    l = ImageOps.autocontrast(im.convert("L"), cutoff=1)
    l = ImageEnhance.Brightness(l).enhance(1.25)
    petit = ImageEnhance.Contrast(l).enhance(1.15).resize((w // taille_px, h // taille_px), Image.LANCZOS)
    bit = petit.convert("1").resize((w, h), Image.NEAREST)
    m = 1 - np.asarray(bit).astype(float)
    pap, enc = hexrgb(papier), hexrgb(encres[0])
    return pap + (enc - pap) * m[..., None]


def texture(kind, w, h, couleur=None):
    base = {"papier": "EFE3C8", "sombre": "111111", "journal": "EDE6D6", "kraft": "C9A97A"}[kind]
    c = hexrgb(couleur or base)
    a = np.ones((h, w, 3)) * c
    # taches basse fréquence
    amp = {"papier": 7, "sombre": 5, "journal": 6, "kraft": 12}[kind]
    low = RNG.normal(0, 1, (h // 60 + 2, w // 60 + 2))
    low = np.asarray(Image.fromarray(((low - low.min()) / (np.ptp(low) + 1e-9) * 255).astype("uint8")).resize((w, h), Image.BICUBIC)).astype(float) / 255 - .5
    a += (low * amp * 2)[..., None]
    # fibres (papier, kraft)
    if kind in ("papier", "kraft", "journal"):
        f = RNG.normal(0, 1, (h, w))
        f = np.asarray(Image.fromarray(((f - f.min()) / np.ptp(f) * 255).astype("uint8")).filter(ImageFilter.BoxBlur(1)).resize((w, h))).astype(float) / 255 - .5
        a += (f * (10 if kind == "kraft" else 5))[..., None]
    # vignettage doux
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a *= (1 - np.clip(d - .55, 0, 1) * (.35 if kind == "sombre" else .10))[..., None]
    return grain(a, 7 if kind == "sombre" else 4)


def save(a, out):
    im = Image.fromarray(np.clip(a, 0, 255).astype("uint8"))
    if out.lower().endswith((".jpg", ".jpeg")):
        im.save(out, quality=90, optimize=True, progressive=True)
    else:
        im.save(out)
    print(f"ok {out} {im.size[0]}x{im.size[1]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("traiter")
    t.add_argument("src"); t.add_argument("out")
    t.add_argument("--taille", default="1920x1080")
    t.add_argument("--cadre", default="0.5,0.5")
    t.add_argument("--preset", default="chaud", choices=list(PRESETS) + ["presse", "trame", "pixel"])
    t.add_argument("--sombre", default=None, choices=["bas", "haut", "gauche", "droite", "aucun"])
    t.add_argument("--force", type=float, default=None)
    t.add_argument("--encres", default=None)
    t.add_argument("--papier", default=None)
    t.add_argument("--grain", type=float, default=None)
    x = sub.add_parser("texture")
    x.add_argument("kind", choices=["papier", "sombre", "journal", "kraft"]); x.add_argument("out")
    x.add_argument("--couleur", default=None)
    x.add_argument("--taille", default="1920x1080")
    a = ap.parse_args()

    if a.cmd == "texture":
        w, h = taille(a.taille)
        save(texture(a.kind, w, h, a.couleur), a.out)
        return

    w, h = taille(a.taille)
    cx, cy = (float(v) for v in a.cadre.split(","))
    im = crop_to(Image.open(a.src).convert("RGB"), w, h, cx, cy)
    enc = tuple(a.encres.split(",")) if a.encres else None

    if a.preset == "presse":
        arr = presse(im, a.papier or "EDE6D6", a.force or 0, a.sombre or "aucun", 7 if a.grain is None else a.grain)
    elif a.preset == "trame":
        arr = trame(im, enc or ("FF48B0", "0078BF"), a.papier or "F2EBDD")
    elif a.preset == "pixel":
        arr = pixel(im, enc or ("111111",), a.papier or "FFFFFF")
    else:
        p = dict(PRESETS[a.preset])
        arr = etalonner(im, p)
        arr = degrade(arr, a.sombre or p["sombre"], p["force"] if a.force is None else a.force)
        arr = grain(arr, p["grain"] if a.grain is None else a.grain)
    save(arr, a.out)


if __name__ == "__main__":
    sys.exit(main())
