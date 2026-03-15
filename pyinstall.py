import requests
import re

url = "https://www.python.org/downloads/"
html = requests.get(url).text

match = re.search(r'Or get the standalone installer for\s*<a href="([^"]+)">([^<]+)</a>', html)

if match:
    link = match.group(1)
    version = match.group(2)

    print("Versi terbaru:", version)
    print("Link:", link)

    print("Downloading...")

    r = requests.get(link)
    with open("python.exe", "wb") as f:
        f.write(r.content)

    print("Download selesai!")
else:
    print("Installer tidak ditemukan")
