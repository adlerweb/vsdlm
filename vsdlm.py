# 2023 Florian Knodt - www.adlerweb.info
# This code is licensed under MIT license (see LICENSE.txt for details)

import requests
import math
import time
import os
import sys
from urllib.parse import urlparse, unquote

def humanSize(size, bits=False, speed=False, decimals=1):
    units = ["", "K", "M", "G", "T", "P", "E", "Z", "Y", "R", "Q"]
    suffix = "B"
    div = 1024
    if bits:
        suffix = "Bit"
        div = 1000
    index = 0
    
    if speed:
        suffix = suffix + "/s"

    while size >= div and index < len(units) - 1:
        size /= div
        index += 1

    return f"{size:.{decimals}f} {units[index]}{suffix}"

def processURL():
    with open("in.txt", "r") as input_file:
        url = input_file.readline().strip()

        if not url:
            return False

    with open("current.txt", "w") as output_file:
        output_file.write(url)

    with open("in.txt", "r") as input_file:
        lines = input_file.readlines()

    with open("in.txt", "w") as input_file:
        input_file.writelines(lines[1:])

    return url

def downloadFile(url, progress=True):
    response = requests.head(url, allow_redirects=True)
    file_name = unquote(os.path.basename(urlparse(response.url).path))
    resume = False
    downloaded_size = 0
    total_size = int(response.headers.get('content-length', 0))
    total = humanSize(total_size)
    
    print(f"Writing to {file_name}, expecting {total}")

    if os.path.exists(file_name):
        resume = True
        file_size = os.path.getsize(file_name)
        headers = {'Range': f'bytes={file_size}-'}
        downloaded_size = file_size
        downloaded = humanSize(downloaded_size)
        print(f"Resuming download at {downloaded}")
    else:
        headers = None
        file_size = 0

    while downloaded_size < total_size:
        response = requests.get(url, headers=headers, stream=True)
        block_size = 4096
        num_blocks = math.ceil(total_size / block_size)
        start_time = time.time()

        with open(file_name, 'ab' if resume else 'wb') as file:
            for data in response.iter_content(block_size):
                file.write(data)
                downloaded_size += len(data)
                if progress:
                    percent = min(int((downloaded_size / total_size) * 100), 100)
                    downloaded = humanSize(downloaded_size)
                    elapsed_time = time.time() - start_time
                    download_speed_bytes = (downloaded_size - file_size) / elapsed_time
                    download_speed_bits = download_speed_bytes * 8
                    download_speed = humanSize(download_speed_bits, bits=True, speed=True, decimals=2)
                    progress_str = f"Downloaded: {percent}% ({downloaded}/{total}) @ {download_speed}"
                    progress_str = progress_str.ljust(len(progress_str) + 10)  # Pad with 10 extra spaces
                    print(progress_str, end='\r')


    total = humanSize(total_size)
    os.remove("current.txt")
    print(f"\nDownload of {file_name} complete, {total}!")

while True:
    if os.path.exists("exit.txt"):
        print("Exiting as requested.")
        os.remove("exit.txt")
        sys.exit()
        
    url = False
    if os.path.exists("current.txt"):
        with open("current.txt", "r") as input_file:
            url = input_file.readline().strip()

    if url:
        print(f"Resuming download")
    else:
        url = processURL()

    if url:
        print(f"Downloading file from URL: {url}")
        downloadFile(url)
    else:
        print("No URL found.", end='\r')
        time.sleep(1)