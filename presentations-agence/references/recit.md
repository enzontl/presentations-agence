# Récit : le fond avant la forme

Un beau deck sur un récit flou reste un deck faible. Ce fichier sert à l'étape 1 du procédé : fixer le message, la storyline et le plan avant toute slide. Il se lit avec `fond.md`, la page de travail du deck.

## 1. Le message en une phrase

Écrire la phrase que le public doit répéter en sortant. Elle a un sujet, un verbe et une conséquence.

- Faible : « Présentation du projet Kōri. »
- Fort : « Le cold brew en canette peut devenir un réflexe en épicerie fine, à condition de baisser la marge du distributeur. »

Si la phrase ne tient pas, le sujet n'est pas prêt : revenir à la recherche, pas aux slides.

## 2. Affirmation et preuve

C'est la règle de chaque slide. **Le titre est une phrase qui affirme** ; **le corps de la slide en est la preuve** (un chiffre, un graphique, un objet, une photo). Rien d'autre.

| Titre étiquette (à éviter) | Titre qui affirme |
| --- | --- |
| Le marché | Le marché du café froid double en trois ans |
| Fréquentation | Les entrées progressent pour la quatrième année |
| Notre solution | Une canette infusée 48 heures, vendue 3,20 € |
| Conclusion | Trois décisions à prendre avant mars |

Test : les titres lus d'affilée (`titres.txt` après `rendu.py`) racontent toute l'histoire, sans les slides.

## 3. Choisir une structure

| Structure | Quand | Déroulé |
| --- | --- | --- |
| **SCQA** (situation, complication, question, réponse) | Comité, conseil, restitution | Ce qui est vrai aujourd'hui, ce qui change, la question que ça pose, notre réponse |
| **Pyramide** (la réponse d'abord) | Public pressé, direction | La conclusion en slide 2, puis trois arguments, chacun avec ses preuves |
| **Problème, solution, preuve** | Pitch, lancement | La douleur concrète, ce qu'on propose, pourquoi ça marche (chiffres, test, clients) |
| **Trois actes** | Conférence, grand public | Le monde avant, le basculement, le monde après |
| **Constat puis sens** | Bilan, rapport annuel | Les chiffres de l'année, ce qu'ils veulent dire, ce qu'on fait ensuite |
| **Question puis enquête** | Étude, mémoire, data | La question, la méthode en une slide, les découvertes une par une, la réponse |

## 4. Les plans types

Un plan = une liste de types de contenu, à passer à `scripts/tirage.py --plan`. Les adapter, ne pas les remplir de force.

**Pitch, 10 slides, 10 minutes**
`cover, contexte, chiffre-cle, offre, comparaison, repartition, etapes, equipe, plusieurs-chiffres, closing`
Problème, preuve que le problème est grand, la solution, en quoi elle est meilleure, le modèle économique, le plan, l'équipe, ce qu'on demande, la phrase finale.

**Soutenance ou mémoire, 12 slides, 15 minutes**
`cover, sommaire, contexte, methode, chiffre-cle, evolution, comparaison, territoire, avant-apres, citation, plusieurs-chiffres, closing`

**Bilan ou rapport annuel, 8 slides**
`cover, plusieurs-chiffres, evolution, repartition, comparaison, citation, etapes, closing`

**Restitution d'étude, 10 slides**
`cover, chiffre-cle, methode, comparaison, evolution, repartition, persona, avant-apres, plusieurs-chiffres, closing`

## 5. Le minutage

- Compter 45 secondes à 1 minute par slide de contenu, 15 secondes pour une cover ou un intercalaire.
- 10 minutes d'oral : 8 à 12 slides. Au-delà, l'orateur court et le public décroche.
- Mettre les détails, les tableaux complets et les sources longues en **annexes**, après la slide de fin : elles servent aux questions, pas à l'oral.

## 6. Problèmes fréquents et corrections

| Problème | Signe | Correction |
| --- | --- | --- |
| Mur de texte | Plus de 30 mots sur la slide | Affirmation + preuve, le reste dans les notes |
| Maladie des puces | Une liste à la place d'une idée | Une idée par slide, montrée par un objet ou un chiffre |
| Slide fourre-tout | Trois messages sur une slide | La couper en trois, ou garder le plus fort |
| Joli mais vide | Une belle image sans affirmation | Écrire d'abord le titre-phrase, puis choisir l'image qui le prouve |
| Surcharge | Le public doit lire et écouter en même temps | Trois niveaux de texte au plus, l'orateur dit le reste |
| Chiffre orphelin | Un chiffre sans comparaison | Le comparer : à l'an dernier, au concurrent, à une chose connue (« 3 fois la taille de… ») |

## 7. Le script dans les notes

- Des phrases parlées, pas un résumé : écrire ce que l'orateur dit, mot pour mot ou presque.
- 80 à 130 mots par slide de contenu (environ 45 secondes à 1 minute).
- La première phrase reprend le titre avec d'autres mots ; la dernière amène la slide suivante.
- Le prénom de l'orateur en tête s'il y en a plusieurs.
- Les sources et les crédits photo à la fin des notes.

## 8. Préparer les questions

Lister dans `fond.md` les 5 questions les plus probables du public et la slide d'annexe ou le chiffre qui y répond. Un jury pose presque toujours : la source d'un chiffre clé, la limite de la méthode, le coût, le calendrier, et « pourquoi vous ».

## 9. Le script scène par scène (deck à plusieurs voix)

Pour un oral à plusieurs, écrire un fichier `script.md` à côté du deck, dans ce format (repris d'un pitch à cinq voix de 20 minutes) :

- **En tête** : la durée, la distribution (qui dit quelles scènes), le nombre de mots par orateur. Compter 130 mots parlés par minute : 2 600 mots pour 20 minutes, environ 500 par orateur à cinq.
- **Une section par scène** : `## SCÈNE 4 · CE QUE SEUL X POSSÈDE`, puis `**3:40 à 4:50 · PRÉNOM**`.
- **À L'ÉCRAN** : ce que montre la slide, en une phrase. Pas dit à voix haute.
- **Le texte parlé**, mot pour mot, avec `[clic]` à chaque sous-étape.
- *(Didascalies en italique entre parenthèses)* : gestes, passage de relais, démo. Pas dites.
- **Si on demande** : les réponses préparées aux questions probables sur cette scène.

Le texte de chaque scène va tel quel dans les notes de sa slide : la vue présentateur (`P`) l'affiche pendant l'oral.

## 10. La feuille de calcul et les annexes de secours

- **Chaque chiffre a sa ligne de calcul**, à la fin du script ou dans `fond.md` : le chiffre, la formule, chaque hypothèse dite à voix haute, la source. Exemple : « 6,3 % de contacts qualifiés = 45 000 formulaires × 15 % de bons contacts ÷ 107 000 visiteurs des pages programme ». Un jury qui demande « d'où vient ce chiffre ? » doit recevoir la ligne en dix secondes.
- **Les annexes de secours** viennent après la slide de fin, jamais pendant l'oral : le détail complet (les dix cas d'usage, la matrice chiffrée) et une slide « Chaque chiffre, et d'où il vient ». On y saute avec la vue d'ensemble (`O`).
- **La démo en direct a un plan B** : une exécution enregistrée qui s'affiche d'elle-même si le service ne répond pas dans les 15 secondes, et une slide qui dit comment la relancer.
