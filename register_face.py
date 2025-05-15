import cv2
import dlib
import os
import numpy as np
import pickle

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Download below
facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# Create a directory to store encodings
if not os.path.exists("encodings"):
    os.makedirs("encodings")

name = input("Enter student name: ")

cap = cv2.VideoCapture(0)
count = 0
descriptors = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        shape = sp(gray, face)
        face_descriptor = facerec.compute_face_descriptor(frame, shape)
        descriptors.append(np.array(face_descriptor))
        count += 1

        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, f"Capturing {count}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Register Face - Press Q to stop", frame)

    if count >= 10 or cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Save descriptors
with open(f'encodings/{name}.pkl', 'wb') as f:
    pickle.dump(descriptors, f)

print(f"[INFO] Face data saved for {name}")
