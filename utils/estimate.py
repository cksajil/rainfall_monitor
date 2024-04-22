import librosa
import numpy as np
from .helper import config


def create_cnn_data(raw_data: np.ndarray) -> np.ndarray:
    """
    Calculates and returns STFT on raw input audio provided
    """
    Zxx = librosa.stft(raw_data)
    stft_sample = np.abs(Zxx)
    return stft_sample[np.newaxis, :, :]


def combine_audios(file_paths: str) -> np.ndarray:
    """
    Combines various audio files in their chronological order
    based on list of audio file paths provided
    """
    audio = np.array([])
    for file_path in file_paths:
        audio_segment, _ = librosa.load(file_path, sr=int(config["sampling_rate"]))
        audio = np.append(audio, audio_segment)
    return audio


def estimate_rainfall(model: any, file_paths: str) -> float:
    """
    Computed the models prediction on input data provided
    """
    audio = combine_audios(file_paths)
    audio = audio[: config["seq_len"]]
    stft_sample = create_cnn_data(audio)
    y_pred = model.predict(stft_sample, verbose=0)[0][0]
    return y_pred
