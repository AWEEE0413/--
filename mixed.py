from pydub import AudioSegment
from datetime import datetime   
import numpy as np  
def mix_audio(song_path, recording, output_path="mixed_audio.mp3"):
    """
    混合一首歌與一段錄音，並將結果保存為 MP3 文件。

    參數:
    - song_path: 歌曲文件的路徑。
    - recording: 包含錄音數據的 NumPy 數組。
    - output_path: 混合音頻文件保存的路徑（預設為 "mixed_audio.mp3"）。
    """
    # 加載歌曲
    song = AudioSegment.from_file(song_path)

    # 將錄音轉換為 AudioSegment 物件
    recording_segment = AudioSegment(
        recording.tobytes(), 
        frame_rate=44100,
        sample_width=recording.dtype.itemsize, 
        channels=2
    )

    # 混合歌曲和錄音
    mixed = song.overlay(recording_segment)

    # 保存混合後的音頻
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = f"{timestamp}_{output_path}"
    mixed.export(output_filename, format="mp3")
    print(f"已將混合音頻保存到 {output_filename}")

# NumPy 錄音數組 `recording` 和一個歌曲文件路徑 `song_path`
# mix_audio(song_path, recording, "output_mixed_audio.mp3")