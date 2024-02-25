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
pygame.display.set_caption('Recording Game')

# 初始化 PyAudio
p = pyaudio.PyAudio()

# 設定錄音參數
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 30  # 預設錄音時間為 30 秒

# 創建音樂播放器
pygame.mixer.init()

# 初始化變數
points = 0
recording = False
recorded_audio = None

# 設定按鍵
R_KEY = pygame.K_r

# 開始錄音
def start_recording():
    global recording
    recording = True

    # 使用選擇的歌曲路徑進行後續操作
    play_song()

    # 播放音樂的同時，播放錄音
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)
    stream.write(recorded_audio)

    # 等待音樂播放完畢
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # 停止錄音
    stream.stop_stream()
    stream.close()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)
    frames = []
    stream.start_stream()
    return stream, frames

frames = []

# 處理音訊流的 callback 函式
def callback(in_data, frame_count, time_info, status):
    global frames
    frames.append(in_data)  # 將讀取的音訊加入 frames 中
    return in_data, pyaudio.paContinue

# 在播放音樂的地方初始化 music_stream
music_stream = p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      output=True)
music_stream.start_stream()

# 在錄音的地方初始化 stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=callback)
stream.start_stream()

'''
#檢查selected_song是否有效
if os.path.isfile(selected_song):
    mix_and_save(recorded_audio, selected_song)
else:
    print(f"{selected_song} is not a valid file path.")
'''

def mix_and_save(recorded_audio, selected_song):
    
    # 生成時間戳記作為檔名
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # 保存混音結果為 WAV
    output_wav_folder = "output_wav"
    if not os.path.exists(output_wav_folder):
        os.makedirs(output_wav_folder)
    mixed_audio_path = f"{output_wav_folder}/mixed_audio_{timestamp}.wav"
    mixed_audio = pygame.mixer.music.get_pos()
    wf = wave.open(mixed_audio_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(mixed_audio)
    wf.close()

    # 保存混音結果為 MP3
    output_mp3_folder = "output_mp3"
    if not os.path.exists(output_mp3_folder):
        os.makedirs(output_mp3_folder)
    mixed_audio_mp3_path = f"{output_mp3_folder}/mixed_audio_{timestamp}.mp3"
    mixed_audio_wav = AudioSegment.from_wav(mixed_audio_path)
    mixed_audio_wav.export(mixed_audio_mp3_path, format="mp3")

    # 刪除 WAV 檔案
    # os.remove(mixed_audio_path)

# 主迴圈
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == R_KEY:
                recorded_audio = start_recording()
                #mix_and_save(recorded_audio, selected_song)
    # 更新視窗
    pygame.display.flip()

# 關閉 Pygame
pygame.quit()



