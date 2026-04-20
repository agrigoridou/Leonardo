# -*- coding: utf-8 -*-
import subprocess
import time

def navigate_to(place):
    url = f"https://www.google.com/maps/search/{place}"

    process = subprocess.Popen([
        "chromium", # Ή chromium-browser αν είσαι σε παλιότερο λειτουργικό
        "--kiosk",
        "--incognito",
        "--noerrdialogs",
        url
    ])

    time.sleep(8)
    process.terminate()