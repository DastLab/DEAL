from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
class InfoLoader(ABC,Generic[T]):
    parameters_string:str
    return_info:T
    parameters:dict

    def __init__(self, parameters_string:str, return_info:type[T]):
        self.parameters_string = parameters_string
        self.return_info = return_info
        self._load_parameters_dict()

    def _load_parameters_dict(self):
        self.parameters = {}
        p=self.parameters_string.split(',')
        for e in p:
            splitted=e.split(':')
            self.parameters[splitted[0]]=splitted[1]

    @abstractmethod
    def load_info(self) -> T:
        pass

