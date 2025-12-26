# NewDriver 🚗

Jeu de voiture contrôlé par la tête et le regard via YOLO + Eye Tracking.

## 🎮 Deux versions

### Version Pygame (Desktop)
```bash
python game/main.py
```

### Version Web (Flask)
```bash
cd webapp
python app.py
# Ouvrir http://localhost:8080
```

## 📁 Structure

```
NewDriver/
├── game/                  # Version Pygame
├── webapp/                # Version Web Flask
├── training/              # Entrainement YOLO
├── scripts/               # Outils
├── Dataset/               # Données
└── Gen/                   # Génération
```

## 🤖 Classes YOLO

| ID | Nom | Action |
|----|-----|--------|
| 0 | visage_serieux | Freiner |
| 1 | livre_droite | Tourner droite |
| 2 | livre_milieu | Tout droit |
| 3 | livre_gauche | Tourner gauche |
| 4 | visage_sourire | Accélérer |

## 👁️ Eye Tracking

- **Regarde l'écran** → Peut accélérer
- **Ne regarde pas** → Freine automatiquement
- **Yeux fermés** → Détection somnolence

## 🎮 Contrôles

| Action | Contrôle |
|--------|----------|
| Direction | Position du livre |
| Accélérer | Sourire |
| Freiner | Visage sérieux |
| Mode Test | Touche T |

## 🚀 Scripts

```bash
python scripts/train.py          # Entraîner
python scripts/test_interface.py # Tester webcam
python scripts/organizer.py      # Créer YOLO_Ready
```

## ⚙️ Environnement

```bash
conda activate yolo
pip install ultralytics pygame flask opencv-python
```
