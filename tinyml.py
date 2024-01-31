import pathlib
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

tflite_model_file = pathlib.Path("model.tflite")
model_size_kb = tflite_model_file.write_bytes(tflite_model) / 1024
print("Size of TensorFlow Lite Model: {} KB:", model_size_kb)

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_content=tflite_model)
interpreter.allocate_tensors()

# Get input and output tensors - to run inference
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print(input_details)
print(output_details)


to_predict = a = np.float32(np.random.rand(1, 10))
print("value to predict:", to_predict)

# setting the 'to_predict' value at the appropriate index location of input tensor
interpreter.set_tensor(input_details[0]["index"], to_predict)

# running inference on 'to_predict' value
interpreter.invoke()

# read the result that is stored at the appropriate index location of output tensor
tflite_results = interpreter.get_tensor(output_details[0]["index"])
print("predicted value:", tflite_results)
