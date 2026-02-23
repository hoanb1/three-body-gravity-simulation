from PyQt6.QtOpenGLWidgets import QOpenGLWidget
import moderngl as mgl
import numpy as np
from OpenGL.GL import glViewport

class GLWidget(QOpenGLWidget):
    def __init__(self, bodies):
        super().__init__()
        self.bodies = bodies
        # Orthographic projection matrix: left, right, bottom, top, near, far
        self.mvp = np.array([
            [0.01, 0, 0, 0],
            [0, 0.01, 0, 0],
            [0, 0, 0.01, 0],
            [0, 0, 0, 1]
        ], dtype='f4')

    def initializeGL(self):
        print("initializeGL called")
        try:
            self.ctx = mgl.create_context()
            print("ModernGL context created successfully")
        except Exception as e:
            print(f"Failed to create ModernGL context: {e}")
            return
        
        try:
            with open('shaders/basic.vert', 'r') as f:
                vert = f.read()
            with open('shaders/basic.frag', 'r') as f:
                frag = f.read()
            print(f"Vertex shader: {vert}")
            print(f"Fragment shader: {frag}")
            self.program = self.ctx.program(vertex_shader=vert, fragment_shader=frag)
            print("Shader program created successfully")
        except Exception as e:
            print(f"Failed to create shader program: {e}")
            return
        
        try:
            self.program['mvp'] = self.mvp.flatten()
            positions = np.array([b.pos for b in self.bodies], dtype='f4').flatten()
            print(f"Positions: {positions}")
            self.vbo = self.ctx.buffer(positions.tobytes())
            self.vao = self.ctx.vertex_array(self.program, [(self.vbo, '3f', 'in_position')])
            print("VBO and VAO created successfully")
        except Exception as e:
            print(f"Failed to create buffers: {e}")

    def paintGL(self):
        self.ctx.clear(0, 0, 0)
        positions = np.array([b.pos for b in self.bodies], dtype='f4').flatten()
        self.vbo.write(positions.tobytes())
        self.vao.render(mgl.POINTS, vertices=len(self.bodies))

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
