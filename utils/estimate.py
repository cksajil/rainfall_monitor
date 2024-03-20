import librosa
import numpy as np
from .helper import load_config


def create_cnn_data(raw_data: np.ndarray) -> np.ndarray:
    Zxx = librosa.stft(raw_data)
    stft_sample = np.abs(Zxx)
    return stft_sample[np.newaxis, :, :]


def combine_audios(file_paths: str) -> np.ndarray:
    audio = np.array([])
    config = load_config("config.yaml")
    for file_path in file_paths:
        audio_segment, _ = librosa.load(file_path, sr=int(config["sampling_rate"]))
        audio = np.append(audio, audio_segment)
    return audio


def estimate_rainfall(model: any, file_paths: str) -> float:
    # unable to find data type of model
    # model data is collecting from functions in helper.py
    print(len(file_paths))
    audio = combine_audios(file_paths)
    config = load_config("config.yaml")
    audio = audio[: config["seq_len"]]
    stft_sample = create_cnn_data(audio)
    y_pred = model.predict(stft_sample, verbose=0)[0][0]
    return y_pred
