import cv2
import pygame
import threading
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys

# Initialize pygame mixer for sound
pygame.mixer.init()

# Function to play the alarm
def play_alarm():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("D:/Drowiness/music.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

# Function to stop the alarm
def stop_alarm():
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

# Load Haar cascades for face and eye detection
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

if faceCascade.empty() or eyeCascade.empty():
    messagebox.showerror("Error", "Failed to load Haar cascades. Check file paths.")
    sys.exit()

# Variables for calibration and monitoring
start_time = None
blink_durations = []
DROWSINESS_THRESHOLD = 1.5
calibration_complete = False
default_calibration_duration = 15
adjusted_calibration_duration = 1
alarm_active = False
monitoring_active = False

#  Function to load and display the logo
def load_logo():
    try:
        logo = Image.open("ddu.jpg").resize((175, 175))
        logo = ImageTk.PhotoImage(logo)
        logo_label.config(image=logo)
        logo_label.image = logo
    except Exception as e:
        messagebox.showerror("Error", f"Logo not found: {e}")

# Function for calibration phase
def calibrate():
    global start_time, calibration_complete, blink_durations, DROWSINESS_THRESHOLD
    cap = cv2.VideoCapture(0)
    calibration_start = time.time()
    calibration_duration = default_calibration_duration

    no_blinks_detected = True

    cv2.namedWindow("Calibration - Face Detection", cv2.WINDOW_NORMAL)

    while True:
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_region = gray[y:y + h, x:x + w]
            eyes = eyeCascade.detectMultiScale(face_region, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10))

            if len(eyes) == 0:
                if start_time is None:
                    start_time = time.time()
                no_blinks_detected = False
            else:
                if start_time is not None:
                    blink_duration = time.time() - start_time
                    blink_durations.append(blink_duration)
                    start_time = None

        elapsed_time = time.time() - calibration_start
        countdown_time = max(0, calibration_duration - int(elapsed_time))
        update_status(f"Calibration in Progress... {countdown_time}s", "blue")
        window.update()

        cv2.imshow("Calibration - Face Detection", img)

        if elapsed_time > calibration_duration:
            break

    cap.release()
    cv2.destroyWindow("Calibration - Face Detection")

    if no_blinks_detected:
        calibration_duration = adjusted_calibration_duration
        messagebox.showwarning("No Blinks Detected", f"No blinks detected. Reducing calibration duration to {calibration_duration} second.")

    if blink_durations:
        avg_blink_duration = sum(blink_durations) / len(blink_durations)
        DROWSINESS_THRESHOLD = avg_blink_duration * 2
        messagebox.showinfo("Calibration Complete", f"Average blink duration: {avg_blink_duration:.2f} seconds.\n"
                                                    f"Drowsiness threshold: {DROWSINESS_THRESHOLD:.2f} seconds.")
    else:
        messagebox.showwarning("Calibration Failed", "No blinks were detected. Using default threshold.")
        DROWSINESS_THRESHOLD = 2.5

    calibration_complete = True
    update_status("Calibration Complete", "green")

#  Function for real-time monitoring
def monitor():
    global start_time, alarm_active, monitoring_active

    if not calibration_complete:
        messagebox.showerror("Error", "Calibration not completed yet!")
        return

    if monitoring_active:
        return

    monitoring_active = True
    cap = cv2.VideoCapture(0)

    while monitoring_active:
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_region = gray[y:y + h, x:x + w]
            eyes = eyeCascade.detectMultiScale(face_region, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10))

            if len(eyes) == 0:
                if start_time is None:
                    start_time = time.time()
                else:
                    elapsed_time = time.time() - start_time
                    if elapsed_time > DROWSINESS_THRESHOLD:
                        #  Trigger the alarm and red border IMMEDIATELY
                        if not alarm_active:
                            alarm_active = True
                            threading.Thread(target=play_alarm).start()
                        
                        #  Show RED BORDER IMMEDIATELY WHEN ALARM STARTS
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 4)
                        cv2.putText(img, "Drowsy", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                        update_status("Drowsiness Detected! Alarm Triggered.", "red")
            else:
                start_time = None
                if alarm_active:
                    stop_alarm()
                    alarm_active = False
                
                #  Show GREEN BORDER when awake
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
                cv2.putText(img, "Awake", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                update_status("Monitoring - Eyes Open", "green")

        cv2.imshow('Drowsiness Monitoring', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    stop_alarm()
    monitoring_active = False

#  Function to update status label
def update_status(message, color):
    status_label.config(text=message, fg=color)

#  Function to exit the application
def exit_app():
    global monitoring_active
    monitoring_active = False
    stop_alarm()
    window.quit()
    window.destroy()
    sys.exit()

#  Tkinter Interface
def create_interface():
    global window, status_label, logo_label
    window = tk.Tk()
    window.title("Drowsiness Detection System")
    window.geometry("1000x700")
    window.config(bg="#f4f4f9")

    logo_label = tk.Label(window, bg="#f4f4f9")
    logo_label.pack(pady=10)
    load_logo()

    tk.Button(window, text="Start Calibration", font=("Arial", 16), width=25, height=2, bg="#4caf50", fg="white", command=calibrate).pack(pady=10)
    tk.Button(window, text="Start Monitoring", font=("Arial", 16), width=25, height=2, bg="#ff9800", fg="white", command=monitor).pack(pady=10)
    tk.Button(window, text="Exit", font=("Arial", 16), width=25, height=2, bg="#f44336", fg="white", command=exit_app).pack(pady=10)

    status_label = tk.Label(window, text="Welcome! Please start calibration.", font=("Arial", 16), fg="blue", bg="#f4f4f9")
    status_label.pack(pady=30)

    window.mainloop()

#  Start GUI
create_interface()
