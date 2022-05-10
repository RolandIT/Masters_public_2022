import dataset
import models
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torch.optim as optim
import wandb
import numpy as np
from tqdm import tqdm
import os
import sklearn.metrics as metrics
import inspect
import sys


def get_model_names():
    model_names = []
    classmembers = inspect.getmembers(sys.modules[models.__name__], inspect.isclass)
    for r in classmembers:
        model_names.append(r[0])
    return model_names


def split_dataset(dataset, l=0.2, h=0.8):
    data_len = len(dataset)
    high = int(data_len * h)
    low = int(data_len * l)

    if high + low < data_len:
        high += 1

    return torch.utils.data.random_split(dataset, [high, low])

def validation(model, valloader, loss_fnc):

    val_loss =  0.0
    truth = np.array([])
    predicted = np.array([])

    # with torch.no_grad():
    for i, data in enumerate(valloader):
        images, labels = data
        images = images.to(device)
        images = images.float()
        images = torch.transpose(images, 1, 3)
        labels = labels.to(device)
        output = model(images)

        l = loss_fnc(output, labels)
        val_loss = l.item()
        predictions = torch.argmax(output, -1)

        labels = labels.cpu()
        predictions = predictions.cpu()
        truth = np.append(truth, labels.numpy())
        predicted = np.append(predicted, predictions.numpy())

    f1score = 100 * metrics.f1_score(truth, predicted, average='weighted')
    acc = 100 * metrics.accuracy_score(truth, predicted)
    tn, fp, fn, tp = metrics.confusion_matrix(truth, predicted).ravel()
    false_positive = fp / (fp + tn)
    false_negative = fn / (tp + fn)
    true_positive = tp / (tp + fn)
    true_negative = tn / (tn + fp)

    return f1score, acc, val_loss, false_positive, false_negative, true_positive, true_negative

def train(EPOCH, model, trainloader, valloader, testloader, optimizer, loss_fnc, early_s_param):
    min_val_loss = np.inf
    for x in range(EPOCH):
        r_loss = 0.0
        val_loss = 0.0
        no_val_loss_change = 0
        with tqdm(enumerate(trainloader), unit='Batch') as tbatch:
            for i, data in tbatch:
                tbatch.set_description(f"Epoch {x}")
                images, labels = data
                images = images.to(device)
                images = images.float()
                images = torch.transpose(images, 1, 3)
                labels = labels.to(device)

                optimizer.zero_grad()

                outputs = model(images)
                loss = loss_fnc(outputs, labels)
                loss.backward()
                optimizer.step()

                r_loss += loss.item()
                
                if i % 100 == 0 and i!=0:    
                    f1score, acc, val_loss, false_positive, false_negative, true_positive, true_negative = validation(model, valloader, loss_fnc)
                    wandb.log({"loss": r_loss/100})
                    wandb.log({"acc": acc})
                    wandb.log({"f1_score": f1score})
                    wandb.log({"false_positive_rate": false_positive})
                    wandb.log({"true_positive_rate": true_positive})
                    wandb.log({"false_negative_rate": false_negative})
                    wandb.log({"true_negative_rate": true_negative})
                    wandb.log({"val_loss": val_loss})
                    r_loss = 0.0
                    no_val_loss_change +=1
                    if min_val_loss > val_loss:
                        no_val_loss_change = 0
                        print('Validation Loss Decreased')
                        min_val_loss = val_loss
                        torch.save(model.state_dict(), cwd + '/Trained_models/' + type(model).__name__ + '.pth')
                        
                    if no_val_loss_change >= early_s_param:
                        
                        truth = np.array([])
                        predicted = np.array([])

                        with torch.no_grad():
                            for i, data in enumerate(testloader):
                                images, labels = data
                                images = images.to(device)
                                images = images.float()
                                images = torch.transpose(images, 1, 3)
                                labels = labels.to(device)
                                output = model(images)

                                l = loss_fnc(output, labels)
                                val_loss = l.item()
                                predictions = torch.argmax(output, -1)

                                labels = labels.cpu()
                                predictions = predictions.cpu()
                                truth = np.append(truth, labels.numpy())
                                predicted = np.append(predicted, predictions.numpy())

                        wandb.log({"conf_mat" : wandb.plot.confusion_matrix(probs=None,
                        y_true=truth, preds=predicted,
                        class_names=["Empty" , "Occupied"])})
                        wandb.finish()
                        return

                tbatch.set_postfix(loss=loss.item(), val_loss=val_loss)



cwd = os.getcwd()
dir = 'C:/Users/rolan/OneDrive/Documents/STU FIIT/Masters thesis/PKLot+EXT_Dataset'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("Device currently used: ", device)

labels_file = open(dir + '/labels.csv', 'r')
dat = dataset.TrainingDataset(labels_file, dir, dataset.imResize)
train_data, test_data = split_dataset(dat)
train_data, val_data = split_dataset(train_data, l=0.01, h=0.99)

EPOCH = 10
batch_size = 64
early_s_param = 10

learning_rates = [0.01, 0.001]
loss_fncs = [torch.nn.CrossEntropyLoss]
optimizers = [optim.Adam, optim.Adagrad, optim.SGD]

trainloader = DataLoader(dataset=train_data, batch_size=batch_size, shuffle=True)
valloader = DataLoader(dataset=val_data, batch_size=batch_size, shuffle=True)
testloader = DataLoader(dataset=test_data, batch_size=batch_size, shuffle=True)

model_names = get_model_names()
for lr in learning_rates:
    for loss_fnc in loss_fncs:
        for o in optimizers:
            for m in model_names:
                model_class = getattr(models, m)(2)
                model = model_class.to(device)
                optimizer = o(model.parameters(), lr=lr)
                config = dict(
                    learning_rate = lr,
                    model = model,
                    optimizer = o,
                    loss_fnc = loss_fnc,
                )
                run = wandb.init(project='masters_thesis', entity='rolands', config=config)
                wandb.watch(model)
                train(EPOCH, model, trainloader, valloader,testloader, optimizer, loss_fnc(), early_s_param)


model = models.C16C32C64C128C64C16FC256(2).to(device)
o = optimizers[2](model.parameters(), lr=0.01)
config = dict(
    learning_rate = 0.01,
    model = model,
    optimizer = o,
    loss_fnc = loss_fncs[0],
)
run = wandb.init(project='masters_thesis', entity='rolands', config=config)
wandb.watch(model)
train(EPOCH, model, trainloader, valloader,testloader, o, loss_fncs[0](), early_s_param)
