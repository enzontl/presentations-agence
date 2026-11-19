# Commandes

Le skill s'appelle sans argument pour un deck neuf (le procédé complet du SKILL.md), ou avec une commande et une cible pour travailler sur un deck qui existe :

```
/presentations-agence audit mon-deck/deck.html
/presentations-agence plus-audacieux mon-deck/deck.html 3,5
```

Règles valables pour toutes les commandes :

- **Ne jamais retoucher une slide validée** par l'utilisateur (liste dans `fond.md`). La signaler si la commande la vise, et passer.
- **Garder le style du deck.** Une commande change l'intensité, la variété ou la finition, pas l'univers (sauf `changer-style`).
- **Finir chaque commande par la boucle** : `lint.py`, `rendu.py`, la critique de `references/critique.md` sur les slides touchées, et un résumé de ce qui a changé.

## audit : critiquer sans rien modifier

Pour un deck fait par quelqu'un d'autre, par un autre outil, ou avant une livraison.

1. Si la cible est un PDF : en tirer une image par page (`sips -s format png` sur macOS, ou `pdftoppm -png`). Si c'est un PPTX : demander un export PDF, puis faire de même. Si c'est un HTML : `lint.py` puis `rendu.py`.
2. Faire les sept passes de `references/critique.md` sur les images.
3. Rendre un rapport : la note sur 10 et ses plafonds, les résultats du lint s'il y en a, les trois problèmes les plus graves avec la slide, le défaut et la correction proposée, puis ce qui marche et qu'il faut garder.
4. Ne modifier aucun fichier. Proposer ensuite la commande qui corrige (`refaire-chiffres`, `varier`, `polish`…).

## polish : la finition, sans toucher aux layouts

1. `lint.py --corriger` pour les espaces insécables.
2. Corriger tout ce que signalent `lint.py` et `rendu.py` : débordements, titres sur 3 lignes, texte sous un tampon, images manquantes, polices en repli.
3. Sur les captures : alignements sur la grille du style, marges égales, contraste du texte sur les photos, chiffres en `tabular-nums`, sources présentes, marqueur de page sur chaque slide.
4. Vérifier les notes : script présent, crédits photo à la fin.
5. Ne changer ni la composition ni les couleurs des slides.

## plus-audacieux : monter l'intensité

Pour un deck jugé « sage », « plat », « trop corporate ». Sur les slides indiquées, ou sur tout le deck.

1. **Échelle** : le titre ou le chiffre héros grossit d'un cran franc (1,5 à 2 fois), quitte à être coupé par le bord (`bleed`).
2. **Contraste** : une slide sur trois passe au fond d'impact du style (sombre, fond nuit, couleur pop pleine).
3. **Élément signature** : il devient visible sur chaque slide (tampon, bandeau, défaut de repérage, champ d'accent).
4. **Image** : plein cadre plutôt qu'encadrée, cadrage plus serré.
5. Respecter les plafonds du style : couleurs pop par slide, un tampon par slide, un accent par slide en suisse.

## plus-sobre : baisser l'intensité

Pour un public plus classique (comité, jury) ou un deck jugé « too much ».

1. Retirer les éléments décoratifs en trop : tampons sur les slides de lecture, inclinaisons, textures appuyées.
2. Revenir au fond de lecture du style sur les slides denses.
3. Réduire le titre d'un cran s'il écrase la preuve.
4. Garder l'élément signature sur la cover et le marqueur de page : c'est ce qui garde l'identité.

## refaire-chiffres : les slides de chiffres

Le défaut le plus fréquent (voir SKILL.md, « Slides de chiffres »).

1. Repérer les slides de chiffres : `lint.py` (alerte « chiffres de même taille ») et les titres qui contiennent un nombre.
2. Re-tirer leur layout : `tirage.py ... --redraw <numéros>` avec un type `chiffre-cle`, `plusieurs-chiffres`, `repartition` ou `evolution`.
3. Appliquer les règles : un chiffre héros, posé dans un objet ou une figure du style, rien de vide, la source visible, une forme différente de la slide de chiffres voisine.

## varier : casser les répétitions

1. Lancer `rendu.py` et lire la rubrique « Rythme » du rapport.
2. Pour chaque paire signalée, re-tirer l'une des deux slides (`tirage.py --redraw`), ou changer le côté de l'image, le fond, ou la forme du graphique.
3. Relancer jusqu'à ce que la rubrique « Rythme » soit vide ou que chaque paire restante soit justifiée.

## changer-style : même contenu, autre univers

1. Lire la fiche du nouveau style en entier.
2. Reconstruire le plan à partir des slides existantes (un type de contenu par slide, d'après `data-section` et le contenu).
3. `tirage.py --style <nouveau>` puis `nouveau_deck.py` dans un nouveau dossier : ne jamais écraser l'ancien deck.
4. Reporter le texte, les chiffres, les notes et les sources ; retraiter les images avec le préréglage du nouveau style.

## notes : écrire le script de l'orateur

1. Suivre `references/recit.md`, section 7 : phrases parlées, 80 à 130 mots par slide, la première phrase reprend le titre, la dernière amène la suivante.
2. Ajouter les sources et les crédits photo à la fin des notes de chaque slide.
3. Si plusieurs orateurs : demander qui présente quoi, puis mettre le prénom en tête.

## exporter : livrer

`export.py` pour le HTML autonome, `exporter.py --pdf --pptx` pour le PDF et le PowerPoint. Rappeler que le PPTX n'est pas modifiable (une image par slide).
