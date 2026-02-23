from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QHBoxLayout, QDialog, QFormLayout, QDoubleSpinBox, QGroupBox, QDialogButtonBox, QSpinBox, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QKeyEvent, QMouseEvent, QWheelEvent
import sys
import numpy as np
import csv
import json
import logging
from OpenGL.GL import *
from OpenGL.GLU import *
from src.core.physics import rk4_step, Body

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, bodies, radii):
        super().__init__()
        self.bodies = bodies
        self.scale = 1.0  # Scale factor for projection
        self.trails = [[] for _ in bodies]
        self.max_trail_length = 2000
        self.offset_x = 0
        self.offset_y = 0
        self.last_mouse_pos = None
        self.rotation_x = 20  # Initial 3D tilt
        self.rotation_y = 30  # Initial 3D rotation
        self.rotation_z = 10
        self.offset_z = 0
        self.selected_body = -1
        self.radii = radii
        
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
        light_pos = [0, 0, -100, 1]  # From viewing direction, illuminating objects
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        # Add ambient lighting
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.3, 0.3, 0.3, 1])
        
        # Create quadric for spheres
        self.quadric = gluNewQuadric()
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(self.offset_x, self.offset_y, self.offset_z)  # Move camera back
        glRotatef(self.rotation_x, 1, 0, 0)  # Rotate around X axis
        glRotatef(self.rotation_y, 0, 1, 0)  # Rotate around Y axis
        glRotatef(self.rotation_z, 0, 0, 1)  # Rotate around Z axis
        
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
        glVertex3f(200 * self.scale, 0, 0)
        # Y axis green
        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 200 * self.scale, 0)
        # Z axis blue
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 200 * self.scale)
        glEnd()
        
        # Draw grid lines on XY plane
        glLineWidth(1.5)
        glColor4f(0.4, 0.4, 0.4, 0.6)
        for x in range(-500, 501, 50):
            glBegin(GL_LINES)
            glVertex3f(x * self.scale, -500 * self.scale, 0)
            glVertex3f(x * self.scale, 500 * self.scale, 0)
            glEnd()
        for y in range(-500, 501, 50):
            glBegin(GL_LINES)
            glVertex3f(-500 * self.scale, y * self.scale, 0)
            glVertex3f(500 * self.scale, y * self.scale, 0)
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
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glLineWidth(2.0)
        colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]  # Red, Green, Blue
        for i, trail in enumerate(self.trails):
            if len(trail) > 1:
                glBegin(GL_LINE_STRIP)
                for pos in trail:
                    glColor4f(colors[i % len(colors)][0], colors[i % len(colors)][1], colors[i % len(colors)][2], 0.7)
                    glVertex3f(pos[0] * self.scale, pos[1] * self.scale, pos[2] * self.scale)
                glEnd()
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        
        # Draw bodies as spheres with lighting
        for i, body in enumerate(self.bodies):
            x, y, z = body.pos * self.scale
            glPushMatrix()
            glTranslatef(x, y, z)
            colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]  # Red, Green, Blue
            glMaterialfv(GL_FRONT, GL_DIFFUSE, colors[i % len(colors)] + (1,))
            gluSphere(self.quadric, self.radii[i], 20, 20)
            glPopMatrix()
            # Update trail
            self.trails[i].append(body.pos.copy())
            if len(self.trails[i]) > self.max_trail_length:
                self.trails[i].pop(0)
    
    def mousePressEvent(self, event: QMouseEvent):
        self.last_mouse_pos = event.position()
        
        # Object selection on left click without modifiers
        if event.button() == 1 and not event.modifiers():
            self.selected_body = (self.selected_body + 1) % len(self.bodies)
            logging.info("Selected body: %d", self.selected_body)
        
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.last_mouse_pos:
            dx = event.position().x() - self.last_mouse_pos.x()
            dy = event.position().y() - self.last_mouse_pos.y()
            
            if event.buttons().value & 1:  # Left button
                modifiers = event.modifiers()
                if modifiers & Qt.KeyboardModifier.ShiftModifier:
                    # Pan (move coordinate system)
                    self.offset_x += dx * 0.01
                    self.offset_y -= dy * 0.01
                elif modifiers & Qt.KeyboardModifier.ControlModifier:
                    # Zoom
                    if dy > 0:
                        self.scale /= 1.1
                    else:
                        self.scale *= 1.1
                elif modifiers & Qt.KeyboardModifier.AltModifier:
                    # Rotate around Z axis
                    self.rotation_z += dx * 0.5
                else:
                    # Rotate around X and Y axes
                    self.rotation_y += dx * 0.5
                    self.rotation_x += dy * 0.5
                    
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
        self.bodies_data = [
            {'mass': 50, 'radius': 2.5, 'pos': [50, 50, 10], 'vel': [20, 10, 5]},
            {'mass': 100, 'radius': 5, 'pos': [100, 50, 20], 'vel': [15, 20, 10]},
            {'mass': 200, 'radius': 10, 'pos': [50, 100, 30], 'vel': [10, 15, 20]}
        ]
        self.radii = [d['radius'] for d in self.bodies_data]
        self.setWindowTitle("OpenGL Three-Body Simulation")
        self.setGeometry(100, 100, 1000, 600)
        
        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        central_widget.setLayout(layout)
        
        # GL widget
        self.gl_widget = OpenGLWidget(bodies, self.radii)
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
        
        # Selected body label
        self.selected_label = QLabel("Selected Body: None")
        control_layout.addWidget(self.selected_label)
        
        # Full screen button
        fullscreen_button = QPushButton("Full Screen")
        fullscreen_button.clicked.connect(self.toggle_fullscreen)
        control_layout.addWidget(fullscreen_button)
        
        # Settings button
        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.open_settings)
        control_layout.addWidget(settings_button)
        
        # Export Data button
        export_button = QPushButton("Export Data")
        export_button.clicked.connect(self.export_data)
        control_layout.addWidget(export_button)
        
        # Save Config button
        save_button = QPushButton("Save Config")
        save_button.clicked.connect(self.save_config)
        control_layout.addWidget(save_button)
        
        # Load Config button
        load_button = QPushButton("Load Config")
        load_button.clicked.connect(self.load_config)
        control_layout.addWidget(load_button)
        
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
        
        # Update selected body info
        if self.gl_widget.selected_body >= 0:
            body = self.bodies[self.gl_widget.selected_body]
            info = f"Selected Body {self.gl_widget.selected_body}: Mass {body.mass:.1f}, Pos ({body.pos[0]:.1f}, {body.pos[1]:.1f}, {body.pos[2]:.1f}), Vel ({body.vel[0]:.1f}, {body.vel[1]:.1f}, {body.vel[2]:.1f})"
            self.selected_label.setText(info)
        else:
            self.selected_label.setText("Selected Body: None")

    def update_fps(self):
        fps = self.frame_count
        self.fps_label.setText(f"FPS: {fps}")
        self.frame_count = 0

    def reset_simulation(self):
        logging.info("Simulation reset")
        self.bodies = [Body(d['mass'], d['pos'], d['vel']) for d in self.bodies_data]
        self.gl_widget.bodies = self.bodies
        self.gl_widget.radii = self.radii
        self.gl_widget.scale = 1.0
        self.gl_widget.offset_x = 0
        self.gl_widget.offset_y = 0
        self.gl_widget.offset_z = 0
        self.gl_widget.rotation_x = 20  # Reset to 3D view
        self.gl_widget.rotation_y = 30  # Reset to 3D view
        self.gl_widget.rotation_z = 10
        self.gl_widget.trails = [[] for _ in self.bodies]
        self.time_scale = 1.0
        self.time_slider.setValue(10)
        self.gl_widget.update()

    def set_time_scale(self, value):
        self.time_scale = value / 10.0
        logging.info("Time scale changed to %.2f", self.time_scale)

    def toggle_fullscreen(self):
        logging.info("Full screen toggled")
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def open_settings(self):
        logging.info("Settings dialog opened")
        dialog = SettingsDialog(self.bodies_data, self)
        if dialog.exec():
            self.bodies_data = dialog.get_data()
            self.radii = [d['radius'] for d in self.bodies_data]
            self.reset_simulation()

    def export_data(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export Data", "", "CSV Files (*.csv)")
        if filename:
            try:
                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Body ID', 'Mass', 'Radius', 'Pos X', 'Pos Y', 'Pos Z', 'Vel X', 'Vel Y', 'Vel Z'])
                    for i, body in enumerate(self.bodies):
                        writer.writerow([i, body.mass, self.radii[i], body.pos[0], body.pos[1], body.pos[2], body.vel[0], body.vel[1], body.vel[2]])
                QMessageBox.information(self, "Export Successful", f"Data exported to {filename}")
                logging.info("Data exported to %s", filename)
            except Exception as e:
                QMessageBox.warning(self, "Export Failed", str(e))
                logging.error("Data export failed: %s", str(e))

    def save_config(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Config", "", "JSON Files (*.json)")
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.bodies_data, f, indent=4)
                QMessageBox.information(self, "Save Successful", f"Config saved to {filename}")
                logging.info("Config saved to %s", filename)
            except Exception as e:
                QMessageBox.warning(self, "Save Failed", str(e))
                logging.error("Config save failed: %s", str(e))

    def load_config(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Config", "", "JSON Files (*.json)")
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.bodies_data = json.load(f)
                self.radii = [d['radius'] for d in self.bodies_data]
                self.reset_simulation()
                QMessageBox.information(self, "Load Successful", f"Config loaded from {filename}")
                logging.info("Config loaded from %s", filename)
            except Exception as e:
                QMessageBox.warning(self, "Load Failed", str(e))
                logging.error("Config load failed: %s", str(e))

class SettingsDialog(QDialog):
    def __init__(self, bodies_data, parent=None):
        super().__init__(parent)
        self.bodies_data = bodies_data.copy()
        self.setWindowTitle("Simulation Settings")
        self.resize(800, 600)  # Better default size
        
        # Predefined defaults for new bodies
        self.defaults = [
            {'mass': 100, 'radius': 5, 'pos': [50, 50, 10], 'vel': [20, 10, 5]},
            {'mass': 102, 'radius': 5, 'pos': [100, 50, 20], 'vel': [15, 20, 10]},
            {'mass': 104, 'radius': 5, 'pos': [50, 100, 30], 'vel': [10, 15, 20]},
            {'mass': 106, 'radius': 5, 'pos': [150, 50, 40], 'vel': [25, 5, 15]},
            {'mass': 108, 'radius': 5, 'pos': [100, 150, 50], 'vel': [5, 25, 10]},
            {'mass': 110, 'radius': 5, 'pos': [200, 100, 60], 'vel': [20, 15, 25]},
            {'mass': 112, 'radius': 5, 'pos': [150, 200, 70], 'vel': [15, 20, 30]},
            {'mass': 114, 'radius': 5, 'pos': [250, 150, 80], 'vel': [30, 10, 20]},
            {'mass': 116, 'radius': 5, 'pos': [200, 250, 90], 'vel': [10, 30, 15]},
            {'mass': 118, 'radius': 5, 'pos': [300, 200, 100], 'vel': [25, 25, 35]},
        ]
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Configure initial conditions for celestial bodies in the gravitational simulation."))
        
        self.num_bodies_spin = QSpinBox()
        self.num_bodies_spin.setRange(1, 10)
        self.num_bodies_spin.setValue(len(self.bodies_data))
        self.num_bodies_spin.valueChanged.connect(self.update_bodies)
        self.num_bodies_spin.setToolTip("Number of celestial bodies in the simulation (1-10)")
        layout.addWidget(QLabel("Number of Bodies:"))
        layout.addWidget(self.num_bodies_spin)
        
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["Body", "Mass", "Radius", "Pos X", "Pos Y", "Pos Z", "Vel X", "Vel Y", "Vel Z"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
        self.update_bodies()  # Initial creation
    
    def update_bodies(self):
        num = self.num_bodies_spin.value()
        while len(self.bodies_data) < num:
            index = len(self.bodies_data)
            self.bodies_data.append(self.defaults[index].copy())
        while len(self.bodies_data) > num:
            self.bodies_data.pop()
        self.table.setRowCount(num)
        for i in range(num):
            # Body label
            item = QTableWidgetItem(f"Body {i+1}")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(i, 0, item)
            
            # Mass
            mass_spin = QDoubleSpinBox()
            mass_spin.setRange(1, 200)
            mass_spin.setValue(self.bodies_data[i]['mass'])
            self.table.setCellWidget(i, 1, mass_spin)
            
            # Radius (auto)
            radius_spin = QDoubleSpinBox()
            radius_spin.setRange(1, 20)
            radius_spin.setValue(self.bodies_data[i]['mass'] / 20)
            radius_spin.setEnabled(False)
            self.table.setCellWidget(i, 2, radius_spin)
            mass_spin.valueChanged.connect(lambda val, rs=radius_spin: rs.setValue(val / 20))
            
            # Pos
            for j in range(3):
                spin = QDoubleSpinBox()
                spin.setRange(-200, 200)
                spin.setValue(self.bodies_data[i]['pos'][j])
                self.table.setCellWidget(i, 3 + j, spin)
            
            # Vel
            for j in range(3):
                spin = QDoubleSpinBox()
                spin.setRange(-100, 100)
                spin.setValue(self.bodies_data[i]['vel'][j])
                self.table.setCellWidget(i, 6 + j, spin)
    
    def get_data(self):
        data = []
        for i in range(self.table.rowCount()):
            mass = self.table.cellWidget(i, 1).value()
            radius = self.table.cellWidget(i, 2).value()
            pos = [self.table.cellWidget(i, 3 + j).value() for j in range(3)]
            vel = [self.table.cellWidget(i, 6 + j).value() for j in range(3)]
            data.append({'mass': mass, 'radius': radius, 'pos': pos, 'vel': vel})
        return data

def main():
    logging.basicConfig(level=logging.INFO, filename='simulation.log', format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Application started")
    bodies = [
        Body(50, [50, 50, 10], [20, 10, 5]),
        Body(100, [100, 50, 20], [15, 20, 10]),
        Body(200, [50, 100, 30], [10, 15, 20])
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
