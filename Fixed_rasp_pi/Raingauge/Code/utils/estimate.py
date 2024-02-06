import librosa
import numpy as np
from .helper import load_config


def create_cnn_data(raw_data):
	"""Function to compute STFT of the audio samples"""
	Zxx = librosa.stft(raw_data)
	stft_sample = np.abs(Zxx)
	return stft_sample[np.newaxis, :, :]  # 3D array definition for the  number of inputs during the prediction


def combine_audios(file_paths):
	"""Function to merge the audio files as a numpy array"""
	audio = np.array([])
	config = load_config("config.yaml")
	for file_path in file_paths:
		audio_segment, _ = librosa.load(file_path, sr=int(config["sampling_rate"]))
		audio = np.append(audio, audio_segment)
	return audio


def estimate_rainfall(model, file_paths):
	"""Function to estimate the rainfall with the ML Model"""
	audio = combine_audios(file_paths)
	config = load_config("config.yaml")
	audio = audio[:config["seq_len"]]
	stft_sample = create_cnn_data(audio)
	y_pred = model.predict(stft_sample, verbose=0)[0][0]
	return y_pred
