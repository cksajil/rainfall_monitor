import pickle
import librosa
import numpy as np
import tensorflow as tf
import tensorflow_io as tfio
import matplotlib.pyplot as plt

fid = open("audio_files.pkl", "rb")
audio_files = pickle.load(fid)  # python dictionary
audio_yes_loud = audio_files["audio_yes_loud"]
sr_yes_loud = audio_files["sr_yes_loud"]


spectrogram_yes_loud = tfio.audio.spectrogram(
    audio_yes_loud / 1.0,
    nfft=2048,
    window=len(audio_yes_loud),
    stride=int(sr_yes_loud * 0.008),
)

spectrogram_yes_loud = tf.math.log(spectrogram_yes_loud)
spectrogram_yes_loud = spectrogram_yes_loud.numpy()

mfcc_yes_loud = librosa.power_to_db(
    librosa.feature.melspectrogram(
        np.float32(audio_yes_loud),
        sr=sr_yes_loud,
        n_fft=2048,
        hop_length=512,
        n_mels=128,
    ),
    ref=np.max,
)

fig1, ax1 = plt.subplots()
plt.imshow(spectrogram_yes_loud, aspect="auto")
plt.title("Spectrogram")
plt.show()

fig2, ax2 = plt.subplots()
plt.imshow(mfcc_yes_loud, aspect="auto")
plt.title("Spectrogram")
plt.show()
