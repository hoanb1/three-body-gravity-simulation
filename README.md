# N-Body Gravity Simulation (Web App)

A beautiful 3D gravity simulation built with React, Three.js, and Tailwind CSS. Simulate the gravitational interactions of multiple celestial bodies (2-9) in real-time with an intuitive web interface and random initialization.

## 🌟 Live Demo

Visit the live application at [test.hoan.uk](https://test.hoan.uk)

## ✨ Features

- **3D Visualization**: Immersive 3D rendering of celestial bodies and their orbital trails using Three.js.
- **Real-time Physics**: Accurate gravitational force calculations with numerical integration.
- **Variable Body Count**: Simulate 2-9 celestial bodies with adjustable parameters.
- **Random Initialization**: Generate random masses, positions, and velocities on each reset.
- **Interactive Controls**:
  - Mouse: Orbit, zoom, and pan the 3D view.
  - Body Count: Adjust number of objects (2-9).
  - Mass Settings: Customize mass for each body.
  - Velocity Settings: Set initial velocity vectors (x, y, z) for each body.
  - Time Scale: Adjust simulation speed (0.1x to 10x).
  - Initialize: Regenerate all random values and restart simulation.
  - Full Screen: Toggle immersive mode.
- **Object Selection**: Click on bodies to select and view their properties (mass, position, velocity).
- **Camera Follow**: Option to make the camera follow the selected object with manual adjustments allowed.
- **UI Toggle**: Hide/show the control panel for unobstructed viewing.
- **Responsive Design**: Works seamlessly on desktop and mobile browsers.

## 🚀 Technologies Used

- **Frontend**: React 18 with hooks and modern JavaScript
- **3D Graphics**: Three.js with React Three Fiber for WebGL rendering
- **Styling**: Tailwind CSS for responsive, utility-first UI design
- **Physics**: Custom JavaScript implementation of gravitational forces and numerical integration
- **Deployment**: Cloudflare Tunnel for secure, global access + systemd service on Raspberry Pi
- **Build Tools**: Create React App with optimized production builds

## 💻 Installation & Running Locally

1. **Prerequisites**: Node.js 16+ and npm

2. **Clone the repository**:
   ```bash
   git clone https://github.com/hoanb1/three-body-gravity-simulation.git
   cd three-body-gravity-simulation
   ```

3. **Install dependencies**:
   ```bash
   cd web-app
   npm install
   ```

4. **Start the development server**:
   ```bash
   npm start
   ```
   Open [http://localhost:3000](http://localhost:3000) in your browser.

5. **Build for production**:
   ```bash
   npm run build
   npm install -g serve
   serve -s build
   ```

## 🌐 Deployment

The application is deployed on a Raspberry Pi with Cloudflare Tunnel and systemd service:

- **Server**: Raspberry Pi 4 at 192.168.3.24
- **Local Port**: Dynamic (assigned by systemd)
- **Tunnel**: Cloudflare Tunnel routing test.hoan.uk to the local server
- **Global Access**: https://test.hoan.uk
- **Service**: systemd service for automatic startup and management

**Deployment Steps**:
1. Build the production app: `npm run build`
2. Copy build to server: `scp -r build pi@192.168.3.24:~/web-app-build`
3. Install systemd service:
   - Copy web-app.service to /etc/systemd/system/
   - `sudo systemctl daemon-reload`
   - `sudo systemctl enable web-app`
   - `sudo systemctl start web-app`
4. Configure Cloudflare tunnel to match the service port
5. Restart cloudflared: `sudo systemctl restart cloudflared`

## 📖 Usage

1. **Adjust Body Count**: Use the slider to set 2-9 celestial bodies.
2. **Customize Parameters**: Set individual masses and initial velocity vectors (x, y, z) for each body.
3. **Initialize Simulation**: Click "INITIALIZE" to generate random positions and restart with your custom parameters.
4. **View the Simulation**: Observe the bodies interacting gravitationally with orbital trails.
5. **Adjust Time Scale**: Use the slider to speed up or slow down the simulation.
6. **Select Objects**: Click on any body to highlight and view its properties.
7. **Follow Camera**: Check "FOLLOW ON" to track the selected object.
8. **Reset**: Click "INITIALIZE" again to regenerate all random values.
9. **Hide UI**: Click "HIDE CONTROLS" for a full-screen experience.
10. **Navigate**: Use mouse to rotate, zoom, and pan the 3D view.

## 🧮 Physics Implementation

The simulation implements:
- **Gravitational Force**: F = G × m₁ × m₂ / r²
- **Numerical Integration**: Euler method for position and velocity updates
- **Time Step**: 0.01 seconds with adjustable scaling (0.1x to 10x)
- **Mass Proportional Sizing**: Body radius scales with mass for visual representation
- **Random Initialization**: Positions spaced in circle, velocities with controlled randomness

## 🎨 UI/UX Design

- **Glassmorphism**: Modern backdrop blur effects with transparent panels
- **Responsive Layout**: Adaptive design for various screen sizes
- **Interactive Elements**: Hover effects, smooth transitions, and intuitive controls
- **Color Scheme**: Light space theme with bright accent colors
- **Dynamic Controls**: UI updates based on selected body count

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Open a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with React Three Fiber for seamless 3D integration
- Tailwind CSS for beautiful, responsive UI
- Three.js for powerful WebGL rendering
- Cloudflare for reliable tunneling
- systemd for service management on Raspberry Pi

## 📚 Development History

This project evolved from a Python desktop application (PyQt6 + OpenGL) to a modern web application using React and Three.js for better accessibility, performance, and cross-platform compatibility.

---

**Note**: The original Python implementation is available in the Git history for reference.