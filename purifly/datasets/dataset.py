import datasets
import datasets.dataset
from purifly.datasets.features import Features

class Dataset(object):
    def __init__(self, features: Features) -> None:
        self._fields = []
        self._data = []