#!/usr/bin/env python3
"""Tire au sort un layout par slide, dans le style choisi.

Pourquoi un script : un modèle à qui l'on demande de choisir un layout revient toujours
au même choix par défaut, et deux slides voisines finissent par se ressembler. Ici le
hasard choisit parmi ce qui convient, avec trois règles :
  - deux slides voisines n'ont jamais la même forme (photo, courbe, objet, typo...) ;
  - un layout ne sert qu'une fois par deck tant qu'il reste une alternative ;
  - les layouts tirés dans les projets récents sont défavorisés (historique global).

  python tirage.py --style rapport-suisse --plan cover,chiffre-cle,evolution,comparaison,citation,closing
  python tirage.py --style une-de-journal --plan plan.txt --seed 4 --out mon-deck/tirage.json
  python tirage.py --style magazine-de-mode --plan ... --redraw 3     # re-tire seulement la slide 3
  python tirage.py --types                                             # liste les types de contenu
  python tirage.py --style data-journalisme --liste                    # tous les layouts du style

Sources des layouts : les gabarits validés (gabarits/index.json, prêts à copier) et les
layouts décrits dans la fiche du style (references/<style>.md, à construire d'après la fiche).
Sortie : un tableau lisible et un fichier tirage.json que lit nouveau_deck.py.
"""
import argparse
import json
import pathlib
import random
import re
import sys
import time
import unicodedata

SKILL = pathlib.Path(__file__).resolve().parent.parent
HIST = pathlib.Path.home() / ".cache" / "presentations-agence" / "historique.json"

# type de contenu -> mots qui le signalent dans la colonne « Contenu » des fiches
TYPES = {
    "cover": ["cover", "couverture", "une"],
    "sommaire": ["sommaire", "intercalaire", "structure"],
    "chiffre-cle": ["chiffre cle", "le chiffre"],
    "plusieurs-chiffres": ["plusieurs chiffres", "trois chiffres", "chiffres cles", "en chiffres", "synthese chiffree", "objectifs", "kpi", "chiffres"],
    "evolution": ["evolution"],
    "comparaison": ["comparaison", "comparer", "classement", "observe", "insight", "relation", "scores", "tailles de groupes", "comparaison de profils"],
    "avant-apres": ["avant"],
    "repartition": ["repartition", "proportion", "tableau chiffre", "tableau financier", "tableau", "prix"],
    "offre": ["offre", "gamme", "produit", "merch"],
    "etapes": ["etapes", "segments", "processus", "roadmap", "planning", "chronologie", "historique", "calendrier", "programme", "parcours", "agenda"],
    "persona": ["persona", "portrait", "interview", "temoignage", "besoin", "client"],
    "citation": ["citation", "statement", "manifeste", "vision", "positionnement", "engagement", "fin d'une epoque"],
    "territoire": ["territoire", "carte"],
    "methode": ["methode", "methodologie", "sources", "reseau, espace"],
    "closing": ["closing", "conclusion", "derniere"],
    "equipe": ["equipe", "partenaires", "organisation"],
    "campagne": ["campagne", "visuels", "inspiration", "moodboard", "fidelite", "acces"],
    "contexte": ["contexte", "probleme", "idee centrale", "anatomie"],
}
# si le style n'a aucun layout du type demandé, on cherche dans ces types voisins
VOISINS = {
    "chiffre-cle": ["plusieurs-chiffres", "repartition"], "plusieurs-chiffres": ["chiffre-cle", "repartition"],
    "evolution": ["comparaison", "plusieurs-chiffres"], "comparaison": ["evolution", "avant-apres", "plusieurs-chiffres"],
    "avant-apres": ["comparaison"], "repartition": ["plusieurs-chiffres", "chiffre-cle"], "territoire": ["comparaison", "plusieurs-chiffres"],
    "offre": ["campagne", "repartition"], "etapes": ["sommaire"], "persona": ["citation", "contexte"], "citation": ["contexte", "closing"],
    "methode": ["contexte"], "equipe": ["persona"], "campagne": ["offre"], "sommaire": ["etapes"], "contexte": ["citation", "persona"],
    "closing": ["citation"], "cover": ["citation"],
}
# fond d'impact par style : une slide sur trois le prend (les slides 3, 6, 9…), pour casser l'uniformité
FOND_IMPACT = {
    "editorial-objet-reel": "sombre #111111 (texture sombre)",
    "studio-sombre": None,  # déjà tout en fond nuit : l'alternance vient des slides objet
    "rapport-suisse": "fond inversé #141414, ou champ d'accent pleine hauteur",
    "une-de-journal": "page « édition spéciale » : bandeau rouge et gros titre seul",
    "affiche-serigraphie": "aplat d'une encre pleine page, texte en réserve",
    "magazine-de-mode": "photo plein cadre",
    "data-journalisme": "fond nuit #17232C",
    "brutalisme-web": "terminal, fond #0A0A0A",
}
SOMBRES = {"sombre", "nuit", "photo"}

