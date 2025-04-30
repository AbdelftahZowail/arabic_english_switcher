import sys
import pyautogui
import pyperclip
import keyboard
import winreg as reg
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
from pynput.keyboard import Controller, Key
import ctypes
import os
from datetime import datetime


# Define the custom logging function
def log_message(message):

    # Ensure the logs folder exists
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    # Define the log file path
    log_file = os.path.join(logs_dir, "prints.log")

    # Add a timestamp to each message
    log_entry = f"{message}\n"

    # Append the message to the log file with utf-8 encoding
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(log_entry)


timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_message(f'[{timestamp}] ------------NEW INSTANCE------------')

lastClipboard = ''
kb_controller = Controller()


def translate_text(text):
    if not text:
        return text
    if detect_majority_language(text):
        translation_dict = EN_TO_AR
    else:
        translation_dict = AR_TO_EN

    # Translate the text using the selected dictionary
    return "".join(translation_dict.get(char, char) for char in text)


# Example عسشلث
EN_TO_AR = {
    'q': 'ض', 'w': 'ص', 'e': 'ث', 'r': 'ق', 't': 'ف',
    'y': 'غ', 'u': 'ع', 'i': 'ه', 'o': 'خ', 'p': 'ح',
    'a': 'ش', 's': 'س', 'd': 'ي', 'f': 'ب', 'g': 'ل',
    'h': 'ا', 'j': 'ت', 'k': 'ن', 'l': 'م', 'z': 'ئ',
    'x': 'ء', 'c': 'ؤ', 'v': 'ر', 'b': 'لا', 'n': 'ى',
    'm': 'ة', '[': 'ج', ']': 'د', ';': 'ك', '\'': 'ط',
    '\\': '\\', ',': 'و', '.': 'ز', '/': 'ظ', 'Q': 'َ',
    'W': 'ً', 'E': 'ُ', 'R': 'ٌ', 'T': ',لإ', 'Y': ',إ',
    'U': '‘', 'I': '÷', 'O': '×', 'P': ',؛', '{': '<',
    '}': '>', 'A': 'ِ', 'S': 'ٍ', 'D': ']', 'F': '[',
    'G': ',لأ', 'H': ',أ', 'J': ',ـ', 'K': '،', 'L': '/',
    ':': ':', '"': '"', '|': '|', 'Z': '~', 'X': 'ْ',
    'C': '}', 'V': '{', 'B': ',لآ', 'N': ',آ', 'M': '’',
    '<': ',', '>': '.', '?': '؟'
}
AR_TO_EN = {
    'ض': 'q', 'ص': 'w', 'ث': 'e', 'ق': 'r', 'ف': 't',
    'غ': 'y', 'ع': 'u', 'ه': 'i', 'خ': 'o', 'ح': 'p',
    'ش': 'a', 'س': 's', 'ي': 'd', 'ب': 'f', 'ل': 'g',
    'ا': 'h', 'ت': 'j', 'ن': 'k', 'م': 'l', 'ئ': 'z',
    'ء': 'x', 'ؤ': 'c', 'ر': 'v', 'لا': 'b', 'ى': 'n',
    'ة': 'm', 'ج': '[', 'د': ']', 'ك': ';', 'ط': '\'',
    '\\': '\\', 'و': ',', 'ز': '.', 'ظ': '/', 'َ': 'Q',
    'ً': 'W', 'ُ': 'E', 'ٌ': 'R', ',لإ': 'T', ',إ': 'Y',
    '‘': 'U', '÷': 'I', '×': 'O', ',؛': 'P', '<': '{',
    '>': '}', 'ِ': 'A', 'ٍ': 'S', ']': 'D', '[': 'F',
    ',لأ': 'G', ',أ': 'H', ',ـ': 'J', '،': 'K', '/': 'L',
    ':': ':', '"': '"', '|': '|', '~': 'Z', 'ْ': 'X',
    '}': 'C', '{': 'V', ',لآ': 'B', ',آ': 'N', '’': 'M',
    ',': '<', '.': '>', '؟': '?'
}


