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


def combine_and_trim_audios(file_paths):
    audio = combine_audios(file_paths)
    audio = audio[: config["seq_len"]]
    audio = np.float32(audio)
    return audio


def estimate_rainfall(interpreter: any, file_paths: list) -> float:
    """
    Computed the models prediction on input data provided
    """
    audio = combine_and_trim_audios(file_paths)
    stft_sample = create_cnn_data(audio)
    del audio
    stft_sample = np.expand_dims(stft_sample, axis=0)
    stft_sample = np.reshape(stft_sample, (1, 1025, 2672, 1))
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]["index"], stft_sample)
    interpreter.invoke()
    y_pred = interpreter.get_tensor(output_details[0]["index"])[0][0][0]
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
