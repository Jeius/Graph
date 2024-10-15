import sys
import os
from PyQt5 import QtGui, QtWidgets

from graph.gui.ui_main_window import UI_MainWindow

def loadStylesheet(path):
    if getattr(sys, 'frozen', False):  
        base_path = sys._MEIPASS  
    else:
        base_path = os.path.dirname(__file__)  

    file_path = os.path.join(base_path, path)

    with open(file_path, "r") as file:
        stylesheet = file.read()
    return stylesheet

def loadIcon(path):
    if getattr(sys, 'frozen', False):  
        base_path = sys._MEIPASS  
    else:
        base_path = os.path.dirname(__file__)  

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