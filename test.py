import time
from adafruit_servokit import ServoKit

# Initialize the 16-channel HAT
kit = ServoKit(channels=16)

print("Testing both robot arms...")
print("Press Ctrl+C to stop")

# LEFT ARM
LEFT_GRIPPER = 0
LEFT_WRIST = 1
LEFT_ELBOW = 2
LEFT_SHOULDER = 3
LEFT_UPPER = 4
LEFT_BASE = 5

# RIGHT ARM
RIGHT_GRIPPER = 6
RIGHT_WRIST = 7
RIGHT_ELBOW = 8
RIGHT_SHOULDER = 9
RIGHT_UPPER = 10
RIGHT_BASE = 11

ALL_SERVOS = [
    LEFT_GRIPPER, LEFT_WRIST, LEFT_ELBOW, LEFT_SHOULDER, LEFT_UPPER, LEFT_BASE,
    RIGHT_GRIPPER, RIGHT_WRIST, RIGHT_ELBOW, RIGHT_SHOULDER, RIGHT_UPPER, RIGHT_BASE
]

# Calibration
for ch in ALL_SERVOS:
    kit.servo[ch].set_pulse_width_range(500, 2500)

# Αρχική θέση
def home_position():
    print("Going to home position")
    for ch in ALL_SERVOS:
        kit.servo[ch].angle = 90
    time.sleep(2)

# Σήκωμα χεριών
def raise_arms():
    print("Raising both arms")

    kit.servo[LEFT_SHOULDER].angle = 140
    kit.servo[LEFT_ELBOW].angle = 120
    kit.servo[LEFT_WRIST].angle = 110

    kit.servo[RIGHT_SHOULDER].angle = 140
    kit.servo[RIGHT_ELBOW].angle = 120
    kit.servo[RIGHT_WRIST].angle = 110

    time.sleep(3)

# Κατέβασμα χεριών
def lower_arms():
    print("Lowering both arms")

    kit.servo[LEFT_SHOULDER].angle = 90
    kit.servo[LEFT_ELBOW].angle = 90
    kit.servo[LEFT_WRIST].angle = 90

    kit.servo[RIGHT_SHOULDER].angle = 90
    kit.servo[RIGHT_ELBOW].angle = 90
    kit.servo[RIGHT_WRIST].angle = 90

    time.sleep(3)


try:
    home_position()

    while True:
        raise_arms()
        lower_arms()

except KeyboardInterrupt:
    print("Test stopped")
