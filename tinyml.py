import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense

# Generate synthetic data
X = np.random.rand(100, 10)
y = np.random.randint(0, 2, 100)

# Create the model
model = Sequential()
model.add(Dense(16, activation="relu", input_shape=(10,)))
model.add(Dense(1, activation="sigmoid"))

# Compile the model
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

# Fit the model
model.fit(X, y, epochs=10)

# Evaluate the model
loss, accuracy = model.evaluate(X, y)
print("Loss:", loss)
print("Accuracy:", accuracy)

export_dir = "saved_TF_model/model1"
tf.saved_model.save(model, export_dir)

# Convert the model.
converter = tf.lite.TFLiteConverter.from_saved_model(export_dir)
tflite_model = converter.convert()
