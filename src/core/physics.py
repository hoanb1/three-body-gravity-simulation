import numpy as np

G = 100  # Scaled gravitational constant

class Body:
    def __init__(self, mass, pos, vel):
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)

def compute_forces(bodies):
    forces = [np.zeros(3) for _ in bodies]
    for i, body1 in enumerate(bodies):
        for j, body2 in enumerate(bodies):
            if i != j:
                r = body2.pos - body1.pos
                dist = np.linalg.norm(r)
                if dist > 1e-6:  # Avoid division by zero
                    force = G * body1.mass * body2.mass / dist**3 * r
                    forces[i] += force
    return forces

def rk4_step(bodies, dt):
    # k1
    forces1 = compute_forces(bodies)
    k1_v = [force / body.mass for force, body in zip(forces1, bodies)]
    k1_x = [body.vel.copy() for body in bodies]

    # k2
    temp_pos = [body.pos + 0.5 * dt * k1_x[i] for i, body in enumerate(bodies)]
    temp_vel = [body.vel + 0.5 * dt * np.array(k1_v[i]) for i, body in enumerate(bodies)]
    temp_bodies = [Body(body.mass, temp_pos[i], temp_vel[i]) for i, body in enumerate(bodies)]
    forces2 = compute_forces(temp_bodies)
    k2_v = [force / body.mass for force, body in zip(forces2, temp_bodies)]
    k2_x = [temp.vel.copy() for temp in temp_bodies]

    # k3
    temp_pos2 = [body.pos + 0.5 * dt * k2_x[i] for i, body in enumerate(bodies)]
    temp_vel2 = [body.vel + 0.5 * dt * np.array(k2_v[i]) for i, body in enumerate(bodies)]
    temp_bodies2 = [Body(body.mass, temp_pos2[i], temp_vel2[i]) for i, body in enumerate(bodies)]
    forces3 = compute_forces(temp_bodies2)
    k3_v = [force / body.mass for force, body in zip(forces3, temp_bodies2)]
    k3_x = [temp.vel.copy() for temp in temp_bodies2]

    # k4
    temp_pos3 = [body.pos + dt * k3_x[i] for i, body in enumerate(bodies)]
    temp_vel3 = [body.vel + dt * np.array(k3_v[i]) for i, body in enumerate(bodies)]
    temp_bodies3 = [Body(body.mass, temp_pos3[i], temp_vel3[i]) for i, body in enumerate(bodies)]
    forces4 = compute_forces(temp_bodies3)
    k4_v = [force / body.mass for force, body in zip(forces4, temp_bodies3)]
    k4_x = [temp.vel.copy() for temp in temp_bodies3]

    # Update positions and velocities
    for i, body in enumerate(bodies):
        body.pos += dt / 6 * (np.array(k1_x[i]) + 2 * np.array(k2_x[i]) + 2 * np.array(k3_x[i]) + np.array(k4_x[i]))
        body.vel += dt / 6 * (np.array(k1_v[i]) + 2 * np.array(k2_v[i]) + 2 * np.array(k3_v[i]) + np.array(k4_v[i]))
