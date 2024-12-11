from abc import ABC, abstractmethod

from loader.classes.abstract_class.info_loader import InfoLoader
from loader.classes.json_class.execution_result.execution_result import ExecutionResult


class ExecutionResultLoader(InfoLoader, ABC):
    def __init__(self, parameters_string:str):
        super().__init__(parameters_string, ExecutionResult)

    @abstractmethod
    def load_info(self) -> ExecutionResult:
        pass


