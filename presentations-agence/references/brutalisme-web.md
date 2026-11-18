# Style "Brutalisme web"

## 1. L'idée et quand l'utiliser

**En une phrase** : une interface brute assumée, avec des polices système, des bordures noires épaisses, le bleu des liens, une grille visible et aucun arrondi, comme une page web de 1996 ou une documentation technique tapée à la main.

Univers de référence : les premiers sites web, les pages "Index of /", la documentation technique, les terminaux, les fichiers README, les diffs de code, les zines numériques. Ses objets servent de layouts : la page d'accueil, le listing de dossier, la page 404, le terminal, le diff, le changelog, le formulaire HTML, le tableau brut, la boîte d'alerte, le fil de commits.

**Quand l'utiliser**
- Produit tech, outil pour développeurs, API, startup, open source, hackathon.
- Un public développeur, produit ou geek, qui reconnaît les codes et apprécie l'ironie.
- Une marque qui veut paraître honnête, directe, sans marketing.

**Quand l'éviter**
- Un jury ou un comité classique qui prendra la brutalité pour du travail bâclé.
- Le luxe, la mode, la santé, tout ce qui demande de la délicatesse.

## 2. Palette

| Rôle | Hex | Règle |
| --- | --- | --- |
| Blanc page | `#FFFFFF` | Fond par défaut. Ici le blanc pur est voulu |
| Noir | `#000000` | Texte, bordures de 3 à 4 px, ombres dures |
| Bleu lien | `#0000EE` | Liens soulignés, éléments cliquables, mot clé |
| Violet visité | `#551A8B` | Les parties déjà vues (sommaire) |
| Jaune surligneur | `#FFFF00` | Fond derrière un mot ou un chiffre, une fois par slide |
| Gris système | `#C0C0C0` | Boutons, barres de fenêtre |
| Rouge erreur | `#FF0000` | Erreurs, lignes supprimées d'un diff |
| Vert terminal | `#00C853` sur `#0A0A0A` | Slides terminal uniquement, lignes ajoutées d'un diff |

- **Règle : 2 couleurs pop maximum par slide** en plus du noir et blanc (bleu lien + une autre).
- Les slides terminal inversent le fond (noir) et prennent le vert comme seule couleur.

```css
:root{
  --white:#FFFFFF; --black:#000000; --link:#0000EE; --visited:#551A8B; --mark:#FFFF00;
  --sys:#C0C0C0; --err:#FF0000; --term:#00C853; --term-bg:#0A0A0A;
  --f-head:"Arimo",sans-serif; --f-text:"Tinos",serif; --f-mono:"JetBrains Mono",monospace;
}
.slide{background:var(--white);color:var(--black);font-family:var(--f-text)}
.box{border:4px solid var(--black);box-shadow:10px 10px 0 var(--black)}
a,.link{color:var(--link);text-decoration:underline;text-decoration-thickness:3px;text-underline-offset:6px}
```

## 3. Polices

Les polices "par défaut" des navigateurs, en version Google Fonts : c'est ce qui donne l'effet "page non stylée".

