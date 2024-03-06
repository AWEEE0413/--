"""
  Previewing(audio_filename, mixed_filename)
        0 -> Choosing(audio_filename)
        1 -> Recording(audio_filename)
        2 -> Exporting(mixed_filename)
        3 -> Previewing(audio_filename, mixed_filename)

"""

import pygame
import subprocess
import os
import sys
from choose import play_song
import sounddevice as sd
import keyboard
from datetime import datetime

# 初始化 Pygame
pygame.init()
pygame.display.init()

# 設定視窗大小
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("previewing Game")

# 獲得選定的歌曲路徑
selected_song = sys.argv[1]

# 獲得混音後的音頻文件
mixed_filename = sys.argv[2]

# 撥放混音後的音頻文件
pygame.mixer.music.load(mixed_filename)
pygame.mixer.music.play()

previewing = True  # 用於追蹤是否正在預覽
while previewing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            previewing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                subprocess.Popen(["python3", "record.py", selected_song])
                # 回到錄音
                pygame.quit()
            elif event.key == pygame.K_e:
                subprocess.Popen(["python3", "export.py", mixed_filename])
                # 導出錄音
                pygame.quit()
            elif event.key == pygame.K_p:
                # replay
                pygame.mixer.music.load(mixed_filename)
                pygame.mixer.music.play()
            elif event.key == pygame.K_c:
                subprocess.Popen(["python3", "choose.py"])
                # 選擇歌曲
                pygame.quit()
