"""
Tracker de tete pour NewDriver
Detecte la position du livre et l'expression du visage
"""

import cv2
import threading
from pathlib import Path

try:
    from ultralytics import YOLO
except ImportError:
    print("Erreur: ultralytics n'est pas installe")
    exit(1)

from .constants import CLASS_NAMES


class HeadTracker:
    """Detecteur de position du livre et expression via YOLO"""
    
    def __init__(self, model_path):
        self.model = YOLO(str(model_path))
        self.cap = None
        self.running = False
        self.current_direction = "MILIEU"
        self.current_action = "STOP"
        self.confidence = 0.0
        self.frame = None
        self.lock = threading.Lock()
        self.detections = []
        
        # INVERSION DES CONTROLES (camera miroir)
        self.invert_x = True
        
    def start(self):
        """Demarre la capture webcam"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Erreur: Impossible d'ouvrir la webcam")
            return False
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        self.running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        return True
        
    def stop(self):
        """Arrete la capture"""
        self.running = False
        if self.cap:
            self.cap.release()
            
    def _capture_loop(self):
        """Boucle de capture et detection"""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue
                
            # Detection YOLO
            results = self.model(frame, conf=0.25, imgsz=320, verbose=False)
            
            # Collecter toutes les detections par type
            livre_detections = {}
            visage_detections = {}
            detected = []
            
            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    
                    detected.append(f"{CLASS_NAMES.get(cls_id, '?')}: {conf:.0%}")
                    
                    # Livre (1=droite, 2=milieu, 3=gauche)
                    if cls_id in [1, 2, 3]:
                        if cls_id not in livre_detections or conf > livre_detections[cls_id]:
                            livre_detections[cls_id] = conf
                            
                    # Visage (0=serieux, 4=sourire)
                    if cls_id in [0, 4]:
                        if cls_id not in visage_detections or conf > visage_detections[cls_id]:
                            visage_detections[cls_id] = conf
            
            # Determiner la direction
            direction = "MILIEU"
            max_livre_conf = 0.0
            
            for cls_id, conf in livre_detections.items():
                if conf > max_livre_conf:
                    max_livre_conf = conf
                    if cls_id == 1:  # livre_droite
                        direction = "DROITE"
                    elif cls_id == 3:  # livre_gauche
                        direction = "GAUCHE"
                    elif cls_id == 2:  # livre_milieu
                        direction = "MILIEU"
            
            # INVERSION des controles X (camera miroir)
            if self.invert_x:
                if direction == "DROITE":
                    direction = "GAUCHE"
                elif direction == "GAUCHE":
                    direction = "DROITE"
            
            # Determiner l'action - STOP par defaut
            action = "STOP"
            max_visage_conf = 0.0
            
            if 4 in visage_detections:
                sourire_conf = visage_detections[4]
                serieux_conf = visage_detections.get(0, 0)
                
                if sourire_conf > serieux_conf:
                    action = "ACCELERER"
                    max_visage_conf = sourire_conf
                else:
                    action = "STOP"
                    max_visage_conf = serieux_conf
            elif 0 in visage_detections:
                action = "STOP"
                max_visage_conf = visage_detections[0]
            
            with self.lock:
                self.current_direction = direction
                self.current_action = action
                self.confidence = max(max_livre_conf, max_visage_conf)
                self.frame = frame
                self.detections = detected
                
    def get_state(self):
        """Retourne l'etat actuel"""
        with self.lock:
            return self.current_direction, self.current_action, self.confidence, self.detections
            
    def get_frame(self):
        """Retourne le dernier frame (en miroir pour affichage)"""
        with self.lock:
            if self.frame is not None:
                # Flip horizontal pour que l'utilisateur se voie en miroir
                return cv2.flip(self.frame.copy(), 1)
            return None


def find_latest_model():
    """Trouve le dernier modele entraine"""
    runs_path = Path(__file__).parent.parent / "training" / "runs" / "detect"
    if not runs_path.exists():
        runs_path = Path("/Users/leod/Documents/Dev/NewDriver/training/runs/detect")
    
    if runs_path.exists():
        train_dirs = sorted(
            [d for d in runs_path.iterdir() if d.is_dir() and d.name.startswith('train')],
            key=lambda x: x.stat().st_mtime, reverse=True
        )
        for train_dir in train_dirs:
            best_path = train_dir / "weights" / "best.pt"
            if best_path.exists():
                return best_path
            last_path = train_dir / "weights" / "last.pt"
            if last_path.exists():
                return last_path
    
    # Fallback: chercher dans scripts/runs
    scripts_runs = Path("/Users/leod/Documents/Dev/NewDriver/scripts/runs/detect")
    if scripts_runs.exists():
        train_dirs = sorted(
            [d for d in scripts_runs.iterdir() if d.is_dir() and d.name.startswith('train')],
            key=lambda x: x.stat().st_mtime, reverse=True
        )
        for train_dir in train_dirs:
            best_path = train_dir / "weights" / "best.pt"
            if best_path.exists():
                return best_path
            last_path = train_dir / "weights" / "last.pt"
            if last_path.exists():
                return last_path
                
    return None