| Rôle | Google Fonts | Usage |
| --- | --- | --- |
| Titres | Arimo (700) | Titres géants (120 à 360 px), interligne .9, interlettrage -.03em (clone d'Arial) |
| Texte | Tinos (400, italique) | Corps (28 à 34 px), comme le Times par défaut d'un navigateur |
| Code et labels | JetBrains Mono (400, 700) | Terminal, URLs, balises, chiffres, métadonnées |

Alternatives : Space Mono ou IBM Plex Mono pour le code, Archivo Black pour des titres plus lourds.

## 4. Éléments signature

- **Barre d'adresse** en haut de chaque slide, qui joue le rôle de sous-titre de section : `https://kori.fr/deck/03-marche`.
- **Balises visibles** en gris mono à côté des titres : `<h1>`, `</section>`.
- **Bordures noires de 4 px et ombres dures décalées** (10 px, sans flou) sur les blocs mis en avant.
- **Liens bleus soulignés** pour les mots clés et le "Lire la suite".
- **Compteur de visiteurs** en marqueur de page : `VISITEUR N° 000003` (numéro de page sur 6 chiffres).
- **Curseur clignotant** `█` à la fin du titre principal ou de la ligne de terminal.
- **Horodatage** et métadonnées en mono : `modifié le 2026-11-17 09:42`, `12 Ko`.

## 5. Traitement des images

- Préréglage `pixel` : tramage 1 bit (Floyd-Steinberg), une encre sur blanc. Noir pour la plupart, bleu lien pour une image clé. L'effet "écran ancien" rend les photos honnêtes et cohérentes.
- Captures d'écran brutes du produit, sans maquette de téléphone ni d'ordinateur, posées dans un cadre noir de 4 px avec une barre de fenêtre grise.
- Images rectangulaires, jamais arrondies, ombre dure décalée possible.
- Pas de texture : le fond blanc pur fait partie du style.

```bash
python scripts/images.py traiter raw/equipe.jpg assets/equipe.jpg --taille 900x1080 --preset pixel
python scripts/images.py traiter raw/produit.jpg assets/produit.jpg --taille 1200x700 --preset pixel --encres 0000EE
```

## 6. Mise en page et animations

- Grille visible quand elle aide : filets noirs de 2 px qui découpent la slide en zones, comme un tableau HTML.
- Alignement à gauche, texte qui touche presque les bords (marges de 48 à 64 px), blocs empilés.
- Contraste brutal d'échelle : un titre de 340 px coupé par le bord à côté d'un texte de 28 px.
- Les chiffres en barres ASCII (`██████████░░░░ 71 %`) ou en tableau HTML brut.
- Animations "machine" : apparition instantanée ligne par ligne (effet terminal, 60 ms par ligne), curseur qui clignote, `wipe` en escalier (`steps(12)`). Jamais de fondu doux ni de rebond.

## 7. Bibliothèque de layouts

| Contenu | Layout | Astuce |
| --- | --- | --- |
| Cover | Page d'accueil `index.html` : titre géant, sous-titre en Tinos, liens bleus | Curseur clignotant, compteur de visiteurs |
| Sommaire | Listing `Index of /deck/` : dossiers, dates, tailles | Les parties vues en violet |
| Problème | Page `404 Not Found` : ce qui manque aujourd'hui | "Le serveur n'a pas trouvé de bonne solution" |
| Processus, démo | Terminal : commandes et sorties, une étape par ligne | Fond noir, vert terminal |
| Avant / après | Diff : lignes rouges supprimées, lignes vertes ajoutées | `- ancien process` / `+ nouveau process` |
| Roadmap | `CHANGELOG.md` : versions, dates, ajouts | La version à venir en jaune surligneur |
| Offre, prix | Formulaire HTML : boutons radio, cases, bouton "Envoyer" gris | Le plan recommandé coché |
| Chiffres | Barres ASCII ou tableau HTML à bordures | Le chiffre clé surligné en jaune |
| Produit | `README.md` : titre, badges en texte, installation, usage | Blocs de code en mono |
| Persona, besoin | Ticket d'issue : titre, auteur, labels, description | `#142 ouvert par lea` |
| Historique | Fil de commits : hash, auteur, message, date | Messages de commit drôles et précis |
| Statement | Boîte d'alerte système avec un bouton OK | Une phrase, rien d'autre |
| Équipe | Page "À propos" de 1998 : photos tramées, liens mailto | Noms en liens bleus |
| Closing | Pied de page : "© 2026", "Retour en haut", contact | Un lien bleu vers la démo |

## 8. Ton des textes

- Direct, technique, honnête, pince-sans-rire.
- Les titres peuvent être des commandes, des noms de fichiers ou des messages système : `npm install kori`, `Erreur 404 : bon café introuvable`.
- Phrases courtes, présent, pas de jargon marketing ("révolutionnaire", "solution innovante").
- L'humour vise les clichés tech et les process absurdes, jamais les gens.

## 9. Interdits spécifiques

- Coins arrondis, ombres floues, dégradés, glassmorphism.
- Maquettes d'iPhone ou de MacBook autour des captures.
- Polices "modernes" de startup (géométriques rondes) à la place des polices système.
- Plus de 2 couleurs pop par slide.
- Un brutalisme illisible : la brutalité est dans la forme, jamais dans la lisibilité (texte 24 px minimum, contraste fort).

## 10. Check avant de livrer

- [ ] Barre d'adresse et compteur de visiteurs sur chaque slide.
- [ ] Aucun arrondi, aucune ombre floue, aucun dégradé.
- [ ] 2 couleurs pop maximum par slide, terminal en vert seul.
- [ ] Images tramées en 1 bit ou captures brutes encadrées.
- [ ] Chaque layout reprend un objet réel du web ou du code (404, diff, README, terminal).
- [ ] Le texte reste lisible projeté : 24 px minimum.
