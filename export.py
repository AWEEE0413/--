import os
import sys
from datetime import datetime

mixed_filename = sys.argv[1]
output_dir = "exports"
os.makedirs(output_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
output_path = f"{output_dir}/mix_{timestamp}.mp3"
os.rename(mixed_filename, output_path)
print(f"Exported to: {output_path}")
