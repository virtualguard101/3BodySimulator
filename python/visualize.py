# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///

import numpy as np
import matplotlib.pyplot as plt
from three_body import Body, step

def simulate(n_steps=500, dt=1e3):
    bodies = [
        Body(mass=1.0e30, pos=[0,0,0], vel=[0,1e4,0]),
        Body(mass=1.0e30, pos=[1e11,0,0], vel=[0,-1e4,0]),
        Body(mass=1.0e30, pos=[0,1e11,0], vel=[-1e4,0,0]),
    ]
    traj = np.zeros((n_steps, 3, 3))
    for i in range(n_steps):
        for j, b in enumerate(bodies):
            traj[i,j] = b.pos
        step(bodies, dt)
    return traj

if __name__=="__main__":
    traj = simulate()
    plt.figure(figsize=(6,6))
    for i in range(3):
        plt.plot(traj[:,i,0], traj[:,i,1], label=f"Body {i}")
    plt.legend()
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Three-Body Simulation")
    plt.axis("equal")
    plt.show()
