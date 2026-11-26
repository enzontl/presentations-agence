---
name: presentations-agence
description: "Crée, refait ou améliore une présentation de niveau agence, sans look généré par IA : deck, slides, pitch deck, keynote, soutenance, oral, business case, talk, deck investisseurs ou comex, présentation client, restitution d'étude, rapport ou PDF transformé en slides, slides à partir des photos ou graphiques de l'utilisateur. À utiliser même pour une demande courte qui ne parle pas de design (« fais-moi une présentation », « j'ai besoin de slides pour… », « make a pitch deck »), dès qu'un nombre de slides ou une date d'oral est donné, et quand un deck fait générique ou trop IA. Propose 9 styles tirés d'univers réels (objet réel, studio sombre, rapport suisse, une de journal, sérigraphie, magazine de mode, data-journalisme, brutalisme web, espace de travail) avec fond avant forme, vraies photos traitées, rendu PNG vérifié, script dans les notes, export HTML. Pas pour : seulement un script oral, corriger des notes, convertir un PPTX en PDF, résumer un document, un graphique isolé, un design system d'app."
---

# Présentations de niveau agence

Ce skill fabrique des decks qui ont l'air conçus par une agence. Le principe tient en une phrase : chaque deck emprunte les codes d'un univers visuel qui existe vraiment (un ticket de caisse, une une de journal, une affiche sérigraphiée, un rapport annuel suisse). Le format raconte le concept avant même que le texte soit lu.

C'est l'inverse d'un template. Un template part d'une grille vide et la remplit. Ici, on part d'un objet réel et on y range le contenu. C'est ce qui supprime le look "généré par IA" : une IA moyenne produit des cartes, des icônes dans des ronds et des dégradés, parce que c'est la moyenne de ce qu'elle a vu. Un objet réel a des contraintes, des imperfections et une histoire, et ça se voit.

Ce fichier contient le procédé commun à tous les styles. Chaque style a son fichier dans `references/`. **Lire en entier le fichier du style choisi avant de dessiner la première slide.**

## Commandes

Sans argument : un deck neuf, avec le procédé complet ci-dessous. Avec une commande, sur un deck qui existe (détail dans `references/commandes.md`) :

| Commande | Ce qu'elle fait |
| --- | --- |
| `audit <deck>` | Critique notée d'un deck HTML, PDF ou PPTX, trois priorités, sans rien modifier |
| `polish <deck>` | Finition : espaces, débordements, alignements, contrastes, notes, sans toucher aux layouts |
| `plus-audacieux <deck> [slides]` | Monte l'échelle, le contraste et l'élément signature |
| `plus-sobre <deck> [slides]` | Retire le décoratif, revient au fond de lecture, garde l'identité |
| `refaire-chiffres <deck>` | Re-tire et reconstruit les slides de chiffres selon les règles |
| `varier <deck>` | Casse les slides voisines trop semblables signalées par le rendu |
| `changer-style <deck> <style>` | Même contenu dans un autre univers, dans un nouveau dossier |
| `notes <deck>` | Écrit le script de l'orateur dans les notes |
| `exporter <deck> [html, pdf, pptx]` | Livre le deck dans le format demandé |

Une demande en langage naturel qui correspond à une commande (« critique mon deck », « rends-le plus punchy », « mes slides de chiffres sont plates ») suit la même procédure.

## Les 9 styles

| Style | Fichier | Univers réel | Registre | Fond dominant |
| --- | --- | --- | --- | --- |
| Éditorial objet réel | `references/editorial-objet-reel.md` | Magazine + objets de l'univers du sujet (ticket, menu, billet) | Audacieux, drôle | Alterné sombre et crème |
| Studio sombre | `references/studio-sombre.md` | Photo de produit en studio, objet 3D | Premium, sérieux | Bleu nuit |
| Rapport suisse | `references/rapport-suisse.md` | Rapports annuels suisses, style typographique international | Rigoureux, sobre | Blanc papier |
| Une de journal | `references/une-de-journal.md` | Presse quotidienne, éditions spéciales | Narratif, institutionnel | Papier journal |
| Affiche sérigraphie | `references/affiche-serigraphie.md` | Affiches de concert, risographie, caractères en bois | Festif, engagé | Papier crème et encres |
| Magazine de mode | `references/magazine-de-mode.md` | Couvertures et éditoriaux de magazines, lookbooks | Premium, image | Blanc et photo pleine page |
| Data-journalisme | `references/data-journalisme.md` | Enquêtes graphiques de la presse | Démonstratif | Papier clair |
| Brutalisme web | `references/brutalisme-web.md` | Premiers sites web, docs techniques, terminaux | Brut, tech, ironique | Blanc, noir, bleu lien |
| Espace de travail | `references/espace-de-travail.md` | Outils de travail en équipe (type Notion) : bases de données, kanban, surligneurs | Méthodique, doux, preuves de pilotage | Blanc et pastels |

