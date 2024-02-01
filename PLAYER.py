import os
import keyboard

def play_next_song(folder_path):
    """
    Plays the next song in the folder.
    """
    # 在播放下一首歌曲之前顯示歌名
    display_song_name()
    
    # 播放下一首歌曲的程式碼
    song_list = os.listdir(folder_path)
    # Add your logic to play the next song from the song_list
    
def display_song_name():
    """
    Displays the name of the current song.
    """
    # 顯示歌名的程式碼
    pass

folder_path = r"C:\Users\kung\樹洞\PY"  # Replace with the actual folder path
keyboard.add_hotkey('c', lambda: (play_next_song(folder_path), display_song_name()))
keyboard.wait('esc')
