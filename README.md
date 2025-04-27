# OptiVision: Real-time Object Detection and Analysis

OptiVision is a real-time object detection and analysis system capable of processing images, videos, and RTSP streams. It uses TensorFlow, OpenCV, and a sleek Flask web interface to provide real-time detection results, visualizations, and analytics for any object detection task.

---

## Homepage

Welcome to **OptiVision**! This is the central page of the application where you can navigate to different sections for processing images, videos, and streams. The homepage provides quick access to each detection feature.

![Homepage Image](https://github.com/user-attachments/assets/47462dcc-7e8c-4409-9ebc-1eb0171eb740)
![image](https://github.com/user-attachments/assets/7799e268-224d-47ea-a0d9-639870e25e54)



---

## RTSP Stream

**Stream live feeds from RTSP cameras and detect objects in real-time with precision.**

### Features:
- Seamless connection to RTSP camera streams.
- Real-time object detection and tracking.
- Display detected objects live as the stream plays.


### How to Use:
1. Enter the RTSP stream URL or channel ID in the provided input field.
2. Click **Start Stream** to begin receiving and analyzing the feed.
3. Detected objects will be displayed live with bounding boxes.

---

## Process Image

**Upload static images for detailed object detection and analysis.**

### Features:
- Upload any image to detect objects.
- View detected objects with bounding boxes.
- Save and download the processed image with detected objects.

![image](https://github.com/user-attachments/assets/74f8e55a-653f-4039-9ddb-7f42117391be)


### How to Use:
1. Click **Upload Image** and select an image from your computer.
2. Set the detection threshold to control sensitivity.
3. Click **Process Image** to view the results.
4. Download the processed image by clicking the **Download Image** button.

---

## Process Video

**Analyze uploaded videos to identify and track objects frame by frame.**

### Features:
- Upload video files for object detection.
- Track objects across frames with bounding boxes.
- Video playback with detected objects.

![image](https://github.com/user-attachments/assets/f533e7e6-4245-4855-b8a7-129d1e42969a)


### How to Use:
1. Upload a video file by clicking **Upload Video**.
2. Select the detection options (e.g., processing every nth frame).
3. Click **Start Processing** to view the video with detected objects.
4. Watch the video in real-time or download the processed video.

---

## Process Stream

**Connect and analyze streams from various sources for seamless detection.**

### Features:
- Support for RTSP and HTTP-based stream sources.
- Real-time frame-by-frame analysis.
- View detected objects on a live video feed.

### How to Use:
1. Enter the stream URL (RTSP or HTTP).
2. Click **Start Stream** to connect to the stream.
3. View real-time object detection results.
4. Optionally, download detection results.

---

## Graphs & Analytics

**Visualize detection performance and trends with interactive charts.**

### Features:
- View detection statistics like object counts and accuracy over time.
- Generate trend graphs for object detection performance.
- Interactive and dynamic charts for better analysis.

![image](https://github.com/user-attachments/assets/b0619b19-4464-4048-9e6b-204771d23e5c)
\
![image](https://github.com/user-attachments/assets/e93031eb-b12b-4b93-9c6e-0209bae675ef)
\
![image](https://github.com/user-attachments/assets/4bc7f3c9-c2b8-4fc8-9b6b-1f05d4f8aa3a)



### How to Use:
1. Select a date range to visualize the detection statistics.
2. View the generated interactive graphs showing trends and performance.
3. Analyze the data for further insights into detection accuracy.

---

## Al Chatbot

**Get instant help and insights from our intelligent assistant.**

### Features:
- Chat with an AI-powered assistant for help.
- Get real-time insights and troubleshooting for detection tasks.

![chatbot-ai](https://github.com/user-attachments/assets/c3727edd-e336-4b88-80de-60e7d578cfc6)


### How to Use:
1. Open the chatbot by clicking the **Chat with Assistant** button.
2. Type your question or request for help.
3. Get responses to help guide you through any detection task or issue.

---

# Real-Time Object Detection and Live Stream Analysis Using Jetson Nano

## 🎯 MINI PROJECT

### 👥 TEAM MEMBERS
- **Ganesh Patidar** (20214061)
- **Hardik Kumar Singh** (20214249)
- **Divyanshu** (20214317)
- **Harsh Dave** (20214534)

---

## 📌 CONTENTS
- [Problem Statement](#problem-statement)
- [Introduction](#introduction)
- [Motivation](#motivation)
- [Applications](#applications)
- [Proposed Work](#proposed-work)
- [Experimental Setup](#experimental-setup)
- [Result Analysis](#result-analysis)
- [Challenges](#challenges)
- [Future Work](#future-work)
- [References](#references)

---

## 📢 Problem Statement
- **Livestream Camera Integration with Jetson Nano Hardware**
- **Object Detection on Images, Videos, and Livestream Feeds**

## 📖 Introduction
This project implements a **real-time object detection system** using Jetson Nano, leveraging deep learning algorithms for accurate and efficient object classification. It enhances surveillance, security, and operational efficiency in various applications.

## 💡 Motivation
The inspiration for this project stems from the critical need to improve **security measures** in **public transport systems**. By leveraging **real-time CCTV feeds**, we aim to provide an **automated surveillance system** that ensures passenger safety, particularly for vulnerable groups. Our **goal** is to enable authorities to detect potential security threats **proactively**.

## 🚀 Applications
- **Surveillance and Security Systems**
- **Traffic Management**
- **Retail Analytics**
- **Industrial Automation**
- **Smart Cities**
- **Environmental Monitoring**

## 🔍 Proposed Work
- **Jetson Nano Setup**
- **Live Stream Implementation**
- **Data Collection & Model Training**
- **Evaluation of Object Detection Models**
- **Performance Analysis of Different Models**

## 🛠 Experimental Setup
### 1️⃣ **Setting Up Jetson Nano**
- Flashed the **NVIDIA OS** using **Balena Etcher**.
- Installed **JetPack SDK 4.4.0** for development.
- Booted Jetson Nano and configured the environment.

### 2️⃣ **Live Streaming Implementation**
- Utilized **OpenCV with CUDA** for optimized real-time video processing.
- Enabled efficient video capture and frame-by-frame object detection.

### 3️⃣ **Data Collection & Model Training**
- Collected data using `simple_image_download`.
- Labeled images using `labelImg`.
- Trained a **YOLOv7** model using **Google Colab** for improved computational performance.

### 4️⃣ **Evaluation of Object Detection Models**
- Compared **TensorFlow Model Zoo** models:
  - **SSD ResNet50 640x640**
  - **CenterNet ResNet101 FPNv1 512x512**
- Evaluated based on **mean Average Precision (mAP)** and **inference time**.

### 5️⃣ **Performance Metrics**
- **Precision** = TP / (TP + FP)
- **Recall** = TP / (TP + FN)
- **mAP** = Average of AP across all classes

## 📊 Result Analysis
### ✅ **Accuracy Comparison**
| Model | mAP (Accuracy) |
|--------|--------------|
| **CenterNet ResNet-101** | **Low** |
| **SSD ResNet-50** | **Moderate** |
| **YOLOv7 (Custom)** | **High** |

### ⚡ **Inference Time Trade-offs**
- **Fastest:** CenterNet ResNet-101 (Low accuracy, high speed)
- **Balanced:** SSD ResNet-50 (Moderate speed & accuracy)
- **Most Accurate:** YOLOv7 (High accuracy, slower inference)

### 📷 **Example Results**
![Comparison Graph](https://github.com/Hardik-111/livestream_object_detection/assets/89783619/801819ba-2871-4f6b-8425-f33bab728d98)

![Result Image_1](https://github.com/Hardik-111/livestream_object_detection/assets/89783619/97cc35d7-9780-44a0-89d6-f23a6198ab97)

![Result Image_2](https://github.com/Hardik-111/livestream_object_detection/assets/89783619/b056f45f-4228-430f-8a54-67c2858e3232)

![Result Image_3](https://github.com/Hardik-111/livestream_object_detection/assets/89783619/e6c20bff-9184-4b23-92a8-c9f266b7d69c)

![Result Image_4](https://github.com/Hardik-111/livestream_object_detection/assets/89783619/b43ee2dd-9ef5-426a-a1b1-efff22b16faa)

## 🛑 Challenges
- **Proxy Configuration Issues**
- **Package Installation Errors**
- **SSL Wrong Version Number**
- **Python Version Conflicts**
- **Extended Training Time**
- **Jetson Nano Compatibility Issues**
- **Unexpected Shutdowns During Execution**

## 🔮 Future Work
- **Performance Optimization**
- **Cloud Integration**
- **Real-time Alerts & Notifications**
- **Enhanced User Interface**
- **IoT Device Integration**

## 📚 References
1. **Abadi, M. et al.** [TensorFlow Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md)
2. **Liu, W., Anguelov, D., et al.** SSD: Single Shot Multibox Detector, ECCV (2016)
3. **Redmon, J., et al.** YOLO: Unified, Real-Time Object Detection, IEEE TPAMI (2016)
4. **Wang, J., et al.** YOLOv7: Trainable Bag of Freebies, IEEE TPAMI (2021)
5. **[PyTorch for Jetson](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048)**

---

🚀 **Thank you!** We appreciate your time in reviewing our project! 🎯



