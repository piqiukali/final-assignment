import pygame
import random
import time
import os

# 初始化Pygame
pygame.init()

# 设置屏幕尺寸
screen_width, screen_height = 900, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置图片路径（相对路径）
base_dir = os.path.dirname(__file__)  # 获取当前文件的目录
image_dir = os.path.join(base_dir, 'assets', 'images')  # 图片文件夹路径

# 加载背景音乐
pygame.mixer.music.load(os.path.join(image_dir, 'background_music.mp3'))  # 替换为相对路径
pygame.mixer.music.play(-1)

# 加载图片
background_image = pygame.image.load(os.path.join(image_dir, 'background_image.jpg'))  # 游戏背景
player_image = pygame.image.load(os.path.join(image_dir, 'player_image.png'))  # 玩家图片
enemy_image = pygame.image.load(os.path.join(image_dir, 'enemy_image.png'))  # 敌人图片
success_image = pygame.image.load(os.path.join(image_dir, 'success_image.png'))  # 成功结束页面图片
game_over_image = pygame.image.load(os.path.join(image_dir, 'game_over_image.JPG'))  # 游戏结束页面图片

# 定义颜色
black = (0, 0, 0)
green = (0, 255, 0)

# 字体设置
font = pygame.font.SysFont("monospace", 35)

