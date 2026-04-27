import os
import threading
import time
import random

from speech import speak
from listener import listen
from navigation import navigate_to
from utils import extract_place
from gui import RobotGUI
from ai import basic_response
from vision import detect_face

gui = RobotGUI()

# Αυτό κλειδώνει τη φωνή ώστε να μην διακόπτεται
is_speaking = False 

def safe_speak(text):
    global is_speaking
    is_speaking = True
    speak(text)
    is_speaking = False

def vision_loop():
    greeted = False
    waved = False

    hello_options = ["Γεια σου!", "Σε βλέπω!", "Γεια χαρά!"]
    wave_options = ["Καλώς ήρθες!", "Γεια σου και σε σένα!", "Χαίρομαι που σε βλέπω!", "Έλα, γεια!"]

    while True:
        found, dx, dy, is_waving = detect_face()

        # Αν σε δει πρώτη φορά, μιλάει ΜΟΝΟ αν δεν διαβάζει ήδη κάτι
        if found and not greeted:
            if not is_speaking:
                safe_speak(random.choice(hello_options))
            greeted = True

        if found:
            gui.set_eye_target(True, dx, dy)
            
            # Αν του κουνήσεις το χέρι, μιλάει ΜΟΝΟ αν δεν διαβάζει κάτι
            if is_waving and not waved:
                gui.set_emotion("happy")
                if not is_speaking:
                    safe_speak(random.choice(wave_options))
                waved = True
        else:
            gui.set_eye_target(False, 0, 0)
            waved = False 

        time.sleep(0.3) 

def assistant_loop():
    safe_speak("Έτοιμο!")

    while True:
        gui.listening()
        command = listen()

        if not command:
            gui.idle()
            continue

        response, emotion = basic_response(command)

        if response:
            gui.set_emotion(emotion)
            # Διαβάζει το μεγάλο κείμενο και κλειδώνει τη φωνή
            safe_speak(response)
            gui.idle()
            continue

        if "επιστροφή" in command or "κλείσε" in command:
            gui.set_emotion("talking")
            safe_speak("Επιστρέφω στην οθόνη")
            
            os.system("pkill chromium")
            os.system("pkill chromium-browser")
            
            gui.root.after(0, gui.bring_to_front)
            gui.idle()
            continue

        if "πήγαινε" in command:
            place = extract_place(command)

            if place:
                gui.set_emotion("happy")
                safe_speak(f"Σε πηγαίνω στο {place}")
                
                gui.root.after(0, gui.root.withdraw)
                navigate_to(place)
                gui.idle()
            else:
                gui.error()
                safe_speak("Δεν κατάλαβα τον προορισμό")
                gui.idle()
            continue

threading.Thread(target=assistant_loop, daemon=True).start()
threading.Thread(target=vision_loop, daemon=True).start()

gui.run()
