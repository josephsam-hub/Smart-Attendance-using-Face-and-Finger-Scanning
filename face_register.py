import cv2
import os

# Create a directory for saving datasets
dataset_dir = 'face_dataset'
if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir)

# Ask user for name or ID
name = input("Enter student name or ID: ")
student_dir = os.path.join(dataset_dir, name)

if not os.path.exists(student_dir):
    os.makedirs(student_dir)
else:
    print("Directory already exists. New images will be added.")

# Start webcam
cap = cv2.VideoCapture(0)
count = 0

print("Capturing faces. Press 'q' to stop.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Register Face - Press 'q' to exit", frame)

    # Save every 5th frame to reduce duplicates
    if count % 5 == 0:
        img_path = os.path.join(student_dir, f"{name}_{count}.jpg")
        cv2.imwrite(img_path, frame)
        print(f"Saved: {img_path}")

    count += 1

    # Press q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
