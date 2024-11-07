import pygame
import random

# 初始化Pygame
pygame.init()

# 设置屏幕尺寸
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# 字体设置
font = pygame.font.SysFont("monospace", 35)

# 玩家设置
player_size = 50
player_pos = [screen_width // 2, screen_height // 2]

# 敌人设置
enemy_size = 50
enemy_pos = [random.randint(0, screen_width - enemy_size), random.randint(0, screen_height - enemy_size)]
enemy_speed = [random.choice([-5, 5]), random.choice([-5, 5])]

# 时钟
clock = pygame.time.Clock()
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                intro = False

        screen.fill(black)
        text = font.render("Press any key to start", True, white)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
        pygame.display.update()
        clock.tick(15)

def game_loop():
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
 # 获取按键
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 10
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
            player_pos[0] += 10
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= 10
        if keys[pygame.K_DOWN] and player_pos[1] < screen_height - player_size:
            player_pos[1] += 10

        # 更新敌人位置
        enemy_pos[0] += enemy_speed[0]
        enemy_pos[1] += enemy_speed[1]

        # 碰到边界反弹
        if enemy_pos[0] <= 0 or enemy_pos[0] >= screen_width - enemy_size:
            enemy_speed[0] = -enemy_speed[0]
        if enemy_pos[1] <= 0 or enemy_pos[1] >= screen_height - enemy_size:
            enemy_speed[1] = -enemy_speed[1]

        # 检测碰撞
        if (enemy_pos[0] < player_pos[0] < enemy_pos[0] + enemy_size or
            enemy_pos[0] < player_pos[0] + player_size < enemy_pos[0] + enemy_size) and \
                (enemy_pos[1] < player_pos[1] < enemy_pos[1] + enemy_size or
                 enemy_pos[1] < player_pos[1] + player_size < enemy_pos[1] + enemy_size):
            game_over = True
             # 绘制
        screen.fill(black)
        pygame.draw.rect(screen, red, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
        pygame.draw.rect(screen, white, (player_pos[0], player_pos[1], player_size, player_size))

        # 更新屏幕
        pygame.display.update()

        # 控制帧率
        clock.tick(30)

    pygame.quit()

# 运行游戏
game_intro()
game_loop()