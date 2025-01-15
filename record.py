import os
import sys
import wave
import alsaaudio
import serial
import threading
from datetime import datetime

# 初始化 Arduino 通訊
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# 錄音參數
device_name = "plughw:1,0"  # USB 音效卡設備名稱
channels = 1
rate = 44100
format = alsaaudio.PCM_FORMAT_S16_LE
periodsize = 1024
frames = []
recording = True

# 初始化音效卡
audio_in = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, device=device_name)
audio_in.setchannels(channels)
audio_in.setrate(rate)
audio_in.setformat(format)
audio_in.setperiodsize(periodsize)

# 播放選擇歌曲
selected_song = sys.argv[1]
os.system(f"mpg123 {selected_song} &")

# LED 閃爍
def led_blink():
    while recording:
        arduino.write(b"LED:BLINK\n")
        time.sleep(0.5)

# 儲存錄音檔案
def save_recording():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_dir = "recordings"
    os.makedirs(output_dir, exist_ok=True)
    filepath = f"{output_dir}/record_{timestamp}.wav"
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
    print(f"Saved recording: {filepath}")

# 錄音邏輯
def record_audio():
    global recording
    blink_thread = threading.Thread(target=led_blink)
    blink_thread.start()
    try:
        while recording:
            length, data = audio_in.read()
            if length:
                frames.append(data)
            if arduino.in_waiting > 0:
                command = arduino.readline().decode().strip()
                if command == "STOP":
                    recording = False
    finally:
        blink_thread.join()
        audio_in.close()
        arduino.write(b"LED:IDLE\n")

if __name__ == "__main__":
    record_audio()
    save_recording()
