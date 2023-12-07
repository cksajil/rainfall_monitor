import librosa
import numpy as np
from .helper import load_config


def create_cnn_data(raw_data):
    Zxx = librosa.stft(raw_data)
    stft_sample = np.abs(Zxx)
    return stft_sample[np.newaxis, :, :]


def combine_audios(file_paths):
    audio = np.array([])
    config = load_config("config.yaml")
    for file_path in file_paths:
        audio_segment, _ = librosa.load(file_path)
        audio = np.append(audio, audio_segment)
    audio = audio[-1 * config["seq_len"] :]
    return audio


def estimate_rainfall(model, file_paths):
    audio = combine_audios(file_paths)
    stft_sample = create_cnn_data(audio)
    y_pred = model.predict(stft_sample, verbose=0)[0][0]
    return y_pred
