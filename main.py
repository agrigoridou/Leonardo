# -*- coding: utf-8 -*-
from gui import RobotGUI

if __name__ == "__main__":
    # Το GUI διαχειρίζεται πλέον εσωτερικά το speech_loop
    gui = RobotGUI()
    gui.run()