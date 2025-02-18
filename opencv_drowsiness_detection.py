import cv2
import pygame
import threading
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Initialize the pygame mixer (for alarm sound)
pygame.mixer.init()

# Function to play the alarm (with threading for efficiency)
def play_alarm():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("D:/Drowiness/music.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Play indefinitely

# Function to stop the alarm
def stop_alarm():
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

# Load the haarcascade models for face and eyes
eye_cascPath = 'haarcascade_eye_tree_eyeglasses.xml'
face_cascPath = 'haarcascade_frontalface_alt.xml'
faceCascade = cv2.CascadeClassifier(face_cascPath)
eyeCascade = cv2.CascadeClassifier(eye_cascPath)

# Variables for calibration and monitoring
start_time = None
blink_durations = []
DROWSINESS_THRESHOLD = 1.5  # Default threshold
calibration_complete = False
default_calibration_duration = 15  # Increased to 30 seconds
adjusted_calibration_duration = 1  # If no blinks, use 1 second calibration time

# Function for calibration phase
def calibrate():
    global start_time, calibration_complete, blink_durations, DROWSINESS_THRESHOLD
    cap = cv2.VideoCapture(0)
    calibration_start = time.time()
    calibration_duration = default_calibration_duration

    no_blinks_detected = True  # Flag to check if blinks were detected

    # Create a separate OpenCV window for calibration
    cv2.namedWindow("Calibration - Face Detection", cv2.WINDOW_NORMAL)

    # Start the countdown loop and update the label
    while True:
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.resize(img, (600, 500))  # Resize for faster processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                face_region = gray[y:y + h, x:x + w]
                eyes = eyeCascade.detectMultiScale(face_region, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10))

                if len(eyes) == 0:
                    if start_time is None:
                        start_time = time.time()
                    no_blinks_detected = False  # Blink detected, update the flag
                else:
                    if start_time is not None:
                        blink_duration = time.time() - start_time
                        blink_durations.append(blink_duration)
                        start_time = None

        # Show countdown on the Tkinter window
        elapsed_time = time.time() - calibration_start
        countdown_time = max(0, calibration_duration - int(elapsed_time))
        update_status(f"Calibration in Progress... {countdown_time}s", "blue")
        
        # Refresh the Tkinter window to update the countdown in real time
        window.update()

        # Show the face detection in the OpenCV window
        cv2.imshow("Calibration - Face Detection", img)

        if elapsed_time > calibration_duration:
            break

    cap.release()
    cv2.destroyWindow("Calibration - Face Detection")

    # If no blinks were detected, reduce the calibration time to 1 second
    if no_blinks_detected:
        calibration_duration = adjusted_calibration_duration
        messagebox.showwarning("No Blinks Detected", f"No blinks detected. Reducing calibration duration to {calibration_duration} second.")
    
    if blink_durations:
        avg_blink_duration = sum(blink_durations) / len(blink_durations)
        DROWSINESS_THRESHOLD = avg_blink_duration * 2  # Adjust the multiplier if needed
        messagebox.showinfo("Calibration Complete", f"Average blink duration: {avg_blink_duration:.2f} seconds.\n"
                                                    f"Drowsiness threshold: {DROWSINESS_THRESHOLD:.2f} seconds.")
    else:
        messagebox.showwarning("Calibration Failed", "No blinks were detected. Using default threshold.")
        # Set to a default threshold when no blinks are detected
        DROWSINESS_THRESHOLD = 2.5  # This can be adjusted as needed
        
    calibration_complete = True
    update_status("Calibration Complete", "green")

# Function for real-time monitoring
def monitor():
    if not calibration_complete:
        messagebox.showerror("Error", "Calibration not completed yet!")
        return

    global start_time
    cap = cv2.VideoCapture(0)
    alarm_triggered = False  # Flag to ensure alarm is only triggered once

    while True:
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.resize(img, (600, 500))  # Resize for faster processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                face_region = gray[y:y + h, x:x + w]
                eyes = eyeCascade.detectMultiScale(face_region, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10))

                if len(eyes) == 0:  # Eyes closed
                    if start_time is None:
                        start_time = time.time()
                    else:
                        elapsed_time = time.time() - start_time
                        if elapsed_time > DROWSINESS_THRESHOLD and not alarm_triggered:
                            threading.Thread(target=play_alarm).start()  # Trigger alarm in a thread
                            alarm_triggered = True
                            update_status("Drowsiness Detected! Alarm Triggered.", "red")
                else:
                    start_time = None
                    alarm_triggered = False
                    stop_alarm()
                    update_status("Monitoring - Eyes Open", "green")

        cv2.imshow('Drowsiness Monitoring', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    stop_alarm()

# Update the status label
def update_status(message, color):
    status_label.config(text=message, fg=color)

# Tkinter interface
def create_interface():
    global window, status_label
    window = tk.Tk()
    window.title("Drowsiness Detection System")
    window.geometry("1000x700")  # Increased window size
    window.config(bg="#f4f4f9")

    # Create a Frame for the logo and header
    top_frame = tk.Frame(window, bg="#f4f4f9")
    top_frame.pack(pady=20)

    # Load and display NIELIT logo (ensure the logo file path is correct)
    try:
        # Load the logo using PIL
        logo_image = Image.open("Nielit.png")  # Ensure the path is correct
        logo_image = logo_image.resize((250, 150))  # Resize the logo
        logo_image = ImageTk.PhotoImage(logo_image)  # Convert the image to a Tkinter-compatible format

        logo_label = tk.Label(top_frame, image=logo_image, bg="#f4f4f9")
        logo_label.image = logo_image  # Keep a reference to avoid garbage collection
        logo_label.pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Logo not found: {e}")

    # Header (title) under logo
    header_label = tk.Label(top_frame, text="Drowsiness Detection System", font=("Arial", 24, "bold"), fg="black", bg="#f4f4f9")
    header_label.pack(pady=10)

    # Button Frame
    button_frame = tk.Frame(window, bg="#f4f4f9")
    button_frame.pack(pady=30)

    # Buttons for actions
    tk.Button(button_frame, text="Start Calibration", font=("Arial", 16), width=20, height=2, bg="#4caf50", fg="white", command=calibrate).pack(pady=10)
    tk.Button(button_frame, text="Start Monitoring", font=("Arial", 16), width=20, height=2, bg="#ff9800", fg="white", command=monitor).pack(pady=10)
    tk.Button(button_frame, text="Exit", font=("Arial", 16), width=20, height=2, bg="#f44336", fg="white", command=window.quit).pack(pady=10)

    # Status Label (for messages like "Calibration in progress...")
    status_label = tk.Label(window, text="Welcome! Please start calibration.", font=("Arial", 16), fg="blue", bg="#f4f4f9")
    status_label.pack(pady=30)

    window.mainloop()

# Start the Tkinter interface
create_interface()
