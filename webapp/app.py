#!/usr/bin/env python3
"""
NewDriver Web - Interface Flask avec detection YOLO + Eye Tracking
"""

from flask import Flask, render_template, Response, jsonify, request
import cv2
import threading
import time
import numpy as np
from pathlib import Path

try:
    from ultralytics import YOLO
except ImportError:
    print("pip install ultralytics flask")
    exit(1)

app = Flask(__name__)

# Configuration
CLASS_NAMES = {
    0: "visage_serieux",
    1: "livre_droite", 
    2: "livre_milieu",
    3: "livre_gauche",
    4: "visage_sourire"
}


class EyeTracker:
    """Detecteur de regard base sur OpenCV (sans MediaPipe)"""
    
    def __init__(self):
        # Charger le detecteur de visage et yeux d'OpenCV
        cv2_path = cv2.data.haarcascades
        self.face_cascade = cv2.CascadeClassifier(cv2_path + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2_path + 'haarcascade_eye.xml')
        
    def analyze(self, frame):
        """Analyse le regard"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return "NO_FACE", 0.5, False
        
        # Prendre le premier visage
        x, y, w, h = faces[0]
        roi_gray = gray[y:y+h, x:x+w]
        
        # Detecter les yeux
        eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
        
        if len(eyes) < 2:
            # Moins de 2 yeux detectes = yeux fermes ou regarde ailleurs
            return "DETOURNE", 0.5, False
        
        # Calculer la position moyenne des yeux
        eye_centers = []
        for (ex, ey, ew, eh) in eyes[:2]:
            eye_center_x = ex + ew // 2
            eye_centers.append(eye_center_x)
        
        # Position moyenne relative au visage
        avg_eye_x = sum(eye_centers) / len(eye_centers)
        ratio = avg_eye_x / w
        
        # Determiner la direction
        if ratio < 0.35:
            direction = "GAUCHE"
            looking = False
        elif ratio > 0.65:
            direction = "DROITE"
            looking = False
        else:
            direction = "CENTRE"
            looking = True
        
        return direction, ratio, True


class GameState:
    def __init__(self):
        self.model = None
        self.cap = None
        self.running = False
        self.direction = "MILIEU"
        self.action = "STOP"
        self.speed = 0
        self.score = 0
        self.car_x = 50
        self.detections = []
        self.fps = 0
        self.game_active = False
        self.lock = threading.Lock()
        
        # Eye tracking
        self.looking_at_screen = True
        self.eye_direction = "CENTRE"
        self.gaze_ratio = 0.5
        self.eyes_open = True
        self.last_frame = None
        
        # Eye tracker
        self.eye_tracker = EyeTracker()

state = GameState()


def find_model():
    paths = [
        Path("/Users/leod/Documents/Dev/NewDriver/training/runs/detect"),
        Path("/Users/leod/Documents/Dev/NewDriver/scripts/runs/detect")
    ]
    for runs_path in paths:
        if runs_path.exists():
            train_dirs = sorted(
                [d for d in runs_path.iterdir() if d.is_dir() and d.name.startswith('train')],
                key=lambda x: x.stat().st_mtime, reverse=True
            )
            for train_dir in train_dirs:
                best = train_dir / "weights" / "best.pt"
                if best.exists():
                    return best
    return None


def load_model():
    model_path = find_model()
    if model_path:
        state.model = YOLO(str(model_path))
        print(f"Modele charge: {model_path}")
        return True
    return False


def detection_loop():
    state.cap = cv2.VideoCapture(0)
    state.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    state.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    state.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    fps_counter = 0
    last_fps_time = time.time()
    
    while state.running:
        ret, frame = state.cap.read()
        if not ret:
            continue
        
        # Flip pour miroir
        frame = cv2.flip(frame, 1)
        state.last_frame = frame.copy()
            
        fps_counter += 1
        if time.time() - last_fps_time >= 1.0:
            state.fps = fps_counter
            fps_counter = 0
            last_fps_time = time.time()
        
        # Detection YOLO
        results = state.model(frame, conf=0.25, imgsz=320, verbose=False)
        
        # Analyse du regard
        eye_dir, gaze_ratio, eyes_open = state.eye_tracker.analyze(frame)
        
        # Analyser les resultats YOLO
        livre_det = {}
        visage_det = {}
        detections = []
        
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                detections.append({"class": CLASS_NAMES.get(cls_id, "?"), "conf": conf})
                
                if cls_id in [1, 2, 3]:
                    if cls_id not in livre_det or conf > livre_det[cls_id]:
                        livre_det[cls_id] = conf
                if cls_id in [0, 4]:
                    if cls_id not in visage_det or conf > visage_det[cls_id]:
                        visage_det[cls_id] = conf
        
        # Direction basee sur le livre (CONTROLES INVERSES)
        direction = "MILIEU"
        max_conf = 0
        for cls_id, conf in livre_det.items():
            if conf > max_conf:
                max_conf = conf
                if cls_id == 1:  # livre_droite -> voiture DROITE
                    direction = "DROITE"
                elif cls_id == 3:  # livre_gauche -> voiture GAUCHE
                    direction = "GAUCHE"
                elif cls_id == 2:
                    direction = "MILIEU"
        
        # Action basee sur le visage ET le regard
        action = "STOP"
        looking_at_screen = (eye_dir == "CENTRE") and eyes_open
        
        if looking_at_screen:
            if 4 in visage_det:
                if visage_det[4] > visage_det.get(0, 0):
                    action = "ACCELERER"
        
        with state.lock:
            state.direction = direction
            state.action = action
            state.detections = detections
            state.looking_at_screen = looking_at_screen
            state.eye_direction = eye_dir
            state.gaze_ratio = gaze_ratio
            state.eyes_open = eyes_open
            
            if state.game_active:
                if action == "ACCELERER":
                    state.speed = min(state.speed + 2, 100)
                else:
                    state.speed = max(state.speed - 1, 0)
                
                target = 50
                if direction == "GAUCHE":
                    target = 15
                elif direction == "DROITE":
                    target = 85
                state.car_x += (target - state.car_x) * 0.05
                
                state.score += int(state.speed / 20)
    
    state.cap.release()


def generate_frames():
    while state.running:
        if state.last_frame is None:
            continue
        
        frame = state.last_frame.copy()
        
        # Detection YOLO
        if state.model:
            results = state.model(frame, conf=0.25, imgsz=320, verbose=False)
            frame = results[0].plot()
        
        # Ajouter indicateur de regard
        with state.lock:
            color = (0, 255, 0) if state.looking_at_screen else (0, 0, 255)
            text = f"Regard: {state.eye_direction}"
            cv2.putText(frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            
            eyes_text = "Yeux: OUVERTS" if state.eyes_open else "Yeux: FERMES"
            cv2.putText(frame, eyes_text, (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/start', methods=['POST'])
def start():
    if not state.running:
        if load_model():
            state.running = True
            state.game_active = True
            state.score = 0
            state.speed = 0
            state.car_x = 50
            threading.Thread(target=detection_loop, daemon=True).start()
            return jsonify({"status": "started"})
        return jsonify({"status": "error", "message": "Modele non trouve"})
    return jsonify({"status": "already running"})


@app.route('/stop', methods=['POST'])
def stop():
    state.running = False
    state.game_active = False
    return jsonify({"status": "stopped"})


@app.route('/state')
def get_state():
    with state.lock:
        return jsonify({
            "direction": state.direction,
            "action": state.action,
            "speed": state.speed,
            "score": state.score,
            "car_x": state.car_x,
            "fps": state.fps,
            "detections": state.detections,
            "game_active": state.game_active,
            "looking_at_screen": state.looking_at_screen,
            "eye_direction": state.eye_direction,
            "eyes_open": state.eyes_open,
            "gaze_ratio": state.gaze_ratio
        })


if __name__ == '__main__':
    print("NewDriver Web - http://localhost:8080")
    print("Features: YOLO + Eye Tracking")
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
