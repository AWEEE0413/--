import os
from pydub import AudioSegment

def trim_audio_files(folder_path, trim_duration):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".wav") or file_name.endswith(".mp3"):
            input_file = os.path.join(folder_path, file_name)
            output_file = os.path.join(folder_path, f"{file_name[:-4]}_10secTrimmed.mp3")  # Change file extension to mp3
            
            # Skip if output file already exists
            if os.path.exists(output_file):
                print(f"File {output_file} already exists, skipping.")
                continue
            
            audio = AudioSegment.from_file(input_file)
            trimmed_audio = audio[:trim_duration]
            output_audio = trimmed_audio
            output_audio.export(output_file, format="mp3")  # Export as mp3
            
            print(f"Trimmed audio saved to {output_file}")

folder_path = r"C:\Users\kung\樹洞\PY"  # Replace with the path to your folder containing audio files
trim_duration = 10000  # Trim duration in milliseconds (10 seconds)

trim_audio_files(folder_path, trim_duration)