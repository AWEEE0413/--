import os
import sys
import serial

# 初始化 Arduino 通訊
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

selected_song = sys.argv[1]
mixed_filename = sys.argv[2]

# 播放音效
def play_audio(file):
    os.system(f"mpg123 {file}")

# 主程式
if __name__ == "__main__":
    print("Previewing audio...")
    play_audio(mixed_filename)
    while True:
        if arduino.in_waiting > 0:
            command = arduino.readline().decode().strip()
            if command == "RETRY":
                os.system(f"python3 record.py {selected_song}")
                break
            elif command == "EXPORT":
                os.system(f"python3 export.py {mixed_filename}")
                break
            elif command == "CANCEL":
                os.system("python3 choose.py")
                break
