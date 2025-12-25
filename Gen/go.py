import os
import shutil
import subprocess
import sys

def run():
    source_dir = "Collections"
    dest_dir = "img"
    script_path = os.path.join("..", "scripts", "empty.py")

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dest_dir, file)
                shutil.move(src_file, dst_file)

    if os.path.exists(script_path):
        subprocess.run([sys.executable, script_path])
    else:
        print(f"Le fichier {script_path} est introuvable.")

if __name__ == "__main__":
    run()