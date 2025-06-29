DESIGN AND IMPLEMENTATION OF A SMART DOORBELL BASED ON FACIAL DETECTION AND IOT

Cre: https://youtu.be/NteJ33ETxmA?si=2XiOFeneJdEJX11p

Link youtube (old version) https://youtu.be/yMygB4hThUI?si=juEYFKzhCrF24ZOg
Link youtube (new version) https://youtube.com/shorts/BH15ADZUEco?si=b3THPnh-ZV1-eSyH


# Smart Doorbell Project

## Overview
This project focuses on the design and implementation of a **Smart Doorbell** system based on facial detection and Internet of Things (IoT) technologies. The system integrates face detection using Haar Cascade, cloud storage, real-time notifications, and a mobile application for remote monitoring and interaction. The project was developed by Nguyen Thi Tam and Tran Hoang Minh as part of a final exam at The University of Science and Technology.

## Table of Contents
- [Project Description](#project-description)
- [System Design](#system-design)
- [Methodology](#methodology)
- [Experiment Setup](#experiment-setup)
- [Mobile Application](#mobile-application)
- [Results](#results)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Description
The Smart Doorbell system enhances home security and convenience by incorporating facial detection, cloud storage, and real-time communication features. When a visitor approaches, the system detects their face, captures images or videos, and sends notifications to the homeowner's mobile device. It supports two-way audio communication and allows remote access to stored media via cloud platforms like Cloudinary and Firebase.

## System Design
The system is built around a **Raspberry Pi 5** board, integrated with:
- **Raspberry Pi Camera V2** for capturing high-definition images and videos.
- **ReSpeaker 2-Mics Pi HAT** for two-way audio communication.
- **Stereo speaker** and **2W USB-C Power Supply** for operation.
- The system connects to cloud services (Cloudinary and Firebase) for secure storage and remote access.
- When a visitor presses the doorbell, the system initiates a real-time video call and can trigger an alarm for unknown visitors.

Key features:
- **Face Detection**: Utilizes Haar Cascade for real-time face recognition.
- **Cloud Storage**: Stores images and videos securely for later review.
- **Notifications**: Sends alerts to the homeowner's mobile device.
- **Two-Way Audio**: Enables communication between the homeowner and visitor.
- **Video Streaming**: Provides live video feed and recorded footage access.

## Methodology
The face detection mechanism is based on the **Haar Cascade** algorithm, introduced by Paul Viola and Michael Jones in 2001. This method uses Haar-like features (rectangular patterns resembling edges, lines, or corners) to identify faces with a reported detection accuracy of up to 99.7%. The system processes images in real-time, capturing and analyzing facial features to trigger doorbell functions.

## Experiment Setup
The hardware setup includes:
- **Raspberry Pi 5** as the main controller.
- **Raspberry Pi Camera V2** for video and image capture.
- **ReSpeaker 2-Mics Pi HAT** for audio input/output.
- **Cloud Services**: Cloudinary and Firebase for data storage and remote access.

Testing was conducted with 50 images and 50 videos under various conditions, including different lighting levels (day to night), face angles, and distances. The results are summarized in figures and tables within the project documentation.

## Mobile Application
A user-friendly mobile application was designed to interact with the Smart Doorbell. Key features include:
- **Video Call**: Initiated via a "Call Video" button for real-time interaction with visitors.
- **Cloud Access**: Allows users to view stored images and videos on Cloudinary.
- **Notifications**: Provides real-time alerts for doorbell events.
- **User Interface**: Intuitive design for seamless user experience (illustrated in Fig. 10 of the project document).

The application demonstrated low latency and high reliability during testing.

## Results
The Smart Doorbell system achieved high accuracy in face detection under controlled and real-world conditions. Tests showed robust performance across varying lighting conditions, face angles, and distances. The integration with the mobile application was seamless, enabling efficient management of stored media and real-time communication.

## Repository Structure (on-going)
```
Smart-Doorbell/
├── src/
│   ├── face_detection.py         # Python script for Haar Cascade face detection
│   ├── cloud_integration.py     # Script for Cloudinary and Firebase integration
│   ├── video_call.py            # Script for real-time video call functionality
│   ├── audio_stream.py          # Script for two-way audio communication
├── docs/
│   ├── Final_Exam_Report.pdf    # Project documentation
├── README.md                    # Project overview and instructions
```

## Requirements
- **Hardware**:
  - Raspberry Pi 5
  - Raspberry Pi Camera V2
  - ReSpeaker 2-Mics Pi HAT
  - Stereo speaker
  - 2W USB-C Power Supply
- **Software**:
  - Python 3.x
  - OpenCV for face detection
  - Cloudinary and Firebase SDKs
  - Mobile application development tools (e.g., Flutter or React Native)
- **Dependencies**:
  - Install required Python libraries: `opencv-python`, `cloudinary`, `firebase-admin`

## Installation (on-going)
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/Smart-Doorbell.git
   ```
2. Set up the Raspberry Pi 5 with the required hardware components.
3. Install dependencies:
   ```bash
   pip install opencv-python cloudinary firebase-admin
   ```
4. Configure Cloudinary and Firebase credentials in `cloud_integration.py`.
5. Deploy the mobile application on a compatible device (e.g., iOS or Android).

## Usage (on-going)
1. Power on the Raspberry Pi and ensure all hardware components are connected.
2. Run the face detection script:
   ```bash
   python src/face_detection.py
   ```
3. Test cloud integration and notifications:
   ```bash
   python src/cloud_integration.py
   ```
4. Launch the mobile application and press the "Call Video" button to test real-time video and audio functionality.
5. Access stored images and videos via the mobile app or cloud platform.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or bug fixes.

## License
This project is licensed under the MIT License.
