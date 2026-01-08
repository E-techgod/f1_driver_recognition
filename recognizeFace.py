import os
from pathlib import Path
import cv2
import csv 
import time
import pickle
import pyttsx3
import requests
import threading
import numpy as np
import mediapipe as mp
from datetime import datetime
from driverInfo import driver_info
from sklearn.neighbors import KNeighborsClassifier


ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
ATTENDANCE_DIR = ROOT_DIR / "Attendance"

# Load face detection model
faceDetect = cv2.CascadeClassifier(str(DATA_DIR / "haarcascade_frontalface_default.xml"))

# Load data (FACES and LABELS)
with open(DATA_DIR / "listNames.pkl", 'rb') as f: 
    LABELS = pickle.load(f)
with open(DATA_DIR / "listFaces.pkl", 'rb') as f: 
    FACES = pickle.load(f)

# ====== FIX: Ensure equal number of samples ======
min_samples = min(len(FACES), len(LABELS))  # Take the smallest count
FACES = FACES[:min_samples]  # Trim to match
LABELS = LABELS[:min_samples]  # Trim to match
print(f"Training KNN with {len(FACES)} faces and {len(LABELS)} labels")  # Debug check

# Train KNN
Knn = KNeighborsClassifier(n_neighbors=5)
Knn.fit(FACES, LABELS)

COL_NAMES = ['NAME', 'TIME']

# Initialize text-to-speech engine
def speak(text):
    def run():
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()

def send_attendance_to_api(driver_name):
    url = "http://localhost:5006/attendance"  # make sure this matches your server.py
    data = {
        "driver_name": driver_name,
        "timestamp": datetime.now().isoformat()
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"API logged: {driver_name}")
        else:
            print(f"API error: {response.status_code} — {response.text}")
    except Exception as e:
        print(f"API failed for {driver_name}: {e}")

cap = cv2.VideoCapture(1)
mode = "normal"  # Initial mode

# Driver's team logo
logo_dir = DATA_DIR / "logos"
logos = {}  
for file in os.listdir(logo_dir):
    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
        name = os.path.splitext(file)[0]  # "Lando Norris"
        driver_name = name.replace("_", " ")
        path = logo_dir / file
        img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        if img is not None:
            logos[driver_name] = img

# Driver's flag 
flag_dir = DATA_DIR / "flags"
flags= {}
for file in os.listdir(flag_dir):
    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
        name = os.path.splitext(file)[0]  # "Lando Norris"
        driver_name = name.replace("_", " ")
        path = flag_dir / file
        img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        if img is not None:
            flags[driver_name] = img
