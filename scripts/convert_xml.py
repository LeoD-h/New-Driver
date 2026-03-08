#!/usr/bin/env python3
"""
Convert XML labels to YOLO format
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import os

# YOLO class names (French labels kept as identifiers)
CLASSES = [
    'visage_serieux',    # serious face
    'livre_droite',      # book right
    'livre_milieu',      # book center
    'livre_gauche',      # book left
    'visage_sourire'     # smiling face
]


def convert_xml_to_yolo(xml_path, output_dir):
    """Convert a single XML annotation file to YOLO format"""
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
            
            # Convert to YOLO format (center_x, center_y, width, height)
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
        print(f"Converted: {xml_file.name}")


if __name__ == "__main__":
    main()