# ordre de lecture des formes : la première trouvée dans la description gagne
FORMES = [
    ("objet3d", ["objet 3d", "slide objet", "cyclo", "objet eclate", "objets alignes", "deux objets"]),
    ("carte", ["carte choroplethe", "carte schematique", "plan du site", "carte ou liste"]),
    ("waffle", ["waffle"]),
    ("dumbbell", ["dumbbell", "slope"]),
    ("courbe", ["courbe", "sparkline", "frise"]),
    ("colonnes", ["colonnes sur", "colonnes groupees", "barres verticales"]),
    ("barres", ["barres", "barre horizontale", "barre empilee"]),
    ("table", ["tableau", "table", "listing", "liste", "diff", "changelog", "terminal", "readme", "formulaire"]),
    ("objet", ["ticket", "facture", "fiche", "carte a tampons", "carte de", "billet", "bracelet", "setlist", "etiquette", "menu", "affiche", "flyer", "sticker", "tote", "erratum", "annonces", "programme tele", "bulletin", "mur d'affiches", "objet"]),
    ("photo", ["photo", "portrait", "plein cadre"]),
]


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def type_de(contenu):
    c = norm(contenu)
    for t, mots in TYPES.items():
        if any(re.search(r"\b" + re.escape(m) + r"\b", c) for m in mots):
            return t
    return "contexte"


def forme_de(texte):
    t = norm(texte)
    for f, mots in FORMES:
        if any(m in t for m in mots):
            return f
    return "typo"


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", norm(s)).strip("-")[:40]


def layouts(style):
    out = []
    idx = SKILL / "gabarits" / "index.json"
    for g in json.loads(idx.read_text()) if idx.exists() else []:
        if g["style"] == style:
            out.append(dict(id=g["id"], type=g["type"], forme=g["forme"], source="gabarit",
                            fichier=g["fichier"], description=g["description"], image=g["image"]))
    fiche = SKILL / "references" / f"{style}.md"
    if not fiche.exists():
        sys.exit(f"Style inconnu : {style}. Styles : " + ", ".join(p.stem for p in (SKILL / 'references').glob('*.md')))
    txt = fiche.read_text()
    sec = txt[txt.find("Bibliothèque de layouts"):]
    for ligne in sec.splitlines()[1:]:
        if ligne.startswith("## "):
            break
        cells = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[0] in ("Contenu", "---") or set(cells[0]) <= set("- "):
            continue
        contenu, layout, astuce = cells
        out.append(dict(id="fiche-" + slug(contenu), type=type_de(contenu), forme=forme_de(layout + " " + astuce),
                        source="fiche", fichier=None, description=f"{contenu} : {layout}. Astuce : {astuce}", image=None))
    return out


def lire_hist():
    try:
        return json.loads(HIST.read_text())
    except Exception:
        return []


