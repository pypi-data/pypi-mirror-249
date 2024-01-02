import mlflow
import numpy as np
import matplotlib.pyplot as plt
from functools import wraps


class Pytorch:
    """
    pytorch version : 1.9.0 <= torch <= 2.1.1
    """
    def __init__(self, url: str, port: int) -> None:
        self.url = url
        self.port = port
    
    def logger(self, experiment_name: str = None, run_name: str = None):
        def logging(func):
            @wraps(func)
            def func_decorator(*args, **kwargs):
                mlflow.set_tracking_uri(uri=self.url + ":" + str(self.port))
                if experiment_name:
                    mlflow.set_experiment(experiment_name)
                mlflow.pytorch.autolog()
                with mlflow.start_run(run_name=run_name) as run:
                    func(*args, **kwargs)
                    print("Logged data and model in run: {}".format(run.info.run_id))
            return func_decorator
        # TODO : plt.figure 이미지 추가
        return logging
