from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QTimer
from src.renderer.gl_widget import GLWidget
from src.core.physics import rk4_step

class MainWindow(QMainWindow):
    def __init__(self, bodies):
        super().__init__()
        self.bodies = bodies
        self.time_scale = 1.0
        self.setWindowTitle("Three-Body Simulation")
        self.setGeometry(100, 100, 800, 600)
        self.gl_widget = GLWidget(bodies)
        self.setCentralWidget(self.gl_widget)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)  # ~60 FPS

    def update_simulation(self):
        rk4_step(self.bodies, 0.01 * self.time_scale)
        self.gl_widget.update()
