import sys
import os
from PyQt5 import QtGui, QtWidgets

from graph.gui.ui_main_window import UI_MainWindow

# Function to load and apply the stylesheet from a file
def loadStylesheet(path):
     # Determine if the application is running as a script or as a bundled executable
    if getattr(sys, 'frozen', False):  # Check if we're in a PyInstaller bundle
        base_path = sys._MEIPASS  # Temporary folder used by PyInstaller
    else:
        base_path = os.path.dirname(__file__)  # Directory of the script

    # Construct the full path to the stylesheet file
    file_path = os.path.join(base_path, path)

    # Open and read the stylesheet
    with open(file_path, "r") as file:
        stylesheet = file.read()

    return stylesheet

def loadIcon(path):
     # Determine if the application is running as a script or as a bundled executable
    if getattr(sys, 'frozen', False):  # Check if we're in a PyInstaller bundle
        base_path = sys._MEIPASS  # Temporary folder used by PyInstaller
    else:
        base_path = os.path.dirname(__file__)  # Directory of the script

    # Construct the full path to the icon
    file_path = os.path.join(base_path, path)

    return QtGui.QIcon(file_path)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = QtWidgets.QMainWindow()
    main_window.resize(1420, 820)
    main_window.setWindowTitle("Graph Illustrator by Julius Pahama")
    main_window.setStyleSheet(loadStylesheet("style/globals.css"))
    main_window.setWindowIcon(loadIcon("icon.webp"))

    ui = UI_MainWindow(main_window)
    main_window.show()

    app.exec_()