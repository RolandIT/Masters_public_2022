import torch
import torch.nn as nn

class C16C32x2C16FC128(nn.Module):

    def __init__(self, classnum=2):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=7, stride=2, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(16, 32, kernel_size=3, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(32, 32, kernel_size=3, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(32, 32, kernel_size=3, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(32, 32, kernel_size=3, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(32, 16, kernel_size=3, padding=0),
            nn.ReLU(inplace=True),
        )
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=1)
        self.classifier = nn.Sequential(
            nn.Linear(16 * 50 * 50, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(128, classnum),
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.maxpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

class C16C32C64C128C64C16FC256(nn.Module):

    def __init__(self, classnum=2):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=7, stride=2, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(16, 32, kernel_size=5, stride=2, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(32, 64 , kernel_size=3, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(64, 128, kernel_size=3, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(128, 64, kernel_size=3, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(64, 16, kernel_size=3, padding=0),
            nn.ReLU(inplace=True),
        )
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=1)
        self.classifier = nn.Sequential(
            nn.Linear(16 * 15 * 15, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(256, classnum),
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.maxpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x


class C16C32C16C8x6FC64(nn.Module):

    def __init__(self, classnum=2):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=5, stride=2, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(32, 16 , kernel_size=3, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(16, 8, kernel_size=3, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(8, 8, kernel_size=3, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(8, 8, kernel_size=3, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(8, 8, kernel_size=3, padding=0),
            nn.ReLU(inplace=True),    
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(8, 8, kernel_size=3, padding=0),
            nn.ReLU(inplace=True),  
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(8, 8, kernel_size=3, padding=0),
            nn.ReLU(inplace=True),       
        )
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=1)
        self.classifier = nn.Sequential(
            nn.Linear(8 * 5 * 5, 64),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(64, classnum),
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.maxpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

class C8x5FC128(nn.Module):

    def __init__(self, classnum=2):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 8, kernel_size=11, stride=1, padding="same"),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=4, stride=1),
            nn.Conv2d(8, 8, kernel_size=7, stride=1, padding="same"),
            nn.ReLU(inplace=True),
            nn.Conv2d(8, 8, kernel_size=5, stride=1, padding="same"),
            nn.ReLU(inplace=True),
            nn.Conv2d(8, 8, kernel_size=5, stride=1, padding="same"),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=1),
            nn.Conv2d(8, 8, kernel_size=3, stride=1, padding="same"),
            nn.ReLU(inplace=True),
        )
        self.maxpool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.classifier = nn.Sequential(
            nn.Linear(8* 73 * 73, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(128, classnum),
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.maxpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

class C8x5FC128V(nn.Module):

    def __init__(self, classnum=2):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 8, kernel_size=11, stride=1, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=4, stride=1),
            nn.Conv2d(8, 8, kernel_size=7, stride=1, padding=0),
            nn.ReLU(inplace=True),
            nn.Conv2d(8, 8, kernel_size=5, stride=1, padding=0),
            nn.ReLU(inplace=True),
            nn.Conv2d(8, 8, kernel_size=5, stride=1, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=1),
            nn.Conv2d(8, 8, kernel_size=3, stride=1, padding=0),
            nn.ReLU(inplace=True),
        )
        self.maxpool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.classifier = nn.Sequential(
            nn.Linear(8* 60 * 60, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(128, classnum),
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.maxpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

class C8x4FC32(nn.Module):

    def __init__(self, classnum=2):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 8, kernel_size=11, stride=1, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=1),
            nn.Conv2d(8, 8, kernel_size=7, stride=1, padding=0),
            nn.ReLU(inplace=True),
            nn.Conv2d(8, 8, kernel_size=5, stride=1, padding=0),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=1),
            nn.Conv2d(8, 8, kernel_size=3, stride=1, padding=0),
            nn.ReLU(inplace=True),
        )
        self.maxpool = nn.MaxPool2d(kernel_size=2, stride=1)
        self.classifier = nn.Sequential(
            nn.Linear(8 * 125 * 125, 32),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(32, classnum),
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.maxpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x