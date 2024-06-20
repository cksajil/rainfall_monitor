import librosa
import numpy as np
from os import remove
from .helper import config
from os.path import exists


def create_cnn_data(raw_data: np.ndarray) -> np.ndarray:
    """
    Calculates and returns STFT on raw input audio provided
    """
    Zxx = librosa.stft(raw_data)
    stft_sample = np.abs(Zxx)
    return stft_sample[np.newaxis, :, :]


def combine_audios(file_paths: list) -> np.ndarray:
    """
    Combines various audio files in their chronological order
    based on list of audio file paths provided
    """
    audio = np.array([])
    for file_path in file_paths:
        audio_segment, _ = librosa.load(file_path, sr=int(config["sampling_rate"]))
        audio = np.append(audio, audio_segment)
    return audio


def estimate_rainfall(model: any, file_paths: list) -> float:
    """
    Computed the models prediction on input data provided
    """
    audio = combine_audios(file_paths)
    audio = audio[: config["seq_len"]]
    stft_sample = create_cnn_data(audio)
    input_details = model.get_input_details()
    output_details = model.get_output_details()
    stft_sample = np.float32(stft_sample)
    model.set_tensor(input_details[0]["index"], stft_sample)
    model.invoke()
    y_pred = model.get_tensor(output_details[0]["index"])
    return y_pred


def delete_files(file_paths):
    """Function to delete wav files after inference"""
    for file_path in file_paths:
        try:
            if exists(file_path):
                remove(file_path)
                print(f"Deleted: {file_path}")
            else:
                print(f"File does not exist: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
