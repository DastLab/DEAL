from abc import ABC, abstractmethod

from loader.classes.abstract_class.info_loader import InfoLoader
from loader.classes.json_class.dataset.dataset import Dataset


class DatasetLoader(InfoLoader, ABC):
    def __init__(self, parameters_string:str):
        super().__init__(parameters_string, Dataset)

    @abstractmethod
    def load_info(self) -> Dataset:
        pass


