document.addEventListener('DOMContentLoaded', () => {
    const fileUpload = document.getElementById('file-upload');
    const webcamButton = document.getElementById('webcam-button');
    const webcamModal = document.getElementById('webcam-modal');
    const closeButton = document.querySelector('.close-button');
    const webcamVideo = document.getElementById('webcam-video');
    const captureButton = document.getElementById('capture-button');
    const resultContainer = document.getElementById('result-container');
    const resultImage = document.getElementById('result-image');
    const predictionLabel = document.getElementById('prediction-label');
    const predictionConfidence = document.getElementById('prediction-confidence');
    const loadingSpinner = document.getElementById('loading-spinner');

    let stream;

    // Handle file upload
    fileUpload.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);
            predict(formData);
        }
    });

    // Open webcam modal
    webcamButton.addEventListener('click', async () => {
        webcamModal.style.display = 'block';
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            webcamVideo.srcObject = stream;
        } catch (error) {
            console.error("Error accessing webcam:", error);
            alert("Could not access the webcam. Please check permissions.");
        }
    });

    // Close webcam modal
    closeButton.addEventListener('click', () => {
        webcamModal.style.display = 'none';
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    });

    // Capture image from webcam
    captureButton.addEventListener('click', () => {
        const canvas = document.createElement('canvas');
        canvas.width = webcamVideo.videoWidth;
        canvas.height = webcamVideo.videoHeight;
        canvas.getContext('2d').drawImage(webcamVideo, 0, 0);
        const imageData = canvas.toDataURL('image/jpeg');

        predict({ image: imageData });

        webcamModal.style.display = 'none';
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    });

    // Function to send data to the backend for prediction
    async function predict(data) {
        loadingSpinner.classList.remove('hidden');
        resultContainer.classList.add('hidden');

        let fetchOptions;
        if (data instanceof FormData) {
            fetchOptions = {
                method: 'POST',
                body: data
            };
        } else {
            fetchOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            };
        }

        try {
            const response = await fetch('/predict', fetchOptions);
            const result = await response.json();

            if (result.error) {
                alert(result.error);
            } else {
                resultImage.src = result.image;
                predictionLabel.textContent = `Prediction: ${result.label}`;
                predictionConfidence.textContent = `Confidence: ${result.confidence}`;
                resultContainer.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Error during prediction:', error);
            alert('An error occurred. Please try again.');
        } finally {
            loadingSpinner.classList.add('hidden');
        }
    }
});
