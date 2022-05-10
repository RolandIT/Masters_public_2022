from torch.utils.data import Dataset
import pandas as pd 
import os
import cv2

class TrainingDataset(Dataset):
    def __init__(self, labels_file, dataset_dir, transforms = None):
        self.labels = pd.read_csv(labels_file)
        self.transforms = transforms
        self.dataset_dir = dataset_dir
    
    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        impath = os.path.join(self.dataset_dir, self.labels.iloc[index, 0])
        image = cv2.imread(impath)
        label = self.labels.iloc[index, 1]
        if self.transforms:
            image = self.transforms(image)
        return image, label

def imResize(im):
    return cv2.resize(im,(150,150))