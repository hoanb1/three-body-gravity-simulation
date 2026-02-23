# 3-Body Gravity Simulation (Web App)

A beautiful 3D gravity simulation built with React, Three.js, and Tailwind CSS. Simulate the gravitational interactions of three celestial bodies in real-time with an intuitive web interface.

## 🌟 Live Demo

Visit the live application at [test.hoan.uk](https://test.hoan.uk)

## ✨ Features

- **3D Visualization**: Immersive 3D rendering of celestial bodies and their orbital trails using Three.js.
- **Real-time Physics**: Accurate gravitational force calculations with numerical integration.
- **Interactive Controls**:
  - Mouse: Orbit, zoom, and pan the 3D view.
  - Time Scale: Adjust simulation speed (0.1x to 10x).
  - Reset: Restart the simulation.
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
- **Deployment**: Cloudflare Tunnel for secure, global access
- **Build Tools**: Create React App with optimized production builds

## � Installation & Running Locally

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
   Open [http://localhost:3001](http://localhost:3001) in your browser.

5. **Build for production**:
   ```bash
   npm run build
   npm install -g serve
   serve -s build
   ```

## 🌐 Deployment

The application is deployed on a Raspberry Pi with Cloudflare Tunnel:

- **Server**: Raspberry Pi 4 at 192.168.3.24
- **Local Port**: 3001
- **Tunnel**: Cloudflare Tunnel routing test.hoan.uk to the local server
- **Global Access**: https://test.hoan.uk

**Deployment Steps**:
1. Build the production app: `npm run build`
2. Copy build to server: `scp -r build pi@192.168.3.24:~/web-app-build`
3. Serve on server: `serve -s ~/web-app-build -l 3001`
4. Ensure Cloudflare tunnel is configured for the hostname

## 📖 Usage

1. **View the Simulation**: Observe the three bodies interacting gravitationally.
2. **Adjust Time Scale**: Use the slider to speed up or slow down the simulation.
3. **Select Objects**: Click on any body to highlight and view its properties.
4. **Follow Camera**: Check "Follow Selected" to track the selected object.
5. **Reset**: Click "Reset" to restart with initial conditions.
6. **Hide UI**: Click "Hide UI" for a full-screen experience.
7. **Navigate**: Use mouse to rotate, zoom, and pan the 3D view.

## 🧮 Physics Implementation

The simulation implements:
- **Gravitational Force**: F = G × m₁ × m₂ / r²
- **Numerical Integration**: Euler method for position and velocity updates (configurable precision)
- **Time Step**: 0.01 seconds with adjustable scaling
- **Mass Proportional Sizing**: Body radius scales with mass for visual representation

## 🎨 UI/UX Design

- **Glassmorphism**: Modern backdrop blur effects with transparent panels
- **Responsive Layout**: Adaptive design for various screen sizes
- **Interactive Elements**: Hover effects, smooth transitions, and intuitive controls
- **Color Scheme**: Dark space theme with bright accent colors

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Open a pull request

## � License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with React Three Fiber for seamless 3D integration
- Tailwind CSS for beautiful, responsive UI
- Three.js for powerful WebGL rendering
- Cloudflare for reliable tunneling

## � Development History

This project evolved from a Python desktop application (PyQt6 + OpenGL) to a modern web application using React and Three.js for better accessibility, performance, and cross-platform compatibility.

---

**Note**: The original Python implementation is available in the Git history for reference.