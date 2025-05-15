import cv2
import os
import tkinter as tk
from tkinter import messagebox
from threading import Thread

def capture_faces(name):
    dataset_dir = 'face_dataset'
    student_dir = os.path.join(dataset_dir, name)

    if not os.path.exists(student_dir):
        os.makedirs(student_dir)

    cap = cv2.VideoCapture(0)
    count = 0
    print("Capturing 25 face images...")

    while count < 25:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Capturing - Press 'q' to quit", frame)

        img_path = os.path.join(student_dir, f"{name}_{count}.jpg")
        cv2.imwrite(img_path, frame)
        print(f"[✓] Saved: {img_path}")
        count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Success", f"Captured 25 images for {name}")

def start_capture():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Input Error", "Please enter a student name or ID.")
        return
    Thread(target=capture_faces, args=(name,)).start()

# GUI Setup
app = tk.Tk()
app.title("Face Registration")
app.geometry("400x200")

tk.Label(app, text="Enter Student Name or ID:", font=("Arial", 12)).pack(pady=10)
name_entry = tk.Entry(app, font=("Arial", 12), width=30)
name_entry.pack(pady=5)

start_button = tk.Button(app, text="Start Capturing Faces", font=("Arial", 12), command=start_capture)
start_button.pack(pady=20)

app.mainloop()
