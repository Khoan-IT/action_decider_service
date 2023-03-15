import torch
from torch import nn

class DQNModel(nn.Module):
    def __init__(self, hidden_size, state_size, num_actions):
        super(DQNModel, self).__init__()
        
        self.hidden_size = hidden_size
        self.state_size = state_size
        self.num_actions = num_actions
        
        self.fc1 = nn.Linear(self.state_size, 256)
        self.fc2 = nn.Linear(256, self.hidden_size)
        self.activation = nn.ReLU()
        self.fc3 = nn.Linear(self.hidden_size, self.num_actions)
    
    def forward(self, x):
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.fc3(x)
        return x
        