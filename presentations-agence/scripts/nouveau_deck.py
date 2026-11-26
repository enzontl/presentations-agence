#!/usr/bin/env python3
"""Crée le dossier d'un deck prêt à remplir, à partir d'un tirage ou d'une liste de gabarits.

  python nouveau_deck.py mon-deck --tirage mon-deck/tirage.json
  python nouveau_deck.py mon-deck --style rapport-suisse --layouts cover-champ-accent,chiffre-table
  python nouveau_deck.py mon-deck --tirage tirage.json --sans-polices      # hors ligne

Ce que fait le script :
  - crée mon-deck/ avec raw/, assets/, renders/ et un fond.md à remplir s'il n'existe pas ;
  - copie base.css et le style.css du style ;
  - télécharge les polices du style (scripts/polices.py) ;
  - génère les textures du style (scripts/images.py) ;
  - assemble deck.html : une section par slide, dans l'ordre du tirage.
    Un layout qui a un gabarit est copié tel quel (texte d'exemple à remplacer).
    Un layout « à construire d'après la fiche » devient une section .a-construire avec la
    description du layout : rendu.py la signale tant qu'elle n'est pas construite.
Le deck.html existant n'est jamais écrasé (utiliser --force pour le refaire).
"""
import argparse
import html
import json
import pathlib
import shutil
import subprocess
import sys

SKILL = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = SKILL / "scripts"

FOND = """# Fond du deck

## Brief
- Consignes, durée, public, critères :

## Message en une phrase


## Storyline (les titres lus d'affilée racontent tout)
1.

## Sources des chiffres
| Chiffre | Source | Date | Lien |
| --- | --- | --- | --- |

## Images
| Fichier | Slide | Photographe | URL |
| --- | --- | --- | --- |

## Slides validées par l'utilisateur (ne plus y toucher)
"""

STUB = """<section class="slide a-construire" data-section="{section}">
  <!-- À CONSTRUIRE d'après references/{style}.md, layout : {desc} -->
  <p style="left:96px;top:96px;font:700 28px/1.3 sans-serif;color:#c00;width:1500px">À construire : {desc_txt}</p>
  <aside class="notes"></aside>
</section>"""


def run(cmd):
    print("$", " ".join(str(c) for c in cmd))
    r = subprocess.run([sys.executable, *map(str, cmd)], capture_output=True, text=True)
    print((r.stdout or r.stderr).strip()[-400:])
    return r.returncode == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dossier")
    ap.add_argument("--tirage")
    ap.add_argument("--style")
    ap.add_argument("--layouts", default="")
    ap.add_argument("--sans-polices", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    if a.tirage:
        t = json.loads(pathlib.Path(a.tirage).read_text())
        style, slides = t["style"], t["slides"]
    elif a.style and a.layouts:
        style = a.style
        idx = {g["id"]: g for g in json.loads((SKILL / "gabarits" / "index.json").read_text()) if g["style"] == style}
        slides = []
        for i, lid in enumerate(x for x in a.layouts.split(",") if x):
            if lid not in idx:
                sys.exit(f"Gabarit inconnu pour {style} : {lid}. Disponibles : {', '.join(idx)}")
            slides.append(dict(idx[lid], slide=i + 1, source="gabarit", demande=idx[lid]["type"]))
    else:
        ap.error("donner --tirage, ou --style et --layouts")

    g = SKILL / "gabarits" / style
    if not g.exists():
        sys.exit(f"Pas de gabarits pour le style {style}")
    d = pathlib.Path(a.dossier)
    for sub in ("raw", "assets", "renders"):
        (d / sub).mkdir(parents=True, exist_ok=True)
    if not (d / "fond.md").exists():
        (d / "fond.md").write_text(FOND)
    shutil.copy(SKILL / "assets" / "base.css", d / "base.css")
    shutil.copy(g / "style.css", d / "style.css")

    if not a.sans_polices:
        fams = [l.strip() for l in (g / "polices.txt").read_text().splitlines() if l.strip()]
        run([SCRIPTS / "polices.py", *fams, "--out", d / "fonts"])
    for tex in json.loads((g / "style.json").read_text()).get("textures", []):
        kind, couleur = ("papier", "F2EBDD") if tex == "papier-seri" else (tex, None)
        out = d / "assets" / f"{tex}.jpg"
        if not out.exists():
            run([SCRIPTS / "images.py", "texture", kind, out] + (["--couleur", couleur] if couleur else []))

    page = d / "deck.html"
    if page.exists() and not a.force:
        print(f"\n{page} existe déjà : rien écrit (--force pour le refaire).")
        return
    commun = (g / "commun.html").read_text() if (g / "commun.html").exists() else ""
    # commun.html : après le commentaire d'en-tête, ce qui précède le premier <script> va en début de body
    # (sprite SVG, canvas du monde 3D), les scripts en fin de body
    corps = commun.split("-->", 1)[1] if commun.lstrip().startswith("<!--") else commun
    cut = corps.find("<script")
    sprite = (corps[:cut] if cut >= 0 else corps).strip()
    scripts = corps[cut:].strip() if cut >= 0 else ""
    sections = []
    for s in slides:
        if s.get("source") == "gabarit" and s.get("fichier"):
            sections.append((SKILL / s["fichier"]).read_text().strip())
        else:
            desc = s["description"]
            sections.append(STUB.format(section=html.escape(s.get("demande", "")), style=style,
                                        desc=desc.replace("--", "-"), desc_txt=html.escape(desc)))
    page.write_text(f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Deck</title>
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="base.css">
<link rel="stylesheet" href="style.css">
<style>.a-construire{{background:repeating-linear-gradient(45deg,#fff,#fff 20px,#fee 20px,#fee 40px)}}</style>
</head>
<body class="deck">
{sprite}
{chr(10).join(chr(10) + x + chr(10) for x in sections)}
{scripts}
</body></html>
""")
    n_g = sum(1 for s in slides if s.get("source") == "gabarit")
    print(f"\n{page} : {len(slides)} slides, {n_g} depuis un gabarit, {len(slides) - n_g} à construire.")
    print("Ensuite : remplacer tout le texte d'exemple, construire les sections .a-construire, traiter les images, puis rendu.py.")


if __name__ == "__main__":
    main()
