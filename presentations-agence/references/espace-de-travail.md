# Style "Espace de travail"

## 1. L'idée et quand l'utiliser

**En une phrase** : chaque slide est une page d'un espace de travail collaboratif (bases de données en tableau ou en kanban, frises, surligneurs pastel, notes manuscrites) : le projet se montre en train d'être piloté, preuves à l'appui.

Univers de référence : les outils de travail en équipe de type Notion, leurs bases de données (vues Tableau, Tableau de bord, Chronologie, Galerie), leurs surligneurs et leurs étiquettes pastel. Référence d'origine : le deck « Can Singulier. open in 84 days, before Valentine's Day? » (gestion de projet, une parfumerie à ouvrir en 84 jours).

**Quand l'utiliser**
- Gestion de projet, plan de lancement, feuille de route, soutenance de projet en équipe, cas d'école en mode projet (backlog, sprints, budget, risques, RACI).
- Un public qui veut voir la méthode : jury de gestion de projet, comité de pilotage, client qui achète une organisation.
- Quand les preuves sont des objets de pilotage : un backlog, un Gantt, une matrice des risques, un budget.

**Quand l'éviter**
- Une marque à forte image (mode, luxe) : l'interface prend le dessus sur le produit. Mettre plutôt l'univers du produit en ouverture et en fermeture.
- Un public allergique aux outils (grand public, conférence) : préférer Une de journal ou Objet réel.

## 2. Palette

| Rôle | Hex | Règle |
| --- | --- | --- |
| Fond | `#FFFFFF`, secondaire `#F7F6F3` | Blanc pour les slides, gris chaud pour les colonnes et les cartouches |
| Encre | `#191918`, texte `#37352F`, gris `#787774` | Jamais de noir pur |
| Filets | `#E8E7E3` | Bords des bases de données, séparateurs de lignes |
| Surligneurs de titre | jaune `#FFE89E`, menthe `#D4F4EA`, violet `#EAD9FF`, bleu `#D1EAFF`, pêche `#FFE0C8`, rouge `#FADAD9` | Un seul surligneur par titre, sur le groupe de mots qui porte la preuve |
| Panneaux de section | jaune `#FFE18C`, violet `#E1C9FF`, bleu `#BFE0FF`, vert `#BCEFC9`, pêche `#FFD5B4` | Une couleur par partie, dans cet ordre, pour tout le deck |
| Étiquettes | paires texte / fond : orange `#D9730D` / `#FBECDD`, vert `#448361` / `#EDF3EC`, bleu `#337EA9` / `#E7F3F8`, violet `#9065B0` / `#F6F3F9`, rouge `#D44C47` / `#FDEBEC`, gris `#787774` / `#F1F1EF` | Les statuts et catégories des bases de données, jamais décoratives |
| Intertitre | rouge `#D44C47` | L'intertitre manuscrit au-dessus du titre |

- **Règle : le surligneur est le seul aplat de couleur vive d'une slide de contenu.** Les étiquettes restent pâles, la base de données reste blanche.
- La couleur du surligneur peut changer d'une slide à l'autre (c'est le rythme du deck) ; la couleur des panneaux suit l'ordre des parties.

```css
:root{
  --bg:#FFFFFF; --bg2:#F7F6F3; --ink:#191918; --text:#37352F; --muted:#787774; --rule:#E8E7E3;
  --nh-jaune:#FFE89E; --nh-menthe:#D4F4EA; --nh-violet:#EAD9FF; --nh-bleu:#D1EAFF; --nh-peche:#FFE0C8; --nh-rouge:#FADAD9;
  --f-sans:"Inter",system-ui,sans-serif; --f-serif:"Instrument Serif",Georgia,serif;
  --f-main:"Caveat",cursive; --f-mono:"IBM Plex Mono",monospace;
}
```

Le `style.css` complet (classes `.tete`, `.kicker`, `.titre`, `.preuve`, `.base`, `.onglets`, `table.tb`, `.tag`, `.colonnes`, `.carte`, `.panneau`, `.question`) est dans `gabarits/espace-de-travail/`.

## 3. Polices

| Rôle | Google Fonts | Usage |
| --- | --- | --- |
| Interface | Inter (400 à 700) | Titres (64 px, graisse 600, interlettrage -.022em), texte des bases de données, étiquettes |
| Serif | Instrument Serif (romain et italique) | Covers, questions, titres de partie, grands chiffres de cartouche |
| Main | Caveat (600, 700) | Intertitres en capitales, numéros de partie, annotations sur les graphiques |
| Code | IBM Plex Mono (400, 500) | Méta des bases de données, identifiants (`US-18`, `RSK-1`), pieds de slide |

## 4. Éléments signature

- **L'en-tête en trois lignes, centré en haut** : intertitre manuscrit rouge en capitales, titre-affirmation en Inter avec un surligneur pastel qui se trace, ligne de preuve avec les chiffres en gras. C'est la seule partie centrée : le contenu en dessous est un objet.
- **La fenêtre de base de données** : icône, nom de la base, méta en mono à droite (« 16 actives · 73 pts · 1 exclue »), onglets de vue (Tableau, Tableau de bord, Chronologie) avec l'onglet actif souligné.
- **Les identifiants** en code (`US-18`, `RSK-1`) repris dans le titre ou la ligne de preuve : ils relient l'affirmation à la ligne de la base.
- **Les intercalaires en panneau** : un grand rectangle arrondi de couleur pastel, le numéro de partie manuscrit, le titre en serif.
- **Une carte barrée** dans les kanbans : ce que l'équipe refuse de faire.

## 5. Traitement des images

- Peu de photos : les objets de pilotage sont les images. Une photo, si elle sert, est rectangulaire, coins arrondis de 12 px, préréglage `neutre`, posée comme une image collée dans une page.
- Les plans, cartes et schémas se dessinent en traits fins et aplats pastel. Un plan d'espace peut être une scène 3D isométrique claire (même technique que l'annexe de `studio-sombre.md`, sur fond blanc et matières crème), avec étiquettes arrondies pointant les zones.
- Captures d'écran réelles de l'outil : nettes, dans une fenêtre aux coins arrondis, jamais dans une maquette d'ordinateur.

