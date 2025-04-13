# Sentinel Auto-Loader Hook for .npz files

import os
import numpy as np
import pandas as pd

SYNC_FOLDER = "./cloud_sync"

def load_latest_entropy_data():
    files = [f for f in os.listdir(SYNC_FOLDER) if f.endswith(".npz")]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(SYNC_FOLDER, x)), reverse=True)
    if not files:
        return pd.DataFrame(columns=["Time", "Entropy", "Sentinel_Anomaly", "QGI_Meta_Coherence_Flag"])
    fpath = os.path.join(SYNC_FOLDER, files[0])
    data = np.load(fpath)
    entropy = data["entropy"]
    return pd.DataFrame({
        "Time": range(len(entropy)),
        "Entropy": entropy,
        "Sentinel_Anomaly": np.zeros(len(entropy)),
        "QGI_Meta_Coherence_Flag": np.zeros(len(entropy))
    })
