from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
import numpy as np
from OpenGL.GL import *

class SimpleGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        
    def initializeGL(self):
        glClearColor(0.5, 0.5, 0.5, 1.0)  # Gray background
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        # Draw a simple triangle
        glBegin(GL_TRIANGLES)
        glColor3f(1, 0, 0)
        glVertex2f(-0.5, -0.5)
        glColor3f(0, 1, 0)
        glVertex2f(0.5, -0.5)
        glColor3f(0, 0, 1)
        glVertex2f(0, 0.5)
        glEnd()

class SimpleGLWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple OpenGL Test")
        self.setGeometry(100, 100, 800, 600)
        self.gl_widget = SimpleGLWidget()
        self.setCentralWidget(self.gl_widget)

def main():
    app = QApplication(sys.argv)
    window = SimpleGLWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
