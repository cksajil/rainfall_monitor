import librosa
import numpy as np


def create_cnn_data(raw_data):
    Zxx = librosa.stft(raw_data)
    stft_sample = np.abs(Zxx)
    return stft_sample


def estimate_rainfall(model, file_path):
    audio, Fs = librosa.load(file_path)
    stft_sample = create_cnn_data(audio)
    y_pred = model.predict(stft_sample, verbose=0)[0][0]
    return y_pred
