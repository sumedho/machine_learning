from joblib import load
import pandas as pd
import numpy as np
import sys
from threading import Thread

class Model:
    def __init__(self, file_name):
        def get_last_column(X):
            return X[:, -1].reshape(-1, 1)

        setattr(sys.modules['__main__'], 'get_last_column', get_last_column)

        self.__file_name = file_name
        self.__is_ready = False
        self.__model = None
        self.__meta_data = None

    def __load_model(self):
        loaded = load(self.__file_name)
        self.__model = loaded['model']
        self.__meta_data = loaded['metadata']
        self.__is_ready = True

    def load_model(self):
        Thread(target=self.__load_model).start()

    def is_ready(self):
        return self.__is_ready

    def predict(self, features):
        if not self.is_ready():
            raise RuntimeError('Model is not ready yet.')

        input = np.asarray(features).reshape(1, -1)
        result = self.__model.predict(input)
        return int(result[0])