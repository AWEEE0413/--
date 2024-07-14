import subprocess
import sys
from datetime import datetime
import os

# 切换到脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# 获得混音后的音频文件
mixed_filename = sys.argv[1]

print(f"Exporting {mixed_filename}...")

# 保存混音后的音频文件
export_folder = "output_export"
os.makedirs(export_folder, exist_ok=True)
export_filename = f"{export_folder}/export_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
subprocess.run(["ffmpeg", "-i", mixed_filename, export_filename])

print(f"Exported to {export_filename}")

# 直接回到 choose.py
subprocess.Popen(["python3", os.path.join(script_dir, "choose.py")])
