#!/usr/bin/env python3
"""
YOLO training script for NewDriver
"""

from ultralytics import YOLO
from pathlib import Path


def main():
    yaml_path = "/Users/leod/Documents/Dev/NewDriver/Dataset/YOLO_Ready/data.yaml"
    save_dir = Path("/Users/leod/Documents/Dev/NewDriver/training/runs/detect")
    save_dir.mkdir(parents=True, exist_ok=True)
    
    model = YOLO('yolov8n.pt')
    
    model.train(
        data=yaml_path, 
        epochs=50, 
        imgsz=640, 
        device='mps',
        project=str(save_dir), 
        name='train'
    )


if __name__ == "__main__":
    main()
