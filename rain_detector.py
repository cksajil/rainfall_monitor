import librosa
import numpy as np
import pandas as pd
from tqdm import tqdm
from os.path import join
from os import listdir
import tensorflow as tf
from keras.layers import Dense
from keras.models import Sequential
from utils.helper import EarlyStopper
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.initializers import RandomUniform
from tensorflow.keras.regularizers import l2
from sklearn.model_selection import train_test_split

RECORDING_DIR = "./data/rain_mini_dataset"
CLASSES = ["rain", "ambient"]

EPOCHS = 10
BATCH_SIZE =  32
SAMPLE_LEN = 22050

file_names = []
target = []

for label in CLASSES:
    fnames = listdir(join(RECORDING_DIR, label))
    num_samples = len(fnames)
    file_names.extend(fnames)
    target.extend([label]*num_samples)

basic_data = pd.DataFrame()
basic_data["filename"] = file_names
basic_data["class"] = target
basic_data["target"] = basic_data["class"].replace({'ambient': 0, 'rain': 1})

spectrum_data = np.empty((0, 220500), int) 

for index, row in tqdm(basic_data.iterrows(), total=basic_data.shape[0]):
    file_path = join(RECORDING_DIR, row["class"], row["filename"])
    x, Fs = librosa.load(file_path)
    xfft= np.abs(np.fft.fft(x))  
    spectrum_data = np.vstack([spectrum_data, xfft])

X_train, X_test, y_train, y_test = train_test_split(
    spectrum_data,
    basic_data["target"],
    test_size=0.3,
    shuffle=True,
)

def create_dnn(in_shape):
    model = Sequential()
    model.add(Dense(32, activation='relu', input_shape=in_shape))
    model.add(Dense(64, activation='relu', input_shape=in_shape))
    model.add(Dense(128, kernel_initializer=RandomUniform(minval=-0.05,
                    maxval=0.05), kernel_regularizer=l2(0.001),
                    activation='relu'))
    model.add(Dense(256, kernel_initializer=RandomUniform(minval=-0.05,
                    maxval=0.05), kernel_regularizer=l2(0.001), 
                    activation='relu'))
    model.add(Dense(512, kernel_initializer=RandomUniform(minval=-0.05,
                    maxval=0.05), kernel_regularizer=l2(0.001), 
                    activation='relu'))
    model.add(Dense(256, activation='relu', kernel_regularizer=l2(0.001)))
    model.add(Dense(128, activation='relu', kernel_regularizer=l2(0.001)))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(Dense(64, activation='relu', kernel_regularizer=l2(0.001)))
    model.add(Dense(2, kernel_initializer=RandomUniform(minval=-0.05,
                    maxval=0.05), kernel_regularizer=l2(0.001),
                    activation='softmax'))
    
    model.compile(optimizer='Adam',
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

dnn_model = create_dnn(X_train[0].shape)

cp_callback = ModelCheckpoint(
    filepath="./model/dnn.h5",
    monitor="val_accuracy",
    validation_data=(X_test, y_test),
    verbose=1,
    save_best_only=True,
    mode="auto")

early_stopper_cb = EarlyStopper(0.9901)

history = dnn_model.fit(
    X_train,
    y_train,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_split=0.3,
    callbacks=[cp_callback, early_stopper_cb])

loss, test_accuracy = dnn_model.evaluate(X_test, y_test, verbose=2)
stats = "Trained model, accuracy: {:5.2f}% ".format(100 * test_accuracy)
print(stats)
