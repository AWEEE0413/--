import pygame  # 引入 pygame 庫，用於遊戲和多媒體應用的開發
import keyboard  # 引入 keyboard 庫，用於檢測鍵盤事件
import time  # 引入 time 庫，用於時間相關的操作
import os  # 引入 os 庫，用於操作系統相關的功能，如檔案和目錄操作

pygame.init()  # 初始化 pygame 庫

folder_path = "C:\\Users\\kung\\樹洞\\RECSOURCE"  # 指定音樂檔案的路徑

# 從指定的資料夾中找出所有的 mp3 檔案
songs = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.mp3')]
current_song_index = 0  # 設定當前播放的歌曲索引為 0

def play_song(song):  # 定義一個函數用於播放指定的歌曲
    pygame.mixer.music.load(song)  # 加載歌曲
    pygame.mixer.music.play()  # 播放歌曲

def play_next_song():  # 定義一個函數用於播放下一首歌曲
    global current_song_index  # 使用 global 關鍵字來指示 current_song_index 是一個全局變量
    current_song_index = (current_song_index + 1) % len(songs)  # 計算下一首歌曲的索引
    play_song(songs[current_song_index])  # 播放下一首歌曲

def setup_music_end_event():  # 定義一個函數用於設定音樂結束事件
    pygame.mixer.music.set_endevent(pygame.USEREVENT)  # 當一首歌曲播放結束時，pygame 會觸發一個 USEREVENT 事件
    pygame.event.set_allowed(pygame.USEREVENT)  # 允許 USEREVENT 事件被觸發


setup_music_end_event()  # 設定音樂結束事件
def play_current_song():  # 定义一个函数用于播放当前歌曲
    global current_song_index  # 声明 current_song_index 为全局变量
    play_song(songs[current_song_index])  # 播放当前索引指向的歌曲


while True:  # 進入無窮迴圈
    for event in pygame.event.get():  # 從事件隊列中取出所有事件
        if event.type == pygame.USEREVENT:  # 如果事件的類型是 USEREVENT
            play_next_song()  # 歌曲播放結束，播放下一首歌曲
            if current_song_index >= len(songs):  # 檢查是否播放到最後一首歌曲
                pygame.quit()  # 關閉 Pygame
                quit()  # 退出程式

    if keyboard.is_pressed('p'):  # 如果 'p' 键被按下
        play_next_song()  # 播放下一首歌曲
        time.sleep(0.2)  # 暂停 0.2 秒，以避免重复快速触发
        
    if keyboard.is_pressed('r'):  # 如果 'r' 键被按下
        play_current_song()  # 重新播放当前歌曲
        time.sleep(0.2)  # 暂停 0.2 秒，以避免重复快速触发