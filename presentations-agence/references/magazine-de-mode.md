# Style "Magazine de mode"

## 1. L'idée et quand l'utiliser

**En une phrase** : le sujet est traité comme une couverture et un éditorial de magazine, avec une photo pleine page qui domine, un serif à fort contraste, énormément d'air et des légendes minuscules.

Univers de référence : les magazines de mode et de culture, les lookbooks, les catalogues de collection, les éditoriaux photo. Ses objets servent de layouts : la couverture et ses accroches, le sommaire, l'édito signé, la double page photo, la fiche look avec crédits, l'interview, la page shopping, le backstage, le calendrier des défilés, le questionnaire de dernière page.

**Quand l'utiliser**
- Mode, beauté, cosmétique, design, art de vivre, hôtellerie, gastronomie haut de gamme.
- Un lancement de collection, un rebranding, une campagne, un portfolio de créatif.
- Une marque qui vit par l'image, et quand on dispose de belles photos (de l'utilisateur, d'Unsplash ou générées).

**Quand l'éviter**
- Pas de photos de qualité : le style s'effondre sans elles.
- Beaucoup de données ou un public technique.

## 2. Palette

| Rôle | Hex | Règle |
| --- | --- | --- |
| Blanc magazine | `#FAF9F6` | Fond des pages de texte |
| Noir | `#0E0E0E` | Titres, texte, pages sombres |
| Greige | `#D8CFC4` | Fonds de pages calmes, aplats derrière les produits |
| Gris légende | `#8A857E` | Légendes, crédits, folios |
| Couleur saison | prélevée dans la photo, ex. `#9E1B32` | Un mot, un trait, une page entière au plus |

- **Règle : la couleur vient de la photo.** Prélever la couleur saison à la pipette dans la photo principale du deck. Une seule couleur saison pour tout le deck.
- La plupart des slides sont en noir et blanc + photo. La couleur saison apparaît sur 1 slide sur 3.

```css
:root{
  --white:#FAF9F6; --black:#0E0E0E; --greige:#D8CFC4; --grey:#8A857E; --season:#9E1B32;
  --f-didone:"Bodoni Moda",serif; --f-label:"Jost",sans-serif; --f-text:"EB Garamond",serif;
}
.slide{background:var(--white);color:var(--black);font-family:var(--f-text)}
.masthead{font:400 300px/.8 var(--f-didone);letter-spacing:-.04em}
.cover-line{font:500 22px/1.25 var(--f-label);letter-spacing:.14em;text-transform:uppercase}
```

## 3. Polices

| Rôle | Google Fonts | Usage |
| --- | --- | --- |
| Didone | Bodoni Moda (400 à 700, italique) | Titre du magazine, titres d'articles (80 à 320 px), chiffres, citations en italique |
| Labels | Jost (400, 500) | Accroches de couverture, rubriques, crédits, numéros de look, en capitales espacées (.14em à .3em) |
| Texte | EB Garamond (400, italique) | Chapô et texte courant (26 à 32 px), lettrines |

Alternatives : Playfair Display pour la didone, Cormorant pour le texte, Josefin Sans pour les labels.

## 4. Éléments signature

- **Le titre du magazine géant** derrière le sujet de la photo : la tête ou l'objet passe devant les lettres (photo détourée posée par-dessus, ou titre placé dans le vide du ciel).
- **Accroches de couverture** (cover lines) en petit, autour du sujet, alignées sur les bords.
- **Folio** en bas : "KŌRI · NOVEMBRE 2026 · 47", en Jost 18 px gris.
- **Crédits photo verticaux** le long du bord droit.
- **Numéros de look** ("LOOK 07") et **crédits produit** ("Canette 33 cl, aluminium recyclé, 3,20 €").
- **Lettrine** en Bodoni sur 4 lignes au début des textes.

## 5. Traitement des images

- Préréglage `mode` : contraste doux, noirs légèrement relevés (fondu), saturation à peine baissée, grain très fin. Pas de dégradé sombre : **en mode, on ne noircit pas une photo pour poser du texte**. On place le texte dans le vide de l'image (ciel, mur, sol).
- Choisir des photos avec beaucoup d'espace négatif, une lumière naturelle et un sujet net. Portrait pour les pages simples, paysage pour les doubles pages.
- Cadrages audacieux : très serrés (détail, main, matière) ou très larges (silhouette minuscule).
- Une photo par slide, pleine page ou demi-page à fond perdu. Jamais de cadre ni d'ombre.
- Détourage du sujet pour passer devant le titre seulement si le PNG est parfait. Sinon, placer le titre dans le vide.

