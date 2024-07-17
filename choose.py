import pygame.mixer
import time
import os
import subprocess
import RPi.GPIO as GPIO

# 初始化 Pygame 混音器
pygame.mixer.init()

# 設置資料夾路徑和歌曲列表
music_folder = "/home/treehole/--/RECSOURCE"
files = os.listdir(music_folder)
songs = sorted([filename for filename in files if filename.startswith(tuple('0123456789'))])

print(songs)
selected_song_index = None
selected_song = None
song_selected = False  # 用於追蹤是否已經選擇了歌曲

# GPIO 設置
GPIO.setmode(GPIO.BCM)
#26七星潭06首 13三棧溪05首 5鯉魚山04首 11撒固兒03首 17石梯坪02首 3瑞穗01首 21錄音
button_pins = [26,13,5,11,17,3,21]
led_pins = [19,6,0,9,4,2,20]

# 設置 LED 為輸出，初始設置為低電平（亮）
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# 增加延遲以確保GPIO設置完成
time.sleep(0.1)

# 設置按鈕為輸入並啟用上拉電阻
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

    # 更新 LED 狀態
    for i, pin in enumerate(led_pins):
        if i == index:
            GPIO.output(pin, GPIO.LOW)  # 亮起對應的LED
        else:
            GPIO.output(pin, GPIO.HIGH)  # 關閉其他LED

def main_loop():
    global song_selected
    running = True

    last_button_press_time = time.time()
    debounce_delay = 0.3  # 去抖動延遲 (秒)

    try:
        while running:
            current_time = time.time()
            if GPIO.input(button_pins[5]) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
                index = 0
                select_song(index)
                last_button_press_time = current_time
            if GPIO.input(button_pins[4]) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
                index = 1
                select_song(index)
                last_button_press_time = current_time
            if GPIO.input(button_pins[3]) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
                index = 2
                select_song(index)
                last_button_press_time = current_time
            if GPIO.input(button_pins[2]) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
                index = 3
                select_song(index)
                last_button_press_time = current_time
            if GPIO.input(button_pins[1]) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
                index = 4
                select_song(index)
                last_button_press_time = current_time
            if GPIO.input(button_pins[0]) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
                index = 5
                select_song(index)
                last_button_press_time = current_time
            if song_selected and GPIO.input(button_pins[6]) == GPIO.LOW and (current_time - last_button_press_time) > debounce_delay:
                print(selected_song)
                subprocess.Popen(["python3", "/home/treehole/--/record.py", selected_song])
                running = False
                last_button_press_time = current_time
            
            # 保持音樂播放狀態
            if not pygame.mixer.music.get_busy() and selected_song is not None:
                play_song()

            time.sleep(0.1)  # 延遲以減少CPU使用率
    except KeyboardInterrupt:
        print("Exiting program")
    finally:
        # 關閉所有 LED
        for pin in led_pins:
            GPIO.output(pin, GPIO.HIGH)
        # 釋放 GPIO
        GPIO.cleanup()

# 呼叫主迴圈
if __name__ == "__main__":
    main_loop()
