import os
import urllib.request
from pathlib import Path
from tqdm import tqdm

home = str(Path.home())
root_dir = f"{home}/climate-change/ISIMIP"
text_file = open(f"filelist.txt", "r")
file_urls = text_file.read().split('\n')
print(file_urls)

for file_url in tqdm(file_urls):
    file_path = file_url.replace('https://files.isimip.org', root_dir)
    if not os.path.exists(file_path):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            urllib.request.urlretrieve(file_url, file_path)
        except:
            print('error in creating file:', file_path)

