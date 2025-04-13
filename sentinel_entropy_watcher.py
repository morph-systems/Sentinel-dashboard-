# === Sentinel Entropy Watcher (Real-Time) ===

import os
import time
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from astropy.io import fits

# Define directories
WATCH_FOLDER = "/home/user/sentinel/cmb_data"
SYNC_FOLDER = "/home/user/sentinel/cloud_sync"

# Ensure directories exist
os.makedirs(WATCH_FOLDER, exist_ok=True)
os.makedirs(SYNC_FOLDER, exist_ok=True)

# Entropy parser function
def extract_entropy_from_fits(fits_file):
    with fits.open(fits_file) as hdul:
        data = hdul[1].data if len(hdul) > 1 else hdul[0].data
        if data is None or not isinstance(data, np.ndarray):
            raise ValueError("FITS file does not contain valid image data")
        entropy_map = np.log1p(np.abs(data))
        entropy_waveform = np.mean(entropy_map, axis=0) if entropy_map.ndim == 2 else entropy_map
        return entropy_waveform

# Save to sync directory
def sync_to_cloud(local_file, waveform):
    base = os.path.splitext(os.path.basename(local_file))[0]
    out_path = os.path.join(SYNC_FOLDER, f"{base}.npz")
    np.savez(out_path, entropy=waveform)
    print(f"[SYNCED] {out_path}")

# Watchdog handler
class EntropyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".fits"):
            return
        time.sleep(1)  # Wait for file write to complete
        print(f"[NEW FILE] Processing {event.src_path}")
        try:
            waveform = extract_entropy_from_fits(event.src_path)
            sync_to_cloud(event.src_path, waveform)
        except Exception as e:
            print(f"[ERROR] {e}")

# Main loop
if __name__ == "__main__":
    print(f"[WATCHING] {WATCH_FOLDER} for new FITS files...")
    observer = Observer()
    handler = EntropyHandler()
    observer.schedule(handler, WATCH_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
