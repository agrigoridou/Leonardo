from speech import speak
from listener import listen
from navigation import navigate_to
from navigation_info import get_route_info
from utils import extract_place
from gui import RobotGUI
from ai import basic_response
from vision import detect_face

import threading
import time

gui = RobotGUI()

def vision_loop():
    greeted = False

    while True:
        found, direction = detect_face()

        if found and not greeted:
            speak("Γεια σου!")
            greeted = True

        if found:
            print("Follow:", direction)

        time.sleep(2)


def assistant_loop():
    speak("Έτοιμο!")

    while True:
        gui.listening()
        command = listen()

        if not command:
            continue

        # AI RESPONSES
        response, emotion = basic_response(command)

        if response:
            gui.set_emotion(emotion)
            speak(response)
            gui.idle()
            continue

        # NAVIGATION
        if "πήγαινε" in command:
            place = extract_place(command)

            if place:
                gui.set_emotion("happy")

                distance, duration = get_route_info(place)

                if distance and duration:
                    speak(f"Η απόσταση είναι {distance} και θα φτάσεις σε {duration}")

                speak(f"Σε πηγαίνω στο {place}")
                navigate_to(place)

                gui.idle()
            else:
                gui.error()
                speak("Δεν κατάλαβα τον προορισμό")

threading.Thread(target=assistant_loop, daemon=True).start()
threading.Thread(target=vision_loop, daemon=True).start()

gui.run()
