#!/usr/bin/env python3
"""
Interface de test pour le modele YOLO - Detection en temps réel
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time
import os
from pathlib import Path

try:
    from ultralytics import YOLO
except ImportError:
    print("Erreur: ultralytics n'est pas installe. Installez-le avec: pip install ultralytics")
    exit(1)


class YOLOTestInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("NewDriver - Test Interface YOLO")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        
        # Variables
        self.model = None
        self.cap = None
        self.running = False
        self.current_frame = None
        
        # Performance settings
        self.inference_size = 320
        self.frame_count = 0
        self.fps = 0
        self.last_fps_time = 0
        self.fps_counter = 0
        
        # Chemins
        self.base_path = Path("/Users/leod/Documents/Dev/NewDriver")
        self.runs_path = self.base_path / "training" / "runs" / "detect"
        
        self.setup_ui()
        self.find_latest_model()
        
    def setup_ui(self):
        """Configure l'interface"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 11), padding=10)
        style.configure('TLabel', font=('Helvetica', 11), background='#1a1a2e', foreground='white')
        style.configure('Header.TLabel', font=('Helvetica', 18, 'bold'), background='#1a1a2e', foreground='#00d4ff')
        
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        header = ttk.Label(main_frame, text="NewDriver - Test du Modele YOLO", style='Header.TLabel')
        header.pack(pady=(0, 20))
        
        # Controles
        control_frame = tk.Frame(main_frame, bg='#16213e', relief='raised', bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        btn_frame = tk.Frame(control_frame, bg='#16213e')
        btn_frame.pack(pady=15, padx=15)
        
        self.btn_load = tk.Button(btn_frame, text="Charger Modele", command=self.load_model,
                                   bg='#0f3460', fg='white', font=('Helvetica', 11, 'bold'),
                                   relief='flat', padx=15, pady=8)
        self.btn_load.pack(side=tk.LEFT, padx=5)
        
        self.btn_webcam = tk.Button(btn_frame, text="Demarrer Webcam", command=self.toggle_webcam,
                                     bg='#00b894', fg='white', font=('Helvetica', 11, 'bold'),
                                     relief='flat', padx=15, pady=8)
        self.btn_webcam.pack(side=tk.LEFT, padx=5)
        
        self.btn_image = tk.Button(btn_frame, text="Tester Image", command=self.test_image,
                                    bg='#6c5ce7', fg='white', font=('Helvetica', 11, 'bold'),
                                    relief='flat', padx=15, pady=8)
        self.btn_image.pack(side=tk.LEFT, padx=5)
        
        # Slider confiance
        conf_frame = tk.Frame(control_frame, bg='#16213e')
        conf_frame.pack(pady=(0, 15), padx=15, fill=tk.X)
        
        ttk.Label(conf_frame, text="Seuil de confiance:").pack(side=tk.LEFT)
        self.conf_var = tk.DoubleVar(value=0.5)
        self.conf_slider = ttk.Scale(conf_frame, from_=0.1, to=1.0, variable=self.conf_var,
                                      orient=tk.HORIZONTAL, length=200)
        self.conf_slider.pack(side=tk.LEFT, padx=10)
        self.conf_label = ttk.Label(conf_frame, text="0.50")
        self.conf_label.pack(side=tk.LEFT)
        self.conf_slider.bind('<Motion>', self.update_conf_label)
        
        # Video
        video_frame = tk.Frame(main_frame, bg='#0f3460', relief='sunken', bd=3)
        video_frame.pack(fill=tk.BOTH, expand=True)
        
        self.video_label = tk.Label(video_frame, bg='#0f3460')
        self.video_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.show_placeholder()
        
        # Status
        status_frame = tk.Frame(main_frame, bg='#16213e', relief='sunken', bd=1)
        status_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.status_var = tk.StringVar(value="En attente du chargement du modele...")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.pack(pady=8)
        
        # Detections
        self.detection_frame = tk.Frame(main_frame, bg='#16213e', relief='raised', bd=2)
        self.detection_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(self.detection_frame, text="Dernieres detections:", 
                  font=('Helvetica', 12, 'bold')).pack(anchor='w', padx=10, pady=5)
        
        self.detection_text = tk.Text(self.detection_frame, height=3, bg='#0f3460', fg='#00ff88',
                                       font=('Courier', 10), relief='flat')
        self.detection_text.pack(fill=tk.X, padx=10, pady=(0, 10))
        
    def show_placeholder(self):
        placeholder = Image.new('RGB', (800, 500), color='#0f3460')
        photo = ImageTk.PhotoImage(placeholder)
        self.video_label.configure(image=photo)
        self.video_label.image = photo
        
    def update_conf_label(self, event=None):
        self.conf_label.configure(text=f"{self.conf_var.get():.2f}")
        
    def find_latest_model(self):
        if self.runs_path.exists():
            train_dirs = sorted([d for d in self.runs_path.iterdir() if d.is_dir() and d.name.startswith('train')],
                               key=lambda x: x.stat().st_mtime, reverse=True)
            for train_dir in train_dirs:
                best_path = train_dir / "weights" / "best.pt"
                last_path = train_dir / "weights" / "last.pt"
                if best_path.exists():
                    self.status_var.set(f"Modele trouve: {best_path.name} dans {train_dir.name}")
                    self.latest_model_path = best_path
                    return
                elif last_path.exists():
                    self.status_var.set(f"Modele trouve: {last_path.name} dans {train_dir.name}")
                    self.latest_model_path = last_path
                    return
        self.latest_model_path = None
        self.status_var.set("Aucun modele trouve. L'entrainement est-il termine?")
        
    def load_model(self):
        self.find_latest_model()
        
        if self.latest_model_path and self.latest_model_path.exists():
            response = messagebox.askyesno("Charger modele", 
                f"Charger le dernier modele?\n\n{self.latest_model_path}")
            if response:
                self._load_model_file(self.latest_model_path)
                return
        
        filepath = filedialog.askopenfilename(
            title="Selectionner un modele YOLO",
            initialdir=str(self.runs_path),
            filetypes=[("Modele PyTorch", "*.pt"), ("Tous les fichiers", "*.*")]
        )
        if filepath:
            self._load_model_file(Path(filepath))
            
    def _load_model_file(self, path):
        try:
            self.status_var.set(f"Chargement du modele: {path.name}...")
            self.root.update()
            self.model = YOLO(str(path))
            self.status_var.set(f"Modele charge: {path.name}")
            messagebox.showinfo("Succes", f"Modele charge avec succes!\n{path.name}")
        except Exception as e:
            self.status_var.set(f"Erreur: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible de charger le modele:\n{str(e)}")
            
    def toggle_webcam(self):
        if self.running:
            self.stop_webcam()
        else:
            self.start_webcam()
            
    def start_webcam(self):
        if self.model is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger un modele!")
            return
            
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Impossible d'ouvrir la webcam")
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                
            self.running = True
            self.frame_count = 0
            self.last_fps_time = time.time()
            self.fps_counter = 0
            
            self.btn_webcam.configure(text="Arreter Webcam", bg='#e74c3c')
            self.status_var.set("Webcam active - Detection en cours...")
            
            self.webcam_thread = threading.Thread(target=self.webcam_loop, daemon=True)
            self.webcam_thread.start()
            
        except Exception as e:
            self.status_var.set(f"Erreur webcam: {str(e)}")
            messagebox.showerror("Erreur", f"Erreur webcam:\n{str(e)}")
            
    def stop_webcam(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.btn_webcam.configure(text="Demarrer Webcam", bg='#00b894')
        self.status_var.set("Webcam arretee")
        self.show_placeholder()
        
    def webcam_loop(self):
        target_fps = 30
        frame_time = 1.0 / target_fps
        last_display_time = 0
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            self.current_frame = frame.copy()
            self.frame_count += 1
            self.fps_counter += 1
            
            current_time = time.time()
            if current_time - self.last_fps_time >= 1.0:
                self.fps = self.fps_counter
                self.fps_counter = 0
                self.last_fps_time = current_time
            
            # Detection
            results = self.model(frame, conf=self.conf_var.get(), 
                                imgsz=self.inference_size, verbose=False)
            
            if current_time - last_display_time >= frame_time:
                last_display_time = current_time
                
                self.update_detections(results[0])
                annotated_frame = results[0].plot()
                
                cv2.putText(annotated_frame, f"FPS: {self.fps}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                h, w = annotated_frame.shape[:2]
                scale = min(900 / w, 550 / h)
                new_w, new_h = int(w * scale), int(h * scale)
                annotated_frame = cv2.resize(annotated_frame, (new_w, new_h), 
                                            interpolation=cv2.INTER_LINEAR)
                
                frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                photo = ImageTk.PhotoImage(img)
                
                self.video_label.configure(image=photo)
                self.video_label.image = photo
            
    def update_detections(self, result):
        names = result.names
        boxes = result.boxes
        
        if len(boxes) > 0:
            detections = []
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                name = names[cls_id]
                detections.append(f"{name}: {conf:.2%}")
            
            text = " | ".join(detections)
            self.detection_text.delete(1.0, tk.END)
            self.detection_text.insert(tk.END, text)
        else:
            self.detection_text.delete(1.0, tk.END)
            self.detection_text.insert(tk.END, "Aucune detection...")
            
    def test_image(self):
        if self.model is None:
            messagebox.showwarning("Attention", "Veuillez d'abord charger un modele!")
            return
            
        filepath = filedialog.askopenfilename(
            title="Selectionner une image",
            initialdir=str(self.base_path / "Dataset"),
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp"), ("Tous les fichiers", "*.*")]
        )
        
        if filepath:
            try:
                self.stop_webcam()
                
                results = self.model(filepath, conf=self.conf_var.get())
                annotated = results[0].plot()
                
                frame_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                
                w, h = img.size
                scale = min(900 / w, 550 / h)
                new_size = (int(w * scale), int(h * scale))
                img = img.resize(new_size, Image.Resampling.BILINEAR)
                
                photo = ImageTk.PhotoImage(img)
                self.video_label.configure(image=photo)
                self.video_label.image = photo
                
                self.update_detections(results[0])
                self.status_var.set(f"Image analysee: {Path(filepath).name}")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'analyse:\n{str(e)}")
            
    def on_closing(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = YOLOTestInterface(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
