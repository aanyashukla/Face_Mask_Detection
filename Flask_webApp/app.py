import os
import sys
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import base64

# --- Setup Project Paths ---
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = os.getcwd()

face_cascade_path = os.path.join(base_dir, "haarcascade_frontalface_default.xml")
model_path = os.path.join(base_dir, "mask_detector.h5")

# --- Error Checking for Essential Files ---
for file_path in [face_cascade_path, model_path]:
    if not os.path.exists(file_path):
        print(f"FATAL ERROR: A required file could not be found.")
        print(f"The script was looking for it at this exact path: {file_path}")
        print("Please make sure all required files (app.py, .h5 model, and .xml cascade) are in the same folder.")
        sys.exit(1)
# -------------------------------------------

# Initialize the Flask application
app = Flask(__name__)

# Load the pre-trained models and cascades
try:
    mask_model = load_model(model_path)
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    if face_cascade.empty():
        raise IOError(f"Failed to load face cascade from {face_cascade_path}. The file may be corrupt.")
except Exception as e:
    print(f"FATAL ERROR: Failed to load a required model or cascade file.")
    print(f"Reason: {e}")
    sys.exit(1)

# Labels for the classes
LABELS = ["Mask Worn Incorrectly 🥴", "Mask 😊", "No Mask 😢"]


def detect_mask(image):
    """
    Detects faces and predicts mask status using class-specific confidence logic.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    if len(faces) == 0:
        return image, "No Face Detected 🤷‍♀️", 0.0

    (x, y, w, h) = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[0]
    face_roi_color = image[y:y + h, x:x + w]

    face_resized = cv2.resize(face_roi_color, (128, 128))
    face_array = img_to_array(face_resized)
    face_array = np.expand_dims(face_array, axis=0)
    face_array = face_array / 255.0

    prediction = mask_model.predict(face_array)[0]
    label_index = np.argmax(prediction)
    label = LABELS[label_index]
    confidence = prediction[label_index] * 100

    if label_index == 1:  # If initial prediction is "Mask"
        if confidence < 95:
            # If confidence is not very high, it's likely incorrect (e.g., on chin)
            label = LABELS[0]  # Override to "Mask Worn Incorrectly"

    if confidence < 75:
        # If any final prediction has low confidence, it's uncertain
        label = "Uncertain 🤔"

    # Draw a rectangle around the detected face
    cv2.rectangle(image, (x, y), (x + w, y + h), (144, 238, 144), 2)
    return image, label, confidence


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """Handles the prediction request from the frontend."""
    image = None
    if 'file' in request.files:
        file = request.files['file']
        if file.filename:
            filestr = file.read()
            npimg = np.frombuffer(filestr, np.uint8)
            image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    elif 'image' in request.json:
        image_data = request.json['image'].split(',')[1]
        decoded_image = base64.b64decode(image_data)
        npimg = np.frombuffer(decoded_image, np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({'error': 'No image data received'})

    annotated_image, label, confidence = detect_mask(image)
    _, buffer = cv2.imencode('.jpg', annotated_image)
    encoded_image = base64.b64encode(buffer).decode('utf-8')

    return jsonify({
        'label': label,
        'confidence': f'{confidence:.2f}%',
        'image': f'data:image/jpeg;base64,{encoded_image}'
    })

if __name__ == '__main__':
    app.run(debug=True)
