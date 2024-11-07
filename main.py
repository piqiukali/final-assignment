import pygame
import random

# 初始化Pygame
pygame.init()

# 设置屏幕尺寸
screen_width, screen_height = 900, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# 字体设置
font = pygame.font.SysFont("monospace", 35)

# 玩家设置
player_size = 50
player_pos = [screen_width // 2, screen_height // 2]

# 敌人设置
enemy_size = 50
enemy_pos = [random.randint(0, screen_width - enemy_size), random.randint(0, screen_height - enemy_size)]
enemy_speed = [random.choice([-5, 5]), random.choice([-5, 5])]

# 加载背景图片
background_image = pygame.image.load("image/background.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# 时钟
clock = pygame.time.Clock()

def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                intro = False

        # 绘制背景图片
        screen.blit(background_image, (0, 0))
        
          # 绘制按钮
        draw_button("Start Game", screen_width // 2 - 100, screen_height // 2 - 25, 200, 50, green, red, game_loop)

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