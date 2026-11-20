# Style "Rapport suisse"

## 1. L'idée et quand l'utiliser

**En une phrase** : une grille stricte, une seule couleur d'accent et des chiffres énormes alignés au millimètre ; la rigueur de la mise en page devient la preuve du sérieux du contenu.

Univers de référence : les rapports annuels des grandes institutions suisses, les affiches du style typographique international des années 1950 et 1960, la signalétique des gares et des aéroports. Tout tient dans une grille, rien n'est décoratif, le vide est un matériau.

**Quand l'utiliser**
- Résultats annuels, bilan, rapport d'activité, RSE, gouvernance, finance, fondation.
- Comité de direction, conseil d'administration, investisseurs, jury exigeant.
- Une marque sobre, institutionnelle ou une marque d'ingénierie.

**Quand l'éviter**
- Un lancement festif, une marque jeune et décalée : le style paraîtra froid.
- Un sujet qui repose sur l'émotion des images (mode, voyage) : préférer Magazine de mode.

## 2. Palette

| Rôle | Hex | Règle |
| --- | --- | --- |
| Fond papier | `#F4F2EE` | Fond de toutes les slides de lecture |
| Fond inversé | `#141414` | Une slide sur trois environ : cover, intercalaires, chiffre clé. Sans lui, toutes les slides se ressemblent (même papier, même grille) |
| Encre | `#141414` | Titres, chiffres, texte |
| Gris secondaire | `#77746E` | Légendes, sous-titres, données de contexte |
| Filet | `#CFCBC3` | Filets de 1 px, grille des tableaux |
| Accent unique | `#E2231A` (rouge signal) ou la couleur de la marque | Un seul élément par slide |

- **Règle : une seule couleur d'accent dans tout le deck, sur un seul élément par slide** (le chiffre clé, la barre retenue, le numéro de section). L'accent devient un pointeur : l'œil va droit dessus.
- Si la marque a une couleur, elle remplace le rouge. Pas de deuxième accent.

```css
:root{
  --paper:#F4F2EE; --ink:#141414; --grey:#77746E; --rule:#CFCBC3; --accent:#E2231A;
  --f-display:"Inter Tight",sans-serif; --f-text:"Inter",sans-serif; --f-mono:"IBM Plex Mono",monospace;
  --col:122px; --gut:24px; --m:96px;   /* grille 12 colonnes : 12x122 + 11x24 + 2x96 = 1920 */
}
.slide{background:var(--paper);color:var(--ink);font-family:var(--f-text)}
```

## 3. Polices

| Rôle | Google Fonts | Usage |
| --- | --- | --- |
| Display | Inter Tight (500 à 600) | Titres (72 à 120 px) et chiffres géants (240 à 420 px), interlettrage -.03em, jamais en gras lourd |
| Texte | Inter (400, 500) | Corps 26 à 30 px, interligne 1.35, colonnes de 40 à 60 caractères |
| Mono | IBM Plex Mono (400) | Numéros de section, folio, sources, unités, légendes de figures |

Alternatives au display : Hanken Grotesk, Schibsted Grotesk. Une grotesque neutre, jamais une police "de caractère".

## 4. Éléments signature

- **La grille visible par son effet** : tout s'aligne sur 12 colonnes (marges de 96 px, gouttières de 24 px). Les blocs commencent sur une colonne, les lignes de base sont communes.
- **Filets de 1 px pleine largeur** qui séparent les zones, avec le numéro de section posé dessus.
- **Numérotation systématique** : sections `01`, `02`, figures `Fig. 3`, notes `¹`. En mono, en gris.
- **Folio en haut** : nom du rapport + année à gauche, numéro de page à droite, en mono 18 px.
- **Le chiffre géant** aligné à gauche sur la grille, son unité en petit, sa légende sur deux lignes en dessous.
- **Un carré d'accent** de 24 px qui marque l'élément important (devant un titre, sur une barre).

## 5. Traitement des images

- Peu d'images : 1 slide sur 4 au plus. La donnée et le texte suffisent.
- Préréglage `neutre` : désaturé, légèrement froid, contraste doux, presque pas de grain. Pas de dégradé sombre : le texte ne se pose jamais sur une photo.
- Les photos sont des rectangles posés sur la grille (4, 6 ou 8 colonnes de large), jamais en fond plein cadre sauf la cover, et jamais inclinées.
- Noir et blanc possible pour tout le deck si les photos sont hétérogènes.
- Légende numérotée sous chaque image (`Fig. 2 Atelier de Bienne, 2025`).

