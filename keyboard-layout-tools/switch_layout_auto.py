#!/usr/bin/env python3
import subprocess
import time
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGFILE = os.path.join(SCRIPT_DIR, "switch_layout_auto.log")

def log(msg):
    with open(LOGFILE, "a") as f:
        f.write(msg + "\n")

def run_osascript(script):
    p = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE)
    out, _ = p.communicate()
    return out.decode('utf-8')

log("=== Run script ===")

try:
    # Копируем выделенный текст
    run_osascript('tell application "System Events" to keystroke "c" using command down')
    time.sleep(0.10)

    # Получаем из буфера
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    out, _ = p.communicate()
    text = out.decode('utf-8')
    log(f"Clipboard before switch: {repr(text)}")

    RUS_ENG = {
        'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u', 'ш': 'i', 'щ': 'o', 'з': 'p',
        'х': '[', 'ъ': ']', 'ф': 'a', 'ы': 's', 'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k',
        'д': 'l', 'ж': ';', 'э': "'", 'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b', 'т': 'n', 'ь': 'm',
        'б': ',', 'ю': '.',
        'Й': 'Q', 'Ц': 'W', 'У': 'E', 'К': 'R', 'Е': 'T', 'Н': 'Y', 'Г': 'U', 'Ш': 'I', 'Щ': 'O', 'З': 'P',
        'Х': '{', 'Ъ': '}', 'Ф': 'A', 'Ы': 'S', 'В': 'D', 'А': 'F', 'П': 'G', 'Р': 'H', 'О': 'J', 'Л': 'K',
        'Д': 'L', 'Ж': ':', 'Э': '"', 'Я': 'Z', 'Ч': 'X', 'С': 'C', 'М': 'V', 'И': 'B', 'Т': 'N', 'Ь': 'M',
        'Б': '<', 'Ю': '>'
    }
    ENG_RUS = {v: k for k, v in RUS_ENG.items()}

    def switch_layout(text):
        return ''.join(RUS_ENG.get(ch, ENG_RUS.get(ch, ch)) for ch in text)

    switched = switch_layout(text)
    log(f"Clipboard after switch: {repr(switched)}")

    # Кладём обратно в буфер
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.communicate(input=switched.encode('utf-8'))

    time.sleep(0.10)

    # Вставляем текст
    run_osascript('tell application "System Events" to keystroke "v" using command down')
    log("Inserted switched text")

except Exception as e:
    log(f"Error: {e}")
