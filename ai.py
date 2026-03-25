# pip install ultralytics vosk sounddevice
# wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
# unzip vosk-model-small-en-us-0.15.zip
#
# TEST
# is there a person in front of you
# follow the person
#
# start robot
# stop robot
# what do you see
#

import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import os
import csv
import threading
import queue
import sounddevice as sd
import vosk
import json
from ultralytics import YOLO
import subprocess

# =========================
# VISION FOUNDATION MODEL
# =========================
model = YOLO("yolov8n.pt")

# =========================
# VOICE SYSTEM
# =========================
command_queue = queue.Queue()
voice_model = vosk.Model("vosk-model-small-en-us-0.15")

def speak(text):
    print("Robot:", text)
    subprocess.run(["espeak", text])

def voice_listener():
    samplerate = 16000
    rec = vosk.KaldiRecognizer(voice_model, samplerate)

    def callback(indata, frames, time_, status):
        if rec.AcceptWaveform(indata):
            result = json.loads(rec.Result())
            if "text" in result:
                command_queue.put(result["text"])

    with sd.RawInputStream(
        samplerate=samplerate,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=callback
    ):
        while True:
            time.sleep(0.1)

threading.Thread(target=voice_listener, daemon=True).start()

# =========================
# GPIO SETUP
# =========================
TRIG = 13
ECHO = 19
LEFT_PWM_PIN = 18
LEFT_DIR_PIN = 17
RIGHT_PWM_PIN = 23
RIGHT_DIR_PIN = 22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.setup(LEFT_PWM_PIN, GPIO.OUT)
GPIO.setup(LEFT_DIR_PIN, GPIO.OUT)
GPIO.setup(RIGHT_PWM_PIN, GPIO.OUT)
GPIO.setup(RIGHT_DIR_PIN, GPIO.OUT)

left_pwm = GPIO.PWM(LEFT_PWM_PIN, 100)
right_pwm = GPIO.PWM(RIGHT_PWM_PIN, 100)

left_pwm.start(0)
right_pwm.start(0)

# =========================
# MOTOR CONTROL
# =========================
def set_motor_speed(left_speed, right_speed):
    GPIO.output(LEFT_DIR_PIN, left_speed >= 0)
    GPIO.output(RIGHT_DIR_PIN, right_speed >= 0)

    left_pwm.ChangeDutyCycle(min(abs(left_speed), 100))
    right_pwm.ChangeDutyCycle(min(abs(right_speed), 100))

def stop_motors():
    left_pwm.ChangeDutyCycle(0)
    right_pwm.ChangeDutyCycle(0)

# =========================
# PID
# =========================
Kp = 0.4
Kd = 0.2
Ki = 0.0

base_speed = 60
last_error = 0
integral = 0

# =========================
# DISTANCE SENSOR
# =========================
def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.01)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    timeout = time.time()
    while GPIO.input(ECHO) == 0:
        if time.time() - timeout > 0.03:
            return 9.99
    start = time.time()

    timeout = time.time()
    while GPIO.input(ECHO) == 1:
        if time.time() - timeout > 0.03:
            return 9.99
    stop = time.time()

    elapsed = stop - start
    distance = (elapsed * 34300) / 2
    return round(distance / 100, 2)

# =========================
# CAMERA
# =========================
cap = cv2.VideoCapture(0)
time.sleep(2)

if not cap.isOpened():
    print("Camera error")
    exit()

robot_running = False

# =========================
# MAIN LOOP
# =========================
try:
    while True:

        ret, frame = cap.read()
        if not ret:
            continue

        # =========================
        # VOICE COMMANDS
        # =========================
        if not command_queue.empty():
            command = command_queue.get()
            print("Voice:", command)

            if "start robot" in command:
                robot_running = True
                speak("Starting robot")

            elif "stop robot" in command:
                robot_running = False
                stop_motors()
                speak("Stopping")

            elif "what do you see" in command:
                speak("Scanning environment")

        # =========================
        # OBJECT DETECTION
        # =========================
        results = model(frame, imgsz=320, conf=0.4)

        detected_objects = []

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]
                detected_objects.append(label)

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.putText(frame,label,(x1,y1-5),
                            cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)

        # =========================
        # LANE FOLLOWING
        # =========================
        if robot_running:

            dist = get_distance()

            if dist < 0.15:
                stop_motors()
                speak("Obstacle detected")
                robot_running = False
            else:

                roi = frame[-200:, :]
                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

                _, binary = cv2.threshold(
                    gray, 100, 255, cv2.THRESH_BINARY_INV
                )

                left = binary[:, :binary.shape[1]//2]
                right = binary[:, binary.shape[1]//2:]

                M_left = cv2.moments(left)
                M_right = cv2.moments(right)

                if M_left["m00"] > 0 and M_right["m00"] > 0:

                    cx_left = int(M_left["m10"]/M_left["m00"])
                    cx_right = int(M_right["m10"]/M_right["m00"]) + binary.shape[1]//2

                    lane_center = (cx_left + cx_right) // 2
                    frame_center = binary.shape[1] // 2

                    error = lane_center - frame_center

                    integral += error
                    derivative = error - last_error

                    correction = Kp*error + Ki*integral + Kd*derivative
                    last_error = error

                    left_speed = base_speed - correction
                    right_speed = base_speed + correction

                    set_motor_speed(left_speed, right_speed)
                else:
                    stop_motors()

        # =========================
        # DISPLAY
        # =========================
        cv2.putText(frame,
                    f"Objects: {', '.join(set(detected_objects[:3]))}",
                    (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0,255,255),
                    2)

        cv2.imshow("AI Robot", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    print("Stopping robot")

finally:
    stop_motors()
    left_pwm.stop()
    right_pwm.stop()
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
