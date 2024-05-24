# Visual Docking Guidance System

The **Visual Docking Guidance System** is a project aimed at assisting users in docking maneuvers by providing visual feedback based on the position of objects detected in a camera feed. This system utilizes computer vision techniques for object detection and MQTT communication for real-time interaction with external devices, such as displays controlled by Arduino.

## Overview

Docking maneuvers, whether in parking spaces, loading docks, or other scenarios, can be challenging, especially in tight spaces or low-visibility conditions. The **Visual Docking Guidance System** aims to address these challenges by providing real-time visual feedback to the user, helping them position their vehicle or object accurately.

The system consists of two main components:

1. **Object Detection System (Python Script)**:
   - Captures video feed from a camera.
   - Detects objects in the camera feed, particularly focusing on identifying objects in specific regions (left, middle, right).
   - Communicates the position of detected objects via MQTT messages.

2. **Display Control System (Arduino Code)**:
   - Listens for MQTT messages containing object position information.
   - Controls animations or visual indicators on a display based on the received messages, providing guidance to the user during docking maneuvers.

## Features

- Real-time object detection using **OpenCV**.
- **MQTT** communication for seamless integration with external devices.
- Customizable display animations to provide intuitive guidance.
- Scalable architecture for extending functionality and adding additional features.

## Getting Started

To set up the **Visual Docking Guidance System**, follow these steps:

1. **Hardware Setup**:
   - Connect a camera to your computer for capturing video feed.
   - Connect an Arduino board to a display or indicator system for visual feedback.

2. **Software Installation**:
   - Install **Python** and the necessary libraries (**OpenCV**, **paho-mqtt**).
   - Upload the Arduino code to your Arduino board.

3. **Configuration**:
   - Configure the **MQTT** broker IP address and port in the Python script and Arduino code.
   - Customize object detection parameters and display animations as needed.

4. **Execution**:
   - Run the Python script to start object detection and **MQTT** communication.
   - Ensure that the Arduino is powered on and connected to the **MQTT** broker.

5. **Usage**:
   - Use the visual feedback provided by the display to guide docking maneuvers.
   - Monitor **MQTT** messages for debugging and troubleshooting.
