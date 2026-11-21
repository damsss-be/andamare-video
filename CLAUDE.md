# Dépôt andamare-video — consignes pour la tâche automatique 2

Ce dépôt sert à la tâche automatique 2 (essai) de la chaîne vidéo d'Andamare. Les consignes de production (règles de Damien, chaîne, registre, statut) ne sont PAS ici : elles restent dans les instructions de la tâche et dans les fichiers du projet « Business Andamare ». En cas de contradiction, les instructions de la tâche et les règles de Damien priment sur ce fichier.

## Utiliser le studio
- Au début de chaque production : `bash studio/verifier.sh`. S'il échoue, continuer sans le studio (comme avant) et le signaler à Damien à la livraison.
- Le Metteur en scène-Monteur utilise `studio/studio.py` (commandes : `python3 studio/studio.py <commande> --help`) au lieu de réécrire un moteur de rendu. Mode d'emploi et pièges connus : `studio/README_studio.md`. Le lui transmettre quand tu le lances.
- Le studio fournit des outils, pas un style : il ne doit jamais imposer un visuel par défaut.
- Clé Pixabay : uniquement depuis le fichier du PC « Pour Claude\Cle_Pixabay.txt », stagé dans la session. Ne jamais l'afficher, la recopier, ni la mettre dans le dépôt.

## Ce qui n'entre jamais dans le dépôt
Vidéos, images, sons, matière, catalogue, archives, clés, fichiers de travail d'une production (voir `.gitignore`). Le dépôt ne contient que du code et du texte.

## Faire grandir le studio
Quand une production invente un outil réutilisable (effet, type de montage, générateur), et seulement après le « oui » de Damien sur la vidéo :
1. ranger l'outil dans `studio/` (général, sans réglages propres à une vidéo, ou avec des exemples clairement marqués comme tels) ;
2. ajouter une ligne dans la section « Faire grandir le studio » de `studio/README_studio.md` ;
3. lancer `bash studio/verifier.sh` ;
4. commit (message en français, court) et push sur `main`.
Ne jamais supprimer ni réécrire un outil existant sans l'accord de Damien. On range un outil, jamais un style à refaire.
