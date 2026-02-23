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
  controlsRef,
  numBodies,
  masses,
  velocities,
  setMasses,
  setVelocities
}) {
  const trailsRef = useRef(bodies.map(() => []));
  const colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#FFA500', '#800080', '#FFC0CB'];
  const { camera } = useThree();

  useFrame(() => {
    // 1. Physics update (RK4)
    rk4_step(bodies, 0.01 * timeScale);

    // 2. Update Trails
    bodies.forEach((body, i) => {
      if (!trailsRef.current[i]) trailsRef.current[i] = [];
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
    // eslint-disable-next-line no-undef
    trailsRef.current = bodies.map(() => []);
    
    // Generate bodies based on numBodies with custom masses
    const newBodies = [];
    const colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#FFA500', '#800080', '#FFC0CB'];

    // Regenerate random masses and velocities on each initialize
    // eslint-disable-next-line no-undef
    const newMasses = Array.from({ length: numBodies }, () => 10 + Math.random() * 290);
    // eslint-disable-next-line no-undef
    const newVelocities = Array.from({ length: numBodies }, () => [5 + Math.random() * 15, (Math.random() - 0.5) * 20, (Math.random() - 0.5) * 20]);
    // eslint-disable-next-line no-undef
    setMasses(newMasses);
    // eslint-disable-next-line no-undef
    setVelocities(newVelocities);
    
    for (let i = 0; i < numBodies; i++) {
      // eslint-disable-next-line no-undef
      const mass = newMasses[i];
      const angle = (i / numBodies) * 2 * Math.PI;
      const radius = 60;
      const centerX = 100;
      const centerY = 100;
      const pos = [
        centerX + radius * Math.cos(angle), // Evenly spaced in circle
        centerY + radius * Math.sin(angle),
        20 + Math.random() * 20   // Z: 20-40
      ];
      // eslint-disable-next-line no-undef
      const vel = newVelocities[i];
      newBodies.push(new Body(mass, pos, vel));
    }
    
    setBodies(newBodies);
    setSelectedBody(-1);
  // eslint-disable-next-line no-undef
  }, [resetTrigger, numBodies]);

  return (
    <>
      <color attach="background" args={['#ffffff']} />
      <ambientLight intensity={0.7} />
      <pointLight position={[100, 100, 150]} intensity={2} />

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
            emissiveIntensity={0.2}
          />
        </mesh>
      ))}

      {bodies.map((body, i) => (
        trailsRef.current[i]?.length > 1 && (
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
  const [fps, setFps] = useState(0);
  const [showPanel, setShowPanel] = useState(true);
  const [numBodies, setNumBodies] = useState(3);
  const [masses, setMasses] = useState(Array(3).fill(50));
  const [velocities, setVelocities] = useState(Array(3).fill([0, 0, 0]));
  const [bodies, setBodies] = useState([
    new Body(50, [50, 50, 10], [20, 10, 5]),
    new Body(50, [100, 50, 20], [15, 20, 10]),
    new Body(50, [50, 100, 30], [10, 15, 20])
  ]);
  const [selectedBody, setSelectedBody] = useState(-1);
  const [timeScale, setTimeScale] = useState(1.0);
  const [resetTrigger, setResetTrigger] = useState(0);
  const [follow, setFollow] = useState(false);

  const controlsRef = useRef(); // Ref để điều khiển OrbitControls
  const frameCountRef = useRef(0);
  const lastTimeRef = useRef(Date.now());

  React.useEffect(() => {
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

  // Reset masses when numBodies changes
  useEffect(() => {
    const defaultMasses = Array.from({ length: numBodies }, () => 10 + Math.random() * 290); // Random mass 10-300
    setMasses(defaultMasses);
  }, [numBodies]);

  // Reset velocities when numBodies changes
  useEffect(() => {
    const defaultVelocities = Array.from({ length: numBodies }, () => [5 + Math.random() * 15, (Math.random() - 0.5) * 20, (Math.random() - 0.5) * 20]); // Random velocity with increased spread, still roughly positive x direction
    setVelocities(defaultVelocities);
  }, [numBodies]);

  return (
    <div className="w-screen h-screen relative bg-gradient-to-br from-blue-200 to-indigo-300">
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
          numBodies={numBodies}
          masses={masses}
          velocities={velocities}
          setMasses={setMasses}
          setVelocities={setVelocities}
        />
      </Canvas>

      {/* UI Overlay */}
      <div className="absolute top-4 left-4 z-10 flex flex-col gap-2">
        <button
          onClick={() => setShowPanel(!showPanel)}
          className="bg-white/10 backdrop-blur-md text-black px-4 py-2 rounded-full border border-gray-400 hover:bg-white/20 transition-all text-xs font-bold"
        >
          {showPanel ? 'HIDE CONTROLS' : 'SHOW CONTROLS'}
        </button>
        <div className="bg-white/50 text-black px-3 py-1 rounded-full text-[10px] font-mono self-start border border-gray-400">
          SYSTEM_STABLE // FPS: {fps}
        </div>
      </div>

      {showPanel && (
        <div className="absolute bottom-6 right-6 bg-white/90 backdrop-blur-xl border border-gray-400 rounded-3xl p-6 shadow-2xl max-w-sm text-black animate-in fade-in slide-in-from-bottom-4 duration-500">
          <h2 className="text-xl font-black mb-4 tracking-tighter italic">ORBITAL_MECHANICS</h2>
          
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-[10px] uppercase tracking-widest text-gray-600 mb-2">
                <span>Objects</span>
                <span>{numBodies}</span>
              </div>
              <input
                type="range"
                min="2"
                max="9"
                step="1"
                value={numBodies}
                onChange={e => setNumBodies(parseInt(e.target.value))}
                className="w-full accent-blue-500"
              />
            </div>

            <div>
              <div className="text-[10px] uppercase tracking-widest text-gray-600 mb-2">Mass Settings</div>
              <div className="grid grid-cols-3 gap-2">
                {masses?.map((mass, i) => (
                  <div key={i} className="text-center">
                    <div className="text-[8px] text-gray-500">Body {i}</div>
                    <input
                      type="number"
                      min="10"
                      max="300"
                      value={mass}
                      onChange={e => {
                        const newMasses = [...masses];
                        newMasses[i] = parseInt(e.target.value) || 50;
                        setMasses(newMasses);
                      }}
                      className="w-full text-[10px] bg-white border border-gray-300 rounded px-1 py-0.5"
                    />
                  </div>
                ))}
              </div>
            </div>

            <div>
              <div className="text-[10px] uppercase tracking-widest text-gray-600 mb-2">Velocity Settings</div>
              <div className="grid grid-cols-3 gap-2">
                {velocities?.map((vel, i) => (
                  <div key={i} className="text-center">
                    <div className="text-[8px] text-gray-500">Body {i}</div>
                    <div className="flex gap-1 justify-center">
                      <input
                        type="number"
                        step="0.1"
                        value={vel[0]}
                        onChange={e => {
                          const newVelocities = [...velocities];
                          newVelocities[i] = [parseFloat(e.target.value) || 0, vel[1], vel[2]];
                          setVelocities(newVelocities);
                        }}
                        className="w-6 text-[8px] bg-white border border-gray-300 rounded px-0.5 py-0"
                        placeholder="VX"
                      />
                      <input
                        type="number"
                        step="0.1"
                        value={vel[1]}
                        onChange={e => {
                          const newVelocities = [...velocities];
                          newVelocities[i] = [vel[0], parseFloat(e.target.value) || 0, vel[2]];
                          setVelocities(newVelocities);
                        }}
                        className="w-6 text-[8px] bg-white border border-gray-300 rounded px-0.5 py-0"
                        placeholder="VY"
                      />
                      <input
                        type="number"
                        step="0.1"
                        value={vel[2]}
                        onChange={e => {
                          const newVelocities = [...velocities];
                          newVelocities[i] = [vel[0], vel[1], parseFloat(e.target.value) || 0];
                          setVelocities(newVelocities);
                        }}
                        className="w-6 text-[8px] bg-white border border-gray-300 rounded px-0.5 py-0"
                        placeholder="VZ"
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <div className="flex justify-between text-[10px] uppercase tracking-widest text-gray-600 mb-2">
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
                className="bg-black text-white font-bold py-2 rounded-xl text-xs hover:bg-gray-800 transition-colors"
              >
                INITIALIZE
              </button>
              <button
                onClick={() => setFollow(!follow)}
                className={`py-2 rounded-xl text-xs font-bold transition-all border ${
                  follow ? 'bg-blue-600 border-blue-400 shadow-[0_0_15px_rgba(37,99,235,0.5)]' : 'bg-transparent border-gray-400 hover:border-gray-600'
                }`}
              >
                {follow ? 'FOLLOW_ON' : 'FOLLOW_OFF'}
              </button>
            </div>

            {selectedBody >= 0 && (
              <div className="p-3 bg-gray-50 rounded-2xl border border-gray-200">
                <div className="text-[10px] text-blue-600 mb-1 font-bold uppercase tracking-tighter">Target_Acquired: Body_{selectedBody}</div>
                <div className="text-[10px] font-mono text-gray-700 leading-tight">
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