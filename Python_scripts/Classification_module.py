from tflite_runtime.interpreter import Interpreter
import os
import models
import cv2
import time
import argparse
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json


FIREBASE_URL = 'https://parkingstatus-5cf98-default-rtdb.europe-west1.firebasedatabase.app/'
MODEL_FILE = 'C16C32x2C16FC128.tflite'
cwd = os.getcwd()

parser = argparse.ArgumentParser(description='Initialize the camera position')
parser.add_argument('plot_name', type=str,
                    help='name of your parking lot layout')
args = vars(parser.parse_args())
plot_name = args['plot_name']

#Firebase initial settings 
cred = credentials.Certificate(f'{cwd}/firebase_credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': FIREBASE_URL
})
dbref = db.reference(f'/parking/{plot_name}')
dbrefM = db.reference(f'/plot_settings/{plot_name}/roiMap')

#Model initial settings
interpreter = Interpreter(f'{cwd}/Trained_models/{MODEL_FILE}')
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# print(device)
# model = models.C16C32C16C8x6FC64(2).to(device)
# model.load_state_dict(torch.load(cwd + '/Trained_models/' + type(model).__name__ + '.pth', map_location=device))

feed = cv2.VideoCapture(0)

def updateOutput(output):
    output = output.tolist()
    output = dict(zip(range(len(output)), output))
    output = json.dumps(output)
    dbref.set(json.loads(output))

def runClassifier(feed):
    patches = dbrefM.get()
    prevOutput = [2] * len(patches)
    output = [1] * len(patches)
    while True:
        start = time.time()
        images = []
        ret, img = feed.read()
        for p in patches:
            coordinates = p.split(' ')
            if(len(coordinates) < 4):
                break
            x1 = int(coordinates[0])
            y1 = int(coordinates[1])
            x2 = int(coordinates[2])
            y2 = int(coordinates[3])
            patch_img = img[y1:y1+y2,x1:x1+x2]
            patch_img = cv2.resize(patch_img,(150,150),interpolation = cv2.INTER_AREA)
            patch_img = (patch_img).astype('float32')
            images.append(patch_img)
        images = np.array(images)
        images = np.transpose(images, (0, 3, 1, 2))

        interpreter.resize_tensor_input(input_details[0]['index'],[len(images),3, 150, 150])
        interpreter.allocate_tensors()
        interpreter.set_tensor(input_details[0]['index'],images)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details[0]['index'])
        print(output)
        output = np.squeeze(output)
        output = np.argmax(output, axis=1)
        if(not np.array_equal(prevOutput, output)):
            prevOutput = output
            updateOutput(output)
        
        end = time.time()
        print("time took: ", end-start)
        print("number of spots classified: ", len(patches))
runClassifier(feed)
