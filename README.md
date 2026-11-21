# andamare-video

La boîte à outils de la **tâche automatique 2** (chaîne de production vidéo d'Andamare, version d'essai).

La tâche 1 n'utilise pas ce dépôt : elle continue de fonctionner comme avant.

## Ce qu'il y a dedans
- `studio/` : les outils de montage réutilisés à chaque vidéo (rendu image par image, cadrage vertical, mixage du son, planches, mesures, 3D). Mode d'emploi : `studio/README_studio.md`.
- `studio/verifier.sh` : vérifie en 20 secondes que les outils marchent.
- `.claude/skills/` : 70 skills publics sous licence libre (HyperFrames de HeyGen pour le montage pro, skills marketing de Corey Haines, video-use pour les vrais rushs). Liste et licences : `TIERS.md`.
- `CLAUDE.md` : les consignes que Claude lit automatiquement quand la tâche ouvre le dépôt.

## Ce qu'il n'y a pas dedans
Les vidéos, la matière, le catalogue et la clé Pixabay restent sur le PC (« Pour Claude ») et sur le Drive. Les consignes de production restent dans le projet « Business Andamare ».

## Revenir en arrière
Chaque changement est enregistré dans l'historique (onglet « Commits » sur GitHub). Si un changement casse quelque chose, on peut revenir à la version d'avant.
