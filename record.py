import os
import sys
import wave
import pygame
import alsaaudio
from datetime import datetime
from pydub import AudioSegment
import subprocess
import RPi.GPIO as GPIO
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
button_pins = [10]
GPIO.setup(button_pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set recording parameters
device = 'plughw:3,0'
channels = 1
rate = 44100
format = alsaaudio.PCM_FORMAT_S16_LE
periodsize = 1024

# Open audio stream for input
audio_in = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL,
                         device=device ,channels=channels, rate=rate, format=format, periodsize=periodsize)


# Get the selected song path from command line argument
selected_song = sys.argv[1]

def start_recording():
    '''
    #Play the beginningmusic
    pygame.mixer.music.load('beginning.mp3')
    pygame.mixer.music.play()
    time.sleep(3.1415926)
    '''
    pygame.mixer.music.load(selected_song)
    pygame.mixer.music.play()

    global frames, start_time, timestamp
    frames = []
    start_time = pygame.time.get_ticks()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    print("* 開始錄音...")

def save_recording():
    print("* 錄音結束...")
    pygame.mixer.music.stop()
    '''
    #Play the endingmusic
    pygame.mixer.music.load('ending.mp3')
    pygame.mixer.music.play()
    time.sleep(3)
    '''
    # Save recording as WAV file
    wav_output_folder = "output_wav"
    os.makedirs(wav_output_folder, exist_ok=True)
    record_audio_path = f"{wav_output_folder}/record_audio_{timestamp}.wav"
    wf = wave.open(record_audio_path, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(2)
    wf.setframerate(rate)
    wf.writeframes(b"".join(frames))
    wf.close()

    # Convert WAV file to MP3
    mp3_output_folder = "output_mp3"
    os.makedirs(mp3_output_folder, exist_ok=True)
    record_audio_mp3_path = f"{mp3_output_folder}/record_audio_{timestamp}.mp3"
    record_audio_wav = AudioSegment.from_wav(record_audio_path)
    record_audio_wav.export(record_audio_mp3_path, format="mp3", bitrate="320k")

    # Load selected song and recorded audio
    global selected_song_audio, recorded_audio
    selected_song_audio = AudioSegment.from_mp3(selected_song)
    recorded_audio = AudioSegment.from_mp3(record_audio_mp3_path)

def mix_audio():
    mixed_audio = recorded_audio.overlay(selected_song_audio)
    final_output_folder = "final_output_mp3"
    os.makedirs(final_output_folder, exist_ok=True)
    mixed_output_mp3_path = f"{final_output_folder}/mixed_audio_{timestamp}.mp3"
    mixed_audio.export(mixed_output_mp3_path, format="mp3", bitrate="320k")
    return mixed_output_mp3_path

def main_loop():
    recording = True
    RECORD_SECONDS = 30

    # 播放音樂
    start_recording()

    while recording:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000
        print(f"錄音中... {elapsed_time:.2f} 秒")

        if elapsed_time >= RECORD_SECONDS:
            recording = False
        if GPIO.input(button_pins[0]) == GPIO.LOW:
            recording = False
        
        length, data = audio_in.read()
        if length:
            frames.append(data)
        
        time.sleep(0.01)  # 加入短暫延遲以減少CPU使用率

    save_recording()
    mixed_output_mp3_path = mix_audio()
    subprocess.Popen(["python3", "preview.py", selected_song, mixed_output_mp3_path])

    # Cleanup
    audio_in.close()
    GPIO.cleanup()

if __name__ == "__main__":
    main_loop()
    pygame.quit()
