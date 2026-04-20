import os

def navigate_to(place):
    url = f"https://www.google.com/maps/dir/?api=1&destination={place}"
    os.system(f'chromium-browser --kiosk "{url}"')
