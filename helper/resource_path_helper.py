import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller's temp folder."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Specify the path to chromedriver.exe
# chromedriver_path = resource_path(os.path.join("drivers", "chromedriver.exe"))
# print(chromedriver_path)