## Choisir le style

### Selon le sujet

| Signal dans le sujet | Style conseillé | Pourquoi |
| --- | --- | --- |
| Univers physique riche : commerce, restauration, sport, voyage, artisanat | Éditorial objet réel | Les objets de cet univers deviennent les layouts |
| Un objet emblématique (bouteille, chaussure, puce, livre) et des données | Studio sombre | L'objet photographié en studio donne le ton premium |
| Résultats, bilan, rapport, gouvernance, finance, RSE | Rapport suisse | La grille et la retenue inspirent confiance |
| Annonce, transformation, actualité, institution qui raconte une étape | Une de journal | Le gros titre impose le message, les colonnes portent le détail |
| Événement, festival, culture, campagne associative, vie de campus | Affiche sérigraphie | Énergie, couleurs d'encre, effet "collé en ville" |
| Mode, beauté, design, art de vivre, marque à forte image | Magazine de mode | La photo domine, le texte se fait rare et élégant |
| Étude, enquête, mémoire, analyse de marché, beaucoup de chiffres | Data-journalisme | Chaque slide démontre avec un graphique annoté |
| Produit tech, outil pour développeurs, startup, public geek | Brutalisme web | Les codes bruts du web parlent à ce public, avec humour |
| Gestion de projet, plan de lancement, backlog, budget, risques, soutenance en équipe | Espace de travail | Les objets de pilotage (kanban, Gantt, matrice) deviennent les preuves |

### Selon le public

| Public | Plutôt | À éviter |
| --- | --- | --- |
| Jury académique, soutenance | Data-journalisme, Rapport suisse, Studio sombre | Brutalisme web face à un jury classique |
| Direction, investisseurs, conseil | Rapport suisse, Studio sombre, Data-journalisme | Affiche sérigraphie |
| Client créatif, agence, marque | Objet réel, Magazine de mode, Sérigraphie | Rapport suisse, trop froid |
| Grand public, conférence, salle large | Une de journal, Objet réel, Sérigraphie | Data-journalisme trop dense |
| Développeurs, équipes produit | Brutalisme web, Data-journalisme, Espace de travail | Magazine de mode |
| Jury de gestion de projet, comité de pilotage | Espace de travail, Rapport suisse | Affiche sérigraphie |

### Selon la marque

- **Charte forte** : garder ses couleurs comme couleurs pop du style, et ses polices si elles existent sur Google Fonts. Le style apporte la mise en page, pas une nouvelle identité.
- **Marque héritage** (or, bordeaux, marine, maison ancienne) : Studio sombre, Magazine de mode ou Rapport suisse.
- **Marque jeune au ton décalé** : Objet réel, Sérigraphie ou Brutalisme web.
- **Pas de marque** (projet, étude, mémoire) : le style vient du sujet et du public.

Proposer toujours à l'utilisateur **deux styles adaptés**, avec une phrase de justification chacun, plus **une option de contraste** plus audacieuse. Un seul style par deck : mélanger deux univers casse l'illusion de l'objet réel.

## Le procédé, dans l'ordre

### 1. Le fond d'abord

Aucune slide avant d'avoir trois choses : le message en une phrase, la storyline, les sources de chaque chiffre. Un beau deck sur un fond flou reste un deck faible, et retoucher la forme après coup coûte trois fois plus cher. **Lire `references/recit.md`** : affirmation et preuve, les structures (SCQA, pyramide, problème-solution-preuve…), les plans types prêts pour `tirage.py`, le minutage, le script des notes.

