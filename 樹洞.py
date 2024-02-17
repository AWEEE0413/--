import os
import keyboard
import pygame
import threading
from pydub import AudioSegment
import sounddevice as sd
import soundfile as sf
from datetime import datetime
import logging
import PLAYER
import REC
import mixed
def play_music_thread(song):
    logging.debug("播放音乐线程开始")
    PLAYER.play_song(song)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    logging.debug("播放音乐线程结束")

def record_audio_thread(duration):
    logging.debug("录音线程开始")
    REC.record_audio(duration)
    logging.debug("录音线程结束")

def setup_hotkeys():
    song = "path/to/your/song.mp3"
    logging.debug("设置快捷键...")

    keyboard.add_hotkey('P', lambda: threading.Thread(target=play_music_thread, args=(song,)).start())
    keyboard.add_hotkey('R', lambda: threading.Thread(target=record_audio_thread, args=(10,)).start())

    logging.debug("快捷键设置完成。按 'P' 播放音乐，按 'R' 开始录音。")

setup_hotkeys()

logging.info("请按 'P' 键同时开始播放音乐和录音...")
try:
    while True:
        pass
except KeyboardInterrupt:
    logging.info("程序终止。")

    
# 配置日誌系統，將日誌信息輸出到文件，並添加時間戳
logging.basicConfig(level=logging.DEBUG,
                    filename='app.log',  # 日誌文件名
                    filemode='a',  # 'a' 表示追加模式，'w' 表示覆蓋模式
                    format='%(asctime)s - %(levelname)s - %(message)s')  # 日誌格式

