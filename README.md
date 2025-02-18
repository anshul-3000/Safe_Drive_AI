# Drowsiness Detection System

## 🚀 Overview
This project implements a **real-time drowsiness detection system** using OpenCV and Python. It monitors eye states and triggers an alarm if prolonged eye closure is detected, helping prevent accidents caused by drowsy driving.

## 🔥 Features
- **Real-time face and eye detection** using OpenCV.
- **Calibration mode** to dynamically adjust the drowsiness threshold.
- **Alarm system** using Pygame to alert users when drowsiness is detected.
- **Tkinter-based GUI** for easy interaction.
- **Processes webcam frames at high speed** for efficient detection.

## 🛠️ Tech Stack
- **Python** – Core programming language
- **OpenCV** – Face and eye detection
- **Pygame** – Alarm sound system
- **Tkinter** – GUI development
- **PIL (Python Imaging Library)** – Image handling
- **Threading** – For efficient background tasks

## 📌 Installation
1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/drowsiness-detection.git
   cd drowsiness-detection
   ```
2. **Install Dependencies**
   ```sh
   pip install opencv-python pygame pillow
   ```
3. **Download Haarcascade Files**
   Ensure the following files are present in the project directory:
   - `haarcascade_frontalface_alt.xml`
   - `haarcascade_eye_tree_eyeglasses.xml`
   
   You can download them from [OpenCV's GitHub](https://github.com/opencv/opencv/tree/master/data/haarcascades).

## 🚀 Usage
1. **Run the script**
   ```sh
   python opencv_drowsiness_detection.py
   ```
2. **Calibration Mode**
   - Click **"Start Calibration"** to set up blink duration.
   - The system will monitor blinks and set a custom drowsiness threshold.
   
3. **Drowsiness Monitoring**
   - Click **"Start Monitoring"** to begin real-time detection.
   - The system will trigger an alarm if eyes remain closed beyond the threshold.
   - Press `q` to exit the monitoring window.

## 🎯 Future Enhancements
- Implement deep learning (CNN-based) detection.
- Mobile integration for real-time driver alerts.
- Cloud-based monitoring and analytics.

## 🤝 Contributing
Feel free to fork the repo, open issues, or submit pull requests!

**🔗 Connect with Me:**  
[LinkedIn](https://www.linkedin.com/in/anshul-chaudhary-b571b5251/) | [GitHub](https://github.com/anshul-3000)

