import os
import requests
import time
from bs4 import BeautifulSoup
from tqdm import tqdm


def download_file(url, directory, limit_speed=None):
    """Downloads a file from a URL and saves it to a directory."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # Extract the filename from the URL and remove everything before and including the '=' character
        filename = url.split("/")[-1].split("=")[-1]
        filepath = os.path.join(directory, filename)
        total_size = int(response.headers.get("Content-Length", 0))
        block_size = int(
            1024 * 1024 * limit_speed) if limit_speed is not None else 1024 * 1024
        progress_bar = tqdm(total=total_size, unit="B",
                            unit_scale=True, desc=filename, leave=True)
        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))
                    if limit_speed is not None:
                        time.sleep(len(chunk) / (block_size * limit_speed))
        progress_bar.close()
        print(f"Downloaded {filename}")
        time.sleep(60)  # Wait for 1 minute before the next download
    else:
        print(f"Failed to download {url}")


def download_zip_files(url, directory, limit_speed=None):
    """Downloads all ZIP files linked on a webpage to a directory."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    file_links = soup.find_all("a", href=True)
    zip_links = [link["href"]
                 for link in file_links if link["href"].endswith(".zip")]
    for link in zip_links:
        filename = link.split("/")[-1].split("=")[-1]
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            print(f"{filename} already downloaded")
        else:
            download_file(link, directory, limit_speed)


if __name__ == "__main__":
    url = ""
    name = ""
    directory = os.path.join("D:", "Pics", name)
    os.makedirs(directory, exist_ok=True)
    download_zip_files(url, directory, limit_speed=1.0)
