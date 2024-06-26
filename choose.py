import pygame.mixer
import time
import os
import sys
import subprocess
import RPi.GPIO as GPIO

# 初始化 Pygame 混音器
pygame.mixer.init()

# 設置資料夾路徑和歌曲列表
music_folder = "./RECSOURCE"
files = os.listdir(music_folder)
# 过滤出以数字开头的文件名，并按数字排序
songs = sorted([filename for filename in files if filename.startswith(tuple('0123456789'))])

# 如果文件名是 01.mp3 到 06.mp3 形式，songs 现在应该是 ['01.mp3', '02.mp3', ..., '06.mp3']

print(songs)
selected_song_index = None
selected_song = None
song_selected = False  # 用於追蹤是否已經選擇了歌曲

# GPIO 設置
GPIO.setmode(GPIO.BCM)
#22七星潭06首 27三棧溪05首 17鯉魚山04首 4撒固兒03首 3石梯坪02首 2瑞穗01首 10錄音
button_pins = [2,3,4,17,27,22,10]
for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 播放所選擇的歌曲
def play_song():
    if selected_song:
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

def main_loop():
    global song_selected
    running = True
    index = 0  # 默认值

    if len(sys.argv) > 1:
        index = int(sys.argv[1])
        select_song(index)
        song_selected = True

    last_button_press_time = time.time()
    debounce_delay = 0.3  # 去抖動延遲 (秒)

    while running:
        current_time = time.time()
        if GPIO.input(button_pins[0]) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
            index = 0
            select_song(index)
            last_button_press_time = current_time
        if GPIO.input(button_pins[1]) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
            index = 1
            select_song(index)
            last_button_press_time = current_time
        if GPIO.input(button_pins[2]) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
            index = 2
            select_song(index)
            last_button_press_time = current_time
        if GPIO.input(button_pins[3]) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
            index = 3
            select_song(index)
            last_button_press_time = current_time
        if GPIO.input(button_pins[4]) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
            index = 4
            select_song(index)
            last_button_press_time = current_time
        if GPIO.input(button_pins[5]) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
            index = 5
            select_song(index)
            last_button_press_time = current_time
        if song_selected and GPIO.input(button_pins[6]) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
            print(selected_song)
            subprocess.Popen(["python3", "record.py", selected_song])
            running = False
            last_button_press_time = current_time
        
        # 保持音樂播放狀態
        if not pygame.mixer.music.get_busy() and selected_song is not None:
            play_song()

        time.sleep(0.1)  # 延遲以減少CPU使用率
    
    # 釋放 GPIO
    GPIO.cleanup()

# 呼叫主迴圈
if __name__ == "__main__":
    main_loop()
