import time
from adafruit_servokit import ServoKit

# Initialize the 16-channel HAT
kit = ServoKit(channels=16)

print("Testing both robot arms...")
print("Press Ctrl+C to stop")

# LEFT ARM (Channels 0-5)
LEFT_GRIPPER  = 0
LEFT_WRIST_P  = 1 # Pitch
LEFT_WRIST_R  = 2 # Rotation
LEFT_ELBOW    = 3
LEFT_SH_LR    = 4 # Shoulder Left/Right
LEFT_SH_FB    = 5 # Shoulder Front/Back

# RIGHT ARM (Channels 6-11)
# Following the same logic starting from 6
RIGHT_GRIPPER = 6
RIGHT_WRIST_P = 7
RIGHT_WRIST_R = 8
RIGHT_ELBOW   = 9
RIGHT_SH_LR   = 10
RIGHT_SH_FB   = 11

ALL_SERVOS = [
    LEFT_GRIPPER, LEFT_WRIST_P, LEFT_WRIST_R, LEFT_ELBOW, LEFT_SH_LR, LEFT_SH_FB,
    RIGHT_GRIPPER, RIGHT_WRIST_P, RIGHT_WRIST_R, RIGHT_ELBOW, RIGHT_SH_LR, RIGHT_SH_FB
]

# Calibration
for ch in ALL_SERVOS:
    kit.servo[ch].set_pulse_width_range(500, 2500)

# Αρχική θέση
def home_position():
    print("Going to home position")
    # Setting middle position (90) for all joints
    for ch in ALL_SERVOS:
        kit.servo[ch].angle = 90
    time.sleep(2)

# Σήκωμα χεριών
def raise_arms():
    print("Raising both arms")

    # Left Arm
    kit.servo[LEFT_SH_FB].angle = 140
    kit.servo[LEFT_ELBOW].angle = 120
    kit.servo[LEFT_WRIST_P].angle = 110

    # Right Arm
    kit.servo[RIGHT_SH_FB].angle = 140
    kit.servo[RIGHT_ELBOW].angle = 120
    kit.servo[RIGHT_WRIST_P].angle = 110

    time.sleep(3)

# Κατέβασμα χεριών
def lower_arms():
    print("Lowering both arms")

    # Left Arm
    kit.servo[LEFT_SH_FB].angle = 90
    kit.servo[LEFT_ELBOW].angle = 90
    kit.servo[LEFT_WRIST_P].angle = 90

    # Right Arm
    kit.servo[RIGHT_SH_FB].angle = 90
    kit.servo[RIGHT_ELBOW].angle = 90
    kit.servo[RIGHT_WRIST_P].angle = 90

    time.sleep(3)

try:
    home_position()

    while True:
        raise_arms()
        lower_arms()

except KeyboardInterrupt:
    print("Test stopped")
    # Optional: move to home before shutting down
    home_position()