import sys
import pygame
import json
import numpy as np
from three_body import Body, step

# 常量
SCALE_INIT = 1e-9     # 初始缩放比例: 物理坐标 (m) -> 屏幕像素
TIMESTEP = 15000       # 每步时间（秒）
WINDOW_SIZE = 1500
FPS = 60              # 帧率上限

# 颜色列表
COLOR_LIST = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100), (255, 100, 255), (100, 255, 255)]

# 加载 JSON 数据并格式化
def load_bodies_from_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    bodies = []
    for idx, entry in enumerate(data):
        pos = entry.get('position', entry.get('pos'))
        vel = entry.get('velocity', entry.get('vel'))
        color = tuple(entry.get('color', COLOR_LIST[idx % len(COLOR_LIST)]))
        b = Body()
        b.mass = entry['mass']
        b.pos = [float(pos[0]), float(pos[1]), 0.0]
        b.vel = [float(vel[0]), float(vel[1]), 0.0]
        bodies.append({'obj': b, 'color': color, 'trail': [], 'show_trail': True})
    return bodies

# 终端输入天体
def get_user_bodies():
    n = int(input("请输入天体数量："))
    bodies = []
    for i in range(n):
        print(f"第 {i+1} 个天体：")
        m = float(input("  质量 (kg): "))
        px, py = map(float, input("  位置 x y (m): ").split())
        vx, vy = map(float, input("  速度 vx vy (m/s): ").split())
        color = tuple(map(int, input("  颜色 R G B: ").split()))
        b = Body()
        b.mass = m
        b.pos = [px, py, 0.0]
        b.vel = [vx, vy, 0.0]
        bodies.append({'obj': b, 'color': color, 'trail': [], 'show_trail': True})
    return bodies

# 主模拟函数
def run_simulation(bodies):
    # 在用户输入后再初始化 Pygame 窗口
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Interactive Three-Body Simulation (C++ Step)")
    font = pygame.font.SysFont("consolas", 20)
    clock = pygame.time.Clock()

    paused = False
    scale = SCALE_INIT
    center = np.array([WINDOW_SIZE//2, WINDOW_SIZE//2], dtype=float)
    time_elapsed = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_UP:
                    scale *= 1.2
                elif event.key == pygame.K_DOWN:
                    scale /= 1.2
                elif event.key == pygame.K_t:
                    for entry in bodies:
                        entry['show_trail'] = not entry['show_trail']

        if not paused:
            # 调用 C++ step
            c_bodies = [entry['obj'] for entry in bodies]
            step(c_bodies, TIMESTEP)
            time_elapsed += TIMESTEP
            # 更新轨迹
            for entry in bodies:
                b = entry['obj']
                x, y = b.pos[0], b.pos[1]
                screen_pos = center + np.array([x*scale, -y*scale])
                entry['trail'].append(tuple(screen_pos))

        # 绘制
        screen.fill((0, 0, 0))
        for entry in bodies:
            if entry['show_trail'] and len(entry['trail']) > 1:
                pygame.draw.lines(screen, entry['color'], False, entry['trail'], 2)
        for idx, entry in enumerate(bodies):
            if entry['trail']:
                sx, sy = entry['trail'][-1]
                pygame.draw.circle(screen, entry['color'], (int(sx), int(sy)), 5)
                v = np.linalg.norm(entry['obj'].vel) / 1000  # km/s
                txt = font.render(f"v{idx+1}={v:.2f}km/s", True, entry['color'])
                screen.blit(txt, (10, 10 + idx*18))
        time_txt = font.render(f"Time={time_elapsed/3600:.1f}h", True, (255,255,255))
        screen.blit(time_txt, (WINDOW_SIZE-160, 10))
        status_txt = font.render(f"{'Paused' if paused else 'Running'}", True, (200,200,200))
        screen.blit(status_txt, (WINDOW_SIZE-160, 30))
        hint_txt = font.render("Space:Pause/Run  Up/Down:Zoom  T:Toggle Trail", True, (200,200,200))
        screen.blit(hint_txt, (10, WINDOW_SIZE-20))

        pygame.display.flip()
        clock.tick(FPS)

# 脚本入口
if __name__ == '__main__':
    print("选择输入方式：1-终端输入  2-JSON 文件读取")
    choice = input("请输入 1 或 2: ")
    if choice.strip() == '1':
        bodies = get_user_bodies()
    elif choice.strip() == '2':
        filepath = input("请输入 JSON 文件路径: ")
        bodies = load_bodies_from_json(filepath)
    else:
        print("输入无效，程序退出。")
        sys.exit(1)
    # 用户完成输入后再弹出模拟窗口
    run_simulation(bodies)

