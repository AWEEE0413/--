"""
Recording(audio_filename)
        0 -> Choosing(audio_filename)
        1 -> Recording(audio_filename)
        done -> Previewing(audio_filename, mixed_filename)

"""

import pygame
import pyaudio
import wave
from datetime import datetime
import os
from pydub import AudioSegment
import sys
from choose import play_song


# 初始化 Pygame
pygame.init()
pygame.display.init()

# 設定視窗大小
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Recording Game")

# 初始化 PyAudio
p = pyaudio.PyAudio()

# 設定錄音參數
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 30

# 開始錄音
stream = p.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)
# 撥放歌曲

# 開始錄音後播放歌曲
import sys

# 获取选定的歌曲路径
selected_song = sys.argv[1]

# 使用选定的歌曲路径进行后续操作
pygame.mixer.music.load(selected_song)
pygame.mixer.music.play()
print("* 開始錄音")

frames = []

# 開始錄音時間
start_time = pygame.time.get_ticks()

# 監聽按鍵事件
recording = True
while recording:
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000  # 轉換為秒

    print(f"已錄音時長：{elapsed_time} 秒")

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # 按下 r 鍵停止錄音
                recording = False

    if elapsed_time >= RECORD_SECONDS:
        recording = False
    data = stream.read(CHUNK)
    frames.append(data)

    # 顯示已錄音的時間
    window_surface.fill((0, 0, 0))  # 清除畫面
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"recording：{elapsed_time:.1f} s", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    window_surface.blit(text, text_rect)  # 顯示文字
    pygame.display.update()  # 更新視窗


print("* 錄音結束")

# 停止錄音
stream.stop_stream()
stream.close()

# 保存錄音結果為 WAV 文件
# 生成時間戳記作為檔名
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# 保存混音結果為 WAV
mixed_audio = b"".join(frames)
wav_output_folder = "output_wav"
if not os.path.exists(wav_output_folder):
    os.makedirs(wav_output_folder)
mixed_audio_path = f"{wav_output_folder}/mixed_audio_{timestamp}.wav"
wf = wave.open(mixed_audio_path, "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(mixed_audio)
wf.close()

# 将 WAV 文件转换为 MP3 文件
mp3_output_folder = "output_mp3"
if not os.path.exists(mp3_output_folder):
    os.makedirs(mp3_output_folder)
mixed_audio_mp3_path = f"{mp3_output_folder}/mixed_audio_{timestamp}.mp3"
mixed_audio_wav = AudioSegment.from_wav(mixed_audio_path)
mixed_audio_wav.export(mixed_audio_mp3_path, format="mp3")

# 載入選擇的歌曲和錄音結果
selected_song_audio = AudioSegment.from_wav(selected_song)
recorded_audio = AudioSegment.from_wav(mixed_audio_path)

# 混音
mixed_audio = selected_song_audio.overlay(recorded_audio)

# 設定輸出資料夾
output_folder = "output_mp3"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 生成時間戳記作為檔名
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# 保存混音結果為 MP3
mixed_audio_mp3_path = f"{output_folder}/mixed_audio_{timestamp}.mp3"
mixed_audio.export(mixed_audio_mp3_path, format="mp3")


# 刪除 WAV 檔案
# os.remove(mixed_audio_path)

# 關閉 Pygame
pygame.quit()
