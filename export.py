"""
Exporting(mixed_filename)
    0 -> Choosing(audio_filename)
"""

import subprocess
import sys
from datetime import datetime
import os

# 獲得混音後的音頻文件
mixed_filename = sys.argv[1]

print(f"Exporting {mixed_filename}...")

# 保存混音後的音頻文件
export_folder = "output_export"
os.makedirs(export_folder, exist_ok=True)
export_filename = f"{export_folder}/export_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
subprocess.run(["ffmpeg", "-i", mixed_filename, export_filename])

print(f"Exported to {export_filename}")

# 直接回到 choose.py
subprocess.Popen(["python3", "choose.py"])
