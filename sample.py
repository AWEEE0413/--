import subprocess
import threading
import time
import keyboard


class EndingHook:
    def __init__(self, next, hook, params=None):
        self.next = next
        self.hook = hook


def shell(main_task, event_dist, ending_task):
    global stop_event
    stop_event = threading.Event()
    task_thread = threading.Thread(target=main_task)
    task_thread.start()

    while True:
        key = keyboard.read_event()
        if key.name in event_dist:
            print("    偵測到事件: ", key.name)
            if event_dist[key.name].hook:
                event_dist[key.name].hook()
            print("    執行: ", event_dist[key.name].next)
            subprocess.Popen(event_dist[key.name].next)
            break

    stop_event.set()
    task_thread.join()

    ending_task()

# The following is a sample of how to use the shell function

def main_tast_sample():
    while not stop_event.is_set():
        print("執行任務中...")
        time.sleep(1)
    print("任務已停止")


def ending_task_sample():
    print("程式結束")

def r_hook():
    print("執行 r 鈎子")


def main():
    shell(main_tast_sample, {"r": EndingHook("python3 sample.py", r_hook)}, ending_task_sample)


if __name__ == "__main__":
    main()
