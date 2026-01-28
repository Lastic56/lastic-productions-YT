import os
import sys

# Set environment variable to indicate desktop mode if needed in main.py
os.environ['DESKTOP_TEST_MODE'] = '1'

print("Starting Lastic Productions in Desktop Mode...")
print("Make sure you have installed requirements: pip install -r requirements.txt")

try:
    import main_desktop as main
    main.VideoDownloaderApp().run()
except ImportError as e:
    print(f"Error importing main application: {e}")
except Exception as e:
    print(f"Application crashed: {e}")
