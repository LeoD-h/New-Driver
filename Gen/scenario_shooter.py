import cv2
import os
import time

CAMERA_INDEX = 0
PHOTOS_PAR_SCENARIO = 15
COMPTE_A_REBOURS = 2

SCENARIOS = [
    # "Sourire_Livre_Gauche",
    # "Sourire_Livre_Droite",
    # "Sourire_Livre_Milieu",
    # "Serieux_Livre_Droite",
    # "Serieux_Livre_Gauche",
    # "Serieux_Livre_Milieu"
    "vide"
]

base_dir = os.path.dirname(os.path.abspath(__file__))
root_save_folder = os.path.join(base_dir, "Collections")

if not os.path.exists(root_save_folder):
    os.makedirs(root_save_folder)

print("START SHOOTING")
print(f"Folder: {root_save_folder}")

cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(3, 640)
cap.set(4, 480)

if not cap.isOpened():
    print("Error: Camera not found")
    exit()

font = cv2.FONT_HERSHEY_SIMPLEX

for scenario in SCENARIOS:
    scenario_folder = os.path.join(root_save_folder, scenario)
    if not os.path.exists(scenario_folder):
        os.makedirs(scenario_folder)
    
    waiting = True
    while waiting:
        ret, frame = cap.read()
        if not ret: break

        cv2.rectangle(frame, (0, 0), (640, 80), (0, 0, 0), -1)
        cv2.putText(frame, f"SCENARIO : {scenario}", (10, 30), font, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, "PRESS SPACE TO START", (10, 60), font, 0.6, (255, 255, 255), 1)
        
        cv2.imshow("Scenario Shooter", frame)
        
        key = cv2.waitKey(1)
        if key == 32:
            waiting = False
        elif key == ord('q'):
            exit()

    print(f"-> Start: {scenario}")
    photos_taken = 0
    start_time = time.time()
    
    while photos_taken < PHOTOS_PAR_SCENARIO:
        ret, frame = cap.read()
        if not ret: break
        
        elapsed = time.time() - start_time
        remaining = COMPTE_A_REBOURS - elapsed

        if remaining > 0:
            center_x = 320
            center_y = 240
            cv2.putText(frame, f"{int(remaining)+1}", (center_x, center_y), font, 4, (0, 255, 255), 4)
            cv2.putText(frame, f"Pose: {scenario}", (10, 450), font, 0.7, (200, 200, 200), 2)
        else:
            timestamp = int(time.time() * 1000)
            filename = f"{scenario}_{timestamp}.jpg"
            save_path = os.path.join(scenario_folder, filename)
            
            clean_ret, clean_frame = cap.read()
            if clean_ret:
                cv2.imwrite(save_path, clean_frame)
                
                cv2.rectangle(frame, (0,0), (640,480), (255,255,255), -1)
                cv2.imshow("Scenario Shooter", frame)
                cv2.waitKey(50)
                
                os.system("afplay /System/Library/Sounds/Tink.aiff")
                
                photos_taken += 1
                print(f"   [{photos_taken}/{PHOTOS_PAR_SCENARIO}] {filename}")
                start_time = time.time()
                continue

        cv2.imshow("Scenario Shooter", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()

cap.release()
cv2.destroyAllWindows()