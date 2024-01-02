import os
import lightning as L
import pytest
import numpy as np
import torch
from torch.nn import functional as F
from torch.utils.data import DataLoader, Subset
from torchmetrics import Accuracy
from torchvision import transforms
from torchvision.datasets import MNIST
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from mlops_utils.mlflow_logger.sklearn import Sklearn
from mlops_utils.mlflow_logger.pytorch import Pytorch

sklearn = Sklearn("http://127.0.0.1", 5000)
pytorch = Pytorch("http://127.0.0.1", 5000)

@pytest.mark.asyncio
@sklearn.logger("test_experiment", "test_runner")
def test_runner_sklearn_logging():
    # 주어진 조건 : 유효한 훈련 데이터
    # prepare training data
    noise = np.random.rand(100, 1)
    X = sorted(10 * np.random.rand(100, 1)) + noise
    y = sorted(10 * np.random.rand(100))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

    # train a model
    pipe = Pipeline([("scaler", StandardScaler()), ("lr", LinearRegression())])
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    # 수행 : 학습 결과 그래프 mlflow 기록
    sklearn.post_board(y_test, preds)

    # 기대하는 결과 : mlflow artifacts에 저장

class MNISTModel(L.LightningModule):
    def __init__(self):
        super().__init__()
        self.l1 = torch.nn.Linear(28 * 28, 10)
        self.accuracy = Accuracy("multiclass", num_classes=10)

    def forward(self, x):
        return torch.relu(self.l1(x.view(x.size(0), -1)))

    def training_step(self, batch, batch_nb):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        pred = logits.argmax(dim=1)
        acc = self.accuracy(pred, y)

        # PyTorch `self.log` will be automatically captured by MLflow.
        self.log("train_loss", loss, on_epoch=True)
        self.log("acc", acc, on_epoch=True)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.02)


@pytest.mark.asyncio
@pytorch.logger("test_pytorch", "test_runner")
def test_runner_pytorch_logging():
    # Initialize our model.
    mnist_model = MNISTModel()

    # Load MNIST dataset.
    train_ds = MNIST(
        os.getcwd(), train=True, download=True, transform=transforms.ToTensor()
    )
    # Only take a subset of the data for faster training.
    indices = torch.arange(32)
    train_ds = Subset(train_ds, indices)
    train_loader = DataLoader(train_ds, batch_size=8)

    # Initialize a trainer.
    trainer = L.Trainer(max_epochs=3)
    trainer.fit(mnist_model, train_loader)



