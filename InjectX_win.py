#--===============================================
#--  author: Tredict, Firr
#--  credit: Tredd / Firr
#--===============================================

from tkinter import *
import requests
from urllib.parse import quote
from pathlib import Path
import json
from tkinter import filedialog
import os
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import shutil
import zipfile
import time

# ==========================
# CONFIG SYSTEM
# ==========================

CONFIG_FILE = "config.json"

default_config = {
    "steamluapath": r"C:\Program Files (x86)\Steam\config\stplug-in",
    "download_folder": str(Path.home() / "Downloads"),
    "steamstart": r"C:\Program Files (x86)\Steam\steam.exe"
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return default_config

def save_config():

    config = {
        "steamluapath": lua_entry.get(),
        "download_folder": download_entry.get(),
        "steamstart": steam_entry.get()
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

    print("Config saved!")

# ==========================
# BROWSE BUTTONS
# ==========================

def browse_lua():
    folder = filedialog.askdirectory()
    if folder:
        lua_entry.delete(0, END)
        lua_entry.insert(0, folder)

def browse_download():
    folder = filedialog.askdirectory()
    if folder:
        download_entry.delete(0, END)
        download_entry.insert(0, folder)

def browse_steam():
    file = filedialog.askopenfilename(filetypes=[("Steam", "*.exe")])
    if file:
        steam_entry.delete(0, END)
        steam_entry.insert(0, file)

# ==========================
# STEAM SEARCH
# ==========================

def search_game(game):

    url = f"https://store.steampowered.com/api/storesearch/?term={quote(game)}&l=english&cc=US"

    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    data = r.json()

    return data["items"]

# ==========================
# INJECT FUNCTION
# ==========================

def inject_game(appid, name):
    
    print(f"Injecting {name} | AppID: {appid}")

    steamluapath = lua_entry.get()
    DOWNLOAD_FOLDER = Path(download_entry.get())
    steamstart = steam_entry.get()

    driver = create_driver(headless=True)

    TARGET_URL = "https://kernelos.org/games/"

    driver.get(TARGET_URL)

    wait = WebDriverWait(driver, 15)

    input_box = wait.until(
        EC.presence_of_element_located((By.ID, "gid"))
    )

    input_box.send_keys(appid)

    btn = driver.find_element(By.ID, "go")
    btn.click()

    print("Generating link...")

    try:

        msg_element = wait.until(
            EC.presence_of_element_located((By.ID, "msg"))
        )

        time.sleep(2)

        msg_text = msg_element.text.strip()

        if "not found" in msg_text.lower():

            print("Game tidak tersedia")
            driver.quit()
            return

    except TimeoutException:

        pass

    download_button = wait.until(
        EC.element_to_be_clickable((By.ID, "dl"))
    )

    download_button.click()

    wait_for_download(DOWNLOAD_FOLDER)

    print("Extracting...")

    zip_path = DOWNLOAD_FOLDER / f"{appid}.zip"
    extract_path = DOWNLOAD_FOLDER / f"{appid}"

    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    luafile = DOWNLOAD_FOLDER / f"{appid}\\{appid}.lua"
    steamluafile = os.path.join(steamluapath, f"{appid}.lua")

    shutil.move(luafile, steamluafile)

    os.system("taskkill /f /im steam.exe")

    time.sleep(5)

    os.startfile(steamstart)

    print("Inject selesai!")


# ==========================
# SEARCH BUTTON
# ==========================

def do_search():

    for widget in result_frame.winfo_children():
        widget.destroy()

    game = input_text.get()

    results = search_game(game)

    if not results:
        Label(result_frame, text="Game tidak ditemukan").pack()
        return

    for g in results:

        row = Frame(result_frame, bd=1, relief="solid", pady=5)
        row.pack(fill="x", padx=20, pady=5)

        label = Label(row, text=f"{g['name']} | AppID: {g['id']}", anchor="w")
        label.pack(side=LEFT, padx=10)

        btn = Button(
            row,
            text="Inject",
            command=lambda appid=g['id'], name=g['name']: inject_game(appid, name)
        )
        btn.pack(side=RIGHT, padx=10)

# ==========================
# LOAD CONFIG
# ==========================

config = load_config()

# ==========================
# WINDOW
# ==========================

window = Tk()
window.title("InjectX")

lebar = 900
tinggi = 600

screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()

x = int((screenwidth/2) - (lebar/2))
y = int((screenheight/2) - (tinggi/2))

window.geometry(f"{lebar}x{tinggi}+{x}+{y}")

# ==========================
# SEARCH BAR
# ==========================

search_frame = Frame(window)
search_frame.pack(pady=20)

title = Label(search_frame, text="InjectX", font=("Segoe UI", 16, "bold"))
title.pack(side=LEFT, padx=10)

input_text = Entry(search_frame, width=60, font=("Segoe UI", 12))
input_text.pack(side=LEFT, padx=10)

search_btn = Button(search_frame, text="Search", command=do_search)
search_btn.pack(side=LEFT)

# ==========================
# RESULT FRAME
# ==========================

result_frame = Frame(window)
result_frame.pack(fill="both", expand=True)

# ==========================
# CONFIG PANEL
# ==========================

config_frame = Frame(window, bd=2, relief="groove")
config_frame.pack(side=BOTTOM, fill="x", padx=10, pady=10)

# Steam Lua Path
Label(config_frame, text="Steam Lua Path").grid(row=0, column=0, padx=5, pady=3)

lua_entry = Entry(config_frame, width=70)
lua_entry.insert(0, config["steamluapath"])
lua_entry.grid(row=0, column=1)

Button(config_frame, text="Browse", command=browse_lua).grid(row=0, column=2, padx=5)

# Download Folder
Label(config_frame, text="Download Folder").grid(row=1, column=0, padx=5, pady=3)

download_entry = Entry(config_frame, width=70)
download_entry.insert(0, config["download_folder"])
download_entry.grid(row=1, column=1)

Button(config_frame, text="Browse", command=browse_download).grid(row=1, column=2, padx=5)

# Steam Path
Label(config_frame, text="Steam Path").grid(row=2, column=0, padx=5, pady=3)

steam_entry = Entry(config_frame, width=70)
steam_entry.insert(0, config["steamstart"])
steam_entry.grid(row=2, column=1)

Button(config_frame, text="Browse", command=browse_steam).grid(row=2, column=2, padx=5)

Button(config_frame, text="Save Config", command=save_config).grid(row=3, column=1, pady=10)

window.mainloop()
