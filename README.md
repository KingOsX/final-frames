# Final Frames

Automatisation de l'extraction de la première et dernière frame de vidéos.

## Fonctionnement

Dépose des vidéos dans le dossier `A traiter/` — le script les détecte automatiquement, extrait les frames, et organise le tout dans `Vidéos/`.

```
Final Frames/
├── A traiter/          ← déposer les vidéos ici
├── Vidéos/             ← résultat final
│   └── nom_video/
│       ├── nom_video.mp4
│       ├── nom_video_first.jpg
│       ├── nom_video_last.jpg
│       └── folder.jpg          ← miniature du dossier (Windows Explorer)
└── process_videos.py
```

## Prérequis

- Python 3.x
- [ffmpeg](https://ffmpeg.org/) accessible dans le PATH

## Lancement

```bash
python process_videos.py
```

Le script surveille `A traiter/` toutes les 5 secondes et traite automatiquement toute nouvelle vidéo détectée. Arrêt avec `Ctrl+C`.

## Formats supportés

`.mp4` `.mov` `.avi` `.mkv` `.wmv` `.flv` `.webm` `.m4v`

## Comportement

- La **première frame** est extraite avec ffmpeg (`-vframes 1`)
- La **dernière frame** est extraite avec `-sseof` (essais à -3s, -1s, -0.5s avant la fin)
- Un fichier `folder.jpg` est créé automatiquement → Windows Explorer affiche la première frame comme miniature du dossier
- Les fichiers vides ou corrompus sont ignorés
- Si un fichier est verrouillé lors du déplacement, le script réessaie au cycle suivant
