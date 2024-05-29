from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2
from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode

# Load the saved model
model = load_model('/content/drive/MyDrive/waste_classification_model.h5')

# Function to preprocess the captured image
def preprocess_image(img):
    img = cv2.resize(img, (150, 150))
    img_array = np.expand_dims(img, axis=0)
    return img_array

# Function to predict waste type from the captured image
def predict_waste(img):
    # Preprocess the image
    img_array = preprocess_image(img)
    # Make prediction
    prediction = model.predict(img_array)
    # Convert prediction to waste type
    if prediction < 0.5:
        waste_type = 'Organic'
    else:
        waste_type = 'Recyclable'
    # Get confidence level
    confidence = round(float(prediction), 2) * 100
    return waste_type, confidence

# Function to capture an image using the webcam
def capture_image():
    js = Javascript('''
        async function capture() {
            const div = document.createElement('div');
            const captureButton = document.createElement('button');
            captureButton.textContent = 'Capture';
            div.appendChild(captureButton);

            const video = document.createElement('video');
            video.style.display = 'block';
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });

            document.body.appendChild(div);
            div.appendChild(video);
            video.srcObject = stream;
            await video.play();

            // Resize the output to fit the video element.
            google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

            // Wait for Capture button click
            await new Promise((resolve) => captureButton.onclick = resolve);

            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            stream.getVideoTracks()[0].stop();
            div.remove();
            return canvas.toDataURL('image/jpeg');
        }
        ''')
    display(js)
    data = eval_js('capture()')
    binary = b64decode(data.split(',')[1])
    image_array = np.frombuffer(binary, dtype=np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return img

# Example usage:
captured_image = capture_image()
predicted_waste, confidence = predict_waste(captured_image)
print("Detected waste:", predicted_waste, "with", confidence, "% confidence")
