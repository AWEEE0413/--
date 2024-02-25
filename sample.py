import sys
import time

from exec_shell import EndingHook, exec_shell


# Check if the correct number of arguments are provided
if len(sys.argv) - 1 != 2:
    print("Usage: python sample.py <param0> <param1>")
    sys.exit(1)


# sys.argv[0] 為 字串 "sample.py"
# sys.argv[1] 為 參數 <param0>
# sys.argv[2] 為 參數 <param1>


# 主任務函數示例
def main_task_sample():
    print("開始執行主任務..., 參數為:", sys.argv[1], sys.argv[2])
    time.sleep(10)  # 模擬長時間執行的任務
    print("主任務完成")


def ending_task_sample():
    print("程式結束")
    print("=====================================")


def r_hook():
    print("        執行 r 鈎子")


def f_hook():
    print("        執行 f 鈎子")


def s_hook():
    print("        執行 s 鈎子: program terminated by 's'.")


def main():
    exec_shell(
        main_task_sample,
        {
            "r": EndingHook("python3 sample.py r 21341234", r_hook),
            "f": EndingHook("python3 sample.py f 343242", f_hook),
            "v": EndingHook(
                "python3 sample.py v wqerqwe", None
            ),  # if you don't want to run any hook
            "s": EndingHook(None, None),  # if you want to exit the program
        },
        EndingHook(None, ending_task_sample),
    )


if __name__ == "__main__":
    main()