def is_mostly_lowercase(text):
    lower_count = sum(1 for c in text if c.islower())
    upper_count = sum(1 for c in text if c.isupper())
    return lower_count > upper_count


last_pasted = ''


def on_f9_pressed():
    log_message(f'--------------------')
    global last_pasted
    log_message("F9 pressed")
    ctypes.WinDLL("User32.dll").keybd_event(0x11, 0, 2, 0)  # Release Ctrl
    ctypes.WinDLL("User32.dll").keybd_event(0x14, 0, 2, 0)  # Release Caps Lock
    pyautogui.hotkey("ctrl", "c")
    text = pyperclip.paste()

    if is_mostly_lowercase(text):
        new_text = text.upper()
    else:
        new_text = text.lower()
    log_message(f'last: "{last_pasted}"\nnew text "{new_text}" ({not new_text == last_pasted})')
    if not new_text == last_pasted:
        log_message('------')
        last_pasted = new_text
        keyboard.write(new_text)


def on_w_pressed():
    log_message(f'--------------------')
    global last_pasted
    ctypes.WinDLL("User32.dll").keybd_event(0x51, 0, 2, 0)  # Release Q
    ctypes.WinDLL("User32.dll").keybd_event(0x11, 0, 2, 0)  # Release Ctrl
    pyautogui.hotkey("ctrl", "c")
    text = pyperclip.paste()

    new_text = translate_text(text)
    log_message(f'last: "{last_pasted}"\nnew text "{new_text}" ({not new_text == last_pasted})')
    if not new_text == last_pasted:
        log_message('------')
        last_pasted = new_text
        keyboard.write(new_text)


def detect_majority_language(text):
    arabic_count = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
    english_count = sum(1 for char in text if 'a' <= char.lower() <= 'z')

    if arabic_count < english_count:
        return True
    else:
        return False


def create_image():
    # Create an image for the tray icon (a simple square with text or a placeholder)
    width, height = 64, 64
    image = Image.new("RGBA", (width, height), (0, 255, 255, 255))  # White background
    draw = ImageDraw.Draw(image)
    draw.text((width // 4, height // 4), "Py", fill="blue")  # Example text/logo
    return image


def add_to_startup():
    """Adds the app to startup only if it hasn't been added yet."""
    exe_path = os.path.abspath(sys.argv[0])  # Get the path of the current executable
    key = reg.HKEY_CURRENT_USER
    key_path = r"Software\CapsApp"  # Custom key for tracking
    log_message('adding')
    # Check if the marker key exists
    try:
        reg_key = reg.OpenKey(key, key_path, 0, reg.KEY_READ)
        already_added = reg.QueryValueEx(reg_key, "AddedToStartup")[0]
        reg.CloseKey(reg_key)
    except FileNotFoundError:
        already_added = False

    if not already_added:
        log_message('not added,,, adding')
        # Add the app to startup
        startup_key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        reg_key = reg.OpenKey(key, startup_key_path, 0, reg.KEY_WRITE)
        reg.SetValueEx(reg_key, "CapsApp", 0, reg.REG_SZ, exe_path)
        reg.CloseKey(reg_key)

        # Mark as added in the custom registry key
        reg_key = reg.CreateKey(key, key_path)
        reg.SetValueEx(reg_key, "AddedToStartup", 0, reg.REG_SZ, "True")
        reg.CloseKey(reg_key)


def on_exit(icon):
    log_message('exiting')
    # Stop the icon and exit the app
    icon.stop()
    keyboard.unhook_all_hotkeys()
    sys.exit(0)


# Add to startup
add_to_startup()

# Set up the system tray icon and menu
icon = Icon("Caps app", create_image(), menu=Menu(MenuItem("Exit", on_exit)))

# Add the F9 hotkey
# keyboard.add_hotkey('ctrl+caps lock', on_f9_pressed)
keyboard.add_hotkey('ctrl+q', on_w_pressed)

# Start the system tray icon
icon.run()

# Ensure the script keeps running and waiting for hotkeys
keyboard.wait()
