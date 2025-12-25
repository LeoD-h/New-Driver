#!/usr/bin/env python3
"""
Script de conversion des labels XML vers format YOLO
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import os

# Classes
CLASSES = ['visage_serieux', 'livre_droite', 'livre_milieu', 'livre_gauche', 'visage_sourire']


def convert_xml_to_yolo(xml_path, output_dir):
    """Convertit un fichier XML en format YOLO"""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    size = root.find('size')
    img_width = int(size.find('width').text)
    img_height = int(size.find('height').text)
    
    output_path = Path(output_dir) / (Path(xml_path).stem + '.txt')
    
    with open(output_path, 'w') as f:
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            if class_name not in CLASSES:
                continue
                
            class_id = CLASSES.index(class_name)
            bbox = obj.find('bndbox')
            
            xmin = float(bbox.find('xmin').text)
            ymin = float(bbox.find('ymin').text)
            xmax = float(bbox.find('xmax').text)
            ymax = float(bbox.find('ymax').text)
            
            # Convertir en format YOLO (centre x, centre y, largeur, hauteur)
            x_center = (xmin + xmax) / 2 / img_width
            y_center = (ymin + ymax) / 2 / img_height
            width = (xmax - xmin) / img_width
            height = (ymax - ymin) / img_height
            
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")


def main():
    xml_dir = Path("/Users/leod/Documents/Dev/NewDriver/Dataset/labelledImg")
    output_dir = Path("/Users/leod/Documents/Dev/NewDriver/Dataset/YOLO_Ready/train/labels")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for xml_file in xml_dir.glob("*.xml"):
        convert_xml_to_yolo(xml_file, output_dir)
        print(f"Converti: {xml_file.name}")


if __name__ == "__main__":
    main()
