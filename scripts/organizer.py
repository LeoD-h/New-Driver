#!/usr/bin/env python3
"""
Organizer - Cree le dataset YOLO_Ready a partir de labelledImg et png
"""

import os
import shutil
import random
from pathlib import Path


def main():
    # Chemins
    base_path = Path("/Users/leod/Documents/Dev/NewDriver/Dataset")
    labelled_img_path = base_path / "labelledImg"
    png_path = base_path / "png"
    output_path = base_path / "YOLO_Ready"
    
    # Creer les repertoires
    train_images = output_path / "train" / "images"
    train_labels = output_path / "train" / "labels"
    val_images = output_path / "val" / "images"
    val_labels = output_path / "val" / "labels"
    
    for folder in [train_images, train_labels, val_images, val_labels]:
        folder.mkdir(parents=True, exist_ok=True)
    
    # Ratio train/val
    val_ratio = 0.2
    
    # Classes
    classes = ['visage_serieux', 'livre_droite', 'livre_milieu', 'livre_gauche', 'visage_sourire']
    
    # Lister les fichiers labels
    label_files = list(labelled_img_path.glob("*.txt"))
    random.shuffle(label_files)
    
    # Split
    val_count = int(len(label_files) * val_ratio)
    val_files = label_files[:val_count]
    train_files = label_files[val_count:]
    
    print(f"Total: {len(label_files)} fichiers")
    print(f"Train: {len(train_files)}, Val: {len(val_files)}")
    
    def copy_pair(label_file, img_dest, label_dest):
        """Copie une paire image/label"""
        # Chercher l'image correspondante
        stem = label_file.stem
        
        # Chercher dans png/
        for ext in ['.png', '.jpg', '.jpeg']:
            img_file = png_path / f"{stem}{ext}"
            if img_file.exists():
                shutil.copy(img_file, img_dest / img_file.name)
                shutil.copy(label_file, label_dest / label_file.name)
                return True
                
        # Chercher dans labelledImg/
        for ext in ['.png', '.jpg', '.jpeg']:
            img_file = labelled_img_path / f"{stem}{ext}"
            if img_file.exists():
                shutil.copy(img_file, img_dest / img_file.name)
                shutil.copy(label_file, label_dest / label_file.name)
                return True
                
        print(f"Image non trouvee pour: {stem}")
        return False
    
    # Copier les fichiers
    train_copied = 0
    for lf in train_files:
        if copy_pair(lf, train_images, train_labels):
            train_copied += 1
            
    val_copied = 0
    for lf in val_files:
        if copy_pair(lf, val_images, val_labels):
            val_copied += 1
    
    print(f"\nCopies effectuees:")
    print(f"Train: {train_copied}")
    print(f"Val: {val_copied}")
    
    # Creer data.yaml
    yaml_content = f"""path: {output_path}
train: train/images
val: val/images

nc: {len(classes)}
names: {classes}
"""
    
    with open(output_path / "data.yaml", 'w') as f:
        f.write(yaml_content)
    
    print(f"\ndata.yaml cree: {output_path / 'data.yaml'}")
    print("\nDataset YOLO_Ready pret!")


if __name__ == "__main__":
    main()