def tirer(style, plan, seed, fixes=None):
    rng = random.Random(seed)
    tous = layouts(style)
    recents = {h["id"] for h in lire_hist()[-40:] if h.get("style") == style}
    res, deja = [], set()
    for i, t in enumerate(plan):
        if fixes and i in fixes:
            res.append(fixes[i]); deja.add(fixes[i]["id"]); continue
        cands = [l for l in tous if l["type"] == t] or [l for l in tous if l["type"] in VOISINS.get(t, [])] or tous
        prev = res[-1]["forme"] if res else None
        nxt = fixes.get(i + 1, {}).get("forme") if fixes else None
        def poids(l):
            w = 3.0 if l["source"] == "gabarit" else 1.0
            if l["id"] in deja: w *= 0.05
            if l["forme"] in (prev, nxt): w *= 0.02
            if l["id"] in recents: w *= 0.4
            return w
        ws = [poids(l) for l in cands]
        choix = rng.choices(cands, weights=ws, k=1)[0]
        res.append(dict(choix, slide=i + 1, demande=t))
        deja.add(choix["id"])
    impact = FOND_IMPACT.get(style)
    for s_ in res:
        clair = s_.get("fond") not in SOMBRES if s_.get("source") == "gabarit" else True
        s_["fond_conseille"] = impact if (impact and s_["slide"] % 3 == 0 and clair) else None
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--style")
    ap.add_argument("--plan", help="types séparés par des virgules, ou un fichier (un type par ligne)")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--out", default="tirage.json")
    ap.add_argument("--redraw", default="", help="numéros de slides à re-tirer, les autres sont gardées (lit --out)")
    ap.add_argument("--types", action="store_true")
    ap.add_argument("--liste", action="store_true")
    a = ap.parse_args()

    if a.types:
        print("\n".join(f"{t:20} {', '.join(m[:4])}" for t, m in TYPES.items())); return
    if not a.style:
        ap.error("--style est requis")
    if a.liste:
        for l in layouts(a.style):
            print(f"{l['type']:18} {l['forme']:9} {l['source']:8} {l['id']}")
        return
    if not a.plan:
        ap.error("--plan est requis")
    p = pathlib.Path(a.plan)
    plan = [x.strip() for x in (p.read_text().splitlines() if p.exists() else a.plan.split(",")) if x.strip()]
    inconnus = [t for t in plan if t not in TYPES]
    if inconnus:
        sys.exit(f"Types inconnus : {inconnus}. Voir --types.")
    seed = a.seed if a.seed is not None else int(time.time())
    fixes = None
    if a.redraw:
        old = json.loads(pathlib.Path(a.out).read_text())["slides"]
        re_ = {int(x) for x in a.redraw.split(",")}
        fixes = {s["slide"] - 1: s for s in old if s["slide"] not in re_}
    res = tirer(a.style, plan, seed, fixes)

    print(f"Tirage {a.style} · graine {seed}\n")
    for s in res:
        mark = "gabarit" if s["source"] == "gabarit" else "à construire d'après la fiche"
        print(f"{s['slide']:02d}  {s['demande']:18} {s['forme']:9} {s['id']}  ({mark})")
        print(f"     {s['description']}")
        if s.get("fond_conseille"):
            print(f"     Fond : {s['fond_conseille']} (une slide sur trois en fond d'impact)")
    pathlib.Path(a.out).write_text(json.dumps(dict(style=a.style, seed=seed, slides=res), ensure_ascii=False, indent=1))
    h = lire_hist() + [dict(style=a.style, id=s["id"], t=int(time.time())) for s in res]
    HIST.parent.mkdir(parents=True, exist_ok=True)
    HIST.write_text(json.dumps(h[-400:]))
    print(f"\nÉcrit : {a.out}. Re-tirer une slide : --redraw 3. Pas convaincu ? relancer sans --seed.")


if __name__ == "__main__":
    main()
