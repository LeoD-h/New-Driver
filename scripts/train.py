#!/usr/bin/env python3
"""
Script d'entrainement YOLO pour NewDriver
"""

from ultralytics import YOLO
from pathlib import Path


def main():
    # Chemins
    yaml_path = "/Users/leod/Documents/Dev/NewDriver/Dataset/YOLO_Ready/data.yaml"
    save_dir = Path("/Users/leod/Documents/Dev/NewDriver/training/runs/detect")
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Charger le modele de base
    model = YOLO('yolov8n.pt')
    
    # Entrainer
    model.train(
        data=yaml_path, 
        epochs=50, 
        imgsz=640, 
        device='mps',  # Apple Silicon
        project=str(save_dir), 
        name='train'
    )


if __name__ == "__main__":
    main()
