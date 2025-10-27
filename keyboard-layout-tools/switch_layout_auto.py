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
    log("Step 1: Cutting selected text...")
    # Cmd+X вырезает текст (удаляет и копирует в буфер) - работает независимо от раскладки
    run_osascript('tell application "System Events" to keystroke "x" using command down')
    log("Step 2: Waiting after cut...")
    time.sleep(0.30)

    # Получаем из буфера
    log("Step 3: Getting text from clipboard...")
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    out, _ = p.communicate()
    text = out.decode('utf-8')
    log(f"Step 4: Got text, length: {len(text)}, first 100 chars: {repr(text[:100])}...")
    
    # Проверяем что что-то было вырезано
    if not text or text.strip() == '':
        log("Warning: No text was cut, nothing was selected or clipboard empty")
        exit(0)
    
    log("Step 5: Starting layout switch...")

    RUS_ENG = {
        'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u', 'ш': 'i', 'щ': 'o', 'з': 'p',
        'х': '[', 'ъ': ']', 'ф': 'a', 'ы': 's', 'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k',
        'д': 'l', 'ж': ';', 'э': "'", 'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b', 'т': 'n', 'ь': 'm',
        'б': ',', 'ю': '.', 'ё': '`',
        'Й': 'Q', 'Ц': 'W', 'У': 'E', 'К': 'R', 'Е': 'T', 'Н': 'Y', 'Г': 'U', 'Ш': 'I', 'Щ': 'O', 'З': 'P',
        'Х': '{', 'Ъ': '}', 'Ф': 'A', 'Ы': 'S', 'В': 'D', 'А': 'F', 'П': 'G', 'Р': 'H', 'О': 'J', 'Л': 'K',
        'Д': 'L', 'Ж': ':', 'Э': '"', 'Я': 'Z', 'Ч': 'X', 'С': 'C', 'М': 'V', 'И': 'B', 'Т': 'N', 'Ь': 'M',
        'Б': '<', 'Ю': '>', 'Ё': '~'
    }
    ENG_RUS = {v: k for k, v in RUS_ENG.items()}

    def switch_layout(text):
        return ''.join(RUS_ENG.get(ch, ENG_RUS.get(ch, ch)) for ch in text)

    switched = switch_layout(text)
    log(f"Step 6: Switched text, first 100 chars: {repr(switched[:100])}...")

    # Кладём обратно в буфер
    log("Step 7: Putting switched text back to clipboard...")
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.communicate(input=switched.encode('utf-8'))
    log("Step 8: Text in clipboard updated")

    # Увеличиваем задержку для обработки Cmd+X
    time.sleep(0.80)
    
    # Используем key code 9 для Cmd+V (независимо от раскладки)
    log("Step 9: Pasting switched text...")
    run_osascript('tell application "System Events" to key code 9 using {command down}')
    log("Step 10: Done")

except Exception as e:
    log(f"Error: {e}")
