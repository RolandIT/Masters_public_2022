# Script for selecting the regions of interest from the lvie camera feed

import cv2
import os
import argparse
import base64
import numpy as np
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


FIREBASE_URL = 'https://parkingstatus-5cf98-default-rtdb.europe-west1.firebasedatabase.app/'

parser = argparse.ArgumentParser(description='Initialize the camera position')
parser.add_argument('plot_name', type=str,
                    help='name of your parking lot layout')
args = vars(parser.parse_args())
plot_name = args['plot_name']

cwd = os.getcwd()
#Firebase initial settings 
cred = credentials.Certificate(cwd + "/firebase_credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': FIREBASE_URL
})
dbref = db.reference(f'plot_settings/{plot_name}/CalibrationFrame/latestFrame')
frame = dbref.get()
frame = base64.b64decode(frame)
frame = np.fromstring(frame, np.uint8)
img = cv2.imdecode(frame, cv2.IMREAD_UNCHANGED)

cv2.namedWindow("Select each parking space",cv2.WINDOW_AUTOSIZE)
regions = cv2.selectROIs("Select each parking space", img)
immap = {}
i = 0
for r in regions:
    immap[i] = str(r[0]) + ' ' + str(r[1]) + ' ' + str(r[2]) + ' ' + str(r[3]) + '\n'
    i+=1

dbref = db.reference(f'plot_settings/{plot_name}/roiMap')
data = json.dumps(immap)
dbref.set(json.loads(data))



