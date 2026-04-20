from speech import speak
from listener import listen
from navigation import navigate_to
from utils import extract_place
from gui import RobotGUI
import threading
import time

gui = RobotGUI()

def assistant_loop():
    speak("Γεια σου! Πες μου που θέλεις να πας")

    while True:
        gui.listening()
        command = listen()

        if not command:
            gui.error()
            continue

        if "πήγαινε" in command:
            place = extract_place(command)

            if place:
                gui.talking()
                speak(f"Σε πηγαίνω στο {place}")
                time.sleep(1)
                navigate_to(place)
                gui.idle()
            else:
                gui.error()
                speak("Δεν κατάλαβα τον προορισμό")

        else:
            gui.error()
            speak("Δεν κατάλαβα την εντολή")

threading.Thread(target=assistant_loop, daemon=True).start()
gui.run()
