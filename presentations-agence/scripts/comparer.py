#!/usr/bin/env python3
"""Comparaison à l'aveugle de deux decks (avec et sans le skill, ou deux versions).

Étape 1, préparer :
  python comparer.py preparer --a sans-skill/renders --b avec-skill/renders --out comparaison/
  -> comparaison/X.png, Y.png (planches), cote-a-cote.png, grille.md, notes.json (à remplir), .cle.json

Les lettres X et Y sont tirées au sort : le juge ne sait pas quel deck vient de quelle source.
Donner au juge (un agent neuf, ou une personne) uniquement les images et grille.md, jamais .cle.json.

Étape 2, après que le juge a rempli notes.json :
  python comparer.py resultat comparaison/
  -> notes pondérées, plafonds, et quel deck (a ou b) gagne.
"""
import argparse
import json
import pathlib
import random
import sys

from PIL import Image, ImageDraw

CRITERES = [("idee", 25, "Chaque slide appartient à un univers et au sujet, impossible à transposer"),
            ("hierarchie", 20, "Un point focal par slide, deux ou trois masses, lisible à 5 mètres"),
            ("recit", 20, "Les titres seuls racontent l'histoire, une idée par slide"),
            ("rythme", 15, "Fonds, compositions et formes varient d'une slide à l'autre"),
            ("finition", 10, "Alignements, aucun débordement, typographie soignée, images nettes"),
            ("chiffres", 10, "Un chiffre héros dans un objet ou une figure, rien de vide, source visible")]
PLAFONDS = ["titre générique ou sur trois lignes", "trois chiffres égaux alignés",
            "deux slides voisines de même composition", "image répétée ou détourage douteux",
            "look généré évident (dégradé violet, cartes à icônes, emojis)"]


def slides(d):
    fs = sorted(pathlib.Path(d).glob("slide-*.png"))
    if not fs:
        sys.exit(f"Aucune slide-NN.png dans {d} : lancer rendu.py d'abord.")
    return fs


def planche(fs, out, cols=3, tw=640):
    th = int(tw * 9 / 16); g = 20
    rows = (len(fs) + cols - 1) // cols
    s = Image.new("RGB", (cols * tw + (cols + 1) * g, rows * th + (rows + 1) * g), (30, 30, 30))
    for k, f in enumerate(fs):
        r, c = divmod(k, cols)
        s.paste(Image.open(f).convert("RGB").resize((tw, th), Image.LANCZOS), (g + c * (tw + g), g + r * (th + g)))
    s.save(out)


def cote(fx, fy, out, tw=720):
    th = int(tw * 9 / 16); g = 20; n = max(len(fx), len(fy))
    s = Image.new("RGB", (2 * tw + 3 * g, n * (th + g) + g + 40), (30, 30, 30))
    d = ImageDraw.Draw(s)
    d.text((g, 12), "X", fill=(230, 230, 230)); d.text((2 * g + tw, 12), "Y", fill=(230, 230, 230))
    for i in range(n):
        for j, fs in enumerate((fx, fy)):
            if i < len(fs):
                s.paste(Image.open(fs[i]).convert("RGB").resize((tw, th), Image.LANCZOS), (g + j * (tw + g), 40 + g + i * (th + g)))
    s.save(out)


def preparer(a):
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    fa, fb = slides(a.a), slides(a.b)
    rng = random.Random(a.seed)
    x_est_a = rng.random() < .5
    fx, fy = (fa, fb) if x_est_a else (fb, fa)
    planche(fx, out / "X.png"); planche(fy, out / "Y.png"); cote(fx, fy, out / "cote-a-cote.png")
    (out / ".cle.json").write_text(json.dumps({"X": "a" if x_est_a else "b", "Y": "b" if x_est_a else "a",
                                               "a": str(a.a), "b": str(a.b)}, indent=1))
    vide = {k: {c: None for c, _, _ in CRITERES} | {"plafonds": [], "commentaire": ""} for k in ("X", "Y")}
    (out / "notes.json").write_text(json.dumps(vide, ensure_ascii=False, indent=1))
    lignes = ["# Grille de jugement à l'aveugle", "",
              "Tu juges deux decks, X et Y, uniquement sur les images : X.png, Y.png et cote-a-cote.png.",
              "Tu ne sais pas comment ils ont été faits et tu ne dois pas chercher à le deviner.", "",
              "Pour chaque deck, note chaque critère de 0 à 10 :", "",
              "| Critère | Poids | 10 = |", "| --- | --- | --- |"]
    lignes += [f"| {c} | {p} % | {d} |" for c, p, d in CRITERES]
    lignes += ["", "Plafonds : si un de ces défauts est visible, la note finale du deck ne peut pas dépasser 6.", ""]
    lignes += [f"- {p}" for p in PLAFONDS]
    lignes += ["", "Remplis notes.json : une note par critère, la liste des plafonds constatés (texte libre), et un commentaire de deux phrases par deck.",
               "Puis dis lequel tu préfères et pourquoi, en une phrase."]
    (out / "grille.md").write_text("\n".join(lignes) + "\n")
    print(f"Prêt dans {out}/ : X.png, Y.png, cote-a-cote.png, grille.md, notes.json.")
    print("Donner au juge les images et grille.md, pas .cle.json. Puis : comparer.py resultat " + str(out))


def resultat(a):
    d = pathlib.Path(a.dossier)
    notes = json.loads((d / "notes.json").read_text()); cle = json.loads((d / ".cle.json").read_text())
    scores = {}
    for k in ("X", "Y"):
        n = notes[k]
        manque = [c for c, _, _ in CRITERES if n.get(c) is None]
        if manque:
            sys.exit(f"notes.json incomplet pour {k} : {manque}")
        s = sum(n[c] * p for c, p, _ in CRITERES) / 100
        if n.get("plafonds"):
            s = min(s, 6.0)
        scores[k] = s
        print(f"{k} = deck {cle[k]} ({cle[cle[k]]}) : {s:.1f} / 10" + (f"  plafonds : {', '.join(n['plafonds'])}" if n.get("plafonds") else ""))
    g = max(scores, key=scores.get)
    if abs(scores["X"] - scores["Y"]) < .3:
        print("Égalité à 0,3 près : pas de gagnant net.")
    else:
        print(f"Gagnant : deck {cle[g]} ({cle[cle[g]]}), +{abs(scores['X'] - scores['Y']):.1f} point(s).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("preparer"); p.add_argument("--a", required=True); p.add_argument("--b", required=True)
    p.add_argument("--out", default="comparaison"); p.add_argument("--seed", type=int, default=None)
    r = sub.add_parser("resultat"); r.add_argument("dossier")
    a = ap.parse_args()
    preparer(a) if a.cmd == "preparer" else resultat(a)


if __name__ == "__main__":
    main()
