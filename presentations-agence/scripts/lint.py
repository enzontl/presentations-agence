#!/usr/bin/env python3
"""Détecteur statique des tics (references/tics.md), avant même le rendu.

  python lint.py mon-deck/deck.html                # rapport, code de sortie 1 s'il y a un BLOQUANT
  python lint.py mon-deck/deck.html --corriger     # répare aussi les espaces insécables
  python lint.py gabarits/... --exemples           # tolère le texte d'exemple des gabarits

Il lit le HTML et les feuilles de style locales, sans navigateur. Il attrape ce qu'un rendu
ne montre pas (notes vides, superlatifs, image répétée, texte de gabarit oublié) et ce
qu'on peut repérer dans le code (dégradé violet, emojis, titres étiquettes, chiffres égaux).
Ce qu'il ne voit pas se juge sur les captures : rendu.py, puis references/critique.md.
"""
import argparse
import colorsys
import pathlib
import re
import sys
import unicodedata
from html.parser import HTMLParser

TITRES_ETIQUETTES = {"contexte", "introduction", "conclusion", "notre solution", "la solution", "le probleme", "problematique",
                     "merci", "merci !", "questions", "questions ?", "des questions ?", "sommaire", "agenda", "resultats",
                     "objectifs", "nos objectifs", "methodologie", "chiffres cles", "a propos", "l'equipe", "notre equipe", "synthese"}
SUPERLATIFS = ["revolutionnaire", "innovant", "innovante", "disruptif", "disruptive", "unique en son genre", "incroyable",
               "exceptionnel", "exceptionnelle", "le meilleur", "la meilleure", "game changer", "game-changer", "best-in-class", "leader du marche"]
EXEMPLES = ["Kōri", "Valmont", "données fictives", "test du skill"]
TEXTURES = ("papier", "sombre", "journal", "kraft")
TITRE_SEL = {"h1", "h2"}
TITRE_CLS = {"title", "titre", "headline", "h1", "h2", "giant", "masthead", "poster"}
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF✅❌⭐✨]")
NOMBRE = re.compile(r"^[+−\-]?\d[\d\s  ,.]*\s?(%|€|k|h|cts|pts|M€|Md€)?\.?$")


def norm(s):
    s = unicodedata.normalize("NFD", s.lower().strip())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


class Slide:
    def __init__(self, n):
        self.n, self.texts, self.titres, self.imgs, self.notes = n, [], [], [], ""
        self.stamps, self.li, self.construire, self.section = 0, [], False, None
        self.nums = []


