# README.md (繁體中文)

## 簡介

這個專案包含四個 Python 腳本，分別是 `choose.py`、`record.py`、`preview.py` 和 `export.py`。這些腳本用於一個基於樹莓派的音頻錄製和播放系統，其中結合了 GPIO 控制 LED 和按鈕，用於選擇、錄製、預覽和導出音頻。

- **[`choose.py`](#choosepy)**: 這個腳本負責讓使用者從可用的音頻文件中選擇一個。選擇後，會觸發錄音過程。
- **[`record.py`](#recordpy)**: 這個腳本負責錄製音頻，並將錄音結果與選擇的音樂文件混合。錄音過程中還包括 LED 指示燈的控制。
- **[`preview.py`](#previewpy)**: 在錄音和混音完成後，這個腳本會讓使用者預覽結果，並選擇是重錄、保存還是取消。
- **[`export.py`](#exportpy)**: 此腳本負責將混音結果導出為 MP3 文件，並將控制返回到 `choose.py`。

## 傳遞資料

這些腳本透過命令行參數來傳遞資料：

- **[`choose.py`](#choosepy)**：選擇聲景後，將選擇的音樂文件路徑作為參數傳遞給 `record.py`。
- **[`record.py`](#recordpy)**：錄音完成後，將混音後的音頻文件路徑作為參數傳遞給 `preview.py`。
- **[`preview.py`](#previewpy)**：使用者決定保存時，將混音文件路徑作為參數傳遞給 `export.py`。
- **[`export.py`](#exportpy)**：導出完成後，會返回到 `choose.py` 以便重新選擇聲景。

## 安裝與使用

1. **安裝依賴**

    確保已經安裝了所需的 Python 庫：

    ```bash
    pip install pygame pydub pyalsaaudio RPi.GPIO
    ```

2. **運行 `choose.py`**

    使用以下命令啟動整個流程：

    ```bash
    python3 choose.py
    ```

3. **傳遞命令行參數**

    在 `choose.py` 中選擇聲景後，腳本會自動將選擇的音樂文件路徑作為參數傳遞給後續腳本。

4. **自動運行**

    可以使用 `crontab` 或其他自動運行工具設置開機自動運行。

## 最終完工圖

![完工圖](https://drive.google.com/file/d/1hm3WPWJ76oYt4k18GBTLhGKZbP7BDrUB/view)

---

# README.md (English)

## Introduction

This project includes four Python scripts: `choose.py`, `record.py`, `preview.py`, and `export.py`. These scripts are part of a Raspberry Pi-based audio recording and playback system, integrating GPIO to control LEDs and buttons for selecting, recording, previewing, and exporting audio.

- **[`choose.py`](#choosepy)**: This script allows the user to select an audio file from the available options. After selection, it triggers the recording process.
- **[`record.py`](#recordpy)**: This script handles audio recording and mixing the recording with the selected audio file. It also controls LED indicators during the recording process.
- **[`preview.py`](#previewpy)**: After recording and mixing, this script allows the user to preview the result and choose to re-record, save, or cancel.
- **[`export.py`](#exportpy)**: This script is responsible for exporting the mixed audio file to an MP3 format and then returning control to `choose.py`.

## Data Passing

These scripts pass data through command-line arguments:

- **[`choose.py`](#choosepy)**: After selecting a soundscape, the path of the selected audio file is passed as an argument to `record.py`.
- **[`record.py`](#recordpy)**: After recording, the path of the mixed audio file is passed as an argument to `preview.py`.
- **[`preview.py`](#previewpy)**: When the user decides to save, the path of the mixed file is passed as an argument to `export.py`.
- **[`export.py`](#exportpy)**: After exporting, it returns control to `choose.py` for re-selection of the soundscape.

## Installation and Usage

1. **Install Dependencies**

    Ensure that the required Python libraries are installed:

    ```bash
    pip install pygame pydub pyalsaaudio RPi.GPIO
    ```

2. **Run `choose.py`**

    Start the entire process with the following command:

    ```bash
    python3 choose.py
    ```

3. **Passing Command-Line Arguments**

    After selecting a soundscape in `choose.py`, the script automatically passes the path of the selected audio file as an argument to the subsequent scripts.

4. **Automated Execution**

    You can set up the script to run automatically at boot using `crontab` or other automation tools.

## Final Product Image

![Final Product Image](https://drive.google.com/file/d/1hm3WPWJ76oYt4k18GBTLhGKZbP7BDrUB/view)
