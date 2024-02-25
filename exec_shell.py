import sys
import threading
import keyboard
import multiprocessing
import subprocess


class EndingHook:
    def __init__(self, next, hook, params=None):
        self.next = next
        self.hook = hook


def listen_for_events(event_dist, event_queue, stop_event):
    while not stop_event.is_set():
        key = keyboard.read_event()
        if key.event_type == keyboard.KEY_DOWN and key.name in event_dist:
            event_queue.put(key.name)


def exec_shell(main_task, event_dist, ending_hook):
    event_queue = multiprocessing.Queue()
    stop_event = threading.Event()

    # 創建一個線程來監聽鍵盤事件
    listener_thread = threading.Thread(
        target=listen_for_events, args=(event_dist, event_queue, stop_event)
    )
    listener_thread.start()

    # 使用多進程來執行主任務
    task_process = multiprocessing.Process(target=main_task)
    task_process.start()


    while task_process.is_alive():
        if not event_queue.empty():
            key_name = event_queue.get()
            # 終止主任務進程
            if key_name in event_dist:
                task_process.terminate()
                stop_event.set()  # 設置停止事件，終止監聽線程
                if event_dist[key_name].hook:
                    event_dist[key_name].hook()
                if event_dist[key_name].next:
                    subprocess.Popen(event_dist[key_name].next)
                task_process.join()
                listener_thread.join()
                return

    if ending_hook.hook:
        ending_hook.hook()

    if ending_hook.next:
        subprocess.Popen(ending_hook.next)

    task_process.terminate()
    task_process.join()
    stop_event.set()  # 設置停止事件，終止監聽線程
    listener_thread.join()

    return
