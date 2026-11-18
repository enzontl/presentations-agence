# Style "Studio sombre"

## 1. L'idée et quand l'utiliser

**En une phrase** : le sujet devient un objet 3D photographié en studio sur un fond sans raccord, et les slides de données gardent l'ambiance du studio (fond nuit, lumière d'en haut, objets flous au premier plan).

Référence d'origine : le deck "Are LEGO themes real universes?" (dépôt lego-universes, `slides/template.html`).

**Quand l'utiliser**
- Le sujet a un objet physique emblématique : une brique, une bouteille, une canette, une chaussure, une puce, un livre.
- Le public est un jury, une soutenance, un comité ou des investisseurs : on veut un rendu "produit premium", sérieux, pas ludique.
- Il y a des données à montrer, avec peu de texte par slide.

**Quand l'éviter**
- Le sujet n'a pas d'objet concret, ou l'objet est trop complexe à modéliser en formes simples (un visage, un animal, un vélo).
- Le deck doit être très dense (rapport de 40 slides).

### Les deux types de slides

**Slide "objet"** (ouverture, une slide de contexte, conclusion) : la scène 3D, l'objet décalé à droite ; le titre et une phrase d'accroche à gauche ; une ligne de 2 ou 3 chiffres clés sous l'accroche.

**Slide "données"** (tout le reste) : un graphique à gauche (1080 px de large), une colonne de texte à droite (510 px). En fond, trois rappels du studio : un dégradé radial bleu venant d'en haut à droite comme un spot, 3 objets flous dans les coins, un grain et un vignettage.

Règle : **3 slides objet maximum sur 10**, sinon l'effet s'use.

## 2. Palette

| Rôle | Hex | Règle |
| --- | --- | --- |
| Fond | `#0B0A09`, dégradé `#0C1631` vers `#06080E` | Toujours le même dégradé sur les slides données |
| Spot | `rgba(44,92,190,.55)` | Radial en haut à droite, accordé avec la matière du cyclo `#163A78` |
| Texte principal | `#EFE9DF` | Blanc cassé chaud, jamais `#FFFFFF` |
| Texte secondaire | `#C9C2B6` | Accroches, corps |
| Légendes | `#948D82` | Sources, pied de page |
| Filets | `rgba(239,233,223,.12)` | Lignes entre les valeurs |
| Grille | `rgba(239,233,223,.08)` | Grille des graphiques |
| Accents (2 à 4) | tirés du sujet, ex. `#DA291C`, `#FFCD00`, `#078BC9`, `#4B9F4A` | Un rôle chacun, voir la règle |

