import glob
import os
import sys
from exec_shell import EndingHook, exec_shell


os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

expected_argv_len = 1
audio_count = 6
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
rec_source_dir = os.path.join(current_dir, "./RECSOURCE")


# Check if the correct number of arguments are provided
if len(sys.argv) - 1 != 1:
    print("Usage: python choosing.py <audio_idx>")
    print("audio_idx: 0 ~ 5")
    sys.exit(1)

audio_idx = int(sys.argv[1])


def play_music(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def main_task_sample():
    mp3_files = glob.glob(os.path.join(rec_source_dir, "*.mp3"))
    if audio_idx < 0 or audio_idx >= len(mp3_files):
        print(f"Invalid audio index: {audio_idx}")
        return
    play_music(mp3_files[audio_idx])


def main():
    exec_shell(
        main_task_sample,
        {
            "r": EndingHook(
                "python3 sample.py r 21341234", None
            ),  # 可以改成轉到 recording.py
            "n": EndingHook(
                f"python3 choosing.py {(audio_idx + 1) % 6}", None
            ),  # 切到下一首
            "0": EndingHook(f"python3 choosing.py 0", None),  # 切到第0首
            "1": EndingHook(f"python3 choosing.py 1", None),  # 切到第1首
            "2": EndingHook(f"python3 choosing.py 2", None),  # 切到第2首
            "3": EndingHook(f"python3 choosing.py 3", None),  # 切到第3首
            "4": EndingHook(f"python3 choosing.py 4", None),  # 切到第4首
            "5": EndingHook(f"python3 choosing.py 5", None),  # 切到第5首
        },
        EndingHook(f"python3 choosing.py {audio_idx}", None),  # 重複當前音樂
    )


if __name__ == "__main__":
    main()
