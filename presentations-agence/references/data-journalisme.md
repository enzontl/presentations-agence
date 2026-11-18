# Style "Data-journalisme"

## 1. L'idée et quand l'utiliser

**En une phrase** : chaque slide démontre au lieu d'affirmer, avec un graphique annoté sur fond papier, une seule couleur d'emphase et une source sous chaque chiffre, comme une enquête graphique de grand quotidien.

Univers de référence : les enquêtes graphiques de la presse en ligne, les atlas, les infographies de quotidiens, les rapports d'instituts statistiques bien faits. Ses conventions servent de layouts : le surtitre coloré, le titre qui conclut, la ligne "Lecture :", la note de méthode, la source, l'annotation posée directement sur la courbe.

**Quand l'utiliser**
- Étude de marché, enquête, mémoire, analyse de politique publique, rapport d'observatoire.
- Un jury, des décideurs, une audience qui veut des preuves.
- Quand les chiffres sont le cœur du propos et qu'on dispose des données brutes.

**Quand l'éviter**
- Pas de données, ou des données trop pauvres pour faire un graphique honnête.
- Un pitch émotionnel, une marque à forte image.

## 2. Palette

| Rôle | Hex | Règle |
| --- | --- | --- |
| Papier | `#F7F5F0` | Fond de toutes les slides |
| Encre | `#1A1A1A` | Titres, texte, axes principaux |
| Gris données | `#B9B4AB` | Toutes les séries de contexte |
| Gris texte | `#6B6760` | Annotations secondaires, sources, axes |
| Grille | `#E3DFD7` | Lignes de grille (4 ou 5 max) |
| Emphase | `#E4572E` | La donnée qui porte le message, et le surtitre |
| Contraste, optionnel | `#2F6DB5` | Seulement quand deux catégories s'opposent |
| Fond nuit | `#17232C`, texte `#F1EDE6`, grille `#33424D`, emphase `#FF6B43` | Covers et slides d'impact, une sur trois environ |
| Teinte d'emphase | `#F4E2D7` | Panneau derrière une colonne de texte, bandes sur les lignes qui portent le message |

- **Règle : tout est gris sauf la donnée qui porte le message.** Une seule couleur d'emphase par graphique. Le bleu de contraste n'apparaît que pour opposer deux groupes (et alors l'orange et le bleu, rien d'autre).
- Un deck tout en papier clair paraît terne : alterner avec le fond nuit pour les covers et les slides d'impact, et utiliser la teinte d'emphase en aplat (panneau, bandes). Retour utilisateur réel : « manque un peu de couleur et de fond ».
- Vérifier les couleurs pour le daltonisme : orange et bleu se distinguent ; jamais rouge contre vert.

```css
:root{
  --paper:#F7F5F0; --ink:#1A1A1A; --data:#B9B4AB; --grey:#6B6760; --grid:#E3DFD7;
  --em:#E4572E; --contrast:#2F6DB5;
  --f-head:"Newsreader",serif; --f-text:"Public Sans",sans-serif; --f-mono:"IBM Plex Mono",monospace;
}
.slide{background:var(--paper);color:var(--ink);font-family:var(--f-text)}
.kicker{font:700 20px/1 var(--f-text);letter-spacing:.12em;text-transform:uppercase;color:var(--em)}
```

## 3. Polices

| Rôle | Google Fonts | Usage |
| --- | --- | --- |
| Titres | Newsreader (500 à 700) | Titres-conclusions (56 à 84 px), chapô (30 px), interligne 1.05 |
| Texte et graphiques | Public Sans (400, 600, 700) | Annotations (20 à 24 px), étiquettes, axes, chiffres des graphiques en `tabular-nums` |
| Notes | IBM Plex Mono (400) | Sources, méthode, "Lecture :", unités (18 à 20 px) |

Alternatives : Source Serif 4 pour les titres, Inter pour les graphiques.

## 4. Éléments signature

- **Surtitre coloré** au-dessus du titre (ENQUÊTE, MOBILITÉ, MARCHÉ), qui joue le rôle de sous-titre de section.
- **Titre qui conclut** : une phrase avec la découverte, et le chiffre dedans.
- **Annotations directes** : un texte court posé sur le graphique, relié au point par un filet fin. Pas de légende séparée quand on peut étiqueter directement.
- **Ligne "Lecture :"** sous les graphiques complexes : "Lecture : en 2025, 42 % des trajets de moins de 3 km se font en voiture."
- **Pied de slide** : "Source : Insee, enquête mobilité 2025 · Traitement : auteur" à gauche, numéro de page à droite.
- **Petits multiples** : la même mini-courbe répétée par catégorie plutôt qu'un graphique illisible à 8 couleurs.

