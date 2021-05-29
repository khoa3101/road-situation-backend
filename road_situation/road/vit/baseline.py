import torch
import torch.nn as nn
import torch.nn.functional as F


class Model(nn.Module):
    def __init__(self, extractor, nclasses):
        super().__init__()
        self.nclasses = nclasses
        self.extractor = extractor
        self.feature_dim = self.extractor.feature_dim
        self.classifier = nn.Linear(self.feature_dim, self.nclasses)

    def forward(self, x):
        x = self.extractor(x)
        return self.classifier(x)

