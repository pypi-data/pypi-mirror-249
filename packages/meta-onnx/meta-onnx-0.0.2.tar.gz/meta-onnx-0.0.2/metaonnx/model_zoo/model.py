import onnxruntime
import numpy as np


def load_model(model_path):
    model = onnxruntime.InferenceSession(model_path,
                                         providers=['CUDAExecutionProvider',
                                                    'CPUExecutionProvider'])
    model_inputs = model.get_inputs()
    model_outputs = model.get_outputs()
    input_names = [model_inputs[i].name for i in range(len(model_inputs))]
    output_names = [model_outputs[i].name for i in range(len(model_outputs))]

    return model, input_names, output_names


def run(images, model, input_names, output_names):
    input_tensor = np.array(images) if isinstance(images, list) else images[np.newaxis, :, :, :]
    outputs = model.run(output_names, {input_names[0]: input_tensor})

    return outputs