# 玩家设置
player_size = 50
player_pos = [screen_width // 2, screen_height // 2]
player_health = 3  # 玩家血条数量

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

def display_health():
    for i in range(player_health):
        pygame.draw.rect(screen, green, (10 + i * 60, 10, 50, 20))

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                intro = False

        screen.blit(background_image, (0, 0))
        draw_button("Start Simple Level", screen_width // 2 - 150, screen_height // 2 - 75, 300, 50, green, (255, 0, 0), simple_level)

        pygame.display.update()
        pygame.time.Clock().tick(15)

def simple_level():
    global player_pos, player_health
    player_pos = [screen_width // 2, screen_height // 2]
    enemy_size = 50
    enemy_pos = [random.randint(0, screen_width - enemy_size), random.randint(0, screen_height - enemy_size)]
    enemy_speed = [random.choice([-5, 5]), random.choice([-5, 5])]

    clock = pygame.time.Clock()
    game_over = False
    start_time = time.time()

    while not game_over:
        elapsed_time = time.time() - start_time
        remaining_time = 20 - int(elapsed_time)
        if remaining_time <= 0:  # 时间到
            game_over = True
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 10
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
            player_pos[0] += 10
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= 10
        if keys[pygame.K_DOWN] and player_pos[1] < screen_height - player_size:
            player_pos[1] += 10

        enemy_pos[0] += enemy_speed[0]
        enemy_pos[1] += enemy_speed[1]

        if enemy_pos[0] <= 0 or enemy_pos[0] >= screen_width - enemy_size:
            enemy_speed[0] = -enemy_speed[0]
        if enemy_pos[1] <= 0 or enemy_pos[1] >= screen_height - enemy_size:
            enemy_speed[1] = -enemy_speed[1]

        # 碰撞检测
        if (enemy_pos[0] < player_pos[0] < enemy_pos[0] + enemy_size or
            enemy_pos[0] < player_pos[0] + player_size < enemy_pos[0] + enemy_size) and \
                (enemy_pos[1] < player_pos[1] < enemy_pos[1] + enemy_size or
                 enemy_pos[1] < player_pos[1] + player_size < enemy_pos[1] + enemy_size):
            player_health -= 1
            enemy_pos = [random.randint(0, screen_width - enemy_size), random.randint(0, screen_height - enemy_size)]
            if player_health <= 0:
                game_over = True

        screen.fill(black)
        display_health()
        timer_surface = font.render(f"Time Left: {remaining_time}", True, (255, 255, 255))
        timer_rect = timer_surface.get_rect(center=(screen_width // 2, 50))  # 倒计时居中
        screen.blit(timer_surface, timer_rect)

        screen.blit(player_image, (player_pos[0], player_pos[1]))  # 绘制玩家
        screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))  # 绘制敌人

        pygame.display.update()
        clock.tick(30)

    if player_health > 0:
        level_transition("Second Level")
        complex_level()
    else:
        game_over_screen()

def level_transition(level_name):
    transition = True
    while transition:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        screen.fill(black)
        text = font.render(f"Welcome to {level_name}!", True, (255, 255, 255))
        screen.blit(text, (screen_width // 2 - 150, screen_height // 2 - 50))
        text2 = font.render("Get Ready...", True, (255, 255, 255))
        screen.blit(text2, (screen_width // 2 - 100, screen_height // 2 + 10))
        
        pygame.display.update()
        pygame.time.delay(4000)  # 展示4秒后再进入下一关
        transition = False

def complex_level():
    global player_pos, player_health
    player_pos = [screen_width // 2, screen_height // 2]

    enemy_size = 50
    num_enemies = 2
    enemies = []

    for _ in range(num_enemies):
        enemy_pos = [random.randint(0, screen_width - enemy_size), random.randint(0, screen_height - enemy_size)]
        enemy_speed = [random.choice([-3, 3]), random.choice([-3, 3])]
        enemies.append((enemy_pos, enemy_speed))

    clock = pygame.time.Clock()
    game_over = False
    start_time = time.time()

    while not game_over:
        elapsed_time = time.time() - start_time
        remaining_time = 20 - int(elapsed_time)
        if remaining_time <= 0:  # 时间到
            game_over = True
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 10
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
            player_pos[0] += 10
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= 10
        if keys[pygame.K_DOWN] and player_pos[1] < screen_height - player_size:
            player_pos[1] += 10

        for i, (enemy_pos,
        enemy_speed) in enumerate(enemies):
            enemy_pos[0] += enemy_speed[0]
            enemy_pos[1] += enemy_speed[1]

            if enemy_pos[0] <= 0 or enemy_pos[0] >= screen_width - enemy_size:
                enemy_speed[0] = -enemy_speed[0]
            if enemy_pos[1] <= 0 or enemy_pos[1] >= screen_height - enemy_size:
                enemy_speed[1] = -enemy_speed[1]

            if check_collision(player_pos, enemy_pos):
                player_health -= 1
                enemy_pos[0] = random.randint(0, screen_width - enemy_size)  # 重置敌人位置
                if player_health <= 0:
                    game_over = True

        screen.fill(black)
        display_health()
        timer_surface = font.render(f"Time Left: {remaining_time}", True, (255, 255, 255))
        timer_rect = timer_surface.get_rect(center=(screen_width // 2, 50))  # 倒计时居中
        screen.blit(timer_surface, timer_rect)

        for enemy in enemies:
            screen.blit(enemy_image, (enemy[0][0], enemy[0][1]))  # 绘制敌人
        screen.blit(player_image, (player_pos[0], player_pos[1]))  # 绘制玩家

        pygame.display.update()
        clock.tick(30)

    if player_health > 0:
        success_screen()
    else:
        game_over_screen()

def check_collision(player_pos, obj_pos):
    return (obj_pos[0] < player_pos[0] < obj_pos[0] + player_size or
            obj_pos[0] < player_pos[0] + player_size < obj_pos[0] + player_size) and \
           (obj_pos[1] < player_pos[1] < obj_pos[1] + player_size or
            obj_pos[1] < player_pos[1] + player_size < obj_pos[1] + player_size)

def success_screen():
    screen.blit(success_image, (0, 0))  # 绘制成功页面图片
    draw_button("Restart", screen_width // 2 - 150, screen_height // 2 + 10, 130, 50, (0, 255, 0), (255, 0, 0), game_intro)
    draw_button("Quit", screen_width // 2 + 20, screen_height // 2 + 10, 130, 50, (0, 255, 0), (255, 0, 0), quit_game)
    pygame.display.update()
    wait_for_action()

def game_over_screen():
    screen.blit(game_over_image, (0, 0))  # 绘制游戏结束页面图片
    draw_button("Restart", screen_width // 2 - 150, screen_height // 2 + 10, 130, 50, (0, 255, 0), (255, 0, 0), game_intro)
    draw_button("Quit", screen_width // 2 + 20, screen_height // 2 + 10, 130, 50, (0, 255, 0), (255, 0, 0), quit_game)
    pygame.display.update()
    wait_for_action()

def wait_for_action():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def quit_game():
    pygame.quit()
    quit()  # 退出游戏

# 运行游戏
game_intro()
