import os
import torch
import models
import argparse
import numpy as np
import onnx
from onnx_tf.backend import prepare
import tensorflow as tf


parser = argparse.ArgumentParser(description='Convert pytorch models to tensorflow lite.')
parser.add_argument('modelname', type=str,
                    help='name of the saved pytorch model')
args = vars(parser.parse_args())
model_name = args['modelname']
cwd = os.getcwd()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_class = getattr(models, model_name)(2)
model = model_class.to(device)
model.load_state_dict(torch.load(cwd + '/Trained_models/' + type(model).__name__ + '.pth'))

dummy_input = np.random.rand(1, 150, 150, 3)
dummy_input = torch.tensor(dummy_input)
dummy_input = torch.transpose(dummy_input, 1, 3)
dummy_input = dummy_input.float()
dummy_input = dummy_input.to(device)

torch.onnx.export(model, dummy_input,cwd + '/Trained_models/' + type(model).__name__ + '.onnx')
model = onnx.load(cwd + '/Trained_models/' + type(model).__name__ + '.onnx')
tf_rep = prepare(model)
tf_rep.export_graph("TF_saved_model")

converter = tf.lite.TFLiteConverter.from_saved_model('TF_saved_model') 
tflite_model = converter.convert()

with open(cwd + '/Trained_models/' + model_name + '.tflite', 'wb') as f:
  f.write(tflite_model)