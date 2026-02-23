import * as THREE from 'three';

export class Body {
  constructor(mass, pos, vel) {
    this.mass = mass;
    this.pos = new THREE.Vector3(...pos);
    this.vel = new THREE.Vector3(...vel);
  }
}

function compute_forces(bodies) {
  const G = 100;
  const forces = bodies.map(() => new THREE.Vector3());
  for (let i = 0; i < bodies.length; i++) {
    for (let j = 0; j < bodies.length; j++) {
      if (i !== j) {
        const r = bodies[j].pos.clone().sub(bodies[i].pos);
        const dist = r.length();
        if (dist > 0) {
          const forceMag = G * bodies[i].mass * bodies[j].mass / (dist * dist);
          const force = r.normalize().multiplyScalar(forceMag);
          forces[i].add(force);
        }
      }
    }
  }
  return forces;
}

export function rk4_step(bodies, dt) {
  const forces = compute_forces(bodies);
  for (let i = 0; i < bodies.length; i++) {
    const body = bodies[i];
    const a = forces[i].divideScalar(body.mass);
    body.vel.add(a.multiplyScalar(dt));
    body.pos.add(body.vel.clone().multiplyScalar(dt));
  }
}
