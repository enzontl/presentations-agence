#!/usr/bin/env python3
"""Télécharge des polices Google Fonts en local et écrit fonts.css.

  python polices.py "Anton" "Playfair Display:ital,wght@0,400;1,400" "Inter:wght@400;600;800" --out fonts/

Chaque argument suit la syntaxe de l'API css2 de Google Fonts (famille, puis axes).
Seuls les sous-ensembles latin et latin-ext sont gardés : ils couvrent le français.
Des polices locales donnent le même rendu hors ligne, dans le rendu PNG et dans l'export.
"""
import argparse
import pathlib
import re
import sys
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("familles", nargs="+")
    ap.add_argument("--out", default="fonts")
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    q = "&".join("family=" + urllib.parse.quote(f, safe=":,;@") for f in a.familles)
    css = get(f"https://fonts.googleapis.com/css2?{q}&display=swap").decode()

    blocs = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*{[^}]+})", css)
    if not blocs:
        blocs = [("latin", b) for b in re.findall(r"@font-face\s*{[^}]+}", css)]
    garde, n = [], 0
    for subset, bloc in blocs:
        if subset not in ("latin", "latin-ext"):
            continue
        url = re.search(r"url\((https://[^)]+)\)", bloc).group(1)
        fam = re.search(r"font-family:\s*'([^']+)'", bloc).group(1)
        style = re.search(r"font-style:\s*(\w+)", bloc).group(1)
        poids = re.search(r"font-weight:\s*([\d ]+)", bloc).group(1).strip().replace(" ", "-")
        nom = f"{fam.replace(' ', '')}-{style}-{poids}-{subset}.woff2"
        (out / nom).write_bytes(get(url))
        garde.append(bloc.replace(url, nom))
        n += 1
    (out / "fonts.css").write_text("\n".join(garde) + "\n")
    print(f"ok {n} fichiers, {out / 'fonts.css'}")


if __name__ == "__main__":
    sys.exit(main())
