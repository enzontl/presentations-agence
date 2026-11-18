# Style "Affiche sérigraphie"

## 1. L'idée et quand l'utiliser

**En une phrase** : chaque slide est une affiche imprimée à la main, avec deux ou trois encres qui se superposent, des caractères en bois, des trames de points et de légers défauts de repérage, comme si elle venait d'être collée en ville.

Univers de référence : les affiches de concerts et de festivals, l'impression en risographie, la sérigraphie d'atelier, la typographie au plomb et au bois. Ses objets servent de layouts : l'affiche, le line-up, le billet, le bracelet, la setlist, le flyer, le plan du site, le sticker, le tote bag.

**Quand l'utiliser**
- Événement, festival, concert, exposition, vie de campus, campagne associative ou militante.
- Une marque jeune, artisanale, engagée, ou une offre culturelle.
- Un public créatif ou grand public, quand on veut de l'énergie.

**Quand l'éviter**
- Un comité de direction, des investisseurs, un rapport financier.
- Un deck très chiffré : la trame et les superpositions gênent la lecture fine des données.

## 2. Palette

Les couleurs sont des **encres** : elles se multiplient entre elles quand elles se superposent, comme sur le papier.

| Rôle | Hex | Règle |
| --- | --- | --- |
| Papier crème | `#F2EBDD` | Fond par défaut |
| Papier kraft, optionnel | `#C9A97A` | Pour une série "atelier" |
| Rose fluo | `#FF48B0` | Encre 1 possible |
| Bleu riso | `#0078BF` | Encre 2 possible |
| Jaune | `#FFE800` | Encre possible, toujours avec une encre foncée |
| Vert sarcelle | `#00838A` | Encre possible |
| Orange | `#FF6C2F` | Encre possible |
| Noir encre | `#1B1A1A` | Texte des infos pratiques, jamais en aplat géant |

- **Règle : 2 encres par slide, plus le papier.** Une troisième seulement sur la cover.
- Choisir 3 ou 4 encres pour tout le deck et les faire tourner par paires. Si la marque a des couleurs, en faire des encres.
- Superposition en `mix-blend-mode:multiply` : rose sur bleu donne un violet profond, et c'est cette troisième couleur "gratuite" qui fait le charme.

```css
:root{
  --paper:#F2EBDD; --ink1:#FF48B0; --ink2:#0078BF; --ink3:#FFE800; --black:#1B1A1A;
  --f-poster:"Big Shoulders Display",sans-serif; --f-wood:"Alfa Slab One",serif;
  --f-text:"Work Sans",sans-serif; --f-info:"DM Mono",monospace;
}
.slide{background:var(--paper) url(assets/papier.jpg) center/cover;color:var(--black)}
.ink{mix-blend-mode:multiply}
.misreg{text-shadow:7px 5px 0 var(--ink2)}   /* défaut de repérage : un liseré de l'autre encre */
```

## 3. Polices

| Rôle | Google Fonts | Usage |
| --- | --- | --- |
| Affiche | Big Shoulders Display (800, 900) | Titres condensés géants (200 à 520 px), interligne .82, capitales |
| Caractère bois | Alfa Slab One | Mots d'accent, chiffres, prix, "COMPLET" |
| Texte | Work Sans (400, 600) | Les rares phrases (26 à 32 px) |
| Infos pratiques | DM Mono (400, 500) | Dates, lieux, horaires, tarifs, numéros de tirage |

Alternatives : Anton pour l'affiche, Rye pour un esprit western, Bungee pour un esprit signalétique.

## 4. Éléments signature

- **Surimpression** : deux encres qui se chevauchent en multiplication, et la troisième couleur qui naît du chevauchement.
- **Défaut de repérage** : un liseré de l'autre encre décalé de 4 à 8 px (`.misreg`, en `text-shadow`), sur le titre. Ne jamais dupliquer un même texte dans les deux encres en multiplication : les deux couches se recouvrent presque entièrement et donnent une teinte sombre et boueuse (rose + bleu = marine, orange + sarcelle = vert noir). La troisième couleur doit naître du chevauchement de deux éléments **différents** (un titre qui passe sur une image, un mot sur un aplat).
- **Trame de points** (halftone) sur les images et sur certains aplats.
- **Bande d'infos pratiques** en bas de chaque affiche, en mono : date, lieu, prix, comme sur une vraie affiche.
- **Marques de repérage** (petites cibles) dans 2 coins et **numéro de tirage** en marqueur de page : "Tirage 03/12".
- **Typo qui remplit tout le format**, mots empilés et coupés par le bord.

