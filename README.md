# Virtual Hand-Tracked Keyboard using OpenCV and HandTrackingModule

This project implements a virtual keyboard interface using hand tracking via a webcam. The keyboard allows real-time text entry using gestures, making it touchless and interactive.

## ✨ Features

- **Hand Tracking:** Uses `cvzone.HandTrackingModule` for accurate hand detection.
- **Right Hand to Type:** Index fingertip is used to select keys.
- **Left Hand Gestures:**
  - **Thumb + Index Finger:** Simulates a click.
  - **Thumb + Middle Finger:** Exits the application.
- **Rounded Key UI:** Each key is rendered with rounded corners for a modern aesthetic.
- **Click Sound Effect:** Plays a click sound upon key press using `pygame`.
- **Text Preview Box:** Displays the last 60 characters typed.

## 🎮 How to Use

1. Raise your **Right Hand** in front of the camera.
2. Hover the index fingertip over a key to highlight.
3. Bring **Left Hand's** **Thumb and Index Finger** together to simulate a click.
4. To **exit**, touch your **Left Hand's** **Thumb and Middle Finger** together.

## 🧑‍💻 Requirements

Install the dependencies:

```bash
pip install opencv-python pyautogui cvzone pygame screeninfo
```

Ensure your webcam is connected and accessible.

## ▶️ How to Run

1. Clone this repository or copy the script.
```bash
git clone https://github.com/ReaalSATYAM/Virtual_Keyboard.git
cd Virtual_Keyboard
```
2. Ensure the file `clickSound.mp3` is in the same directory as the script.
3. Run the Python script:

```bash
python virtual_keyboard.py
```

## 📌 Notes

- The webcam index is set to `1`. If your default webcam is at index `0`, change `cv2.VideoCapture(1)` to `cv2.VideoCapture(0)`.
- Sound effects require a `clickSound.mp3` file in the same directory.
- Adjust detection confidence or distances as per your environment for best performance.

## 📷 Demo
![Image]("demo.png")

## Contributing
Feel free to fork this repository, submit issues, or contribute pull requests. All contributions are welcome!

# Contact Information
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?logo=linkedin&logoColor=white&style=for-the-badge)](https://www.linkedin.com/in/satyam-naithani-sss/)
[![GitHub](https://img.shields.io/badge/-GitHub-181717?logo=github&logoColor=white&style=for-the-badge)](https://github.com/ReaalSATYAM)
---

Enjoy building and typing hands-free! 🖐⌨️