1. Lire les consignes en entier. Repérer les parties imposées, la durée, le public, les critères d'évaluation.
2. Ouvrir une page de travail qui suit ces parties (doc, Notion ou fichier `fond.md` dans le dossier du deck).
3. Faire la recherche et sourcer chaque chiffre (source, date, lien). Ne jamais inventer un chiffre : s'il manque, le demander à l'utilisateur ou l'indiquer comme hypothèse.
4. Choisir une structure et écrire la storyline sous forme de liste de titres-affirmations. Test : lus d'affilée, les titres doivent raconter toute l'histoire.
5. En déduire le plan : un type de contenu par slide (`references/recit.md` donne des plans types par genre de deck).

### 2. Les questions de style

Une seule salve de questions, toujours sous forme de choix (outil de question si disponible, sinon liste numérotée). Ne pas reposer une question à laquelle la demande répond déjà.

1. **Le style** : deux styles recommandés et une option audacieuse, chacun avec son univers en une ligne.
2. **Le fond dominant** : sombre, clair, ou alterné.
3. **La langue** : une seule, ou une principale avec des punchlines dans une autre.
4. **Les titres** : punchline + sous-titre clair (recommandé), phrase qui affirme la conclusion, ou mot seul.
5. **L'élément signature** : trois éléments signature du style choisi, l'utilisateur en garde un ou deux.

### 3. Poser le système du style

Lire le fichier du style en entier. Puis écrire et faire valider, en un bloc court :

- l'univers du sujet en 2 ou 3 mots et, pour les styles à objets, 6 à 10 objets-layouts associés aux types de contenu ;
- la palette en hex, avec le rôle de chaque couleur ;
- les polices et leur rôle ;
- le ton en pourcentage (ex. 70 % audacieux, 30 % premium) ;
- 5 interdits propres à ce deck.

### 4. Les images

Chercher, télécharger, traiter, placer. Voir la section "Pipeline images".

### 5. Tirer les layouts, puis monter le template

