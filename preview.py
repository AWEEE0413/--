import pygame
import subprocess
import os
import sys
from choose import play_song
import sounddevice as sd
import RPi.GPIO as GPIO

# 初始化 Pygame
pygame.mixer.init()

# 初始化 GPIO
GPIO.setmode(GPIO.BCM)
button_pins = [10,17,3,2] #重錄10 回放17 送出3 取消2
for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 獲得選定的歌曲路徑
selected_song = sys.argv[1]

# 獲得混音後的音頻文件
mixed_filename = sys.argv[2]

# 撥放混音後的音頻文件
pygame.mixer.music.load(mixed_filename)
pygame.mixer.music.play()

previewing = True  # 用於追蹤是否正在預覽
while previewing:
    if GPIO.input(button_pins[0]) == GPIO.LOW:
        # 回到錄音
        subprocess.Popen(["python3", "record.py", selected_song])
        previewing = False
    elif GPIO.input(button_pins[1]) == GPIO.LOW:
        # 回放
        pygame.mixer.music.load(mixed_filename)
        pygame.mixer.music.play()
    elif GPIO.input(button_pins[2]) == GPIO.LOW:
        # 送出
        '''
        #Play the exportingmusic
        pygame.mixer.music.load('exporting.mp3')
        pygame.mixer.music.play()
        time.sleep(3)
        '''
        subprocess.Popen(["python3", "export.py", mixed_filename])
        previewing = False
    
    elif GPIO.input(button_pins[3]) == GPIO.LOW:
        # 取消
        subprocess.Popen(["python3", "choose.py"])
        previewing = False
    
    pygame.time.wait(100)  # 避免頻繁檢查按鈕狀態

# 清理 GPIO
GPIO.cleanup()
