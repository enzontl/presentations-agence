# Style "Éditorial objet réel"

## 1. L'idée et quand l'utiliser

**En une phrase** : un magazine éditorial où chaque slide de contenu prend la forme d'un objet réel de l'univers du sujet (ticket, facture, menu, carte, billet, étiquette, affiche) au lieu d'un template.

Le format raconte le concept avant même que le texte soit lu : un tableau de prix devient un ticket de caisse, un programme devient une carte à tampons. C'est ce qui donne l'impression d'un travail d'agence.

**Quand l'utiliser**
- Pitchs de marque ou de projet, lancements, stratégies, présentations créatives, portfolios.
- Quand le sujet a un univers physique identifiable : commerce, restauration, mode, sport, culture, artisanat, voyage, santé.

**Quand l'éviter**
- Sujets très techniques ou rapports chiffrés denses : préférer Data-journalisme ou Rapport suisse.
- Sujets sans univers physique (logiciel abstrait, finance pure) : les objets sonneraient faux.

### Trouver l'univers et ses objets

Nommer l'univers réel du sujet en 2 ou 3 mots, lister 6 à 10 objets de cet univers, associer chaque type de contenu à un objet.

| Univers | Objets-layouts | Couleurs pop possibles |
| --- | --- | --- |
| Épicerie, deli | Ticket de caisse, ticket de commande, menu, carte à tampons | Vert vif, jaune taxi, rouge |
| Café, torréfacteur | Sachet kraft, étiquette d'origine, tableau à la craie, carte de fidélité | Terracotta, vert sauge |
| Sport, club | Feuille de match, billet, tableau de score, maillot | Couleurs du club |
| Pharmacie, beauté | Ordonnance, notice, étiquette, boîte | Vert croix, bleu clinique |
| Festival, musique | Billet, bracelet, setlist, affiche | Fluo, chrome |
| Voyage, transport | Carte d'embarquement, tampon de passeport, carte postale | Bleu ciel, orange signal |
| Mode, atelier | Étiquette de vêtement, patron, carnet de croquis | Noir, une couleur saison |
| Bibliothèque, culture | Fiche de prêt, carte de lecteur, tampon dateur, ticket d'entrée | Rouge tampon, vert reliure |
| Tech, startup | Ticket de support, reçu d'abonnement, écran de terminal | Vert terminal, violet électrique |

## 2. Palette

