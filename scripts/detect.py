#!/usr/bin/env python3
"""
Simple detection script to test the YOLO model
"""

from pathlib import Path
from ultralytics import YOLO
import cv2


def find_model():
    """Find the latest trained model"""
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
    return None


def main():
    model_path = find_model()
    if not model_path:
        print("No model found!")
        return
        
    print(f"Model: {model_path}")
    model = YOLO(str(model_path))
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Webcam error")
        return
        
    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        results = model(frame, conf=0.3, verbose=False)
        annotated = results[0].plot()
        
        cv2.imshow("Detection", annotated)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
