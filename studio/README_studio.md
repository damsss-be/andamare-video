# Studio Andamare — boîte à outils de la chaîne vidéo

Construit le 11/11/2026 (bêta « tâche 3 »), rangé dans ce dépôt GitHub le 21/11/2026 pour la tâche automatique 2. But : que le Réalisateur passe son temps sur l'image et le son de la vidéo, pas à réécrire un moteur de rendu à chaque production. Tout est gratuit et sous licence libre.

Le studio fournit des OUTILS, pas un style. Aucun de ces outils ne doit devenir le visuel par défaut : le rendu change à chaque vidéo (voir la règle d'alternance du fichier de chaîne).

## Mise en place (une fois par production)
Lancer `bash studio/verifier.sh` depuis la racine du dépôt (≈20 s) : il installe ce qui manque et vérifie que le rendu marche.
Copier `studio/studio.py` (et, si besoin, `studio/3d/scene3d_base.html`) dans le dossier de travail de la vidéo, ou l'appeler par son chemin. Pour la 3D : `npm install three@0.160` dans le dossier de travail.

## Les commandes (`python3 studio.py <commande> --help`)
| Commande | Sert à | Exemple |
|---|---|---|
| `polyhaven chercher` | trouver un modèle 3D, une texture ou un éclairage réaliste (CC0) | `polyhaven chercher --type modele --mots chair` |
| `polyhaven prendre` | le télécharger dans `assets/` | `polyhaven prendre --nom ArmChair_01` ; `--type texture --nom wood_floor_deck` ; `--type eclairage --nom lythwood_lounge` |
| `police` | télécharger une vraie police Google Fonts | `police "Bebas Neue" --graisse 400` |
| `pixabay` | chercher de vraies vidéos ou photos | `pixabay video ocean waves --cle <fichier de clé>` |
| `openverse` | chercher des sons et musiques CC0 (Wikimedia Commons) | `openverse applause` |
| `telecharger` | télécharger un résultat | `telecharger <url> clip.mp4` |
| `vertical` | découper une vraie vidéo, la cadrer en 9:16, l'étalonner | `vertical clip.mp4 p1.mp4 --debut 2 --duree 1.6 --etalonnage cinema` |
| `rendre` | rendre une page HTML animée image par image, avec ou sans son | `rendre scene.html v.mp4 --fin 12 --brouillon` |
| `mixer` | assembler musique et bruitages calés, volume normalisé | `mixer son.wav --piste musique.wav:0:0.6 --piste clic.wav:3.2:1 --duree 16` |
| `planche` | planche d'images horodatées pour juger | `planche v.mp4 planche` |
| `mesures` | durée, nombre de plans, durée moyenne d'un plan, poids | `mesures v.mp4` |

`--brouillon` = 540×960 (retouches) ; sans = 1080×1920 (rendu final, une seule fois).
Étalonnages de `vertical` : aucun, chaud, froid, cinema, vif, noir_blanc.

## Contrat d'une page pour `rendre`
La page met `window.ready = true` quand tout est chargé, et expose `window.frame(t)` qui dessine l'instant `t` en secondes. Aucune animation ne dépend de l'horloge réelle. Une page peut tout contenir : 3D, canvas 2D, vidéos réelles en fond (balise `<video>` positionnée avec `currentTime = t`), textes en vraies polices (`@font-face` vers `assets/…ttf`).

## 3D réaliste : `scene3d_base.html`
Fonctions prêtes : `eclairage`, `soleil`, `sol`, `mur`, `modele`, `poser`, `image`, `lisse`, `rebond`. Remplacer le bloc « LA SCÈNE ». Environ 1 s par image en brouillon.
Pièges déjà rencontrés (Damien les a vus) :
- Un objet sans sol réel flotte dans le vide : toujours un `sol`, et un `mur` ou un vrai décor dès que la caméra bouge.
- Exposition entre 0,4 et 0,7 ; au-delà l'image est brûlée et jaune.
- Vérifier sur une image que chaque objet est posé, à la bonne échelle, avec son ombre de contact.
- Les modèles Poly Haven sont des décors et des objets de la vie courante. Un produit du catalogue se montre avec sa vraie photo (fonction `image`), jamais avec un modèle qui lui ressemble.
L'ancien moteur à facettes `studio/3d/moteur_3D_lowpoly.html` reste disponible pour un rendu volontairement stylisé.

## Sons
Pixabay n'a pas d'accès programmé à ses musiques, et certains sites refusent le téléchargement (erreur 403). Dans ce cas : prendre un autre résultat, ou composer la musique et les bruitages par code. Ne jamais contourner un refus.
Pas de voix de synthèse (Damien, 11/11/2026). Une voix n'est utilisée que si elle a été enregistrée par Damien ou Andrew et rangée dans « Claude - Matière ».

## Faire grandir le studio
Quand une production invente un outil réutilisable (un effet, un type de montage, un générateur de texture), le Chef d'orchestre le range dans `studio/` après un « oui » de Damien, ajoute une ligne ici, puis fait un commit et un push (voir CLAUDE.md). On range un outil, jamais un style à refaire.
- `rendu_png.py` (vidéo 25, 12/11/2026) : rend une plage de secondes d'une page animée (contrat `window.ready` / `window.frame(t)`) en PNG numérotés ; reprend là où il s'est arrêté après une coupure et permet de ne re-rendre que les plans modifiés avant un seul encodage. `python3 rendu_png.py page.html dossier --debut 0 --fin 11 [--brouillon]`.
- `incrustation_fond_vert.py` (vidéo 25, 12/11/2026) : incruste une vraie vidéo de personne filmée sur fond vert (Pixabay) : détourage opaque à 100 %, retrait du débord vert, couleurs réchauffées par la lumière de la scène, liseré, flou de profondeur. Les réglages `PLANS` sont des exemples propres à la vidéo 25 : les réécrire à chaque usage.
