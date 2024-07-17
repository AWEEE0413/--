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
import threading

# 切换到脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Initialize Pygame
pygame.init()
pygame.mixer.init()


# Initialize GPIO
GPIO.setmode(GPIO.BCM)
button_pins = [16]
led_pins = [20, 12]  # 0: Recording, 1: Stop Recording

for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)

# Set recording parameters
device = 'plughw:3,0'
channels = 1
rate = 44100
format = alsaaudio.PCM_FORMAT_S16_LE
periodsize = 1024

# Open audio stream for input
audio_in = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL,
                         device=device, channels=channels, rate=rate, format=format, periodsize=periodsize)

# Get the selected song path from command line argument
selected_song = sys.argv[1]

def breathing_led(pin):
    while not song_selected:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.5)

def start_recording():
    #撥放開始音效並等音效播完
    pygame.mixer.music.load("/home/treehole/--/soundeffect/Tree Hole SFX_Start Recording2.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    # Load selected song
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

    #撥放結束音效
    pygame.mixer.music.load("/home/treehole/--/soundeffect/Tree Hole SFX_Submit.mp3")
    pygame.mixer.music.play()

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

    # 设置LED状态
    GPIO.output(led_pins[1], GPIO.HIGH)  # 停止錄音键恒亮

    # 开启录音键闪烁线程
    breathing_thread = threading.Thread(target=breathing_led, args=(led_pins[0],))
    breathing_thread.start()

    # 播放音樂
    start_recording()

    while recording:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000
        print(f"錄音中... {elapsed_time:.2f} 秒")

        if elapsed_time >= RECORD_SECONDS or GPIO.input(button_pins[0]) == GPIO.LOW:
            recording = False
        
        length, data = audio_in.read()
        if length:
            frames.append(data)
        
        time.sleep(0.01)  # 加入短暫延遲以減少CPU使用率

    save_recording()
    mixed_output_mp3_path = mix_audio()
    subprocess.Popen(["python3", os.path.join(script_dir, "preview.py"), selected_song, mixed_output_mp3_path])

    # 关闭呼吸灯线程
    global song_selected
    song_selected = True
    breathing_thread.join()

    # 设置停止录音LED熄灭
    GPIO.output(led_pins[1], GPIO.LOW)

    # Cleanup
    audio_in.close()
    GPIO.cleanup()

if __name__ == "__main__":
    global song_selected
    song_selected = False
    main_loop()
    pygame.quit()
