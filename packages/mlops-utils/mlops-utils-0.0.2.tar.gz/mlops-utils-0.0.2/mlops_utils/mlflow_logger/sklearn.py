import os
import mlflow
import numpy as np
import matplotlib.pyplot as plt
from functools import wraps


class Sklearn:
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
                mlflow.sklearn.autolog()
                with mlflow.start_run(run_name=run_name) as run:
                    func(*args, **kwargs)
                    print("Logged data and model in run: {}".format(run.info.run_id))
            return func_decorator
        return logging
    
    @staticmethod
    def post_board(y_test: np.ndarray, preds: np.ndarray):
        scatter_file = "scatter_plot.png"
        plt.scatter(y_test, preds)
        plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', linewidth=2, label="y=x")
        plt.xlabel("Actual values")
        plt.ylabel("Predicted values")
        plt.savefig(scatter_file)
        
        mlflow.log_artifact(scatter_file, artifact_path="plots")
        
        if os.path.exists(scatter_file):
            os.remove(scatter_file)
        
