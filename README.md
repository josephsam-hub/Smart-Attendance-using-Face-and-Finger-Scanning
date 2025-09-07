Smart Attendance System using Face and Finger Scanning

🚀 A modern attendance monitoring system that integrates Face Recognition and Fingerprint Scanning for secure and automated student/employee attendance.

📌 Features

✅ Face Recognition – Real-time detection and recognition of registered users.

✅ Fingerprint Scanning – Biometric authentication for accurate identification.

✅ Dual Authentication – Option to mark attendance using face, fingerprint, or both.

✅ Attendance Storage – Data stored securely in SQLite/Excel/CSV formats.

✅ GUI Dashboard – Easy-to-use interface for Admins and Students.

✅ Admin Panel – Manage users, view reports, and export attendance.

✅ Voice/Beep Feedback – Alerts when attendance is marked successfully.

🏗️ Tech Stack

Python 3.10+

Libraries: OpenCV, dlib, face_recognition, Tkinter, sqlite3, pandas, xlwt

Hardware Support: Fingerprint Scanner Module (e.g., R305, Digital Persona)

📂 Project Structure
Smart-Attendance-using-Face-and-Finger-Scanning/
│── face_dataset/        # Registered user face images
│── attendance/          # Attendance records (CSV/Excel)
│── database/            # SQLite DB files
│── gui/                 # GUI scripts
│── models/              # Pre-trained models for face recognition
│── app.py               # Main application script
│── requirements.txt     # Dependencies
│── README.md            # Project documentation

⚙️ Installation

Clone this repository

git clone https://github.com/josephsam-hub/Smart-Attendance-using-Face-and-Finger-Scanning.git
cd Smart-Attendance-using-Face-and-Finger-Scanning


Install dependencies

pip install -r requirements.txt


Connect and configure the Fingerprint Scanner.

Run the application

python app.py

🎯 Usage

Register Students/Employees with face and fingerprint.

Start Attendance Session – System automatically marks attendance.

View Attendance Reports – Export data to CSV/Excel for analysis.

(Add GUI/working screenshots here)

👨‍💻 Contributors

Joseph Sam

🏅 Achievements

This project was developed as part of academic/innovation challenges and awarded a Certificate of Achievement.
