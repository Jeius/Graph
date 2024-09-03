from PyQt5.QtWidgets import QApplication, QWidget 
from graph import MainLayout

# Function to load and apply the stylesheet from a file
def load_stylesheet(file_name):
    with open(file_name, "r") as file:
        stylesheet = file.read()
    return stylesheet



if __name__ == "__main__":
    app = QApplication([])
    main_window = QWidget()
    main_window.setGeometry(100, 100, 1280, 720)
    main_window.setWindowTitle("Graph Illustrator by Julius Pahama")
    main_window.setLayout(MainLayout().main_layout)
    main_window.setStyleSheet(load_stylesheet("style/dark_mode.css"))

    main_window.show()

    app.exec_()