**Règle des accents** : ils viennent du sujet (couleurs de la marque, de l'objet), jamais d'une palette générique. Chaque accent a un seul rôle : un accent pour le mot clé du titre, un pour la barre de progression (3 px en bas), et dans les graphiques la couleur porte une information (observé contre hasard, une catégorie). Jamais de couleur décorative.

**Le bleu du fond** se règle à deux endroits qui doivent rester accordés : le dégradé CSS des slides données et la couleur de la matière du cyclo 3D.

```css
:root{
  --bg:#0b0a09; --ink:#efe9df; --ink2:#c9c2b6; --mut:#948d82;
  --line:rgba(239,233,223,.12); --grid:rgba(239,233,223,.08); --gray:#6f685f;
  --hl:#ffcd00; --bar:#da291c; --c1:#078bc9; --c2:#4b9f4a;
  --ease:cubic-bezier(.16,1,.3,1); --f:"Archivo",sans-serif;
}
.slide{background:radial-gradient(ellipse 85% 95% at 72% 0%,rgba(44,92,190,.55),transparent 72%),linear-gradient(#0c1631,#06080e);color:var(--ink);font-family:var(--f)}
```

## 3. Polices

Une seule famille, variable en graisse et en largeur, avec trois rôles. C'est un choix voulu : la sobriété typographique laisse toute la place à l'objet. Ajouter une deuxième famille casserait l'effet "photo produit".

| Rôle | Google Fonts | Réglages |
| --- | --- | --- |
| Titres | Archivo (alternatives : Bricolage Grotesque, Mona Sans) | `h1` 100 px, graisse 820, largeur 112 %, interligne .98, interlettrage -.022em ; `h2` 62 px, graisse 780, largeur 108 % ; `text-wrap:balance` |
| Chiffres héros | Archivo | 120 px, graisse 800, interlettrage -.035em, `tabular-nums` |
| Texte et légendes | Archivo, largeur 100 % | Accroche 31 px (`--ink2`, 32 caractères max de large) ; corps 24 px, interligne 1.45 ; pied de page 19-20 px (`--mut`) |

Charger la police avec ses axes : `python scripts/polices.py "Archivo:wdth,wght@62..125,100..900"`. Dans l'export autonome, elle est intégrée en base64.

## 4. Éléments signature

- **L'objet en studio** sur fond sans raccord, lumière de boîte à lumière venue d'en haut, ombre de contact douce.
- **Mot clé du titre en accent** : un seul groupe de mots par titre (`<span class="hl">`).
- **Barre de progression** de 3 px en bas, couleur accent.
- **Objets flous** dans les coins des slides données (rendus une fois en image, puis floutés).
- **Pied de page** : à gauche le fichier source des chiffres (`results/xxx.csv`), à droite "03 / 10".
- **Grain et vignettage** sur toutes les slides.

## 5. Traitement des images

- Pas de photo d'Unsplash en principe : l'image, c'est l'objet 3D construit en code (voir l'annexe). C'est ce qui rend le style unique.
- Si une photo est indispensable (contexte, lieu), préréglage `studio` : froid, contraste relevé, dégradé sombre fort. Elle doit sembler éclairée par la même lumière.
- Objets flous : un renderer hors écran (420x420) photographie chaque objet une seule fois (`toDataURL`), puis on le pose en `<img class="bgb bleed">` (la classe `bleed` évite une fausse alerte du rendu) : `filter:blur(10px); opacity:.6`, 300 à 440 px, rotation de 12 à 24°, à moitié hors cadre. Aucune 3D en continu sur ces slides.
- Grain de pellicule et vignettage en calque CSS sur toutes les slides.

## 6. Mise en page et animations

- Scène 1920x1080. Marges : 112 px en haut et en bas, 120 px sur les côtés.
- Slide données : titre en haut ; figure en `left:120px; top:330px; width:1080px; height:600px` ; colonne en `left:1290px; top:330px; width:510px`. Pied de page à 48 px du bas.
- Slide objet : titre et accroche à gauche (jusqu'à 860 px), objet à droite (`x = 3.3` dans la scène).
- Texte toujours aligné à gauche.
- Fondu de 0,6 s entre les slides. Entrées en cascade avec `--i` (90 ms d'écart ici) et la courbe `--ease`.
- Lignes de graphique qui se dessinent : `pathLength="1"`, `stroke-dasharray:1`, `stroke-dashoffset` de 1 à 0.
- Objet 3D : rotation presque imperceptible (`rotation.y = -.62 + t*.00009`), atterrissage avec amorti cubique, son ombre apparaît au contact.

### Graphiques

- Faits à la main en SVG ou HTML, à partir des vraies données : un script de build injecte les données et remplace les `{{clés}}` du texte. Aucun chiffre recopié à la main.
- Marques fines, étiquettes directes sur les points importants, 4 ou 5 lignes de grille au maximum.
- Infobulle (`<title>`) sur chaque marque, avec la valeur exacte.

## 7. Bibliothèque de layouts

| Contenu | Layout | Astuce |
| --- | --- | --- |
| Cover | Slide objet : objet à droite, titre + accroche + 3 chiffres à gauche | L'objet tombe et se pose à l'ouverture |
| Contexte | Slide objet avec caméra plus basse | Couper le halo quand la caméra plonge vers le sol |
| Chiffre clé | Chiffre héros 120 px + phrase de définition, objets flous autour | Le chiffre dans la couleur accent du titre |
| Comparer des scores | Barres horizontales | Valeur au bout de chaque barre |
| Observé contre référence | Dumbbell (deux points reliés) | Gris pour la référence, accent pour l'observé |
| Choix d'un paramètre | Courbe avec un seul point mis en avant | Annotation directe du point retenu |
| Évolution | Colonnes sur 3 à 5 périodes | Dernière colonne en accent |
| Tailles de groupes | Points, un par individu | Groupes séparés par du vide, pas par des boîtes |
| Réseau, espace | Graphe ou nuage de points 3D | Pas de studio : `HemisphereLight` .5 + `DirectionalLight` .9 |
| Avant / après | Deux objets côte à côte sur le cyclo | Même lumière, l'ancien en gris |
| Gamme | 3 à 5 objets alignés sur le cyclo, tailles réelles | Étiquettes sous les objets, en `--mut` |
| Anatomie | Objet éclaté, pièces séparées verticalement | Une étiquette par pièce, reliée par un filet |
| Méthodologie | Colonne de texte large + objets flous | Définir chaque mesure en une ligne |
| Statement | Objet seul, une phrase | Aucune donnée |
| Conclusion | Slide objet, 3 chiffres clés | Reprend la cover, caméra différente |

## 8. Ton des textes

- **Le titre est la conclusion de la slide**, en une phrase complète : "L'époque façonne le graphe plus que le thème", pas "Résultats".
- Un seul groupe de mots en accent par titre.
- Colonne de droite : un chiffre héros, une phrase qui dit ce qu'il mesure, puis 2 à 4 lignes clé / valeur séparées par des filets de 1 px.
- Toute mesure est définie en une ligne la première fois qu'elle apparaît.
- Ton sobre, factuel, assuré. Pas d'humour, pas de point d'exclamation.

## 9. Interdits spécifiques

- Plus de 3 slides objet sur 10.
- Cartes en dégradé, glassmorphism, ombres portées colorées.
- Plusieurs familles de polices.
- Une couleur sans rôle, ou un accent qui ne vient pas du sujet.
- Des arêtes vives sur l'objet 3D, des ombres de three.js (bords durs ou bruités), une lumière colorée pour teinter le fond.
- Objets flous qui passent sous un texte ou un graphique.

## 10. Check avant de livrer

- [ ] Chaque titre est une phrase qui affirme la conclusion de la slide.
- [ ] Un seul mot ou groupe de mots en accent par titre.
- [ ] Chaque chiffre vient des données (aucun recopié), source en pied de page.
- [ ] Le fond CSS et la matière du cyclo ont le même bleu.
- [ ] Les objets 3D n'ont aucune arête vive et ont une ombre de contact.
- [ ] Les objets flous ne passent sous aucun texte ni graphique.
- [ ] `?print=1` donne le même rendu à chaque fois (graines fixes).
- [ ] Chaque slide regardée en taille réelle avant de livrer.

---

## Annexe technique : le studio 3D (three.js)

Tout est construit en code, sans modèle importé ni HDRI. Une seule fonction `studio(id, camPos, camTgt, options)` monte le studio ; chaque slide objet l'appelle avec sa caméra et y pose ses objets. three.js est chargé depuis un CDN versionné (ex. `https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.min.js`) puis intégré par `export.py`.

### Rendu

```js
const r=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true,preserveDrawingBuffer:true});
const PRINT=location.search.includes('print=1');
r.setPixelRatio(PRINT?1.5:Math.min(devicePixelRatio,2));
r.outputEncoding=THREE.sRGBEncoding;
r.toneMapping=THREE.ACESFilmicToneMapping; r.toneMappingExposure=1.0;
const lin=hex=>new THREE.Color(hex).convertSRGBToLinear(); // toutes les couleurs passent par là
```

ACES donne des hautes lumières douces, comme une photo. Sans `lin()`, les couleurs de la marque sortent délavées.

### Caméra

`PerspectiveCamera(26°)` : focale serrée de photo produit, peu de déformation. Un peu au-dessus du sujet, qui regarde légèrement vers le bas : `[0, 2.3, 15.5]` vers `[0, .25, 0]`. Sujet décalé du côté opposé au titre (`x = 3.3`).

### Reflets : des boîtes à lumière virtuelles

Une petite scène invisible, convertie en carte d'environnement. C'est le détail qui fait passer de "rendu 3D" à "photo".

```js
const pm=new THREE.PMREMGenerator(r), st=new THREE.Scene();
st.add(new THREE.Mesh(new THREE.BoxGeometry(40,40,40),
  new THREE.MeshBasicMaterial({color:0x050404,side:THREE.BackSide})));          // studio éteint
const panel=(w,h,col,p)=>{ const m=new THREE.Mesh(new THREE.PlaneGeometry(w,h),
  new THREE.MeshBasicMaterial({color:col,side:THREE.DoubleSide})); m.position.set(...p); m.lookAt(0,0,0); st.add(m); };
panel(14,14,new THREE.Color(2.3,2.1,1.85),[2,12,3]);    // grande boîte à lumière au plafond, chaude
panel(10,12,new THREE.Color(.5,.47,.44),[-13,2,6]);     // débouchage à gauche, faible
panel(14,1.6,new THREE.Color(1.2,1.5,2.1),[8,3,-12]);   // bande froide derrière : liseré sur les arêtes
scene.environment=pm.fromScene(st,.04).texture;
```

### Fond sans raccord (cyclo)

Un plan de 60x40 à 200 segments, déformé pour que le sol remonte en mur par un quart de cercle. **Colorer le fond par sa matière, pas par une lumière colorée** : un spot à gélatine bleue n'éclaire qu'une tache au sol.

```js
const F=-1.1, BX=3.3, R=5, L=18, A=Math.PI*R/2;      // hauteur du sol, centre, rayon de la courbe
const sw=new THREE.PlaneGeometry(60,40,1,200), pa=sw.attributes.position;
for(let i=0;i<pa.count;i++){ const s=pa.getY(i)+20; let y,z;
  if(s<L){ z=12-s; y=F; }                                                  // sol
  else if(s<L+A){ const a=(s-L)/R; z=12-L-R*Math.sin(a); y=F+R*(1-Math.cos(a)); } // courbe
  else { z=12-L-R; y=F+R+s-L-A; }                                          // mur
  pa.setXYZ(i,pa.getX(i)+BX,y,z); }
sw.computeVertexNormals();
scene.add(new THREE.Mesh(sw,new THREE.MeshStandardMaterial(
  {color:lin(0x163a78),roughness:1,metalness:0,envMapIntensity:.04})));
```

### Lumières (trois seulement)

```js
const key=new THREE.SpotLight(0xffe6c4,5.5,45,.46,1,1.5);  // chaude, bord très doux, chute réaliste
key.position.set(BX+1.2,11,3); key.target.position.set(BX,F,-1);
const wall=new THREE.SpotLight(0xffdcb4,1.6,50,.5,1,1);    // dégradé sur le mur, détache l'objet du fond
wall.position.set(BX-.5,7,6); wall.target.position.set(BX,1.2,-11);
scene.add(key,key.target,wall,wall.target,new THREE.HemisphereLight(0xfff2e2,0x080504,.08)); // ambiance presque nulle
```

La key light est haute, au-dessus du sujet. Ambiance à 0.08 : des ombres profondes, c'est voulu. Options par slide : cible, position, angle et intensité de la key light.

### Atmosphère

- **Halo** : un plan de 8x14 au-dessus du sujet, texture en dégradé radial chaud (opacité .20 au centre, 0 au bord), `AdditiveBlending`, `depthWrite:false`, `toneMapped:false`. À couper quand la caméra plonge vers le sol.
- **Poussière** : 240 points qui montent lentement, densité gaussienne autour de l'axe de la lumière, teintés chaud, taille .04, mélange additif.
- **Tirage aléatoire à graine fixe** (`sd=(sd*16807)%2147483647`) : chaque export donne la même image.

### Modèle de l'objet

- Aucune arête vive : biseau sur toutes les extrusions (`bevelThickness:.04, bevelSegments:4`).
- Pièces de révolution (canette, bouteille, tenon) en `LatheGeometry` sur un profil, 48 segments, avec un petit chanfrein.
- Une matière physique proche du vrai matériau, avec un léger vernis. Mettre les matières en cache par couleur.

```js
const absMat=hex=>new THREE.MeshPhysicalMaterial({color:lin(hex),roughness:.36,metalness:0,
  clearcoat:.25,clearcoatRoughness:.4,envMapIntensity:1});            // plastique ABS
const STUD=new THREE.LatheGeometry([[0,0],[.3,0],[.3,.165],[.296,.185],[.284,.197],[.265,.2],[0,.2]]
  .map(([x,y])=>new THREE.Vector2(x,y)),48);                           // tenon avec chanfrein
```

Étiquette imprimée (canette, bouteille) : une texture canvas sur la `LatheGeometry`. Le `v` de la texture suit l'indice des points du profil, pas la longueur : peindre l'étiquette entre `v0 = premier point du flanc / (N-1)` et `v1 = dernier point du flanc / (N-1)`, et l'alu nu ailleurs. `u = 0` regarde vers la caméra (+z) : tourner l'objet de `-(angle du centre du logo)` pour que la marque soit face à l'objectif, avec un léger quart de tour pour garder du relief. Attendre `document.fonts.load()` avant de dessiner le texte sur le canvas.

Matières utiles : aluminium de canette (`metalness:1, roughness:.28`), verre (`MeshPhysicalMaterial` avec `transmission:1, roughness:.05, thickness:.4`), papier et carton (`roughness:.85`, pas de vernis), plastique (ci-dessus).

### Ombres sans shadow maps

Sous chaque objet, un plan avec une texture canvas faite de trois rectangles (ou ellipses) flous superposés : une large et légère, une moyenne, une serrée et sombre au contact. Plus belle et plus rapide que les ombres de three.js. Plan posé à `y=.003` avec `polygonOffset`.

```js
// [flou relatif, opacité, agrandissement]
[[.9375,.55,1.3],[.25,.7,1.06],[.046875,.95,1.005]].forEach(([u,a,k])=>{
  ctx.filter=`blur(${u*px}px)`; ctx.fillStyle=`rgba(0,0,0,${a})`;
  ctx.fillRect(-w*px*k/2,-d*px*k/2,w*px*k,d*px*k); });
```

### Mode impression

`?print=1` : chaque slide figée dans son état final, chaque scène 3D rendue une fois puis gardée en image fixe. `scripts/rendu.py` ajoute ce paramètre automatiquement.
