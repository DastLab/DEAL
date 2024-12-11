from abc import ABC
import json
from loader.classes.abstract_class.execution_result_loader import ExecutionResultLoader
from loader.classes.json_class.execution_result.execution_result import ExecutionResult


class DefaultJSONExecutionResultLoader(ExecutionResultLoader, ABC):
    file_path_key='file_path'
    def __init__(self, parameters_string: str):
        super().__init__(parameters_string)

    def load_info(self):
        with open(self.parameters[self.file_path_key], 'r') as file:
            data = json.load(file)
            return ExecutionResult(**data)