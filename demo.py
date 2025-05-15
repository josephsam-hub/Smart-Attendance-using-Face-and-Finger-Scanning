import tkinter as tk
from tkinter import ttk, messagebox
import os
import cv2
import face_recognition
import numpy as np
import pandas as pd
import sqlite3
from pyzbar.pyzbar import decode
from datetime import datetime

# === SQLite Login Authentication ===
def check_login(username, password):
    conn = sqlite3.connect("face_attendance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# === Mark Attendance to CSV and Excel ===
def mark_attendance(name):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    csv_filename = f"attendance/attendance_{date_str}.csv"

    if not os.path.exists("attendance"):
        os.makedirs("attendance")

    if os.path.exists(csv_filename):
        df = pd.read_csv(csv_filename)
        if name in df['Name'].values:
            return "Already Present!"
        else:
            df = pd.concat([df, pd.DataFrame([[name, date_str, time_str]], columns=["Name", "Date", "Time"])] )
            df.to_csv(csv_filename, index=False)
            return "Marked!"
    else:
        df = pd.DataFrame([[name, date_str, time_str]], columns=["Name", "Date", "Time"])
        df.to_csv(csv_filename, index=False)
        return "Marked!"

# === Register Face with Barcode ===
import cv2
import os

def register_face_with_barcode(name, barcode):
    cap = cv2.VideoCapture(0)
    count = 0
    save_path = "face_dataset"
    os.makedirs(save_path, exist_ok=True)

    print("Press 's' to save a face image.")
    print("Press 'q' to quit face scan early.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Register Face", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            filename = f"{barcode}_{name}_{count}.jpg"
            cv2.imwrite(os.path.join(save_path, filename), frame)
            print(f"Saved {filename}")
            count += 1
            if count >= 5:
                print("Captured 5 images. Registration complete.")
                break

        elif key == ord('q'):
            print("Face scan stopped by user.")
            break

    cap.release()
    cv2.destroyAllWindows()

# === Real-Time Face Recognition Attendance ===
def recognize_faces():
    known_encodings = []
    known_names = []

    for filename in os.listdir("face_dataset"):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            path = os.path.join("face_dataset", filename)
            img = face_recognition.load_image_file(path)
            enc = face_recognition.face_encodings(img)
            if enc:
                known_encodings.append(enc[0])
                known_names.append(os.path.splitext(filename)[0])

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, faces)

        for (top, right, bottom, left), enc in zip(faces, encodings):
            matches = face_recognition.compare_faces(known_encodings, enc)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = known_names[match_index]

            label = mark_attendance(name)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, f"{name} ({label})", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Face Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# === Barcode Attendance ===
def mark_barcode_attendance():
    cap = cv2.VideoCapture(0)
    scanned_ids = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        decoded_objects = decode(frame)
        for obj in decoded_objects:
            roll_no = obj.data.decode('utf-8')
            if roll_no not in scanned_ids:
                scanned_ids.add(roll_no)
                now = datetime.now()
                date_str = now.strftime("%Y-%m-%d")
                time_str = now.strftime("%H:%M:%S")
                filename = f"attendance/barcode_attendance_{date_str}.csv"

                if not os.path.exists("attendance"):
                    os.makedirs("attendance")

                if os.path.exists(filename):
                    df = pd.read_csv(filename)
                    if roll_no in df['Roll'].values:
                        print(f"{roll_no} already marked!")
                    else:
                        new_data = pd.DataFrame([[roll_no, date_str, time_str]], columns=["Roll", "Date", "Time"])
                        df = pd.concat([df, new_data])
                        df.to_csv(filename, index=False)
                        print(f"Marked attendance for {roll_no}")
                else:
                    df = pd.DataFrame([[roll_no, date_str, time_str]], columns=["Roll", "Date", "Time"])
                    df.to_csv(filename, index=False)
                    print(f"Marked attendance for {roll_no}")

        cv2.imshow("Barcode Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# === GUI ===
root = tk.Tk()
root.title("Smart Attendance System")
root.geometry("600x500")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

face_tab = ttk.Frame(notebook)
barcode_tab = ttk.Frame(notebook)
register_tab = ttk.Frame(notebook)
notebook.add(face_tab, text='Face Attendance')
notebook.add(barcode_tab, text='Barcode Attendance')
notebook.add(register_tab, text='Register Face')

tk.Button(face_tab, text="Start Face Recognition", command=recognize_faces, height=2, width=30).pack(pady=50)
tk.Button(barcode_tab, text="Start Barcode Scanner", command=mark_barcode_attendance, height=2, width=30).pack(pady=50)

# Registration Form for Barcode + Face
tk.Label(register_tab, text="Enter Name:").pack(pady=5)
entry_name = tk.Entry(register_tab)
entry_name.pack(pady=5)

tk.Label(register_tab, text="Enter Barcode (e.g., ID):").pack(pady=5)
entry_barcode = tk.Entry(register_tab)
entry_barcode.pack(pady=5)

def on_register():
    name = entry_name.get().strip().upper()
    barcode = entry_barcode.get().strip().upper()
    if not name or not barcode:
        messagebox.showerror("Error", "Please enter both name and barcode")
    else:
        register_face_with_barcode(name, barcode)
        messagebox.showinfo("Success", f"Face registered for {name} with barcode {barcode}")

register_btn = tk.Button(register_tab, text="Register Face", command=on_register, height=2, width=30)
register_btn.pack(pady=20)

root.mainloop()