## 6. Mise en page et animations

- En-tête fixe en haut (64 à 300 px), objet de preuve en dessous sur 1480 px de large, pied de slide en mono.
- Les objets ont la taille de vrais écrans : une base de données lisible, 5 à 8 lignes, 3 à 5 colonnes de kanban.
- **Visuel persistant** : quand plusieurs slides de suite parlent du même objet (le même plan, la même matrice), garder l'objet et changer seulement son état (zone surlignée, angle de caméra, avant puis après) : donner le même `view-transition-name` à l'objet sur ces slides, l'export le fait glisser d'un état à l'autre au lieu de couper.
- **Sous-étapes** : les lignes d'un tableau ou les cartes d'une file apparaissent une à une avec `data-etape="1"`, `"2"`… avant de passer à la slide suivante.
- Le surligneur se trace de gauche à droite 350 ms après l'arrivée du titre (`mark.surligneur`, voir `assets/base.css`) ; les titres de partie arrivent mot par mot (`data-anim="mots"`).
- Courbe d'animation de l'outil : `cubic-bezier(.2,0,0,1)`, entrées courtes (0,45 à 0,6 s), rien qui rebondit.

## 7. Bibliothèque de layouts

| Contenu | Layout | Astuce |
| --- | --- | --- |
| Cover | Le nom en grand serif sur un panneau pastel, une icône au trait au-dessus | Le panneau de la cover reprend la couleur de la première partie |
| Question d'ouverture | La question du deck en grand serif, deux mots surlignés | La réponse arrive à la dernière slide |
| Intercalaire | Panneau pastel arrondi plein cadre, numéro manuscrit, titre en serif | Une couleur par partie |
| Chiffre clé | Grand chiffre serif avec surligneur, une ligne de contexte, puis l'objet qui le prouve en sous-étape | Le chiffre d'abord, l'objet ensuite |
| Répartition, budget | Cartouches de chiffres au-dessus d'une base en vue Tableau | La ligne qui compte en surligné jaune pâle |
| Backlog, priorités | Base en vue kanban par priorité (indispensable, important, plus tard, exclu) | Une carte surlignée, une carte barrée |
| Planning | Base en vue Chronologie (Gantt) : couloirs par équipe, jalons en losange | Le jalon final en étiquette rouge |
| Sprints, avancement | Courbe d'avancement (burn-up) fine avec annotations manuscrites | Le point du jour en noir, la cible en pointillé |
| Capacité d'équipe | Tableau personnes × semaines, cellules avec charge et tâche | La colonne du pic en surligné |
| Risques | Matrice probabilité × impact en pastels, avant puis après les parades | Même `view-transition-name` sur les points : ils glissent vers leur nouvelle case |
| Rôles, décisions | Matrice RACI en tableau, pastilles A et R | Une seule pastille A par ligne |
| Parties prenantes | Carte pouvoir × intérêt en quatre quadrants pastel | Les noms en étiquettes |
| Processus, escalade | File de cartes reliées par des flèches fines, une couleur par niveau | Le délai de chaque niveau en mono |
| Plan d'espace | Plan 3D isométrique clair, zones étiquetées, caméra qui se déplace d'une slide à l'autre | Même objet sur plusieurs slides, seul le point de vue change |
| Démo | Panneau pastel plein cadre « Démo », titre en serif flou qui se net | Le moment où l'on quitte les slides |
| Closing | La réponse à la question d'ouverture, trois feux verts en étiquettes | Reprendre les mots surlignés de l'ouverture |

## 8. Ton des textes

- Titres courts en deux temps, souvent avec un point au milieu : « 73 points pour ouvrir. Zéro e-commerce. »
- La ligne de preuve est dense et précise : chiffres en gras, identifiants en code, unités écrites.
- Les intertitres manuscrits sont parlés et brefs : « ce qu'on refuse », « ce qui pourrait mal tourner ».
- Les notes d'orateur sont minutées : `[00:42 à 01:05 · Slide 04]` en tête, utile quand le temps de passage est imposé.

## 9. Interdits spécifiques

- Plus d'un surligneur par titre, ou un surligneur sur un mot sans preuve.
- Des captures floues de l'outil, ou une fausse interface qui imite exactement une marque réelle (logos, noms de produit) : c'est l'esprit de l'outil, pas sa copie.
- Des étiquettes de couleur sans signification (statut, priorité, catégorie).
- Des bases de données illisibles projetées : 16 px minimum dans les cellules, 5 à 8 lignes au plus.
- Des ombres fortes : la fenêtre a une ombre à peine visible, le reste est plat.

## 10. Check avant de livrer

- [ ] Chaque slide de contenu a l'en-tête en trois lignes et un objet de pilotage réel en dessous.
- [ ] Un seul surligneur par titre, posé sur la preuve.
- [ ] Les identifiants cités dans les titres existent dans les bases montrées.
- [ ] Les intercalaires suivent l'ordre des couleurs de panneau.
- [ ] Quand un objet revient sur plusieurs slides, il porte le même `view-transition-name` et ne fait que changer d'état.
- [ ] Les bases de données restent lisibles projetées (16 px minimum).
