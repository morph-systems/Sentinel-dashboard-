# === Sentinel Cosmic Crawler (FITS Fetcher) ===

import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://lambda.gsfc.nasa.gov/data/map/"
DEST_DIR = "./cmb_data"
os.makedirs(DEST_DIR, exist_ok=True)

def fetch_fits_links():
    print("[Crawler] Accessing:", BASE_URL)
    r = requests.get(BASE_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    return [BASE_URL + link.get("href") for link in soup.find_all("a") if link.get("href", "").endswith(".fits")]

def download_fits_file(url):
    filename = os.path.join(DEST_DIR, url.split("/")[-1])
    if os.path.exists(filename):
        return
    print(f"[Download] {filename}")
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)

if __name__ == "__main__":
    fits_urls = fetch_fits_links()
    for u in fits_urls[:3]:  # Limit for demo/testing
        download_fits_file(u)
