# Style "Une de journal"

## 1. L'idée et quand l'utiliser

**En une phrase** : chaque slide est une page de quotidien (manchette, colonnes, filets, photo légendée) et le message principal s'écrit en gros titre, comme une information que tout le monde doit lire.

Univers de référence : la presse quotidienne grand format, les éditions spéciales, les kiosques. Ses objets servent de layouts : la une, l'article à colonnes, l'encadré "L'essentiel", la page Bourse, la météo, le programme télé, les petites annonces, le courrier des lecteurs, l'erratum.

**Quand l'utiliser**
- Une annonce, un lancement, une transformation, une réorganisation : tout ce qui se raconte comme une "nouvelle".
- Une institution, une collectivité, une association qui présente son année.
- Un public large (conférence, salle, collaborateurs) : le code du journal est compris par tout le monde.

**Quand l'éviter**
- Une marque de luxe ou de mode : le papier journal paraîtra bon marché.
- Un deck sans vraie nouvelle à annoncer : le gros titre sonnera creux.

## 2. Palette

| Rôle | Hex | Règle |
| --- | --- | --- |
| Papier journal | `#EDE6D6` | Fond de toutes les pages |
| Papier frais | `#F6F2E8` | Encadrés, cahier "suppléments" |
| Encre | `#161513` | Titres, texte, filets |
| Gris trame | `#6E6960` | Légendes, chapô secondaire, dates |
| Rouge manchette | `#C8102E` | Bandeau "Édition spéciale", flash, une seule zone par page |
| Bleu Bourse, optionnel | `#1F4E79` | Uniquement pour les courbes et tableaux de la page chiffres |

- **Règle : le rouge occupe une seule zone par page** (un bandeau, un mot, un filet épais). Le reste est en noir sur papier.
- La couleur de la marque peut remplacer le rouge.

```css
:root{
  --paper:#EDE6D6; --paper2:#F6F2E8; --ink:#161513; --grey:#6E6960; --red:#C8102E; --blue:#1F4E79;
  --f-mast:"UnifrakturMaguntia",serif; --f-head:"Libre Franklin",sans-serif;
  --f-text:"Source Serif 4",serif; --f-kick:"Libre Franklin",sans-serif;
}
.slide{background:var(--paper) url(assets/journal.jpg) center/cover;color:var(--ink);font-family:var(--f-text)}
```

## 3. Polices

| Rôle | Google Fonts | Usage |
| --- | --- | --- |
| Titre du journal | UnifrakturMaguntia | Le nom du journal en tête de la une, rien d'autre |
| Manchettes | Libre Franklin (800, 900) | Gros titres (90 à 200 px), interligne .92, interlettrage -.02em |
| Texte | Source Serif 4 (400, 600, italique) | Colonnes justifiées 24 à 28 px, chapô en italique 34 px, lettrine |
| Surtitres et légendes | Libre Franklin (600, petites capitales) | Rubriques, légendes, dates, signatures (18 à 22 px) |

Alternatives : Old Standard TT pour un journal plus ancien, Newsreader pour un texte plus moderne.

## 4. Éléments signature

- **La manchette** (en-tête du journal) : nom du journal en gothique, filet double dessous, ligne d'infos en petites capitales : "N° 2 418 · Mardi 17 novembre 2026 · 2,40 €". Le nom du journal est le nom du sujet ou de la marque ("Le Courrier de Kōri").
- **Filets doubles et simples** : épais-fin sous la manchette, fins entre les colonnes.
- **Rubrique en surtitre** au-dessus de chaque titre (ÉCONOMIE, LANCEMENT, ENQUÊTE), qui joue le rôle de sous-titre de section.
- **Lettrine** sur 3 lignes au début de l'article principal.
- **Renvoi** en bas de colonne : "Lire la suite page 4", qui annonce la slide suivante.
- **Folio** en bas : "4 | LE COURRIER DE KŌRI | MARDI 17 NOVEMBRE 2026".
- **Bandeau rouge** "ÉDITION SPÉCIALE" ou "EXCLUSIF", une seule fois par page.

## 5. Traitement des images

- Préréglage `presse` : noir et blanc franc, noirs jamais purs (encre sur papier), blancs teintés papier, grain visible. Toutes les photos du deck dans ce traitement.
- Option couleur "supplément du week-end" : préréglage `doc`, pour une seule photo forte (la une).
- Photos rectangulaires, alignées sur les colonnes, jamais inclinées. Légende en Libre Franklin sous la photo, crédit en petites capitales à droite ("PHOTO ANNA ROSSI / UNSPLASH").
- `texture journal` en fond de toutes les slides.

