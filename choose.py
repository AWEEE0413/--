import time
import os
import serial

# 初始化 Arduino 通訊
arduino = serial.Serial('COM3', 9600, timeout=1)  # 修改為 Arduino 的 COM 埠
time.sleep(2)

# 設置資料夾路徑和歌曲列表
music_folder = "RECSOURCE"
files = os.listdir(music_folder)
songs = sorted([filename for filename in files if filename.startswith(tuple('0123456789'))])

selected_song_index = None
selected_song = None

# 播放所選歌曲
def play_song():
    if selected_song:
        print(f"Playing: {selected_song}")

# 選擇歌曲
def select_song(index):
    global selected_song_index, selected_song
    selected_song_index = index
    selected_song = os.path.join(music_folder, songs[selected_song_index])
    print(f"Selected song: {selected_song}")
    play_song()
    arduino.write(f"LED:{index}\n".encode())

# 主程式
def main_loop():
    while True:
        if arduino.in_waiting > 0:
            button_data = arduino.readline().decode().strip()
            if button_data.startswith("BTN:"):
                button_index = int(button_data.split(":")[1])
                select_song(button_index)
            elif button_data == "RECORD":
                print("Recording started.")
                os.system(f"python3 record.py {selected_song}")
                break

if __name__ == "__main__":
    main_loop()
