## TinyML Stup Guide
The following is the set of general steps needed to create TinyML version of the deep learning model already trained. It is important have a general idea about the hardware we are targetting. The following table shows common embedded boards that supports TinyML and their specifications (RAM, Flash etc.)
### TinyML Boards Specifications

| Board                     | RAM    | Flash | Processor                                  | Power                    | Microphone                                     |
|---------------------------|--------|-------|--------------------------------------------|--------------------------|------------------------------------------------|
| SparkFun Edge             | 384KB  | 1MB   | 32-bit ARM Cortex-M4F processor            | 6uA/MHz                  | 2x MEMS microphones with operational amplifier |
| Arduino Nano 33 BLE Sense | 256KB  | 1MB   | 64 MHz Arm® Cortex-M4F (with FPU)          | 150 uWatts - 23.5 mWatts | MP34DT05                                       |
| STM32F746G Discovery Kit  | 340KB  | 1MB   | STM32F746NGH6 Arm® Cortex®                 |                          | Microphone and Headphone Jack                  |
| Raspberry Pi Pico         | 264KB  | 2MB   | Dual-core Arm Cortex-M0+ processor 133 MHz |                          |                                                |
### Model Size
As we can see most of the boards are having a flash memory of ~1MB. TinyML steps generally does a 4X reduction of already trained models. Hence we are targetting to convert trained models which are less than 4MB in size.

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
model_size_kb = tflite_model_file.write_bytes(tflite_model)/1024
print("Size of TensorFlow Lite Model: {} KB:", model_size_kb)
```
## Testing TinyML Model without Edge Device
The TinyML model we just created can be tested using TensorFlow interpretr.