```bash
python scripts/images.py traiter raw/atelier.jpg assets/atelier.jpg --taille 852x620 --preset neutre
```

Largeurs utiles sur la grille : 3 colonnes = 414 px, 4 colonnes = 560 px, 6 colonnes = 852 px, 8 colonnes = 1144 px. Colonne n commence à 96 + (n-1) x 146 px.

## 6. Mise en page et animations

- Grille de 12 colonnes, tout aligné à gauche. Rien n'est centré.
- Beaucoup de vide : 40 % de la slide reste vide, c'est voulu.
- Hiérarchie par la taille et le gris, pas par la couleur ni le gras.
- Tableaux : filets horizontaux seulement, chiffres alignés à droite en `tabular-nums`, aucune case.
- Graphiques : barres fines, gris pour le contexte, accent pour la valeur qui compte, étiquettes directes.
- Animations minimales : `fade` ou `wipe` (révélation de gauche à droite) pour les barres et les filets, 120 ms d'écart. Aucun rebond.

## 7. Bibliothèque de layouts

| Contenu | Layout | Astuce |
| --- | --- | --- |
| Cover | Titre en display aligné en bas à gauche, année géante en filigrane gris clair | Un seul carré d'accent, folio en haut |
| Sommaire | Liste numérotée en colonne, numéros de page alignés à droite | Filets entre les lignes |
| Intercalaire | Fond inversé, numéro de section géant (`02`) et titre | Le numéro en accent |
| Chiffre clé | Chiffre de 360 px sur 7 colonnes, légende sur 3 colonnes | L'unité en mono, la variation en accent |
| Trois chiffres | Trois colonnes de 4, chiffres alignés sur la même ligne de base | Pas de boîte, juste un filet au-dessus |
| Évolution | Barres verticales fines sur 8 colonnes | Dernière barre en accent, valeurs au-dessus |
| Répartition | Chiffre héros + barre ou colonne découpée, légendes en petit | Gris dégradés, un segment en accent ; jamais les montants de chaque segment au même corps que le héros |
| Tableau financier | Tableau à filets, colonnes N-1 et N, variation | Variation en accent seulement si elle compte |
| Comparaison | Deux colonnes de 6, même structure, filet vertical au centre | Mêmes échelles des deux côtés |
| Citation, engagement | Citation en display 64 px sur 9 colonnes, nom en mono | Guillemets en accent |
| Organisation | Liste des entités en arborescence typographique (retraits) | Pas d'organigramme en boîtes |
| Calendrier | Frise horizontale à filets, jalons en mono | Le jalon actuel en accent |
| Photo | Photo sur 8 colonnes, légende numérotée sur 3 | Jamais de texte sur la photo |
| Méthode, sources | Notes numérotées en deux colonnes, mono 20 px | Style "notes de bas de page" |
| Conclusion | Trois phrases numérotées, très grandes, alignées à gauche | Rien d'autre |

## 8. Ton des textes

- Factuel, précis, affirmatif. Des phrases de 8 à 15 mots.
- Le titre énonce le fait : "Le chiffre d'affaires progresse de 12 % pour la troisième année", pas "Performance".
- Les chiffres arrondis à la précision utile, unité toujours écrite (`M€`, `%`, `t CO₂e`).
- Pas d'adjectif superlatif. La donnée fait le travail de persuasion.

## 9. Interdits spécifiques

- Plus d'une couleur d'accent, ou l'accent sur plus d'un élément par slide.
- Texte centré, éléments hors grille, éléments inclinés.
- Ombres, coins arrondis, dégradés, textures.
- Gras lourd (800, 900) et capitales partout.
- Encadrés, cartes, pictogrammes.

## 10. Check avant de livrer

- [ ] Chaque bloc commence sur une colonne de la grille (vérifier en superposant la grille sur la planche).
- [ ] Une seule couleur d'accent, un seul élément accentué par slide.
- [ ] Folio et numérotation présents et cohérents sur chaque slide.
- [ ] Chiffres en `tabular-nums`, unités écrites, sources en mono.
- [ ] Au moins 35 % de vide sur chaque slide.
- [ ] Une slide sur trois environ en fond inversé ou en champ d'accent : le style est uniforme par nature, c'est ce qui donne le rythme (tests : sans alternance, le juge plafonne le deck pour slides voisines semblables).
- [ ] Aucun texte posé sur une photo.
