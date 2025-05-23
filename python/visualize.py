# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
from three_body import Body, step

def simulate(n_steps=10000, dt=1e3):
    bodies = []
    for init in [
        {"mass": 1.0e30, "pos": [0, 0, 0],      "vel": [0, 1e4, 0]},
        {"mass": 1.0e30, "pos": [1e11, 0, 0],   "vel": [0, -1e4, 0]},
        {"mass": 1.0e30, "pos": [0, 1e11, 0],   "vel": [-1e4, 0, 0]},
    ]:
        b = Body()            # 默认构造
        b.mass = init["mass"]
        b.pos  = init["pos"]
        b.vel  = init["vel"]
        bodies.append(b)

    traj = np.zeros((n_steps, 3, 3))
    for i in range(n_steps):
        for j, b in enumerate(bodies):
            traj[i,j] = b.pos
        step(bodies, dt)
    return traj

if __name__=="__main__":
    traj = simulate()
    plt.figure(figsize=(6,6))

    all_x = traj[...,0]
    all_y = traj[...,1]
    margin = 0.05
    xmin, xmax = all_x.min(), all_x.max()
    ymin, ymax = all_y.min(), all_y.max()
    dx, dy = xmax-xmin, ymax-ymin
    plt.xlim(xmin - dx*margin, xmax + dx*margin)
    plt.ylim(ymin - dy*margin, ymax + dy*margin)

    for i in range(3):
        plt.plot(traj[:,i,0], traj[:,i,1], label=f"Body {i}")
    plt.legend()
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Three-Body Simulation")
    plt.axis("equal")

    out = "three_body.png"
    plt.savefig(out, dpi=150)
    print(f"模拟结果已保存到 {out}")
