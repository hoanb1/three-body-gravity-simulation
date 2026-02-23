import React, { useState, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Grid, Line } from '@react-three/drei';
import * as THREE from 'three';
import { Body, rk4_step } from './physics';
import './App.css';

function Simulation({ bodies, setBodies, timeScale, resetTrigger, selectedBody, setSelectedBody }) {
  const trailsRef = useRef(bodies.map(() => []));
  const colors = ['red', 'green', 'blue'];

  useFrame((state, delta) => {
    rk4_step(bodies, 0.01 * timeScale);
    bodies.forEach((body, i) => {
      trailsRef.current[i].push(body.pos.clone());
      if (trailsRef.current[i].length > 2000) trailsRef.current[i].shift();
    });
    setBodies([...bodies]);
  });

  // Reset when resetTrigger changes
  React.useEffect(() => {
    trailsRef.current = bodies.map(() => []);
    setBodies([
      new Body(50, [50, 50, 10], [20, 10, 5]),
      new Body(100, [100, 50, 20], [15, 20, 10]),
      new Body(200, [50, 100, 30], [10, 15, 20])
    ]);
    setSelectedBody(-1);
    console.log('Simulation reset');
  }, [resetTrigger, setBodies, setSelectedBody]);

  return (
    <>
      <color attach="background" args={['#000000']} />
      <ambientLight intensity={0.3} />
      <pointLight position={[100, 100, 150]} />
      {bodies.map((body, i) => (
        <mesh
          key={i}
          position={body.pos.toArray()}
          onClick={() => {
            setSelectedBody(i);
            console.log(`Selected body: ${i}`);
          }}
        >
          <sphereGeometry args={[body.mass / 20, 20, 20]} />
          <meshStandardMaterial color={colors[i % colors.length]} />
        </mesh>
      ))}
      {bodies.map((body, i) => (
        trailsRef.current[i].length > 1 && (
          <Line
            key={`trail-${i}`}
            points={trailsRef.current[i].map(v => v.toArray())}
            color={colors[i % colors.length]}
            lineWidth={2}
          />
        )
      ))}
      <Grid args={[500, 500]} />
      <primitive object={new THREE.AxesHelper(200)} />
    </>
  );
}

function App() {
  const fpsState = useState(0);
  const fps = fpsState[0];
  const setFps = fpsState[1];
  const [bodies, setBodies] = useState([
    new Body(50, [50, 50, 10], [20, 10, 5]),
    new Body(100, [100, 50, 20], [15, 20, 10]),
    new Body(200, [50, 100, 30], [10, 15, 20])
  ]);
  const [selectedBody, setSelectedBody] = useState(-1);
  const [timeScale, setTimeScale] = useState(1.0);
  const [resetTrigger, setResetTrigger] = useState(0);
  const [showPanel, setShowPanel] = useState(true);
  const frameCountRef = useRef(0);
  const lastTimeRef = useRef(Date.now());

  React.useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      const delta = (now - lastTimeRef.current) / 1000;
      // eslint-disable-next-line no-undef
      setFps(Math.round(frameCountRef.current / delta));
      frameCountRef.current = 0;
      lastTimeRef.current = now;
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  React.useEffect(() => {
    const animate = () => {
      frameCountRef.current++;
      requestAnimationFrame(animate);
    };
    animate();
  }, []);

  const handleReset = () => {
    setResetTrigger(prev => prev + 1);
  };

  const handleExport = () => {
    console.log('Export data:', bodies.map(body => ({
      mass: body.mass,
      pos: body.pos.toArray(),
      vel: body.vel.toArray()
    })));
    alert('Data exported to console');
  };

  const selectedBodyInfo = selectedBody >= 0 ? 
    `Body ${selectedBody}: Mass ${bodies[selectedBody].mass}, Pos (${bodies[selectedBody].pos.x.toFixed(1)}, ${bodies[selectedBody].pos.y.toFixed(1)}, ${bodies[selectedBody].pos.z.toFixed(1)}), Vel (${bodies[selectedBody].vel.x.toFixed(1)}, ${bodies[selectedBody].vel.y.toFixed(1)}, ${bodies[selectedBody].vel.z.toFixed(1)})` 
    : 'Selected Body: None';

  return (
    <div className="w-screen h-screen relative bg-gradient-to-br from-gray-900 via-blue-900 to-indigo-900">
      <Canvas camera={{ position: [100, 100, 100], fov: 60 }}>
        <OrbitControls />
        <Simulation 
          bodies={bodies} 
          setBodies={setBodies} 
          timeScale={timeScale} 
          resetTrigger={resetTrigger} 
          selectedBody={selectedBody} 
          setSelectedBody={setSelectedBody} 
        />
      </Canvas>
      <button 
        onClick={() => setShowPanel(!showPanel)}
        className="absolute top-4 left-4 bg-gray-800/80 hover:bg-gray-700 text-white px-3 py-1 rounded-lg text-sm transition-all duration-300"
      >
        {showPanel ? 'Hide UI' : 'Show UI'}
      </button>
      {showPanel && (
        <div className="absolute bottom-4 right-4 bg-white/5 backdrop-blur-lg border border-white/20 rounded-2xl p-4 shadow-2xl max-w-sm text-white animate-fade-in">
          <h2 className="text-lg font-bold mb-3 text-white">3-Body Gravity Simulation</h2>
          <div className="mb-1 font-light text-sm">
            {/* eslint-disable-next-line no-undef */}
            FPS: {fps}
          </div>
          <div className="mb-1 font-light text-sm">Time Scale: {timeScale.toFixed(1)}x</div>
          <div className="mb-3 text-xs font-light">{selectedBodyInfo}</div>
          <button 
            onClick={handleReset}
            className="bg-gradient-to-r from-pink-500 to-cyan-500 hover:from-pink-600 hover:to-cyan-600 text-white font-bold py-1 px-3 rounded-lg transition-all duration-300 hover:shadow-lg hover:-translate-y-1 mr-1 mb-1 text-sm"
          >
            Reset
          </button>
          <input
            type="range"
            min="0.1"
            max="10"
            step="0.1"
            value={timeScale}
            onChange={(e) => setTimeScale(parseFloat(e.target.value))}
            className="w-full h-1 bg-white/30 rounded-lg appearance-none cursor-pointer mt-1 slider-thumb"
          />
          <button 
            onClick={handleExport}
            className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold py-1 px-3 rounded-lg transition-all duration-300 hover:shadow-lg hover:-translate-y-1 mr-1 mb-1 text-sm"
          >
            Export
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
