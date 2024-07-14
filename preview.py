import os
import subprocess
import sys
import time
import threading
import pygame
import RPi.GPIO as GPIO

# 切换到脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# 初始化 Pygame
pygame.mixer.init()

# 初始化 GPIO
GPIO.setmode(GPIO.BCM)
button_pins = [27, 10, 11, 5]  # 回放27 重錄10  送出11 取消5
led_pins = [22, 9, 0, 6]      # 对应LED引脚

for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)

# 设置LED状态
GPIO.output(led_pins[0], GPIO.HIGH)  # 重錄 LED 恆亮
GPIO.output(led_pins[2], GPIO.HIGH)  # 送出 LED 恆亮
GPIO.output(led_pins[3], GPIO.HIGH)  # 取消 LED 恆亮

# 获取选定的歌曲路径
selected_song = sys.argv[1]

# 获取混音后的音频文件
mixed_filename = sys.argv[2]

# 播放混音后的音频文件
pygame.mixer.music.load(mixed_filename)
pygame.mixer.music.play()

# 定义回放 LED 闪烁函数
def flash_led(pin):
    while previewing:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.5)

# 启动回放 LED 闪烁线程
previewing = True
flash_thread = threading.Thread(target=flash_led, args=(led_pins[0],))
flash_thread.start()

try:
    while previewing:
        if GPIO.input(button_pins[0]) == GPIO.LOW:
            # 回放
            pygame.mixer.music.load(mixed_filename)
            pygame.mixer.music.play()
        elif GPIO.input(button_pins[1]) == GPIO.LOW:
            # 回到录音
            subprocess.Popen(["python3", os.path.join(script_dir, "record.py"), selected_song])
            previewing = False
        elif GPIO.input(button_pins[2]) == GPIO.LOW:
            # 送出
            subprocess.Popen(["python3", os.path.join(script_dir, "export.py"), mixed_filename])
            previewing = False
        elif GPIO.input(button_pins[3]) == GPIO.LOW:
            # 取消
            subprocess.Popen(["python3", os.path.join(script_dir, "choose.py")])
            previewing = False
        
        time.sleep(0.1)  # 避免频繁检查按钮状态

finally:
    # 确保清理 GPIO 和停止闪烁线程
    previewing = False
    flash_thread.join()
    GPIO.cleanup()
