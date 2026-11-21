# Dépôt andamare-video — consignes pour la tâche automatique 2

Ce dépôt sert à la tâche automatique 2 (essai) de la chaîne vidéo d'Andamare. Les consignes de production (règles de Damien, chaîne, registre, statut) ne sont PAS ici : elles restent dans les instructions de la tâche et dans les fichiers du projet « Business Andamare ». En cas de contradiction, les instructions de la tâche et les règles de Damien priment sur ce fichier.

## Répartition des outils pour le montage
- **HyperFrames** (skill `hyperframes`, outil `npx hyperframes`) : composer et rendre la vidéo (animations, textes, transitions, sous-titres, effets de la bibliothèque).
- **Studio** (`studio/studio.py`) : préparer la matière avant HyperFrames — chercher et télécharger des vidéos et photos Pixabay, modèles et textures Poly Haven, polices, sons Openverse ; découper et cadrer un rush en 9:16 (`vertical`) ; juger le résultat (`planche`, `mesures`). C'est aussi la solution de repli complète si HyperFrames ne marche pas.
- **Connecteurs de la tâche** : Unsplash (photos et illustrations libres), Canva (générer une image), Moda (retoucher une image existante).

## Utiliser le studio
- Au début de chaque production : `bash studio/verifier.sh`. S'il échoue, continuer sans le studio (comme avant) et le signaler à Damien à la livraison.
- Le Metteur en scène-Monteur utilise `studio/studio.py` (commandes : `python3 studio/studio.py <commande> --help`) au lieu de réécrire un moteur de rendu. Mode d'emploi et pièges connus : `studio/README_studio.md`. Le lui transmettre quand tu le lances.
- Le studio fournit des outils, pas un style : il ne doit jamais imposer un visuel par défaut.
- Clé Pixabay : uniquement depuis le fichier du PC « Pour Claude\Cle_Pixabay.txt », stagé dans la session. Ne jamais l'afficher, la recopier, ni la mettre dans le dépôt.

## Les skills du dépôt (.claude/skills/)
Skills publics sous licence libre (voir `licences/` et `TIERS.md`), ajoutés le 21/11/2026 à la demande de Damien. Ce sont des sources de savoir-faire et d'inspiration : les règles de Damien, les instructions de la tâche et les fichiers de chaîne passent toujours avant eux. Quand un skill contredit une règle de Damien, la règle de Damien gagne, sans exception.

Qui s'en sert (donne-leur les noms et le chemin `.claude/skills/<nom>/SKILL.md` quand tu les lances). ÉCONOMIE : un agent n'ouvre un skill que si la vidéo en a besoin, et pas plus de 3 par agent et par production.
- **Idéateur** : `social` (scripts de vidéos courtes, accroches), `ad-creative` (angles), `marketing-psychology` (ce qui donne envie, honnêtement) ; au besoin `marketing-ideas`, `video`, `content-strategy`, `customer-research`, `product-marketing`.
- **Contrôleur et Critique** : `ad-creative` pour juger l'accroche et l'angle ; `copy-editing` et `copywriting` pour les textes à l'écran.
- **Metteur en scène-Monteur** : `hyperframes` (à lire en premier), `motion-doctrine` (enchaînements des plans), `cut-the-curve` (catalogue de transitions et d'entrées de texte), `hyperframes-registry` (effets, titres et transitions prêts à l'emploi) ; au besoin `captions-overlay` (sous-titres), `seam-craft` (flashs entre les plans), `manim-video` (schémas animés), `video-use` quand la matière contient de vrais rushs filmés.
- **Agent son** : `media-use` (musique, bruitages, mixage — uniquement les outils gratuits et locaux).
- **Conservateur / analyse des Références de style** : `reverse-any-video` sert ici UNIQUEMENT à analyser le rythme, le montage et la structure des vidéos de référence ; jamais à les reproduire ni à en intégrer un morceau (règle de Damien du 18/11/2026).

Réglages imposés par Damien pour HyperFrames et media-use :
- Format : vertical 1080×1920, 30 i/s (HyperFrames démarre par défaut en 1920×1080 : toujours le changer).
- Pas de voix de synthèse (Damien, 11/11/2026) : aucune voix générée, aucun avatar. Une voix n'est utilisée que si Damien ou Andrew l'ont enregistrée dans « Claude - Matière ».
- Aucune fonction payante, aucun compte HeyGen ni aucun autre service payant : ne jamais créer de compte, se connecter ni payer. Si une étape demande HeyGen, prendre l'alternative gratuite et locale que le skill indique, sinon s'en passer.
- Pas d'aperçu à valider par Damien pendant la production (il n'est pas là) : le rendu final se fait après la relecture interne, puis la vidéo est livrée comme le prévoient les instructions de la tâche. Ne pas proposer l'application de bureau HyperFrames.
- Si HyperFrames ne s'installe pas ou ne rend pas (outil `npx hyperframes`), repasser au studio (`studio/`) sans bloquer, et le signaler à la livraison.

## Ce qui n'entre jamais dans le dépôt
Vidéos, images, sons, matière, catalogue, archives, clés, fichiers de travail d'une production (voir `.gitignore`). Seule exception : les images et exemples fournis avec les skills tiers dans `.claude/skills/`.

## Faire grandir le studio
Quand une production invente un outil réutilisable (effet, type de montage, générateur), et seulement après le « oui » de Damien sur la vidéo :
1. ranger l'outil dans `studio/` (général, sans réglages propres à une vidéo, ou avec des exemples clairement marqués comme tels) ;
2. ajouter une ligne dans la section « Faire grandir le studio » de `studio/README_studio.md` ;
3. lancer `bash studio/verifier.sh` ;
4. commit (message en français, court) et push sur `main`.
Ne jamais supprimer ni réécrire un outil existant sans l'accord de Damien. On range un outil, jamais un style à refaire.
