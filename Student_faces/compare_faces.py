import face_recognition

# Load the images using full file paths
image1 = face_recognition.load_image_file("face1.jpg")
image2 = face_recognition.load_image_file("face2.jpg")

# Encode the faces (convert them to numerical data)
face_encoding1 = face_recognition.face_encodings(image1)[0]
face_encoding2 = face_recognition.face_encodings(image2)[0]

# Compare the faces
results = face_recognition.compare_faces([face_encoding1], face_encoding2)

if results[0]:
    print("The faces match!")
else:
    print("The faces do not match!")