| Rôle | Exemple | Règle |
| --- | --- | --- |
| Sombre chaud (slides d'impact) | `#111111` | Fonds des covers, intercalaires, statements |
| Clair papier (lecture) | `#EFE3C8` ou `#F8F1E1` | Fonds des objets et des slides denses |
| Pop 1, tirée de l'univers | ex. vert vif `#1F9D55` | Tampons, mots clés |
| Pop 2, tirée de l'univers | ex. jaune taxi `#F7C600` | Bandes, étiquettes |
| Pop 3 et 4, optionnelles | ex. rouge `#E03A2F` | Une seule fois par slide si besoin |
| Héritage, si la marque en a une | or, bordeaux, marine | Logo, filets fins, marqueur de page |

- Les couleurs pop sont celles qu'on voit vraiment dans l'univers : enseignes, emballages, uniformes, signalétique.
- Alterner les deux neutres d'une slide à l'autre, pour donner un rythme.
- **Règle : 2 couleurs pop maximum par slide.**

```css
:root{
  --dark:#111111; --paper:#EFE3C8; --paper2:#F8F1E1; --ink:#1A1714;
  --pop1:#1F9D55; --pop2:#F7C600; --pop3:#E03A2F; --heritage:#B08D57;
  --f-display:"Anton",sans-serif; --f-accent:"Playfair Display",serif;
  --f-text:"Inter",sans-serif; --f-mono:"Space Mono",monospace;
}
```

## 3. Polices

| Rôle | Google Fonts | Usage |
| --- | --- | --- |
| Display | Anton, Bebas Neue, Archivo Black | Titres en capitales, très grands (160 à 420 px) |
| Accent | Playfair Display italique, Fraunces italique | Citations, taglines, la voix élégante |
| Texte | Inter, DM Sans | Corps lisible (24 à 32 px) |
| Mono | Space Mono, IBM Plex Mono | Tickets, labels, numéros, prix |

Les titres sont énormes et peuvent être coupés par le bord, par une photo ou par un objet posé dessus (classe `bleed`).

## 4. Éléments signature

- **Tampon incliné** : rectangle de couleur pop, de -6 à -12°, texte en display ou mono capitales. **Un seul par slide** (NEW, VOID, SOLD OUT, PAYÉ, un chiffre).
- **Marqueur de page récurrent** en bas à droite, dans la forme d'un objet de l'univers (ticket, étiquette, billet) avec le nom du sujet et "No. X" (`<span class="pageno">`).
- **Sous-titre de section** en capitales espacées, avec une barre de couleur à gauche, qui situe la slide dans la structure.
- **Duo punchline + sous-titre clair** : la punchline accroche, le sous-titre dit le fond.
- **Détails d'objet** : pointillés de découpe, perforations, code-barres, numéro de série. Ils rendent l'objet crédible.

Classes à mettre dans `style.css` : `.giant`, `.title`, `.sub`, `.section`, `.stamp`, `.receipt`, `.r-line`, `.r-dots`, `.r-cut`, `.stub`, `.tag`.

```css
.stamp{font:400 64px/1 var(--f-display);text-transform:uppercase;padding:14px 26px;color:var(--paper);background:var(--pop3);rotate:-8deg;box-shadow:inset 0 0 0 4px rgba(255,255,255,.25)}
.section{font:700 20px/1 var(--f-mono);letter-spacing:.24em;text-transform:uppercase;padding-left:22px;border-left:8px solid var(--pop1)}
.receipt{background:#FBF8F1;color:var(--ink);font:400 26px/1.5 var(--f-mono);padding:56px 56px 72px;rotate:-1.5deg;filter:drop-shadow(0 18px 30px rgba(0,0,0,.25))}
.r-line{display:flex;justify-content:space-between}
.r-dots{border-top:3px dashed currentColor;opacity:.5;margin:18px 0}
.r-cut{position:absolute;left:0;right:0;bottom:-14px;height:28px;background:radial-gradient(circle at 14px 0,transparent 13px,#FBF8F1 14px) 0 0/28px 28px repeat-x}
```

## 5. Traitement des images

- Préréglage `chaud` : saturation un peu baissée, tons chauds, contraste un peu relevé, grain léger.
- Dégradé sous le texte (`--sombre bas` ou `gauche`, force 0,6 à 0,8) pour les photos plein cadre avec titre.
- Textures : `texture papier` (crème) et `texture sombre`, en `.bg` sous les slides sans photo. `texture kraft` pour les univers café, épicerie, artisanat.
- Compositions : mur d'affiches de travers, avec ombres et plis.
- Objets détourés seulement s'ils sont parfaits (PNG propre, vérifié à 200 %). Sinon, photo entière.

```bash
python scripts/images.py traiter raw/comptoir.jpg assets/comptoir.jpg --taille 1920x1080 --preset chaud --sombre gauche --force .8
python scripts/images.py texture papier assets/papier.jpg --couleur EFE3C8
```

## 6. Mise en page et animations

- Format 1920x1080, éléments en absolu. Asymétrie, beaucoup de vide, objets légèrement de travers (-2° à +2°).
- Marges de 96 à 120 px. L'objet occupe 40 à 60 % de la slide, jamais centré parfaitement.
- 3 niveaux de texte maximum : titre, sous-titre, détail. Le reste va dans les notes.
- Alternance : une slide sombre d'impact, une ou deux slides papier de lecture.
- Animations : montée-fondu (`rise`) pour les textes, chute depuis le haut (`drop`) pour les objets posés, tampon qui claque avec un rebond (`slam`), décalés de 120 ms via `--i`.

## 7. Bibliothèque de layouts

Un deck en utilise en général 10 à 15.

| Contenu | Layout | Astuce |
| --- | --- | --- |
| Cover | Typo géante + objet principal posé dessus | Titre coupé par l'objet, tagline en italique serif |
| Sommaire, intercalaire | Grand numéro (01) sur photo plein cadre | Parties en mono |
| Avant / après | Deux documents de l'univers côte à côte | L'ancien barré d'un tampon VOID, le nouveau tamponné |
| Insight, comparaison | Diptyque papier / photo | Deux univers visuels opposés |
| Chiffre clé | Chiffre sur 40 % de la slide | Source en petit, contexte en tampon |
| Idée centrale | Équation visuelle A × B = C | Résultat dans une bande de couleur |
| Offre, gamme | Une photo plein cadre | Prix ou noms en étiquettes posées dessus |
| Segments, étapes | Une file d'objets (tickets, cartes, billets) | Plutôt qu'une grille de cartes |
| Persona, portrait | Photo pleine hauteur + fiche-objet | Citation en serif, 3 infos max, ligne "pas pour" |
| Tableau chiffré | Ticket de caisse, facture ou relevé | Pointillés, total en gros |
| Synthèse chiffrée | Barre empilée + phases | Une couleur par bloc |
| Objectifs, KPIs | Menu, tableau d'affichage, scoreboard | Étape, indicateur, chiffre en couleur pop |
| Campagne, visuels | Mur d'affiches de travers | Les vraies créations |
| Programme, fidélité | Carte à tampons ou abonnement | Mécanique + avantages |
| Statement | Une photo, une phrase | Rien d'autre |
| Closing | Fond couleur pop, une phrase | Message final + questions |

## 8. Ton des textes

- Punchlines courtes. Une langue principale, éventuellement des touches dans une autre.
- L'humour vise des habitudes ou des clichés, jamais les gens.
- Chaque phrase audacieuse est accompagnée d'une preuve : une date, un savoir-faire, un chiffre.
- Les textes d'objets parlent la langue de l'objet : "TOTAL", "À RENDRE AVANT LE", "PORTE B12", "LOT N°".

## 9. Interdits spécifiques

- Plus de 2 couleurs pop ou plus d'un tampon par slide.
- Un objet qui n'existe pas dans l'univers du sujet (un billet d'avion pour une boulangerie).
- Des objets parfaitement droits et centrés : ils perdent leur réalité.
- Le même objet détouré sur plusieurs slides.
- Des titres en minuscules dans la police display.

## 10. Check avant de livrer

- [ ] Chaque slide de contenu utilise un objet de l'univers, pas une grille générique.
- [ ] 2 couleurs pop max et 1 tampon max par slide.
- [ ] Marqueur de page en forme d'objet et sous-titre de section sur chaque slide.
- [ ] Alternance de fonds sombre et papier visible sur la planche contact.
- [ ] Aucune image répétée, détourages propres, crédits dans les notes.
- [ ] Aucun titre sur 3 lignes, aucun débordement.
- [ ] Le deck se comprend en ne lisant que les titres.
