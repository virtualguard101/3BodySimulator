import pygame
import numpy as np

pygame.init()

# 模拟参数
G = 6.67430e-11  # 万有引力常数
dt = 18000  # 时间步长（秒）

# 获取用户输入天体信息
def get_user_defined_bodies():
    bodies = []
    try:
        n = int(input("请输入模拟的天体数量（建议3）："))
    except ValueError:
        n = 3
    for i in range(n):
        print(f"\n天体 {i+1} 参数：")
        mass = float(input("质量 (kg): "))
        pos = list(map(float, input("位置 x y z (米, 用空格分隔): ").split()))
        vel = list(map(float, input("速度 vx vy vz (米/秒, 用空格分隔): ").split()))
        color = tuple(np.random.randint(100, 256, size=3))
        bodies.append({
            "mass": mass,
            "pos": np.array(pos, dtype='float64'),
            "vel": np.array(vel, dtype='float64'),
            "color": color,
            "trail": []
        })
    return bodies

# 默认参数
default_bodies = [
    {
        "mass": 1.989e30,
        "pos": np.array([0, 0, 0], dtype='float64'),
        "vel": np.array([0, 1e4, 0], dtype='float64'),
        "color": (255, 100, 100),
        "trail": []
    },
    {
        "mass": 1.989e30,
        "pos": np.array([1e11, 0, 0], dtype='float64'),
        "vel": np.array([0, -1e4, 0], dtype='float64'),
        "color": (100, 255, 100),
        "trail": []
    },
    {
        "mass": 1.989e30,
        "pos": np.array([0, 1e11, 0], dtype='float64'),
        "vel": np.array([-1e4, 0, 0], dtype='float64'),
        "color": (100, 100, 255),
        "trail": []
    }
]

use_default = input("是否使用默认天体参数？(y/n): ").strip().lower()
bodies = default_bodies if use_default == 'y' else get_user_defined_bodies()

# 屏幕设置
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Three-Body Dynamic Simulation (Python Only Step)")

scale = 5e8  # 像素/米
offset = np.array([width // 2, height // 2])

# 引力计算函数
def compute_forces(bodies):
    forces = [np.zeros(3) for _ in bodies]
    for i, body_i in enumerate(bodies):
        for j, body_j in enumerate(bodies):
            if i != j:
                r_vec = body_j["pos"] - body_i["pos"]
                distance = np.linalg.norm(r_vec)
                if distance == 0:
                    continue
                force = G * body_i["mass"] * body_j["mass"] / distance**2
                forces[i] += force * r_vec / distance
    return forces

# 主循环
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))  # 黑色背景

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    forces = compute_forces(bodies)
    for i, body in enumerate(bodies):
        acc = forces[i] / body["mass"]
        body["vel"] += acc * dt
        body["pos"] += body["vel"] * dt

        pixel_pos = (body["pos"][:2] / scale + offset).astype(int)
        body["trail"].append(pixel_pos)

    # 画轨迹
    for body in bodies:
        if len(body["trail"]) > 1:
            pygame.draw.lines(screen, body["color"], False, body["trail"], 1)

    # 画天体
    for body in bodies:
        pixel_pos = (body["pos"][:2] / scale + offset).astype(int)
        pygame.draw.circle(screen, body["color"], pixel_pos, 4)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