```bash
python scripts/images.py texture journal assets/journal.jpg
python scripts/images.py traiter raw/foule.jpg assets/foule.jpg --taille 1180x700 --preset presse --cadre 0.5,0.4
```

## 6. Mise en page et animations

- Grille de 6 colonnes (marges 80 px, gouttières 32 px, filets fins entre les colonnes).
- Une hiérarchie forte : un titre énorme, un chapô, puis des colonnes. Le titre occupe toute la largeur ou 4 colonnes.
- Le texte courant reste lisible : 3 colonnes de 8 à 12 lignes maximum par slide. Le reste va dans les notes.
- Les chiffres sont mis en scène comme dans un journal : encadré "Les chiffres", page Bourse, bulletin météo.
- Animations : `fade` pour la page, `wipe` pour les filets, `rise` pour le gros titre. Ton sobre, pas de rebond, sauf le bandeau rouge qui peut arriver en `slam`.

## 7. Bibliothèque de layouts

| Contenu | Layout | Astuce |
| --- | --- | --- |
| Cover | La une : manchette, gros titre sur 2 lignes, grande photo, chapô, deux brèves | Le gros titre est le message du deck |
| Sommaire | "Dans ce numéro" : liste des rubriques avec numéros de page | Une vignette photo par rubrique au plus |
| Problème | Article d'enquête : titre, chapô, 3 colonnes, intertitre | Une citation en exergue entre deux colonnes |
| Chiffres clés | Encadré "Les chiffres" : 3 ou 4 chiffres géants avec une ligne de contexte | Filets entre les chiffres, source en petit |
| Évolution | Page Bourse : courbe fine, tableau des cours, flèches ▲▼ | Le bleu Bourse ici seulement |
| Objectifs, KPIs | Bulletin météo : carte ou liste avec "prévisions" par indicateur | Soleil ou nuage traduits en mots, pas en icônes |
| Avant / après | Erratum : "Contrairement à ce que nous écrivions..." | L'ancienne version barrée, la nouvelle en gras |
| Témoignages | Courrier des lecteurs : 3 lettres courtes signées | Prénom, ville, une phrase par lettre |
| Interview, persona | Entretien question-réponse avec portrait détouré en noir et blanc | Questions en gras, réponses en romain |
| Offre, recrutement | Petites annonces : grille serrée de petites annonces | Une annonce encadrée en rouge |
| Planning | Programme télé : créneaux horaires et "émissions" | Le prime time = le moment clé |
| Fin d'une époque | Avis de décès humoristique : "Le tableur partagé nous a quittés" | L'humour vise l'habitude, jamais les gens |
| Positionnement | Tribune ou éditorial : texte long sur 2 colonnes, signature | Titre en italique serif |
| Statement | Gros titre seul sur toute la page | "Édition spéciale" en bandeau |
| Closing | Dernière page : "À suivre", date du prochain rendez-vous | Manchette réduite en bas |

## 8. Ton des textes

- Le titre est une information : sujet, verbe, complément, au présent. Viser 30 à 45 caractères pour tenir sur 2 lignes en 110 px, et ajouter `text-wrap:balance`. "Kōri met le cold brew en canette", pas "Notre nouveau produit".
- Chapô de deux phrases qui répondent à qui, quoi, quand, pourquoi.
- Surtitres en un ou deux mots.
- Citations entre guillemets français « », toujours attribuées.
- On peut s'amuser avec les codes de la presse (rubriques, avis, erratum), avec une preuve à chaque affirmation.

## 9. Interdits spécifiques

- Plus d'une zone rouge par page.
- Photos en couleur saturée mélangées au noir et blanc.
- Colonnes de plus de 12 lignes, texte en dessous de 22 px.
- Titres sans verbe, gothique ailleurs que dans le nom du journal.
- Faux logos ou faux noms de vrais journaux : le journal porte toujours le nom du sujet.

## 10. Check avant de livrer

- [ ] Chaque slide a une manchette ou un folio avec le nom du journal (le sujet), la date et le numéro de page.
- [ ] Chaque titre est une information avec un verbe.
- [ ] Un seul élément rouge par page.
- [ ] Toutes les photos dans le même traitement, légendées et créditées.
- [ ] Colonnes lisibles projetées : 22 px minimum, 12 lignes maximum.
- [ ] Aucun nom ni logo de journal réel.
