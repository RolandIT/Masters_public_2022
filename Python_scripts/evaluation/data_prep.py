import pandas as pd 
import os
import cv2

def calibrateImg(img):
    cv2.namedWindow("Select each parking space",cv2.WINDOW_AUTOSIZE)
    regions = cv2.selectROIs("Select each parking space", img)
    cv2.destroyAllWindows()
    return regions

def getLabel(path,feed):
    occupancy = ""
    print(path)
    img = cv2.imread(path)
    if feed == "1":
        for r in feed1ROI:
            x1=r[0]
            y1=r[1]
            x2=r[2]
            y2=r[3]
            img_crop=img[y1:y1+y2,x1:x1+x2]
            height, width, channels = img_crop.shape
            img_crop = cv2.resize(img_crop, (width*5,height*5), interpolation = cv2.INTER_AREA)
            cv2.destroyAllWindows()
            cv2.imshow('Press e if empty o if occupied', img_crop)
            pressedKey = cv2.waitKey(0)
            if pressedKey == ord('o'):
                occupancy+="1"
            elif pressedKey == ord('e'):
                occupancy+="0"

    if feed == "2":
        for r in feed2ROI:
            x1=r[0]
            y1=r[1]
            x2=r[2]
            y2=r[3]
            img_crop=img[y1:y1+y2,x1:x1+x2]
            height, width, channels = img_crop.shape
            img_crop = cv2.resize(img_crop, (width*5,height*5), interpolation = cv2.INTER_AREA)
            cv2.destroyAllWindows()
            cv2.imshow('Press e if empty o if occupied', img_crop)
            pressedKey = cv2.waitKey(0)
            if pressedKey == ord('o'):
                occupancy+="1"
            elif pressedKey == ord('e'):
                occupancy+="0"
        return occupancy

    if feed == "3":
        for r in feed3ROI:
            x1=r[0]
            y1=r[1]
            x2=r[2]
            y2=r[3]
            img_crop=img[y1:y1+y2,x1:x1+x2]
            print(img_crop)
            height, width, channels = img_crop.shape
            img_crop = cv2.resize(img_crop, (width*5,height*5), interpolation = cv2.INTER_AREA)
            cv2.destroyAllWindows()
            cv2.imshow('Press e if empty o if occupied', img_crop)
            pressedKey = cv2.waitKey(0)
            if pressedKey == ord('o'):
                occupancy+="1"
            elif pressedKey == ord('e'):
                occupancy+="0"
    return occupancy

def listentries(path,images):
    entries = os.scandir(path)
    for e in entries:
        if os.path.isdir(path + '/' + e.name):
            listentries(path + '/' + e.name, images)
        else:
            images['impath'].append(path + '/' + e.name)
            if "feed1" in path:
                images['occupancy'].append(getLabel(path + '/' + e.name,"1"))
            if "feed2" in path:
                images['occupancy'].append(getLabel(path + '/' + e.name,"2"))
            if "feed3" in path:
                images['occupancy'].append(getLabel(path + '/' + e.name,"3"))
            

feed1img = cv2.imread("./images/feed1/2022-03-15-13-14-52.jpg")
feed1ROI = calibrateImg(feed1img)
with open('feed1roi', 'w+') as f:
    f.write(str(feed1ROI))

feed2img = cv2.imread("./images/feed2/2022-03-17-12-54-21.jpg")
feed2ROI = calibrateImg(feed2img)
with open('feed2roi', 'w+') as f:
    f.write(str(feed2ROI))

feed3img = cv2.imread("./images/feed3/2022-03-15-21-57-15.jpg")
feed3ROI = calibrateImg(feed3img)
with open('feed3roi', 'w+') as f:
    f.write(str(feed3ROI))

dir = './images'
images = {'impath': [], 'occupancy': []}
listentries(dir,images)
im = pd.DataFrame(images)
with open('labels_experiment.csv', 'w+') as f:
    f.write(im.to_csv(index=False))