## 5. Traitement des images

- Préréglage `trame` : bichromie tramée, deux trames de points à angles différents, encres en multiplication, léger décalage. Les photos deviennent des images imprimées.
- Choisir des photos simples et contrastées : une silhouette, un objet, une main, une foule à contre-jour. Les détails fins disparaissent dans la trame.
- Les images peuvent être détourées en forme simple (rond, bande) ou laissées en rectangle avec un bord légèrement irrégulier.
- `texture papier` (crème) ou `texture kraft` sous toutes les slides.

```bash
python scripts/images.py texture papier assets/papier.jpg --couleur F2EBDD
python scripts/images.py traiter raw/foule.jpg assets/foule.jpg --taille 1200x1080 --preset trame --encres FF48B0,0078BF
```

## 6. Mise en page et animations

- Composition d'affiche : un format vertical imaginaire ou la slide entière, une hiérarchie très forte, peu d'éléments.
- La typo est l'image : sur la moitié des slides, aucun visuel autre que les lettres.
- Asymétrie, mots tournés à 90°, empilements. Mais les infos pratiques restent alignées et lisibles.
- Les chiffres sont imprimés en caractères bois géants.
- Animations : `drop` pour les encres qui "tombent" l'une après l'autre (encre 1, puis encre 2 avec 200 ms de retard), `slam` pour le tampon ou le "COMPLET", `wipe` pour les bandes. Effet d'impression couche par couche.

## 7. Bibliothèque de layouts

| Contenu | Layout | Astuce |
| --- | --- | --- |
| Cover | Affiche titre : nom géant sur 2 encres en surimpression, image tramée | Bande d'infos pratiques en bas |
| Sommaire, programme | Line-up : les parties en tailles décroissantes, comme les têtes d'affiche | La partie la plus importante en haut, la plus grande |
| Structure | Plan du site du festival : zones, scènes, chemins | Chaque zone = une partie du deck |
| Chiffre clé | Chiffre en caractère bois sur toute la hauteur, 2 encres décalées | Contexte en mono dans la bande d'infos |
| Plusieurs chiffres | Affiche "résultats" : 3 chiffres empilés, encres alternées | Pas de boîtes, juste la typo |
| Offre, prix | Billet d'entrée : souche détachable, tarifs, numéro | Pointillés de découpe |
| Fidélité, accès | Bracelet tissé : texte répété en bande | Bande pleine largeur, légèrement inclinée |
| Étapes, agenda | Setlist scotchée : liste manuscrite ou mono, ordre de passage | Un morceau barré = une étape terminée |
| Avant / après | Flyer recto / verso | L'ancien en une encre délavée, le nouveau en deux encres |
| Campagne, visuels | Mur d'affiches collées, déchirées, superposées | Les vraies créations, en trame |
| Produit, merch | Tote bag ou t-shirt imprimé avec le visuel | Photo réelle de l'objet ou maquette propre |
| Statement | Sticker rond ou slogan pleine page | Une phrase, une encre |
| Équipe, partenaires | Affiche crédits : noms en colonnes, comme le bas d'une affiche de film | Rôles en mono |
| Closing | Affiche "COMPLET" ou "À BIENTÔT" avec date du prochain rendez-vous | Tampon en caractère bois |

## 8. Ton des textes

- Slogans courts, à crier : 2 à 5 mots en titre.
- Impératif et présent : "Venez tôt", "Ça se passe ici".
- Les infos pratiques sont précises et complètes : date, heure, lieu, prix.
- L'humour et l'engagement sont bienvenus, avec une preuve derrière chaque promesse.

## 9. Interdits spécifiques

- Plus de 2 encres par slide (3 sur la cover).
- Des couleurs qui ne se multiplient pas (aplats opaques qui se cachent).
- Dégradés numériques lisses, photos en couleurs naturelles non tramées.
- Des infos pratiques illisibles ou décoratives.
- Des polices manuscrites "fun" ou des effets grunge plaqués partout.

## 10. Check avant de livrer

- [ ] 2 encres par slide, 3 au plus sur la cover, et elles se superposent en multiplication.
- [ ] Toutes les images tramées avec les mêmes encres que leur slide.
- [ ] Bande d'infos pratiques et numéro de tirage sur chaque slide.
- [ ] Un défaut de repérage visible mais jamais au point de gêner la lecture.
- [ ] Aucun texte dupliqué en deux encres : chaque titre garde sa couleur d'encre pure.
- [ ] Les titres se lisent à 5 mètres sur la planche contact réduite.
