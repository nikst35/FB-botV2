import time
import random
import re
import sys
import subprocess
import importlib
import requests

# Configuration
horny_knjiznice = ["pyautogui", "pyperclip", "pushbullet"]  # do not modify in this stage

api_key = "<INSERT_YOUR_PUSHBULLET_API_KEY>"  # <-- Replace with your own key or leave placeholder
waitForConfirmation = False  # set to False for automatic confirmation

mozniOdgovori = ("Vzamem!", "Uzamem", "vzamem 8===D", "Prevzamem")
mozniOdgovori2 = ("Vzamem če ne dobiš zamenjave :)",)

# --- FILE PATHS (replace with relative or example paths) ---
raw_file = r"<PATH_TO_PROJECT>/RAW.txt"
burn_file = r"<PATH_TO_PROJECT>/BURN.txt"
burn2_file = r"<PATH_TO_PROJECT>/BURN2.txt"
oldState_file = r"<PATH_TO_PROJECT>/OLDStanje.txt"
newState_file = r"<PATH_TO_PROJECT>/NEWStanje.txt"

# --- END CONFIGURATION ---

sys.stdout.reconfigure(encoding='utf-8')
time.sleep(random.uniform(5, 10))  # wait before connecting to Facebook

def is_connected():
    try:
        response = requests.get("https://www.facebook.com", timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def install_knjiznico(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    except Exception as e:
        print(f"Installation failed for {package_name}: {e}")

def preveriKnjiznice():
    for library in horny_knjiznice:
        try:
            importlib.import_module(library)
            print(f"{library} je inštaliran")
        except ImportError:
            print(f"{library} manjka — poskusim namestiti ...")
            install_knjiznico(library)

def internetDela():
    while True:
        if not is_connected():
            print("Ni povezave do FB — ponoven poskus čez 10s")
            time.sleep(10)
            continue
        else:
            print("Povezava s FB vzpostavljena.")
            break

internetDela()
preveriKnjiznice()

import pyautogui
import pyperclip
from pushbullet import Pushbullet

def interface(message):
    pb.push_note("ŽELIŠ NASLEDNI TERMIN ZA DEŽURANJE ? (DA/NE)", message)
    print("Notification sent. Waiting for response...")
    time.sleep(30)
    cnt = 0
    while True:
        pushes = pb.get_pushes()
        time.sleep(15)
        if pushes:
            latest_push = pushes[0]
            if not latest_push.get('title'):
                vsebina = latest_push.get('body', '').lower().strip()
                if vsebina == "da":
                    pb.push_note("Update", "prevzemam termin")
                    postComment(random.choice(mozniOdgovori))
                    return "Da"
                elif vsebina == "ne":
                    pb.push_note("Update", "termin zavrnjen")
                    return "Ne"
                else:
                    pb.push_note("Neveljaven odgovor", "Odgovori s 'Da' ali 'Ne'.")
            else:
                cnt += 1
                if cnt >= 5:
                    pb.push_note("Update", "Ni bilo pravočasnega odgovora.")
                    return
                time.sleep(10)

def inputFile(output_file):
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(random.uniform(10, 15))
    pyautogui.keyDown('down')
    time.sleep(random.uniform(3, 6))
    pyautogui.keyUp('down')
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(random.uniform(0.5, 1))
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(random.uniform(0.5, 1))
    copied_text = pyperclip.paste()
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(copied_text)

def Oddam(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in lines:
            if re.match(r"\s*odda[a-zA-Z]*", line.strip(), re.IGNORECASE):
                outfile.write(line)
                break

def cleanUp(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    lines = lines[10:]
    cnt = 0
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in lines:
            cleaned_line = line.replace("Facebook", "")
            if len(cleaned_line.strip()) >= 3:
                outfile.write(cleaned_line)
                cnt += 1
            if cnt >= 40:
                break

def copyFile(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    pyperclip.copy(content)
    return content

def pisanjeSZamikom(text, min_delay, max_delay):
    for char in text:
        pyautogui.write(char)
        time.sleep(random.uniform(min_delay, max_delay))

def postComment(besedilo):
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(random.uniform(4, 8))
    for _ in range(35):
        pyautogui.press('tab')
        time.sleep(random.uniform(0.05, 0.2))
    pyautogui.press('enter')
    pisanjeSZamikom(besedilo, 0.05, 0.1)
    pyautogui.press('enter')

def Ali_DatoTekI_nIsTa_eNakI(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        return 0 if f1.read() == f2.read() else 1

def KopiranjeDatotek(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        content = infile.read()
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def startup():
    inputFile(raw_file)
    cleanUp(raw_file, burn_file)
    Oddam(burn_file, burn2_file)
    KopiranjeDatotek(burn2_file, oldState_file)
    time.sleep(10)

while True:
    try:
        pb = Pushbullet(api_key)
        break
    except:
        print("PushBullet API key invalid or network error.")
        time.sleep(10)

def main():
    startup()
    while True:
        inputFile(raw_file)
        cleanUp(raw_file, burn_file)
        Oddam(burn_file, burn2_file)
        KopiranjeDatotek(burn2_file, newState_file)
        if Ali_DatoTekI_nIsTa_eNakI(oldState_file, newState_file):
            KopiranjeDatotek(newState_file, oldState_file)
            comment = copyFile(newState_file)
            if waitForConfirmation:
                interface(comment)
            else:
                postComment(random.choice(mozniOdgovori))
                pb.push_note("Prevzet je bil naslednji termin:", comment)
            break  # comment this out for continuous mode

if __name__ == "__main__":
    main()
