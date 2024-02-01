import os
import keyboard
import pygame  # 需要先安裝 pygame 庫，可以使用 pip install pygame 來安裝

def play_next_song(folder_path):
    """
    Plays the next song in the folder.
    """
    song_list = os.listdir(folder_path)
    if not song_list:
        print("No songs found in the folder.")
        return

    # 選擇第一首歌曲來播放
    song_path = os.path.join(folder_path, song_list[0])

    # 在播放下一首歌曲之前顯示歌名
    display_song_name(song_path)

    # 播放下一首歌曲的程式碼
    pygame.mixer.init()
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

def display_song_name(song_path):
    """
    Displays the name of the current song.
    """
    song_name = os.path.basename(song_path)
    print("Now playing: ", song_name)

folder_path = "C:\\Users\\kung\\樹洞\\PY"  # Replace with the actual folder path
keyboard.add_hotkey('c', lambda: play_next_song(folder_path))
keyboard.wait('esc')
