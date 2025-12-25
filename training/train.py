from ultralytics import YOLO
import os

current_script_path = os.path.abspath(__file__)
scripts_dir = os.path.dirname(current_script_path)
project_root = os.path.dirname(scripts_dir)
yaml_path = os.path.join(project_root, "Dataset", "YOLO_Ready", "data.yaml")

save_dir = os.path.join(scripts_dir, "runs", "detect")

if __name__ == '__main__':
    model = YOLO('yolov8n.pt')
    
    model.train(data=yaml_path, epochs=50, imgsz=640, device='mps', project=save_dir, name='train')