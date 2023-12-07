import librosa
import numpy as np
from .helper import load_config


def create_cnn_data(raw_data):
    Zxx = librosa.stft(raw_data)
    stft_sample = np.abs(Zxx)
    return stft_sample[np.newaxis, :, :]


def estimate_rainfall(model, file_path):
    audio, Fs = librosa.load(file_path)
    config = load_config("config.yaml")
    audio = audio[-1 * config["seq_len"] :]
    stft_sample = create_cnn_data(audio)
    y_pred = model.predict(stft_sample, verbose=0)[0][0]
    return y_pred
