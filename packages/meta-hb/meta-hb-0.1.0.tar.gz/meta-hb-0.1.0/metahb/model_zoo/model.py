import platform
import numpy as np

if platform.machine() == 'aarch64':
    from hobot_dnn import pyeasy_dnn as HB
else:
    from horizon_tc_ui import HB_ONNXRuntime as HB


def load_model(model_path):
    if platform.machine() == 'aarch64':
        model = HB.load(model_path)[0]
    else:
        model = HB(model_path)

    return model


def run(images, model):
    input_tensor = np.array(images) if isinstance(images, list) else images[np.newaxis, :, :, :]
    if platform.machine() == 'aarch64':
        outputs = model.forward(input_tensor.astype(np.uint8))
    else:
        input_names = model.input_names
        output_names = model.output_names
        outputs = model.run(output_names, {input_names[0]: input_tensor.astype(np.uint8)}, input_offset=128)

    return outputs
