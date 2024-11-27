import pygame
import sys

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('The Casual Game')

WHITE = (255, 255, 255)
GREEN = (76, 175, 80)
RED = (244, 67, 54)
BLACK = (0, 0, 0)
BLUE = (33, 150, 243)

font_button = pygame.font.Font(None, 48)

# 加载背景音乐
pygame.mixer.music.load('/Users/liuqianwei/start page/background_music.mp3')  # 确保音乐文件在正确的路径
pygame.mixer.music.play(-1)

# 加载背景图像
background_image = pygame.image.load('/Users/liuqianwei/start page/background_image.jpg')  # 确保背景图文件在正确的路径

# 加载按钮图片
button_image = pygame.image.load('/Users/liuqianwei/start page/start_button.JPG')  # 确保图片文件在正确的路径
button_image = pygame.transform.scale(button_image, (300, 80))  # 调整图片大小
button_rect = button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # 设置图片位置

def main():
    while True:
        # 绘制背景图像
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 检查左键点击
                if button_rect.collidepoint(event.pos):
                    print("按钮被点击！")
                    # 在这里添加开始游戏的代码

        # 绘制按钮图片
        screen.blit(button_image, button_rect.topleft)

        pygame.display.update()

if __name__ == '__main__':
    main()