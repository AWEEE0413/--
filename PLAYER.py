import os
import keyboard
import pygame

current_song_index = 0  # 用來追蹤當前播放的歌曲

def play_next_song(folder_path):
    global current_song_index  # 使用全局變數來追蹤當前播放的歌曲

    song_list = os.listdir(folder_path)
    if not song_list:
        print("No songs found in the folder.")
        return

    # 選擇下一首歌曲來播放
    song_path = os.path.join(folder_path, song_list[current_song_index])

    # 在播放下一首歌曲之前顯示歌名
    display_song_name(song_path)

    # 播放下一首歌曲的程式碼
    pygame.mixer.init()
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

    # 更新當前歌曲的索引，以便下次播放下一首歌曲
    current_song_index = (current_song_index + 1) % len(song_list)

def display_song_name(song_path):
    """
    Displays the name of the current song.
    """
    song_name = os.path.basename(song_path)
    print("Now playing: ", song_name)

folder_path = "C:\\Users\\kung\\樹洞\\PY"  # Replace with the actual folder path
keyboard.add_hotkey('c', lambda: play_next_song(folder_path))
keyboard.wait('esc')