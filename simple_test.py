from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
import sys

class SimpleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Test")
        self.setGeometry(100, 100, 400, 300)
        label = QLabel("Hello, PyQt6 is working!", self)
        label.setGeometry(100, 100, 200, 50)

def main():
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
