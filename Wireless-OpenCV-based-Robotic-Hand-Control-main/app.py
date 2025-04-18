import cv2
import mediapipe as mp
import numpy as np
import math
import csv
import os
import datetime
import tkinter as tk
from tkinter import filedialog
import Connect_to_esp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Function to remap values
def remap(value, in_min, in_max, out_min, out_max):
    if out_min < out_max:
        remapped_Value = out_min + (float(value - in_min) / float(in_max - in_min) * (out_max - out_min))
    else:
        remapped_Value = out_max + (float(value - in_min) / float(in_max - in_min) * (out_min - out_max))
    
    return max(min(remapped_Value, max(out_min, out_max)), min(out_min, out_max))

# Function to initialize the camera
def initialize_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return None
    return cap

# Function to calculate angle between vectors
def calculate_angle(v1, v2):
    dot_product = np.dot(v1, v2)
    magnitude_v1 = np.linalg.norm(v1)
    magnitude_v2 = np.linalg.norm(v2)
    if magnitude_v1 * magnitude_v2 == 0:
        return 0
    return math.degrees(math.acos(dot_product / (magnitude_v1 * magnitude_v2)))

# Function to get finger joint angles
def get_joint_angles(hand_landmarks):
    joint_indices = {
        'thumb': [2, 3, 4],
        'index': [5, 6, 8],
        'middle': [9, 10, 12],
        'ring': [13, 14, 16],
        'pinky': [17, 18, 20]
    }
    
    joint_angles = {}
    for finger, indices in joint_indices.items():
        base = np.array([hand_landmarks[indices[0]].x, hand_landmarks[indices[0]].y])
        middle = np.array([hand_landmarks[indices[1]].x, hand_landmarks[indices[1]].y])
        tip = np.array([hand_landmarks[indices[2]].x, hand_landmarks[indices[2]].y])
        
        vector1 = middle - base
        vector2 = tip - middle
        angle = calculate_angle(vector1, vector2)
        joint_angles[finger] = angle
    
    return joint_angles

# Function for Replay Mode
def replay_mode():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a Recorded Session File",
        filetypes=[("CSV Files", "*.csv")],
        initialdir="recorded_sessions"
    )

    if not file_path:
        print("No file selected.")
        return

    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                servo_angles = list(map(float, row))
                Connect_to_esp.set_servo_angles('192.168.114.31', servo_angles)
                print(f"Performing action: {servo_angles}")
                cv2.waitKey(500)  
        print("Session completed.")
    except Exception as e:
        print(f"Error reading file: {e}")

# Main function
def main():
    cap = initialize_camera()
    if cap is None:
        return

    mode = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        # Display mode selection on camera window
        cv2.putText(frame, "Select Mode:", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, "1: Live Mode", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, "2: Replay Mode", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, "Press 'q' to Quit", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Mode Selection", frame)
        
        key = cv2.waitKey(0) & 0xFF
        if key == ord('1'):
            mode = "live"
            break
        elif key == ord('2'):
            mode = "replay"
            break
        elif key == ord('q'):  # Quit on 'q' press
            cap.release()
            cv2.destroyAllWindows()
            return

    cv2.destroyWindow("Mode Selection")

    if mode == "live":
        live_mode(cap)
    elif mode == "replay":
        replay_mode()

    cap.release()
    cv2.destroyAllWindows()

# Function for Live Mode
def live_mode(cap):
    os.makedirs("recorded_sessions", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recorded_sessions/Session_{timestamp}.csv"
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Index", "Ring", "Middle", "Thumb", "Pinky"])

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    joint_angles = get_joint_angles(hand_landmarks.landmark)
                    
                    index = remap(joint_angles['index'], 5, 140, 0, 150)
                    ring = remap(joint_angles['ring'], 5, 130, 0, 150)
                    middle = remap(joint_angles['middle'], 5, 130, 0, 150)
                    thumb = remap(joint_angles['thumb'], 5, 130, 0, 150)
                    pinky = remap(joint_angles['pinky'], 5, 130, 0, 150)
                    
                    servoangles = [index, ring, middle, thumb, pinky]
                    Connect_to_esp.set_servo_angles('192.168.114.31', servoangles)
                    writer.writerow(servoangles)
                    print(servoangles)

            cv2.imshow('Live Mode - Hand Tracking', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    print(f"Session saved: {filename}")

# Run the program
if __name__ == "__main__":
    main()
