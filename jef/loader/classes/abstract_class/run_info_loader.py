from abc import ABC, abstractmethod

from loader.classes.abstract_class.info_loader import InfoLoader
from loader.classes.json_class.run_info.run_info import RunInfo


class RunInfoLoader(InfoLoader, ABC):
    def __init__(self, parameters_string:str):
        super().__init__(parameters_string, RunInfo)

    @abstractmethod
    def load_info(self) -> RunInfo:
        pass


