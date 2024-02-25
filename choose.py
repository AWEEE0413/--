import pygame
import time
import os
import sys
import subprocess

# 初始化 Pygame
pygame.init()
# 初始化視訊系統
pygame.display.init()

# 設置視窗
win = pygame.display.set_mode((200, 200))
pygame.display.set_caption("Select Song")

# 設置資料夾路徑和歌曲列表
music_folder = "C:./RECSOURCE"
songs = os.listdir(music_folder)[:6]
selected_song_index = None
selected_song = None
song_selected = False  # 用於追蹤是否已經選擇了歌曲

# 播放所選擇的歌曲
def play_song():
    pygame.mixer.music.load(selected_song)
    pygame.mixer.music.play()

# 選擇歌曲
def select_song(index):
    global selected_song_index, selected_song, song_selected
    selected_song_index = index
    selected_song = os.path.join(music_folder, songs[selected_song_index])
    print(f"Selected song: {selected_song}")
    play_song()
    song_selected = True  # 設置歌曲已選擇
'''
def get_selected_song():
    # 在這裡返回選擇的歌曲路徑
    return selected_song

# 播放下一首歌曲
def play_next_song():
    global selected_song_index
    selected_song_index = (selected_song_index + 1) % len(songs)
    select_song(selected_song_index)
'''

# 主迴圈
def main_loop():
    global song_selected
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    select_song(0)
                elif event.key == pygame.K_2:
                    select_song(1)
                elif event.key == pygame.K_3:
                    select_song(2)
                elif event.key == pygame.K_4:
                    select_song(3)
                elif event.key == pygame.K_5:
                    select_song(4)
                elif event.key == pygame.K_6:
                    select_song(5)
                elif event.key == pygame.K_r and song_selected:
                    # 開啟 record.py
                    subprocess.Popen(["python3", "record.py", selected_song])
                    # 退出 Pygame
                    pygame.quit()
                    sys.exit()
        if pygame.mixer.music.get_busy() == 0 and selected_song is not None:
            play_song()
        # 更新視窗
        pygame.display.flip()

# 呼叫主迴圈
if __name__ == "__main__":
    main_loop()

# 關閉 Pygame
pygame.quit()


