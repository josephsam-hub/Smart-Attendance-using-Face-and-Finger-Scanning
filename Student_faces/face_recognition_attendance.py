import cv2
import dlib
import numpy as np
import os
from datetime import datetime
import pandas as pd

csv_filename = "attendance.csv"

# STEP 1: Check and create attendance CSV if not exists
print("[STEP 1] Checking CSV file...")
if not os.path.exists(csv_filename):
    df = pd.DataFrame(columns=["Name", "Time"])
    df.to_csv(csv_filename, index=False)
    print("[INFO] attendance.csv created.")
else:
    print("[INFO] attendance.csv already exists.")

# Load Dlib models
print("[STEP 2] Loading Dlib models...")
face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# STEP 3: Load registered faces
def load_registered_faces(dataset_path="face_dataset"):
    print("[STEP 3] Loading registered faces from dataset...")
    names = []
    encodings = []

    for folder in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, folder)
        if os.path.isdir(folder_path):
            for img_file in os.listdir(folder_path):
                img_path = os.path.join(folder_path, img_file)
                img = cv2.imread(img_path)
                if img is None:
                    print(f"[X] Failed to load image: {img_path}")
                    continue

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector(gray)
                if len(faces) > 0:
                    shape = landmark_predictor(gray, faces[0])
                    face_descriptor = face_rec_model.compute_face_descriptor(img, shape)
                    encodings.append(np.array(face_descriptor))
                    names.append(folder)
                    print(f"[✓] Face detected in: {img_file} (Folder: {folder})")
                else:
                    print(f"[X] No face found in: {img_file} (Folder: {folder})")

    print(f"[INFO] Total registered: {len(names)}")
    return names, encodings
# STEP 4: Mark attendance
def mark_attendance(name):
    filename = "attendance.xlsx"
    time_now = datetime.now().strftime("%H:%M:%S")
    date_today = datetime.now().strftime("%Y-%m-%d")
    entry = {"Name": name, "Date": date_today, "Time": time_now}

    if os.path.exists(filename):
        df = pd.read_excel(filename)
    else:
        df = pd.DataFrame(columns=["Name", "Date", "Time"])

    if not ((df["Name"] == name) & (df["Date"] == date_today)).any():
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        df.to_excel(filename, index=False)
        print(f"[✓] Attendance marked in Excel for {name}")
        # Also mark in CSV
        with open(csv_filename, "a") as f:
            f.write(f"{name},{time_now}\n")
            print(f"[✓] Attendance also marked in CSV for {name}")
    else:
        print(f"[!] {name} already marked today")

# Compare face encodings
def compare_faces(known_encodings, face_encoding):
    distances = np.linalg.norm(known_encodings - face_encoding, axis=1)
    min_distance = np.min(distances)
    if min_distance < 0.6:
        index = np.argmin(distances)
        return index, min_distance
    return None, None

# Main process
def recognize_and_mark():
    names, encodings = load_registered_faces()

    if len(encodings) == 0:
        print("[ERROR] No registered faces found. Please register at least one face.")
        return  # Stop execution
    print("[STEP 5] Starting webcam for real-time recognition...")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to capture video.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector(gray)

        for face in faces:
            shape = landmark_predictor(gray, face)
            face_encoding = face_rec_model.compute_face_descriptor(frame, shape)
            face_encoding_np = np.array(face_encoding)

            match_index, distance = compare_faces(encodings, face_encoding_np)
            if match_index is not None:
                name = names[match_index]
                print(f"[MATCH] {name} recognized with distance: {distance:.3f}")
                mark_attendance(name)
                cv2.putText(frame, f"{name}", (face.left(), face.top() - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)
            else:
                print("[INFO] Unknown face detected.")
                cv2.putText(frame, "Unknown", (face.left(), face.top() - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 0, 255), 2)

        cv2.imshow("Face Recognition - Press 'q' to exit", frame)
        if cv2.waitKey(1) == ord('q'):
            print("[INFO] Quitting face recognition...")
            break

    cap.release()
    cv2.destroyAllWindows()

# Run
if __name__ == "__main__":
    recognize_and_mark()