class P(HTMLParser):
    VOID = {"img", "br", "hr", "meta", "link", "input", "source", "use", "path", "line", "rect", "circle"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.slides, self.stack, self.cur, self.depth = [], [], None, 0
        self.inline_css = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = set((a.get("class") or "").split())
        if a.get("style"):
            self.inline_css.append(a["style"])
        if tag == "section" and "slide" in cls and self.cur is None:
            self.cur = Slide(len(self.slides) + 1)
            self.cur.construire = "a-construire" in cls
            self.cur.section = a.get("data-section")
            self.slides.append(self.cur)
            self.depth = 0
        if self.cur is None:
            return
        if tag == "img" and a.get("src"):
            self.cur.imgs.append(a["src"])
        if cls & {"stamp", "tampon"}:
            self.cur.stamps += 1
        if tag == "ul" or tag == "ol":
            self.cur.li.append(0)
        if tag == "li" and self.cur.li:
            self.cur.li[-1] += 1
        if tag not in self.VOID:
            m = re.search(r"font(?:-size)?\s*:[^;]*?(\d+)px", a.get("style", ""))
            self.stack.append(dict(tag=tag, cls=cls, notes="notes" in cls, titre=tag in TITRE_SEL or bool(cls & TITRE_CLS),
                                   key=(tag, " ".join(sorted(cls)), m.group(1) if m else ""), text=""))
            if tag == "section":
                self.depth += 1

    def handle_startendtag(self, tag, attrs):
        # balise auto-fermante (<use/>, <img/>) : on la lit sans l'empiler
        a = dict(attrs)
        if self.cur is not None and tag == "img" and a.get("src"):
            self.cur.imgs.append(a["src"])
        if a.get("style"):
            self.inline_css.append(a["style"])

    def handle_endtag(self, tag):
        if self.cur is None or not self.stack or tag in self.VOID:
            return
        if not any(e["tag"] == tag for e in self.stack):
            return
        while self.stack[-1]["tag"] != tag:
            self._close(self.stack.pop())
        self._close(self.stack.pop(), tag)

    def _close(self, el, tag=None):
        tag = tag or el["tag"]
        t = re.sub(r"\s+", " ", el["text"]).strip()
        if el["titre"] and t:
            self.cur.titres.append(t)
        if t and NOMBRE.match(t) and not el["notes"] and len(re.sub(r"\D", "", t)) >= 1:
            self.cur.nums.append(el["key"])
        if self.stack:
            self.stack[-1]["text"] += " " + el["text"]
        if tag == "section" and self.cur is not None:
            self.depth -= 1
            if self.depth == 0:
                self.cur = None
                self.stack = []

    def handle_data(self, data):
        if self.cur is None or not self.stack:
            return
        self.stack[-1]["text"] += data
        if any(e["notes"] for e in self.stack):
            self.cur.notes += data
        elif data.strip() and self.stack[-1]["tag"] not in ("script", "style"):
            self.cur.texts.append(data)


def violets(css):
    out = []
    for g in re.findall(r"(?:linear|radial|conic)-gradient\(([^;{}]*)\)", css):
        for h in re.findall(r"#([0-9a-fA-F]{6})\b", g):
            r, gg, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
            hue, li, sat = colorsys.rgb_to_hls(r, gg, b)
            if 0.66 <= hue <= 0.84 and sat > 0.35 and 0.15 < li < 0.85:
                out.append("#" + h)
    return out


ESP = re.compile(r"(\d) (?=[%€])|(\w) (?=[:;?!»])|« (?=\w)")


def corriger_texte(t):
    t = re.sub(r"(\d) (\d{3})\b", lambda m: m.group(1) + " " + m.group(2), t)
    t = re.sub(r"(\d) (%|€|h\b|k\b|cl\b|cts|pts)", lambda m: m.group(1) + " " + m.group(2), t)
    t = re.sub(r" ([?!:;»])", lambda m: " " + m.group(1), t)
    return t.replace("« ", "« ")


def corriger(path):
    s = path.read_text()
    out, pos, skip = [], 0, False
    for m in re.finditer(r"<[^>]+>", s):
        txt = s[pos:m.start()]
        out.append(txt if skip else corriger_texte(txt))
        tag = m.group(0).lower()
        if tag.startswith(("<script", "<style")):
            skip = True
        if tag.startswith(("</script", "</style")):
            skip = False
        out.append(m.group(0))
        pos = m.end()
    out.append(s[pos:])
    path.write_text("".join(out))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("--corriger", action="store_true", help="répare les espaces insécables dans le texte")
    ap.add_argument("--exemples", action="store_true", help="tolère le texte d'exemple des gabarits")
    a = ap.parse_args()
    path = pathlib.Path(a.html)
    if a.corriger:
        corriger(path)
    src = path.read_text()
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S))
    for href in re.findall(r"<link[^>]+href=['\"]([^'\"]+\.css)['\"]", src):
        p = (path.parent / href)
        if p.exists() and "fonts" not in href:
            css += "\n" + p.read_text()
    p = P()
    p.feed(src)
    css += "\n" + "\n".join(p.inline_css)

    res = {}  # n -> list of (niveau, message)
    def add(n, niv, msg):
        res.setdefault(n, []).append((niv, msg))

    for c in sorted(set(violets(css))):
        add(0, "BLOQUANT", f"dégradé violet ou indigo ({c}) : couleurs de l'univers du style, en aplat")
    if re.search(r"background-clip\s*:\s*text", css):
        add(0, "BLOQUANT", "texte en dégradé (background-clip:text) : encre pleine")
    flous = len(re.findall(r"box-shadow\s*:[^;]*\d+px\s+\d+px\s+([1-9]\d|[5-9])px", css))
    if flous > 3:
        add(0, "ALERTE", f"{flous} ombres floues : un aplat voisin ou rien, sauf si le style les prévoit")
    ronds = len(re.findall(r"border-radius\s*:\s*(1[6-9]|[2-9]\d)px", css))
    if ronds > 3:
        add(0, "ALERTE", f"{ronds} coins très arrondis : garder les angles de l'objet réel")

    vus = {}
    for s in p.slides:
        txt = " ".join(s.texts)
        tout = txt + " " + s.notes
        if s.construire:
            add(s.n, "BLOQUANT", "section .a-construire : layout pas encore construit")
        if EMOJI.search(txt):
            add(s.n, "BLOQUANT", "emoji dans la slide : des mots ou une vraie image")
        if re.search(r"lorem ipsum|\[image|placeholder|à compléter|xxx", norm(txt)):
            add(s.n, "BLOQUANT", "texte de remplissage (lorem, [image], à compléter)")
        if not a.exemples:
            restes = [e for e in EXEMPLES if e.lower() in tout.lower()]
            if restes:
                add(s.n, "BLOQUANT", f"texte d'exemple de gabarit oublié : {', '.join(restes)}")
        for t in s.titres:
            if norm(t).rstrip(" .") in TITRES_ETIQUETTES:
                add(s.n, "BLOQUANT", f"titre étiquette « {t} » : une phrase qui affirme la conclusion")
            if len(t) > 90:
                add(s.n, "ALERTE", f"titre de {len(t)} caractères : viser moins de 70")
        if not s.titres:
            add(s.n, "ALERTE", "aucun titre repérable (h1, h2, .title, .headline…) : le test des titres seuls sera vide")
        if s.stamps > 1:
            add(s.n, "ALERTE", f"{s.stamps} tampons : un seul par slide")
        for k in s.li:
            if k > 5:
                add(s.n, "ALERTE", f"liste de {k} puces : une idée par slide, le reste en notes")
        groupes = {}
        for key in s.nums:
            groupes[key] = groupes.get(key, 0) + 1
        tailles = [int(k[2]) for k in s.nums if k[2]]
        heros = max(tailles) if tailles else 0
        for key, k in groupes.items():
            if k >= 3 and key[2] and int(key[2]) >= 60 and int(key[2]) == heros:
                add(s.n, "ALERTE", f"{k} chiffres de même taille ({key[2]} px) : un héros et des subordonnés, dans un objet du style")
        if re.search(r"\d{3}|\d\s?%|€", txt) and not re.search(r"source|donnees|d'apres|selon|fictive", norm(tout)):
            add(s.n, "ALERTE", "chiffres sans source visible ni dans les notes")
        sup = [w for w in SUPERLATIFS if re.search(r"\b" + w + r"\b", norm(txt))]
        if sup:
            add(s.n, "ALERTE", f"superlatif sans preuve : {', '.join(sup)}")
        if len(s.notes.strip()) < 20:
            add(s.n, "ALERTE", "notes de l'orateur vides ou trop courtes")
        esp = len(ESP.findall(txt))
        if esp:
            add(s.n, "ALERTE", f"{esp} espace(s) simple(s) avant % € : ; ? ! (lint.py --corriger)")
        for img in s.imgs:
            if img.startswith("data:") or any(t in img for t in TEXTURES):
                continue
            if img in vus:
                add(s.n, "BLOQUANT", f"image déjà utilisée slide {vus[img]:02d} : {img}")
            else:
                vus[img] = s.n

    nb = sum(1 for v in res.values() for niv, _ in v if niv == "BLOQUANT")
    na = sum(1 for v in res.values() for niv, _ in v if niv == "ALERTE")
    for n in sorted(res):
        print("Deck" if n == 0 else f"Slide {n:02d}")
        for niv, msg in res[n]:
            print(f"  {niv:8} {msg}")
    print(f"\n{len(p.slides)} slides · {nb} bloquant(s) · {na} alerte(s)" + ("" if res else " · rien à signaler"))
    print("Corriger chaque BLOQUANT. Garder une ALERTE seulement avec une raison en une phrase. Voir references/tics.md.")
    sys.exit(1 if nb else 0)


if __name__ == "__main__":
    main()
