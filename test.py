import time
from adafruit_servokit import ServoKit

# Initialize the 16-channel HAT
kit = ServoKit(channels=16)

print("Starting servo test on Channel 6...")
print("Press Ctrl+C to stop.")


#left
#channel 0 = griper
#chanel 1-5 apo kato pros ta pano(karpos -omos)

#right
#channel 6 = griper
#chanel 7-11 apo kato pros ta pano(karpos -omos)
kit.servo[0].angle = 180
time.sleep(5) # Gives the arm time to move
kit.servo[0].angle = 0
time.sleep(5)


    