while True:
    ret, frame = cap.read() 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)

    attendance = None  # Reset for this frame
    
    for (x, y, w, h) in faces:
        cropImage = frame[y:y+h, x:x+w]
        reSizeImage = cv2.resize(cropImage, (50, 50)).flatten().reshape(1, -1)
        output = Knn.predict(reSizeImage)
        name= str(output[0])

        # === Step 1: Draw Transparent Box ===
        overlay = frame.copy()
        box_start = (10, 10)
        box_end = (400, 45)  # Adjust height based on how many info lines
        cv2.rectangle(overlay, box_start, box_end, (0, 0, 0), -1)  # Solid black box

        alpha = 0.6  # Transparency factor
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        ATTENDANCE_DIR.mkdir(parents=True, exist_ok=True)
        attendance_csv = ATTENDANCE_DIR / f"Attendance_{date}.csv"
        exist = os.path.isfile(attendance_csv)
        attendance = [str(output[0]), str(timestamp)]


        cv2.putText(frame, str(output[0]), (x+200, y-20), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2) 
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  

        
        info = driver_info.get(name)
        if info:
             # Step 1: Draw transparent box
            lines = info.strip().split('\n')
    
            # Step 1: Calculate dynamic box height
            line_height = 30
            padding = 20
            header_height = 35
            box_top = 10
            box_bottom = box_top + header_height + len(lines) * line_height + padding

            # Step 2: Draw background box
            overlay = frame.copy()
            box_start = (10, box_top)
            box_end = (400, box_bottom)
            cv2.rectangle(overlay, box_start, box_end, (0, 0, 0), -1)
            frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

            # Step 3: Draw logo
            if name in logos:
                logo = logos[name]
                logo_size = 200
                logo = cv2.resize(logo, (logo_size, logo_size))

                frame_height, frame_width = frame.shape[:2]
                x_offset = frame_width - logo_size - 10
                y_offset = 10

                # Before drawing logo, add a white border behind it (optional glow)
                cv2.rectangle(frame, (x_offset-2, y_offset-2), (x_offset+logo_size+2, y_offset+logo_size+2), (0,0,0), thickness=5)
                
                if logo.shape[2] == 4:  # Has alpha channel
                    alpha = logo[:, :, 3] / 255.0
                    for c in range(3):
                        frame[y_offset:y_offset+logo_size, x_offset:x_offset+logo_size, c] = (
                            alpha * logo[:, :, c] +
                            (1 - alpha) * frame[y_offset:y_offset+logo_size, x_offset:x_offset+logo_size, c]
                        )
                else:
                    frame[y_offset:y_offset+logo_size, x_offset:x_offset+logo_size] = logo

            # === Draw Flag (below logo)
            if name in flags:
                flag = flags[name]
                flag_size = 200
                flag = cv2.resize(flag, (flag_size, flag_size))

                x_flag = frame.shape[1] - logo_size - flag_size - 20  # 10px space between them
                y_flag = 10  # same vertical position as logo

                # Before drawing logo, add a white border behind it (optional glow)
                cv2.rectangle(frame, (x_flag-2, y_flag-2), (x_flag+flag_size+2, y_flag+flag_size+2), (0,0,0), thickness=5)

                if flag.shape[2] == 4:
                    alpha = flag[:, :, 3] / 255.0
                    for c in range(3):
                        frame[y_flag:y_flag+flag_size, x_flag:x_flag+flag_size, c] = (
                            alpha * flag[:, :, c] +
                            (1 - alpha) * frame[y_flag:y_flag+flag_size, x_flag:x_flag+flag_size, c]
                        )
                else:
                    frame[y_flag:y_flag+flag_size, x_flag:x_flag+flag_size] = flag


            # Step 2: Draw text
            cv2.putText(frame, name.upper(), (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            lines = info.strip().split('\n')
            for i, line in enumerate(info.split('\n')):
                y = 65 + i * 30
                cv2.putText(frame, line, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        break  # Only one face per frame

    
    #frame = cv2.flip(frame, 1) Flips the Frame 
    output_image = frame

    # Display mode and instructions
    cv2.putText(output_image, "Press 'a' to send data to API", (1400, 1000), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Maintain list of already marked names (at top of script):
    marked_names = set()

    # After drawing mode instructions:
    y_offset = 50
    for idx, name in enumerate(marked_names):
        cv2.putText(output_image, f"{name} marked present", (20, y_offset + idx * 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("frame", output_image)  
    
    key = cv2.waitKey(1)
    if key == ord('a'):

        #phrase= driver_info.get(attendance[0], f"{attendance[0]} is present")
        #speak("Present")

        csv_path = ATTENDANCE_DIR / f"Attendance_{date}.csv"
        write_header = not os.path.isfile(csv_path) or os.path.getsize(csv_path) == 0

        if exist:
            with open(csv_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(attendance)
                
        else:
            with open(csv_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if write_header:
                    writer.writerow(COL_NAMES)
                    writer.writerow(attendance)
                

        # log to API too
        send_attendance_to_api(attendance[0])  # logs driver name to the API

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



"""
# Initialize Mediapipe Selfie Segmentation
#mp_selfie_segmentation = mp.solutions.selfie_segmentation
#selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# Load background image
#imageBackGround = cv2.imread(str(ROOT_DIR / "formula1.jpg"))


    elif key == ord('b'):
        mode = "blur"
    elif key == ord('i'):
        mode = "image"
    elif key == ord('n'):
        mode = "normal"

    cv2.putText(output_image, f"Mode: {mode.upper()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(output_image, "Press 'o' to log attendance", (1400, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(output_image, "Press 'b' = Blur | 'i' = Image | 'n' = Normal", (1400, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(output_image, "Press 'q' to exit", (1400, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)


if mode == "normal":
        output_image = frame
    else:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = selfie_segmentation.process(rgb)
        mask = results.segmentation_mask > 0.5
        condition = np.stack((mask,) * 3, axis=-1)

        if mode == "blur":
            background = cv2.GaussianBlur(frame, (155, 155), 0)
        elif mode == "image":
            background = cv2.resize(imageBackGround, (frame.shape[1], frame.shape[0]))
        else:
            background = np.zeros_like(frame)

        output_image = np.where(condition, frame, background)
    """
