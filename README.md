# Face Mask Detection App 😷

A Flask-based web application that uses a deep learning model to detect whether a person is wearing a face mask correctly, incorrectly, or not at all. 
Simply upload an image or use your webcam for a real-time prediction!

---

## 🚀 Demo

**Live App Link:** `[Link will be added after deployment]`

---

## ✨ A Note on the Frontend

An interesting aspect of this project is that the entire frontend—the HTML structure, the cozy CSS styling, and the interactive JavaScript for handling uploads and webcam access—was developed through **prompt engineering**. 
The user interface was built iteratively by providing detailed prompts and feedback to an AI assistant, showcasing a modern approach to web development.

---

## 🧠 Model Info

* **Model Architecture:** Transfer learning using **MobileNetV2**.
* **Accuracy:** Achieved **~89% validation accuracy**.
* **Dataset:** Trained on the [Face Mask Detection](https://www.kaggle.com/datasets/andrewmvd/face-mask-detection) dataset from Kaggle, which contains 853 images with annotations.
* **Classes:**
    1.  `With Mask`
    2.  `Without Mask`
    3.  `Mask Worn Incorrectly`
* **Input Shape:** `128x128x3` (RGB images of cropped faces).

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Deep Learning:** TensorFlow / Keras
* **Image Processing:** OpenCV, NumPy
* **Frontend:** HTML, CSS, JavaScript

---

## 📁 Project Structure

```
Face-Mask-Detection/
│
├── Model/
│   ├── Face_Mask_Detection.ipynb    # Jupyter notebook for model training
│   └── mask_detector.h5             # Trained Keras model
│
├── Flask_webApp/
│   ├── static/
│   │   ├── style.css                # CSS for styling
│   │   └── script.js                # JavaScript for frontend logic
│   │
│   ├── templates/
│   │   └── index.html               # Main HTML page
│   │
│   ├── app.py                       # Flask application logic
│   ├── haarcascade_frontalface_default.xml # OpenCV face detection model
│   ├── mask_detector.h5             # Trained Keras model (used by app)
│   └── requirements.txt             # Python package requirements
│
└── .gitignore                       # Files/folders to ignore in Git
```

---

## 📝 How to Use (Live App)

1.  Open the live app link (coming soon!).
2.  Click **"📁 Upload a Photo"** to select an image from your device.
3.  Alternatively, click **"📸 Capture from Webcam"** to use your camera.
4.  See the prediction result and confidence score!

---

## 💻 Local Setup

To run this project on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/aanyashukla/Face_Mask_Detection.git](https://github.com/aanyashukla/Face_Mask_Detection)
    ```

2.  **Navigate to the app directory:**
    ```bash
    cd Face_Mask_Detection/Flask_webApp
    ```

3.  **Create a virtual environment and activate it:**
    ```bash
    # For Windows
    python -m venv .venv
    .venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

4.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Flask app:**
    ```bash
    python app.py
    ```
    
---

## 👨‍💻 Author

Made with ❤️ by [Aanya Shukla](https://github.com/aanyashukla/)
