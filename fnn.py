import torch
import torchvision
from sklearn.preprocessing import StandardScaler
from torchvision import transforms, datasets
import os
import numpy as np
from tqdm import tqdm

train = datasets.MNIST("", train = True, download=True,
                      transform = transforms.Compose([transforms.ToTensor()]))

test = datasets.MNIST("", train = False, download=True,
                      transform = transforms.Compose([transforms.ToTensor()]))

trainset = torch.utils.data.DataLoader(train, batch_size=10, shuffle=True)
testset = torch.utils.data.DataLoader(test, batch_size=10, shuffle=True)

import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10000, 7000)
        self.fc2 = nn.Linear(7000, 1000)
        self.fc3 = nn.Linear(1000, 7000)
        self.fc4 = nn.Linear(7000, 1000)
        self.fc5 = nn.Linear(1000, 3)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = self.fc5(x)
        return F.log_softmax(x,dim=1)

net = torch.load("net.pth")
net.eval()
# net = Net()


training_data = np.load("training_data.npy", allow_pickle = True)
print(len(training_data[7][0]))

import torch.optim as optim

optimizer = optim.Adam(net.parameters(), lr=0.001)
loss_function = nn.MSELoss()
scaler = StandardScaler()

X = torch.Tensor([i[0] for i in training_data]).view(-1,  10000)

Y = torch.Tensor([i[1] for i in training_data])

VAL_PCT = 0.1
val_size = int(len(X) * VAL_PCT)

train_X = X[:-val_size]
train_Y = Y[:-val_size]

test_X = X[-val_size:]
test_Y = Y[-val_size:]

BATCH_SIZE = 50
EPOCHS = 10

if(True):
    
    FILE = open("NetRez", "w")
    for epoch in range(EPOCHS):
        for i in tqdm(range(0, len(train_X), BATCH_SIZE), position=0, leave=True):
            batch_X = train_X[i:i+BATCH_SIZE].view(-1, 10000)
            batch_Y = train_Y[i:i+BATCH_SIZE]
            
            net.zero_grad()
            outputs = net(batch_X)
            loss = loss_function(outputs, batch_Y)
            loss.backward()
            optimizer.step()
        
        print(loss)
        correct = 0
        total = 0
        FILE = open("NetRez", "a")
        with torch.no_grad():
            for i in tqdm(range(len(test_X)),  position=0, leave=True):
                real_class = torch.argmax(test_Y[i])
                net_out = net(test_X[i].view(-1, 1, 10000))[0]
                predicted_class = torch.argmax(net_out)
                if predicted_class == real_class:
                    correct += 1
                total +=1
        FILE.write("Accuracy " + str(round(correct/total,3)))
        FILE.close()


torch.save(net, "net.pth")


