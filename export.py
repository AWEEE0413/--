"""
Exporting(mixed_filename)
    0 -> Choosing(audio_filename)

"""

import pygame
import sys
import subprocess


# 初始化 Pygame
pygame.init()
pygame.display.init()

# 設定視窗大小
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Exporting Game")

# 獲得混音後的音頻文件
mixed_filename = sys.argv[1]

# 在pygame顯示mixed_filename
font = pygame.font.Font(None, 36)
text = font.render(mixed_filename, True, (255, 255, 255))
text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
window_surface.blit(text, text_rect)
pygame.display.flip()


exporting = True  # 用於追蹤是否正在導出
while exporting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exporting = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                subprocess.Popen(["python3", "choose.py"])
                # 選擇歌曲
                pygame.quit()
