'''import alsaaudio

# 列出可用的錄音設備
print(alsaaudio.cards())
'''
import alsaaudio
import wave
import numpy as np

# 設定錄音參數
device = 'default'
channels = 1
rate = 44100
format = alsaaudio.PCM_FORMAT_S16_LE
periodsize = 1024

# 開啟音訊輸入
audio_in = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL,
                         channels=channels, rate=rate, format=format, periodsize=periodsize)
print("錄音開始...")

frames = []

# 錄音
for _ in range(rate // periodsize * 5):  # 設定錄製的音訊長度為 5 秒
    length, data = audio_in.read()
    if length:
        frames.append(data)

# 停止錄音
audio_in.close()

# 將錄音資料寫入檔案
with wave.open('output.wav', 'wb') as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(2)
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))

print("音訊已儲存至 output.wav")
print("錄音結束.")