```bash
python scripts/images.py traiter raw/portrait.jpg assets/cover.jpg --taille 1920x1080 --preset mode --cadre 0.6,0.35
python scripts/images.py traiter raw/detail.jpg assets/detail.jpg --taille 960x1080 --preset mode
```

## 6. Mise en page et animations

- La photo occupe 50 à 100 % de la slide. Le texte occupe le vide restant.
- Énormément d'air : marges de 120 px, une seule idée par page.
- Contraste d'échelle extrême : un titre de 300 px à côté d'une légende de 18 px.
- Alignements soignés mais asymétriques : une colonne de texte étroite (360 à 480 px) au bord d'une grande photo.
- Animations lentes et élégantes : `fade` de 1 s pour les photos, `rise` lent pour les titres, aucun rebond. La transition idéale ressemble à une page qu'on tourne.

## 7. Bibliothèque de layouts

| Contenu | Layout | Astuce |
| --- | --- | --- |
| Cover | Couverture : photo pleine page, titre du magazine géant, 3 accroches | Le sujet passe devant le titre, ou le titre dans le ciel |
| Sommaire | Numéros de page en Bodoni géant + titres en Jost + 2 vignettes | Le numéro est l'élément graphique |
| Vision, manifeste | Édito : texte en EB Garamond sur une colonne, signature manuscrite ou en italique | Portrait en petit, en haut |
| Statement | Double page photo, une phrase en italique dans le vide | Rien d'autre |
| Gamme, collection | Lookbook : grille irrégulière de 3 à 5 photos de tailles différentes | Numéros de look sous chaque photo |
| Produit | Fiche look : photo demi-page + crédits produit (matière, prix) | Liste en Jost, prix en Bodoni |
| Persona, client | Interview : grand portrait, questions en Jost, réponses en Garamond | Citation en exergue en italique géant |
| Chiffre clé | Chiffre en Bodoni de 400 px, légende en Jost | La couleur saison sur le chiffre |
| Plusieurs chiffres | Double page photo : le chiffre héros posé dans le vide de l'image (mur, ciel, fenêtre), les autres en colonne étroite | Jamais trois chiffres égaux alignés : retour utilisateur « très générique » |
| Offre, prix | Page shopping : produits détourés sur greige, prix en légende | Des vrais produits, des vrais prix |
| Inspiration | Moodboard : photos, matières, couleurs posées sur fond greige | Une pastille de la couleur saison |
| Processus | Backstage : planche contact noir et blanc, notes manuscrites | Une image entourée = l'étape clé |
| Planning | Calendrier des défilés : dates, lieux, heures en colonnes | Une date en couleur saison |
| Segments | Horoscope de la cible : 4 à 6 profils écrits comme des signes | L'humour vise les habitudes |
| Closing | Dernière page : questionnaire en 5 questions ou une photo et le nom | Titre du magazine en petit en bas |

## 8. Ton des textes

- Peu de mots, choisis. Titres de 1 à 5 mots, souvent en italique.
- Voix éditoriale : élégante, sensorielle, assurée. "La nuit, le café se boit froid."
- Accroches de couverture comme un vrai magazine : "Le cold brew, enfin pressé", "48 heures d'infusion", "Spécial Lyon".
- Les crédits sont précis et sérieux (matière, origine, prix) : ils donnent la preuve sous l'élégance.

## 9. Interdits spécifiques

- Assombrir une photo avec un dégradé pour y poser du texte.
- Plus d'une couleur saison, ou une couleur qui n'est pas dans les photos.
- Texte long, puces, tableaux denses.
- Photos de qualité moyenne, pixelisées, ou de banque d'images trop posées (sourires figés, mains sur ordinateur).
- Cadres, ombres, coins arrondis autour des photos.
- Faux noms ou faux logos de vrais magazines : le magazine porte le nom du sujet.

## 10. Check avant de livrer

- [ ] Chaque photo est nette en taille réelle et traitée avec le préréglage `mode`.
- [ ] Le texte est posé dans le vide des photos, jamais sur un dégradé ajouté.
- [ ] Une seule couleur saison, prélevée dans une photo du deck.
- [ ] Folio et crédits sur chaque slide.
- [ ] Le titre du magazine passe devant le sujet volontairement, ou reste entièrement dans le blanc : jamais une lettre à moitié sur le bord de la photo.
- [ ] Contraste d'échelle visible sur la planche contact (titres géants, légendes minuscules).
- [ ] Aucun nom ni logo de magazine réel.
