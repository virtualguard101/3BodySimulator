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
import json
from three_body import Body, step


def load_bodies_from_json(path):
    """
    从 JSON 文件加载天体参数。
    JSON 格式示例:
    [
      {"mass": ..., "pos": [x,y,z], "vel": [vx,vy,vz]}, ...
    ]
    Returns: list of dict
    """
    with open(path, 'r') as f:
        data = json.load(f)
    bodies = []
    for entry in data:
        m = float(entry['mass'])
        pos = entry.get('pos', entry.get('position'))
        vel = entry.get('vel', entry.get('velocity'))
        bodies.append({
            'mass': m,
            'pos': [float(pos[0]), float(pos[1]), float(pos[2] if len(pos)>2 else 0.0)],
            'vel': [float(vel[0]), float(vel[1]), float(vel[2] if len(vel)>2 else 0.0)]
        })
    return bodies


def get_user_bodies():
    """
    交互式获取用户定义的天体参数。
    """
    bodies = []
    try:
        n = int(input("请输入天体数量（建议 2~5）: "))
    except ValueError:
        print("输入无效，使用默认 3 体。")
        n = 3
    for i in range(n):
        print(f"\n=== 天体 {i+1} 参数 ===")
        m = float(input("质量 mass (kg): "))
        x, y = map(float, input("位置 pos (x y，米): ").split())
        vx, vy = map(float, input("速度 vel (vx vy，米/秒): ").split())
        bodies.append({
            'mass': m,
            'pos': [x, y, 0.0],
            'vel': [vx, vy, 0.0]
        })
    return bodies


def simulate(bodies, n_steps=5000, dt=1e3):
    """
    使用 C++ step 进行静态模拟。
    bodies: list of dict with keys 'mass','pos','vel'
    返回轨迹数组 shape=(n_steps, len(bodies), 3)
    """
    objs = []  # pybind11 封装的 Body
    for bi in bodies:
        b = Body()
        b.mass = bi['mass']
        b.pos = bi['pos']
        b.vel = bi['vel']
        objs.append(b)

    traj = np.zeros((n_steps, len(objs), 3))
    for i in range(n_steps):
        for j, b in enumerate(objs):
            traj[i, j] = b.pos
        step(objs, dt)
    return traj


if __name__ == "__main__":
    # 选择输入方式
    print("请选择初始条件来源：")
    print(" 1 - 默认三体参数")
    print(" 2 - 交互式终端输入")
    print(" 3 - 从 JSON 文件读取")
    choice = input("输入 1/2/3: ").strip()

    if choice == '1':
        bodies = [
            {'mass':1.0e30, 'pos':[0,0,0],      'vel':[0,1e4,0]},
            {'mass':1.0e30, 'pos':[1e11,0,0],   'vel':[0,-1e4,0]},
            {'mass':1.0e30, 'pos':[0,1e11,0],   'vel':[-1e4,0,0]},
        ]
    elif choice == '2':
        bodies = get_user_bodies()
    elif choice == '3':
        path = input("请输入 JSON 文件路径: ")
        bodies = load_bodies_from_json(path)
    else:
        print("无效选项，退出。")
        sys.exit(1)

    # 可选模拟参数
    try:
        n_steps = int(input("请输入模拟步数 n_steps (回车=5000): ") or 5000)
        dt = float(input("请输入时间步长 dt 秒 (回车=1000): ") or 1e3)
    except ValueError:
        print("输入无效，使用默认 n_steps=5000, dt=1e3")
        n_steps, dt = 5000, 1e3

    print(f"开始模拟: 体数={len(bodies)}, 步数={n_steps}, dt={dt}s")
    traj = simulate(bodies, n_steps=n_steps, dt=dt)

    # 自动缩放
    all_x = traj[...,0]
    all_y = traj[...,1]
    xmin, xmax = all_x.min(), all_x.max()
    ymin, ymax = all_y.min(), all_y.max()
    dx, dy = xmax-xmin, ymax-ymin
    margin = 0.05
    plt.figure(figsize=(6,6))
    plt.xlim(xmin - dx*margin, xmax + dx*margin)
    plt.ylim(ymin - dy*margin, ymax + dy*margin)

    # 绘制
    for j in range(len(bodies)):
        plt.plot(traj[:,j,0], traj[:,j,1], label=f"Body {j+1}")
    plt.legend()
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Three-Body Static Simulation")
    plt.axis('equal')

    out = "three_body_static.png"
    plt.savefig(out, dpi=150)
    print(f"模拟结果已保存到 {out}")
