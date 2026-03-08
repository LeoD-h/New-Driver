#!/usr/bin/env python3
"""
Organizer - Builds the YOLO_Ready dataset from labelledImg and png folders
"""

import os
import shutil
import random
from pathlib import Path


def main():
    base_path = Path("/Users/leod/Documents/Dev/NewDriver/Dataset")
    labelled_img_path = base_path / "labelledImg"
    png_path = base_path / "png"
    output_path = base_path / "YOLO_Ready"
    
    # Create output directories
    train_images = output_path / "train" / "images"
    train_labels = output_path / "train" / "labels"
    val_images = output_path / "val" / "images"
    val_labels = output_path / "val" / "labels"
    
    for folder in [train_images, train_labels, val_images, val_labels]:
        folder.mkdir(parents=True, exist_ok=True)
    
    val_ratio = 0.2
    
    # YOLO class names (French labels kept as identifiers)
    classes = [
        'visage_serieux',    # serious face
        'livre_droite',      # book right
        'livre_milieu',      # book center
        'livre_gauche',      # book left
        'visage_sourire'     # smiling face
    ]
    
    # List and shuffle label files
    label_files = list(labelled_img_path.glob("*.txt"))
    random.shuffle(label_files)
    
    # Train/val split
    val_count = int(len(label_files) * val_ratio)
    val_files = label_files[:val_count]
    train_files = label_files[val_count:]
    
    print(f"Total: {len(label_files)} files")
    print(f"Train: {len(train_files)}, Val: {len(val_files)}")
    
    def copy_pair(label_file, img_dest, label_dest):
        """Copy an image/label pair to the destination"""
        stem = label_file.stem
        
        for ext in ['.png', '.jpg', '.jpeg']:
            img_file = png_path / f"{stem}{ext}"
            if img_file.exists():
                shutil.copy(img_file, img_dest / img_file.name)
                shutil.copy(label_file, label_dest / label_file.name)
                return True
                
        for ext in ['.png', '.jpg', '.jpeg']:
            img_file = labelled_img_path / f"{stem}{ext}"
            if img_file.exists():
                shutil.copy(img_file, img_dest / img_file.name)
                shutil.copy(label_file, label_dest / label_file.name)
                return True
                
        print(f"Image not found for: {stem}")
        return False
    
    # Copy files to train and val
    train_copied = 0
    for lf in train_files:
        if copy_pair(lf, train_images, train_labels):
            train_copied += 1
            
    val_copied = 0
    for lf in val_files:
        if copy_pair(lf, val_images, val_labels):
            val_copied += 1
    
    print(f"\nCopied:")
    print(f"Train: {train_copied}")
    print(f"Val: {val_copied}")
    
    # Create data.yaml for YOLO training
    yaml_content = f"""path: {output_path}
train: train/images
val: val/images

nc: {len(classes)}
names: {classes}
"""
    
    with open(output_path / "data.yaml", 'w') as f:
        f.write(yaml_content)
    
    print(f"\ndata.yaml created: {output_path / 'data.yaml'}")
    print("YOLO_Ready dataset is ready!")


if __name__ == "__main__":
    main()
