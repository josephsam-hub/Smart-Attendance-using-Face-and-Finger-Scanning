import cv2
import dlib
import numpy as np

# Load models
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# Load a known face image and compute encoding
known_image = cv2.imread("known.jpg")
known_rgb = cv2.cvtColor(known_image, cv2.COLOR_BGR2RGB)
known_faces = detector(known_rgb)
known_shape = predictor(known_rgb, known_faces[0])
known_encoding = np.array(face_rec_model.compute_face_descriptor(known_rgb, known_shape))

# Start webcam
cap = cv2.VideoCapture(0)

print("Press 'q' to quit")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detector(rgb_frame)

    for face in faces:
        shape = predictor(rgb_frame, face)
        encoding = np.array(face_rec_model.compute_face_descriptor(rgb_frame, shape))

        # Compare encodings
        dist = np.linalg.norm(known_encoding - encoding)
        match = dist < 0.6  # threshold (adjustable)

        label = "Match" if match else "Unknown"
        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0) if match else (0, 0, 255), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.imshow("Face Recognition", frame)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
