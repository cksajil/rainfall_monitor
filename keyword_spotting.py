import os

# import pickle
# import librosa
# import numpy as np
# import tensorflow as tf
# import tensorflow_io as tfio
# import matplotlib.pyplot as plt

# fid = open("audio_files.pkl", "rb")
# audio_files = pickle.load(fid)  # python dictionary
# audio_yes_loud = audio_files["audio_yes_loud"]
# sr_yes_loud = audio_files["sr_yes_loud"]


# spectrogram_yes_loud = tfio.audio.spectrogram(
#     audio_yes_loud / 1.0,
#     nfft=2048,
#     window=len(audio_yes_loud),
#     stride=int(sr_yes_loud * 0.008),
# )

# spectrogram_yes_loud = tf.math.log(spectrogram_yes_loud)
# spectrogram_yes_loud = spectrogram_yes_loud.numpy()
# librosa_mel_data = librosa.feature.melspectrogram(
#     y=np.float32(audio_yes_loud), sr=sr_yes_loud, n_fft=2048, hop_length=512
# )

# mfcc_yes_loud = librosa.power_to_db(librosa_mel_data, ref=np.max)

# fig1, ax1 = plt.subplots()
# plt.imshow(spectrogram_yes_loud, aspect="auto")
# plt.title("Spectrogram")


# fig2, ax2 = plt.subplots()
# plt.imshow(mfcc_yes_loud, aspect="auto")
# plt.title("Spectrogram")
# plt.show()

WANTED_WORDS = "yes,no"
number_of_labels = WANTED_WORDS.count(",") + 1
number_of_total_labels = number_of_labels + 2
equal_percentage_of_training_samples = int(100.0 / (number_of_total_labels))
SILENT_PERCENTAGE = equal_percentage_of_training_samples
UNKNOWN_PERCENTAGE = equal_percentage_of_training_samples

PREPROCESS = "micro"
WINDOW_STRIDE = 20
MODEL_ARCHITECTURE = "tiny_conv"
DATASET_DIR = "dataset/"
LOGS_DIR = "logs/"
TRAIN_DIR = "train/"
