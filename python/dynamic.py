import sys
import pygame
import numpy as np
from three_body import Body, step

# ----- 模拟参数 -----
WIDTH, HEIGHT = 800, 800      # 窗口大小
BG_COLOR = (0, 0, 0)         # 背景颜色
BODY_COLORS = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
RADIUS = 5                   # 绘制质点半径

# 初始化三体
bodies = [
    Body(1e30, [0, 0, 0], [0, 1e4, 0]),
    Body(1e30, [1e11, 0, 0], [0, -1e4, 0]),
    Body(1e30, [0, 1e11, 0], [-1e4, 0, 0]),
]

# 轨迹存储
trajectories = [[[], []] for _ in bodies]

def world_to_screen(pos, center, scale):
    """
    将物理坐标转换为屏幕坐标
    :param pos: [x, y] 物理坐标
    :param center: 屏幕中心点(x, y)
    :param scale: 缩放因子 (m -> px)
    """
    x = center[0] + pos[0] * scale
    y = center[1] - pos[1] * scale
    return int(x), int(y)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Three-Body Dynamic Simulation")
    clock = pygame.time.Clock()

    # 选定将世界坐标映射到屏幕
    center = (WIDTH // 2, HEIGHT // 2)
    scale = 3e-12  # 缩放因子: 1m -> 3e-12px，可以根据需要调节
    dt = 1e3       # 每帧时间步长 (秒)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 推进模拟一步
        step(bodies, dt)

        # 更新轨迹
        for i, b in enumerate(bodies):
            trajectories[i][0].append(b.pos[0])
            trajectories[i][1].append(b.pos[1])

        # 绘制
        screen.fill(BG_COLOR)

        # 绘制轨迹
        for i, traj in enumerate(trajectories):
            pts = [world_to_screen((traj[0][j], traj[1][j]), center, scale) 
                   for j in range(len(traj[0]))]
            if len(pts) > 1:
                pygame.draw.lines(screen, BODY_COLORS[i], False, pts, 1)

        # 绘制质点
        for i, b in enumerate(bodies):
            pos = world_to_screen((b.pos[0], b.pos[1]), center, scale)
            pygame.draw.circle(screen, BODY_COLORS[i], pos, RADIUS)

        pygame.display.flip()
        clock.tick(60)  # 限制帧率为60FPS

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

