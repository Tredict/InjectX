import requests
import re
import time
import os

url = "https://www.python.org/downloads/"
html = requests.get(url).text

match = re.search(r'Or get the standalone installer for\s*<a href="([^"]+)">([^<]+)</a>', html)

if match:
    link = match.group(1)
    version = match.group(2)
    print("Versi terbaru:", version)
    print("Link:", link)

os.system(f'curl -L -o python.exe "{link}"')

