from abc import ABC, abstractmethod

from loader.classes.abstract_class.info_loader import InfoLoader


class ExtraDataLoader(InfoLoader, ABC):
    def __init__(self, parameters_string:str):
        super().__init__(parameters_string, dict)

    @abstractmethod
    def load_info(self) -> dict:
        pass


