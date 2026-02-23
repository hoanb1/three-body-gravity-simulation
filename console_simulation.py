from src.core.physics import Body, rk4_step
import numpy as np

def console_simulation():
    bodies = [
        Body(100, [0, 100, 0], [10, 0, 0]),
        Body(102, [100, 0, 0], [12, 0, 0]),
        Body(104, [0, 0, 100], [14, 0, 0])
    ]
    
    print("Three-Body Gravity Simulation (Console)")
    print("=====================================")
    print("Initial positions:")
    for i, body in enumerate(bodies):
        print(f"Body {i+1}: pos=[{body.pos[0]:.2f}, {body.pos[1]:.2f}, {body.pos[2]:.2f}], vel=[{body.vel[0]:.2f}, {body.vel[1]:.2f}, {body.vel[2]:.2f}]")
    
    # Run simulation for 1000 steps
    for step in range(1000):
        rk4_step(bodies, 0.01)
        
        # Print every 100 steps
        if (step + 1) % 100 == 0:
            print(f"\nStep {step + 1}:")
            for i, body in enumerate(bodies):
                print(f"Body {i+1}: pos=[{body.pos[0]:.2f}, {body.pos[1]:.2f}, {body.pos[2]:.2f}], vel=[{body.vel[0]:.2f}, {body.vel[1]:.2f}, {body.vel[2]:.2f}]")
    
    print("\nSimulation complete!")

if __name__ == "__main__":
    console_simulation()
