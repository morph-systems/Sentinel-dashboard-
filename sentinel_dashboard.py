
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sentinel Dashboard", layout="wide")
st.title("Entropy Sentinel Dashboard")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Entropy Signals", "Upload FITS", "Collapse Detection"])

def load_entropy_data():
    try:
        df = pd.read_csv("entropy_waveform_with_sentinel_prediction.csv")
    except:
        df = pd.DataFrame({
            "Time": np.linspace(0, 10, 300),
            "Entropy": np.random.rand(300),
            "Sentinel_Anomaly": np.zeros(300),
            "QGI_Meta_Coherence_Flag": np.zeros(300),
        })
    return df

if page == "Entropy Signals":
    df = load_entropy_data()
    st.subheader("Entropy Signal Timeline")
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df["Time"], df["Entropy"], label="Entropy", color="teal")
    ax.fill_between(df["Time"], df["Entropy"], where=df["Sentinel_Anomaly"].astype(bool), color='purple', alpha=0.3)
    ax.fill_between(df["Time"], df["Entropy"], where=df["QGI_Meta_Coherence_Flag"].astype(bool), color='orange', alpha=0.2)
    ax.set_xlabel("Time")
    ax.set_ylabel("Entropy")
    st.pyplot(fig)

elif page == "Upload FITS":
    st.subheader("CMB FITS Loader")
    uploaded_file = st.file_uploader("Upload a CMB .FITS file", type=["fits"])
    if uploaded_file:
        st.success(f"Received {uploaded_file.name}. Processing...")

elif page == "Collapse Detection":
    df = load_entropy_data()
    flagged = df[(df["Sentinel_Anomaly"] == 1) | (df["QGI_Meta_Coherence_Flag"] == 1)]
    st.subheader("Detected Collapse Zones")
    st.dataframe(flagged)
