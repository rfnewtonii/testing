import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Target URL for the 2023 ACS Summary Files
BASE_URL = "https://www2.census.gov/programs-surveys/acs/summary_file/2023/table-based-SF/data/5YRData/"

# Directory to save .dat files in /tmp (ephemeral)
DOWNLOAD_DIR = "/tmp/acs_2023_dat"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_dat_links(url):
    """Parse HTML at URL and return list of all .dat file links"""
    print(f"Fetching directory listing from: {url}")
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    links = [
        urljoin(url, a['href'])
        for a in soup.find_all('a', href=True)
        if a['href'].lower().endswith('.dat')
    ]
    print(f"Found {len(links)} .dat files.")
    return links

def download_file(url, dest_dir):
    """Download file from URL into destination directory"""
    local_filename = os.path.join(dest_dir, os.path.basename(url))
    if os.path.exists(local_filename):
        print(f"Skipping (already downloaded): {local_filename}")
        return
    print(f"Downloading: {url}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Saved: {local_filename}")

if __name__ == "__main__":
    dat_links = get_dat_links(BASE_URL)
    for link in dat_links:
        download_file(link, DOWNLOAD_DIR)

    print(f"\n✅ Download complete. Files saved to: {DOWNLOAD_DIR}")
