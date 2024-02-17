import os
from pydub import AudioSegment
import sounddevice as sd
import soundfile as sf
import keyboard
from datetime import datetime

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

def record_audio(duration=10, buffering=44100):
    # 等待 'R' 鍵被按下以開始錄音和實時監聽
    print("按下 'R' 鍵開始錄音和實時監聽...")
    keyboard.wait('R')  # 等待 'R' 鍵
    print("正在錄音和實時監聽...")
    try:
        with sd.Stream(callback=callback):
            myrecording = sd.rec(int(duration * buffering), samplerate=buffering, channels=2)
            sd.wait()
        print("錄音和實時監聽結束")
        return myrecording
    except Exception as e:
        print(f"錄音過程中發生錯誤: {e}")
        return None

def save_recording(recording, filename):
    if recording is not None:
        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            wav_file = f"C:\\Users\\kung\\Documents\\treehall\\--\\{filename}_{timestamp}.wav"
            sf.write(wav_file, recording, 44100)

            # 將 WAV 文件轉換為 MP3
            try:
                audio = AudioSegment.from_wav(wav_file)

                # 對音頻進行標準化處理
                normalized_audio = audio.normalize(headroom=20.0)
                
                # 增加音量
                increased_volume_audio = normalized_audio.apply_gain(20)  # 音量增加 20 dB

                mp3_file = f"C:\\Users\\kung\\Documents\\treehall\\--\\{filename}_{timestamp}.mp3"
                increased_volume_audio.export(mp3_file, format="mp3", bitrate="320k")

                # 轉換完成後刪除 WAV 文件
                os.remove(wav_file)
            except Exception as e:
                print(f"音頻處理過程中發生錯誤: {e}")
        except Exception as e:
            print(f"保存錄音時發生錯誤: {e}")
    else:
        print("沒有錄音可保存。")

recorded_audio = record_audio(duration=10)
save_recording(recorded_audio, "recorded_audio")
