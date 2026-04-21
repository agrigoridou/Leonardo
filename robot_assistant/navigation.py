import subprocess
import time
import urllib.parse

def navigate_to(place):

    destination = urllib.parse.quote(place)

    url = (
        f"https://www.google.com/maps/dir/?api=1"
        f"&destination={destination}"
        f"&travelmode=walking"
    )

    process = subprocess.Popen([
        "chromium-browser",
        "--kiosk",
        "--incognito",
        "--noerrdialogs",
        url
    ])

    # δείχνει τον χάρτη για 10 δευτερόλεπτα
    time.sleep(10)

    # κλείνει και επιστρέφει στο face
    process.terminate()
