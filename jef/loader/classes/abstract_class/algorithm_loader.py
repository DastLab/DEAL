from abc import ABC, abstractmethod

from loader.classes.abstract_class.info_loader import InfoLoader
from loader.classes.json_class.algorithm.algorithm import Algorithm


class AlgorithmLoader(InfoLoader, ABC):
    def __init__(self, parameters_string:str):
        super().__init__(parameters_string, Algorithm)

    @abstractmethod
    def load_info(self) -> Algorithm:
        pass


