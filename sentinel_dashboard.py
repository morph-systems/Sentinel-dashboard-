import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sentinel_dashboard_autoload import load_latest_entropy_data

st.set_page_config(page_title="Sentinel Dashboard", layout="wide")
st.title("Entropy Sentinel Dashboard")

df = load_latest_entropy_data()

st.subheader("Entropy Signal Timeline")
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(df["Time"], df["Entropy"], label="Entropy", color="teal")
ax.fill_between(df["Time"], df["Entropy"], where=df["Sentinel_Anomaly"].astype(bool), color='purple', alpha=0.3, label="Sentinel Anomaly")
ax.fill_between(df["Time"], df["Entropy"], where=df["QGI_Meta_Coherence_Flag"].astype(bool), color='orange', alpha=0.2, label="QGI Risk")
ax.set_xlabel("Time")
ax.set_ylabel("Entropy")
ax.set_title("Entropy Evolution with Sentinel/QGI Flags")
ax.legend()
st.pyplot(fig)
