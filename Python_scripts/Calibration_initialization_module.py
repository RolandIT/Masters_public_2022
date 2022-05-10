import cv2
import os
import argparse
import base64
import firebase_admin
import json
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
dbref = db.reference(f'plot_settings/{plot_name}/CalibrationFrame')

vid = cv2.VideoCapture(0)
ret, frame = vid.read()
vid.release()
cv2.destroyAllWindows()

retval, buffer = cv2.imencode('.jpg', frame)
b64im = base64.b64encode(buffer)
data = {"latestFrame" : b64im.decode('utf-8')}
data = json.dumps(data)
dbref.set(json.loads(data))

