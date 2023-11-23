import librosa
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


def analyze_audio(file):
    audio, sr = librosa.load(file, sr=None)
    duration = librosa.get_duration(y=audio, sr=sr)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(audio)), ref=np.max)

    fig, ax = plt.subplots(2, 1, figsize=(10, 10))
    ax[0].plot(np.arange(len(audio)) / sr, audio)
    ax[0].set_title("Waveform")
    ax[0].set_xlabel("Time (s)")
    ax[0].set_ylabel("Amplitude")

    librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="log", ax=ax[1])
    ax[1].set_title("Spectrogram")
    ax[1].set_xlabel("Time (s)")
    ax[1].set_ylabel("Frequency (Hz)")

    st.pyplot(fig)
    st.write(f"Audio duration: {duration:.2f} seconds")
    st.write(f"Sampling rate: {sr} Hz")


st.title("Acoustic Rainfall Estimation App")
uploaded_file = st.file_uploader("Choose a WAV file", type="wav")

if uploaded_file is not None:
    st.subheader("Uploaded WAV file")
    st.audio(uploaded_file, format="audio/wav")

    st.subheader("Results")
    analyze_audio(uploaded_file)
