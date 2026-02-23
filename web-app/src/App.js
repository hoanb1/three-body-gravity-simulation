// File: App.js
import React, { useState, useRef, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Grid, Line } from '@react-three/drei';
import * as THREE from 'three';
import { Body, rk4_step } from './physics';
import './App.css';

function Simulation({
  bodies,
  setBodies,
  timeScale,
  resetTrigger,
  selectedBody,
  setSelectedBody,
  follow,
  controlsRef
}) {
  const trailsRef = useRef(bodies.map(() => []));
  const colors = ['#FF0000', '#00FF00', '#0000FF'];
  const { camera } = useThree();

  useFrame(() => {
    // 1. Physics update (RK4)
    rk4_step(bodies, 0.01 * timeScale);

    // 2. Update Trails
    bodies.forEach((body, i) => {
      trailsRef.current[i].push(body.pos.clone());
      if (trailsRef.current[i].length > 1500) trailsRef.current[i].shift();
    });

    setBodies([...bodies]);

    // 3. Simple Follow: Just set the selected object to the center of the camera
    if (follow && selectedBody >= 0 && controlsRef.current) {
      controlsRef.current.target.copy(bodies[selectedBody].pos);
      controlsRef.current.update();
    }
  });

  // Center the camera on the object when it is selected
  useEffect(() => {
    if (selectedBody >= 0 && controlsRef.current) {
      controlsRef.current.target.copy(bodies[selectedBody].pos);
      controlsRef.current.update();
    }
  }, [selectedBody, follow]);

  React.useEffect(() => {
    trailsRef.current = bodies.map(() => []);
    setBodies([
      new Body(50, [50, 50, 10], [20, 10, 5]),
      new Body(100, [100, 50, 20], [15, 20, 10]),
      new Body(200, [50, 100, 30], [10, 15, 20])
    ]);
    setSelectedBody(-1);
  }, [resetTrigger, setBodies, setSelectedBody]);

  return (
    <>
      <color attach="background" args={['#050505']} />
      <ambientLight intensity={0.4} />
      <pointLight position={[100, 100, 150]} intensity={1.5} />

      {bodies.map((body, i) => (
        <mesh
          key={i}
          position={body.pos.toArray()}
          onClick={(e) => {
            e.stopPropagation();
            setSelectedBody(i);
          }}
        >
          <sphereGeometry args={[body.mass / 20, 32, 32]} />
          <meshStandardMaterial
            color={colors[i % colors.length]}
            emissive={colors[i % colors.length]}
            emissiveIntensity={0.5}
          />
        </mesh>
      ))}

      {bodies.map((body, i) => (
        trailsRef.current[i].length > 1 && (
          <Line
            key={`trail-${i}`}
            points={trailsRef.current[i].map(v => v.toArray())}
            color={colors[i % colors.length]}
            lineWidth={1.5}
            transparent
            opacity={0.6}
          />
        )
      ))}

      <Grid args={[1000, 1000]} sectionColor="#222" cellColor="#111" infiniteGrid />
    </>
  );
}

function App() {
  const [fps, setFps] = useState(0);
  const [showPanel, setShowPanel] = useState(true);
  const [bodies, setBodies] = useState([
    new Body(50, [50, 50, 10], [20, 10, 5]),
    new Body(100, [100, 50, 20], [15, 20, 10]),
    new Body(200, [50, 100, 30], [10, 15, 20])
  ]);
  const [selectedBody, setSelectedBody] = useState(-1);
  const [timeScale, setTimeScale] = useState(1.0);
  const [resetTrigger, setResetTrigger] = useState(0);
  const [follow, setFollow] = useState(false);

  const controlsRef = useRef();
  const frameCountRef = useRef(0);
  const lastTimeRef = useRef(Date.now());

  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      const delta = (now - lastTimeRef.current) / 1000;
      setFps(Math.round(frameCountRef.current / delta));
      frameCountRef.current = 0;
      lastTimeRef.current = now;
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const animate = () => {
      frameCountRef.current++;
      requestAnimationFrame(animate);
    };
    const id = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(id);
  }, []);

  return (
    <div className="w-screen h-screen relative bg-black overflow-hidden">
      <Canvas camera={{ position: [300, 300, 300], fov: 50, near: 0.1, far: 20000 }}>
        <OrbitControls
          ref={controlsRef}
          makeDefault
          enableDamping={true}
          dampingFactor={0.05}
          minDistance={10}
          maxDistance={5000}
        />

        <Simulation
          bodies={bodies}
          setBodies={setBodies}
          timeScale={timeScale}
          resetTrigger={resetTrigger}
          selectedBody={selectedBody}
          setSelectedBody={setSelectedBody}
          follow={follow}
          controlsRef={controlsRef}
        />
      </Canvas>

      {/* UI Overlay */}
      <div className="absolute top-4 left-4 z-10 flex flex-col gap-2">
        <button
          onClick={() => setShowPanel(!showPanel)}
          className="bg-white/10 backdrop-blur-md text-white px-4 py-2 rounded-full border border-white/20 hover:bg-white/20 transition-all text-xs font-bold"
        >
          {showPanel ? 'HIDE CONTROLS' : 'SHOW CONTROLS'}
        </button>
        <div className="bg-black/50 text-green-400 px-3 py-1 rounded-full text-[10px] font-mono self-start border border-green-900/50">
          SYSTEM_STABLE // FPS: {fps}
        </div>
      </div>

      {showPanel && (
        <div className="absolute bottom-6 right-6 bg-black/60 backdrop-blur-xl border border-white/10 rounded-3xl p-6 shadow-2xl max-w-sm text-white animate-in fade-in slide-in-from-bottom-4 duration-500">
          <h2 className="text-xl font-black mb-4 tracking-tighter italic">ORBITAL_MECHANICS</h2>
          
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-[10px] uppercase tracking-widest text-gray-400 mb-2">
                <span>Time Dilation</span>
                <span>{timeScale.toFixed(1)}x</span>
              </div>
              <input
                type="range" min="0.1" max="10" step="0.1"
                value={timeScale}
                onChange={e => setTimeScale(parseFloat(e.target.value))}
                className="w-full accent-blue-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => setResetTrigger(v => v + 1)}
                className="bg-white text-black font-bold py-2 rounded-xl text-xs hover:bg-gray-200 transition-colors"
              >
                INITIALIZE
              </button>
              <button
                onClick={() => setFollow(!follow)}
                className={`py-2 rounded-xl text-xs font-bold transition-all border ${
                  follow ? 'bg-blue-600 border-blue-400 shadow-[0_0_15px_rgba(37,99,235,0.5)]' : 'bg-transparent border-white/20 hover:border-white'
                }`}
              >
                {follow ? 'FOLLOW_ON' : 'FOLLOW_OFF'}
              </button>
            </div>

            {selectedBody >= 0 && (
              <div className="p-3 bg-white/5 rounded-2xl border border-white/5">
                <div className="text-[10px] text-blue-400 mb-1 font-bold uppercase tracking-tighter">Target_Acquired: Body_{selectedBody}</div>
                <div className="text-[10px] font-mono text-gray-400 leading-tight">
                  X: {bodies[selectedBody].pos.x.toFixed(2)}<br/>
                  Y: {bodies[selectedBody].pos.y.toFixed(2)}<br/>
                  Z: {bodies[selectedBody].pos.z.toFixed(2)}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;