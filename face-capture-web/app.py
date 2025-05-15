from flask import Flask, request, render_template
import os
import base64

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_face', methods=['POST'])
def upload_face():
    data = request.json
    name = data.get("name")
    image_data = data.get("image")
    count = data.get("count")

    if not name or not image_data:
        return {"status": "error", "message": "Missing name or image"}, 400

    student_dir = os.path.join(UPLOAD_FOLDER, name)
    os.makedirs(student_dir, exist_ok=True)

    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)

    with open(os.path.join(student_dir, f"{name}_{count}.jpg"), 'wb') as f:
        f.write(image_bytes)

    return {"status": "success", "message": f"Image {count} saved"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