**Ne pas choisir les layouts à la main.** Un modèle qui choisit revient toujours au même layout par défaut, et deux slides voisines finissent par se ressembler (c'est le premier retour des tests utilisateurs). Le hasard choisit, dans ce qui convient :

```bash
python scripts/tirage.py --style une-de-journal --plan cover,sommaire,contexte,chiffre-cle,evolution,persona,closing --out mon-deck/tirage.json
python scripts/tirage.py --style une-de-journal --plan ... --out mon-deck/tirage.json --redraw 4   # re-tirer une slide
```

Le plan liste un type de contenu par slide (`--types` pour la liste). Le tirage indique aussi un fond d'impact une slide sur trois (« Fond : … ») : le suivre, c'est ce qui évite les slides voisines semblables dans les styles uniformes (suisse, data, journal). Le script tire un layout par slide parmi les gabarits validés et les layouts de la fiche, sans deux formes identiques côte à côte, sans répéter un layout, en évitant ceux des projets récents. Garder le tirage sauf raison écrite (contenu qui ne rentre pas) ; dans ce cas, `--redraw` plutôt qu'un choix à la main.

Puis monter le dossier du deck :

```bash
python scripts/nouveau_deck.py mon-deck --tirage mon-deck/tirage.json
```

Il copie les CSS, télécharge les polices, génère les textures et assemble `deck.html`. Les slides tirées depuis `gabarits/` arrivent déjà construites avec du texte d'exemple (Kōri, Valmont) : **tout le texte et tous les chiffres sont à remplacer**, la composition est à garder. Les layouts « à construire d'après la fiche » arrivent en section `.a-construire` : les construire en reprenant les classes du `style.css`.

Premier livrable visuel : ce template de 6 à 10 slides.

- **Slide 0 « règles »** : pastilles de la palette avec hex et rôle, polices avec leur rôle, les 5 interdits, l'élément signature. Elle sert de contrat visuel pour toute la suite.
- **Les slides tirées**, remplies avec le vrai contenu et les vraies images. Jamais de lorem ipsum ni de rectangle gris : un placeholder empêche de juger le rendu, et c'est exactement par là que le look template revient.

Faire valider le template avant de produire tout le deck.

### 6. La boucle de rendu et la critique

À chaque version : rendre, critiquer sur les captures avec `references/critique.md`, corriger les trois pires défauts, recommencer, trois rounds au plus. Voir la section « Boucle de rendu ».

### 7. Les retours utilisateur

Les retours typiques, à anticiper dès la première version :

- **"Ça fait générique, trop IA"** : remplacer les grilles et les cartes par des layouts du style (typo géante, plein cadre, objets de l'univers).
- **"Cette image revient trop, elle est mal détourée"** : une image par slide, et une photo entière plutôt qu'un détourage douteux.
- **"On ne voit pas assez la marque"** : nom ou logo sur la cover et dans l'élément signature de chaque slide.
- **"C'est trop chargé"** : garder trois niveaux de texte, déplacer le reste dans les notes.
- **"On ne lit pas de loin"** : aucun texte sous 22 px sur la slide, sauf sources et légendes.
- **"Ne touche pas à cette slide"** : la noter comme validée dans `fond.md` et ne plus jamais la retoucher, même pour harmoniser.

### 8. Le deck final

**Porte de sortie, obligatoire** : `python scripts/lint.py mon-deck/deck.html --livraison` doit finir sans bloquant. Il vérifie en plus du lint habituel que le rendu est à jour, que la critique est écrite dans `fond.md` (« Critique, round N », « Note : x / 10 »), que la dernière note atteint 8 ou que trois rounds ont été faits, et qu'il ne reste qu'une paire de slides voisines semblables au plus, justifiée (« slides 05 et 06 : gardé car … »), avec deux rounds de critique dans ce cas. Au-delà d'une paire, aucune justification n'est acceptée : re-tirer ou changer fond, côté ou forme. Les tests ont montré qu'un agent pressé saute la critique : cette porte l'en empêche. Ne jamais livrer un deck qui ne la passe pas.


- Retirer la slide règles et les slides en trop.
- Ordonner selon le récit et découper en sections (le sous-titre de section de chaque slide doit suivre ce découpage).
- Écrire le script de chaque orateur dans les notes : phrases parlées, 30 à 60 secondes par slide, le prénom de l'orateur en tête s'il y en a plusieurs.
- Mettre les crédits photo à la fin des notes de la slide concernée, et un récapitulatif dans les notes de la dernière slide.

### 9. Les livrables annexes, si utile

Script complet de l'oral, fiche de sources et réponses aux 5 questions probables (`references/recit.md`), export HTML autonome, PDF, PowerPoint (`scripts/exporter.py`).

## Structure technique du deck

Le deck est un fichier HTML. Une slide = une `<section class="slide">` de 1920x1080, éléments en position absolue. Cette structure est la même pour tous les styles, ce qui permet aux scripts de rendu et d'export de marcher partout.

```
mon-deck/
├── fond.md        brief, storyline, sources, slides validées, table images
├── deck.html      toutes les slides
├── base.css       copie de assets/base.css (structure, animations)
├── style.css      le style choisi (copie de gabarits/<style>/style.css)
├── tirage.json    les layouts tirés au sort (scripts/tirage.py)
├── fonts/         polices locales + fonts.css (scripts/polices.py)
├── raw/           photos téléchargées, non traitées
├── assets/        photos traitées, textures
└── renders/       PNG de chaque slide + planche contact
```

```html
<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="base.css">
<link rel="stylesheet" href="style.css">
</head>
<body class="deck">
  <section class="slide" data-section="Le marché">
    <img class="bg" src="assets/marche.jpg" alt="">
    <h2 class="title" data-anim="rise" style="--i:1">Le titre qui conclut</h2>
    <p class="sub" data-anim="rise" style="--i:2">Le sous-titre qui dit le fond.</p>
    <aside class="notes">Script de l'orateur. Crédit photo : Prénom Nom, Unsplash.</aside>
  </section>
</body></html>
```

- `assets/base.css` fournit la structure, le compteur de pages (`.pageno`), l'image plein cadre (`.bg`) et les animations `rise`, `drop`, `slam`, `fade` déclenchées par `data-anim` et décalées de 120 ms par `--i`. Les animations ne jouent qu'en mode présentation : en rendu statique, chaque élément est dans son état final.
- Chaque style a ses propres classes dans `style.css`. Le fichier du style les liste avec ses jetons CSS.
- `gabarits/<style>/` contient les slides validées par un utilisateur exigeant, prêtes à copier : `style.css`, un fichier HTML par layout (en-tête : type, forme, fond, image attendue), `polices.txt`, et `commun.html` quand le style a des scripts (graphiques, 3D) ou un sprite SVG. `gabarits/index.json` les recense. Partir d'un gabarit plutôt que d'une page blanche : c'est ce qui garde le niveau d'un deck à l'autre.
- Les polices : `python scripts/polices.py "Anton" "Inter:wght@400;600" --out fonts/` télécharge les fichiers Google Fonts et écrit `fonts/fonts.css`. Des polices locales garantissent un rendu identique hors ligne et dans l'export.
- **Si l'environnement propose un type d'artifact Slides ou un outil de présentation**, y transposer la même structure : une section par slide, mêmes classes, images uploadées dans l'espace d'assets de l'artifact et référencées par l'URL renvoyée. Garder une table "fichier vers URL" dans `fond.md`, utile pour les exports.

## Pipeline images (commun à tous les styles)

### 1. Les sources

- **Unsplash** (gratuit, haute définition) pour les photos réelles : personnes, lieux, objets, textures.
- **Visuels générés** (ChatGPT, Midjourney, Higgsfield...) seulement pour ce qui n'existe pas encore : un produit, une affiche de campagne, un packaging. Claude écrit les prompts, l'utilisateur génère et renvoie les images.
- **Les photos de l'utilisateur** dès qu'il en a : ce sont les plus crédibles.
- Jamais de photo d'une personnalité réelle.

### 2. Les domaines à autoriser

Le téléchargement depuis le shell ou l'environnement de code passe par `images.unsplash.com`. Selon l'environnement, l'utilisateur doit ajouter `unsplash.com` et `images.unsplash.com` aux domaines autorisés (dans Claude.ai : Paramètres, Capacités). Sans ça, rien ne se télécharge. Tester avec un `curl -I` avant de chercher des photos.

### 3. Trouver l'URL exacte d'une photo

Les pages HTML d'unsplash.com ont une protection anti-bot. Ne pas la contourner (pas de faux navigateur, pas d'API privée, pas de scraping) : passer par la recherche web puis par une lecture de page autorisée.

1. Recherche web limitée au domaine `unsplash.com`, avec une requête précise : sujet + lumière + cadrage. Exemples : "market stall night close-up", "workshop hands top view dark", "portrait street natural light". Les requêtes en anglais donnent de meilleurs résultats.
2. Lecture de la page photo trouvée (WebFetch ou équivalent) avec la consigne : "Return only the exact full URL of the main photo on images.unsplash.com, and the photographer's name". Lire plusieurs pages dans le même appel quand c'est possible.
3. Télécharger en haute définition dans `raw/` :

```bash
curl -sSL "<url_sans_parametres>?fm=jpg&q=82&w=2200" -o raw/<nom>.jpg
```

4. Noter le nom du photographe dans la table images de `fond.md`, pour les crédits.

Chercher 2 ou 3 candidates par slide et choisir en regardant les fichiers téléchargés : une photo se juge à l'œil, pas à sa description.

### 4. Traiter chaque image

Même traitement pour toutes les photos d'un deck, pour qu'il semble shooté par une seule personne. `scripts/images.py` fait tout, avec un préréglage par style :

```bash
python scripts/images.py traiter raw/x.jpg assets/x.jpg --taille 1920x1080 --preset chaud --sombre bas
python scripts/images.py traiter raw/y.jpg assets/y.jpg --taille 960x1080 --preset presse --cadre 0.5,0.3
python scripts/images.py texture papier assets/papier.jpg --couleur EFE3C8
```

| Étape | Ce qu'elle fait | Pourquoi |
| --- | --- | --- |
| Recadrage au format exact | Plein cadre 1920x1080, demi-écran 960x1080, bande, portrait. `--cadre x,y` choisit le centre | Le navigateur ne recadre jamais aussi bien qu'un choix humain |
| Étalonnage | Saturation, chaleur, contraste, selon le préréglage du style | Unifie des photos de sources différentes |
| Assombrissement sous le texte | Dégradé depuis le bas, la gauche, la droite ou le haut (`--sombre`) | Le texte reste lisible sans bandeau noir |
| Grain | Bruit léger | Supprime l'aspect "image de banque" trop lisse |

Préréglages : `chaud` (objet réel), `studio`, `neutre` (suisse), `presse` (journal, noir et blanc), `trame` (sérigraphie, bichromie tramée, avec `--encres`), `mode`, `doc` (data-journalisme), `pixel` (brutalisme, tramage 1 bit). Le fichier du style précise les réglages.

Autres traitements :

- **Textures** : `texture papier`, `texture sombre`, `texture journal`, `texture kraft`, réutilisées en `.bg` sous les slides sans photo.
- **Compositions** : mur d'affiches, planche contact, pile de documents. Les construire avec PIL en collant les visuels de travers, avec ombre douce et léger pli.
- **Détourages** : seulement des PNG propres (fond transparent, sans liseré, vérifiés en zoomant à 200 %). En cas de doute, photo entière.

### 5. Placer

- `<img class="bg" src="assets/x.jpg" alt="">` en premier enfant de la section pour un plein cadre.
- **Règle absolue : une image = une slide.** La même photo sur deux slides donne immédiatement l'impression d'un manque de matière.
- Crédits dans les notes de la slide (`Photo : Prénom Nom, Unsplash`).

## Boucle de rendu (à chaque version)

Regarder le rendu réel est la seule façon de voir ce que l'utilisateur verra. Le code HTML ne montre ni un titre sur trois lignes, ni un tampon qui cache un chiffre.

```bash
python scripts/lint.py mon-deck/deck.html --corriger      # d'abord : les tics visibles dans le code
python scripts/rendu.py mon-deck/deck.html --out mon-deck/renders
```

`lint.py` lit le HTML sans navigateur et attrape les tics du registre `references/tics.md` : dégradé violet, emojis, titres étiquettes (« Contexte », « Conclusion »), texte d'exemple de gabarit oublié, image répétée, section à construire, lorem ipsum (bloquants), et en alerte trois chiffres égaux sans héros, chiffres sans source, superlatifs sans preuve, notes vides, listes trop longues, espaces non insécables (`--corriger` les répare). Corriger chaque bloquant ; garder une alerte seulement avec une raison en une phrase.

Le script rend chaque slide en PNG 1920x1080 (Chrome sans interface, animations coupées, polices locales), assemble `planche.png` et écrit `rapport.txt` avec les problèmes détectés : titre sur 3 lignes ou plus, élément qui sort de la slide, texte coupé dans sa boîte, image manquante, police non chargée, texte trop petit. Option `--slides 3,5` pour ne rendre que certaines slides.

Le script écrit aussi `titres.txt` (les titres seuls, pour tester le récit), `planche-floue.png` (les masses, comme en plissant les yeux) et, dans le rapport, la rubrique « Rythme » : les slides voisines qui se ressemblent trop. Une section `.a-construire` restante est signalée en tête.

Puis :

1. Lire `rapport.txt` et corriger tout ce qui est cassé.
2. Critiquer sur les captures avec `references/critique.md` : sept passes (titres seuls, plisser les yeux, une seconde, cacher le nom, les voisines, les chiffres, le style), une note sur 10 avec plafonds, la critique écrite.
3. Corriger les trois problèmes les plus graves, relancer le rendu, recommencer.
4. Trois rounds au plus. S'arrêter avant si la note atteint 8 sans plafond.

Un élément volontairement coupé par le bord (titre géant, objet flou, filigrane) porte la classe `bleed` : le rapport l'ignore. Pour une slide qui dessine en JavaScript (three.js, graphiques générés), allonger l'attente : `--attente 3000`.

Ce que le rapport ne voit pas, et qu'il faut chercher sur la planche : un titre de deux lignes qui chevauche le sous-titre placé trop haut, un mot seul sur la dernière ligne, deux encres ou deux couleurs qui se mélangent en une teinte boueuse, un élément qui touche une photo sans le vouloir.

**Avant de publier** une nouvelle version : comparer les fichiers en ligne avec la copie locale. Si l'utilisateur a modifié quelque chose de son côté, repartir de sa version et y reporter les corrections. Publier seulement les fichiers changés.

## Slides de chiffres (tous les styles)

C'est là que le look généré revient le plus vite. Retour utilisateur réel : « trois chiffres alignés avec des filets, ça fait Claude, c'est vide ».

- Jamais trois chiffres ou plus de même taille sans un chiffre plus grand : `lint.py` le bloque, et ce blocage ne se justifie pas. Une barre de répartition garde ses étiquettes en petit, sous un chiffre héros.
- Un chiffre héros qui domine (trois à cinq fois plus grand que les autres), les autres subordonnés.
- Le chiffre vit dans un objet ou une figure du style : ticket, infographie hachurée, carte à cercles, line-up de festival, sommaire de magazine, colonne de répartition sur la grille.
- Remplir le format : une slide de chiffres n'a pas de grand vide non composé.
- Varier la composition d'une slide de chiffres à l'autre (graphique plein cadre, figure + colonne, héros + petits multiples, titre dans le graphique).
- Varier aussi la forme : jamais deux slides voisines avec le même type de graphique (trois courbes d'affilée se ressemblent, même avec des mises en page différentes). Alterner courbe, waffle, colonnes groupées, dumbbell, carte, chiffre géant.
- Varier l'objet d'une slide de chiffres à l'autre dans un même style : en magazine, un « chiffre + photo » puis un questionnaire ou un sommaire ; en objet réel, un ticket puis une fiche, une étiquette prix ou une carte de lecteur posées à côté.

## Typographie française (tous les styles)

- Espace insécable avant `%`, `€`, `:`, `;`, `?`, `!`, `»` et après `«`, et dans les milliers (`412 000` avec une espace fine insécable). Sans elle, un `%` ou un `€` se retrouve seul en début de ligne.
- `text-wrap: balance` sur tous les titres : il évite le mot seul sur la dernière ligne.
- Guillemets français « », apostrophe typographique ’ dans les titres en grand corps.
- Chiffres en `tabular-nums` dès qu'ils sont alignés ou comparés.

## Interdits communs (anti-look généré)

Le registre complet et daté est dans `references/tics.md` (avec ce que `lint.py` détecte). La liste courte :

Valables pour tous les styles. Chaque fichier de style ajoute les siens.

- Rangées de cartes symétriques, icônes dans des ronds, pictogrammes génériques à la place d'une donnée.
- Dégradés violet et bleu, glassmorphism, ombres portées partout, coins arrondis par défaut.
- Emojis.
- Tout centré, tout de la même taille, puces à rallonge, paragraphes.
- Titres génériques : "Contexte", "Notre solution", "Introduction", "Conclusion".
- Plus de trois niveaux de texte sur une slide.
- La même image ou le même objet sur plusieurs slides.
- Des couleurs sans rôle : chaque couleur a une fonction écrite dans la slide règles.
- Des chiffres sans source.
- Du blanc pur #FFFFFF et du noir pur #000000 en grands aplats, sauf si le style l'exige (brutalisme web).

## Mise en scène (export autonome)

L'export (`scripts/export.py`) ajoute une vraie mise en scène, pilotée par de simples attributs dans le HTML. Elle vient du deck « Singulier. » (référence du style Espace de travail), mais sert dans tous les styles.

| Effet | Comment | Quand |
| --- | --- | --- |
| **Visuel persistant** | Donner le même `style="view-transition-name:plan"` à l'objet sur plusieurs slides de suite : l'export le fait glisser et se transformer d'une slide à l'autre (View Transitions), sans rejouer son entrée | Le même plan, la même matrice ou le même graphique qui change d'état : zone surlignée, avant puis après, autre angle |
| **Sous-étapes** | `data-etape="1"`, `"2"`… sur des éléments : ils apparaissent un à un avant de passer à la slide suivante, et restent visibles quand on revient en arrière | Les lignes d'un tableau, les cartes d'une file, les points d'une démonstration |
| **Mots un par un** | `data-anim="mots"` sur un titre | Titres de partie, phrase de fin |
| **Surligneur qui se trace** | `<mark class="surligneur" style="--surligneur:#FFE89E">mot</mark>` | Le groupe de mots qui porte la preuve dans un titre |
| **Sens du retour** | Automatique : en revenant en arrière, les entrées viennent d'en haut | Toujours |
| **Progression par partie** | `<body class="deck" data-progression>` : une barre découpée selon les `data-section` | Decks longs, soutenances minutées |

Au clavier, en plus des flèches : `O` vue d'ensemble par partie (cliquer pour sauter), `P` vue présentateur dans une autre fenêtre (minuteur, titre de la slide suivante, notes en grand, synchronisée avec l'écran projeté), `N` notes, `F` plein écran. Le rendu PNG (`rendu.py`) montre l'état final de chaque slide, sous-étapes comprises.

## Export HTML autonome

Pour partager hors de Claude, envoyer par mail ou intégrer dans un outil comme Notion :

```bash
python scripts/export.py mon-deck/deck.html --out mon-deck/deck-autonome.html
```

Le script assemble tout dans un seul fichier : feuilles de style incluses, images converties en WebP (1920 px max, qualité 80) et intégrées en base64, polices intégrées en base64, scripts externes intégrés. Il ajoute une navigation au clavier (flèches, espace, Page suivante, clic), `N` notes, `O` vue d'ensemble, `P` vue présentateur, `F` plein écran, la mise en scène ci-dessus, une mise à l'échelle à la taille de la fenêtre, et écrit les numéros de page en dur. Compter environ 0,5 Mo par slide. Le fichier s'ouvre hors ligne le jour de l'oral.

### PDF et PowerPoint

```bash
python scripts/exporter.py mon-deck/deck.html --pdf --pptx
```

- **PDF** : une page 1920x1080 par slide, fonds et 3D compris, texte sélectionnable. Pour l'envoi par mail et l'impression.
- **PPTX** : une slide 16:9 par slide, l'image en plein cadre et le script de l'orateur dans les notes PowerPoint. S'ouvre dans PowerPoint, Keynote et Google Slides (Importer). Le texte n'y est pas modifiable : pour corriger, corriger le HTML et réexporter. Le dire à l'utilisateur quand il demande un PowerPoint « modifiable ».

## Check commun avant de livrer

- [ ] Le deck se comprend en ne lisant que les titres.
- [ ] Chaque slide de contenu utilise un layout du style, jamais une grille générique.
- [ ] Les règles de couleur et de tampon du style sont respectées sur chaque slide.
- [ ] Marqueur de page et repère de section sur chaque slide.
- [ ] Aucune image répétée, détourages propres, crédits dans les notes.
- [ ] `lint.py --livraison` sans bloquant (critique écrite, rythme réglé), alertes justifiées.
- [ ] Aucun titre sur 3 lignes, aucun débordement : `rapport.txt` vide et planche vérifiée.
- [ ] Critique écrite, note de 8 ou plus sans plafond (`references/critique.md`).
- [ ] Aucun texte d'exemple de gabarit oublié (chercher « Kōri », « Valmont », « données fictives »).
- [ ] Chaque chiffre a sa source dans les notes ou en pied de slide.
- [ ] Espaces insécables en place (aucun `%`, `€` ou `?` seul en début de ligne).
- [ ] Script de l'orateur dans les notes de chaque slide.
- [ ] Les slides validées par l'utilisateur n'ont pas été retouchées.
- [ ] Le check propre au style (fin du fichier du style) est passé.

## Tester le skill

- `evals/` contient trois cas réels (pitch en autonomie, audit d'un deck généré, soutenance à partir d'un CSV), au format lu par `claude plugin eval`. Chaque cas a sa demande, sa description du résultat attendu et ses critères vérifiables. Lancer avec : `claude plugin eval . --allow-tools Write,Edit,Bash --scaffold` depuis le dossier du skill (exécutions réelles et facturées).
- Pour comparer deux decks à l'aveugle (avec et sans le skill, ou deux versions) : `python scripts/comparer.py preparer --a <renders A> --b <renders B>`, faire noter les images par un juge qui ne voit que `grille.md`, puis `python scripts/comparer.py resultat comparaison/`.
