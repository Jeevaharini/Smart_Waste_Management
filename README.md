
# Raspberry Pi Waste Categorization System with Machine Learning

This project utilizes a Raspberry Pi to automate the sorting of waste into wet and dry categories. It further classifies dry waste into organic and recyclable types using a VGG16 machine learning model for image recognition with a webcam. The system employs ultrasonic sensors, a soil moisture sensor, and servo motors to achieve this. Data is sent to a ThingSpeak channel for monitoring.

## Features
- Automatic detection and sorting of waste.
- Differentiates between wet, organic, and recyclable waste.
- Uses a VGG16 model for image classification via a webcam.
- Sends real-time data to ThingSpeak.

## Components
- Raspberry Pi
- Ultrasonic Sensors
- Soil Moisture Sensor
- Servo Motors
- Webcam
- Pre-trained VGG16 Model

## Setup
1. Connect all sensors, the webcam, and actuators to the Raspberry Pi as per the GPIO pin configuration in the script.
2. Ensure you have the required libraries installed:
   - `RPi.GPIO`
   - `tensorflow`
   - `keras`
   - `opencv-python`
   - `urllib`
3. Run the script on the Raspberry Pi.
4. Monitor the data on ThingSpeak.

## Usage
- The script continuously monitors for waste and sorts it accordingly.
- For dry waste, the webcam captures an image, and the VGG16 model classifies it as organic or recyclable.

