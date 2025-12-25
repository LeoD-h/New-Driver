# NewDriver

Jeu de voiture controle par detection de la tete via YOLO.

## Structure du projet

```
NewDriver/
├── README.md
├── game/                       # JEU PRINCIPAL
│   ├── main.py                # Point d'entree (python game/main.py)
│   ├── constants.py           # Constantes
│   ├── entities.py            # Voiture et obstacles
│   ├── tracker.py             # Detection YOLO
│   └── ui.py                  # Interface utilisateur
├── training/                   # Entrainement du modele
│   ├── train.py               # Script d'entrainement
│   └── runs/detect/           # Modeles entraines
├── Dataset/                    # Donnees d'entrainement
│   ├── labelledImg/           # Images labellisees
│   └── YOLO_Ready/            # Dataset formate YOLO
└── Gen/                        # Outils de generation
```

## Classes du modele

| ID | Nom | Action |
|----|-----|--------|
| 0 | visage_serieux | Stop/Freiner |
| 1 | livre_droite | Tourner a droite |
| 2 | livre_milieu | Tout droit |
| 3 | livre_gauche | Tourner a gauche |
| 4 | visage_sourire | Accelerer |

## Utilisation

### Lancer le jeu
```bash
cd NewDriver
python game/main.py
```

### Entrainer le modele
```bash
cd NewDriver
python training/train.py
```

## Controles du jeu

- **Livre a GAUCHE** -> Voiture tourne a gauche
- **Livre au MILIEU** -> Voiture va tout droit
- **Livre a DROITE** -> Voiture tourne a droite
- **SOURIRE** -> Accelerer
- **SERIEUX** -> Freiner/Stop

### Clavier
- **T** : Mode test (desactive obstacles)
- **ESPACE** : Rejouer
- **ESC** : Quitter
- **Fleches** : Controle manuel (debug)
