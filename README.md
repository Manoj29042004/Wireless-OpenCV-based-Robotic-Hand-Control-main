
# 🤖 Wireless Human-Robot Interaction: Replicating Hand Movements Using OpenCV and Embedded Systems

This project demonstrates a **gesture-controlled robotic hand** that mimics real-time human finger movements using computer vision and embedded systems. Using OpenCV, MediaPipe, and ESP8266, the system interprets hand gestures and replicates them on a 3D-printed robotic hand. Two operational modes — **Live Mode** and **Replay Mode** — are supported for flexibility in interaction.

## 📽️ Demo Preview
*(Insert demo GIF or YouTube link here if available)*

---

## 🔍 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technologies Used](#technologies-used)
- [Hardware Components](#hardware-components)
- [Setup Instructions](#setup-instructions)
- [Results](#results)
- [Future Improvements](#future-improvements)
- [Contributors](#contributors)

---

## 🚀 Project Overview

The goal of this project is to create a natural and intuitive Human-Robot Interaction (HRI) interface. Hand gestures are captured through a camera, processed to extract finger angles, and transmitted wirelessly to a robotic hand. The hand replicates these gestures using five MG995 servo motors.

---

## ✨ Features
- 🖐️ Real-time hand gesture recognition using OpenCV and MediaPipe
- 🔄 Two operation modes: 
  - **Live Mode**: Real-time gesture replication
  - **Replay Mode**: Playback of pre-recorded gestures
- 📡 Wireless control via ESP8266 using HTTP GET requests
- 🧠 Vector-based finger joint angle calculation and mapping
- 🔌 No physical controllers required

---

## 🧠 System Architecture

```
[Camera] --> [OpenCV + MediaPipe] --> [Joint Angle Calculation]
              ↓
          [Python Script] --> [ESP8266 via Wi-Fi]
              ↓
    [Robotic Hand with 5 Servo Motors]
```

---

## 🛠️ Technologies Used

- **Python** for gesture processing and communication
- **OpenCV & MediaPipe** for real-time hand landmark detection
- **ESP8266 NodeMCU** microcontroller for Wi-Fi communication
- **Arduino IDE** for servo control programming
- **CSV** for storing and replaying gestures

---

## 🧩 Hardware Components

- 📷 Webcam or smartphone camera
- 🤖 3D-Printed Robotic Hand
- 🔧 5x MG995 Servo Motors
- 🌐 ESP8266 NodeMCU Microcontroller
- 🔋 5V Power Supply for servos

---

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/human-robot-gesture-hand.git
   cd human-robot-gesture-hand
   ```

2. **Install required Python packages**
   ```bash
   pip install opencv-python mediapipe numpy requests
   ```

3. **Upload the Arduino sketch** to ESP8266 from the `firmware/` folder using the Arduino IDE.

4. **Run the Python script**
   ```bash
   python gesture_control.py
   ```

5. **Choose the mode**:
   - `Live Mode` for real-time control
   - `Replay Mode` to load pre-recorded gestures from `gestures.csv`

---

## 📊 Results

| Condition        | Accuracy  |
|------------------|-----------|
| Bright Light     | 96.2%     |
| Dim Light        | 93.5%     |
| Low Light        | 89.7%     |
| Replay Accuracy  | 95.2%     |
| Thumb Accuracy   | ~91.5%    |
| Response Time    | 120–180ms |

---

## 🚧 Future Improvements

- Improve gesture recognition in low-light environments using adaptive brightness filters
- Optimize Wi-Fi communication to reduce latency
- Integrate AI models for advanced gesture classification
- Extend gesture vocabulary (e.g., multi-hand gestures)
- Apply to applications like prosthetics, virtual reality, and assistive robotics

---

## 👨‍💻 Contributors

- **G. Manoj**  
- **Y. Tanmai Sabari**  
- **V. Brunda**  
- **P. Kalyan Babu**  
- **Y. Madhu Babu**  
- **Dr. M. Vamshi Krishna** *(Faculty Guide)*

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 📬 Contact

For any queries or collaboration, please reach out to:  
📧 gudisevabrothers@gmail.com  
📧 tanmaiyalamanchili@gmail.com  
📧 vissamsettibrunda02@gmail.com
