# NewDriver

A car game controlled by head position and facial expression using YOLO object detection and eye tracking.

The player holds a book in front of the camera. The position of the book (left, center, right) controls the steering direction. Smiling accelerates the car, while a serious face brakes. Eye tracking detects whether the player is looking at the screen and if their eyes are open.


## Getting Started

```bash
cd webapp
python app.py
# Open http://localhost:8080
```


## YOLO Classes

| ID | Name             | Translation   | Action     |
|----|------------------|---------------|------------|
| 0  | visage_serieux   | serious face  | Brake      |
| 1  | livre_droite     | book right    | Turn right |
| 2  | livre_milieu     | book center   | Go straight|
| 3  | livre_gauche     | book left     | Turn left  |
| 4  | visage_sourire   | smiling face  | Accelerate |


## Eye Tracking

- Looking at the screen: the player can accelerate.
- Looking away: the car brakes automatically.
- Eyes closed: drowsiness detection.


## Controls

| Action      | Input              |
|-------------|--------------------:|
| Steering    | Book position      |
| Accelerate  | Smile              |
| Brake       | Serious face       |
| Test mode   | T key              |


## More Info

For more information, visit [leoduquenne.fr](https://leoduquenne.fr/)
