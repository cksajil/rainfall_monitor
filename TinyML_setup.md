## TinyML Stup Guide
The following is the set of general steps needed to create TinyML version of the deep learning model already trained. It is important have a general idea about the low specification hardware we are targetting. The following table shows common embedded boards that supports TinyML and their specifications (RAM, Flash etc.)
### TinyML Boards Specifications

| Board                     | RAM    | Flash | Processor                                  | Power                    | Microphone                                     |
|---------------------------|--------|-------|--------------------------------------------|--------------------------|------------------------------------------------|
| SparkFun Edge             | 384KB  | 1MB   | 32-bit ARM Cortex-M4F processor            | 6uA/MHz                  | 2x MEMS microphones with operational amplifier |
| Arduino Nano 33 BLE Sense | 256KB  | 1MB   | 64 MHz Arm® Cortex-M4F (with FPU)          | 150 uWatts - 23.5 mWatts | MP34DT05                                       |
| STM32F746G Discovery Kit  | 340KB  | 1MB   | STM32F746NGH6 Arm® Cortex®                 |                          | Microphone and Headphone Jack                  |
| Raspberry Pi Pico         | 264KB  | 2MB   | Dual-core Arm Cortex-M0+ processor 133 MHz |                          |                                                |
### Model Size
As we can see most of the boards are having a flash memory of **~1MB**. TinyML steps generally does a **4X** reduction of already trained models. Hence we are targetting to convert trained models which are usually not more than **4MB** in size.

## Conversion to TinyML Model

### Saving Trained Keras Model
The following code snippet saves the trained Keras models to a specific folder.

```python
export_dir = 'saved_TF_model/model1'
tf.saved_model.save(model, export_dir)
```
### Convert Keras/TF Model to TFLite Model
The following code snippet converts the trained model to tensorflow lite model.
```python
converter = tf.lite.TFLiteConverter.from_saved_model(export_dir)
tflite_model = converter.convert()  
```
### Saving TFLite Model
Now we can save the tflite model and get its size in KB.
```python
import pathlib
tflite_model_file = pathlib.Path("model.tflite")
model_size_kb = tflite_model_file.write_bytes(tflite_model) /  1024
print("Size of TensorFlow Lite Model: {} KB:".format(model_size_kb))
```
## Testing TinyML Model without Edge Device
```python
# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_content=tflite_model)
interpreter.allocate_tensors()

# Get input and output tensors - to run inference
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print(input_details)
print(output_details)
```
This will give elaborate details of the tflite models input and output such as input shape, output shape, quantization, sparsity etc. ***We have to make sure that the input tensor we pass in have the same shape and dtype (Float32 or Float64) as the tflite models input shape we just inspected***.

Now we can pass the input tensor and get the output tensor.

```python
to_predict = np.float32(np.random.rand(1, 10))
print("value to predict:", to_predict)

# setting the 'to_predict' value at the appropriate index location of input tensor
interpreter.set_tensor(input_details[0]["index"], to_predict)

# running inference on 'to_predict' value
interpreter.invoke()

# read the result that is stored at the appropriate index location of output tensor
tflite_results = interpreter.get_tensor(output_details[0]["index"])
print("predicted value:", tflite_results)
```
## TFLite Optimizations
###  Dynamic Range Quantization
In additions to tflite conversion, it is possible to explore the effect of TF Lite optimization on size, performance, and accuracy of the model. Just like the earlier case we can load the full size model and do the quantization optimization.
```python
#Again loads the full size model
converter = tf.lite.TFLiteConverter.from_saved_model(export_dir)

#This will represent model weights as 8-bit precision values as opposed to Float32, resulting in ~4X reduction
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model_opt = converter.convert()

tflite_model_opt_1 = pathlib.Path("model_opt_1.tflite")
model_size_kb_opt = tflite_model_file.write_bytes(tflite_model_opt) /  1024
print("Size of TensorFlow Lite Opt Model: {} KB:".format(model_size_kb_opt))

size_reduction = np.round(model_size_kb / model_size_kb_opt, 1)
print("There is {}x reduction in size".format(size_reduction))
```
###  Integer Quantization
In integer quantization the weights and activations are converted to 8-bit fixed-point numbers from 32-bit floating point numbers. This is done by making use of a representative dataset. The steps to do the same is shown below.
```python
converter = tf.lite.TFLiteConverter.from_saved_model(CATS_VS_DOGS_SAVED_MODEL)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

def	representative_data_gen():
	for input_value, _ in test_batches.take(100):
		yield [input_value]
		
converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]

tflite_model_opt_2 = converter.convert()
tflite_model_opt_2 = pathlib.Path("model_opt_2.tflite")
tflite_model_opt_2.write_bytes(tflite_model)
```