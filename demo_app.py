import yaml
import librosa
import numpy as np
import streamlit as st
from stqdm import stqdm
from os.path import join
import matplotlib.pyplot as plt
from keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
from tensorflow.keras.initializers import RandomUniform
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense


def load_config(config_name):
    """
    A function to load and return config file in YAML format
    """
    CONFIG_PATH = "./config/"
    with open(join(CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)

    return config


config = load_config("config.yaml")
INFERENCE_DURATION = config["inference_duration"]
LEARNING_RATE = config["learning_rate"]
N_CLASSES = config["n_classes"]
CNN_DIM = config["cnn_dim"]
model_path = join(config["model_dir"], config["model_name"])


def load_wav(file_path):
    audio, Fs = librosa.load(file_path, sr=None)
    duration = librosa.get_duration(y=audio, sr=Fs)
    audio /= np.max(np.abs(audio), axis=0)
    return audio, Fs, duration


def create_cnn_data(raw_data):
    stft_data = np.empty(shape=[0, CNN_DIM[0], CNN_DIM[1]])
    for row in raw_data:
        Zxx = librosa.stft(row)
        stft_sample = np.abs(Zxx)
        stft_data = np.vstack([stft_data, stft_sample[np.newaxis, ...]])
    return stft_data


def create_cnn_model(in_shape):
    model = Sequential()
    adamopt = Adam(learning_rate=LEARNING_RATE, beta_1=0.9, beta_2=0.999, epsilon=1e-8)
    model.add(
        Conv2D(
            8,
            kernel_size=(3, 3),
            activation="relu",
            input_shape=(in_shape[0], in_shape[1], 1),
        )
    )
    model.add(Conv2D(16, (2, 2), activation="relu"))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(32, (3, 3), activation="relu"))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(16, (3, 3), activation="relu"))
    model.add(Flatten())
    model.add(
        Dense(
            8,
            kernel_initializer=RandomUniform(minval=-0.05, maxval=0.05),
            kernel_regularizer=l2(0.001),
            activation="relu",
        )
    )
    model.add(
        Dense(
            N_CLASSES,
            kernel_initializer=RandomUniform(minval=-0.05, maxval=0.05),
            kernel_regularizer=l2(0.001),
            activation="softmax",
        )
    )

    model.compile(
        optimizer=adamopt, loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )
    return model


def count_rain_drops(model, file_path):
    audio, Fs, duration = load_wav(file_path)
    segment_len = int(INFERENCE_DURATION * Fs)
    n_segments = int(duration / INFERENCE_DURATION)
    n_drops = 0

    for i in stqdm(range(n_segments)):
        audio_segment = audio[i * segment_len : i * segment_len + segment_len]
        audio_segment = audio_segment.reshape(1, -1)
        spectrum_data = create_cnn_data(audio_segment)
        y_pred = model.predict(spectrum_data, verbose=0)[0]
        indx = np.argmax(y_pred)
        n_drops += indx
    return audio, Fs, n_drops, duration


def plot_spectrogram(audio):
    D = librosa.amplitude_to_db(np.abs(librosa.stft(audio)), ref=np.max)
    fig, ax = plt.subplots(figsize=(10, 4))
    librosa.display.specshow(D, sr=Fs, x_axis="time", y_axis="log", ax=ax)
    ax.set_title("Spectrogram")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    st.pyplot(fig)


st.title("Acoustic Rainfall Estimation App")
file_path = st.file_uploader("Choose a WAV file", type="wav")

if file_path is not None:
    model = create_cnn_model(CNN_DIM)
    model.build(input_shape=CNN_DIM)
    model.load_weights(model_path)

    st.subheader("Results")
    audio, Fs, n_drops, duration = count_rain_drops(model, file_path)
    col1, col2, col3 = st.columns(3)
    col1.metric(
        label="No. of rain drops detected", value=n_drops, delta_color="inverse"
    )
    col2.metric(label="Audio duration (sec)", value=duration, delta_color="inverse")
    col3.metric(label="Sampling rate (samples/sec)", value=Fs, delta_color="inverse")

    plot_spectrogram(audio)
    st.audio(file_path, format="audio/wav")
