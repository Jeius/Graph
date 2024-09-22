import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget 
from PyQt5 import QtCore, QtGui, QtWidgets

from graph.gui.ui_main_window import UI_MainWindow

# Function to load and apply the stylesheet from a file
def load_stylesheet(file_name):
     # Determine if the application is running as a script or as a bundled executable
    if getattr(sys, 'frozen', False):  # Check if we're in a PyInstaller bundle
        base_path = sys._MEIPASS  # Temporary folder used by PyInstaller
    else:
        base_path = os.path.dirname(__file__)  # Directory of the script

    # Construct the full path to the stylesheet file
    file_path = os.path.join(base_path, file_name)

    # Open and read the stylesheet
    with open(file_path, "r") as file:
        stylesheet = file.read()

    return stylesheet


if __name__ == "__main__":
    app = QApplication([])
    main_window = QtWidgets.QMainWindow()
    main_window.setGeometry(100, 100, 1280, 720)
    main_window.setWindowTitle("Graph Illustrator by Julius Pahama")
    main_window.setStyleSheet(load_stylesheet("style/globals.css"))

    ui = UI_MainWindow(main_window)
    main_window.show()

    app.exec_()