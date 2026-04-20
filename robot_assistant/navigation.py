import subprocess
import time

def navigate_to(place):
    url = f"https://www.google.com/maps/dir/?api=1&destination={place}"

    process = subprocess.Popen([
        "chromium-browser",
        "--kiosk",
        "--incognito",
        "--noerrdialogs",
        url
    ])

    time.sleep(8)

    process.terminate()
