# Style "Heure bleue"

## 1. L'idée et quand l'utiliser

**En une phrase** : un seul monde en 3D vit derrière toutes les slides, au crépuscule, et il se transforme au fil du récit (un immeuble qui se construit acte par acte, une ville qui s'allume) pendant que la caméra change de point de vue à chaque slide.

Référence d'origine : le pitch « Give the product away. Sell the preparation. » (stratégie IA pour un promoteur immobilier, dépôt `Exowz/nexity-ai-strategy`) : un immeuble fictif à l'heure bleue, d'abord dessin au-dessus d'une palissade, puis fondations, structure, façade, finitions, et enfin les fenêtres qui s'allument.

La différence avec Studio sombre : Studio sombre photographie un objet, slide par slide. Heure bleue fait vivre **un lieu** pendant tout le deck, et son évolution est la métaphore du récit (ce qui n'existe pas encore devient réel).

**Quand l'utiliser**
- Le sujet a un lieu ou un objet qui se construit : immobilier, ville, usine, magasin, campus, produit en fabrication, infrastructure.
- Un pitch en équipe de 15 à 25 minutes, devant un jury : l'effet tient sur la durée parce que le monde change à chaque acte.
- Quand on a le temps de développer (une à deux journées de plus qu'un deck classique).

**Quand l'éviter**
- Pas de lieu concret, ou un deck à livrer vite : préférer Studio sombre (un objet par slide) ou Data-journalisme.
- Un ordinateur de présentation faible ou inconnu : prévoir la version PDF (une image fixe par slide).

## 2. Palette

| Rôle | Hex | Règle |
| --- | --- | --- |
| Nuit | fond `#0B1433`, feuille `#142048`, hors cadre `#060A1C` | Le ciel et les panneaux de texte |
| Texte | `#F1F3F9`, secondaire `#B6BFD8`, légendes `#8590B2` | Jamais de blanc pur |
| Filets | `rgba(241,243,249,.16)` et `.32` | Séparateurs, axes |
| Lumière des fenêtres | `#FFC46B` | La phrase clé de chaque titre, le client, ce qu'il voit : la chaleur |
| Vermillon | `#FF6A45` | Uniquement nos décisions et les marques au crayon |
| Bleu plan | `#9DBCFF` | Le dessin de ce qui n'existe pas encore (traits du plan, palissade) |

- **Règle : deux accents seulement, chacun avec un sens.** L'ambre éclaire (la phrase clé, la personne), le vermillon tranche (ce que nous décidons). Le bleu plan n'apparaît que tant que le lieu n'est pas construit.
- La teinte du ciel suit le récit : bleu du soir au début, nuit franche et fenêtres allumées à la fin.

```css
:root{
  --nuit:#0B1433; --feuille:#142048; --g1:#F1F3F9; --g2:#B6BFD8; --g3:#8590B2;
  --filet:rgba(241,243,249,.16); --lumiere:#FFC46B; --crayon:#FF6A45; --plan:#9DBCFF;
  --f-titre:"Archivo Narrow",sans-serif; --f-texte:"IBM Plex Sans",sans-serif; --f-mono:"IBM Plex Mono",monospace;
  --ease:cubic-bezier(.22,1,.36,1);
}
```

## 3. Polices

| Rôle | Google Fonts | Usage |
| --- | --- | --- |
| Titres | Archivo Narrow (600) | Titres-affirmations de 60 à 72 px, interligne 1.02, à gauche ; chiffres héros |
| Texte | IBM Plex Sans (400, 500, 600, italique) | Corps 26 px, légendes 19 à 20 px, citations |
| Données | IBM Plex Mono (400, 500) | Annotations, sources, étiquettes épinglées |

## 4. Éléments signature

- **Le monde qui se construit** : une variable `build` de 0 à 5 par slide (0 dessin, 1 fondations, 2 structure, 3 façade, 4 fini, 5 allumé et habité). Le public voit le projet avancer en même temps que l'argument.
- **La caméra qui vole** entre deux slides, comme un drone : vue de rue, vue aérienne, plan du dessus, fenêtre d'un appartement.
- **Le titre qui monte mot par mot puis s'allume** : `data-anim="mots"` sur le titre et `<em class="allume">` sur la phrase clé, qui prend la lumière des fenêtres une fois les mots posés.
- **Les marques au crayon vermillon** : cercle autour d'un chiffre, soulignement, barré, coche, flèche (`svg.crayon`, voir SKILL.md, « Mise en scène »), pour nos décisions seulement.
- **Les étiquettes épinglées au monde** : une carte de texte reliée à un point du lieu (l'appartement B204, la grue), qui suit le point quand la caméra bouge.
- **Le texte à gauche, le monde à droite** : la caméra décale le point regardé vers la droite (`shift`) pour laisser la colonne de texte libre.

## 5. Traitement des images

- Pas de photos : tout est construit en code (three.js), comme dans l'annexe de `studio-sombre.md` (rendu ACES, couleurs passées par `lin()`, ombres douces).
- Une ville procédurale autour du lieu principal (blocs, fenêtres allumées au hasard, lampadaires, quelques voitures), pour l'échelle.
- Un **voile** sombre (`veil`) sur le monde et un **dégradé** sous le texte (`scrim` : à gauche, plein écran ou aucun) gardent la lecture : plus la slide est dense, plus le voile monte.
- Un léger halo (bloom) sur les lumières, coupé automatiquement si l'ordinateur rame.

## 6. Mise en page et animations

- Marges de 120 px ; titre en haut à gauche sur 1080 à 1680 px de large ; le contenu en colonne à gauche ou en panneaux semi-opaques (`rgba(6,10,28,.8)`, filet supérieur ambre).
- **Le changement de slide en trois temps** : l'ancien texte s'efface tout de suite (0,25 s), la caméra vole (1,2 à 2,6 s), le nouveau texte arrive quand elle se pose. Au premier slide d'un acte, le texte attend plus longtemps (le monde change de stade).
- **Les sous-étapes changent aussi la caméra** : une pose peut dépendre de l'étape en cours (vue de rue, puis recul au clic suivant).
- La caméra n'est jamais figée : une lente dérive autour du point regardé.
- Courbe : `cubic-bezier(.22,1,.36,1)`.

## 7. Bibliothèque de layouts

| Contenu | Layout | Astuce |
| --- | --- | --- |
| Cover | Le lieu à l'état de dessin bleu au-dessus du terrain, titre en deux lignes dont la seconde allumée | Le dessin dit « ça n'existe pas encore » |
| Problème | Vue de rue, trois chiffres en bas à gauche, un formulaire ou un obstacle épinglé au lieu | L'obstacle est un objet dans le monde |
| Marché, concurrents | Vue aérienne de toute la ville, voile fort, le lieu au centre | Les concurrents sont les autres immeubles |
| Parcours client | Caméra au ras de la rue, une étiquette épinglée par étape (chiffre + citation) | Un chiffre et une citation par étape |
| Atouts | Plan vu du dessus, numéros épinglés sur les zones, liste à gauche | Le cercle au crayon sur le chiffre qui compte |
| Tensions, choix | Fondations en cours, tableau à gauche, le choix entouré au crayon | Vermillon pour notre décision |
| Benchmark | Structure en cours, tableau « ce qu'on prend, ce qu'on laisse », lignes barrées au crayon | |
| Cas d'usage | Façade, bulles numérotées épinglées sur les fenêtres | Un cas d'usage = une fenêtre |
| Échelle, niveaux | Vue de l'immeuble étage par étage, un niveau par étage | Le niveau choisi en premier, le plus bas |
| Matrice | Voile fort, matrice impact × complexité en panneau, cercles au crayon | La grue en arrière-plan |
| Feuille de route | Finitions, frise sur trois niveaux, la grue s'en va | |
| Chiffre clé | Trois chiffres géants, le dernier entouré au crayon | Le monde en plongée, voile léger |
| Démo en direct | Caméra devant la fenêtre de l'appartement, la démo en iframe dans un téléphone | Prévoir une démo enregistrée si le serveur ne répond pas |
| Preuve | Fenêtres allumées, un chiffre avant → après, garde-fous en liste | |
| Demande | Trois décisions numérotées en vermillon, la phrase de la cover reprise | Le lieu fini et habité derrière |
| Annexes | Toute la ville la nuit, voile fort, tableaux denses | Après la slide de fin, pour les questions |

## 8. Ton des textes

- Titres-affirmations courts, souvent en deux temps, avec la phrase clé allumée : « Nexity vend des logements *qui n'existent pas encore*. »
- Un chiffre et une citation d'entretien côte à côte : la preuve chiffrée et la voix du terrain.
- Les décisions sont écrites comme des actions datées : « Libérer le plan, sur 10 programmes, en test A/B. »

## 9. Interdits spécifiques

- Plus de deux accents, ou l'ambre et le vermillon employés pour décorer.
- Un monde qui ne change pas d'un acte à l'autre : sans évolution, ce n'est qu'un fond animé.
- Du texte posé sur le monde sans voile ni dégradé : la lisibilité passe avant le décor.
- Une caméra qui bouge pendant que le texte arrive : le texte attend qu'elle se pose.
- Une démo en direct sans plan B (vidéo ou exécution enregistrée).

## 10. Check avant de livrer

- [ ] Chaque slide a sa pose de caméra, son stade de construction et son voile écrits dans la table des poses.
- [ ] Le monde évolue entre les actes : le public peut dire où en est le projet en regardant le fond.
- [ ] Une seule phrase allumée par titre ; le vermillon seulement sur nos décisions.
- [ ] Le texte reste lisible sur chaque pose (rendu de chaque slide, et de chaque sous-étape quand la caméra change).
- [ ] Le PDF de secours montre une image fixe du monde par slide.
- [ ] Le deck tourne sur l'ordinateur de présentation, voile et halo compris, ou se dégrade proprement.

---

## Annexe technique : le monde persistant

Le monde est un `<canvas id="monde">` en `position:fixed` derrière les slides, hors des sections, et les slides ont un fond transparent. L'export (`scripts/export.py`) émet un événement à chaque changement de slide ou de sous-étape :

```js
document.addEventListener('deck:slide', e => {
  const { i, etape, pose } = e.detail;          // pose = data-pose de la slide, en JSON
  const p = Object.assign({}, POSES[i] || {}, pose ? JSON.parse(pose) : {});
  volerVers(p, etape);                           // caméra, stade, voile
});
```

**La table des poses**, une ligne par slide (c'est là qu'on règle un cadrage) :

```js
// build : 0 dessin · 1 fondations · 2 structure · 3 façade · 4 fini · 5 allumé
// shift : décalage du point regardé à l'écran (0 centre, .3 à droite) pour libérer le texte à gauche
const POSES = [
  { pos:[44,5,50],   look:[-4,9,0], build:0, shift:.22, fov:38, voile:0,   scrim:'gauche' },  // 1 cover
  { pos:[-120,95,170], look:[0,0,0], build:0, shift:.05, fov:32, voile:.35, scrim:'plein' }, // 3 la ville
  { pos:[40,7,50],   look:[2,9,0],  build:5, shift:.24, fov:36, crepuscule:1, duree:2.6 },    // 15 tout s'allume
];
```

Une pose peut dépendre de la sous-étape : `pose: etape >= 2 ? vueA : vueB`.

**Le vol de caméra** : interpoler position, cible et champ avec un amorti (`1-(1-k)**3`) sur `duree` secondes (1,2 par défaut, 2,6 pour un changement d'acte), puis une dérive lente autour de la cible pour que le monde ne soit jamais figé. Le stade `build` s'anime aussi : les éléments d'un stade montent du sol ou apparaissent en fondu.

**Les étiquettes épinglées** : projeter chaque point 3D à l'écran à chaque image (`vecteur.project(camera)`), puis placer l'élément HTML à ces coordonnées dans le repère 1920x1080 de la slide.

**La qualité adaptative** : mesurer la durée des images ; si plus de 90 images dépassent 30 ms, couper le halo, puis baisser la résolution. Un ordinateur faible garde un monde fluide.

**L'impression** : avec `?print=1`, rendre une image fixe du monde pour chaque pose et la poser en fond de la slide, pour que le PDF de secours soit complet.

**L'audit** : rendre chaque slide et, quand la caméra change pendant les sous-étapes, chaque étape. `rendu.py` signale les textes qui se chevauchent ou débordent sur l'état final ; pour les états intermédiaires, regarder les captures.
