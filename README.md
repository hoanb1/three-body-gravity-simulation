# 3D Three-Body Gravity Simulation

A professional, real-time 3D simulation of gravitational interactions between celestial bodies using PyQt6, OpenGL, and NumPy. Features accurate physics, interactive controls, and polished graphics.

## 🚀 Features

### Physics Engine
- **RK4 Integration**: High-precision numerical integration for stable, accurate orbital mechanics
- **NumPy Vectorized Calculations**: Optimized force computations for real-time performance
- **Customizable Bodies**: Mass, initial position, and velocity for each celestial body

### 3D Rendering & Graphics
- **OpenGL Rendering**: ModernGL with immediate mode for smooth 3D visualization
- **Spherical Bodies**: Lit spheres with Phong shading proportional to mass
- **Orbital Trails**: Long, colored trails (2000+ points) showing historical paths
- **Coordinate Planes**: Semi-transparent XY, XZ, YZ planes with grid lines for spatial reference
- **Lighting**: Ambient and directional lighting for realistic depth perception

### Interactive Controls
- **Mouse Navigation**:
  - Left-click + drag: Rotate view (XY) / Shift: Pan / Ctrl: Zoom / Alt: Rotate Z-axis
  - Wheel zoom for additional scaling
- **Settings Dialog**: Professional table-based interface for body parameters
- **Dynamic Body Management**: Add/remove bodies (1-10) with auto-generated parameters
- **Real-time Adjustments**: Time scale, reset simulation, full screen mode

### User Interface
- **Real-time Displays**: FPS counter, current body position
- **Professional Layout**: Control panel with intuitive buttons and sliders
- **Responsive Design**: Table-based settings with scrollable interface

## 📦 Installation

### Prerequisites
- Python 3.8+
- Ubuntu/Debian-based Linux (recommended for OpenGL support)

### Setup
```bash
# Clone or download the project
cd /path/to/project

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🎮 Usage

### Running the Simulation
```bash
python opengl_3d.py
```

### Controls
- **Mouse**:
  - Drag: Rotate view
  - Shift + Drag: Pan camera
  - Ctrl + Drag: Zoom
  - Alt + Drag: Rotate Z-axis
  - Wheel: Zoom
- **Settings**: Click "Settings" to customize bodies and parameters
- **Reset**: Reset simulation to initial state
- **Time Scale**: Adjust simulation speed (0.1x - 10x)
- **Full Screen**: Toggle full screen mode

### Console Testing
```bash
python console_simulation.py
```

## 🏗️ Architecture

```
ThreeBodySim/
├── src/
│   ├── core/physics.py        # RK4 integrator, force calculations
│   ├── renderer/gl_widget.py  # OpenGL rendering, trails, lighting
│   ├── ui/main_window.py      # PyQt6 interface, controls
│   └── main.py               # Application entry point
├── shaders/                   # GLSL shaders (basic.vert, basic.frag)
├── console_simulation.py      # Console physics testing
├── opengl_3d.py              # Main GUI application
├── requirements.txt          # Python dependencies
└── README.md
```

### Key Components
- **Body Class**: Encapsulates mass, position, velocity
- **RK4 Step Function**: 4th-order Runge-Kutta integration
- **GLWidget**: Handles OpenGL context, rendering pipeline
- **SettingsDialog**: Table-based parameter editor
- **MainWindow**: Qt application with real-time controls

## 📊 Technical Details

- **Physics Accuracy**: RK4 integration ensures stable long-term simulations
- **Performance**: 60 FPS with NumPy optimization
- **Rendering**: OpenGL immediate mode with lighting and blending
- **UI Framework**: PyQt6 with responsive widgets and dialogs

## 🎯 Completed Checklist

### UI/UX Requirements ✅
- [x] Reset Simulation button
- [x] Time Scale adjustment (0.1x - 10x)
- [x] Real-time displays (FPS, coordinates)
- [x] Full Screen mode
- [x] Professional settings interface

### Graphics Requirements ✅
- [x] Orbital Trails with color coding
- [x] Lighting effects (Phong shading)
- [x] Coordinate planes and grids
- [x] Proportional body sizing

### Advanced Features ✅
- [x] Dynamic body addition/removal
- [x] Mouse modifier controls
- [x] Customizable initial conditions
- [x] GitHub repository with documentation

## 📝 Development Notes

This project demonstrates professional software development practices:
- Modular architecture with clear separation of concerns
- Optimized physics calculations using NumPy
- Modern GUI with PyQt6 and OpenGL integration
- Comprehensive user controls and real-time feedback
- Extensive documentation and version control

## 🔗 Repository

The complete source code and documentation are available on GitHub:  
https://github.com/hoanb1/three-body-gravity-simulation

## 🤝 Contributing

Feel free to fork and enhance the simulation with additional features like:
- Texture mapping for planetary surfaces
- Advanced lighting models
- Particle effects
- Multi-body scenarios
- Export capabilities

---

Built with ❤️ using PyQt6, OpenGL, and NumPy