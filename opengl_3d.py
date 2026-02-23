from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QHBoxLayout
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QKeyEvent, QMouseEvent, QWheelEvent
import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from src.core.physics import rk4_step, Body

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, bodies):
        super().__init__()
        self.bodies = bodies
        self.scale = 1.0  # Scale factor for projection
        self.trails = [[] for _ in bodies]
        self.max_trail_length = 500
        self.offset_x = 0
        self.offset_y = 0
        self.last_mouse_pos = None
        self.rotation_x = 0
        self.rotation_y = 0
        
    def initializeGL(self):
        print("initializeGL called")
        glClearColor(1, 1, 1, 1)  # Bright white background
        glEnable(GL_POINT_SMOOTH)
        glPointSize(10.0)
        
        # Set orthographic projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-300, 300, -300, 300, -1000, 1000)
        glMatrixMode(GL_MODELVIEW)
        
        # Enable lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        light_pos = [100, 100, 100, 1]
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        
        # Create quadric for spheres
        self.quadric = gluNewQuadric()
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(self.offset_x, self.offset_y, -5)  # Move camera back
        glRotatef(self.rotation_x, 1, 0, 0)  # Rotate around X axis
        glRotatef(self.rotation_y, 0, 1, 0)  # Rotate around Y axis
        
        # Enable blending for transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Disable lighting for planes
        glDisable(GL_LIGHTING)
        
        # Draw XY plane (z=0)
        glColor4f(0.5, 0.5, 0.5, 0.2)
        glBegin(GL_QUADS)
        glVertex3f(-300, -300, 0)
        glVertex3f(300, -300, 0)
        glVertex3f(300, 300, 0)
        glVertex3f(-300, 300, 0)
        glEnd()
        
        # Draw XZ plane (y=0)
        glColor4f(0.5, 0.5, 0.5, 0.2)
        glBegin(GL_QUADS)
        glVertex3f(-300, 0, -300)
        glVertex3f(300, 0, -300)
        glVertex3f(300, 0, 300)
        glVertex3f(-300, 0, 300)
        glEnd()
        
        # Draw YZ plane (x=0)
        glColor4f(0.5, 0.5, 0.5, 0.2)
        glBegin(GL_QUADS)
        glVertex3f(0, -300, -300)
        glVertex3f(0, 300, -300)
        glVertex3f(0, 300, 300)
        glVertex3f(0, -300, 300)
        glEnd()
        
        # Re-enable lighting
        glEnable(GL_LIGHTING)
        glDisable(GL_BLEND)
        
        # Draw axis lines
        glDisable(GL_LIGHTING)
        glLineWidth(3.0)
        glBegin(GL_LINES)
        # X axis red
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(200, 0, 0)
        # Y axis green
        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 200, 0)
        # Z axis blue
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 200)
        glEnd()
        glEnable(GL_LIGHTING)
        
        # Draw a colored triangle to verify rendering
        glBegin(GL_TRIANGLES)
        glColor3f(1, 0, 0)
        glVertex3f(-1, -1, 0)
        glColor3f(0, 1, 0)
        glVertex3f(1, -1, 0)
        glColor3f(0, 0, 1)
        glVertex3f(0, 1, 0)
        glEnd()
        
        # Draw trails
        glDisable(GL_LIGHTING)
        glLineWidth(1.0)
        for i, trail in enumerate(self.trails):
            if len(trail) > 1:
                glBegin(GL_LINE_STRIP)
                for pos in trail:
                    glColor3f(0.2, 0.2, 0.2)  # Dark gray trails on white background
                    glVertex3f(pos[0] * self.scale, pos[1] * self.scale, pos[2] * self.scale)
                glEnd()
        glEnable(GL_LIGHTING)
        
        # Draw bodies as spheres with lighting
        for i, body in enumerate(self.bodies):
            x, y, z = body.pos * self.scale
            glPushMatrix()
            glTranslatef(x, y, z)
            colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]  # Red, Green, Blue
            glMaterialfv(GL_FRONT, GL_DIFFUSE, colors[i] + (1,))
            gluSphere(self.quadric, 5, 10, 10)
            glPopMatrix()
            # Update trail
            self.trails[i].append(body.pos.copy())
            if len(self.trails[i]) > self.max_trail_length:
                self.trails[i].pop(0)
    
    def mousePressEvent(self, event: QMouseEvent):
        self.last_mouse_pos = event.position()
        
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.last_mouse_pos:
            dx = event.position().x() - self.last_mouse_pos.x()
            dy = event.position().y() - self.last_mouse_pos.y()
            
            if event.buttons().value & 1:  # Left button - rotate
                self.rotation_y += dx * 0.5
                self.rotation_x += dy * 0.5
            elif event.buttons().value & 4:  # Middle button - pan
                self.offset_x += dx * 0.01
                self.offset_y -= dy * 0.01
            elif event.buttons().value & 2:  # Right button - zoom
                if dy > 0:
                    self.scale /= 1.1
                else:
                    self.scale *= 1.1
                    
            self.last_mouse_pos = event.position()
            self.update()
            
    def wheelEvent(self, event: QWheelEvent):
        # Mouse wheel zoom
        if event.angleDelta().y() > 0:
            self.scale *= 1.1
        else:
            self.scale /= 1.1
        self.update()
            
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == 82:  # R - reset
            self.scale = 0.01
            self.offset_x = 0
            self.offset_y = 0
            self.rotation_x = 0
            self.rotation_y = 0
            self.trails = [[] for _ in self.bodies]
            self.update()

