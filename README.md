# Arabic/English Text Switcher

This Python script runs in the background on Windows systems to help quickly fix text that was accidentally typed using the wrong keyboard layout (specifically between English QWERTY and Arabic). When triggered by a hotkey, it copies selected text, detects if it was likely meant to be Arabic or English based on the characters typed, translates it to the corresponding characters on the *other* layout, and types the corrected text back.

## Problem Solved

Have you ever typed a sentence in Arabic, only to realize your keyboard was still set to English, resulting in gibberish like `sghl hggi hgkhs`? Or typed English and gotten Arabic characters like `صثيثشىف فخق سعلاشق`? This tool fixes that instantly with a hotkey press.

## Features

*   **Hotkey Activated:** Translates selected text when `Ctrl+Q` is pressed.
*   **Bi-directional Translation:**
    *   Converts English QWERTY characters to their Arabic keyboard equivalents.
    *   Converts Arabic characters back to their English QWERTY equivalents.
*   **Automatic Language Detection:** Determines whether the selected text consists primarily of English layout characters or Arabic characters to apply the correct translation map.
*   **Clipboard Integration:** Uses the clipboard to grab the selected text.
*   **Direct Text Input:** Simulates keyboard input (`keyboard.write`) to replace the selected text with the translation.
*   **System Tray Icon:** Runs minimized in the system tray with an option to exit.
*   **Windows Startup:** Automatically adds itself to run on Windows startup (can be managed via Task Manager).
*   **Logging:** Records actions (startup, hotkey presses, translations, exits) to a `logs/prints.log` file for troubleshooting.

## Prerequisites

*   **Operating System:** Windows (Uses `winreg` and `ctypes.WinDLL` for startup and system functions).
*   **Python 3.x:** The script is written for Python 3.
*   **Required Python Libraries:**
    *   `pyautogui`: For sending hotkeys (`Ctrl+C`).
    *   `pyperclip`: For clipboard interaction.
    *   `keyboard`: For detecting hotkeys and writing text.
    *   `pystray`: For the system tray icon.
    *   `Pillow` (PIL): For creating the system tray icon image.
    *   `pynput`: For simulating keyboard events (used for releasing keys).

## Installation

1.  **Install Python:** If you don't have Python 3 installed, download it from [python.org](https://www.python.org/) and ensure it's added to your system's PATH during installation.
2.  **Download the Script:** Save the Python code as `main.py` (or a similar name).
3.  **Install Dependencies:** Open Command Prompt or PowerShell and run:
    ```bash
    pip install pyautogui pyperclip keyboard pystray Pillow pynput
    ```

## Usage

1.  **Run the Script:**
    *   Double-click `main.py` or run `python main.py` from the command line.
    *   Alternatively, to run without a console window appearing, use `pythonw.exe main.py`.
2.  **Background Operation:** The script will run in the background. You should see a new icon (a simple square with "Py") in your system tray (notification area).
3.  **Translate Text:**
    *   Type text in any application.
    *   If you realize you used the wrong keyboard layout (e.g., typed English characters when you meant Arabic), **select the incorrect text**.
    *   Press the hotkey: `Ctrl + Q`.
    *   The script will briefly copy the text, determine the correction, and type the translated version, replacing your selection.
4.  **Exit the Application:** Right-click the system tray icon and select "Exit".

## How It Works

1.  **Hotkey Detection:** The `keyboard` library listens for the `Ctrl+Q` combination.
2.  **Copy Selection:** `pyautogui` sends a `Ctrl+C` command to copy the currently selected text.
3.  **Clipboard Access:** `pyperclip` reads the text from the clipboard.
4.  **Language Detection:** The script counts the number of common Arabic vs. Latin alphabet characters in the copied text.
5.  **Translation Mapping:** Based on the detection, it uses either the `EN_TO_AR` or `AR_TO_EN` dictionary to map each character to its counterpart on the *other* keyboard layout.
6.  **Paste/Write Result:** The `keyboard.write()` function simulates typing the translated characters, effectively replacing the original selection.
7.  **Duplicate Prevention:** It stores the last translated text (`last_pasted`) to avoid accidentally re-translating the same text immediately if the hotkey is pressed again on the already corrected text.
