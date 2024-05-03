"""
Recording(audio_filename)
        0 -> Choosing(audio_filename)
        1 -> Recording(audio_filename)
        done -> Previewing(audio_filename, mixed_filename)

"""

import os
import sys
import wave
import pygame
import pyaudio
import alsaaudio
from datetime import datetime
from pydub import AudioSegment
import subprocess

# Initialize Pygame
pygame.init()
pygame.display.init()

# Set window size
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Recording Game")

# Initialize PyAudio
p = pyaudio.PyAudio()

# Set recording parameters
CHUNK = 1024
FORMAT = alsaaudio.PCM_FORMAT_S16_LE
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 30

# Open audio stream for output
stream_out = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)

# Open audio stream for input
# stream_in = p.open(
#     format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
# )

# Get the selected song path from command line argument
selected_song = sys.argv[1]



def start_recording():
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

    # Display "錄音結束" on the pygame window
    font = pygame.font.SysFont(None, 36)
    text = font.render("錄音結束", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    window_surface.blit(text, text_rect)
    pygame.display.update()

    # Stop audio streams
    #stream_in.stop_stream()
    #stream_in.close()
    stream_out.stop_stream()
    stream_out.close()

    # Save recording as WAV file
    wav_output_folder = "output_wav"
    os.makedirs(wav_output_folder, exist_ok=True)
    record_audio_path = f"{wav_output_folder}/record_audio_{timestamp}.wav"
    wf = wave.open(record_audio_path, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
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
    # 播放開始音效
    pygame.mixer.music.load("hpjwd-axrpe.wav")
    pygame.mixer.music.play()
    # 等待音效播放完畢
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    # 播放音樂
    start_recording()

    while recording:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                recording = False

        if elapsed_time >= RECORD_SECONDS:
            recording = False

        data = stream_out.read(CHUNK)
        frames.append(data)

        # Update window
        window_surface.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Recording: {elapsed_time:.1f} s", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        window_surface.blit(text, text_rect)
        pygame.display.update()

    save_recording()
    mixed_output_mp3_path = mix_audio()
    subprocess.Popen(["python3", "preview.py", selected_song, mixed_output_mp3_path])


if __name__ == "__main__":
    main_loop()
    pygame.quit()
