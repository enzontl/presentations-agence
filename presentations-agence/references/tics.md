# Tics : le registre daté

Un tic est un procédé qui fait lire une slide comme générée. Ce n'est pas du mauvais design en soi : la plupart ont commencé comme de bonnes idées. Ils sont devenus des tics parce qu'ils sortent par défaut, partout, sans raison.

Ce registre ne donne jamais une police, une couleur ou un composant de remplacement : chaque liste « utilisez plutôt ceci » devient la vague de tics suivante. Les remplacements sont des procédés : partir de l'univers du style, tirer le layout (`tirage.py`), poser le chiffre dans un objet.

`scripts/lint.py` détecte les entrées marquées **lint**. Statut : **bloquant** veut dire que le lint échoue ; **alerte** veut dire qu'il faut une raison écrite pour le garder.

## 1. Première vague (2023-2024) : le look « IA générique »

| Tic | Statut | Faire plutôt |
| --- | --- | --- |
| Dégradé violet ou indigo en fond, sur les titres ou les boutons | bloquant, lint | Les couleurs de l'univers du style, en aplat |
| Texte en dégradé (`background-clip:text`) | bloquant, lint | Encre pleine |
| Emojis en pictos ou en puces | bloquant, lint | Des mots, ou une vraie image |
| Trois cartes identiques avec une icône dans un rond | bloquant | Un objet de l'univers, une file d'objets |
| Ombre grise floue sous chaque bloc | alerte, lint | Un aplat d'une teinte voisine, ou rien |
| Coins très arrondis sur tous les blocs | alerte, lint | Les angles de l'objet réel (un ticket a des angles droits) |
| Tout centré, titre + sous-titre + image dessous | alerte, lint | Asymétrie, grille du style |

## 2. Deuxième vague (2025) : la slide « consultant »

| Tic | Statut | Faire plutôt |
| --- | --- | --- |
| Titres étiquettes : « Contexte », « Notre solution », « Conclusion », « Merci » | bloquant, lint | Une phrase qui affirme la conclusion de la slide |
| Puces à rallonge, plus de 5 lignes | alerte, lint | Une idée par slide, le reste dans les notes |
| Trois ou quatre chiffres de même taille alignés, séparés de filets | alerte, lint | Un chiffre héros dans un objet du style (voir SKILL.md, « Slides de chiffres ») |
| La même image sur deux slides | bloquant, lint | Une image = une slide |
| Lorem ipsum, rectangle gris, « [Image ici] » | bloquant, lint | Le vrai contenu, la vraie image |

## 3. Troisième vague (2025-2026) : le « correctif » devenu un look

Ces procédés sont apparus pour éviter la première vague, puis se sont généralisés à leur tour.

| Tic | Statut | Faire plutôt |
| --- | --- | --- |
| Serif italique géant comme titre de toutes les slides | alerte | Le réserver au style qui le justifie (magazine de mode) |
| Fond crème partout « pour faire chic » | alerte | Le fond du style, et l'alternance qu'il prévoit |
| Grain plaqué sur tout sans raison de style | alerte | Le grain fait partie du traitement d'image du style, pas un filtre global |
| Une seule police sans caractère sur tout le deck | alerte | Les 3 ou 4 rôles typographiques de la fiche |
| Slides voisines de même composition | alerte, rendu.py | `tirage.py`, puis `--redraw` |

## 4. Tics de contenu

| Tic | Statut | Faire plutôt |
| --- | --- | --- |
| Superlatifs sans preuve (« révolutionnaire », « innovant », « unique ») | alerte, lint | Une preuve : date, chiffre, savoir-faire |
| Chiffre sans source | alerte, lint (pas de source sur une slide qui a des chiffres) | La source en pied de slide ou dans les notes |
| Slide sans notes de l'orateur | alerte, lint | Le script parlé dans `<aside class="notes">` |
| Texte d'exemple d'un gabarit oublié (Kōri, Valmont, données fictives) | bloquant, lint | Remplacer tout le texte du gabarit |
| `%`, `€`, `:` ou `?` séparés par une espace simple | alerte, lint (`--corriger` le répare) | Espace insécable |

## 5. Pourquoi supprimer ne suffit pas

Retirer tous les tics donne une slide propre et vide. Le contraire du générique n'est pas l'absence de défaut : c'est une idée tirée du sujet (l'objet réel, la une, l'affiche) et une hiérarchie franche. Le lint attrape les tics ; seule la critique sur les captures (`references/critique.md`) dit si la slide a une idée.
