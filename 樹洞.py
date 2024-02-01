import os
import keyboard
import pygame
from pydub import AudioSegment
import sounddevice as sd
import soundfile as sf
from datetime import datetime

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

def display_song_name(song_path):#顯示歌名
    """
    Displays the name of the current song.
    """
    song_name = os.path.basename(song_path)
    print("Now playing: ", song_name)

folder_path = "C:\\Users\\kung\\樹洞\\PY"  # Replace with the actual folder path
keyboard.add_hotkey('c', lambda: play_next_song(folder_path))
keyboard.wait('esc')


def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

def record_audio(duration=10, buffering=44100):
    # 錄音功能，持續指定的秒數
    print("Press A to start recording and monitoring...")
    keyboard.wait('A')  # Wait for the 'A' key to be pressed
    print("Recording and monitoring...")
    with sd.Stream(callback=callback):
        myrecording = sd.rec(int(duration * buffering), samplerate=buffering, channels=2)
        sd.wait()
    print("Recording and monitoring finished")
    return myrecording

#def save_recording(recording, filename):
    # 將錄音保存為文件
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    wav_file = f"C:\\Users\\kung\\樹洞\\{filename}_{timestamp}.wav"
    sf.write(wav_file, recording, 44100)

    # Convert the WAV file to MP3
    audio = AudioSegment.from_wav(wav_file)

    # Normalize the audio to -20 dB
    normalized_audio = audio.normalize(headroom=20.0)
    
    # Increase the volume
    increased_volume_audio = normalized_audio.apply_gain(20) # Increase volume by 20 dB

    mp3_file = f"C:\\Users\\kung\\樹洞\\{filename}_{timestamp}.mp3" 
    normalized_audio.export(mp3_file, format="mp3", bitrate="320k")

    # Remove the WAV file
    os.remove(wav_file)
def mix_audio(song_path, recording):
    # Load the song
    song = AudioSegment.from_file(song_path)

    # Convert the recording to an AudioSegment
    recording_segment = AudioSegment(
        recording.tobytes(), 
        frame_rate=44100,
        sample_width=recording.dtype.itemsize, 
        channels=2
    )

    # Mix the song and the recording
    mixed = song.overlay(recording_segment)

    # Save the mixed audio
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    mixed.export("mixed_audio.mp3", format="mp3")


recorded_audio = record_audio(duration=10)
save_recording(recorded_audio, "recorded_audio")