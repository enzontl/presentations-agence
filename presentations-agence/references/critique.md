# Critique : juger le rendu

`rendu.py` sans alerte veut dire que rien de cassé n'a été mesuré. Ça ne dit pas si le deck est bon. Cette grille sert à le savoir.

Juger seulement les images, jamais le code. Celui qui a écrit le code y lit ses intentions ; les captures montrent ce qui est vraiment là. Si un défaut se voit sur une capture, il est réel, quoi que dise le HTML.

## 1. Les sept passes

Ouvrir les fichiers de `renders/`. Faire chaque passe séparément, sans les mélanger.

1. **Les titres seuls.** Lire `titres.txt`, rien d'autre. Le récit doit tenir debout : chaque titre est une phrase qui affirme quelque chose, pas une étiquette (« Résultats », « Contexte »). Un titre qu'on ne comprend qu'en voyant la slide est à réécrire.
2. **Plisser les yeux.** Regarder `planche-floue.png`. Chaque slide doit se réduire à deux ou trois masses de tailles nettement différentes. Beaucoup de petites masses semblables veut dire que tout est moyen et que rien ne mène.
3. **Une seconde.** Ouvrir chaque slide en taille réelle, regarder une seconde, détourner les yeux. Qu'a-t-on vu ? Il doit y avoir une seule réponse : un chiffre, un mot, un objet, une image. Si la réponse est « une slide », il n'y a pas de point focal.
4. **Cacher le nom.** Masquer mentalement le nom de la marque ou du sujet. Cette slide pourrait-elle appartenir à un concurrent, ou à un autre secteur ? Si oui, elle n'a pas d'idée : revenir à l'univers et aux objets du style.
5. **Les voisines.** Sur `planche.png`, comparer chaque slide à la précédente et à la suivante. Même composition, même côté pour l'image, même forme de graphique : il faut en changer une. `rapport.txt` signale les paires suspectes dans « Rythme ».
6. **Les chiffres.** Sur chaque slide de chiffres : un chiffre héros qui domine, posé dans un objet ou une figure du style, pas de grand vide non composé, une source visible.
7. **Le style.** Relire le check de la fiche du style et vérifier chaque point sur les captures : couleurs, tampons, marqueur de page, traitement des images.

## 2. La note

Noter chaque critère de 0 à 10 sur l'ensemble du deck, puis faire la moyenne pondérée.

| Critère | Poids | 10 = |
| --- | --- | --- |
| Idée | 25 % | Chaque slide appartient à l'univers du style et au sujet, impossible à transposer |
| Hiérarchie | 20 % | Un point focal par slide, deux ou trois masses, lisible à 5 mètres |
| Récit | 20 % | Les titres seuls racontent l'histoire, une idée par slide |
| Rythme | 15 % | Fonds, compositions et formes varient d'une slide à l'autre |
| Finition | 10 % | Alignements, espaces insécables, aucun débordement, images nettes |
| Chiffres | 10 % | Héros, objet, source, rien de vide |

**Plafonds** : la note ne dépasse pas 6 si l'un de ces défauts reste visible, quoi qu'il arrive ailleurs.

- Un titre générique ou sur trois lignes.
- Trois chiffres de même taille alignés et séparés de filets.
- Deux slides voisines avec la même composition.
- Une image répétée, un détourage douteux.
- Une section `.a-construire` encore présente, ou du texte d'exemple d'un gabarit (Kōri, Valmont) oublié.

## 3. Écrire la critique

Écrire la critique avant de corriger, dans ce format, dans `fond.md` ou dans la réponse :

```
Critique, round 1
Note : 6,8 / 10 (plafond : slides 4 et 5 même composition)
1. Slide 05 : même composition que la 04 (chiffre à gauche, figure à droite). Passer en objet plein cadre.
2. Slide 07 : point focal absent, trois masses égales. Agrandir le chiffre héros, réduire le reste.
3. Slide 02 : titre « Le marché » générique. Réécrire en affirmation : « Le marché double en trois ans ».
```

Trois problèmes au plus par round, les plus graves d'abord : un plafond passe avant tout le reste.

## 4. Quand s'arrêter

- Corriger les trois problèmes, relancer `rendu.py`, refaire les passes.
- Trois rounds au maximum. Au-delà, montrer le deck à l'utilisateur avec la dernière critique.
- S'arrêter avant si la note atteint 8 sans aucun plafond.
- Ne jamais retoucher une slide que l'utilisateur a validée, même si la grille la critique : le signaler seulement.
