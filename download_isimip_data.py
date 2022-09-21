import os
import urllib.request
from pathlib import Path

home = str(Path.home())
root_dir = f"{home}/climate-change/ISIMIP data"
text_file = open(f"{root_dir}/filelist.txt", "r")
file_urls = text_file.read().split('\n')
print(file_urls)

for file_url in file_urls:
    file_path = file_url.replace('https://files.isimip.org', root_dir)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    urllib.request.urlretrieve(file_url, file_path)

