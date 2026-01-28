import os
from kivy.config import Config

# --- SIMULATE MOBILE SCREEN ---
# Standard mobile resolution (approx 9:19 ratio)
WIDTH = 360
HEIGHT = 740

Config.set('graphics', 'width', str(WIDTH))
Config.set('graphics', 'height', str(HEIGHT))
Config.set('graphics', 'resizable', '0') # Fix size for simulation

import main

if __name__ == '__main__':
    print(f"Starting Lastic Productions MOBILE SIMULATOR ({WIDTH}x{HEIGHT})...")
    main.MobileDownloaderApp().run()