## 5. Traitement des images

- Presque pas de photos : le graphique est l'image. 1 slide sur 6 au plus porte une photo.
- Si une photo sert de preuve (un terrain, un lieu), préréglage `doc` : documentaire, désaturé, sans dégradé. Petit format, légendée et sourcée comme une pièce du dossier.
- Les cartes sont dessinées en SVG à partir de vraies géométries (GeoJSON), en gris avec la zone d'intérêt en emphase.
- Graphiques en SVG, générés par un script (Python ou JS) à partir des données : un script de build lit le CSV et écrit le SVG ou injecte les valeurs. Aucun chiffre recopié à la main.

```bash
python scripts/images.py traiter raw/terrain.jpg assets/terrain.jpg --taille 720x480 --preset doc
```

## 6. Mise en page et animations

- Titre en haut à gauche sur 2 lignes au plus, chapô dessous, graphique sur 70 % de la slide, pied de slide.
- Le graphique respire : marges internes généreuses, 4 ou 5 lignes de grille, axes discrets, étiquettes directes.
- Une forme par message :
  - courbe pour une évolution dans le temps ;
  - barres horizontales classées pour comparer des catégories ;
  - dumbbell ou slope chart pour avant / après ;
  - waffle (100 carrés) pour une proportion ;
  - nuage de points annoté pour une relation ;
  - petits multiples pour comparer des profils.
- Animations qui servent la lecture : la courbe se dessine (`stroke-dashoffset` de 1 à 0), les barres poussent (`wipe`), puis l'annotation apparaît (`fade`, 300 ms après). Jamais d'animation décorative.

## 7. Bibliothèque de layouts

| Contenu | Layout | Astuce |
| --- | --- | --- |
| Cover | Titre-question + un graphique "teaser" en grand, une seule série en emphase | La réponse arrive plus loin |
| Chiffre clé | Grand chiffre (280 px) + phrase de contexte + comparaison | "C'est 3 fois plus qu'en 2015" |
| Évolution | Courbe annotée, la série clé en emphase, les autres en gris | 2 ou 3 annotations datées |
| Classement | Barres horizontales triées, valeur au bout | Une barre en emphase |
| Avant / après | Dumbbell ou slope chart entre deux dates | Étiquettes aux deux extrémités |
| Proportion | Waffle de 100 carrés | "Sur 100 trajets..." |
| Comparaison de profils | Petits multiples (6 à 12 mini-graphiques) | Même échelle partout |
| Territoire | Carte choroplèthe ou à symboles proportionnels | Gris clair + emphase, légende courte |
| Relation | Nuage de points annoté, droite de tendance discrète | Nommer 3 points remarquables |
| Parcours, flux | Sankey ou diagramme de flux simplifié | 5 flux au plus |
| Chronologie | Frise horizontale avec événements et une courbe en fond | Les dates en mono |
| Tableau | Tableau classé avec mini-barres ou sparklines | Lignes zébrées très légères |
| Témoignage | Citation d'enquêté + chiffre qui la confirme | La citation en Newsreader italique |
| Méthode | Note de méthode : sources, échantillon, limites | Mono, deux colonnes |
| Conclusion | "Ce qu'il faut retenir" : 3 chiffres et 3 phrases | Chaque chiffre renvoie à sa slide |

## 8. Ton des textes

- Le titre affirme la découverte : "Les trajets courts restent motorisés à 42 %", pas "Mobilité urbaine".
- Chapô : une phrase qui donne le contexte et la nuance.
- Annotations factuelles, au présent, 10 mots au plus.
- Toute mesure est définie la première fois. Toute source est citée.
- Pas d'effet de manche : la sobriété fait la crédibilité.

## 9. Interdits spécifiques

- Plus d'une couleur d'emphase par graphique (le bleu de contraste seulement pour opposer deux groupes).
- Camemberts à plus de 3 parts, graphiques 3D, doubles axes trompeurs, axes qui ne partent pas de zéro pour des barres.
- Légende séparée quand on peut étiqueter directement.
- Un chiffre sans source, une échelle sans unité.
- Icônes à la place des données (sauf waffle).

## 10. Check avant de livrer

- [ ] Chaque titre affirme une découverte et contient un chiffre quand c'est possible.
- [ ] Chaque graphique : une forme adaptée au message, une seule emphase, annotations directes.
- [ ] Chaque chiffre vient d'un fichier de données, pas d'une saisie manuelle.
- [ ] Source et numéro de page sur chaque slide.
- [ ] Les couleurs restent distinctes en simulation de daltonisme.
- [ ] Les graphiques se lisent projetés : étiquettes de 20 px minimum.
