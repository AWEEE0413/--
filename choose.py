import pygame
import time
import os
import sys
import subprocess
import pygame.mixer
import RPi.GPIO as GPIO

# 初始化 Pygame.mixer
pygame.mixer.init()

# 初始化 GPIO
GPIO.setmode(GPIO.BCM)
button_pins = [17, 18, 27, 22, 23, 24, 25]
GPIO.setup(button_pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 設置資料夾路徑和歌曲列表
music_folder = "C:./RECSOURCE"
songs = os.listdir(music_folder)[:6]
selected_song_index = None
selected_song = None
song_selected = False  # 用於追蹤是否已經選擇了歌曲


# 播放所選擇的歌曲
def play_song():
    pygame.mixer.music.load(selected_song)
    pygame.mixer.music.play()
    if not os.path.exists(selected_song):
        print(f"Error: {selected_song} does not exist.")


# 選擇歌曲
def select_song(index):
    global selected_song_index, selected_song, song_selected
    selected_song_index = index
    selected_song = os.path.join(music_folder, songs[selected_song_index])
    print(f"Selected song: {selected_song}")
    play_song()
    song_selected = True  # 設置歌曲已選擇


"""
def get_selected_song():
    # 在這裡返回選擇的歌曲路徑
    return selected_song

# 播放下一首歌曲
def play_next_song():
    global selected_song_index
    selected_song_index = (selected_song_index + 1) % len(songs)
    select_song(selected_song_index)
"""


# 主迴圈
def main_loop():
    global song_selected
    running = True
    index = 0  # 默认值

    if len(sys.argv) > 1:
        index = int(sys.argv[1])
        select_song(index)
        song_selected = True

    while running:
        for i, pin in enumerate(button_pins[:6]):
            if GPIO.input(pin) == GPIO.LOW:
                select_song(i)
                song_selected = True
                time.sleep(0.2)  # 防止按钮抖动

        if song_selected and GPIO.input(button_pins[6]) == GPIO.LOW:  # 检测录音按钮
            print(selected_song)
            # 开启 record.py
            subprocess.Popen(["python3", "record.py", selected_song])
            running = False

        # 这里添加播放歌曲的逻辑
        if selected_song:
            play_song()
            song_selected = False

        time.sleep(0.1)  # 防止 CPU 占用过高

    # 清理 GPIO 引脚设置
    GPIO.cleanup()

# 呼叫主迴圈
if __name__ == "__main__":
    main_loop()

# 關閉 Pygame
pygame.quit()