class OpenGLWindow(QMainWindow):
    def __init__(self, bodies):
        super().__init__()
        self.bodies = bodies
        self.time_scale = 1.0
        self.setWindowTitle("OpenGL Three-Body Simulation")
        self.setGeometry(100, 100, 1000, 600)
        
        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        central_widget.setLayout(layout)
        
        # GL widget
        self.gl_widget = OpenGLWidget(bodies)
        layout.addWidget(self.gl_widget, 3)  # Stretch factor 3
        
        # Control panel
        control_panel = QWidget()
        control_layout = QVBoxLayout()
        control_panel.setLayout(control_layout)
        
        # Reset button
        reset_button = QPushButton("Reset Simulation")
        reset_button.clicked.connect(self.reset_simulation)
        control_layout.addWidget(reset_button)
        
        # Time scale label
        time_label = QLabel("Time Scale")
        control_layout.addWidget(time_label)
        
        # Time scale slider
        self.time_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_slider.setRange(1, 100)
        self.time_slider.setValue(10)
        self.time_slider.valueChanged.connect(self.set_time_scale)
        control_layout.addWidget(self.time_slider)
        
        # FPS label
        self.fps_label = QLabel("FPS: 0")
        control_layout.addWidget(self.fps_label)
        
        # Coordinate label
        self.coord_label = QLabel("Pos: (0.0, 0.0, 0.0)")
        control_layout.addWidget(self.coord_label)
        
        # Full screen button
        fullscreen_button = QPushButton("Full Screen")
        fullscreen_button.clicked.connect(self.toggle_fullscreen)
        control_layout.addWidget(fullscreen_button)
        
        layout.addWidget(control_panel, 1)  # Stretch factor 1
        
        # FPS timer
        self.fps_timer = QTimer()
        self.fps_timer.timeout.connect(self.update_fps)
        self.fps_timer.start(1000)
        self.frame_count = 0
        
        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)  # ~60 FPS
        
    def update_simulation(self):
        rk4_step(self.bodies, 0.01 * self.time_scale)
        self.frame_count += 1
        self.gl_widget.update()
        # Update coordinates
        pos = self.bodies[0].pos
        self.coord_label.setText(f"Pos: ({pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f})")

    def update_fps(self):
        fps = self.frame_count
        self.fps_label.setText(f"FPS: {fps}")
        self.frame_count = 0

    def reset_simulation(self):
        self.bodies = [
            Body(100, [0, 100, 0], [10, 0, 0]),
            Body(102, [100, 0, 0], [12, 0, 0]),
            Body(104, [0, 0, 100], [14, 0, 0])
        ]
        self.gl_widget.bodies = self.bodies
        self.gl_widget.scale = 1.0
        self.gl_widget.offset_x = 0
        self.gl_widget.offset_y = 0
        self.gl_widget.rotation_x = 0
        self.gl_widget.rotation_y = 0
        self.gl_widget.trails = [[] for _ in self.bodies]
        self.time_scale = 1.0
        self.time_slider.setValue(10)
        self.gl_widget.update()

    def set_time_scale(self, value):
        self.time_scale = value / 10.0

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

def main():
    print("App starting")
    bodies = [
        Body(100, [50, 50, 10], [20, 10, 5]),
        Body(102, [100, 50, 20], [15, 20, 10]),
        Body(104, [50, 100, 30], [10, 15, 20])
    ]
    app = QApplication(sys.argv)
    print("QApplication created")
    window = OpenGLWindow(bodies)
    print("Window created")
    window.show()
    print("Window shown")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
